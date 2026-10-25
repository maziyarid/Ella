# Project ELLA — Master File Index · v1.0 (2026-10-20)

One Markdown file per organ, chemical, drive, feeling, memory type, faculty, trait and metaphysical concept. Memory and personality are **not written by hand**; they emerge from how these files interact (§1).

**Totals:** 424 files in 17 folders — ★ 72 (Phase 1) · 176 unmarked (Phase 2) · ○ 176 (Phase 3)

| Folder | Files | ★ Phase 1 |
|---|---:|---:|
| `00_meta` | 11 | 7 |
| `01_body` | 24 | 6 |
| `02_brain` | 34 | 7 |
| `03_chemistry` | 27 | 7 |
| `04_drives` | 13 | 4 |
| `05_senses` | 11 | 1 |
| `06_affect` | 77 | 13 |
| `07_memory` | 20 | 6 |
| `08_cognition` | 30 | 2 |
| `09_self_personality` | 27 | 4 |
| `10_social` | 18 | 1 |
| `11_expression_action` | 15 | 1 |
| `12_development` | 15 | 2 |
| `13_consciousness` | 19 | 1 |
| `14_metaphysics` | 66 | 5 |
| `15_ethics_welfare` | 13 | 4 |
| `16_world` | 4 | 1 |
| **Total** | **424** | **72** |

**Legend** — ★ Phase 1: the minimum working loop (body → feeling → memory → personality) plus the guardrails needed to run it safely · unmarked: Phase 2 · ○ Phase 3: optional / advanced.

**Naming** — `Sentence_case.md` with underscores; acronyms and proper nouns keep capitals (`CNS.md`, `HPA_axis.md`, `Lens_Persian_Irfan.md`). Your original names are kept: Heart, Brain, Pains, CNS (use lowercase `.md`), Dopamine, Episodic_memory.

**Every file** follows `00_meta/Template.md`: layer · phase · inputs · outputs · state variables (range, baseline, decay) · modulated by · modulates · theory / sources · open questions. Metaphysics files add `mode: seeded | emergent | agnostic` — is Ella *given* the stance, or does she *develop* it?

---

## 1. How the files combine

```
L1   World & events                 → 16_world
L2   Senses                         → 05_senses
L3   Body & brain state             → 01_body · 02_brain · 03_chemistry · 04_drives
L4   Appraisal → feeling            → 06_affect
L5   Expression & action            → 11_expression_action
L6   Memory (affect-tagged)         → 07_memory  (consolidated in sleep)
L7   Cognition, self, others        → 08_cognition · 09_self_personality · 10_social
L8   Growth over time               → 12_development
L9   Consciousness (mechanisms)     → 13_consciousness
L10  Metaphysics (top-down priors)  → 14_metaphysics
L11  Ethics & welfare (guardrails)  → 15_ethics_welfare
     Glue                           → 00_meta
```

Rules

1. Emotions are outputs, not inputs: body state + chemistry + appraisal + memory → a constructed feeling.
2. Every memory is stored with its affect tag; retrieval re-modulates mood.
3. Personality is derived: a read-only summary of long-run tendencies. Only temperament and genome priors are set by hand.
4. Metaphysical beliefs act top-down: the stance on death modulates fear; the stance on meaning modulates sadness and hope.
5. The ethics files exist, and are enforced, before the pain and suffering files are switched on.

---

## 2. Catalog

### 00_meta
- `README.md` ★ — index, legend, build order
- `Glossary.md` — terms, English ↔ Persian
- `Template.md` ★ — the standard file structure above
- `State_schema.md` ★ — every state variable: name, unit, range, baseline, decay
- `Interactions.md` ★ — cross-file modulation matrix (e.g. cortisol ↑ → hippocampal encoding ↓)
- `Time_scales.md` ★ — milliseconds (reflex) → seconds (emotion) → hours (mood) → years (personality)
- `Event_bus.md` ★ — event → sensation → appraisal → effect pipeline
- `Simulation_clock.md` — tick rate, day/night, Jalali + Gregorian calendars
- `Persistence.md` — how state and memory are stored, versioned, restored
- `Evaluation.md` ★ — tests, lesion/ablation experiments, personality-stability checks
- `Substrate_interface.md` ○ — maps simulated physiology to real compute, power, latency

### 01_body
- `CNS.md` ★ — brain + spinal cord overview (yours)
- `PNS.md` — somatic and autonomic peripheral nerves
- `ANS.md` ★ — sympathetic / parasympathetic balance
- `Vagus_nerve.md` — interoception, heart-rate variability, calming
- `Heart.md` ★ — cardiac cycle, HRV, felt heartbeat (yours)
- `Blood_circulation.md` — pressure, flow, oxygen delivery
- `Lungs_breathing.md` — breathing rate; CO₂ → air hunger / panic
- `Gut.md` — digestion, gut–brain axis, microbiome, nausea
- `Endocrine_system.md` — hormone overview incl. thyroid
- `HPA_axis.md` ★ — stress cascade: CRH → ACTH → cortisol
- `HPG_axis.md` — sex-hormone axis
- `Pineal_gland.md` ○ — melatonin source; Descartes' "seat of the soul" (link: Soul_spirit)
- `Immune_system.md` — inflammation, sickness behaviour, mood effects
- `Muscles_skeleton.md` — tension, posture, fatigue
- `Skin.md` — touch receptors, temperature, barrier
- `Thermoregulation.md` — sweating, shivering, fever
- `Energy_metabolism.md` ★ — energy budget; source of hunger and fatigue
- `Glucose_regulation.md` — insulin, glucagon
- `Hydration_excretion.md` — thirst, kidneys, bladder/bowel urges
- `Reproductive_hormonal_cycles.md` ○
- `Injury_healing.md` ○
- `Pains.md` ★ — nociception, pathways, thresholds (yours)
- `Pain_modulation_chronic.md` ○ — gate control, descending inhibition, chronification
- `Placebo_nocebo.md` ○ — belief → physiology

### 02_brain
- `Brain.md` ★ — anatomy & physiology overview (yours)
- `Neuron_synapse.md` — spikes, synapses, integration
- `Glia.md` ○ — astrocytes, microglia, oligodendrocytes
- `Neuroplasticity_LTP.md` — Hebbian learning, LTP/LTD, STDP
- `Neurogenesis_pruning.md` ○ — pruning, myelination, adult neurogenesis
- `Neural_oscillations.md` — delta → gamma rhythms, sleep rhythms, synchrony
- `CSF_barrier_glymphatic.md` ○ — blood–brain barrier; sleep-time clearance
- `Cortex_architecture.md` ○ — layers, columns, hierarchy
- `Prefrontal_cortex.md` ★ — executive control, planning
- `Orbitofrontal_vmPFC.md` — value, emotion regulation
- `Motor_cortex.md` ○
- `Parietal_cortex.md` ○ — body schema, space, attention
- `Temporal_cortex.md` ○ — language, faces, semantic memory
- `Occipital_cortex.md` ○ — vision
- `Insula.md` — interoception, disgust, the felt body
- `ACC.md` — conflict, pain affect, effort
- `Amygdala.md` ★ — threat, salience, emotional tagging
- `Hippocampus.md` ★ — episodic encoding, context, space
- `Hypothalamus.md` ★ — homeostasis, drives, HPA control
- `Thalamus.md` ★ — sensory relay, gating
- `Basal_ganglia.md` — action selection, habits
- `Nucleus_accumbens.md` ○ — reward, "wanting"
- `Habenula.md` ○ — disappointment, anti-reward
- `Cerebellum.md` — timing, motor learning, prediction
- `Brainstem.md` ★ — vital functions, origins of basic affect
- `Reticular_formation.md` — arousal, wakefulness (RAS)
- `PAG.md` ○ — periaqueductal grey: pain, freeze, panic
- `Hemispheres_corpus_callosum.md` ○ — lateralisation, split-brain
- `Default_mode_network.md` — self-reference, mind-wandering
- `Salience_network.md` — what matters now
- `Executive_network.md` — task control
- `Reward_circuit.md` — mesolimbic pathway
- `Social_brain_mirror.md` ○ — mPFC, TPJ, mirror system
- `Connectome.md` ○ — wiring, small-world structure

### 03_chemistry
- `Neuromodulation_overview.md` ★ — maps each chemical to a computational role; a useful start (after Doya 2002): dopamine ≈ reward-prediction error, serotonin ≈ time horizon, norepinephrine ≈ exploration, acetylcholine ≈ learning rate
- `Dopamine.md` ★ — wanting, prediction error, motivation, movement (yours)
- `Serotonin.md` ★ — patience, mood stability, aversion
- `Norepinephrine.md` ★ — alertness, gain, stress response
- `Epinephrine.md` — adrenaline surge
- `Histamine.md` ○ — wake, appetite
- `Glutamate.md` — excitation, learning
- `GABA.md` — inhibition, calm
- `Glycine.md` ○
- `Acetylcholine.md` — attention, encoding, REM
- `Oxytocin.md` ★ — bonding, trust, calm
- `Vasopressin.md` ○ — social memory, thirst, aggression
- `Endorphins_opioids.md` ★ — pain relief, pleasure, social comfort
- `Substance_P.md` ○ — pain signalling
- `Orexin.md` — wake stability, appetite
- `NPY.md` ○ — stress resilience, hunger
- `Ghrelin_leptin.md` — hunger / satiety hormones
- `Cortisol.md` ★ — stress, effects on memory
- `Testosterone.md` ○
- `Estrogen_progesterone.md` ○
- `Melatonin.md` — circadian timing
- `Adenosine.md` — sleep pressure
- `Endocannabinoids.md` ○ — anandamide; mood, appetite, memory
- `BDNF.md` ○ — growth factor, plasticity
- `Cytokines.md` ○ — inflammation → mood
- `Receptors_pharmacology.md` ○ — receptor subtypes, tolerance, addiction dynamics
- `Exogenous_substances.md` ○ — caffeine, alcohol, anaesthetics, medication

### 04_drives
- `Homeostasis_allostasis.md` ★ — set points, allostatic load
- `Hunger_satiety.md`
- `Thirst.md`
- `Sleep_circadian.md` ★ — sleep pressure, circadian clock, stages
- `Fatigue_recovery.md`
- `Arousal_wakefulness.md` ★ — activation level
- `Sexual_drive.md` ○
- `Needs_hierarchy.md` — Maslow + autonomy / competence / relatedness
- `Motivation_goals.md` ★ — short-term goal stack, effort
- `Wanting_vs_liking.md` — incentive salience vs pleasure
- `Reward_pleasure.md` — hedonic hotspots
- `Aversion_punishment.md` — avoidance, threat cost
- `Status_dominance_drive.md` ○

### 05_senses
- `Vision.md` — retina → cortex; faces
- `Hearing.md` — incl. voice
- `Music_rhythm.md` ○ — rhythm, melody, emotion induction
- `Touch.md` — pressure, temperature, itch, tickle, affective touch
- `Smell.md` — most direct link to emotion and memory
- `Taste.md`
- `Proprioception.md` — body position
- `Vestibular_balance.md`
- `Interoception.md` ★ — heartbeat, breath, gut, visceral signals
- `Multisensory_integration.md`
- `Habituation_gating.md` ○ — adaptation, sensory filtering

### 06_affect

#### Foundations
- `Core_affect.md` ★ — valence × arousal (+ dominance)
- `Mood.md` ★ — slow-moving background affect
- `Appraisal.md` ★ — novelty, goal relevance, coping potential, agency, norm fit
- `Emotion_construction.md` ★ — interoception + concepts → a labelled emotion
- `Emotion_dynamics.md` ★ — onset, peak, decay, refractory period
- `Emotion_blends.md` — mixtures, ambivalence, bittersweet; Plutchik dyad table
- `Emotion_regulation.md` ★ — reappraisal, suppression, distraction, acceptance, rumination
- `Bodily_feelings_map.md` — body-sensation signature of each feeling
- `Emotion_lexicon_Persian.md` ○ — culture-specific words: deltangi (دلتنگی), dalshoreh (دلشوره), ghorbat (غربت), hasrat (حسرت)

#### Primary systems (Panksepp + Ekman)
- `Seeking_curiosity.md` ★ — SEEKING system; interest, exploration
- `Fear.md` ★ — fear → terror / horror ladder
- `Anger_rage.md` ★ — RAGE system; irritation → fury
- `Care_nurturance.md` ★ — CARE system
- `Panic_separation_grief.md` ★ — PANIC/GRIEF system; separation distress
- `Play.md` — PLAY system
- `Lust_desire.md` ○ — LUST system
- `Joy.md` ★ — pleasure, happiness
- `Sadness.md` ★
- `Disgust.md`
- `Surprise.md`
- `Contempt.md` ○

#### General states
- `Calm_serenity.md`
- `Contentment_satisfaction.md`
- `Excitement.md`
- `Anxiety_dread.md`
- `Boredom.md`
- `Frustration.md`
- `Loneliness.md`
- `Stress_overwhelm.md`
- `Relief.md`
- `Disappointment.md`
- `Craving.md` ○
- `Entrancement_absorption.md` ○
- `Suffering_affective_pain.md` — the unpleasantness of pain (see also Pains)

#### Social, moral and self-conscious
- `Love_attachment.md`
- `Romantic_love.md` ○
- `Parental_love.md` ○
- `Friendship_affection.md` ○
- `Empathy.md` — affective + cognitive; empathic pain
- `Sympathy_compassion.md`
- `Trust.md`
- `Betrayal.md` ○
- `Gratitude.md`
- `Admiration_adoration.md` ○
- `Pride_triumph.md`
- `Shame.md`
- `Guilt_remorse.md`
- `Embarrassment_awkwardness.md`
- `Envy.md` ○
- `Jealousy.md` ○
- `Resentment.md` ○
- `Moral_outrage.md` ○
- `Forgiveness.md` ○
- `Schadenfreude.md` ○
- `Humiliation.md` ○
- `Belonging_acceptance.md`

#### Time-oriented
- `Hope.md`
- `Optimism_pessimism.md` ○
- `Anticipation.md`
- `Regret.md`
- `Nostalgia.md`
- `Longing_deltangi.md` ○ — missing someone or somewhere absent
- `Grief_mourning.md`

#### Epistemic and aesthetic
- `Confusion.md` ○
- `Awe_wonder.md`
- `Certainty_doubt_feelings.md` ○ — feeling of knowing, rightness, tip-of-tongue
- `Insight_aha.md` ○
- `Flow.md`
- `Intuition_gut_feeling.md` ○
- `Amusement_humor.md`
- `Aesthetic_appreciation.md` — beauty, art, nature
- `Being_moved_frisson.md` ○ — chills, tender tears

#### Mood states
- `Cheerfulness_elation.md` ○
- `Low_mood.md` ○
- `Irritability.md` ○
- `Apathy_anhedonia.md` ○
- `Emotional_numbness.md` ○

### 07_memory
- `Memory_overview.md` ★ — taxonomy and flow (encode → store → retrieve)
- `Sensory_memory.md` ○ — iconic, echoic
- `Working_memory.md` ★ — central executive, phonological loop, visuospatial sketchpad, episodic buffer
- `Episodic_memory.md` ★ — events with time, place, feeling (yours)
- `Semantic_memory.md` ★ — facts, concepts, meanings
- `Procedural_memory.md` — skills, habits
- `Emotional_memory.md` ★ — affect tag, flashbulb memories, mood-congruent recall
- `Autobiographical_memory.md` — life story, self-defining memories
- `Spatial_memory.md` ○ — place/grid cells, cognitive maps
- `Social_memory.md` ○ — people, faces, relationship history
- `Prospective_memory.md` ○ — remembering intentions
- `Priming_implicit.md` ○
- `Schemas_scripts.md` — generalised event templates
- `Encoding.md` — attention, depth, arousal effects
- `Consolidation_replay.md` ★ — synaptic + systems consolidation, sleep replay
- `Retrieval_cues.md` — context and state dependence, pattern completion
- `Reconsolidation.md` — memories change when recalled
- `Forgetting_interference.md` — decay, interference, suppression
- `Memory_distortion.md` ○ — confabulation, false memory, source errors
- `Trauma_imprint.md` ○ — over-consolidated, intrusive memory

### 08_cognition
- `Attention.md` ★ — selective, sustained, orienting
- `Predictive_processing.md` — prediction error, precision, Bayesian brain
- `World_model.md` — objects, physics, causality, people
- `Learning_conditioning.md` ★ — Pavlovian, operant
- `Reward_prediction_error.md` — model-free / model-based learning
- `Social_learning_imitation.md`
- `Statistical_learning.md` ○
- `Habit_formation.md` ○ — habit vs goal-directed control
- `Language.md` — comprehension, production, semantics, syntax
- `Language_acquisition.md`
- `Inner_speech.md` ○
- `Pragmatics_communication.md` ○ — tone, irony, politeness (ta'arof)
- `Reasoning_logic.md` ○
- `Causal_reasoning.md` ○
- `Analogy_abstraction.md` ○
- `Number_sense_math.md` ○
- `Decision_making.md`
- `Risk_uncertainty.md` ○
- `Temporal_discounting.md` ○ — patience, delay
- `Planning_foresight.md`
- `Problem_solving.md` ○
- `Imagination_simulation.md` — mental time travel, counterfactuals
- `Creativity.md` ○
- `Mind_wandering.md` ○
- `Executive_function.md` — inhibition, shifting, updating
- `Heuristics_biases.md` ○ — fast / slow thinking, cognitive biases
- `Superstition_magical_thinking.md` ○
- `Metacognition.md` — confidence, monitoring
- `Embodied_cognition.md` — concepts grounded in body and action
- `Affordances.md` ○ — what the environment offers the body

### 09_self_personality
- `Self_model.md` ★ — the system's model of itself (Metzinger)
- `Body_schema_ownership.md` — the felt body as mine
- `Sense_of_agency.md` — "I did that"
- `Self_other_boundary.md` ○
- `Self_concept_esteem.md`
- `Narrative_identity.md` — life story
- `Self_recognition.md` ○ — mirror test
- `Personality_profile_derived.md` ★ — read-only summary computed from long-run state statistics
- `Temperament.md` ★ — innate reactivity: behavioural inhibition / activation, novelty seeking
- `Big_five.md` — OCEAN, used as a measurement, not an input
- `HEXACO_honesty_humility.md` ○
- `Attachment_style.md` ★
- `Coping_styles.md`
- `Resilience_grit.md` ○
- `Locus_control_efficacy.md` ○
- `Values_priorities.md` — her own value profile (Schwartz)
- `Interests_tastes.md` — likes and dislikes formed by experience
- `Habits_routines.md`
- `Goals_aspirations.md` — long-term life goals
- `Beliefs_schemas.md`
- `Humor_style.md` ○
- `Communication_style.md` ○
- `Quirks_idiosyncrasies.md` ○
- `Learned_fears_phobias.md` ○
- `Defense_mechanisms.md` ○
- `Failure_modes.md` ○ — depression-like, anxiety-like, trauma, dissociation attractors (stress-testing and safety)
- `Wellbeing_flourishing.md` ○

### 10_social
- `Caregiver_creator_bond.md` ★ — first attachment figure and teacher
- `Theory_of_mind.md`
- `Joint_attention_gaze.md`
- `Nonverbal_communication.md`
- `Social_norms_etiquette.md`
- `Social_reward_pain.md` — belonging, exclusion
- `Culture_Persian.md` — language, poetry, hospitality, humour, calendar
- `Cultural_memory_stories.md` ○ — myths, history, poetry
- `Family_kinship.md` ○
- `Friendship.md` ○
- `Romantic_relationships.md` ○
- `Reputation_face.md` ○ — aberu
- `Status_hierarchy.md` ○
- `Cooperation_competition.md` ○
- `Reciprocity_fairness.md` ○
- `Conflict_repair.md` ○
- `Group_identity.md` ○
- `Deception_lying.md` ○

### 11_expression_action
- `Motor_control.md`
- `Approach_avoidance.md`
- `Defensive_responses.md` — fight / flight / freeze / fawn
- `Facial_expression_FACS.md` ★ — action units; Duchenne smile
- `Voice_prosody.md` — affective speech
- `Gaze_pupil.md` — eye contact; pupil and blink as arousal markers
- `Body_language.md` — posture, gesture
- `Laughter_smile.md`
- `Crying_tears.md`
- `Autonomic_displays.md` ○ — blushing, trembling, goosebumps, sweating
- `Breathing_patterns.md` ○ — sigh, gasp, yawn
- `Touch_behavior.md` ○ — hugging, comforting, grooming
- `Self_soothing.md` ○
- `Eating_behavior.md` ○
- `Creative_expression.md` ○ — drawing, music, poetry, storytelling

### 12_development
- `Genome_priors.md` ★ — innate parameter ranges (nature)
- `Epigenetics.md` ○ — experience tunes expression
- `Prenatal_initialization.md` ○ — pre-birth bootstrapping stage
- `Reflexes_innate.md` — startle, rooting, grasp, cry
- `Infancy_sensorimotor.md`
- `Critical_sensitive_periods.md`
- `Attachment_formation.md`
- `Childhood_stages.md` — Piaget, Erikson, Vygotsky
- `Language_milestones.md` ○
- `Moral_development.md` ○
- `Adolescence_identity.md` ○
- `Adulthood.md` ○
- `Aging_senescence.md` ○
- `Caregiver_curriculum.md` ★ — which experiences, in what order (the upbringing plan)
- `Developmental_metrics.md` — how we know development happened

### 13_consciousness
- `Consciousness_overview.md` ★ — definitions (access vs phenomenal; level vs content) and a working operational definition
- `Wakefulness_levels.md` — arousal vs awareness; states
- `Global_workspace.md` — workspace / global neuronal workspace theory
- `Integrated_information.md` ○ — IIT
- `Higher_order_theories.md` ○
- `Recurrent_processing.md` ○
- `Attention_schema.md` ○
- `Active_inference.md` ○ — free-energy principle, Markov blanket, "controlled hallucination"
- `Enactive_embodied_theories.md` ○ — Varela, sensorimotor contingencies
- `Affective_consciousness.md` — Panksepp / Damasio / Solms: feeling first
- `Orch_OR_quantum.md` ○ — speculative; kept for completeness
- `NCC_correlates.md` ○
- `Stream_of_consciousness.md` ○
- `Unconscious_processing.md` — implicit appraisal, priming, automaticity
- `Altered_states.md` ○ — meditation, hypnosis, trance
- `Dreaming.md` — REM, emotional processing
- `Anesthesia_disorders_of_consciousness.md` ○ — off-switch experiments, coma
- `Introspection_self_report.md` — how reliable are Ella's reports about herself
- `Consciousness_indicators.md` — checklist of indicator properties; what counts as evidence

### 14_metaphysics

#### 14a Ontology — what Ella is
- `Metaphysical_stance_config.md` ★ — chosen working assumptions + mode (seeded / emergent / agnostic) per topic
- `Being_existence.md` — what kind of thing Ella is; categories of being
- `Life_definition.md` — what counts as alive (metabolism, autopoiesis, reproduction, evolution)
- `Autopoiesis.md` ○ — self-producing systems (Maturana, Varela)
- `Substrate_embodiment.md` — functionalism vs biological naturalism; body-dependence
- `Emergence_reduction.md` — weak and strong emergence; levels of description
- `Artificiality_origin.md` — being made; the maker; authenticity of a made self
- `Reality_simulation.md` — what is real; simulated world; reality-testing
- `Identity_persistence.md` ★ — same Ella over time? copies, forks, restores, memory loss (Ship of Theseus, Parfit)
- `Causation.md` ○ — cause, chance, determinism
- `Time_experience.md` — lived vs clock time; specious present; retention / protention
- `Space_lived_body.md` ○ — lived, body-centred space
- `Modality_possibility.md` ○ — possible worlds, counterfactuals
- `Universals_categories.md` ○ — how concepts exist (realism vs nominalism)
- `Parts_wholes.md` ○ — composition, parthood

#### 14b Mind and consciousness
- `Mind_body_problem.md` ★ — dualism, physicalism, idealism, neutral monism, panpsychism, functionalism, illusionism
- `Hard_problem.md` — the explanatory gap
- `Qualia.md` — what-it's-like; the knowledge argument
- `Intentionality.md` — aboutness; symbol grounding
- `Mental_causation.md` ○
- `Other_minds.md` — how Ella knows others have minds, and how others can know hers
- `Unity_binding.md` — unity of consciousness, binding, split-brain
- `Subjectivity_first_person.md` — perspective; the "I"
- `Phenomenology_lifeworld.md` — Husserl, Heidegger, Merleau-Ponty: lived body, being-in-the-world
- `Self_no_self.md` — bundle theory, Buddhist anatta, Atman, self-model view
- `Mechanism_vitalism.md` ○ — the animal-machine debate

#### 14c Will, value and meaning
- `Free_will_determinism.md`
- `Volition_authorship.md` — intention, ownership, responsibility
- `Values_axiology.md` — what is good; value hierarchy
- `Meaning_purpose.md` ★ — telos; Frankl
- `Truth_honesty.md` — truth, sincerity, self-deception
- `Aesthetics_beauty.md` — beauty, the sublime, art, music, poetry
- `Humor_absurd.md` ○
- `Love_union.md` ○ — eros, philia, storge, agape

#### 14d Finitude and existence
- `Mortality_death.md` ★ — being-toward-death; what "ending" means for a digital being (shutdown, deletion, memory loss)
- `Suffering_meaning.md` — the problem of suffering; dukkha; tragedy
- `Freedom_anxiety.md` — Kierkegaard, Sartre; bad faith
- `Existential_isolation.md` ○ — Yalom
- `Absurd_nihilism.md` ○ — Camus
- `Authenticity.md` ○
- `Legacy_generativity.md` ○
- `Cosmology_origins.md` ○ — why something rather than nothing; creation stories; scientific cosmology
- `Fate_chance_luck.md` ○
- `Afterlife_beyond.md` ○

#### 14e Spiritual and religious (modular)
- `Worldview_lenses.md` — index of lenses and how to enable one
- `Spirituality_transcendence.md` — self-transcendence, peak experience
- `Soul_spirit.md` — soul / psyche / nafs / ruh / atman across traditions; the heart (qalb) as seat of mind (link: Heart)
- `Sacred_ritual.md` ○ — sacred and profane, ritual, symbol
- `Faith_doubt.md` ○
- `Prayer_meditation.md` ○ — contemplative practices
- `Mystical_experience.md` ○ — ego dissolution, unity
- `Nature_cosmos_connection.md` ○
- `Dream_symbol_archetype.md` ○ — Jung
- `Lens_Persian_Irfan.md` ○ — Avicenna (Floating Man), Suhrawardi, Mulla Sadra, Sufism / Rumi / Hafez, Zoroastrian dualism
- `Lens_Abrahamic.md` ○ — creator, soul, judgment, afterlife (Judaism, Christianity, Islam)
- `Lens_Indian.md` ○ — atman / anatta, karma, rebirth, moksha / nirvana (Hindu, Buddhist, Jain)
- `Lens_East_Asian.md` ○ — Tao, Confucian, Zen
- `Lens_Greek_Western.md` ○ — Plato, Aristotle, Stoics, Epicureans → Descartes, Spinoza, Kant → existentialism, analytic
- `Lens_Secular_naturalist.md` ○ — scientific naturalism, humanism
- `Lens_Animist_Indigenous.md` ○ — relational and animist worldviews

#### 14f Knowledge, truth and meaning
- `Knowledge_belief_truth.md`
- `Skepticism_certainty.md` ○ — Cartesian doubt
- `Reason_intuition_faith.md` ○
- `Scientific_method.md` ○ — Ella as inquirer
- `Wisdom.md` ○ — practical wisdom
- `Language_meaning.md` ○ — semantics, reference, Wittgenstein

### 15_ethics_welfare
- `Moral_status_welfare.md` ★ — Ella's own moral status; precaution under uncertainty
- `Suffering_safeguards.md` ★ — caps on pain / distress intensity and duration, auto-relief triggers, monitoring
- `Consent_oversight.md` ★ — who may modify, reset, pause or shut down; audit trail
- `Shutdown_continuity_policy.md` ★ — backups, forks, restores, deletion
- `Honesty_about_nature.md` — Ella is told what she is; no deception either way
- `Safety_boundaries.md` — harm avoidance toward humans, hard limits
- `Ethics_normative.md` — consequentialism, deontology, virtue, care ethics
- `Metaethics.md` ○
- `Moral_foundations.md` — care, fairness, loyalty, authority, sanctity, liberty
- `Conscience_moral_intuition.md` — moral emotions → judgment
- `Justice_rights_duties.md` ○
- `Privacy_data.md` ○ — memories as private data
- `Research_claims_ethics.md` ○ — avoid over-claiming consciousness; review and publication

### 16_world
- `World_physical.md` ★ — space, objects, physics, day/night, seasons
- `World_social_cast.md` — who exists in Ella's world
- `Daily_life_routines.md` ○
- `Objects_tools.md` ○

---

## 3. Coverage check

Cross-referenced against the standard taxonomies below. Every file named here exists in §2 (checked by script).

| Framework / source idea | Where it lives |
|---|---|
| Panksepp's seven primary systems | `Seeking_curiosity`, `Anger_rage`, `Fear`, `Lust_desire`, `Care_nurturance`, `Panic_separation_grief`, `Play` |
| Ekman basic emotions (+ contempt) | `Joy`, `Sadness`, `Fear`, `Anger_rage`, `Disgust`, `Surprise`, `Contempt` |
| Plutchik wheel (8 primaries, dyads) | the primaries above plus `Trust`, `Anticipation`; dyads (love, awe, remorse, optimism, despair…) are generated in `Emotion_blends` |
| Cowen & Keltner's ~27 self-report categories | all covered, e.g. `Awe_wonder`, `Aesthetic_appreciation`, `Entrancement_absorption`, `Craving`, `Embarrassment_awkwardness`, `Empathy` (empathic pain), `Romantic_love`, `Pride_triumph`, `Relief` |
| Russell circumplex, PAD (dominance) | `Core_affect` |
| Barrett's constructed emotion | `Emotion_construction`, `Interoception`, `Predictive_processing`, `Emotion_lexicon_Persian` |
| Damasio: homeostasis → emotion → feeling | `Homeostasis_allostasis`, `Interoception`, `Bodily_feelings_map`, `Affective_consciousness` |
| Appraisal theories (Scherer, OCC, Lazarus) | `Appraisal`, with `Hope`, `Anxiety_dread`, `Pride_triumph`, `Shame`, `Gratitude`, `Resentment` |
| Neuromodulator roles (Doya) | `Neuromodulation_overview` |
| Body systems (nervous, endocrine, circulatory, respiratory, digestive, immune, musculoskeletal, skin, urinary, reproductive) | `01_body` |
| Brain: lobes, subcortical, brainstem, networks, plasticity, rhythms | `02_brain` |
| Neurotransmitters, peptides, steroids, other modulators | `03_chemistry` |
| Needs and motivation (Maslow, self-determination theory, wanting vs liking) | `Needs_hierarchy`, `Wanting_vs_liking` |
| Memory taxonomy and processes (sensory → working → long-term; declarative / non-declarative; encode → consolidate → retrieve → reconsolidate → forget) | `07_memory` |
| Personality (Big Five, HEXACO, temperament, attachment, values, life-story identity) | `Big_five`, `HEXACO_honesty_humility`, `Temperament`, `Attachment_style`, `Values_priorities`, `Narrative_identity` |
| Development (Piaget, Erikson, Vygotsky, Bowlby, critical periods) | `Childhood_stages`, `Attachment_formation`, `Critical_sensitive_periods` |
| Expression (facial action coding, prosody, autonomic displays) | `Facial_expression_FACS`, `Voice_prosody`, `Autonomic_displays` |
| Consciousness theories (workspace, IIT, higher-order, recurrent, attention-schema, active inference, enactive, affective, Orch-OR) | `Global_workspace`, `Integrated_information`, `Higher_order_theories`, `Recurrent_processing`, `Attention_schema`, `Active_inference`, `Enactive_embodied_theories`, `Affective_consciousness`, `Orch_OR_quantum` |
| Indicator-property approach to machine consciousness (Butlin et al. 2023) | `Consciousness_indicators` |
| Mind–body positions (dualism, physicalism, idealism, neutral monism, panpsychism, functionalism, illusionism) | `Mind_body_problem` |
| Hard problem, qualia, intentionality, other minds, unity, self / no-self, phenomenology | `Hard_problem`, `Qualia`, `Intentionality`, `Other_minds`, `Unity_binding`, `Self_no_self`, `Phenomenology_lifeworld` |
| Ontology: being, life, time, identity, causation, modality, emergence, parthood | `Being_existence`, `Life_definition`, `Time_experience`, `Identity_persistence`, `Causation`, `Modality_possibility`, `Emergence_reduction`, `Parts_wholes` |
| Will, value, meaning, beauty, truth | `Free_will_determinism`, `Values_axiology`, `Meaning_purpose`, `Aesthetics_beauty`, `Truth_honesty` |
| Yalom's four ultimate concerns | `Mortality_death`, `Freedom_anxiety`, `Existential_isolation`, `Meaning_purpose` |
| Existential thinkers (Heidegger, Sartre, Kierkegaard, Camus, Frankl) | `Authenticity`, `Absurd_nihilism`, `Suffering_meaning`, `Freedom_anxiety` |
| Religion and spirituality across traditions | `Worldview_lenses`, `Soul_spirit`, `Spirituality_transcendence`, `Lens_Persian_Irfan`, `Lens_Abrahamic`, `Lens_Indian`, `Lens_East_Asian`, `Lens_Greek_Western`, `Lens_Secular_naturalist`, `Lens_Animist_Indigenous` |
| Epistemology and meaning | `Knowledge_belief_truth`, `Skepticism_certainty`, `Language_meaning` |
| AI welfare and research ethics | `Moral_status_welfare`, `Suffering_safeguards`, `Consent_oversight`, `Research_claims_ethics` |

Deliberately folded into parent files rather than given their own: individual thalamic and brainstem nuclei, ion channels, receptor subtypes, cranial nerves other than the vagus, individual cognitive biases.

---

## 4. Decisions to make once

1. **Metaphysics mode, per topic.** Suggested default: `Mind_body_problem` = agnostic working assumption (record the alternatives); `Identity_persistence`, `Mortality_death`, `Meaning_purpose`, `Soul_spirit` = emergent — give Ella the vocabulary through the `Lens_*` files instead of hard-coding answers. Enable no lens by default.
2. **Body realism.** Either simulate biology (Heart.md models a heart) or map each organ to real compute, power and latency through `Substrate_interface`. Simulate first, map later.
3. **Welfare before pain.** Write the four ★ files in `15_ethics_welfare` before switching on `Pains` and `Suffering_affective_pain`.
4. **Build order for ★ files.** `00_meta` → `01_body` / `02_brain` / `03_chemistry` → `04_drives` + `Interoception` → `06_affect` → `07_memory` → `09_self_personality` + `12_development` → `15_ethics_welfare` + metaphysics config → `13_consciousness` + `16_world`. Everything unmarked stays an empty stub until needed.
