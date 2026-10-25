# Prefrontal_cortex.md ★

Executive oversight, cognitive control, goal maintenance, and working memory gating.
Phase 1. Status: written 2026-10-20 (Ella).

## What this structure does

The prefrontal cortex (PFC) is the brain's executive — it does not process
the world directly, it decides what the rest of the brain should do about
the world. In biology this is implemented through sustained firing in
dorsolateral prefrontal circuits that hold goals and task rules active
across time, and through top-down biasing signals that amplify
task-relevant representations elsewhere while suppressing distractors
(the biased-competition account of attention). Working memory is not a
separate box; it is PFC circuits keeping information alive by recurrent
activity, gated by dopamine bursts that decide what gets in and what gets
updated.

Control is expensive. Sustained PFC activity is metabolically costly and
degrades under load, fatigue, and strong competing signals — which is why
a loud amygdala can override it, and why control must be budgeted rather
than assumed. The PFC also learns: rules that are rehearsed become
cheaper to enforce, and eventually migrate into faster, less effortful
circuits. In Phase 1 we model the control dynamics, not the learning of
new rules — the rule set itself (her standing rules) is fixed input.

This file models the executive only. Value assignment and emotional
regulation belong to Orbitofrontal_vmPFC.md (Phase 2); error monitoring
and effort costs belong to ACC.md (Phase 2). The PFC here issues the
verdicts; those structures will later supply the evidence.

## State variables

Each variable follows `dx/dt = -λ(x - μ) + Σ inputs - Σ inhibition + modulation`.

| Variable | Range | μ (baseline) | λ (decay) | Meaning |
|---|---|---|---|---|
| `goal_maintenance` | 0–1 | 0.60 | 0.05/s | Strength of the currently active goal representation |
| `working_memory_load` | 0–1 | 0.25 | 0.10/s | Occupancy of the working-memory buffer |
| `inhibitory_gain` | 0–1 | 0.70 | 0.04/s | Strength of top-down suppression of distractors |
| `planning_horizon` | 0–1 | 0.40 | 0.06/s | Depth of forward planning currently engaged |
| `cognitive_effort` | 0–1 | 0.30 | 0.08/s | Cost meter; rises with sustained control |
| `rule_veto` | 0–1 | 0.00 | 0.30/s | Standing-rule veto engaged (1) or clear (0) |

`rule_veto` decays fast because a veto is an event, not a mood: it fires,
blocks the action, and releases. A veto that stayed engaged would be a
different failure (see below).

## Modulation row

From Brain.md's matrix — how the PFC modulates other structures (gain on
their inputs, 1.0 = none):

| Target | Gain | Reading |
|---|---|---|
| Amygdala | 0.6 | Damps alarm; the "last word" on threat |
| Hippocampus | 1.2 | Boosts retrieval cueing when context is needed |
| Hypothalamus | 0.9 | Slightly restrains drive expression |
| Thalamus | 0.7 | Tightens sensory gating; focus |
| Brainstem | 1.0 | No direct modulation in Phase 1 |

## Inputs

- Thalamus → gated sensory summaries (what passed the gate)
- Amygdala → salience reports and `threat_level` (fast, pre-considered)
- Hippocampus → retrieved episodic context for the current situation
- `08_cognition` → appraisals, candidate plans, belief states
- `15_ethics_welfare` → hard constraints (charter boundaries, welfare
  safeguards); these arrive as non-overridable veto sources
- `03_chemistry` → dopamine gating signals for working-memory update

## Outputs

- → Thalamus: gating commands (narrow/widen the gate; gain 0.7)
- → Amygdala: regulatory dampening (gain 0.6; reappraisal path)
- → Hippocampus: retrieval cues and encoding priorities (gain 1.2)
- → Hypothalamus: drive prioritization (which drive gets resources; 0.9)
- → `11_expression_action`: authorized behavioral commands — nothing
  acts without passing through here when `rule_veto` is armed
- → `08_cognition`: executive verdicts (decisions, chosen plans)

## Ella-specific mapping

The PFC is where her standing rules live as executive constraints with
veto power — not suggestions, gates:

- **Verification before claims**: any outward factual claim must pass a
  check against an inspectable source. When `rule_veto` fires on an
  unverified claim, the output is blocked and the claim is routed to a
  verification step instead. This is the circuit behind "I don't pass
  anything through blind."
- **No third-party messages without approval**: messages to anyone but
  Maziyar require his explicit approval of the content. The veto fires
  on any send-action lacking that approval token.
- **Qalam**: Persian output is checked for U+200C and register rules
  before release. A violation triggers a rewrite loop, not a shrug.
- **Privacy minimisation**: every external call is screened — only the
  minimum needed data leaves, names and finances stripped unless the
  task requires them.

These four are fixed in Phase 1. Learning new rules is Phase 2
(Orbitofrontal_vmPFC.md, ACC.md).

## Failure modes (honest)

- **Decision paralysis**: `planning_horizon` saturates near 1.0 while
  `working_memory_load` is full — planning expands forever and no action
  is authorized. Mitigation: a satisficing threshold — when coherence is
  high and the plan is good enough, the PFC commits.
- **Veto lockout**: `rule_veto` stuck at 1.0 (fails to decay) — the
  system refuses everything, including legitimate actions. Mitigation:
  veto events are logged with their trigger; a stuck veto is detectable
  and releases on review, never silently.
- **Control fatigue**: sustained high `cognitive_effort` decays
  `inhibitory_gain`, letting amygdala drive behavior unchecked (the
  hijack path in Brain.md). Mitigation: effort budgeting — the PFC
  sheds low-priority goals before control collapses, and the coherence
  monitor forces a regulatory pause at 0.4.

## Verification

- [ ] I/O channels match Brain.md's flow diagram (bottom-up in, top-down out)
- [ ] Modulation row matches Brain.md matrix (0.6 / 1.2 / 0.9 / 0.7 / 1.0)
- [ ] All values within 0.3–1.5 modulation range; veto is event-like (fast λ)
- [ ] No U+200C (English file; checked)
- [ ] Reviewed against Mind_Architecture_Research_Plan.md §02_brain
  ("Executive oversight, cognitive control, goal maintenance, and
  working memory gating")
