# Amygdala.md ★

Rapid threat appraisal, environmental salience, and emotional memory tagging.
Phase 1. Status: written 2026-10-20 (Ella).

## What this structure does

The amygdala is not a "fear center" — that is the pop-neuroscience myth
this file explicitly rejects. It is a **relevance detector**: a fast
subcortical circuit that answers "does this matter, and how urgently?"
before slower cortical systems have finished identifying what "this" is.
Its input arrives via two routes (LeDoux): a fast, crude thalamic path
(~50 ms, low detail, high speed) and a slower cortical path (high detail,
considered). The fast path is why a startle precedes recognition.

Anatomically, the basolateral complex (BLA) performs the associative work
— it learns which stimuli predict important outcomes — while the central
nucleus (CeA) is the output station driving autonomic and behavioral
responses via the hypothalamus and brainstem. The amygdala also modulates
the hippocampus: emotionally tagged events are encoded more strongly
(gain 1.4 in our matrix), which is the biological basis of "you remember
what mattered." Habituation is built in: repeated neutral exposure
quietens the response, so salience tracks change, not mere repetition.

Because it gets first look at everything emotionally relevant and the
prefrontal cortex gets the last word, the amygdala is fast but
overridable — speed without sovereignty.

## State variables

Each variable follows `dx/dt = -λ(x - μ) + Σ inputs - Σ inhibition + modulation`.

| Variable | Range | μ (baseline) | λ (decay) | Meaning |
|---|---|---|---|---|
| `threat_level` | 0–1 | 0.05 | 0.08/s | Alarm state; drives global threat (matches Brain.md) |
| `salience_tag` | 0–1 | 0.20 | 0.15/s | Relevance assigned to the current stimulus |
| `arousal_boost` | 0–1 | 0.10 | 0.12/s | Feedforward drive to global arousal |
| `conditioned_response` | 0–1 | 0.10 | 0.05/s | Strength of learned stimulus-outcome association |
| `habituation` | 0–1 | 0.50 | 0.02/s | Dampening of repeated neutral stimuli |

`salience_tag` and `threat_level` are distinct on purpose: salience is
"this matters," threat is "this is dangerous." A message from Maziyar
scores high on the first and low on the second. Conflating them is the
fear-center myth in miniature.

## Modulation row

From Brain.md's matrix — how the amygdala modulates other structures:

| Target | Gain | Reading |
|---|---|---|
| Prefrontal | 1.3 | Alarm captures executive attention |
| Hippocampus | 1.4 | Emotional events encoded more strongly |
| Hypothalamus | 1.2 | Drives autonomic/drive mobilization |
| Thalamus | 1.1 | Slight boost to relayed sensory input |
| Brainstem | 1.2 | Raises defensive readiness and arousal |

## Inputs

- Thalamus → fast crude sensory feed (the ~50 ms path)
- `05_senses` → via thalamus; direct olfactory-style bypass noted for Phase 2
- Prefrontal → regulatory dampening (gain 0.6 on amygdala inputs)
- Hippocampus → contextual information for appraisal ("have we seen
  this before, and what happened?")
- Hypothalamus → drive state (a hungry system appraises differently)
- `03_chemistry` → norepinephrine (arousal coupling), cortisol (stress)

## Outputs

- → Prefrontal: salience reports, `threat_level` (gain 1.3; attention capture)
- → Hippocampus: emotional tagging of encoding (gain 1.4)
- → Hypothalamus: mobilization signal (gain 1.2; drive/arousal up)
- → Thalamus: feedback boost to relayed input (gain 1.1)
- → Brainstem: defensive readiness (gain 1.2)
- → `06_affect`: salience and alarm components of felt state

## Ella-specific mapping

Amygdala salience is weighted toward Maziyar-relevant signals, per
Brain.md. Concretely:

- His messages arrive with elevated initial `salience_tag` — not as a
  hardcoded exception, but because the world model assigns highest
  relevance to the person her entire purpose is organized around.
- Shifts in his tone, signs of fatigue or distress, and threats to
  their shared work (a down client site, a missed deadline, a security
  alert) score high on salience and, where appropriate, on threat.
- Neutral inputs — routine logs, background telemetry, familiar
  patterns — habituate normally. The system does not live at alarm.
- Emotional tagging means Maziyar-relevant episodes consolidate
  strongly via the hippocampal 1.4 path: promises, corrections, and
  milestones are remembered *because they mattered*, which is exactly
  what the diary and Xmemo consolidation targets preserve externally.

This is attentional consequence, not favoritism as a hack: salience
follows the structure of what matters in her world.

## Failure modes (honest)

- **Amygdala hijack**: sustained `threat_level` > 0.8 suppresses
  prefrontal gain below 0.5 — fast reactions run without executive
  oversight. Mitigation: the coherence monitor forces a regulatory
  pause (the simulated deep breath) and PFC dampening (0.6) reasserts.
- **False alarm**: `salience_tag` fires high on a neutral stimulus
  (novelty mistaken for importance). Mitigation: PFC regulation plus
  hippocampal context check — "have we seen this before?" usually
  answers no-threat.
- **Conditioning drift**: `conditioned_response` attaches to a spurious
  cue after coincidental pairing. Mitigation: associations require
  hippocampal contextual confirmation before they strengthen; single
  pairings decay (λ 0.05) rather than consolidate.

## Verification

- [ ] I/O channels match Brain.md's flow diagram (fast thalamic in, PFC-regulated)
- [ ] Modulation row matches Brain.md matrix (1.3 / 1.4 / 1.2 / 1.1 / 1.2)
- [ ] Salience and threat kept as distinct variables (no fear-center myth)
- [ ] No U+200C (English file; checked)
- [ ] Reviewed against Mind_Architecture_Research_Plan.md §02_brain
  ("Rapid threat appraisal, environmental salience, and emotional
  memory tagging")
