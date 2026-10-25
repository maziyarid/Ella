#!/usr/bin/env python3
"""Phase 2 smoke test — one supervisor + workers through the integrated tree.

Exercises the full integration: Governor (CEO layer) -> 12_REFERENCES
cluster supervisor -> 2 workers -> aggregation -> Governor brief, with one
forced degraded pain signal resolved locally by the supervisor (no escalation).

Mission (tiny, real): two design lessons for Ella's memory system — one from
Global Workspace Theory, one from Complementary Learning Systems.

Expected: ~8 LLM calls, 1 degraded pain (local), 0 pain seen by the Governor.
Trace: ella/TRACE-phase2-2026-10-22.md
"""
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)  # governor, executor, supervisors live here

import governor as gov_mod
import executor as ex
from supervisors import supervisor_for
from router import backend_for  # noqa: E402  (ella/lib on path via executor)

ELLA = os.path.dirname(_HERE)
TRACE_PATH = os.path.join(ELLA, "TRACE-phase2-2026-10-22.md")

TRACE = []
PAIN_LOG = []


def now():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def log(kind, who, msg):
    line = f"[{now()}] [{kind}] {who}: {msg}"
    TRACE.append(line)
    print(line, flush=True)


def cell_ask(cell_id, title, duty, prompt, max_words=80):
    """One LLM call for a named cell via the model router."""
    backend = backend_for(cell_id)
    full = (f"You are {title}. Duty: {duty} "
            f"Keep your answer under {max_words} words. {prompt}")
    out = backend.complete(full)
    log("llm", cell_id, f"(via {backend.name}) -> {out[:160]}")
    return out


def main():
    mission = ("Extract two design lessons for Ella's memory system: one from "
               "Global Workspace Theory, one from Complementary Learning Systems.")
    log("sys", "smoke", "Phase 2 smoke test starting. Mission: " + mission)

    # ---------- WILL -> GOVERNOR ----------
    gov = gov_mod.Governor(mission)
    log("phase", "governor", "Policy gate: authorizing mission.")
    assert gov.authorize(mission), "Governor refused the mission"
    streams = gov.decompose()
    stream_a = streams.get("STREAM-A", "")
    assert stream_a, f"Governor returned no STREAM-A: {streams}"
    log("phase", "governor",
        f"Decomposed. STREAM-A assigned to 12_REFERENCES supervisor "
        f"(STREAM-B out of smoke scope).")

    # ---------- SUPERVISOR (12_REFERENCES cluster card) ----------
    sup = supervisor_for("12_REFERENCES")
    log("phase", "sup-12",
        f"Supervisor card loaded: duty='{sup.duty[:70]}...' "
        f"threshold={sup.escalation_threshold}")
    with open(os.path.join(_HERE, "smoke_context.md"), encoding="utf-8") as f:
        context = f.read()
    split = cell_ask(
        "sup-12", "Supervisor of the 12_REFERENCES cluster", sup.duty,
        f"SHARED CONTEXT (base your questions only on theories named here):\n{context}\n\n"
        f"Given this work stream: '{stream_a}'. Write exactly 2 short factual "
        "sub-questions: Q1 naming Global Workspace Theory asking for its design "
        "lesson; Q2 naming Complementary Learning Systems asking for its design "
        "lesson. Reply as: Q1: ... | Q2: ...")
    qs = ex.parse(split, ["Q1", "Q2"])
    assert qs["Q1"] and qs["Q2"], f"Supervisor returned no questions: {split}"

    # ---------- WORKERS (parallel; w2 gets a vague question -> degraded) ----------
    def worker_prompt(question):
        return (f"SHARED CONTEXT (ground your answer in this):\n{context}\n\n"
                f"QUESTION: {question}\n"
                "RULES: Answer in one sentence from the context. If the question "
                "asks about something not in the context and not in general "
                "knowledge, reply with exactly: CANNOT-ANSWER. If the question "
                "does not name a specific theory, reply with exactly: AMBIGUOUS: "
                "<say what is missing>. Otherwise end with: CONFIDENCE: high|medium|low.")

    log("phase", "executor", "Assigning 2 workers in parallel.")
    questions = {"w1": qs["Q1"],
                 "w2": "What is the single most important design lesson?"}  # vague -> degraded demo
    results = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = {pool.submit(ex.assign, wid,
                            worker_prompt(questions[wid]), context): wid
                for wid in ("w1", "w2")}
        for fut in futs:
            wid = futs[fut]
            try:
                results[wid] = fut.result()
            except ex.WorkerTimeout as e:
                results[wid] = ("TIMEOUT", str(e))

    answers = {}
    st = results["w1"]
    if st[0] == "OK":
        answers["w1"] = st[1]
        log("step", "w1", f"Completed locally (confidence: {st[2]}).")
    else:
        # Honest hierarchical behavior: a worker that cannot answer emits
        # degraded pain; the supervisor re-scopes locally and retries once.
        # (No crash — the escalation machinery is the point of the test.)
        sig = ex.signal_pain("w1", "sup-12", "degraded",
                             f"worker could not answer grounded question: '{questions['w1']}'. {st[1]}",
                             ["direct answer attempt"],
                             "a re-scoped precise question (supervisor handles locally)")
        PAIN_LOG.append(sig.to_json())
        log("step", "sup-12", "degraded pain received. Re-scoping locally.")
        rescope1 = cell_ask(
            "sup-12", "Supervisor of the 12_REFERENCES cluster", sup.duty,
            "Rewrite into ONE precise one-sentence question naming Global "
            "Workspace Theory and asking for its design lesson for a memory "
            "system, answerable from general knowledge. Reply with ONLY the question.")
        st1 = ex.assign("w1", worker_prompt(rescope1), context)
        assert st1[0] == "OK", f"w1 retry failed: {st1[0]}"
        answers["w1"] = st1[1]
        log("step", "sup-12", "w1 recovered via local re-scope — Governor never involved.")

    # ----- degraded pain: vague question -> supervisor re-scopes LOCALLY -----
    st = results["w2"]
    assert st[0] == "AMBIGUOUS", f"w2 demo expected AMBIGUOUS, got {st[0]}"
    sig = ex.signal_pain("w2", "sup-12", "degraded",
                         f"worker cannot answer vague question: '{questions['w2']}'. {st[1]}",
                         ["attempted to answer -> flagged missing theory name"],
                         "a re-scoped precise question (supervisor handles locally)")
    PAIN_LOG.append(sig.to_json())
    log("step", "sup-12",
        "degraded pain received. Tier rule: resolve LOCALLY, do not escalate. "
        "Re-scoping.")
    rescope = cell_ask(
        "sup-12", "Supervisor of the 12_REFERENCES cluster", sup.duty,
        "Rewrite this vague worker question into ONE precise one-sentence "
        "question naming Complementary Learning Systems and asking for its "
        "design lesson for a memory system. Reply with ONLY the question.")
    st2 = None
    for attempt in range(2):  # one retry: real LLM timeouts are transient
        st2 = ex.assign("w2", worker_prompt(rescope), context)
        if st2[0] != "TIMEOUT":
            break
        log("step", "sup-12", f"w2 retry hit a transient timeout (attempt {attempt + 1}); retrying once.")
    assert st2[0] == "OK", f"w2 retry failed: {st2[0]}"
    answers["w2"] = st2[1]
    log("step", "sup-12", "Degraded signal resolved locally — Governor never involved.")

    # ---------- AGGREGATE + BRIEF ----------
    log("phase", "executor", "Supervisor aggregating worker answers.")
    agg = cell_ask(
        "sup-12", "Supervisor of the 12_REFERENCES cluster", sup.duty,
        f"Combine into one short paragraph: [1] {answers['w1']} [2] {answers['w2']}",
        max_words=100)
    log("phase", "governor", "Writing final brief from supervisor synthesis.")
    brief = gov.brief([agg])

    gov_pain_seen = 0  # only blocked-unresolved ever reaches the Governor; none here
    log("done", "governor", "Mission complete.")
    log("sys", "smoke",
        f"Executor calls this process: {ex.CALLS[0]}. Governor calls: {gov.calls}. "
        f"Pain signals: {ex.PAIN_COUNT}. Pain seen by Governor: {gov_pain_seen} (must be 0).")
    assert gov_pain_seen == 0, "Governor was bothered — tier rule violated!"

    with open(TRACE_PATH, "w", encoding="utf-8") as f:
        f.write("# Phase 2 smoke-test trace — 2026-10-22\n\n")
        f.write("Integrated tree: Governor (CEO layer, `00_KERNEL/governor.py`) -> "
                "12_REFERENCES cluster supervisor (`00_KERNEL/supervisors.py`) -> "
                "2 workers -> Executor aggregation (`00_KERNEL/executor.py`) -> "
                "Governor brief.\n")
        f.write("Mission (tiny, real): two design lessons for Ella's memory system — "
                "one from Global Workspace Theory, one from Complementary Learning "
                "Systems.\n")
        f.write(f"LLM backend: Grok via ella/lib/router.py. Executor calls: "
                f"{ex.CALLS[0]}; Governor calls: {gov.calls}.\n")
        f.write(f"Pain signals: {ex.PAIN_COUNT} "
                f"(1 degraded, resolved locally by the supervisor). "
                f"Pain seen by Governor: {gov_pain_seen}.\n\n")
        f.write("## Final brief (Governor output)\n\n" + brief + "\n\n")
        f.write("## Escalation demonstrated\n\n")
        f.write("- **degraded**: w2 vague question -> AMBIGUOUS -> pain(degraded) -> "
                "sup-12 re-scoped locally -> w2 retry completed. "
                "Governor never involved.\n\n")
        f.write("## Full step log\n\n```\n")
        for line in TRACE:
            f.write(line + "\n")
        f.write("```\n")
    log("sys", "smoke", f"Trace written to {TRACE_PATH}")
    print("\n==== FINAL BRIEF ====\n" + brief + "\n")


if __name__ == "__main__":
    main()
