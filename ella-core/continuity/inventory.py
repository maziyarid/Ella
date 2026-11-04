#!/usr/bin/env python3
"""Ella memory-layout inventory v0.1 — local, read-only, for Maziyar to review and run.

Subcommands:

  scan       Inspects exactly /home/ella/memory and /home/ella/diary. Prints a PRIVATE
             inventory (relative paths, types, sizes, sha256) as JSON on stdout.
             Never prints file contents. Never follows symlinks. Never writes a file.
  summarize  Reads a private inventory file and prints a SANITIZED summary
             (counts, size buckets, extension counts, aggregate hashes). No names,
             no paths, no per-file hashes, no times.
  compare    Compares two private inventories and prints counts only (changed, added,
             removed). Run scan twice to catch changes that timestamps can miss.

The private inventory stays on the PC. Only the summary is meant to be shared, after review.
This script has no network code, starts nothing and writes nothing. The caller's shell
redirect is the only thing that creates a file.

Suggested use (see LIVE_INVENTORY_PROCEDURE.md):
    set -C; umask 077; D=~/ella-inventory-$(date -u +%Y%m%dT%H%M%SZ); mkdir -m 700 "$D"
    sudo -u ella python3 -I -B - scan < inventory.py > "$D/inventory.json"
    python3 -I -B inventory.py summarize "$D/inventory.json" > "$D/summary.json"
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from datetime import datetime, timezone

VERSION = "0.1.0"
BASE = "/home/ella"                 # fixed; there is no option to point this elsewhere
TARGETS = ("memory", "diary")        # the only directories inspected
CHUNK = 1 << 20
MAX_DEPTH = 32                       # deeper directories are reported, not descended
EXT_BUCKETS = (".md", ".jsonl", ".json", ".txt", ".log", ".db", ".sqlite", ".sqlite3", ".yaml", ".yml", ".csv", ".gpg")
SIZE_BUCKETS = ((0, "0"), (1024, "<1KiB"), (64 * 1024, "<64KiB"), (1024 * 1024, "<1MiB"),
                (16 * 1024 * 1024, "<16MiB"))

O_DIR = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
O_FILE = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOCTTY | getattr(os, "O_CLOEXEC", 0)


class OutputInsideTarget(Exception):
    pass


def _kind(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "special"


def _hash_fd(fd: int):
    h, n = hashlib.sha256(), 0
    while True:
        b = os.read(fd, CHUNK)
        if not b:
            break
        h.update(b)
        n += len(b)
    return "sha256:" + h.hexdigest(), n


def _safe_name(name: str) -> tuple[str, bool]:
    """Names are str with surrogate escapes for undecodable bytes. Keep JSON valid and mark such names."""
    try:
        name.encode("utf-8")
        return name, False
    except UnicodeEncodeError:
        return os.fsencode(name).decode("utf-8", "backslashreplace"), True


def _same(st_a, st_b) -> bool:
    return (st_a.st_dev, st_a.st_ino) == (st_b.st_dev, st_b.st_ino)


def _scan_dir(dfd: int, rel: str, target: str, out_ident, entries: list, depth: int, dev: int):
    try:
        names = sorted(os.listdir(dfd))
    except OSError as exc:
        entries.append({"target": target, "rel": rel or ".", "type": "dir", "status": "not_listable",
                        "error": type(exc).__name__})
        return
    for name in names:
        shown, odd = _safe_name(name)
        child = f"{rel}/{shown}" if rel else shown
        try:
            st = os.stat(name, dir_fd=dfd, follow_symlinks=False)
        except OSError as exc:
            entries.append({"target": target, "rel": child, "type": "unknown", "status": "not_stat_able",
                            "error": type(exc).__name__})
            continue
        if out_ident and (st.st_dev, st.st_ino) == out_ident:
            raise OutputInsideTarget(f"{target}/{child}")
        kind = _kind(st.st_mode)
        row = {"target": target, "rel": child, "type": kind, "depth": depth + 1}
        if odd:
            row["name_not_utf8"] = True
        if kind == "symlink":
            row["status"] = "not_followed"          # the link target is never read or resolved
        elif kind == "special":
            row["status"] = "not_opened"            # fifo, socket or device: never opened
        elif st.st_dev != dev:
            row["status"] = "other_filesystem_not_entered"   # mount point or bind-mounted file
        elif kind == "dir":
            if depth + 1 >= MAX_DEPTH:
                row["status"] = "depth_limit_not_descended"
                entries.append(row)
                continue
            try:
                cfd = os.open(name, O_DIR, dir_fd=dfd)
            except OSError as exc:
                row.update(status="not_accessible", error=type(exc).__name__)
                entries.append(row)
                continue
            try:
                if not _same(os.fstat(cfd), st):
                    row["status"] = "replaced_during_scan"
                    entries.append(row)
                    continue
                row["status"] = "ok"
                entries.append(row)
                _scan_dir(cfd, child, target, out_ident, entries, depth + 1, dev)
            finally:
                os.close(cfd)
            continue
        else:
            try:
                fd = os.open(name, O_FILE, dir_fd=dfd)
            except OSError as exc:
                row.update(status="not_readable", size=st.st_size, error=type(exc).__name__)
                entries.append(row)
                continue
            try:
                before = os.fstat(fd)
                if not stat.S_ISREG(before.st_mode) or not _same(before, st):
                    row.update(status="replaced_during_scan")
                else:
                    digest, n = _hash_fd(fd)
                    after = os.fstat(fd)
                    changed = (n != before.st_size or after.st_size != before.st_size
                               or after.st_mtime_ns != before.st_mtime_ns
                               or after.st_ctime_ns != before.st_ctime_ns)
                    row.update(status="changed_during_read" if changed else "ok", size=n, sha256=digest,
                               nlink=before.st_nlink)
            except OSError as exc:
                row.update(status="not_readable", error=type(exc).__name__)
            finally:
                os.close(fd)
        entries.append(row)


def _stdout_ident():
    try:
        st = os.fstat(sys.stdout.fileno())
        return (st.st_dev, st.st_ino) if stat.S_ISREG(st.st_mode) else None
    except (OSError, ValueError, AttributeError):
        return None


def scan(base: str = BASE, out_ident=None) -> dict:
    report = {"tool": "ella-memory-inventory", "version": VERSION, "kind": "PRIVATE — do not share or upload",
              "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "base": base, "targets": [], "entries": []}
    try:
        bst = os.stat(base, follow_symlinks=False)
    except FileNotFoundError:
        report["base_status"] = "missing"
        report["targets"] = [{"target": t, "status": "missing_parent"} for t in TARGETS]
        return report
    except OSError as exc:
        report["base_status"] = f"not_accessible:{type(exc).__name__}"
        report["targets"] = [{"target": t, "status": "not_accessible_parent"} for t in TARGETS]
        return report
    if stat.S_ISLNK(bst.st_mode):
        report["base_status"] = "symlink_refused"
        report["targets"] = [{"target": t, "status": "parent_is_symlink_refused"} for t in TARGETS]
        return report
    try:
        bfd = os.open(base, O_DIR)
    except OSError as exc:
        report["base_status"] = f"not_accessible:{type(exc).__name__}"
        report["targets"] = [{"target": t, "status": "not_accessible_parent"} for t in TARGETS]
        return report
    if not _same(os.fstat(bfd), bst):
        os.close(bfd)
        report["base_status"] = "replaced_during_scan"
        report["targets"] = [{"target": t, "status": "parent_replaced_during_scan"} for t in TARGETS]
        return report
    report["base_status"] = "ok"
    try:
        for t in TARGETS:
            row = {"target": t}
            try:
                st = os.stat(t, dir_fd=bfd, follow_symlinks=False)
            except FileNotFoundError:
                row["status"] = "missing"
                report["targets"].append(row)
                continue
            except OSError as exc:
                row.update(status="not_accessible", error=type(exc).__name__)
                report["targets"].append(row)
                continue
            if stat.S_ISLNK(st.st_mode):
                row["status"] = "symlink_refused"
            elif not stat.S_ISDIR(st.st_mode):
                row["status"] = "not_a_directory"
            else:
                try:
                    tfd = os.open(t, O_DIR, dir_fd=bfd)
                except OSError as exc:
                    row.update(status="not_accessible", error=type(exc).__name__)
                else:
                    try:
                        if not _same(os.fstat(tfd), st):
                            row["status"] = "replaced_during_scan"
                            report["targets"].append(row)
                            continue
                        row.update(status="present", mode=oct(stat.S_IMODE(st.st_mode)),
                                   owner_uid=st.st_uid)
                        entries = []
                        _scan_dir(tfd, "", t, out_ident, entries, 0, st.st_dev)
                        report["entries"].extend(entries)
                    finally:
                        os.close(tfd)
            report["targets"].append(row)
    finally:
        os.close(bfd)
    return report


# ----------------------------------------------------------------- summary

def _bucket(size: int) -> str:
    for limit, label in SIZE_BUCKETS:
        if size <= limit if limit == 0 else size < limit:
            return label
    return ">=16MiB"


def _ext(rel: str) -> str:
    name = rel.rsplit("/", 1)[-1]
    if "." not in name.lstrip("."):
        return "(none)"
    ext = "." + name.rsplit(".", 1)[-1].lower()
    return ext if ext in EXT_BUCKETS else "(other)"


def summarize(inv: dict, inv_bytes: bytes) -> dict:
    out = {"tool": "ella-memory-inventory-summary", "version": VERSION,
           "kind": "SANITIZED — review before sharing; contains no names, paths, per-file hashes or times",
           "private_inventory_sha256": "sha256:" + hashlib.sha256(inv_bytes).hexdigest(),
           "base_status": inv.get("base_status"), "targets": {}}
    for t in inv.get("targets", []):
        name = t["target"]
        rows = [e for e in inv.get("entries", []) if e["target"] == name]
        files = [e for e in rows if e["type"] == "file"]
        ok = [e for e in files if e.get("status") == "ok"]
        agg = hashlib.sha256()
        for e in sorted(ok, key=lambda e: e["rel"]):
            agg.update(f"{e['rel']}\0{e['sha256']}\n".encode("utf-8"))
        statuses = {}
        for e in rows:
            if e.get("status") not in ("ok", None):
                statuses[e["status"]] = statuses.get(e["status"], 0) + 1
        sizes, exts = {}, {}
        for e in ok:
            sizes[_bucket(e["size"])] = sizes.get(_bucket(e["size"]), 0) + 1
            exts[_ext(e["rel"])] = exts.get(_ext(e["rel"]), 0) + 1
        out["targets"][name] = {
            "status": t.get("status"),
            "mode": t.get("mode"),
            "counts": {k: sum(1 for e in rows if e["type"] == k) for k in ("file", "dir", "symlink", "special", "unknown")},
            "files_hashed": len(ok),
            "total_bytes_hashed": sum(e["size"] for e in ok),
            "size_buckets": dict(sorted(sizes.items())),
            "extensions": dict(sorted(exts.items())),
            "max_depth": max((e.get("depth", 0) for e in rows), default=0),
            "hardlinked_files": sum(1 for e in ok if e.get("nlink", 1) > 1),
            "non_ok_entries": dict(sorted(statuses.items())),
            "aggregate_sha256": "sha256:" + agg.hexdigest() if ok else None,
        }
    return out


def compare(a: dict, b: dict) -> dict:
    """Two private inventories -> counts only. Use it to detect files that changed between two passes, which
    timestamp checks can miss (same-size rewrites within one filesystem timestamp tick)."""
    def files(inv):
        return {(e["target"], e["rel"]): (e.get("size"), e.get("sha256"), e.get("status"))
                for e in inv.get("entries", []) if e["type"] == "file"}
    fa, fb = files(a), files(b)
    changed = sum(1 for k in fa.keys() & fb.keys() if fa[k] != fb[k])
    other = lambda inv: sorted((e["target"], e["rel"], e["type"], e.get("status"))
                               for e in inv.get("entries", []) if e["type"] != "file")
    out = {"tool": "ella-memory-inventory-compare", "version": VERSION,
           "kind": "SANITIZED — counts only",
           "files_changed": changed, "files_added": len(fb.keys() - fa.keys()),
           "files_removed": len(fa.keys() - fb.keys()),
           "non_file_entries_differ": other(a) != other(b),
           "targets_differ": a.get("targets") != b.get("targets")}
    out["identical"] = not (changed or out["files_added"] or out["files_removed"]
                            or out["non_file_entries_differ"] or out["targets_differ"])
    return out


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["scan"] and len(argv) == 1:
        try:
            inv = scan(BASE, _stdout_ident())
        except OutputInsideTarget as exc:
            print(f"refused: the output file is inside an inspected directory ({exc}). "
                  "Redirect output outside /home/ella/memory and /home/ella/diary.", file=sys.stderr)
            return 3
        sys.stdout.write(json.dumps(inv, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
        missing = [t for t in inv["targets"] if t.get("status") != "present"]
        for t in missing:
            print(f"note: {t['target']}: {t['status']}", file=sys.stderr)
        return 0
    if argv[:1] == ["summarize"] and len(argv) == 2:
        with open(argv[1], "rb") as fh:  # the private inventory only; nothing under /home/ella
            data = fh.read()
        sys.stdout.write(json.dumps(summarize(json.loads(data.decode("utf-8")), data),
                                    ensure_ascii=False, indent=1, sort_keys=True) + "\n")
        return 0
    if argv[:1] == ["compare"] and len(argv) == 3:
        docs = []
        for path in argv[1:]:
            with open(path, "rb") as fh:
                docs.append(json.loads(fh.read().decode("utf-8")))
        sys.stdout.write(json.dumps(compare(*docs), indent=1, sort_keys=True) + "\n")
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
