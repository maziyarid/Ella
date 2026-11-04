#!/usr/bin/env python3
"""Owner-attestation register verifier v0.1 (isolated; tested with disposable keys only).

Decides whether a signed, append-only register (ATTESTATION.md) grants owner authority to a record's exact bytes.
Everything fails closed: any missing input, tooling problem, signature problem, malformed or conflicting entry, or
rollback-anchor mismatch refuses the whole register, and then no record gets owner authority.

Isolation:
- Inputs are bytes the caller read once; the same bytes are verified and parsed.
- gpg runs with a fresh temporary home directory that contains only the supplied public key. The user's keyring,
  agent and configuration are never consulted. The temporary directory is removed afterwards.
- A valid signature is not enough. The signing key (or its primary key) must equal an explicitly configured trusted
  fingerprint. With no configured fingerprint, every register is refused.

Trusted-state assumptions (not established by this module): the gpg binary is genuine; the trusted fingerprint and the
public key file come from a location the record writer cannot modify; the rollback anchor is stored where the record
writer cannot rewind it. See ATTESTATION.md §6.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import weakref
from types import MappingProxyType
from datetime import datetime, timezone

VERSION = "0.1.0"
OWNER_LEVELS = ("owner_approved", "owner_stated")
ACTIONS = ("approve", "withdraw", "replace")
FIELDS_REQUIRED = {"seq", "action", "record_id", "source_id", "record_sha256", "decision_ref", "issued_at"}
FIELDS_ALLOWED = FIELDS_REQUIRED | {"authority", "expires_at", "supersedes_entry"}
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
FPR_RE = re.compile(r"^(?:[0-9A-F]{40}|[0-9A-F]{64})$")
CTRL_RE = re.compile(r"[\x00-\x1f\x7f]")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
GPG_TIMEOUT_S = 30
BAD_STATUS = ("BADSIG", "ERRSIG", "EXPSIG", "EXPKEYSIG", "REVKEYSIG", "NO_PUBKEY", "NODATA", "FAILURE")


def sha(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def normalize_fpr(value) -> str | None:
    if not isinstance(value, str):
        return None
    v = value.replace(" ", "").upper()
    return v if FPR_RE.match(v) else None


def _ts(v):
    if not isinstance(v, str) or not TS_RE.match(v):
        raise ValueError("timestamp must be YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _refused(reason: str, **kw) -> dict:
    return {"verifier_version": VERSION, "status": "refused", "reason": reason, "approvals": {},
            "owner_approval_evidence": f"none: {reason}", **kw}


# --------------------------------------------------------------- signature

def _run(cmd, env, timeout):
    """Run in a new process group; on timeout, kill the whole group so no child outlives the call."""
    proc = subprocess.Popen(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.communicate()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def verify_signature(data: bytes, signature: bytes, public_key: bytes, trusted_fpr: str,
                     gpg_binary: str = "gpg") -> tuple[bool, str, str | None]:
    """Return (ok, reason, signer_primary_fpr). Never touches the caller's keyring."""
    exe = shutil.which(gpg_binary) if os.sep not in gpg_binary else (gpg_binary if os.access(gpg_binary, os.X_OK) else None)
    if exe is None:
        return False, "verification_tool_missing", None
    home = tempfile.mkdtemp(prefix="ella-attest-gnupg-")
    os.chmod(home, 0o700)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C", "LC_ALL": "C", "GNUPGHOME": home}
    base = [exe, "--homedir", home, "--batch", "--no-tty", "--no-options", "--no-auto-key-retrieve",
            "--no-auto-key-locate", "--keyid-format", "long"]
    try:
        kf, df, sf = (os.path.join(home, n) for n in ("trusted.pub", "register.bin", "register.sig"))
        for path, blob in ((kf, public_key), (df, data), (sf, signature)):
            with open(path, "wb") as fh:
                fh.write(blob)
        try:
            imp = _run(base + ["--import", kf], env, GPG_TIMEOUT_S)
            if imp.returncode != 0:
                return False, "verification_failed:public_key_import", None
            ver = _run(base + ["--status-fd", "1", "--trust-model", "always", "--verify", sf, df], env, GPG_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            return False, "verification_failed:timeout", None
        except OSError:
            return False, "verification_tool_missing", None
        status = [ln.split()[1:] for ln in ver.stdout.decode("utf-8", "replace").splitlines()
                  if ln.startswith("[GNUPG:] ") and len(ln.split()) > 1]
        kinds = [s[0] for s in status]
        bad = [k for k in kinds if k in BAD_STATUS]
        if bad:
            return False, "verification_failed:" + bad[0].lower(), None
        valid = [s for s in status if s[0] == "VALIDSIG"]
        if ver.returncode != 0 or kinds.count("GOODSIG") != 1 or len(valid) != 1:
            return False, "verification_failed:no_single_good_signature", None
        v = valid[0]
        signing_fpr = v[1].upper() if len(v) > 1 else ""
        primary_fpr = v[10].upper() if len(v) > 10 else signing_fpr
        sig_class = v[9] if len(v) > 9 else ""
        if sig_class != "00":
            return False, "verification_failed:not_a_binary_detached_signature", None
        if primary_fpr != trusted_fpr:   # the pin is the primary key; a subkey counts only through its primary
            return False, "untrusted_signer", primary_fpr
        return True, "ok", primary_fpr
    finally:
        try:
            gpgconf = shutil.which("gpgconf")
            if gpgconf:
                subprocess.run([gpgconf, "--homedir", home, "--kill", "all"], env=env,
                               capture_output=True, timeout=10)
        except (OSError, subprocess.TimeoutExpired):
            pass
        shutil.rmtree(home, ignore_errors=True)


# ---------------------------------------------------------------- register

def _no_dupes(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key")
    return dict(pairs)


def parse_register(data: bytes) -> tuple[list[dict] | None, str]:
    if data == b"":
        return [], "ok"
    if not data.endswith(b"\n"):
        return None, "malformed:last_line_not_terminated"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None, "malformed:not_utf8"
    entries = []
    for i, line in enumerate(text[:-1].split("\n"), start=1):
        if "\r" in line or line != line.strip():
            return None, f"malformed:line_{i}_whitespace_or_cr"
        try:
            e = json.loads(line, object_pairs_hook=_no_dupes)
        except ValueError:
            return None, f"malformed:line_{i}_not_a_json_object"
        if not isinstance(e, dict):
            return None, f"malformed:line_{i}_not_a_json_object"
        if not FIELDS_REQUIRED <= set(e) or not set(e) <= FIELDS_ALLOWED:
            return None, f"malformed:line_{i}_fields"
        if type(e["seq"]) is not int or e["seq"] != i:
            return None, f"malformed:line_{i}_seq_not_contiguous"
        if e["action"] not in ACTIONS:
            return None, f"malformed:line_{i}_action"
        for k in ("record_id", "source_id", "decision_ref"):
            if not isinstance(e[k], str) or not e[k] or CTRL_RE.search(e[k]):
                return None, f"malformed:line_{i}_{k}"
        if not isinstance(e["record_sha256"], str) or not SHA_RE.match(e["record_sha256"]):
            return None, f"malformed:line_{i}_record_sha256"
        try:
            _ts(e["issued_at"])
            if e.get("expires_at") is not None:
                _ts(e["expires_at"])
        except ValueError:
            return None, f"malformed:line_{i}_timestamp"
        sup = e.get("supersedes_entry")
        if e["action"] in ("approve", "replace") and e.get("authority") not in OWNER_LEVELS:
            return None, f"malformed:line_{i}_authority"
        if e["action"] == "withdraw" and e.get("authority") is not None:
            return None, f"malformed:line_{i}_authority_on_withdraw"
        if e["action"] == "approve" and sup is not None:
            return None, f"malformed:line_{i}_supersedes_on_approve"
        if e["action"] in ("withdraw", "replace") and (type(sup) is not int or not 1 <= sup < i):
            return None, f"malformed:line_{i}_supersedes_entry"
        entries.append(e)
    return entries, "ok"


def resolve(entries: list[dict], now: datetime) -> tuple[dict | None, str, dict]:
    """Return active approvals keyed by 'source_id\\0record_id', or a conflict reason."""
    active, by_seq, notes = {}, {}, {"expired": 0, "not_yet_valid": 0, "withdrawn": 0, "replaced": 0}
    for e in entries:
        key = f"{e['source_id']}\0{e['record_id']}"
        by_seq[e["seq"]] = e
        if e["action"] in ("withdraw", "replace"):
            old = by_seq[e["supersedes_entry"]]
            okey = f"{old['source_id']}\0{old['record_id']}"
            if old["action"] == "withdraw" or active.get(okey, {}).get("seq") != old["seq"]:
                return None, f"conflict:entry_{e['seq']}_supersedes_inactive_entry", notes
            if e["action"] == "withdraw" and (old["source_id"], old["record_id"], old["record_sha256"]) != \
                    (e["source_id"], e["record_id"], e["record_sha256"]):
                return None, f"conflict:entry_{e['seq']}_withdraw_does_not_match", notes
            if e["action"] == "replace":
                if old["source_id"] != e["source_id"]:
                    return None, f"conflict:entry_{e['seq']}_replace_across_sources", notes
                if old["record_id"] != e["record_id"]:
                    return None, f"conflict:entry_{e['seq']}_replace_changes_record_id", notes
                if old["record_sha256"] == e["record_sha256"]:
                    return None, f"conflict:entry_{e['seq']}_replace_with_same_bytes", notes
            del active[okey]
            notes["withdrawn" if e["action"] == "withdraw" else "replaced"] += 1
            if e["action"] == "withdraw":
                continue
        if key in active:
            return None, f"conflict:entry_{e['seq']}_second_active_approval", notes
        active[key] = e
    granted = {}
    for key, e in active.items():
        if _ts(e["issued_at"]) > now:
            notes["not_yet_valid"] += 1
            continue
        if e.get("expires_at") is not None and _ts(e["expires_at"]) <= now:
            notes["expired"] += 1
            continue
        granted[key] = {"record_sha256": e["record_sha256"], "authority": e["authority"], "seq": e["seq"],
                        "decision_ref": e["decision_ref"]}
    return granted, "ok", notes


# ---------------------------------------------------------------- rollback

def check_anchor(data: bytes, entries: list[dict], anchor) -> tuple[bool, str]:
    """anchor = {"latest_seq": n, "prefix_sha256": sha256 of the first n lines (with their newlines)}."""
    if not isinstance(anchor, dict) or set(anchor) != {"latest_seq", "prefix_sha256"} \
            or type(anchor["latest_seq"]) is not int or anchor["latest_seq"] < 0 \
            or not isinstance(anchor["prefix_sha256"], str) or not SHA_RE.match(anchor["prefix_sha256"]):
        return False, "anchor_malformed"
    n = anchor["latest_seq"]
    if len(entries) < n:
        return False, "rollback_detected:register_older_than_anchor"
    prefix = b"".join(ln + b"\n" for ln in data.split(b"\n")[:n]) if n else b""
    if sha(prefix) != anchor["prefix_sha256"]:
        return False, "rollback_or_fork_detected:prefix_mismatch"
    return True, "ok"


def anchor_for(data: bytes) -> dict:
    """What the owner would store as the new anchor after accepting this register. Never written by this module."""
    n = 0 if data == b"" else data.count(b"\n")
    return {"latest_seq": n, "prefix_sha256": sha(data)}


# ----------------------------------------------------------------- top level

def verify_register(register: bytes | None, signature: bytes | None, public_key: bytes | None,
                    trusted_fpr, anchor, now: datetime, gpg_binary: str = "gpg") -> dict:
    fpr = normalize_fpr(trusted_fpr)
    if trusted_fpr is None:
        return _refused("no_trusted_signer_configured")
    if fpr is None:
        return _refused("trusted_fingerprint_invalid")
    if register is None:
        return _refused("register_missing")
    if signature is None:
        return _refused("signature_missing")
    if public_key is None:
        return _refused("trusted_public_key_missing")
    if anchor is None:
        return _refused("rollback_anchor_missing")
    info = {"register_sha256": sha(register)}
    ok, reason, signer = verify_signature(register, signature, public_key, fpr, gpg_binary)
    if not ok:
        return _refused(reason, signer_primary_fpr=signer, **info)
    entries, why = parse_register(register)
    if entries is None:
        return _refused(why, **info)
    ok, why = check_anchor(register, entries, anchor)
    if not ok:
        return _refused(why, **info)
    granted, why, notes = resolve(entries, now)
    if granted is None:
        return _refused(why, **info)
    proof = _Proof(granted)
    _ISSUED.add(proof)
    return {"_proof": proof, "verifier_version": VERSION, "status": "verified", "reason": "ok", "signer_primary_fpr": signer,
            "entries": len(entries), "approvals": granted, "notes": notes,
            "owner_approval_evidence": "verified_detached_signature_from_configured_fingerprint",
            "rollback_check": "prefix_matches_supplied_anchor", "anchor_if_accepted": anchor_for(register), **info}


class _Proof:
    """Issued only by verify_register. owner_authority reads approvals from here, never from the result dict,
    so a hand-built or edited dict cannot grant authority. (In-process code could still call private
    functions; this guards against data mistakes and injected dicts, not against hostile code in the process.)"""
    __slots__ = ("approvals", "__weakref__")

    def __init__(self, granted):
        self.approvals = MappingProxyType({k: MappingProxyType(dict(v)) for k, v in granted.items()})


_ISSUED: "weakref.WeakSet[_Proof]" = weakref.WeakSet()


def owner_authority(result: dict, source_id: str, record_id: str, record_sha256: str) -> tuple[str | None, str]:
    """Owner authority for one record, or (None, reason). Only a result issued by verify_register can grant it."""
    if not isinstance(result, dict) or result.get("status") != "verified":
        return None, "no_verified_register"
    proof = result.get("_proof")
    if type(proof) is not _Proof or proof not in _ISSUED:
        return None, "no_verified_register"
    a = proof.approvals.get(f"{source_id}\0{record_id}")
    if a is None:
        return None, "not_approved"
    if a["record_sha256"] != record_sha256:
        return None, "record_bytes_differ_from_approved_bytes"
    return a["authority"], "ok"
