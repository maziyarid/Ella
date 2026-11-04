"""Tests for inventory.py. Every tree here is invented in a temporary directory; nothing touches /home/ella."""
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
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

    def test_non_utf8_name_is_marked_and_json_stays_valid(self):
        raw = os.path.join(os.fsencode(self.t.base / "diary"), b"inv-\xff\xfe.jsonl")
        with open(raw, "wb") as fh:
            fh.write(MARKER.encode())
        inv = self.t.scan()
        odd = [e for e in inv["entries"] if e.get("name_not_utf8")]
        self.assertEqual(len(odd), 1)
        text = json.dumps(inv, ensure_ascii=False)
        text.encode("utf-8")  # must not raise
        self.assertNotIn(MARKER, text)
        buf = io.StringIO()
        with mock.patch.object(inventory, "BASE", str(self.t.base)), mock.patch.object(sys, "stdout", buf), \
                redirect_stderr(io.StringIO()):
            self.assertEqual(inventory.main(["scan"]), 0)
        json.loads(buf.getvalue())

    def test_depth_limit_reported_not_descended(self):
        d = self.t.base / "memory"
        for i in range(inventory.MAX_DEPTH + 3):
            d = d / f"d{i}"
        d.mkdir(parents=True)
        (d / "deep.txt").write_bytes(MARKER.encode())
        inv = self.t.scan()
        self.assertIn("depth_limit_not_descended", [e["status"] for e in inv["entries"]])
        self.assertFalse(any(e["rel"].endswith("deep.txt") for e in inv["entries"]))
        self.assertLessEqual(max(e["depth"] for e in inv["entries"]), inventory.MAX_DEPTH)

    def test_file_swapped_for_fifo_between_stat_and_open(self):
        target = self.t.base / "memory" / "MEMORY.md"
        real_open = inventory.os.open

        def swapping_open(path, flags, *a, **k):
            if path == "MEMORY.md" and not flags & os.O_DIRECTORY:
                target.unlink()
                os.mkfifo(target)
            return real_open(path, flags, *a, **k)
        with mock.patch.object(inventory.os, "open", swapping_open):
            rows = by_rel(self.t.scan())   # O_NONBLOCK: opening the FIFO does not hang
        self.assertEqual(rows[("memory", "MEMORY.md")]["status"], "replaced_during_scan")
        self.assertNotIn("sha256", rows[("memory", "MEMORY.md")])

    def test_file_swapped_for_symlink_between_stat_and_open(self):
        target = self.t.base / "memory" / "MEMORY.md"
        real_open = inventory.os.open

        def swapping_open(path, flags, *a, **k):
            if path == "MEMORY.md" and not flags & os.O_DIRECTORY:
                target.unlink()
                target.symlink_to(self.t.root / "outside.txt")
            return real_open(path, flags, *a, **k)
        with mock.patch.object(inventory.os, "open", swapping_open):
            rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "MEMORY.md")]["status"], "not_readable")   # ELOOP from O_NOFOLLOW
        self.assertNotIn("sha256", rows[("memory", "MEMORY.md")])

    def test_directory_swapped_between_stat_and_open(self):
        sub = self.t.base / "memory" / "notebook"
        real_open = inventory.os.open

        def swapping_open(path, flags, *a, **k):
            if path == "notebook" and flags & os.O_DIRECTORY:
                sub.rename(self.t.base / "memory" / "moved")
                sub.mkdir()
            return real_open(path, flags, *a, **k)
        with mock.patch.object(inventory.os, "open", swapping_open):
            rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "notebook")]["status"], "replaced_during_scan")

    def test_target_swapped_for_symlink_between_stat_and_open(self):
        real_open = inventory.os.open
        diary = self.t.base / "diary"

        def swapping_open(path, flags, *a, **k):
            if path == "diary":
                diary.rename(self.t.root / "old-diary")
                diary.symlink_to(self.t.root / "old-diary")
            return real_open(path, flags, *a, **k)
        with mock.patch.object(inventory.os, "open", swapping_open):
            inv = self.t.scan()
        self.assertEqual({x["target"]: x["status"] for x in inv["targets"]}["diary"], "not_accessible")
        self.assertFalse(any(e["target"] == "diary" for e in inv["entries"]))

    def test_metadata_change_during_read_detected(self):
        target = self.t.base / "memory" / "MEMORY.md"
        real = inventory._hash_fd

        def chmod_then_read(fd):
            time.sleep(0.03)               # cross the filesystem timestamp tick (4 ms on the test ext4)
            os.chmod(target, 0o640)        # ctime changes; size and mtime do not
            return real(fd)
        with mock.patch.object(inventory, "_hash_fd", chmod_then_read):
            rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "MEMORY.md")]["status"], "changed_during_read")

    def test_summary_vocabulary_is_closed(self):
        os.mkfifo(self.t.base / "memory" / SECRET_NAME)
        (self.t.base / "memory" / f"{SECRET_NAME}.weird-ext").write_bytes(b"x")
        inv = self.t.scan()
        s = inventory.summarize(inv, json.dumps(inv).encode())
        flat = json.dumps(s)
        self.assertNotIn(SECRET_NAME, flat)
        self.assertNotIn("weird", flat)
        allowed = set(inventory.EXT_BUCKETS) | {"(none)", "(other)"}
        for t in s["targets"].values():
            self.assertLessEqual(set(t["extensions"]), allowed)

    def test_compare_two_scans_counts_only(self):
        a = self.t.scan()
        (self.t.base / "diary" / "2026-01-01.jsonl").write_bytes(b"same-size?")
        (self.t.base / "memory" / f"{SECRET_NAME}-new.md").write_bytes(b"n")
        (self.t.base / "memory" / "MEMORY.md").unlink()
        b = self.t.scan()
        c = inventory.compare(a, b)
        self.assertEqual(c["files_changed"], 1)
        self.assertEqual(c["files_added"], 1)
        self.assertEqual(c["files_removed"], 1)
        self.assertFalse(c["identical"])
        self.assertNotIn(SECRET_NAME, json.dumps(c))
        self.assertTrue(inventory.compare(b, self.t.scan())["identical"])

    def test_other_filesystem_is_not_entered(self):
        real_stat = inventory.os.stat

        def fake_stat(path, *a, **k):
            st = real_stat(path, *a, **k)
            if path == "notebook":
                vals = list(st)
                vals[2] = st.st_dev + 1          # st_dev
                return os.stat_result(vals)
            return st
        with mock.patch.object(inventory.os, "stat", fake_stat):
            rows = by_rel(self.t.scan())
        self.assertEqual(rows[("memory", "notebook")]["status"], "other_filesystem_not_entered")
        self.assertFalse(any(r[1].startswith("notebook/") for r in rows))

    def test_file_open_flags(self):
        for flag in (os.O_NOFOLLOW, os.O_NONBLOCK, os.O_NOCTTY):
            self.assertTrue(inventory.O_FILE & flag)
        self.assertFalse(inventory.O_FILE & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))

    def test_default_base_is_fixed(self):
        self.assertEqual(inventory.BASE, "/home/ella")
        self.assertEqual(inventory.TARGETS, ("memory", "diary"))
        with redirect_stderr(io.StringIO()):
            self.assertEqual(inventory.main(["scan", "/tmp"]), 2)


if __name__ == "__main__":
    unittest.main()
