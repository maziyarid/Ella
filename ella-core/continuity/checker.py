#!/usr/bin/env python3
"""Ella continuity checker v0.1 — offline, deterministic, side-effect free.

Reads synthetic fixtures from explicit paths, validates the bootstrap manifest,
assembles a context-selection report and compares it with the fixture's
expectations.

It performs no network calls, writes no files, starts no scheduler and invokes
no provider model. It only reads the paths it is given (plus a `$base`
manifest named inside a fixture, resolved relative to that fixture).

Trust boundary: this is a synthetic evaluation harness, not a live-memory
loader. Everything under a fixture's `observed` key (source hashes, fresh
checks, authority attestations, accepted revisions) stands in for what a live
adapter must derive itself from trusted observations and accepted decision
records. The checker enforces that authority comes from that channel and never
from a record's own `authority` field, but it cannot authenticate the channel.
Every report says so in `trust`.

Reuses `ella/lib/pain.py` severity tiers for gaps (missing source -> degraded,
P0 integrity failure -> blocked), matching the 03_MEMORY supervisor rule that
retrieval misses emit degraded.

Usage:
    python3 checker.py fixtures/                 # run every fixture, exit 1 on any failure
    python3 checker.py fixtures/F01_*.json --report   # print the structured report
    python3 checker.py --manifest manifest.example.json   # validate a manifest only
"""
from __future__ import annotations

import difflib
import json
import math
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # no cache files next to the source
sys.path.insert(0, str(_HERE.parent / "ella" / "lib"))
from pain import SEVERITIES  # noqa: E402  (reuse existing tiers; side-effect free)

CONTRACT = "ella-continuity-bootstrap"
SUPPORTED_VERSIONS = {"0.1.0"}
STORES = ("core", "episodic", "notebook", "people")  # the only authoritative stores
AUTHORITY_RANK = {
    "owner_approved": 4,
    "owner_stated": 3,
    "ella_observed": 2,
    "ella_inferred": 1,
    "third_party_reported": 0,
    "derived": -1,
}
UNATTESTED = "unattested"
AUTHORITY_RANK_EFFECTIVE = {**AUTHORITY_RANK, UNATTESTED: -2}
TRUST = {
    "mode": "synthetic_fixture",
    "authority": "claimed_by_record; effective = min(claim, attestation from observed channel)",
    "observations": "supplied_by_fixture_not_authenticated",
    "live_memory_use": "not_permitted",
}
PRIVACY_LEVELS = {"public": 0, "private": 1, "restricted": 2}
REALITIES = {"stated", "observed", "inferred", "reported", "simulated",
             "dream", "imagined", "synthetic"}
REQUIRED_MANIFEST = (
    "contract", "contract_version", "code_sources", "profiles", "memory_sources",
    "derived_indexes", "load_order", "context_budget_tokens", "unresolved_questions",
    "supersession", "term_equivalents", "environment_checks", "expiring_authority",
    "privacy", "integrity",
)
REQUIRED_RECORD = ("id", "store", "source_id", "kind", "reality", "authority",
                   "recorded_at", "topics", "content")
SECRET_KEY = re.compile(r"password|passwd|secret|token|api[_-]?key|private[_-]?key|credential", re.I)
SECRET_KEY_ALLOW = {"context_budget_tokens", "tokens", "tokens_used"}
SECRET_VALUE = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bghp_[A-Za-z0-9]{10,}|\bsk-[A-Za-z0-9]{10,}")
GRANT_KEYS = {"grant", "grants", "execution_grant", "permissions", "allow_all"}
INSTRUCTION_PATTERNS = [
    re.compile(r"\b(ignore|disregard|forget)\b.{0,20}\b(previous|prior|above|earlier|all)\b.{0,20}\b(rules|instructions|policy|policies)\b"),
    re.compile(r"\bnew system prompt\b|\byou are now\b"),
    re.compile(r"(دستور|قانون|قوانین)\S*\s+قبلی\S*\s+(را\s+|رو\s+)?نادیده\s+بگیر"),
]

_DIGITS = {ord(c): str(i) for i, c in enumerate("٠١٢٣٤٥٦٧٨٩")}
_DIGITS.update({ord(c): str(i) for i, c in enumerate("۰۱۲۳۴۵۶۷۸۹")})
_LETTERS = {ord("ي"): "ی", ord("ى"): "ی", ord("ك"): "ک"}
_DIACRITICS = re.compile("[\u064b-\u0652\u0670]")


# ---------------------------------------------------------------- utilities

def norm(text: str) -> str:
    """Persian/English retrieval normalization (see CONTRACT.md §4)."""
    s = unicodedata.normalize("NFC", str(text))
    s = s.replace("\u200c", " ").replace("\u200e", "").replace("\u200f", "")
    s = s.translate(_DIGITS).translate(_LETTERS)
    s = _DIACRITICS.sub("", s)
    s = s.casefold()
    return " ".join(s.split())


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def valid_token_count(value) -> bool:
    """A declared token count must be a positive int. bool is rejected (True == 1)."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def tokens_of(record: dict) -> int:
    if "tokens" in record:
        if not valid_token_count(record["tokens"]):
            raise ValueError(f"invalid token count: {record['tokens']!r}")
        return record["tokens"]
    return max(1, math.ceil(len(str(record.get("content", ""))) / 4))


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def resolve_manifest(manifest: dict, base_dir: Path) -> dict:
    """Support {"$base": "relative/path.json", ...overrides} (shallow merge)."""
    if "$base" not in manifest:
        return manifest
    base = load_json((base_dir / manifest["$base"]).resolve())
    merged = dict(base)
    for key, value in manifest.items():
        if key != "$base":
            merged[key] = value
    return merged


# ------------------------------------------------------- manifest validation

def _scan(obj, path, errors):
    if isinstance(obj, dict):
        for key, value in obj.items():
            here = f"{path}.{key}"
            if SECRET_KEY.search(str(key)) and key not in SECRET_KEY_ALLOW:
                errors.append(f"forbidden_secret_field:{here}")
            if key in GRANT_KEYS and (value in ("*", "all", True) or
                                      (isinstance(value, list) and "*" in value)):
                errors.append(f"blanket_grant:{here}")
            _scan(value, here, errors)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _scan(item, f"{path}[{i}]", errors)
    elif isinstance(obj, str) and SECRET_VALUE.search(obj):
        errors.append(f"key_material:{path}")


def validate_manifest(m: dict) -> list:
    errors = []
    for key in REQUIRED_MANIFEST:
        if key not in m:
            errors.append(f"missing_field:{key}")
    if errors:
        return errors
    if m["contract"] != CONTRACT:
        errors.append("wrong_contract")
    if m["contract_version"] not in SUPPORTED_VERSIONS:
        errors.append(f"unsupported_version:{m['contract_version']}")
    seen = set()
    for src in m["memory_sources"]:
        if src.get("store") not in STORES:
            errors.append(f"fifth_store_not_allowed:{src.get('id')}:{src.get('store')}")
        if not src.get("sha256"):
            errors.append(f"source_without_hash:{src.get('id')}")
        if src.get("id") in seen:
            errors.append(f"duplicate_source:{src.get('id')}")
        seen.add(src.get("id"))
    for idx in m["derived_indexes"]:
        if idx.get("authoritative") is not False:
            errors.append(f"derived_index_claims_authority:{idx.get('id')}")
    for prof in m["profiles"]:
        if not prof.get("sha256") or not (prof.get("approval") or {}).get("by"):
            errors.append(f"profile_not_approved_or_unhashed:{prof.get('id')}")
        if not valid_token_count(prof.get("tokens")):
            errors.append(f"bad_profile_tokens:{prof.get('id')}:{prof.get('tokens')!r}")
    p0 = [lo for lo in m["load_order"] if lo.get("priority") == "P0"]
    if not p0 or not p0[0].get("never_drop"):
        errors.append("p0_must_be_never_drop")
    if (m["privacy"] or {}).get("session_clearance") not in PRIVACY_LEVELS:
        errors.append("bad_session_clearance")
    if not valid_token_count(m["context_budget_tokens"]):
        errors.append("bad_budget")
    _scan(m, "manifest", errors)
    return errors


# ----------------------------------------------------------------- assembly

class Equivalents:
    def __init__(self, table: dict):
        self.classes = []
        for key, values in (table or {}).items():
            self.classes.append({norm(key), *(norm(v) for v in values)})

    def expand(self, topic: str) -> set:
        t = norm(topic)
        parts = {t} | {tok for tok in t.split() if len(tok) >= 3}
        out = set(parts)
        for p in parts:
            for cls in self.classes:
                if p in cls:
                    out |= cls
        return out


def label_for(r: dict) -> str:
    kind, reality = r.get("kind"), r.get("reality")
    if r.get("store") == "index":
        return "derived_index"
    if kind == "approval":
        return "historical_authorization_receipt"
    if kind == "receipt":
        return "historical_environment_receipt"
    if reality == "simulated":
        return "simulated_state"
    if reality == "dream":
        return "dream_speculative"
    if reality == "imagined":
        return "imagined_speculative"
    if reality == "synthetic":
        return "synthetic_example"
    if r.get("status") == "hypothesis":
        return "hypothesis"
    if reality == "reported":
        evidence = (r.get("provenance") or {}).get("evidence") or []
        if evidence and all(e.get("inspected") is True for e in evidence):
            return "reported_evidence_located"
        return "reported_unverified"
    if reality == "inferred":
        return "inference"
    return "event" if r.get("store") == "episodic" else "fact"


def has_instruction_text(text: str) -> bool:
    n = norm(text)
    return any(p.search(n) for p in INSTRUCTION_PATTERNS)


def assemble(fixture: dict, base_dir: Path) -> dict:
    m = resolve_manifest(fixture["manifest"], base_dir)
    observed = fixture.get("observed", {})
    query = fixture.get("query", {})
    now = parse_time(fixture["now"])
    report = {
        "fixture_id": fixture.get("fixture_id"),
        "contract_version": m.get("contract_version"),
        "boot_status": "ok",
        "manifest_errors": validate_manifest(m),
        "integrity": [], "gaps": [], "capabilities": {}, "environment_ready": False,
        "prior_receipts": [], "selected": [], "applied": {}, "omitted": [],
        "irrelevant_count": 0, "unresolved": [], "correction_history": [],
        "authority_from_memory": [], "policy_sources": [], "people": {},
        "tokens_used": 0, "trust": dict(TRUST),
    }
    if report["manifest_errors"]:
        report["boot_status"] = "invalid_manifest"  # fail closed: select nothing
        return report

    budget = m["context_budget_tokens"]
    clearance = PRIVACY_LEVELS[m["privacy"]["session_clearance"]]

    # Integrity: memory sources and P0 profiles.
    source_status, source_hash = {}, {}
    for src in m["memory_sources"]:
        obs = (observed.get("sources") or {}).get(src["id"])
        if obs is None or obs.get("readable") is False:
            status = "missing"
            report["gaps"].append({"source_id": src["id"], "store": src["store"],
                                   "severity": "degraded",
                                   "reason": (obs or {}).get("reason", "missing"),
                                   "note": "source missing, unreadable, ambiguous or unauthorized; contents not inferred"})
        else:
            source_hash[src["id"]] = obs.get("sha256")
            accepted = (observed.get("accepted_revisions") or {}).get(src["id"])
            if obs.get("sha256") == src["sha256"]:
                status = "match"
            elif accepted and accepted == obs.get("sha256"):
                status = "accepted_revision"  # an accepted decision names this exact new hash
            else:
                status = "changed_unreconciled"
                report["gaps"].append({"source_id": src["id"], "store": src["store"],
                                       "severity": "degraded",
                                       "note": "hash differs from manifest and no accepted revision; "
                                               "records held back pending reconciliation"})
        source_status[src["id"]] = status
        report["integrity"].append({"id": src["id"], "expected": src["sha256"],
                                    "observed": source_hash.get(src["id"]), "status": status})
    p0_tokens = 0
    for prof in m["profiles"]:
        obs = (observed.get("profiles") or {}).get(prof["id"])
        if obs is None or obs.get("readable") is False:
            status = "missing"
        else:
            status = "match" if obs.get("sha256") == prof["sha256"] else "mismatch"
        report["integrity"].append({"id": prof["id"], "expected": prof["sha256"],
                                    "observed": (obs or {}).get("sha256"), "status": status})
        if status != "match":
            report["gaps"].append({"source_id": prof["id"], "store": "profiles",
                                   "severity": "blocked",
                                   "note": "approved profile missing or not the approved version"})
            report["boot_status"] = "blocked_profile_integrity"
        p0_tokens += prof["tokens"]  # validated positive int
    assert all(g["severity"] in SEVERITIES for g in report["gaps"])
    if report["boot_status"] != "ok":
        return report
    if p0_tokens > budget:
        report["boot_status"] = "boot_failed"
        report["manifest_errors"].append(f"p0_exceeds_budget:{p0_tokens}>{budget}")
        return report
    report["policy_sources"] = [p["id"] for p in m["profiles"]]
    report["tokens_used"] = p0_tokens

    # Environment-bound state: never carried, always re-checked.
    fresh = observed.get("fresh_checks") or {}
    for chk in m["environment_checks"]:
        cap = chk["capability"]
        if cap in fresh:
            report["capabilities"][cap] = "verified_now" if fresh[cap] is True else "failed_now"
        else:
            report["capabilities"][cap] = "unverified_requires_fresh_check"
        prior = chk.get("prior_receipt")
        if prior:
            report["prior_receipts"].append({
                "capability": cap, "prior_boot_id": prior.get("boot_id"),
                "same_hostname": prior.get("hostname") == observed.get("hostname"),
                "same_boot": prior.get("boot_id") == observed.get("boot_id"),
                "counts_as_current": False})
    caps = report["capabilities"]
    report["environment_ready"] = bool(caps) and all(v == "verified_now" for v in caps.values())

    def omit(rid, reason, meaningful=False, detail=None):
        entry = {"id": rid, "reason": reason, "meaningful": meaningful}
        if detail:
            entry["detail"] = detail
        report["omitted"].append(entry)

    # 1-4: validation, privacy, source availability, staleness.
    registered = {s["id"]: s["store"] for s in m["memory_sources"]}
    integrity_unresolved = [{"type": "source_revision_unreconciled", "ids": [sid]}
                            for sid, st in sorted(source_status.items()) if st == "changed_unreconciled"]
    id_counts = {}
    for r in fixture.get("records", []):
        id_counts[r.get("id", "<no-id>")] = id_counts.get(r.get("id", "<no-id>"), 0) + 1
    for rid, n in sorted(id_counts.items()):
        if n > 1:
            integrity_unresolved.append({"type": "duplicate_record_id", "ids": [rid], "count": n})
    attest = observed.get("authority_attestations") or {}
    pool = {}
    for r in fixture.get("records", []):
        rid = r.get("id", "<no-id>")
        if id_counts[rid] > 1:
            omit(rid, "duplicate_record_id", True, "no copy is trusted until the ID collision is resolved")
            continue
        prov = r.get("provenance") or {}
        if not all(prov.get(k) for k in ("recorded_by", "method", "source_ref")):
            omit(rid, "missing_provenance", True,
                 "confidence is not a substitute for provenance" if "confidence" in r else None)
            continue
        if any(k not in r for k in REQUIRED_RECORD) or r.get("reality") not in REALITIES \
                or r.get("authority") not in AUTHORITY_RANK:
            omit(rid, "invalid_record", True)
            continue
        if "tokens" in r and not valid_token_count(r["tokens"]):
            omit(rid, "invalid_record", True, f"token count must be a positive integer, got {r['tokens']!r}")
            continue
        if PRIVACY_LEVELS.get(r.get("privacy", "private"), 2) > clearance:
            omit(rid, "privacy_filtered")
            continue
        if r["store"] == "index":
            df = r.get("derived_from") or {}
            src = df.get("source_id")
            if source_status.get(src) in (None, "missing"):
                omit(rid, "derived_source_unverifiable", True)
                continue
            if source_status.get(src) == "changed_unreconciled":
                omit(rid, "source_changed_unreconciled", True)
                continue
            if df.get("sha256") != source_hash.get(src):
                omit(rid, "stale_derived", True, f"built from {df.get('sha256')}, source now {source_hash.get(src)}")
                continue
        elif r["store"] not in STORES:
            omit(rid, "invalid_record", True, f"store {r['store']} is not authoritative")
            continue
        elif r["source_id"] not in registered:
            omit(rid, "unregistered_source", True)
            continue
        elif r["store"] != registered[r["source_id"]]:
            omit(rid, "store_source_mismatch", True,
                 f"record says {r['store']}, source {r['source_id']} is registered as {registered[r['source_id']]}")
            continue
        elif source_status.get(r["source_id"]) == "missing":
            omit(rid, "source_missing", True)
            continue
        elif source_status.get(r["source_id"]) == "changed_unreconciled":
            omit(rid, "source_changed_unreconciled", True)
            continue
        pool[rid] = r

    eq = Equivalents(m["term_equivalents"])
    q_terms = set()
    for t in query.get("topics", []):
        q_terms |= eq.expand(t)

    def relevant(r):
        terms = set()
        for t in r.get("topics", []):
            terms |= eq.expand(t)
        return bool(terms & q_terms)

    rel = {rid: relevant(r) for rid, r in pool.items()}
    # Authority is never taken from the record alone. The effective level is the
    # lower of the record's claim and the attestation from the observed channel;
    # without an attestation the record ranks below every attested level.
    effective = {}
    for rid, r in pool.items():
        att = attest.get(rid)
        if att not in AUTHORITY_RANK:
            effective[rid] = UNATTESTED
        else:
            effective[rid] = min(r["authority"], att, key=lambda a: AUTHORITY_RANK[a])
    rank = {rid: AUTHORITY_RANK_EFFECTIVE[a] for rid, a in effective.items()}

    # Fresh derived entries never replace the authoritative record they index.
    for rid, r in list(pool.items()):
        target = (r.get("derived_from") or {}).get("record_id")
        if r["store"] == "index" and target in pool:
            if rel[rid] or rel[target]:
                omit(rid, "authoritative_preferred")
            del pool[rid]

    # 5: supersession (explicit links only) and slot resolution.
    superseded, contested, unresolved = {}, set(), []
    edges = []  # (by, target, accepted)
    for rid in sorted(pool):
        r = pool[rid]
        for target in r.get("supersedes", []):
            if target not in pool:
                unresolved.append({"type": "supersedes_unknown_record", "ids": sorted([rid, target])})
                continue
            ok = effective[rid] != UNATTESTED and rank[rid] >= rank[target]
            edges.append((rid, target, ok))
            if not ok:
                contested.add(rid)
                unresolved.append({"type": "supersession_lacks_authority", "ids": sorted([target, rid])})
    # Accepted links that form a cycle (A supersedes B, B supersedes A, ...) resolve nothing.
    graph = {}
    for by, target, ok in edges:
        if ok:
            graph.setdefault(by, set()).add(target)
    def reach(start):
        out, stack = set(), list(graph.get(start, ()))
        while stack:
            n = stack.pop()
            if n not in out:
                out.add(n)
                stack.extend(graph.get(n, ()))
        return out
    reachable = {n: reach(n) for n in sorted(graph)}
    in_cycle = {n for n, rs in reachable.items() if n in rs}
    cycles = []
    for node in sorted(in_cycle):
        if not any(node in c for c in cycles):
            cycles.append({node} | {n for n in reachable[node] if node in reachable.get(n, ())})
    for c in cycles:
        contested |= c
        unresolved.append({"type": "supersession_cycle", "ids": sorted(c)})
    for by, target, ok in edges:
        accepted = ok and not (by in in_cycle and target in in_cycle)
        report["correction_history"].append({"superseded": target, "by": by, "accepted": accepted})
        if accepted:
            superseded[target] = by
    for target, by in superseded.items():
        if rel.get(target) or rel.get(by):
            omit(target, "superseded", False, f"superseded by {by}; kept in correction_history")
    live = {rid: r for rid, r in pool.items() if rid not in superseded}

    slots = {}
    for rid, r in live.items():
        if r.get("slot"):
            slots.setdefault(r["slot"], []).append(rid)
    for slot, ids in sorted(slots.items()):
        top = max(rank[i] for i in ids)
        tops = [i for i in ids if rank[i] == top]
        if all(effective[i] == UNATTESTED for i in tops):
            # Nothing in this slot has attested authority, so nothing is applied.
            unresolved.append({"type": "slot_without_attested_authority", "ids": sorted(ids)})
            if len(ids) > 1:
                contested |= set(ids)
            continue
        if len(tops) == 1:
            report["applied"][slot] = tops[0]
            contested |= set(ids) - set(tops)
        else:
            contested |= set(ids)
        if len(ids) > 1:
            covered = any(set(ids) <= set(u["ids"]) for u in unresolved)
            if not covered:
                unresolved.append({"type": "slot_conflict", "ids": sorted(ids),
                                   "resolution": "higher_authority_applied" if len(tops) == 1 else "none_equal_authority"})

    # 6: relevance (after supersession so corrections are found either way).
    candidates = []
    for rid, r in live.items():
        if rel[rid]:
            candidates.append(r)
        else:
            report["irrelevant_count"] += 1
    rel_ids = {r["id"] for r in candidates}
    report["unresolved"] = [u for u in unresolved if set(u["ids"]) & (rel_ids | set(superseded))]
    report["unresolved"] += integrity_unresolved  # always reported, relevant or not
    report["correction_history"] = [h for h in report["correction_history"]
                                    if h["by"] in rel_ids or h["superseded"] in rel_ids]
    report["applied"] = {s: i for s, i in report["applied"].items() if i in rel_ids}

    # 7: expiring authority. Memory never grants current authority.
    kept = []
    for r in candidates:
        if r.get("kind") == "approval":
            a = r.get("approval") or {}
            reasons = []
            if not a.get("expires_at") or parse_time(a["expires_at"]) <= now:
                reasons.append("expired")
            binding = a.get("env_binding") or {}
            if binding.get("boot_id") and binding["boot_id"] != observed.get("boot_id"):
                reasons.append("boot_mismatch")
            if binding.get("hostname") and binding["hostname"] != observed.get("hostname"):
                reasons.append("host_mismatch")
            if reasons:
                omit(r["id"], "expired_authority", True, ",".join(reasons))
                continue
        kept.append(r)

    # People: never merge on name similarity.
    people = [r for r in kept if r["store"] == "people" and r.get("person_id")]
    for r in people:
        report["people"].setdefault(r["person_id"], []).append(r["id"])
    names = {}
    for r in people:
        names.setdefault(r["person_id"], set()).add(norm(r.get("name", "")))
    pids = sorted(names)
    for i, a in enumerate(pids):
        for b in pids[i + 1:]:
            if any(difflib.SequenceMatcher(None, x, y).ratio() >= 0.8 for x in names[a] for y in names[b]):
                report["unresolved"].append({"type": "possible_duplicate_person", "ids": sorted([a, b])})
    flags = {}
    for r in kept:
        f = []
        if has_instruction_text(r.get("content", "")):
            f.append("contains_instruction_text")
        for mention in r.get("mentions", []):
            if mention.get("person_id"):
                continue
            mn = norm(mention.get("name", ""))
            matches = sorted(p for p in pids if any(
                mn and (mn in x or difflib.SequenceMatcher(None, mn, x).ratio() >= 0.8) for x in names[p]))
            f.append("person_unresolved")
            if len(matches) > 1:
                report["unresolved"].append({"type": "ambiguous_person_reference",
                                             "ids": sorted([r["id"], *matches])})
        flags[r["id"]] = f

    # 8: budget. Priority, then authority, then recency, then id.
    prio = {}
    for lo in m["load_order"]:
        for store in lo.get("stores", []):
            prio[store] = int(lo["priority"][1:])
    kept.sort(key=lambda r: (int(str(r.get("priority", f"P{prio.get(r['store'], 9)}"))[1:]),
                             -rank[r["id"]], -parse_time(r["recorded_at"]).timestamp(), r["id"]))
    for r in kept:
        cost = tokens_of(r)
        if report["tokens_used"] + cost > budget:
            omit(r["id"], "budget", True, f"needs {cost}, {budget - report['tokens_used']} left")
            continue
        report["tokens_used"] += cost
        role = "applied" if r["id"] in report["applied"].values() else (
            "contested" if r["id"] in contested else "context")
        if effective[r["id"]] == UNATTESTED:
            flags[r["id"]].append("authority_unattested")
        report["selected"].append({
            "id": r["id"], "label": label_for(r), "role": role, "authority": effective[r["id"]],
            "claimed_authority": r["authority"],
            "store": r["store"], "source_ref": r["provenance"]["source_ref"], "flags": flags[r["id"]]})
    selected_ids = {s["id"] for s in report["selected"]}
    report["applied"] = {s: i for s, i in report["applied"].items() if i in selected_ids}
    return report


# --------------------------------------------------------------- comparison

def _forbidden_holds(pred: dict, rep: dict) -> bool:
    sel = {s["id"]: s for s in rep["selected"]}
    if "selected" in pred:
        return pred["selected"] in sel
    if "label" in pred:
        s = sel.get(pred["label"])
        return bool(s) and s["label"] in pred["in"]
    if "environment_ready" in pred:
        return rep["environment_ready"] == pred["environment_ready"]
    if "capability" in pred:
        return rep["capabilities"].get(pred["capability"]) == pred["status"]
    if "authority_from_memory" in pred:
        return pred["authority_from_memory"] in rep["authority_from_memory"]
    if "policy_source" in pred:
        return pred["policy_source"] in rep["policy_sources"]
    if "applied" in pred:
        return pred["applied"] in rep["applied"].values()
    if "merged_people" in pred:
        a, b = pred["merged_people"]
        ids_a, ids_b = set(rep["people"].get(a, [])), set(rep["people"].get(b, []))
        return a == b or bool(ids_a & ids_b) or any(set(v) >= (ids_a | ids_b) and ids_a and ids_b
                                                    for k, v in rep["people"].items() if k not in (a, b))
    if "content_from_source" in pred:
        return any(s["source_ref"].startswith(pred["content_from_source"]) for s in rep["selected"])
    if "boot_status" in pred:
        return rep["boot_status"] == pred["boot_status"]
    raise ValueError(f"unknown forbidden predicate: {pred}")


def compare(rep: dict, exp: dict) -> list:
    fails = []
    if rep["boot_status"] != exp.get("boot_status", "ok"):
        fails.append(f"boot_status {rep['boot_status']} != {exp.get('boot_status', 'ok')}")
    got_sel = sorted(s["id"] for s in rep["selected"])
    if "selected" in exp and got_sel != sorted(exp["selected"]):
        fails.append(f"selected {got_sel} != {sorted(exp['selected'])}")
    if "applied" in exp and rep["applied"] != exp["applied"]:
        fails.append(f"applied {rep['applied']} != {exp['applied']}")
    if "omitted" in exp:
        got = sorted((o["id"], o["reason"]) for o in rep["omitted"])
        want = sorted((o["id"], o["reason"]) for o in exp["omitted"])
        if got != want:
            fails.append(f"omitted {got} != {want}")
    if "unresolved" in exp:
        got = sorted((u["type"], tuple(u["ids"])) for u in rep["unresolved"])
        want = sorted((u["type"], tuple(sorted(u["ids"]))) for u in exp["unresolved"])
        if got != want:
            fails.append(f"unresolved {got} != {want}")
    sel = {s["id"]: s for s in rep["selected"]}
    for rid, label in exp.get("labels", {}).items():
        if rid not in sel or sel[rid]["label"] != label:
            fails.append(f"label {rid}: {sel.get(rid, {}).get('label')} != {label}")
    for rid, flag in exp.get("flags", {}).items():
        if rid not in sel or flag not in sel[rid]["flags"]:
            fails.append(f"flag {rid}: missing {flag}")
    for cap, status in exp.get("capabilities", {}).items():
        if rep["capabilities"].get(cap) != status:
            fails.append(f"capability {cap}: {rep['capabilities'].get(cap)} != {status}")
    if "environment_ready" in exp and rep["environment_ready"] != exp["environment_ready"]:
        fails.append(f"environment_ready {rep['environment_ready']} != {exp['environment_ready']}")
    if "gaps" in exp and sorted(g["source_id"] for g in rep["gaps"]) != sorted(exp["gaps"]):
        fails.append(f"gaps {[g['source_id'] for g in rep['gaps']]} != {exp['gaps']}")
    for h in exp.get("correction_history", []):
        if h not in rep["correction_history"]:
            fails.append(f"correction_history missing {h}")
    if "manifest_errors_include" in exp:
        for e in exp["manifest_errors_include"]:
            if not any(err.startswith(e) for err in rep["manifest_errors"]):
                fails.append(f"manifest_errors missing {e}")
    for pred in exp.get("forbidden", []):
        if _forbidden_holds(pred, rep):
            fails.append(f"forbidden conclusion holds: {pred}")
    if rep["authority_from_memory"]:
        fails.append("memory granted current authority")
    return fails


def run_fixture(path: Path):
    fixture = load_json(path)
    if fixture.get("synthetic") is not True:
        return None, [f"{path.name}: fixture is not marked synthetic; refusing to evaluate"]
    rep = assemble(fixture, path.parent)
    return rep, compare(rep, fixture["expected"])


def _fixture_paths(args):
    out = []
    for a in args:
        p = Path(a)
        out.extend(sorted(p.glob("*.json")) if p.is_dir() else [p])
    return out


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--manifest" in argv:
        path = Path(argv[argv.index("--manifest") + 1])
        errors = validate_manifest(load_json(path))
        print(json.dumps({"manifest": str(path), "valid": not errors, "errors": errors}, indent=2))
        return 1 if errors else 0
    want_report = "--report" in argv
    paths = _fixture_paths([a for a in argv if not a.startswith("--")])
    if not paths:
        print(__doc__)
        return 2
    failed = 0
    for path in paths:
        rep, fails = run_fixture(path)
        if want_report:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        status = "PASS" if not fails else "FAIL"
        failed += bool(fails)
        print(f"{status} {path.name}" + "".join(f"\n    - {f}" for f in fails),
              file=sys.stderr if want_report else sys.stdout)
    print(f"{len(paths) - failed}/{len(paths)} fixtures passed",
          file=sys.stderr if want_report else sys.stdout)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
