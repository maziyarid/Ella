# Phase 2 smoke-test trace — 2026-10-22

Integrated tree: Governor (CEO layer, `00_KERNEL/governor.py`) -> 12_REFERENCES cluster supervisor (`00_KERNEL/supervisors.py`) -> 2 workers -> Executor aggregation (`00_KERNEL/executor.py`) -> Governor brief.
Mission (tiny, real): two design lessons for Ella's memory system — one from Global Workspace Theory, one from Complementary Learning Systems.
LLM backend: Grok via ella/lib/router.py. Executor calls: 3; Governor calls: 2.
Pain signals: {'info': 0, 'degraded': 1, 'blocked': 0} (1 degraded, resolved locally by the supervisor). Pain seen by Governor: 0.

## Final brief (Governor output)

**Final brief**

Both claims stand. No revision required.

- Global Workspace Theory (Baars 1988; Dehaene et al. 1998): selection is competitive, then a global broadcast—not all-to-all shouting.
- Complementary Learning Systems (McClelland et al. 1995): fast episodic capture, slow neocortical consolidation, and offline replay.
- Sources confirmed. Direction holds: model broadcast after competition, and separate fast and slow learning with replay.

## Escalation demonstrated

- **degraded**: w2 vague question -> AMBIGUOUS -> pain(degraded) -> sup-12 re-scoped locally -> w2 retry completed. Governor never involved.

## Full step log

```
[12:10:27] [sys] smoke: Phase 2 smoke test starting. Mission: Extract two design lessons for Ella's memory system: one from Global Workspace Theory, one from Complementary Learning Systems.
[12:10:27] [phase] governor: Policy gate: authorizing mission.
[12:10:33] [phase] governor: Decomposed. STREAM-A assigned to 12_REFERENCES supervisor (STREAM-B out of smoke scope).
[12:10:33] [phase] sup-12: Supervisor card loaded: duty='Research open questions and log sources with what they changed. Unveri...' threshold=degraded
[12:10:36] [llm] sup-12: (via grok) -> Q1: What design lesson does Global Workspace Theory state? | Q2: What design lesson does Complementary Learning Systems state?
[12:10:36] [phase] executor: Assigning 2 workers in parallel.
[12:11:00] [step] w1: Completed locally (confidence: high).
[12:11:00] [step] sup-12: degraded pain received. Tier rule: resolve LOCALLY, do not escalate. Re-scoping.
[12:11:02] [llm] sup-12: (via grok) -> What design lesson does Complementary Learning Systems theory offer for building a memory system that separates fast episodic storage from slow structured conso
[12:11:09] [step] sup-12: Degraded signal resolved locally — Governor never involved.
[12:11:09] [phase] executor: Supervisor aggregating worker answers.
[12:11:19] [llm] sup-12: (via grok) -> Both claims hold and need no revision. Global Workspace Theory (Baars 1988; Dehaene, Kerszberg & Changeux 1998) supports competitive selection then global broad
[12:11:19] [phase] governor: Writing final brief from supervisor synthesis.
[12:11:24] [done] governor: Mission complete.
[12:11:24] [sys] smoke: Executor calls this process: 3. Governor calls: 2. Pain signals: {'info': 0, 'degraded': 1, 'blocked': 0}. Pain seen by Governor: 0 (must be 0).
```
