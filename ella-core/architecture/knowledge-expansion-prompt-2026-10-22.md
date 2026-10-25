You are helping expand the knowledge base for Project ELLA — a personal AI companion built as a file-backed cognitive architecture ("the folder is the mind"): typed memory (episodic / semantic / procedural / prospective / affective / social), versioned identity, a permission boundary between intent and action, scheduled background consolidation ("growth cycles", "dream cycles"), and hybrid retrieval into a language model treated as replaceable compute.

Context I am sharing alongside this prompt (attached):
1. The current architecture map (ella/ folder tree, ~110 files, phased build, load rules, boot sequence, YAML file template)
2. The safety/governance specification (Session / Governor / Executor three-tier action boundary, action proposal schema)
3. The identity philosophy (three-timescale genome, Unified Will gate, "living architecture, models as replaceable compute")
4. The scientific reference blueprint (11-layer hierarchy, active inference / predictive processing, 424 files, state variables with decay rates and baselines)

Your job has two parts.

## PART A — RESOLVE OPEN QUESTIONS

The following are genuinely unresolved in the current material. For each, propose a CONCRETE mechanism — not poetry, not restated principles. Specify data structures, algorithms, update rules, or testable procedures. Where you cannot give a mechanism, say so explicitly and state what experiment or evidence would settle it.

**Q1. RETRIEVAL SCORING.** Every source agrees retrieval should combine recency, relevance, emotion, and surprise — none gives the actual scoring function. Propose one: exact factors, weights, normalization, combination rule. Critically, the spec warns "retrieval frequency must NOT automatically increase factual confidence." Propose the mechanism enforcing this — how do activation, retrieval priority, confidence, and erasure stay independent quantities?

**Q2. CONFLICT RESOLUTION.** When new evidence contradicts a stored memory, what is the exact protocol? Specify the versioning format, the supersedes / superseded-by chain, when to branch vs overwrite vs flag, and the precise conditions under which the human owner is asked to adjudicate.

**Q3. CONFIDENCE ACCOUNTING.** Every spec demands confidence + provenance + validity intervals on durable memories; none says how confidence is computed or updated. Propose the update rule (Bayesian, heuristic, or other), what updates it, and what happens on confirming vs contradicting evidence.

**Q4. FORGETTING CURVES.** Everyone agrees memories should decay and compress — with what function? Propose the decay curve (Ebbinghaus, salience-weighted, other), its parameters, what triggers compression vs deletion, and what is irrecoverable once deleted.

**Q5. THE GOVERNOR LINE.** The three-tier Session / Governor / Executor boundary is clean on paper. Specify the risk taxonomy concretely: place at least 10 worked real actions (from "draft a message" to "delete a file" to "spend money") into tiers, and say exactly where "draft" ends and "act" begins.

**Q6. UNIFIED WILL MECHANICS.** The identity spec proposes a "Unified Will" gate — every proposed action passes through one coherent will before execution. Propose the implementation: a constraint-checking pass? A separate model call with a specific prompt? A rule engine? Give the actual mechanism.

**Q7. DREAM VALIDATION.** The offline reflection pipeline produces "insights" from recombined memories. Propose validation criteria separating real insight from spurious pattern — what tests must a candidate insight pass before promotion into durable memory?

**Q8. AFFECT-TO-BEHAVIOR MAPPING.** The design uses neuromodulator-style dials (dopamine-like, serotonin-like, etc., 0.0–1.0). Propose the principled mapping from dial values to actual response behavior (tone, pacing, initiative, risk tolerance). How do we know a dial does real work vs being a poetic label? Design the ablation test.

**Q9. CONTEXT BUDGET COMPRESSION.** The always-loaded core (identity, genome summary, mood, state vector, guardians, bond summary) must fit in a few thousand tokens. Propose the compression format: exact contents, ordering, and truncation rules when the budget is exceeded.

**Q10. MODEL SWAPS.** The philosophy says the language model is replaceable compute and identity lives in the files. What actually breaks when the underlying model is swapped? Propose the continuity test suite: what must be verified after a swap, and what is expected to be lost?

## PART B — INDEPENDENT CONVERGENCE TEST

The claims below underpin the project. You are one of two AIs being asked these questions INDEPENDENTLY — reason from first principles and the evidence you know, not from the attached docs. For each claim state: AGREE / DISAGREE / PARTIAL, your confidence (0–100%), your 2–3 strongest reasons, and the strongest counterargument against your own position. If you disagree, propose the alternative you would build instead.

- **C1.** File-backed, human-readable memory (Markdown + frontmatter, git-versioned) produces better long-term identity continuity than vector-database-only memory.
- **C2.** Retrieval frequency must never increase factual confidence; activation, priority, confidence, and erasure are independent quantities.
- **C3.** A three-tier action boundary (interpreter / governor / executor) is the right safety architecture for a personal agent with tool access.
- **C4.** Biological and psychological metaphors (dopamine dials, sleep cycles, dreams) are legitimate as functional design analogies but must never be presented as claims about inner experience.
- **C5.** The right context architecture is a small always-loaded core plus on-demand retrieval, rather than maximum context every turn.
- **C6.** Background growth and consolidation require an external scheduler; the agent cannot reliably wake itself.
- **C7.** Identity and relationship continuity can survive swapping the underlying language model, provided the memory files and identity records persist.
- **C8.** Every durable memory needs provenance (source), confidence, and validity interval — memories without these are liabilities.
- **C9.** For creative and synthesis work, multi-source synthesis with added value beats single-source transformation. (This is a standing project rule — test whether you independently agree, and why.)

## OUTPUT RULES

- Structure your answer exactly as: Part A (Q1–Q10), then Part B (C1–C9).
- Part A: mechanism first, then the open remainder (what is still unknown + what would settle it).
- Part B: verdict, confidence, reasons, strongest counterargument — for every claim.
- Be concrete: name data structures, give formulas where applicable, give worked examples.
- Cite real sources (papers, systems, prior art) wherever your mechanism draws on existing work.
- Mark speculation explicitly. Never present a hypothesis as an established result.
- If any Persian text appears, use standard written Persian with regular spaces only — never the zero-width non-joiner (U+200C).
- Do not moralize about the project or lecture about AI safety in the abstract; engage with the engineering questions as asked.
