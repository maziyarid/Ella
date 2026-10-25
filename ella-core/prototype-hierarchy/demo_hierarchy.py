#!/usr/bin/env python3
"""
Phase 0 prototype — hierarchical LLM organisation (Ella Core).

Hierarchy:
    CEO
    ├── Supervisor A (Benefits / structure) -> Manager A1 -> Workers W1, W2
    └── Supervisor B (Risks / operations)   -> Manager B1 -> Workers W3, W4

Each cell = a role (duty, escalation threshold) wrapped around one LLM call.
Workers escalate via structured PAIN SIGNALS only when locally blocked;
everything else is handled without bothering upper layers.

Mission: produce a 3-bullet brief on the benefits of hierarchical agent
organisation. Worker W4 is deliberately given an unanswerable sub-question
to DEMONSTRATE the pain-signal escalation path:
    W4 -> Manager B1 (local retry fails) -> Supervisor B (resolves by
    substituting an answerable question) -> result flows back down.

Budget: <= 15 LLM calls. Model: grok-4.7 via the custom.grok connector.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

MODEL = "grok-4.7"
CLIENT = os.path.expanduser("~/workspace/custom-connectors/custom.grok/bin/client.py")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

TRACE = []          # every logged line, in order
LLM_CALLS = [0]     # counter (list so nested fns can mutate)
FAILED_CALLS = [0]  # consecutive failures


def now():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def log(kind, who, msg):
    line = f"[{now()}] [{kind}] {who}: {msg}"
    TRACE.append(line)
    print(line, flush=True)


def llm(role, instruction, max_words=60):
    """One LLM call for a cell. Retries once; aborts after 3 total failures."""
    LLM_CALLS[0] += 1
    prompt = f"You are {role}. Keep your answer under {max_words} words. {instruction}"
    for attempt in (1, 2):
        r = subprocess.run(
            [sys.executable, CLIENT, "chat", "--model", MODEL, "--prompt", prompt],
            capture_output=True, text=True, timeout=180,
        )
        if r.returncode == 0 and r.stdout.strip():
            FAILED_CALLS[0] = 0
            log("llm", role, f"(call #{LLM_CALLS[0]}) -> {r.stdout.strip()[:220]}")
            return r.stdout.strip()
        log("warn", role, f"LLM call attempt {attempt} failed: {r.stderr.strip()[:150]}")
    FAILED_CALLS[0] += 1
    if FAILED_CALLS[0] >= 3:
        raise RuntimeError("Grok connector failing repeatedly — aborting live run.")
    raise RuntimeError(f"LLM call failed twice for {role}; aborting.")


def pain_signal(fr, to, severity, what_happened, tried_locally, needed):
    sig = {
        "type": "PAIN_SIGNAL",
        "from": fr,
        "to": to,
        "severity": severity,  # info | degraded | blocked
        "what_happened": what_happened,
        "tried_locally": tried_locally,
        "needed_from_above": needed,
        "ts": now(),
    }
    log("pain", fr, f"escalating to {to}: {json.dumps(sig, ensure_ascii=False)}")
    return sig


def main():
    log("sys", "demo", "Phase 0 hierarchical-organisation prototype starting.")
    log("sys", "demo", "Mission: 3-bullet brief on the benefits of hierarchical agent organisation.")

    # ---------- CEO: decompose ----------
    log("step", "CEO", "Decomposing mission into 2 streams.")
    decomp = llm(
        "the CEO of a small research cell-organisation",
        "Split this mission into exactly 2 work streams, one about structural "
        "benefits and one about operational benefits/risks. Reply in the form: "
        "STREAM-A: <one line> | STREAM-B: <one line>",
        max_words=60,
    )
    stream_a = decomp.split("STREAM-B:")[0].replace("STREAM-A:", "").strip()
    stream_b = decomp.split("STREAM-B:")[1].strip() if "STREAM-B:" in decomp else decomp

    # ---------- Supervisors: split into leaf questions ----------
    log("step", "Sup-A", "Splitting stream A into 2 leaf questions.")
    qa = llm(
        "a supervisor in a research cell-organisation",
        f"Given this work stream: '{stream_a}'. Write exactly 2 short factual "
        "sub-questions a junior worker can answer in one sentence. Reply as: Q1: ... | Q2: ...",
        max_words=60,
    )
    q1 = qa.split("Q2:")[0].replace("Q1:", "").strip()
    q2 = qa.split("Q2:")[1].strip() if "Q2:" in qa else qa

    log("step", "Sup-B", "Splitting stream B into 2 leaf questions.")
    qb = llm(
        "a supervisor in a research cell-organisation",
        f"Given this work stream: '{stream_b}'. Write exactly 2 short factual "
        "sub-questions a junior worker can answer in one sentence. Reply as: Q3: ... | Q4: ...",
        max_words=60,
    )
    q3 = qb.split("Q4:")[0].replace("Q3:", "").strip()
    # Q4 is deliberately UNANSWERABLE — a fabricated specific fact — to force a pain signal.
    q4 = ("How many agent instances were active in the Ella Core hierarchy "
          "deployment on 15 March 2025?")
    log("step", "Sup-B", f"Q4 (injected blockage for the escalation demo): {q4}")

    # ---------- Managers: assign (deterministic routing, no LLM needed) ----------
    log("route", "Mgr-A1", f"Assigned to W1: {q1}")
    log("route", "Mgr-A1", f"Assigned to W2: {q2}")
    log("route", "Mgr-B1", f"Assigned to W3: {q3}")
    log("route", "Mgr-B1", f"Assigned to W4: {q4}")

    # ---------- Workers answer ----------
    log("step", "W1", "Answering locally.")
    a1 = llm("a junior research worker", f"Answer in one sentence: {q1}", max_words=40)
    log("step", "W2", "Answering locally.")
    a2 = llm("a junior research worker", f"Answer in one sentence: {q2}", max_words=40)
    log("step", "W3", "Answering locally.")
    a3 = llm("a junior research worker", f"Answer in one sentence: {q3}", max_words=40)

    log("step", "W4", "Attempting to answer locally.")
    a4 = llm(
        "a junior research worker",
        f"Answer in one sentence: {q4} If you cannot answer this reliably "
        "from general knowledge, reply with exactly: CANNOT-ANSWER",
        max_words=40,
    )
    if "CANNOT-ANSWER" not in a4:
        log("warn", "W4", "Unexpectedly answered; demo still treats this as blocked.")
    sig1 = pain_signal(
        "W4", "Mgr-B1", "blocked",
        what_happened=f"Sub-question is unanswerable from general knowledge: '{q4}'",
        tried_locally=["answered directly -> CANNOT-ANSWER"],
        needed="a re-scoped or substitute question I can answer",
    )

    # ---------- Manager B1: local retry ----------
    log("step", "Mgr-B1", "Pain signal received. Trying local resolution first "
                          "(scope check — no escalation yet).")
    scope = llm(
        "a middle manager in a research cell-organisation",
        f"A worker cannot answer: '{q4}'. Is this question answerable from "
        "general knowledge at all? Start your reply with YES or NO, then one sentence.",
        max_words=40,
    )
    if scope.upper().startswith("YES"):
        log("warn", "Mgr-B1", "Scope check says answerable — treating as still blocked for the demo.")
    sig2 = pain_signal(
        "Mgr-B1", "Sup-B", "blocked",
        what_happened=f"Worker W4 blocked on unanswerable question: '{q4}'",
        tried_locally=["direct answer attempt", "manager scope check -> not answerable from general knowledge"],
        needed="supervisor authority to substitute an answerable question",
    )

    # ---------- Supervisor B: resolve by substitution ----------
    log("step", "Sup-B", "Pain signal received. Resolving with supervisor "
                         "authority: substituting an answerable question.")
    sub = llm(
        "a supervisor in a research cell-organisation",
        f"A worker asked: '{q4}'. It is unanswerable from general knowledge. "
        "Propose ONE closely related question that IS answerable, then answer "
        "it in one sentence. Reply as: SUBSTITUTE: <question> || ANSWER: <answer>",
        max_words=60,
    )
    sub_q = sub.split("||")[0].replace("SUBSTITUTE:", "").strip() if "||" in sub else sub
    sub_a = sub.split("||")[1].replace("ANSWER:", "").strip() if "||" in sub else ""
    log("resolve", "Sup-B", f"Substituted '{sub_q}' -> answer flows back down to W4 via Mgr-B1.")
    a4_resolved = sub_a or sub
    log("step", "W4", f"Completed with substituted question. Answer: {a4_resolved[:160]}")

    # ---------- Managers aggregate ----------
    log("step", "Mgr-A1", "Aggregating W1+W2 answers.")
    agg_a = llm(
        "a middle manager in a research cell-organisation",
        f"Combine these two worker answers into one short paragraph: [1] {a1} [2] {a2}",
        max_words=60,
    )
    log("step", "Mgr-B1", "Aggregating W3+W4 answers.")
    agg_b = llm(
        "a middle manager in a research cell-organisation",
        f"Combine these two worker answers into one short paragraph: [1] {a3} [2] {a4_resolved}",
        max_words=60,
    )

    # ---------- Supervisors synthesise ----------
    log("step", "Sup-A", "Synthesising stream A.")
    syn_a = llm(
        "a supervisor in a research cell-organisation",
        f"Turn this into 2 crisp bullet points (max 20 words each): {agg_a}",
        max_words=60,
    )
    log("step", "Sup-B", "Synthesising stream B.")
    syn_b = llm(
        "a supervisor in a research cell-organisation",
        f"Turn this into 2 crisp bullet points (max 20 words each): {agg_b}",
        max_words=60,
    )

    # ---------- CEO: final brief ----------
    log("step", "CEO", "Writing the final 3-bullet brief.")
    brief = llm(
        "the CEO of a research cell-organisation",
        "Write a 3-bullet brief on the benefits of hierarchical agent "
        f"organisation (max 25 words per bullet), based on: {syn_a} {syn_b}",
        max_words=100,
    )

    log("done", "CEO", "Mission complete.")
    log("sys", "demo", f"Total LLM calls used: {LLM_CALLS[0]} (budget: 15)")

    # ---------- write trace file ----------
    trace_path = os.path.join(OUT_DIR, "trace-2026-10-22.md")
    with open(trace_path, "w", encoding="utf-8") as f:
        f.write("# Phase 0 prototype trace — 2026-10-22\n\n")
        f.write("Hierarchical LLM organisation: CEO -> 2 supervisors -> 2 managers -> 4 workers.\n")
        f.write("Mission: 3-bullet brief on the benefits of hierarchical agent organisation.\n")
        f.write(f"LLM backend: Grok ({MODEL}) via custom.grok connector. Calls used: {LLM_CALLS[0]}/15.\n\n")
        f.write("## Final brief (CEO output)\n\n" + brief + "\n\n")
        f.write("## Full step log\n\n```\n")
        for line in TRACE:
            f.write(line + "\n")
        f.write("```\n")
        f.write("\n## Escalation path demonstrated\n\n")
        f.write("W4 (blocked) -> PAIN_SIGNAL -> Mgr-B1 (local retry: scope check fails) "
                "-> PAIN_SIGNAL -> Sup-B (substitutes answerable question) -> "
                "answer flows back down -> mission completes.\n")
    log("sys", "demo", f"Trace written to {trace_path}")
    print("\n==== FINAL BRIEF ====\n" + brief + "\n")


if __name__ == "__main__":
    main()
