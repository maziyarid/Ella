#!/usr/bin/env python3
"""Ella continuity adapter v0.1 — read-only, synthetic copies only.

Reads a copy of the discovered `/home/ella` layout, derives everything the
checker's `observed` channel needs from the bytes it actually reads plus a
separately controlled attestation file, and hands the result to
`checker.assemble`. Output is one JSON document on stdout.

It never writes, migrates, schedules, opens sockets or calls a model. It
refuses any root that is not marked as a synthetic copy (`.synthetic-copy`)
and always refuses `/home/ella` itself: live use is not approved.

Usage:
    python3 -B adapter.py --root synthetic/home-ella \
        --manifest synthetic/manifest.json \
        --attestations synthetic/attestations.json \
        --topics tea date --now 2026-11-03T12:00:00Z
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import checker  # noqa: E402  (extend the existing checker; no second authority)
import attest_verify  # noqa: E402  (owner levels only from a verified register)

ADAPTER_VERSION = "0.1.0"
LIVE_ROOTS = {Path("/home/ella")}
MARKER = ".synthetic-copy"
FENCE_OPEN, FENCE_CLOSE = "```ella-record", "```"
TRUST = {
    "mode": "synthetic_copy_read_only",
    "hashes": "derived_from_bytes_read_by_this_process",
    "authority": "attestation file outside the memory root, bound to record_sha256",
    "episodic_stream": "diary/ only (D2); other event logs are read-only legacy inputs, never loaded",
    "writes": "none", "network": "none", "scheduler": "none", "model_calls": "none",
    "live_memory_use": "not_permitted",
}


class Refused(Exception):
    pass


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    with open(path, "rb") as fh:  # the only file-opening call in this module
        return fh.read()


# ------------------------------------------------------------ path policy

def rel_ok(ref: str) -> PurePosixPath | None:
    """A ref must be relative, normalized and free of `..`."""
    p = PurePosixPath(ref)
    if p.is_absolute() or ".." in p.parts or str(p) in ("", "."):
        return None
    return p


def under(ref: PurePosixPath, roots) -> bool:
    return any(ref == PurePosixPath(r.rstrip("/")) or
               PurePosixPath(r.rstrip("/")) in ref.parents for r in roots)


def no_symlink_on_path(root: Path, ref: PurePosixPath) -> bool:
    cur = root
    for part in ref.parts:
        cur = cur / part
        if cur.is_symlink():
            return False
    return True


def walk_files(base: Path):
    """Regular files under `base`, sorted; any symlink inside makes the source unauthorized."""
    out, links = [], []
    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        dirnames.sort()
        for name in sorted(dirnames):
            if (Path(dirpath) / name).is_symlink():
                links.append(Path(dirpath) / name)
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.is_symlink():
                links.append(p)
            elif stat.S_ISREG(p.lstat().st_mode):
                out.append(p)
    return sorted(out), links


# --------------------------------------------------------------- parsing

def extract_records(rel: str, data: bytes):
    """Yield (line_no, raw_line_bytes, record|None, problem|None). Prose is never parsed."""
    text = data.decode("utf-8", errors="strict")
    lines = text.split("\n")
    suffix = PurePosixPath(rel).suffix
    if suffix == ".jsonl":
        candidates = [(i + 1, ln) for i, ln in enumerate(lines) if ln.strip()]
        prose = 0
    elif suffix == ".md":
        candidates, inside, prose = [], False, 0
        for i, ln in enumerate(lines):
            if not inside and ln.strip() == FENCE_OPEN:
                inside = True
            elif inside and ln.strip() == FENCE_CLOSE:
                inside = False
            elif inside and ln.strip():
                candidates.append((i + 1, ln))
            elif ln.strip():
                prose += 1
    else:
        return [], len([ln for ln in lines if ln.strip()])
    out = []
    for no, ln in candidates:
        raw = ln.encode("utf-8")
        try:
            rec = json.loads(ln)
            if not isinstance(rec, dict):
                raise ValueError("not an object")
            out.append((no, raw, rec, None))
        except ValueError as exc:
            out.append((no, raw, None, f"unparseable: {type(exc).__name__}"))
    return out, prose


# ------------------------------------------------------------ attestation

def load_attestations(root: Path, path: Path | None, layout: dict):
    """The attestation source must live outside every authorized memory root."""
    # A separate file is a boundary, not evidence of owner approval. No signature is verified here (ATTESTATION.md).
    info = {"status": "absent", "sha256": None, "label": None,
            "owner_approval_evidence": "none: unsigned boundary file, no signature verified"}
    if path is None:
        return info, {}, {}
    rp = path.resolve()
    info["label"] = path.name
    try:
        inside = rp.is_relative_to(root.resolve())
    except ValueError:
        inside = False
    if inside:
        info["status"] = "unauthorized_inside_memory_root"
        return info, {}, {}
    if not rp.is_file():
        info["status"] = "missing"
        return info, {}, {}
    data = read_bytes(rp)
    info["sha256"] = sha(data)
    try:
        doc = json.loads(data.decode("utf-8"))
    except ValueError:
        info["status"] = "unparseable"
        return info, {}, {}
    info["status"] = "read"
    by_record = {}
    for a in doc.get("attestations", []):
        if a.get("record_id") and a.get("record_sha256") and a.get("authority") and a.get("decision_ref"):
            by_record.setdefault(a["record_id"], []).append(a)
    revisions = {}
    for r in doc.get("accepted_revisions", []):
        if r.get("source_id") and r.get("sha256") and r.get("decision_ref"):
            revisions[r["source_id"]] = r["sha256"]
    return info, by_record, revisions


# ----------------------------------------------------------------- adapter

def adapt(root: Path, manifest: dict, attestation_path: Path | None, topics, now: str,
          boot_id: str | None, hostname: str | None, include_input: bool = False,
          owner_register: dict | None = None) -> dict:
    """owner_register is the result of attest_verify.verify_register, computed by the caller.

    The adapter itself runs no subprocess. Owner levels (owner_approved, owner_stated) are granted only through
    attest_verify.owner_authority on a verified result; the unsigned attestation file can never grant them."""
    root = Path(root)
    if root.resolve() in LIVE_ROOTS or any(root.resolve() == p.resolve() for p in LIVE_ROOTS if p.exists()):
        raise Refused("live root refused: live memory use is not approved")
    if not (root / MARKER).is_file():
        raise Refused(f"root has no {MARKER} marker; refusing to read it")

    layout = manifest.get("layout") or {}
    authorized = layout.get("authorized_roots", [])
    episodic_ref = PurePosixPath(layout.get("episodic_stream", "diary/").rstrip("/"))
    findings = []  # adapter-level findings: no content, only names, hashes, counts

    def finding(kind, **kw):
        findings.append({"type": kind, **kw})

    att_info, att_by_record, accepted = load_attestations(root, attestation_path, layout)
    if att_info["status"] != "read":
        finding("attestation_source_" + att_info["status"].split("_")[0], status=att_info["status"])

    # Episodic rule (D2): exactly one episodic source, and it is diary/.
    epi = [s for s in manifest["memory_sources"] if s.get("store") == "episodic"]
    if len(epi) != 1:
        finding("episodic_stream_ambiguous", source_ids=sorted(s["id"] for s in epi))

    # Overlapping refs are ambiguous: no source can claim the same bytes as another.
    refs = {}
    for s in manifest["memory_sources"]:
        r = rel_ok(s.get("ref", ""))
        refs[s["id"]] = r
    ambiguous = set()
    ids = sorted(refs)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ra, rb = refs[a], refs[b]
            if ra and rb and (ra == rb or ra in rb.parents or rb in ra.parents):
                ambiguous |= {a, b}
                finding("source_overlap_ambiguous", source_ids=[a, b])
    if len(epi) != 1:
        ambiguous |= {s["id"] for s in epi}

    observed_sources, records, source_rows = {}, [], []
    covered = set()
    for s in manifest["memory_sources"]:
        sid, ref = s["id"], refs[s["id"]]
        row = {"id": sid, "store": s["store"], "ref": s.get("ref"), "expected": s.get("sha256")}
        reason = None
        if ref is None or not under(ref, authorized):
            reason = "unauthorized_path"
        elif s["store"] == "episodic" and ref != episodic_ref:
            reason = "unauthorized_episodic_source"  # D2: only diary/
        elif sid in ambiguous:
            reason = "ambiguous"
        elif not no_symlink_on_path(root, ref):
            reason = "unauthorized_symlink"
        path = root / ref if ref is not None else None
        if reason is None and not path.exists():
            reason = "missing"
        files, links = ([], [])
        if reason is None:
            if path.is_dir():
                files, links = walk_files(path)
                if links:
                    reason = "unauthorized_symlink"
            elif path.is_file():
                files = [path]
            else:
                reason = "missing"
        if reason is not None:
            row.update(status=reason, observed=None, files=0, records=0)
            observed_sources[sid] = {"readable": False, "reason": reason}
            source_rows.append(row)
            continue

        # Hash the exact bytes that are parsed. Directory hash = hash of "relpath\0filehash\n" lines.
        blobs, manifest_lines = {}, []
        for f in files:
            rel = f.relative_to(root).as_posix()
            data = read_bytes(f)
            blobs[rel] = data
            covered.add(rel)
            manifest_lines.append(f"{f.relative_to(path).as_posix() if path.is_dir() else f.name}\0{sha(data)}\n")
        observed = sha("".join(manifest_lines).encode("utf-8")) if path.is_dir() else sha(blobs[next(iter(blobs))])
        observed_sources[sid] = {"readable": True, "sha256": observed}
        n_rec = 0
        for rel, data in blobs.items():
            try:
                parsed, prose = extract_records(rel, data)
            except UnicodeDecodeError:
                finding("undecodable_file", source_id=sid, file=rel, sha256=sha(data))
                continue
            if prose and PurePosixPath(rel).suffix != ".jsonl":
                finding("prose_not_parsed", source_id=sid, file=rel, lines=prose)
            for no, raw, rec, problem in parsed:
                where = f"{rel}#L{no}"
                if problem:
                    finding("unparseable_record_line", source_id=sid, at=where, sha256=sha(raw))
                    continue
                rec = dict(rec)
                prov = dict(rec.get("provenance") or {})
                if "source_ref" in prov:
                    prov["claimed_source_ref"] = prov["source_ref"]
                prov["source_ref"] = "copy://" + where  # derived from where the bytes were read
                rec["provenance"] = prov
                rec["source_id"] = sid  # derived from location, never from the record
                rec.setdefault("store", s["store"])  # a declared store stays a claim the checker verifies
                rec["record_sha256"] = sha(raw)
                for k in ("attestation", "attestations", "authority_attestations", "accepted_revisions"):
                    if k in rec:
                        rec.pop(k)
                        finding("self_attestation_ignored", at=where, field=k)
                records.append(rec)
                n_rec += 1
        row.update(status="read", observed=observed, files=len(files), records=n_rec)
        source_rows.append(row)

    # Profiles (P0): hash only, content kept for the context block if it verifies.
    observed_profiles, profile_text = {}, {}
    for p in manifest.get("profiles", []):
        ref = rel_ok(p.get("ref", ""))
        if ref is None or not under(ref, authorized) or not no_symlink_on_path(root, ref):
            observed_profiles[p["id"]] = {"readable": False, "reason": "unauthorized_path"}
            continue
        f = root / ref
        if not f.is_file():
            observed_profiles[p["id"]] = {"readable": False, "reason": "missing"}
            continue
        data = read_bytes(f)
        covered.add(ref.as_posix())
        observed_profiles[p["id"]] = {"readable": True, "sha256": sha(data)}
        if sha(data) == p.get("sha256"):
            profile_text[p["id"]] = data.decode("utf-8", errors="replace")

    # Legacy inputs: hashed and counted, never parsed into records, never loaded.
    legacy_rows = []
    for li in layout.get("legacy_inputs", []):
        ref = rel_ok(li.get("ref", ""))
        row = {"id": li.get("id"), "ref": li.get("ref"), "kind": li.get("kind")}
        if ref is None or not under(ref, authorized) or not no_symlink_on_path(root, ref):
            row["status"] = "unauthorized_path"
        elif not (root / ref).is_file():
            row["status"] = "missing"
        else:
            data = read_bytes(root / ref)
            covered.add(ref.as_posix())
            row.update(status="read_only_legacy_not_loaded", sha256=sha(data), bytes=len(data),
                       nonblank_lines=sum(1 for ln in data.split(b"\n") if ln.strip()))
        legacy_rows.append(row)

    # Anything else under an authorized root: name and size only. Never opened.
    for r in authorized:
        base = root / r
        if base.is_file() or base.is_symlink():
            continue
        if base.is_dir():
            files, links = walk_files(base)
            for f in files:
                rel = f.relative_to(root).as_posix()
                if rel not in covered:
                    finding("unregistered_file_not_read", file=rel, bytes=f.lstat().st_size)
            for ln in links:
                finding("symlink_not_followed", file=ln.relative_to(root).as_posix())

    # Authority. Owner levels: only from a verified, signed register, bound to the exact record bytes.
    # Lower levels: from the unsigned attestation file (a boundary; no trusted issuer exists for them yet).
    attest = {}
    for rec in records:
        rid = rec.get("id")
        cands = att_by_record.get(rid, [])
        owner_cands = [a for a in cands if a["authority"] in attest_verify.OWNER_LEVELS]
        if owner_cands:
            finding("unsigned_owner_attestation_ignored", record_id=rid)
        cands = [a for a in cands if a["authority"] not in attest_verify.OWNER_LEVELS]
        good = [a for a in cands if a["record_sha256"] == rec["record_sha256"]]
        if cands and not good:
            finding("attestation_record_hash_mismatch", record_id=rid)
        if good:
            attest[rid] = min((a["authority"] for a in good),
                              key=lambda x: checker.AUTHORITY_RANK.get(x, -9))
        level, why = attest_verify.owner_authority(owner_register, rec.get("source_id"), rid, rec["record_sha256"])
        if level is not None:
            attest[rid] = level
        elif why == "record_bytes_differ_from_approved_bytes":
            finding("owner_approval_hash_mismatch", record_id=rid)
    rev = {sid: h for sid, h in accepted.items()}

    fresh = {}
    for chk in manifest.get("environment_checks", []):
        cap = chk.get("capability", "")
        if cap.startswith("copy_path:"):
            ref = rel_ok(cap.split(":", 1)[1])
            fresh[cap] = bool(ref and under(ref, authorized) and (root / ref).exists())

    checker_manifest = {k: v for k, v in manifest.items() if k != "layout"}
    checker_input = {
        "fixture_id": "adapter-run",
        "now": now,
        "manifest": checker_manifest,
        "observed": {"hostname": hostname, "boot_id": boot_id, "sources": observed_sources,
                     "profiles": observed_profiles, "fresh_checks": fresh,
                     "authority_attestations": attest, "accepted_revisions": rev},
        "query": {"topics": list(topics)},
        "records": records,
    }
    report = checker.assemble(checker_input, _HERE)
    report["trust"]["mode"] = "adapter_synthetic_copy"
    report["trust"]["observations"] = "derived_by_adapter_from_bytes_read"

    # Bounded context block: what a caller would place in the runtime's system message.
    by_id = {r["id"]: r for r in records if "id" in r}
    parts = []
    if report["boot_status"] == "ok":
        for pid in report["policy_sources"]:
            parts.append(f"[P0 {pid}]\n{profile_text.get(pid, '').strip()}")
        for s in report["selected"]:
            rec = by_id.get(s["id"], {})
            parts.append(f"[{s['label']} | {s['role']} | authority={s['authority']} | {s['source_ref']}]\n"
                         f"{str(rec.get('content', '')).strip()}")
        open_items = [f"- {u['type']}: {', '.join(u['ids'])}" for u in report["unresolved"]]
        if open_items:
            parts.append("[unresolved — do not treat as settled]\n" + "\n".join(open_items))
    context_block = "\n\n".join(parts)

    out = {
        "adapter_version": ADAPTER_VERSION,
        "trust": dict(TRUST),
        "sources": source_rows,
        "profiles": {k: {kk: vv for kk, vv in v.items()} for k, v in observed_profiles.items()},
        "legacy_inputs": legacy_rows,
        "attestation_source": att_info,
        "owner_register": _register_summary(owner_register),
        "findings": findings,
        "checker_input_sha256": sha(json.dumps(checker_input, sort_keys=True, ensure_ascii=False).encode("utf-8")),
        "report": report,
        "context_block": context_block,
        "context_block_sha256": sha(context_block.encode("utf-8")),
    }
    if include_input:
        out["checker_input"] = checker_input
    return out


def _register_summary(result):
    if not isinstance(result, dict):
        return {"status": "absent", "owner_approval_evidence": "none: no signed register supplied"}
    keep = ("status", "reason", "entries", "register_sha256", "signer_primary_fpr", "owner_approval_evidence",
            "rollback_check", "notes")
    out = {k: result[k] for k in keep if k in result}
    out["approvals_granted"] = len(result.get("approvals", {})) if result.get("status") == "verified" else 0
    return out


def _read_outside(root: Path, p: str | None):
    """Read a trust input once; refuse it if it lies inside the memory root."""
    if p is None:
        return None
    rp = Path(p).resolve()
    if rp.is_relative_to(Path(root).resolve()):
        raise Refused(f"trust input inside the memory root refused: {Path(p).name}")
    return read_bytes(rp) if rp.is_file() else None


def current_boot_id():
    p = Path("/proc/sys/kernel/random/boot_id")
    try:
        return read_bytes(p).decode().strip() if p.is_file() else None
    except OSError:
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--attestations")
    ap.add_argument("--register", help="signed owner register (JSONL), outside the root")
    ap.add_argument("--register-sig", help="detached OpenPGP signature over --register")
    ap.add_argument("--trusted-key", help="public key file of the trusted signer")
    ap.add_argument("--trusted-fpr", help="pinned fingerprint of the trusted signer; required for owner authority")
    ap.add_argument("--anchor", help="rollback anchor JSON {latest_seq, prefix_sha256}, outside the root")
    ap.add_argument("--topics", nargs="*", default=[])
    ap.add_argument("--now", default=None, help="ISO time; defaults to the current UTC time")
    ap.add_argument("--emit-checker-input", action="store_true",
                    help="include the exact checker input (fixture-shaped) in the output")
    args = ap.parse_args(argv)
    now = args.now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        manifest = json.loads(read_bytes(Path(args.manifest)).decode("utf-8"))
        register = None
        if any((args.register, args.register_sig, args.trusted_key, args.trusted_fpr, args.anchor)):
            anchor_bytes = _read_outside(Path(args.root), args.anchor)
            try:
                anchor = json.loads(anchor_bytes.decode("utf-8")) if anchor_bytes is not None else None
            except ValueError:
                anchor = "unparseable"
            register = attest_verify.verify_register(
                _read_outside(Path(args.root), args.register), _read_outside(Path(args.root), args.register_sig),
                _read_outside(Path(args.root), args.trusted_key), args.trusted_fpr, anchor,
                datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc))
        out = adapt(Path(args.root), manifest, Path(args.attestations) if args.attestations else None,
                    args.topics, now, current_boot_id(), socket.gethostname(),
                    include_input=args.emit_checker_input, owner_register=register)
    except Refused as exc:
        print(json.dumps({"refused": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if out["report"]["boot_status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
