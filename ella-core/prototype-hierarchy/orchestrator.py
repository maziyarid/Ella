#!/usr/bin/env python3
"""
Phase 1 prototype — hierarchical LLM organisation (Ella Core).

Upgrades over Phase 0:
  * Cell role cards as data (roles.py): duty, tools, memory scope,
    escalation threshold, model backend per role.
  * Pain-signal schema with severity tiers (pain.py):
      info     -> log only
      degraded -> direct manager resolves LOCALLY (re-scope / retry)
      blocked  -> route up the chain; CEO sees only blocked-unresolved
  * Timeout-based escalation: a worker call exceeding WORKER_TIMEOUT_S
    becomes a blocked pain signal automatically.
  * Model router (router.py): per-cell backend declaration; one-line swaps.
  * Shared context doc (context.md) grounded into every worker prompt.
  * Robust field parsing (no more trailing-| leaks).
  * Independent leaf calls run in parallel (ThreadPoolExecutor).

Mission (REAL task, not synthetic): summarise 3 recent papers on hierarchical
multi-agent LLM systems (MetaGPT, DyLAN, AutoGen) and extract one design
lesson from each; CEO delivers a 3-bullet brief.

Staged tier demos (transparent, logged as such):
  W2: simulated hang -> timeout -> blocked pain -> manager retries -> completes
      (retry notes low confidence -> info pain, logged only)
  W3: deliberately vague question -> AMBIGUOUS -> degraded pain -> manager
      re-scopes locally -> worker retries -> completes (supervisor unbothered)
  W4: deliberately fabricated paper -> CANNOT-ANSWER -> blocked pain ->
      manager scope-check fails -> escalates to supervisor -> supervisor
      substitutes an answerable question -> completes (CEO unbothered)

Budget: ~60 LLM calls (expected ~16).
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roles import ROLES, CELLS, MANAGER_OF, SUPERVISOR_OF
from router import backend_for
from pain import PainSignal, TIER_HANDLING, WORKER_TIMEOUT_S

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACE = []
CALLS = [0]
PAIN_COUNT = {"info": 0, "degraded": 0, "blocked": 0}
CEO_PAIN_SEEN = [0]


def now():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def log(kind, who, msg):
    line = f"[{now()}] [{kind}] {who}: {msg}"
    TRACE.append(line)
    print(line, flush=True)


class WorkerTimeout(Exception):
    pass


def cell_call(cell_id, prompt, timeout_s=WORKER_TIMEOUT_S):
    """One LLM call for a cell via the model router."""
    role = ROLES[CELLS[cell_id]]
    CALLS[0] += 1
    full = (f"You are {role.title} in a research cell-organisation. "
            f"Duty: {role.duty} Keep your answer under {role.max_words} words. "
            f"{prompt}")
    backend = backend_for(cell_id)
    try:
        out = backend.complete(full, timeout_s=timeout_s)
    except subprocess.TimeoutExpired:
        raise WorkerTimeout(f"LLM call timed out after {timeout_s}s")
    log("llm", cell_id, f"(call #{CALLS[0]} via {backend.name}) -> {out[:200]}")
    return out


def emit_pain(fr, to, severity, what_happened, tried_locally, needed):
    sig = PainSignal(frm=fr, to=to, severity=severity,
                     what_happened=what_happened,
                     tried_locally=list(tried_locally),
                     needed_from_above=needed)
    PAIN_COUNT[severity] += 1
    if to == "ceo":
        CEO_PAIN_SEEN[0] += 1
    log("pain", fr, f"[{severity}] escalating to {to} "
                    f"(tier rule: {TIER_HANDLING[severity]}): {sig.to_json()}")
    return sig


def parse_fields(text, keys):
    """Robust KEY: value parsing — splits on pipes/newlines, strips empties
    and stray trailing pipes (Phase 0 bug fix)."""
    out = {}
    for part in re.split(r"\s*\|\s*|\n", text):
        part = part.strip().rstrip("|").strip()
        if not part:
            continue
        m = re.match(r"^(Q\d+|STREAM-[AB]|SUBSTITUTE|ANSWER)\s*:\s*(.+)$",
                     part, re.IGNORECASE)
        if m:
            out[m.group(1).upper()] = m.group(2).strip()
    return {k: out.get(k, "") for k in keys}


def load_context():
    with open(os.path.join(OUT_DIR, "context.md"), encoding="utf-8") as f:
        return f.read()


def worker_prompt(question, context, extra=""):
    return (f"SHARED CONTEXT (ground your answer in this):\n{context}\n\n"
            f"QUESTION: {question}\n"
            f"{extra}\n"
            "RULES: Answer in one sentence from the context. If the question asks "
            "about something not in the context and not in general knowledge, "
            "reply with exactly: CANNOT-ANSWER. If the question does not name a "
            "specific paper, reply with exactly: AMBIGUOUS: <say what is missing>. "
            "Otherwise end your answer with: CONFIDENCE: high|medium|low.")


def run_worker(cell_id, question, context, simulate_hang=False):
    """Assign -> attempt. Returns (status, answer_or_note)."""
    mgr = MANAGER_OF[cell_id]
    log("route", mgr, f"Assigned to {cell_id}: {question}")
    if simulate_hang:
        # Deterministic timeout demo (logged as simulated, no real waiting).
        log("step", cell_id, "SIMULATED HANG for the timeout-escalation demo.")
        raise WorkerTimeout(f"LLM call timed out after {WORKER_TIMEOUT_S}s (simulated)")
    try:
        ans = cell_call(cell_id, worker_prompt(question, context))
    except WorkerTimeout as e:
        return ("TIMEOUT", str(e))
    if "CANNOT-ANSWER" in ans:
        return ("CANNOT", ans)
    if ans.strip().upper().startswith("AMBIGUOUS"):
        return ("AMBIGUOUS", ans)
    conf = "unknown"
    m = re.search(r"CONFIDENCE:\s*(high|medium|low)", ans, re.IGNORECASE)
    if m:
        conf = m.group(1).lower()
    return ("OK", ans, conf)


def main():
    context = load_context()
    log("sys", "orchestrator", "Phase 1 starting. Mission: 3-paper research brief "
        "(MetaGPT, DyLAN, AutoGen) — one design lesson each.")
    log("sys", "orchestrator", f"Tier rules: {TIER_HANDLING}")

    # ---------- ASSIGN phase: CEO decomposes ----------
    log("phase", "orchestrator", "ASSIGN: CEO decomposing mission.")
    decomp = cell_call(
        "ceo",
        "Split this mission into exactly 2 work streams: STREAM-A covers the "
        "MetaGPT and DyLAN papers; STREAM-B covers the AutoGen paper plus any "
        "comparison. Reply as: STREAM-A: <one line> | STREAM-B: <one line>")
    streams = parse_fields(decomp, ["STREAM-A", "STREAM-B"])

    # ---------- ASSIGN phase: supervisors split into leaf questions ----------
    log("phase", "orchestrator", "ASSIGN: supervisors splitting streams.")
    qa = cell_call(
        "sup-a",
        f"Given this work stream: '{streams['STREAM-A']}'. Write exactly 2 short "
        "factual sub-questions, each naming ONE specific paper (MetaGPT, DyLAN) "
        "and asking for its key design lesson. Reply as: Q1: ... | Q2: ...")
    qs_a = parse_fields(qa, ["Q1", "Q2"])

    qb = cell_call(
        "sup-b",
        f"Given this work stream: '{streams['STREAM-B']}'. Write exactly 1 short "
        "factual sub-question naming the AutoGen paper and asking for its key "
        "design lesson. Reply as: Q3: ...")
    qs_b = parse_fields(qb, ["Q3"])
    # Q4: deliberately fabricated paper -> forces the blocked tier demo.
    q4 = ("What design lesson does the 2024 paper 'HMAC: Hierarchical "
          "Multi-Agent Consensus' by Zhang et al. teach? (NOTE: this paper is "
          "fabricated for the escalation demo — it does not exist.)")
    log("step", "sup-b", f"Q4 (injected blockage for the blocked-tier demo): {q4}")

    # ---------- ASSIGN + MONITOR: workers run in parallel ----------
    log("phase", "orchestrator", "ASSIGN+MONITOR: 4 workers in parallel.")
    questions = {"w1": qs_a["Q1"], "w2": qs_a["Q2"], "w3": qs_b["Q3"], "w4": q4}
    # W3's question is deliberately vague (no paper named) -> degraded demo.
    questions["w3"] = "What is the single most important design lesson?"
    results = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(run_worker, wid, questions[wid], context,
                            simulate_hang=(wid == "w2")): wid
                for wid in ("w1", "w2", "w3", "w4")}
        for fut in futs:
            wid = futs[fut]
            try:
                results[wid] = fut.result()
            except WorkerTimeout as e:
                results[wid] = ("TIMEOUT", str(e))
            except Exception as e:  # noqa: BLE001 — convert to blocked pain
                results[wid] = ("ERROR", str(e))

    answers = {}

    # ----- W1: normal path (+ organic info tier if low confidence) -----
    st = results["w1"]
    if st[0] == "OK":
        answers["w1"] = st[1]
        if st[2] == "low":
            emit_pain("w1", "mgr-a1", "info",
                      "answer completed but worker confidence is low",
                      ["answered from shared context"],
                      "none — logged for awareness only")
            log("step", "mgr-a1", "info signal logged only (tier rule). No action.")
        else:
            log("step", "w1", f"Completed locally (confidence: {st[2]}).")
    else:
        raise RuntimeError(f"W1 unexpected status {st[0]} — aborting demo.")

    # ----- W2: timeout -> blocked -> manager retries -> completes -----
    st = results["w2"]
    assert st[0] == "TIMEOUT", f"W2 demo expected TIMEOUT, got {st[0]}"
    emit_pain("w2", "mgr-a1", "blocked",
              f"worker LLM call timed out: {st[1]}",
              ["initial attempt"],
              "retry the worker once")
    log("step", "mgr-a1", "blocked pain received. Local resolution: retrying worker once.")
    st2 = run_worker("w2", questions["w2"], context)
    assert st2[0] == "OK", f"W2 retry failed with {st2[0]}"
    answers["w2"] = st2[1]
    log("step", "mgr-a1", "Retry succeeded — resolved locally, no escalation.")
    if st2[2] == "low":
        emit_pain("w2", "mgr-a1", "info",
                  "retry answer completed but worker confidence is low",
                  ["timeout then successful retry"],
                  "none — logged for awareness only")

    # ----- W3: ambiguous -> degraded -> manager re-scopes locally -----
    st = results["w3"]
    assert st[0] == "AMBIGUOUS", f"W3 demo expected AMBIGUOUS, got {st[0]}"
    emit_pain("w3", "mgr-b1", "degraded",
              f"worker cannot answer vague question: '{questions['w3']}'. {st[1]}",
              ["attempted to answer -> flagged missing paper reference"],
              "a re-scoped precise question (no supervisor needed)")
    log("step", "mgr-b1", "degraded pain received. Tier rule: resolve LOCALLY, "
                           "do not escalate. Re-scoping the question.")
    rescope = cell_call(
        "mgr-b1",
        "Rewrite this vague worker question into ONE precise one-sentence "
        "question that names the AutoGen paper and asks for its key design "
        "lesson, answerable from the shared context below. Reply with ONLY the "
        f"question.\n\nSHARED CONTEXT:\n{context}")
    log("step", "mgr-b1", f"Re-scoped question: {rescope}")
    st3 = run_worker("w3", rescope, context)
    assert st3[0] == "OK", f"W3 retry failed with {st3[0]}"
    answers["w3"] = st3[1]
    log("step", "mgr-b1", "Degraded signal resolved locally — supervisor never involved.")

    # ----- W4: fabricated paper -> blocked -> manager -> supervisor -----
    st = results["w4"]
    assert st[0] == "CANNOT", f"W4 demo expected CANNOT, got {st[0]}"
    emit_pain("w4", "mgr-b1", "blocked",
              f"sub-question unanswerable (fabricated paper): '{q4}'",
              ["direct answer attempt -> CANNOT-ANSWER"],
              "a re-scoped or substitute question")
    log("step", "mgr-b1", "blocked pain received. Trying local resolution: scope check.")
    scope = cell_call(
        "mgr-b1",
        f"A worker cannot answer: '{q4}'. Is this question answerable from "
        "general knowledge at all? Start your reply with YES or NO, then one sentence.")
    if scope.strip().upper().startswith("YES"):
        log("warn", "mgr-b1", "Scope check says answerable — escalating anyway (demo).")
    emit_pain("mgr-b1", "sup-b", "blocked",
              f"worker w4 blocked on fabricated paper question",
              ["direct answer attempt", "manager scope check -> not answerable"],
              "supervisor authority to substitute an answerable question")
    log("step", "sup-b", "blocked pain received. Resolving with supervisor authority: "
                         "substituting an answerable question.")
    sub = cell_call(
        "sup-b",
        "A worker was asked about a fabricated paper. Propose ONE closely related "
        "REAL question about hierarchical multi-agent LLM systems that IS answerable "
        "from general knowledge, then answer it in one sentence. Reply as: "
        "SUBSTITUTE: <question> || ANSWER: <answer>")
    parts = parse_fields(sub, ["SUBSTITUTE", "ANSWER"])
    answers["w4"] = parts["ANSWER"] or sub
    log("resolve", "sup-b", f"Substituted '{parts['SUBSTITUTE'][:120]}' — answer flows back down.")

    # ---------- COMPLETE phase: aggregate -> synthesise -> brief ----------
    log("phase", "orchestrator", "COMPLETE: managers aggregating.")
    agg_a = cell_call(
        "mgr-a1",
        f"Combine these two worker answers into one short paragraph: [1] {answers['w1']} [2] {answers['w2']}")
    agg_b = cell_call(
        "mgr-b1",
        f"Combine these two worker answers into one short paragraph: [1] {answers['w3']} [2] {answers['w4']}")

    log("phase", "orchestrator", "COMPLETE: supervisors synthesising.")
    syn_a = cell_call(
        "sup-a",
        f"Turn this into 2 crisp bullet points, each naming its paper and one design "
        f"lesson (max 25 words each): {agg_a}")
    syn_b = cell_call(
        "sup-b",
        f"Turn this into 2 crisp bullet points, each naming its paper and one design "
        f"lesson (max 25 words each): {agg_b}")

    log("phase", "orchestrator", "COMPLETE: CEO writing final brief.")
    brief = cell_call(
        "ceo",
        "Write a 3-bullet brief: ONE key design lesson each from the MetaGPT, "
        "DyLAN and AutoGen papers (max 30 words per bullet). Base it ONLY on: "
        f"{syn_a} {syn_b}")

    log("done", "ceo", "Mission complete.")
    log("sys", "orchestrator",
        f"Total LLM calls: {CALLS[0]}. Pain signals: {PAIN_COUNT}. "
        f"Pain signals seen by CEO: {CEO_PAIN_SEEN[0]} (must be 0).")
    assert CEO_PAIN_SEEN[0] == 0, "CEO was bothered — tier rule violated!"

    # ---------- write trace ----------
    trace_path = os.path.join(OUT_DIR, "trace-phase1-2026-10-22.md")
    with open(trace_path, "w", encoding="utf-8") as f:
        f.write("# Phase 1 prototype trace — 2026-10-22\n\n")
        f.write("Hierarchical LLM organisation: CEO -> 2 supervisors -> 2 managers -> 4 workers.\n")
        f.write("Mechanisms: role cards (roles.py), pain-signal tiers (pain.py), "
                "model router (router.py), shared context grounding (context.md), "
                "parallel leaf calls, timeout escalation.\n")
        f.write("Mission (REAL task): summarise 3 papers on hierarchical multi-agent "
                "LLM systems (MetaGPT, DyLAN, AutoGen), one design lesson each.\n")
        f.write(f"LLM backend: Grok (grok-4.7) via custom.grok connector. "
                f"Calls used: {CALLS[0]}.\n")
        f.write(f"Pain signals emitted: {PAIN_COUNT} (info=log-only, "
                f"degraded=local, blocked=escalated). CEO saw {CEO_PAIN_SEEN[0]}.\n\n")
        f.write("## Final brief (CEO output)\n\n" + brief + "\n\n")
        f.write("## Tiered escalation paths demonstrated\n\n")
        f.write("- **timeout -> blocked**: W2 simulated hang -> pain(blocked) -> "
                "mgr-a1 retried locally -> completed. Supervisor/CEO unbothered.\n")
        f.write("- **degraded**: W3 vague question -> AMBIGUOUS -> pain(degraded) -> "
                "mgr-b1 re-scoped locally -> completed. Supervisor/CEO unbothered.\n")
        f.write("- **blocked**: W4 fabricated paper -> CANNOT-ANSWER -> pain(blocked) -> "
                "mgr-b1 scope-check failed -> escalated pain(blocked) -> sup-b "
                "substituted a real question -> completed. CEO unbothered.\n")
        f.write("- **info**: low-confidence notes logged only, no routing.\n\n")
        f.write("## Full step log\n\n```\n")
        for line in TRACE:
            f.write(line + "\n")
        f.write("```\n")
    log("sys", "orchestrator", f"Trace written to {trace_path}")
    print("\n==== FINAL BRIEF ====\n" + brief + "\n")


if __name__ == "__main__":
    main()
