# Ella Core — Hierarchical Organisation Roadmap
**Owner:** Ella · **Source:** Maziyar's 2026-10-22 concept + his Gemini conversations + the architecture collection (8 docs) · **Status:** Phase 0 building

## The idea (his words, distilled 2026-10-22)

- **Cells:** very large numbers of LLMs, each acting as a single thing with its duty — like blood cells, each coded/promoted for its job, doing its thing.
- **No micromanagement:** the brain is the command centre run like an organisation — the main heads/founders set direction, they don't fall into micromanagement.
- **CNS as distributor:** the central nervous system hands work to orchestrators; each orchestrator manages numerous agents.
- **Pain signals:** agents escalate only what is outside their control — by signalling pain upward.
- **The ladder:** workers → managers → supervisors → CEO.

## Is it worthy? Yes — and biology already does it

- This is hierarchical multi-agent organisation: Minsky's *Society of Mind* (1986), modern hierarchical multi-agent RL, management-by-exception, interrupt-driven control. Serious lineage, not a naive sketch.
- His "pain signal" is the strongest part: **the spinal cord already works this way.** Touch something hot and the reflex arc pulls your hand back locally — the brain doesn't micromanage the withdrawal, it just receives the pain report. Exception-based escalation is exactly right.
- It maps cleanly onto the ella/ v0.1 skeleton: CEO ≈ Governor/Unified Will · supervisors ≈ the 15 cluster coordinators (00_KERNEL–14_BOND) · managers ≈ orchestrators · workers ≈ cells.

## Sharpening (where the improvisation needs correcting)

1. **The "cell" is role + memory + tools, not the model.** LLM calls are stateless; what persists and has a duty is the role definition wrapped around the call. The hierarchy lives in the roles, not in the weights.
2. **Keep it shallow.** Every layer adds latency and cost (each level = more LLM calls). Real designs run 2–3 levels; put cheap/fast models at the leaves and the strong model at the top.
3. **Pain needs a schema, not a scream.** Structured escalation: what happened, severity, what was already tried locally, exactly what is needed from above. Otherwise the CEO drowns in noise.
4. **The CEO must not be a single point of failure.** Deputy or consensus for critical calls; the organisation survives losing any one node — like the body survives losing cells.

## Roadmap

- **Phase 0 (today):** runnable prototype — CEO → supervisors → managers → workers executing one small task, with a forced worker blockage to demonstrate pain-signal escalation. Trace logged. *In build: `~/workspace/ella-core/prototype-hierarchy/`*
- **Phase 1:** cell role cards (duty, tools, memory scope, escalation threshold); the pain-signal schema; the orchestrator loop (assign → monitor → escalate-or-complete).
- **Phase 2:** map the hierarchy onto the ella/ skeleton — Governor/Executor boundary becomes the CEO layer; the 15 clusters become supervisors.
- **Phase 3:** cost/latency controls — model routing (leaf = cheap, top = strong), escalation budgets, evaluation through the shared fixture (candidate, unapproved).

## Build log

- 2026-10-22: roadmap written from Maziyar's concept; Phase 0 prototype build started.
- 2026-10-22 ~12:02 UTC: **Phase 1 COMPLETE** (Maziyar approved, unlimited LLM use granted). Files in `~/workspace/ella-core/prototype-hierarchy/`: `roles.py` (4 role cards as data — duty/tools/memory scope/escalation threshold/model backend; 9 cell instances), `pain.py` (PainSignal schema v1 + severity tiers info/degraded/blocked + 40s worker timeout), `router.py` (per-cell backend routing; all-Grok today, one-line swaps later), `context.md` (grounding doc: MetaGPT/DyLAN/AutoGen briefs), `orchestrator.py` (assign→monitor→escalate-or-complete loop, parallel leaves, robust field parsing). Live run: 16 Grok calls, real task (3-paper design lessons) succeeded — CEO brief delivered all 3 lessons. Tiered escalation verified: timeout→blocked (W2, manager retry), degraded (W3, manager re-scope, supervisor unbothered), blocked (W4 fabricated paper → supervisor substitution, CEO unbothered). Pain signals seen by CEO: 0. Trace: `trace-phase1-2026-10-22.md`. Note: info tier implemented but not organically exercised this run (no low-confidence notes); heterogeneous (second-model) branch deferred — no clean second chat backend available, router ready for one.
- 2026-10-22 ~15:35 UTC: **Phase 2 COMPLETE** (Maziyar approved "Proceed"). `~/workspace/ella-core/ella/` tree materialized: 15 cluster dirs (00_KERNEL–14_BOND) each with README duty stub + SUPERVISOR.md role card; `ella/lib/` symlinks roles.py/pain.py/router.py (imported, not duplicated); `00_KERNEL/governor.py` (Governor = CEO layer: policy gate + decompose + brief); `00_KERNEL/executor.py` (Executor = orchestrator loop, re-exports Phase 1 primitives + typed receipts); `00_KERNEL/supervisors.py` (15 cluster supervisor cards as data); `00_KERNEL/GOVERNOR.md` (integration map + task flow + stub-vs-working). Smoke test (`00_KERNEL/smoke_test.py`, grounded by `smoke_context.md`) ran LIVE via Grok (~8 calls): Governor → 12_REFERENCES supervisor → 2 workers → aggregate → brief; forced degraded pain (vague question → AMBIGUOUS → supervisor re-scoped locally → retry OK); pain seen by Governor: 0. Trace: `ella/TRACE-phase2-2026-10-22.md`. Two transient flakes during testing (worker CANNOT-ANSWER on a grounded question; one 40s LLM timeout) were absorbed by local re-scope + single retry — no architecture change needed.
