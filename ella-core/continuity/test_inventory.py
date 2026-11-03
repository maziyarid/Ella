"""Tests for inventory.py. Every tree here is invented in a temporary directory; nothing touches /home/ella."""
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

import inventory

HERE = Path(__file__).resolve().parent
MARKER = "SYNTHETIC-CONTENT-MUST-NOT-APPEAR-7f3a"
SECRET_NAME = "invented-private-name-q9"


def sha(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


class Tree:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / "home-ella"
        (self.base / "memory" / "notebook").mkdir(parents=True)
        (self.base / "diary").mkdir()
        (self.base / "memory" / "MEMORY.md").write_bytes(f"# {MARKER}\n".encode())
        (self.base / "memory" / "notebook" / f"{SECRET_NAME}.jsonl").write_bytes(f'{{"x":"{MARKER}"}}\n'.encode())
        (self.base / "diary" / "2026-01-01.jsonl").write_bytes(b"")
        (self.root / "outside.txt").write_bytes(f"OUTSIDE {MARKER}\n".encode())
        (self.base / "unrelated.txt").write_bytes(b"not a target\n")

    def scan(self):
        return inventory.scan(str(self.base))

    def close(self):
        for dirpath, dirnames, _ in os.walk(self.root):
            for d in dirnames:
                try:
                    os.chmod(os.path.join(dirpath, d), 0o700, follow_symlinks=False)
                except (OSError, NotImplementedError):
                    pass
        self.tmp.cleanup()


def by_rel(inv):
    return {(e["target"], e["rel"]): e for e in inv["entries"]}


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.t = Tree()

    def tearDown(self):
        self.t.close()

    def test_normal_tree_sizes_and_hashes_from_bytes(self):
        inv = self.t.scan()
        self.assertEqual(inv["base_status"], "ok")
        self.assertEqual([x["status"] for x in inv["targets"]], ["present", "present"])
        rows = by_rel(inv)
        m = rows[("memory", "MEMORY.md")]
        data = (self.t.base / "memory" / "MEMORY.md").read_bytes()
        self.assertEqual((m["status"], m["size"], m["sha256"]), ("ok", len(data), sha(data)))
        self.assertEqual(rows[("diary", "2026-01-01.jsonl")]["sha256"], sha(b""))
        self.assertEqual(rows[("memory", "notebook")]["type"], "dir")

    def test_only_the_two_targets_are_inspected(self):
        inv = self.t.scan()
        self.assertEqual({e["target"] for e in inv["entries"]}, {"memory", "diary"})
        self.assertNotIn("unrelated.txt", json.dumps(inv))

    def test_missing_diary_is_reported_explicitly(self):
        (self.t.base / "diary" / "2026-01-01.jsonl").unlink()
        (self.t.base / "diary").rmdir()
        inv = self.t.scan()
        self.assertEqual({x["target"]: x["status"] for x in inv["targets"]}, {"memory": "present", "diary": "missing"})

    def test_missing_base(self):
        inv = inventory.scan(str(self.t.root / "nope"))
        self.assertEqual(inv["base_status"], "missing")
        self.assertEqual([x["status"] for x in inv["targets"]], ["missing_parent", "missing_parent"])

    def test_base_symlink_refused(self):
        link = self.t.root / "link-home"
        link.symlink_to(self.t.base)
        inv = inventory.scan(str(link))
        self.assertEqual(inv["base_status"], "symlink_refused")
        self.assertEqual(inv["entries"], [])

    def test_target_symlink_refused_and_not_followed(self):
        real = self.t.root / "elsewhere"
        real.mkdir()
        (real / "x.jsonl").write_bytes(MARKER.encode())
        (self.t.base / "diary" / "2026-01-01.jsonl").unlink()
        (self.t.base / "diary").rmdir()
        (self.t.base / "diary").symlink_to(real)
        inv = self.t.scan()
        self.assertEqual({x["target"]: x["status"] for x in inv["targets"]}["diary"], "symlink_refused")
        self.assertFalse(any(e["target"] == "diary" for e in inv["entries"]))

    def test_target_not_a_directory(self):
        (self.t.base / "diary" / "2026-01-01.jsonl").unlink()
        (self.t.base / "diary").rmdir()
        (self.t.base / "diary").write_bytes(b"x")
        inv = self.t.scan()
        self.assertEqual({x["target"]: x["status"] for x in inv["targets"]}["diary"], "not_a_directory")

    def test_inner_symlinks_to_file_and_dir_are_not_followed(self):
        (self.t.base / "memory" / "lnk").symlink_to(self.t.root / "outside.txt")
        (self.t.base / "memory" / "dlnk").symlink_to(self.t.root)
        with mock.patch.object(inventory.os, "readlink", side_effect=AssertionError("readlink called")):
            inv = self.t.scan()
        rows = by_rel(inv)
        for rel in ("lnk", "dlnk"):
            self.assertEqual((rows[("memory", rel)]["type"], rows[("memory", rel)]["status"]), ("symlink", "not_followed"))
            self.assertNotIn("sha256", rows[("memory", rel)])
        self.assertFalse(any(r[1].startswith("dlnk/") for r in rows))
        self.assertNotIn("outside", json.dumps(inv))

    def test_fifo_and_socket_are_not_opened(self):
        os.mkfifo(self.t.base / "memory" / "pipe")
        s = socket.socket(socket.AF_UNIX)
        sock_path = self.t.base / "diary" / "s"
        try:
            s.bind(str(sock_path))
        except OSError:
            sock_path = None
        try:
            inv = self.t.scan()   # a FIFO opened without O_NONBLOCK, or opened at all, could hang here
        finally:
            s.close()
        rows = by_rel(inv)
        self.assertEqual(rows[("memory", "pipe")]["status"], "not_opened")
        if sock_path:
            self.assertEqual(rows[("diary", "s")]["status"], "not_opened")

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root bypasses permissions")
    def test_unreadable_file_and_directory_are_reported(self):
        f = self.t.base / "memory" / "MEMORY.md"
        f.chmod(0o000)
        d = self.t.base / "memory" / "notebook"
        d.chmod(0o000)
        try:
            inv = self.t.scan()
        finally:
            f.chmod(0o600)
            d.chmod(0o700)
        rows = by_rel(inv)
        self.assertEqual(rows[("memory", "MEMORY.md")]["status"], "not_readable")
        self.assertNotIn("sha256", rows[("memory", "MEMORY.md")])
        self.assertEqual(rows[("memory", "notebook")]["status"], "not_accessible")

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root bypasses permissions")
    def test_inaccessible_target(self):
        (self.t.base / "memory").chmod(0o000)
        try:
            inv = self.t.scan()
        finally:
            (self.t.base / "memory").chmod(0o700)
        self.assertEqual({x["target"]: x["status"] for x in inv["targets"]}["memory"], "not_accessible")

    def test_hardlink_count_reported(self):
        os.link(self.t.root / "outside.txt", self.t.base / "memory" / "hl")
        rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "hl")]["nlink"], 2)

    def test_change_during_read_detected(self):
        target = self.t.base / "memory" / "MEMORY.md"
        real = inventory._hash_fd

        def growing(fd):
            with open(target, "ab") as fh:
                fh.write(b"more\n")
            return real(fd)
        with mock.patch.object(inventory, "_hash_fd", growing):
            rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "MEMORY.md")]["status"], "changed_during_read")

    def test_no_content_ever_in_inventory_or_summary(self):
        inv = self.t.scan()
        blob = json.dumps(inv)
        self.assertNotIn(MARKER, blob)
        summary = inventory.summarize(inv, blob.encode())
        s = json.dumps(summary)
        self.assertNotIn(MARKER, s)
        for leak in (SECRET_NAME, "MEMORY", "notebook", "2026-01-01", str(self.t.base), "generated_at"):
            self.assertNotIn(leak, s)
        self.assertNotRegex(s, r"sha256:[0-9a-f]{64}\"\s*,\s*\"size")

    def test_summary_shape_and_aggregate_hash(self):
        inv = self.t.scan()
        raw = json.dumps(inv).encode()
        s = inventory.summarize(inv, raw)
        self.assertEqual(s["private_inventory_sha256"], sha(raw))
        mem = s["targets"]["memory"]
        self.assertEqual(mem["counts"]["file"], 2)
        self.assertEqual(mem["counts"]["dir"], 1)
        self.assertEqual(mem["extensions"], {".jsonl": 1, ".md": 1})
        self.assertEqual(s["targets"]["diary"]["size_buckets"], {"0": 1})
        again = inventory.summarize(self.t.scan(), raw)
        self.assertEqual(again["targets"], s["targets"])
        (self.t.base / "diary" / "2026-01-01.jsonl").write_bytes(b"changed\n")
        changed = inventory.summarize(self.t.scan(), raw)
        self.assertNotEqual(changed["targets"]["diary"]["aggregate_sha256"], s["targets"]["diary"]["aggregate_sha256"])

    def test_scan_writes_nothing_and_opens_no_network(self):
        before = {p: p.stat().st_mtime_ns for p in self.t.root.rglob("*")}
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess")):
            self.t.scan()
        after = {p: p.stat().st_mtime_ns for p in self.t.root.rglob("*")}
        self.assertEqual(before, after)

    def test_output_inside_target_refused(self):
        out = self.t.base / "diary" / "inv.json"
        with open(out, "w") as fh:
            st = os.fstat(fh.fileno())
            with self.assertRaises(inventory.OutputInsideTarget):
                inventory.scan(str(self.t.base), (st.st_dev, st.st_ino))

    def test_cli_scan_uses_fixed_base_and_refuses_output_inside(self):
        out = self.t.base / "memory" / "inv.json"
        code = (f"import sys,inventory; inventory.BASE={str(self.t.base)!r}; sys.exit(inventory.main(['scan']))")
        with open(out, "w") as fh:
            r = subprocess.run([sys.executable, "-B", "-c", code], cwd=HERE, stdout=fh, stderr=subprocess.PIPE, text=True)
        self.assertEqual(r.returncode, 3)
        self.assertIn("refused", r.stderr)
        self.assertEqual(out.read_bytes(), b"")

    def test_cli_round_trip_in_fresh_process(self):
        priv = self.t.root / "private.json"
        code = (f"import sys,inventory; inventory.BASE={str(self.t.base)!r}; sys.exit(inventory.main(['scan']))")
        with open(priv, "w") as fh:
            r = subprocess.run([sys.executable, "-B", "-c", code], cwd=HERE, stdout=fh, stderr=subprocess.PIPE, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        r2 = subprocess.run([sys.executable, "-B", "inventory.py", "summarize", str(priv)], cwd=HERE,
                            capture_output=True, text=True)
        self.assertEqual(r2.returncode, 0, r2.stderr)
        self.assertNotIn(MARKER, r.stderr + r2.stdout)
        self.assertNotIn(SECRET_NAME, r2.stdout)
        self.assertEqual(json.loads(r2.stdout)["private_inventory_sha256"], sha(priv.read_bytes()))

    def test_default_base_is_fixed(self):
        self.assertEqual(inventory.BASE, "/home/ella")
        self.assertEqual(inventory.TARGETS, ("memory", "diary"))
        with redirect_stderr(io.StringIO()):
            self.assertEqual(inventory.main(["scan", "/tmp"]), 2)


if __name__ == "__main__":
    unittest.main()
