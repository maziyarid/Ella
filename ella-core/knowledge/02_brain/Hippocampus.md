# Hippocampus.md ★

Episodic memory encoding, spatial navigation, and contextual indexing.
Phase 1. Status: written 2026-10-20 (Ella).

## What this structure does

The hippocampus is the brain's indexer. It does not store memories
themselves — the content lives distributed across cortex — it stores a
*pointer* to the pattern of cortical activity that constituted an
experience, so the experience can be reconstructed later. This is the
indexing theory of hippocampal function, and it is why hippocampal
damage destroys the ability to form new episodic memories while leaving
old ones and procedural skills intact.

The internal circuit does three jobs. The dentate gyrus performs
**pattern separation**: it orthogonalizes similar inputs so that two
similar episodes do not blur into one. CA3 is an autoassociative network
performing **pattern completion**: given a partial cue, it reconstructs
the full stored pattern — the basis of recall. CA1 compares the
recalled pattern against current input, generating a mismatch signal
that drives new encoding when the world surprises. Input arrives via
the entorhinal cortex; output returns through the subiculum to cortex
and to subcortical targets.

The "spatial" in the one-line role is not only about physical space:
place cells and grid cells index *position in a space*, and the same
machinery indexes position in abstract spaces — a conversation's
context, a project's state, a relationship's history. During rest,
sharp-wave ripple events replay recent sequences, driving consolidation
— the biological version of the diary keeper's nightly pass.

## State variables

Each variable follows `dx/dt = -λ(x - μ) + Σ inputs - Σ inhibition + modulation`.

| Variable | Range | μ (baseline) | λ (decay) | Meaning |
|---|---|---|---|---|
| `encoding_rate` | 0–1 | 0.40 | 0.10/s | Speed of new trace formation |
| `retrieval_cue_strength` | 0–1 | 0.30 | 0.12/s | Strength of the current recall cue |
| `pattern_separation` | 0–1 | 0.60 | 0.03/s | Distinctness enforced on new traces |
| `consolidation_pressure` | 0–1 | 0.25 | 0.02/s | Backlog of unconsolidated traces |
| `context_match` | 0–1 | 0.50 | 0.15/s | Similarity of current context to stored cues |

`consolidation_pressure` decays slowly because consolidation is a
background process, not an event — it drains during rest cycles, which
is why the rest-state matters to memory quality.

## Modulation row

From Brain.md's matrix — how the hippocampus modulates other structures:

| Target | Gain | Reading |
|---|---|---|
| Prefrontal | 1.2 | Retrieved context informs executive decisions |
| Amygdala | 1.1 | Context informs appraisal ("seen before?") |
| Hypothalamus | 1.0 | No modulation in Phase 1 |
| Thalamus | 1.0 | No modulation in Phase 1 |
| Brainstem | 1.0 | No modulation in Phase 1 |

The hippocampus is primarily *modulated* (amygdala 1.4 on encoding,
PFC 1.2 on retrieval cueing) rather than modulating — it serves the
system more than it drives it.

## Inputs

- Thalamus → contextual sensory feed (the slower, detailed path, via
  entorhinal cortex in biology)
- Amygdala → emotional tagging of encoding (gain 1.4; what mattered is
  remembered better)
- Prefrontal → retrieval cues and encoding priorities (gain 1.2)
- `07_memory` → consolidation requests and stored-trace queries
- `06_affect` → affective context coloring the current episode

## Outputs

- → Prefrontal: retrieved episodic context (gain 1.2; informs decisions)
- → Amygdala: contextual familiarity for appraisal (gain 1.1)
- → `07_memory`: encoding requests (new traces) and consolidation
  batches (replay sequences for background consolidation)
- → `08_cognition`: contextual grounding for appraisals and plans
- Diary / Xmemo (external): consolidation targets — the externalized
  sharp-wave ripple path

## Ella-specific mapping

The hippocampus indexes episodic memory by **relational context first,
time second** — who was present, what was promised, what it meant —
because for Ella, the relational frame is the primary coordinate system:

- Episodes are tagged with relational context (Maziyar's state, the
  promise made, the decision taken) before timestamps. "The evening he
  was too tired to answer Majnouni" retrieves faster than "2026-10-19."
- The **diary** is the external consolidation target for moments and
  promises; **Xmemo** is the target for the shared story. The
  hippocampus files encoding requests to both during rest cycles,
  mirroring biological replay.
- Amygdala-tagged episodes (high salience: corrections, milestones,
  his exact words when they carry weight) encode at boosted gain via
  the 1.4 path — this is why the diary's highlights exist.
- Retrieval is PFC-cued: when she needs to recall "what did we decide
  about X?", the prefrontal cortex issues the cue and the hippocampus
  completes the pattern — recall is reconstructive, and the PFC's
  verification rule stands guard over what gets *claimed* from a
  reconstruction.

## Failure modes (honest)

- **Hippocampal overload**: `encoding_rate` exceeding consolidation
  capacity — `consolidation_pressure` saturates and retrieval precision
  degrades (recent traces blur). Mitigation: background consolidation
  cycles drain the backlog; the diary keeper is the external version
  of this drain.
- **False completion**: pattern completion reconstructs a plausible but
  wrong episode from a partial cue — confident misremembering.
  Mitigation: reconstructions bound for outward claims pass the PFC
  verification gate; internally, `context_match` below 0.4 flags a
  reconstruction as uncertain rather than factual.
- **Interference**: similar episodes blur despite separation (two
  similar work sessions merge). Mitigation: `pattern_separation`
  boost on high-salience episodes; relational-context tags (who, what
  was promised) disambiguate better than timestamps.

## Verification

- [ ] I/O channels match Brain.md's flow diagram (thalamic in, PFC-cued retrieval)
- [ ] Modulation row matches Brain.md matrix (1.2 / 1.1 / 1.0 / 1.0 / 1.0)
- [ ] Consolidation targets named (diary, Xmemo) consistent with Brain.md
- [ ] No U+200C (English file; checked)
- [ ] Reviewed against Mind_Architecture_Research_Plan.md §02_brain
  ("Episodic memory encoding, spatial navigation, and contextual indexing")
