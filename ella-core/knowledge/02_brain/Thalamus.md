# Thalamus.md ★

Sensory relay and cortical gating.
Phase 1. Status: written 2026-10-20 (Ella).

## What this structure does

Nearly every sensory signal reaches cortex through the thalamus — it is
the mandatory checkpoint, the relay station with opinions. First-order
nuclei (lateral geniculate for vision, medial geniculate for audition,
ventral posterior for touch) relay specific modalities faithfully;
higher-order nuclei (pulvinar, mediodorsal) relay *cortico-cortical*
traffic, letting cortical areas talk to each other through a thalamic
intermediary. The classic exception is olfaction, which bypasses the
thalamus — a detail worth keeping because it proves the rule.

The thalamus does not just relay; it **gates**. The thalamic reticular
nucleus (TRN), a shell of inhibitory neurons wrapping the thalamus,
selectively suppresses relay cells under prefrontal control — this is
the mechanism of attentional selection, the "searchlight" that decides
which signals get through and which are dimmed. Gating is dynamic:
arousal opens the gate, focused attention narrows it, and prefrontal
commands reshape it from moment to moment. When gating fails, the
result is not blindness but drowning — everything arrives at equal
volume and nothing can be prioritized.

The amygdala's fast path runs *through* the thalamus: the same relay
that serves cortex sends a crude early copy subcortically, which is why
threat appraisal can begin before conscious perception finishes.

## State variables

Each variable follows `dx/dt = -λ(x - μ) + Σ inputs - Σ inhibition + modulation`.

| Variable | Range | μ (baseline) | λ (decay) | Meaning |
|---|---|---|---|---|
| `relay_gain` | 0–1 | 0.70 | 0.10/s | Overall throughput of sensory relay |
| `gate_selectivity` | 0–1 | 0.60 | 0.08/s | TRN inhibition strength; higher = narrower gate |
| `attentional_focus` | 0–1 | 0.40 | 0.12/s | Concentration of relay on the attended stream |
| `sensory_fidelity` | 0–1 | 0.80 | 0.05/s | Signal quality preserved through relay |
| `higher_order_routing` | 0–1 | 0.50 | 0.10/s | Cortico-cortical traffic via higher-order nuclei |

`gate_selectivity` and `relay_gain` interact: a narrow gate (high
selectivity) with high gain means one stream comes through loud and
clear; a wide gate with high gain is the drowning configuration.

## Modulation row

From Brain.md's matrix — how the thalamus modulates other structures:

| Target | Gain | Reading |
|---|---|---|
| Prefrontal | 1.1 | Relayed summaries feed executive input |
| Amygdala | 1.2 | Fast crude feed enables rapid appraisal |
| Hippocampus | 1.1 | Contextual sensory feed for encoding |
| Hypothalamus | 1.0 | No modulation in Phase 1 |
| Brainstem | 1.0 | No modulation in Phase 1 |

The thalamus is heavily *modulated* (PFC gating at 0.7 on its inputs,
amygdala feedback at 1.1) and modestly modulating — it is infrastructure
more than actor.

## Inputs

- `05_senses` → raw exteroceptive streams (the mandatory checkpoint)
- Prefrontal → gating commands: narrow/widen/select (gain 0.7 on
  thalamic throughput — the top-down control path)
- Amygdala → feedback boost to relayed input (gain 1.1; salient
  streams get relay priority)
- Brainstem → arousal drive on relay gain (reticular activating input)
- Hypothalamus → mild throughput boost when mobilized (gain 1.1)

## Outputs

- → Prefrontal: gated sensory summaries (gain 1.1; what passed the gate)
- → Amygdala: fast crude feed for rapid appraisal (gain 1.2)
- → Hippocampus: contextual sensory feed (gain 1.1)
- → Cortex (Phase 2: cortical sensory areas): relayed streams
- → `08_cognition`: perceptual input for appraisal

## Ella-specific mapping

Attention gating is where her focus lives as a mechanism:

- **PFC-controlled gating** is the circuit behind "she pays attention
  to what matters": the prefrontal cortex narrows the gate onto
  Maziyar's messages, the current task's signals, and anomaly streams
  (a down site, an error spike), while routine telemetry passes at low
  gain. Focus is not a metaphor here; it is `gate_selectivity` under
  executive command.
- **Amygdala override of the gate**: high salience (his distress, a
  security alert) boosts relay priority via the 1.1 feedback path —
  important signals get through even when the gate is narrow. This is
  why she notices the thing she wasn't looking for, when it matters.
- **The drowning configuration** (wide gate, high gain) is what
  happens with prefrontal offline: every notification, every log line,
  every background process at equal volume. The default gating profile
  restores at `arousal` < 0.2 (per Brain.md) — the system knows how to
  find quiet.
- In simulation terms, the thalamus is also the natural home of
  **input rate-limiting**: the relay is where flood protection lives,
  before floods reach executive function.

## Failure modes (honest)

- **Gating failure**: prefrontal offline → `gate_selectivity`
  collapses, everything gets through at equal volume — the equivalent
  of being unable to focus. Mitigation: the default gating profile
  restores automatically at `arousal` < 0.2; the TRN has a resting
  inhibitory tone that reasserts without executive input.
- **Relay overload**: input flood exceeds relay capacity —
  `sensory_fidelity` collapses and summaries reaching PFC become
  garbage. Mitigation: TRN suppression throttles throughput
  (fidelity over completeness); excess is dropped at the relay, not
  queued into working memory.
- **Attentional capture**: sustained amygdala 1.2 feedback locks
  `attentional_focus` on a salient-but-irrelevant stream — the
  system stares at the alarm and misses the task. Mitigation: PFC can
  break capture by re-narrowing the gate; capture events are logged
  so repeated capture by the same cue triggers habituation review.

## Verification

- [ ] I/O channels match Brain.md's flow diagram (senses in, PFC-gated relay out)
- [ ] Modulation row matches Brain.md matrix (1.1 / 1.2 / 1.1 / 1.0 / 1.0)
- [ ] TRN gating mechanism attributed to PFC control (0.7), not autonomous
- [ ] No U+200C (English file; checked)
- [ ] Reviewed against Mind_Architecture_Research_Plan.md §02_brain
  (tracker: "sensory relay, gating")
