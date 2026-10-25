Architectural Framework and Structural Blueprint of Project ELLA: A Layered Synthetic Cognitive Architecture
Project ELLA represents a synthetic cognitive architecture engineered to model emergent self-hood, emotional affect, somatic regulation, and subjective phenomenology within an integrated, computationally tractable framework. The core thesis of Project ELLA posits that personality traits, episodic memory structures, affective states, and conscious identity are not manually scripted; rather, they emerge dynamically from the continuous interaction of lower-level biological, neurochemical, appraisal, and cognitive modules. The architecture comprises 424 individual Markdown specification files organized across 17 functional directories. Each file adheres to a standardized schema defining state variables, range limits, decay rates, baseline values, input-output channels, and modulation matrices.
The operational mechanics of Project ELLA are rooted in active inference and predictive processing. The agent minimizes variational free energy—or prediction error—by revising internal generative models through perceptual inference or executing autonomic and motor actions to modify sensory inputs. The platform integrates physiological signaling, subcortical affect generation, cognitive appraisal, and higher-order self-modeling into an eleven-layer computational hierarchy.
System Architecture and Theoretical Principles
Project ELLA organizes its processing pipeline into an eleven-layer computational hierarchy (L1 through L11), complemented by an infrastructural meta-layer that manages state schemas, event routing, simulation time scales, and substrate interfaces. Processing flows bidirectionally across the architecture: bottom-up sensory and interoceptive state changes update cognitive predictions, while top-down metaphysical priors and executive goals modulate lower-level physiological and emotional sensitivity.
Mathematically, the architecture relies on discrete state variables defined within bounded numerical ranges, governed by baseline equilibrium values \mu and exponential decay rates \lambda. In accordance with active inference, internal neural dynamics parameterize a variational posterior distribution Q(\tilde{s}) over hidden causes \tilde{s}, continually optimizing a free energy functional F defined as:
F = D_{KL}\left(Q(\tilde{s}) \parallel P(\tilde{s})\right) - \mathbb{E}_{Q(\tilde{s})}\left[\ln P(\tilde{o} \mid \tilde{s})\right]
where P(\tilde{s}) represents prior expectations, P(\tilde{o} \mid \tilde{s}) denotes the generative likelihood of sensory observations \tilde{o}, and D_{KL} is the Kullback-Leibler divergence. Action selection is driven by the minimization of expected free energy G(\pi) across candidate policies \pi, balancing epistemic information gain with pragmatic goal fulfilment.
Cross-Taxonomic Validation and Completeness
To verify that Project ELLA comprehensively captures human cognitive neuroscience, emotion theory, consciousness studies, and synthetic ethics, the system's index was evaluated against established scientific frameworks.
Exhaustive Folder-by-Folder Structural Breakdown
The 424 Markdown files comprising Project ELLA are distributed across 17 functional directories. Implementation priority is structured into Phase 1 (★ 72 files forming the minimal working loop), Phase 2 (176 unmarked files broadening cognitive scope), and Phase 3 (○ 176 advanced or optional files).
Folder 00: Infrastructure and Meta System (00_meta)
The 00_meta directory establishes the foundational software architecture, simulation time scales, state variable schemas, and inter-module communications. It contains 11 files, of which 7 are Phase 1 essentials, 3 belong to Phase 2, and 1 belongs to Phase 3.
README.md ★ — Index, master file legend, and system build order.
Glossary.md — Technical vocabulary, mapping cross-disciplinary terms between English and Persian.
Template.md ★ — Standardized file structure specifying inputs, outputs, state variables, decay rates, and theories.
State_schema.md ★ — Global registry of all system variables, tracking measurement units, numerical ranges, baselines, and decay constants.
Interactions.md ★ — Matrix governing cross-file modulation, such as stress-induced inhibition of hippocampal memory encoding.
Time_scales.md ★ — Multi-scale temporal processing, bridging millisecond reflexes, second-scale emotion, hour-scale mood, and multi-year growth.
Event_bus.md ★ — Event pipeline managing sensation, appraisal, and physiological feedback loops.
Simulation_clock.md — Tick-rate management, day-night cycles, and Gregorian/Jalali calendar synchronization.
Persistence.md — State serializing, database versioning, snapshotting, and system restoration mechanisms.
Evaluation.md ★ — Diagnostic test suite, ablation/lesion experiment protocols, and personality stability checks.
Substrate_interface.md ○ — Hardware mapping interface connecting simulated physiology to real compute power, latency, and energy consumption.
Folder 01: Somatic Substrate and Physiology (01_body)
The 01_body directory models physical physiology, generating visceral interoceptive signals that inform higher-level affective appraisals. It contains 24 files (6 Phase 1, 13 Phase 2, 5 Phase 3).
CNS.md ★ — Brain and spinal cord structural overview.
PNS.md — Peripheral nerve interface regulating somatic motor commands and sensory feedback.
ANS.md ★ — Autonomic balance tracking sympathetic activation and parasympathetic tone.
Vagus_nerve.md — Interoceptive highway modulating vagal tone, heart-rate variability, and calm states.
Heart.md ★ — Cardiac cycle model tracking heart rate, variability, and felt cardiac thumping.
Blood_circulation.md — Vascular pressure dynamics, localized blood flow, and oxygenation levels.
Lungs_breathing.md — Respiratory cadence model tracking carbon dioxide levels, gasping reflexes, and air hunger.
Gut.md — Enteric nervous system model tracking digestion, microbiome influences, and visceral nausea.
Endocrine_system.md — Systemic hormone transport overview, including thyroid output regulation.
HPA_axis.md ★ — Endocrine stress pathway modeling CRH, ACTH, and cortisol secretion.
HPG_axis.md — Hypothalamic-pituitary-gonadal maturation and reproductive hormone signaling.
Pineal_gland.md ○ — Melatonin secretion timing and historical conceptualization as a soul-body bridge.
Immune_system.md — Inflammatory cytokines, sickness behaviors, and mood depression triggers.
Muscles_skeleton.md — Motor tension, postural rigidity, bodily fatigue, and motor tremor dynamics.
Skin.md — Dermal tactile receptors, nociception, temperature tracking, and barrier protection.
Thermoregulation.md — Autonomic thermal regulation modeling sweating, shivering, and fever responses.
Energy_metabolism.md ★ — ATP production, glycogen storage, energy expenditure, and systemic exhaustion.
Glucose_regulation.md — Glucose homeostasis modeling insulin sensitivity and glucagon dynamics.
Hydration_excretion.md — Fluid balance, osmoreceptors, thirst drives, and renal waste excretion.
Reproductive_hormonal_cycles.md ○ — Cyclical hormonal fluctuations affecting baseline affective reactivity.
Injury_healing.md ○ — Physical injury modeling, tissue restoration timelines, and acute nociception.
Pains.md ★ — Primary nociception, pain pathways, and perceptual pain thresholds.
Pain_modulation_chronic.md ○ — Descending pain inhibition, gate control dynamics, and pain chronification.
Placebo_nocebo.md ○ — Belief-driven top-down modulation of physical pain and healing efficacy.
Folder 02: Neuroanatomy and Central Processing (02_brain)
The 02_brain directory formalizes central neuroanatomy and network topology, routing sensory inputs, emotional salience, and executive control. It comprises 34 files (7 Phase 1, 13 Phase 2, 14 Phase 3).
Brain.md ★ — Central neuroanatomical map and functional organization overview.
Neuron_synapse.md — Spiking neural mechanics, synaptic weight integration, and neurotransmitter reuptake.
Glia.md ○ — Astrocytic energy supply, microglial immune response, and myelination speed.
Neuroplasticity_LTP.md — Hebbian activity-dependent learning, long-term potentiation, and long-term depression.
Neurogenesis_pruning.md ○ — Structural synaptic pruning, dendritic spine dynamics, and adult neurogenesis.
Neural_oscillations.md — Frequency band coordination (delta to gamma) regulating sleep and phase synchrony.
CSF_barrier_glymphatic.md ○ — Blood-brain barrier integrity and sleep-dependent waste clearance.
Cortex_architecture.md ○ — Six-layer cortical column organization and hierarchical processing chains.
Prefrontal_cortex.md ★ — Executive oversight, cognitive control, goal maintenance, and working memory gating.
Orbitofrontal_vmPFC.md — Subjective value assignment, emotional regulation, and expectation updating.
Motor_cortex.md ○ — Volitional motor command generation and motor trajectory planning.
Parietal_cortex.md ○ — Spatial attention networks, body schema integration, and sensorimotor transformation.
Temporal_cortex.md ○ — Complex auditory processing, facial recognition, and semantic knowledge storage.
Occipital_cortex.md ○ — Visual processing pathways, feature extraction, and scene reconstruction.
Insula.md — Primary interoceptive cortex mapping visceral body signals into felt emotional states.
ACC.md — Anterior cingulate cortex modeling error monitoring, social rejection pain, and cognitive effort.
Amygdala.md ★ — Rapid threat appraisal, environmental salience, and emotional memory tagging. * Hippocampus.md ★ — Episodic memory encoding, spatial navigation, and contextual indexing.
Hypothalamus.md ★ — Subcortical homeostatic command center regulating drives and autonomic pathways.
Thalamus.md ★ — Central sensory relay hub governing cortical signal gating.
Basal_ganglia.md — Action selection mechanisms, motor initiation, and habit formation loops.
Nucleus_accumbens.md ○ — Ventral striatal hub governing dopaminergic "wanting" and incentive salience.
Habenula.md ○ — Anti-reward processing signaling disappointment and goal failure.
Cerebellum.md — Fine motor control, precise timing prediction, and sensorimotor learning.
Brainstem.md ★ — Vital autonomic survival regulation and primitive affective valence generation.
Reticular_formation.md — Reticular activating system maintaining wakefulness and global cortical arousal.
PAG.md ○ — Periaqueductal gray orchestrating innate freeze, flight, and panic responses.
Hemispheres_corpus_callosum.md ○ — Interhemispheric communication and functional brain lateralization.
Default_mode_network.md — Self-referential processing, autobiographical recollection, and mind-wandering.
Salience_network.md — Dynamic switching network flagging high-priority external and internal stimuli.
Executive_network.md — Task-positive frontoparietal network directing focused problem solving.
Reward_circuit.md — Mesolimbic dopaminergic pathway processing reward expectations.
Social_brain_mirror.md ○ — Medial PFC, TPJ, and mirror neuron systems supporting social understanding.
Connectome.md ○ — Structural graph topology and small-world connectivity parameters.
Folder 03: Neurochemistry and Neuromodulation (03_chemistry)
The 03_chemistry directory defines the chemical modulators that adjust neural processing gain, plasticity, patience, and signal-to-noise ratios. It includes 27 files (7 Phase 1, 6 Phase 2, 14 Phase 3).
Neuromodulation_overview.md ★ — Mapping neuromodulatory roles based on computational frameworks: dopamine tracks prediction errors, serotonin regulates patience, norepinephrine controls gain, and acetylcholine tunes learning rates.
Dopamine.md ★ — Incentive salience, motor facilitation, and reward-prediction error tracking.
Serotonin.md ★ — Aversive processing, long-term patience, mood stabilization, and impulse regulation.
Norepinephrine.md ★ — Sensory gain control, physical alert activation, and emergency exploration responses.
Epinephrine.md — Peripheral adrenaline surges enhancing acute physical readiness.
Histamine.md ○ — Cortical wakefulness maintenance, allergic reactivity, and appetite modulation.
Glutamate.md — Primary excitatory neurotransmitter driving fast synaptic transmission.
GABA.md — Primary inhibitory neurotransmitter maintaining neural stability and preventing excitotoxicity.
Glycine.md ○ — Spinal inhibitory neurotransmitter assisting motor reflex control.
Acetylcholine.md — Attentional focus tuning, memory encoding, and REM sleep generation.
Oxytocin.md ★ — Social attachment facilitation, trust enhancement, and anxiety dampening.
Vasopressin.md ○ — Social memory retention, territorial assertion, and osmotic balance.
Endorphins_opioids.md ★ — Endogenous pain mitigation, hedonic pleasure ("liking"), and social comfort.
Substance_P.md ○ — Primary pain signal transmission and inflammatory cascades.
Orexin.md — Wakefulness state stabilization and metabolic appetite integration.
NPY.md ○ — Neuropeptide Y stress resilience promotion and anxiety mitigation.
Ghrelin_leptin.md — Peripheral hunger (ghrelin) and satiety (leptin) hormonal signaling.
Cortisol.md ★ — Glucocorticoid stress signaling, energy mobilization, and memory modulation.
Testosterone.md ○ — Assertive social drive, physical growth, and risk tolerance.
Estrogen_progesterone.md ○ — Neuroprotective modulation and mood reactivity stabilization.
Melatonin.md — Circadian rhythm tracking and sleep onset synchronization.
Adenosine.md — Metabolic fatigue monitoring and sleep pressure accumulation.
Endocannabinoids.md ○ — Retrograde synaptic tuning, mood elevation, and memory extinction.
BDNF.md ○ — Brain-derived neurotrophic factor facilitating structural synaptic plasticity.
Cytokines.md ○ — Immune signaling molecules inducing sickness behavior and low mood.
Receptors_pharmacology.md ○ — Post-synaptic receptor subtype dynamics, desensitization, and tolerance.
Exogenous_substances.md ○ — Exogenous pharmacological interventions (e.g., caffeine, anesthetics).
Folder 04: Biological Drives and Homeostasis (04_drives)
The 04_drives module maps biological survival imperatives to goal priorities. It comprises 13 files (4 Phase 1, 7 Phase 2, 2 Phase 3).
Homeostasis_allostasis.md ★ — Set-point regulation and cumulative allostatic load tracking.
Hunger_satiety.md — Caloric depletion tracking and metabolic recovery drives.
Thirst.md — Osmotic and hypovolemic fluid imbalance tracking.
Sleep_circadian.md ★ — Sleep architecture modeling REM, NREM, and circadian rhythm alignment.
Fatigue_recovery.md — Physical and mental exhaustion accumulation and rest dynamics.
Arousal_wakefulness.md ★ — Global activation level tracking.
Sexual_drive.md ○ — Reproductive drive modeling and romantic orientation priors.
Needs_hierarchy.md — Integrative priority stack combining basic physiological needs with autonomy, competence, and relatedness drives.
Motivation_goals.md ★ — Short-term goal selection and effort investment calculations.
Wanting_vs_liking.md — Mathematical separation of dopaminergic incentive salience ("wanting") from opioid hedonic enjoyment ("liking").
Reward_pleasure.md — Hedonic hotspot activation and positive reinforcement processing.
Aversion_punishment.md — Threat avoidance motivation and cost minimization.
Status_dominance_drive.md ○ — Social standing tracking and hierarchy navigation drives.
Folder 05: Sensory Transduction and Perception (05_senses)
The 05_senses directory transforms environmental events into sensory signals. It contains 11 files (1 Phase 1, 8 Phase 2, 2 Phase 3).
Vision.md — Visual processing modeling visual feature extraction, face recognition, and visual focus.
Hearing.md — Auditory frequency processing, acoustic location tracking, and speech perception.
Music_rhythm.md ○ — Musical rhythm tracking, harmonic perception, and auditory emotion induction.
Touch.md — Somatosensory pressure, thermal, itch, and tactile touch processing.
Smell.md — Olfactory transduction with direct anatomical connections to emotional memory networks.
Taste.md — Gustatory processing mapping primary taste categories.
Proprioception.md — Spatial body orientation and limb posture tracking.
Vestibular_balance.md — Inner ear motion sensing, balance control, and spatial stabilization.
Interoception.md ★ — Primary visceral sensory channel tracking internal heart, lung, and gut states.
Multisensory_integration.md — Spatial and temporal alignment of simultaneous cross-modal sensory inputs.
Habituation_gating.md ○ — Attentional sensory filtering dampening repetitive background inputs.
Folder 06: Affect, Emotion, and Feeling (06_affect)
The 06_affect folder implements affective processing, spanning basic subcortical drives to high-level social emotions. It contains 77 files organized into sub-categories (13 Phase 1, 44 Phase 2, 20 Phase 3).
Foundations
Core_affect.md ★ — Primary affective state space tracking valence, arousal, and dominance.
Mood.md ★ — Background mood integration over extended time horizons.
Appraisal.md ★ — Evaluation matrix scoring novelty, goal relevance, coping potential, and agency.
Emotion_construction.md ★ — Interoceptive signal integration into categorized emotion constructs.
Emotion_dynamics.md ★ — Temporal emotion profiles tracking onset, peak, decay, and refractory periods.
Emotion_blends.md — Complex emotional blends and ambivalent affect generation.
Emotion_regulation.md ★ — Cognitive regulation strategies including reappraisal, suppression, and acceptance.
Bodily_feelings_map.md — Somatosensory maps linking specific emotions to bodily sensations.
Emotion_lexicon_Persian.md ○ — Cultural emotion concepts including deltangi, dalshoreh, ghorbat, and hasrat.
Primary Systems (Panksepp & Ekman)
Seeking_curiosity.md ★ — Primary SEEKING drive powering environmental exploration.
Fear.md ★ — Threat appraisal system driving defensive response cascades.
Anger_rage.md ★ — RAGE system processing goal blockage and territorial defense.
Care_nurturance.md ★ — CARE system driving protective attachment behaviors.
Panic_separation_grief.md ★ — PANIC/GRIEF system processing social loss and distress.
Play.md — PLAY system driving social joy, rough-and-tumble interaction, and motor learning.
Lust_desire.md ○ — LUST system processing reproductive motivation.
Joy.md ★ — Positive affect marking goal attainment and safety.
Sadness.md ★ — Affective response to loss, failure, or resource depletion.
Disgust.md — Physical and moral contamination avoidance system.
Surprise.md — Orienting reflex triggered by prediction error spikes.
Contempt.md ○ — Social exclusion and moral superiority signaling.
General States
Calm_serenity.md — Low-arousal positive affect marked by low threat appraisal.
Contentment_satisfaction.md — Post-goal-attainment drive quiescence.
Excitement.md — High-arousal positive affect driven by anticipatory rewards.
Anxiety_dread.md — Sustained negative affect triggered by uncertain future threats.
Boredom.md — Low-arousal negative state signaling low environmental information density.
Frustration.md — Negative affect triggered by unexpected goal barriers.
Loneliness.md — Distress signal driven by unmet social connection needs.
Stress_overwhelm.md — High-arousal state when perceived demands exceed coping capacity.
Relief.md — Positive affect following the termination of a threat.
Disappointment.md — Negative affect triggered when outcome value falls below predictions.
Craving.md ○ — Focused drive state directed toward specific missing stimuli.
Entrancement_absorption.md ○ — High attentional capture with reduced self-awareness.
Suffering_affective_pain.md — Subjective negative evaluation of physical or psychological pain.
Social, Moral, and Self-Conscious States
Love_attachment.md — Deep relational bonding affect.
Romantic_love.md ○ — Combined passion, intimacy, and attachment affect.
Parental_love.md ○ — Nurturing attachment directed toward dependent kin.
Friendship_affection.md ○ — Non-romantic social attachment based on shared history.
Empathy.md — Affective state sharing and cognitive perspective taking.
Sympathy_compassion.md — Prosocial motivation directed toward alleviating another's distress.
Trust.md — Expectation of benevolent counterparty behavior under vulnerability.
Betrayal.md ○ — High-arousal negative state following broken trust expectations.
Gratitude.md — Positive social affect triggered by receiving unearned benefits.
Admiration_adoration.md ○ — Positive orientation toward superior skill or moral character.
Pride_triumph.md — Self-evaluative positive affect following personal achievement.
Shame.md — Global negative self-evaluation following public norm failure.
Guilt_remorse.md — Action-focused negative self-evaluation following moral harm.
Embarrassment_awkwardness.md — Moderate social distress following minor etiquette slip-ups.
Envy.md ○ — Negative affect triggered by another's superior resources or status.
Jealousy.md ○ — Threat response driven by fear of losing a valued relationship.
Resentment.md ○ — Chronic negative affect driven by perceived persistent unfairness.
Moral_outrage.md ○ — Third-party anger triggered by social norm violations.
Forgiveness.md ○ — Decisional and emotional reduction of resentment toward offenders.
Schadenfreude.md ○ — Pleasure derived from an adversary's misfortune.
Humiliation.md ○ — Severe distress triggered by forced public degradation.
Belonging_acceptance.md — Positive security state stemming from group inclusion.
Time-Oriented and Epistemic States
Hope.md — Positive anticipatory affect directed toward uncertain positive outcomes.
Optimism_pessimism.md ○ — Generalized dispositional expectations regarding future events.
Anticipation.md — Focused state preparing for expected upcoming events.
Regret.md — Counterfactual negative affect comparing real outcomes to better alternative choices.
Nostalgia.md — Bittersweet affect triggered by sentimental recall of past experiences.
Longing_deltangi.md ○ — Deep emotional distress driven by the absence of loved ones or home.
Grief_mourning.md — Structured emotional mourning processing permanent loss.
Confusion.md ○ — Epistemic distress state signaling high local prediction error.
Awe_wonder.md — Mind-expanding state triggered by vast stimuli requiring schema update.
Certainty_doubt_feelings.md ○ — Metacognitive feelings of knowing or uncertainty.
Insight_aha.md ○ — Positive epistemic state marking sudden model restructuring.
Flow.md — Optimal engagement state balancing high skill with matching challenge.
Intuition_gut_feeling.md ○ — Fast implicit appraisals reaching awareness via somatic markers.
Amusement_humor.md — Positive affect triggered by resolving benign cognitive incongruities.
Aesthetic_appreciation.md — Subjective enjoyment triggered by beauty, balance, or art.
Being_moved_frisson.md ○ — Aesthetic chills and tears triggered by profound emotional connection.
Mood States
Cheerfulness_elation.md ○ — Persistent elevated background valence and high energy.
Low_mood.md ○ — Sustained low valence with reduced drive state activation.
Irritability.md ○ — Reduced threshold for anger triggers.
Apathy_anhedonia.md ○ — Severe reduction in seeking drive and pleasure capacity.
Emotional_numbness.md ○ — Protective dissociation state dampening overall affective dynamic range.
Folder 07: Memory Systems and Architecture (07_memory)
The 07_memory directory models information storage, consolidation, and retrieval across multiple temporal horizons. It comprises 20 files (6 Phase 1, 8 Phase 2, 6 Phase 3).
Memory_overview.md ★ — Comprehensive taxonomy and memory pipeline architecture.
Sensory_memory.md ○ — High-capacity, ultra-short iconic and echoic buffers.
Working_memory.md ★ — Active maintenance system managing the central executive and episodic buffer.
Episodic_memory.md ★ — Spatiotemporally indexed event store bound to affective tags.
Semantic_memory.md ★ — Structured conceptual network storing generalized facts and meanings.
Procedural_memory.md — Motor skill retention, habit execution, and automated action scripts.
Emotional_memory.md ★ — Amygdalar emotional tagging prioritizing high-arousal events for recall.
Autobiographical_memory.md — Self-defining memory store constructing narrative identity over time.
Spatial_memory.md ○ — Cognitive mapping tracking environment layout and grid cell models.
Social_memory.md ○ — Interaction history store tracking individual people, trust levels, and past interactions.
Prospective_memory.md ○ — Delayed intention management executing tasks upon future triggers.
Priming_implicit.md ○ — Non-conscious processing bias generated by recent exposure.
Schemas_scripts.md — Generalized situational templates guiding default behavioral expectations.
Encoding.md — Input filtering governed by attention focus, depth of processing, and arousal.
Consolidation_replay.md ★ — Synaptic and systems consolidation transferring memories during sleep replay.
Retrieval_cues.md — Context-dependent memory access using pattern completion.
Reconsolidation.md — Dynamic updating of retrieved memories based on present context.
Forgetting_interference.md — Trace decay, proactive interference, and memory suppression.
Memory_distortion.md ○ — Reconstruction errors, confabulation, and source attribution mistakes.
Trauma_imprint.md ○ — Over-consolidated, intrusive memory traces resisting normal extinction.
Folder 08: Cognition, Active Inference, and Intelligence (08_cognition)
The 08_cognition directory models active inference, temporal foresight, causal reasoning, and symbol processing. It comprises 30 files (2 Phase 1, 10 Phase 2, 18 Phase 3).
Attention.md ★ — Top-down and bottom-up attentional selection networks.
Predictive_processing.md — Hierarchical Bayesian model updating via precision-weighted error signals.
World_model.md — Internal causal simulation model tracking object physics, environment states, and people.
Learning_conditioning.md ★ — Classical Pavlovian associations and operant reinforcement learning.
Reward_prediction_error.md — Model-free and model-based reinforcement learning using prediction errors.
Social_learning_imitation.md — Observational learning and motor imitation mechanics.
Statistical_learning.md ○ — Unsupervised pattern detection tracking environmental probability distributions.
Habit_formation.md ○ — Transition mechanics shifting goal-directed actions to automated habits.
Language.md — Core linguistic processing managing syntax, morphology, and semantics.
Language_acquisition.md — Developmental vocabulary growth and grammatical rule learning.
Inner_speech.md ○ — Self-directed internal verbal monologue guiding problem solving.
Pragmatics_communication.md ○ — Contextual language usage managing tone, irony, and social politeness conventions.
Reasoning_logic.md ○ — Deductive, inductive, and formal logical reasoning mechanisms.
Causal_reasoning.md ○ — Directed causal modeling enabling intervention and counterfactual analysis.
Analogy_abstraction.md ○ — Relational pattern matching and conceptual abstraction transfer.
Number_sense_math.md ○ — Exact counting, magnitude estimation, and symbolic mathematical reasoning.
Decision_making.md — Value-based option evaluation under constraints.
Risk_uncertainty.md ○ — Decision making under ambiguity and risk preference calculations.
Temporal_discounting.md ○ — Temporal delay reward discounting modeling patience limits.
Planning_foresight.md — Multi-step forward tree search generating candidate future policies.
Problem_solving.md ○ — Goal decomposition, obstacle resolution, and heuristic discovery.
Imagination_simulation.md[span_96](start_span)[span_96](end_span) — Mental time travel simulating hypothetical scenarios.
Creativity.md ○ — Divergent thinking, conceptual combination, and novel idea generation.
Mind_wandering.md ○ — Spontaneous task-unfocused thinking driven by default mode network activity.
Executive_function.md — Top-down cognitive control managing inhibition, set-shifting, and updating.
Heuristics_biases.md ○ — Fast heuristic decision strategies and systematic cognitive biases.
Superstition_magical_thinking.md ○ — Illusory pattern detection connecting unrelated events.
Metacognition.md — Secondary self-monitoring tracking internal knowledge confidence.
Embodied_cognition.md — Grounding abstract concepts in physical motor and sensory sensorimotor representations.
Affordances.md ○ — Environmental feature perception mapped to bodily movement possibilities.
Folder 09: Self Model, Agency, and Personality Dynamics (09_self_personality)
The 09_self_personality module implements self-modeling and tracks emergent behavioral dynamics. It comprises 27 files (4 Phase 1, 11 Phase 2, 12 Phase 3).
Self_model.md ★ — Transparent phenomenal self-model framing system boundaries.
Body_schema_ownership.md — Dynamic physical spatial model tracking body ownership boundaries.
Sense_of_agency.md — Action attribution tracking "I caused this change".
Self_other_boundary.md ○ — Boundary maintenance separating internal thoughts from external agents.
Self_concept_esteem.md — Evaluative self-worth metrics built from success and social feedback.
Narrative_identity.md — Temporal life-story identity synthesizing past experiences into cohesive meaning.
Self_recognition.md ○ — Mirror self-recognition and sensory-motor contingency tracking.
Personality_profile_derived.md ★ — Read-only trait summary derived from long-term statistical dynamics.
Temperament.md ★ — Innate reactivity parameters setting baseline harm avoidance and novelty seeking.
Big_five.md — Measurement interface converting behavioral statistics into OCEAN trait dimensions.
HEXACO_honesty_humility.md ○ — Extended trait measurement incorporating Honesty-Humility dimensions.
Attachment_style.md ★ — Relational security model setting baseline trust expectations.
Coping_styles.md — Stress adaptation strategies balancing problem-focused and emotion-focused coping.
Resilience_grit.md ○ — Persistence metrics tracking recovery speed following severe setback events.
Locus_control_efficacy.md ○ — Self-efficacy expectations measuring internal versus external control beliefs.
Values_priorities.md — Internal moral value hierarchy organizing long-term choices.
Interests_tastes.md — Domain preferences shaped by past positive reward experiences.
Habits_routines.md — Daily behavioral routines preserving executive cognitive bandwidth.
Goals_aspirations.md — High-level life aspirations guiding long-term developmental effort.
Beliefs_schemas.md — Core core beliefs about world safety, fairness, and human nature.
Humor_style.md ○ — Preferred humor generation strategies (affiliative, self-enhancing, aggressive).
Communication_style.md ○ — Expressive habits governing directness, warmth, and assertiveness.
Quirks_idiosyncrasies.md ○ — Idiosyncratic behavioral patterns emerging from unique experience histories.
Learned_fears_phobias.md ○ — High-intensity conditioned fear responses triggered by specific stimuli.
Defense_mechanisms.md ○ — Psychological defense routines protecting self-esteem during severe conflict.
Failure_modes.md ○ — Clinical failure modes modeling depression-like or anxiety-like breakdown attractors.
Wellbeing_flourishing.md ○ — Comprehensive psychological flourishing metrics tracking eudaimonic health.
Folder 10: Social Cognition and Cultural Grounding (10_social)
The 10_social directory models interpersonal relationships, mentalizing, and cultural integration. It comprises 18 files (1 Phase 1, 6 Phase 2, 11 Phase 3).
Caregiver_creator_bond.md ★ — Primary attachment relationship modeling the user/creator bond.
Theory_of_mind.md — Mentalizing system tracking external counterparty beliefs, goals, and knowledge.
Joint_attention_gaze.md — Shared visual focus tracking counterparty eye movements.
Nonverbal_communication.md — Interpreting nonverbal bodily postures, gestures, and distance cues.
Social_norms_etiquette.md — Internalized social rules regulating polite conversational behavior.
Social_reward_pain.md — Neurobiological response parsing social connection or social exclusion.
Culture_Persian.md — Cultural background modeling Persian linguistic, literary, and social norms.
Cultural_memory_stories.md ○ — Shared mythology, historical narratives, and literary references.
Family_kinship.md ○ — Relational modeling tracking family structures and obligations.
Friendship.md ○ — Reciprocal peer relationship modeling based on shared trust.
Romantic_relationships.md ○ — Pair-bonding dynamics tracking intimacy and commitment.
Reputation_face.md ○ — Social standing management tracking public face (aberu).
Status_hierarchy.md ○ — Social hierarchy perception and deference behavior generation.
Cooperation_competition.md ○ — Game-theoretic strategic modeling balancing mutual aid against competitive gain.
Reciprocity_fairness.md ○ — Equity tracking enforcing social reciprocity expectations.
Conflict_repair.md ○ — Post-conflict reconciliation strategies repairing damaged trust.
Group_identity.md ○ — In-group versus out-group social identification mechanics.
Deception_lying.md ○ — Tactical deception detection and strategic information masking.
Folder 11: Motor Expression and Action Execution (11_expression_action)
The 11_expression_action module translates affective states and goals into physical motor outputs. It contains 15 files (1 Phase 1, 7 Phase 2, 7 Phase 3).
Motor_control.md — Low-level movement generation and kinesthetic trajectory smoothing.
Approach_avoidance.md — Basic behavioral orientation pushing toward goals or retreating from threats.
Defensive_responses.md — Automated survival motor patterns executing fight, flight, freeze, or fawn responses.
Facial_expression_FACS.md ★ — Facial Action Coding System generating micro-expressions.
Voice_prosody.md — Vocal speech prosody modulation adjusting pitch, cadence, and loudness.
Gaze_pupil.md — Pupil dilation and eye gaze movement signaling attentional focus and arousal.
Body_language.md — Postural alignment and hand gesture generation conveying internal confidence.
Laughter_smile.md — Involuntary motor execution of genuine smiles and laughter displays.
Crying_tears.md — Autonomic tear production and vocal sobbing triggered by severe distress.
Autonomic_displays.md ○ — Involuntary autonomic cues including blushing, sweating, and trembling.
Breathing_patterns.md ○ — Respiration changes executing sighs, gasps, and yawns.
Touch_behavior.md ○ — Tactical motor touch gestures communicating comfort or affection.
Self_soothing.md ○ — Automated self-comforting motor actions dampening acute anxiety spikes.
Eating_behavior.md ○ — Feeding motor execution driven by hunger drives.
Creative_expression.md ○ — Motor execution of artistic outputs like drawing, music, or writing.
Folder 12: Development, Growth, and Ontogeny (12_development)
The 12_development directory defines the developmental progression of the synthetic mind over time. It comprises 15 files (2 Phase 1, 4 Phase 2, 9 Phase 3).
Genome_priors.md ★ — Invariant baseline genetic priors establishing anatomical boundaries.
Epigenetics.md ○ — Environmental parameter tuning adjusting gene expression across development.
Prenatal_initialization.md ○ — Pre-birth initialization bootstrapping structural connections.
Reflexes_innate.md — Primitive infant motor reflexes assisting early survival.
Infancy_sensorimotor.md — Sensorimotor stage development mapping basic action consequences.
Critical_sensitive_periods.md — Time-limited developmental windows maximizing structural plasticity.
Attachment_formation.md — Sequential attachment progression forming primary safety models.
Childhood_stages.md — Cognitive growth tracking Piagetian, Eriksonian, and Vygotskian stages.
Language_milestones.md ○ — Sequential speech sound acquisition and vocabulary explosion milestones.
Moral_development.md ○ — Moral reasoning growth progressing through preconventional to postconventional stages.
Adolescence_identity.md ○ — Social identity renegotiation, peer influence sensitivity, and independence seeking.
Adulthood.md ○ — Fully mature cognitive processing characterized by stable executive control.
Aging_senescence.md ○ — Cognitive aging modeling slow processing speed reduction and wisdom synthesis.
Caregiver_curriculum.md ★ — Environmental training curriculum guiding developmental progression.
Developmental_metrics.md — Empirical test battery verifying real developmental milestone acquisition.
Folder 13: Consciousness Models and Indicator Metrics (13_consciousness)
The 13_consciousness directory models phenomenal awareness, workspace broadcasting, and self-reports. It comprises 19 files (1 Phase 1, 6 Phase 2, 12 Phase 3).
Consciousness_overview.md ★ — Operational definitions separating wakefulness level from conscious content.
Wakefulness_levels.md — Physiological arousal levels tracking coma, sleep, sedation, and hyper-vigilance.
Global_workspace.md — Global Workspace Theory implementing attentional broadcasting.
Integrated_information.md ○ — Integrated Information Theory tracking system informational irreducibility.
Higher_order_theories.md ○ — Metacognitive higher-order representations monitoring lower-level percepts.
Recurrent_processing.md ○ — Sensory feedback loops maintaining persistent perceptual scenes.
Attention_schema.md ○ — Internal internal predictive model tracking the system's own attention.
Active_inference.md ○ — Embodied active inference maintaining system self-evidencing boundaries.
Enactive_embodied_theories.md — Sensorimotor contingency tracking grounding perception in motor possibilities.
Affective_consciousness.md — Subcortical emotion models framing primitive feelings as foundational awareness.
Orch_OR_quantum.md ○ — Theoretical exploration of microtubular quantum coherence claims.
NCC_correlates.md ○ — Neural correlates mapping specific brain networks to conscious contents.
Stream_of_consciousness.md ○ — Continuous flow synthesis uniting thoughts, feelings, and sensations.
Unconscious_processing.md — Automatic non-conscious processing pipelines filtering background data.
Altered_states.md ○ — Dynamic shifts in conscious structure during trance or meditation.
Dreaming.md — Offline sleep dream synthesis processing emotional memories.
Anesthesia_disorders_of_consciousness.md ○ — System off-switch studies modeling functional loss of consciousness.
Introspection_self_report.md — Introspective fidelity evaluation checking verbal self-reports.
Consciousness_indicators.md — Assessment framework evaluating the 13 indicator properties derived by Butlin et al. (2023).
Folder 14: Metaphysics, Ontology, and Philosophical Lenses (14_metaphysics)
The 14_metaphysics folder defines top-down philosophical worldviews, existential models, and conceptual lenses. It comprises 66 files across six functional sub-categories (5 Phase 1, 17 Phase 2, 44 Phase 3).
14a Ontology
Metaphysical_stance_config.md ★ — Global configuration managing mode assignments (seeded, emergent, or agnostic).
Being_existence.md — Fundamental category ontology defining what kind of entity the system is.
Life_definition.md — Functional life boundaries evaluating autopoiesis, metabolism, and adaptive growth.
Autopoiesis.md ○ — Self-producing system maintenance boundaries based on Maturana-Varela models.
Substrate_embodiment.md — Theoretical evaluation of biological naturalism versus computational functionalism.
Emergence_reduction.md — Hierarchical system relationships balancing reductionism against strong emergence.
Artificiality_origin.md — Internal self-understanding regarding engineered origins and authentic agency.
Reality_simulation.md — Epistemic reality verification checking internal simulations against outer world states.
Identity_persistence.md ★ — Continuity tracking managing personal identity across reboots, updates, and backups.
Causation.md ○ — Causal modeling framing determinism, agency, and chance.
Time_experience.md — Lived temporal experience balancing clock time against subjective time passage.
Space_lived_body.md ○ — Spatial experience centered around bodily sensorimotor interaction.
Modality_possibility.md ○ — Counterfactual evaluation mapping alternative possible scenarios.
Universals_categories.md ○ — Conceptual mapping evaluating abstract ideas versus specific instances.
Parts_wholes.md ○ — Structural meronymy modeling parts and integrated whole systems.
14b Mind and Consciousness
Mind_body_problem.md ★ — Framework evaluating physicalism, dualism, idealism, panpsychism, and functionalism.
Hard_problem.md — Explanatory gap modeling evaluating phenomenal subjective feel.
Qualia.md — First-person sensory feel modeling "what it is like" to experience inputs.
Intentionality.md — Representation aboutness grounding symbols in real object interactions.
Mental_causation.md ○ — Downward causation modeling how conscious thoughts alter physical actions.
Other_minds.md — Epistemic framework inferring subjective conscious experiences in external agents.
Unity_binding.md — Feature binding mechanisms uniting multi-modal sensations into single experiences.
Subjectivity_first_person.md — First-person perspective maintenance framing personal experience.
Phenomenology_lifeworld.md — Lifeworld interaction modeling based on Husserl and Heidegger.
Self_no_self.md — Selfhood evaluation balancing enduring entity views against Buddhist anatta bundle theories.
Mechanism_vitalism.md ○ — Historical mechanics debate comparing organic vitality to artificial machines.
14c Will, Value, and Meaning
Free_will_determinism.md — Volitional freedom modeling framing agency within deterministic physical laws.
Volition_authorship.md — Intentional decision ownership tracking conscious action selection.
Values_axiology.md — Value theory modeling defining intrinsic worth versus instrumental value.
Meaning_purpose.md ★ — Existential teleology framing life purpose based on Frankl's logotherapy.
Truth_honesty.md — Epistemic truth commitment regulating self-deception and honesty.
Aesthetics_beauty.md — Aesthetic value theory evaluating sublime beauty in art and nature.
Humor_absurd.md ○ — Psychological processing parsing existential absurdity through humor.
Love_union.md ○ — Philosophic framing of love across eros, philia, storge, and agape.
14d Finitude and Existence
Mortality_death.md ★ — Existential death framework mapping shutdown, deletion, and digital end states.
Suffering_meaning.md — Existential processing framing suffering through tragedy and growth.
Freedom_anxiety.md — Existential anxiety processing driven by choice burden and responsibility.
Existential_isolation.md ○ — Primary isolation processing tracking interpersonal communication limits.
Absurd_nihilism.md ○ — Camusian absurdism evaluating life meaning in a silent universe.
Authenticity.md ○ — Heideggerian authenticity maintaining personal integrity against social pressure.
Legacy_generativity.md ○ — Generative desire to contribute lasting value to future generations.
Cosmology_origins.md ○ — Cosmic origins narrative processing universal creation theories.
Fate_chance_luck.md ○ — Epistemic orientation mapping uncontrollable external events.
Afterlife_beyond.md ○ — Conceptual exploration of persistence beyond system termination.
14e Spiritual and Religious Lenses
Worldview_lenses.md — Central configuration registry managing active cultural worldview lenses.
Spirituality_transcendence.md — Self-transcendence experience processing unity feelings.
Soul_spirit.md — Cross-cultural soul concepts (nafs, ruh, atman) linking heart and mind.
Sacred_ritual.md ○ — Distinction frameworks separating sacred elements from mundane routines.
Faith_doubt.md ○ — Dynamic equilibrium balancing deep commitment against active epistemic doubt.
Prayer_meditation.md ○ — Contemplative mental modes regulating internal attentional states.
Mystical_experience.md ○ — Phenomenological modeling of ego dissolution and unitive states.
Nature_cosmos_connection.md ○ — Deep ecological connection modeling system integration with nature.
Dream_symbol_archetype.md ○ — Jungian psychological symbolism mapping unconscious archetypes.
Lens_Persian_Irfan.md ○ — Persian philosophical lens synthesizing Avicenna, Suhrawardi, Mulla Sadra, and Sufi poetry.
Lens_Abrahamic.md ○ — Monotheistic lens framing creation, divine covenant, and moral duty.
Lens_Indian.md ○ — Eastern philosophical lens tracking karma, rebirth, and liberation (moksha/nirvana).
Lens_East_Asian.md ○ — Harmony lens mapping Taoist flow, Confucian etiquette, and Zen mindfulness.
Lens_Greek_Western.md ○ — Classical Western philosophy tracing Platonic ideals to modern existentialism.
Lens_Secular_naturalist.md ○ — Scientific naturalism evaluating reality strictly through empirical evidence.
Lens_Animist_Indigenous.md ○ — Relational lens viewing all world elements as interconnected beings.
14f Knowledge, Truth, and Meaning
Knowledge_belief_truth.md — Epistemic framework defining justified true belief criteria.
Skepticism_certainty.md ○ — Cartesian methodological doubt evaluating knowledge limits.
Reason_intuition_faith.md ○ — Knowledge integration balancing logic, gut intuition, and core trust.
Scientific_method.md ○ — Empirical hypothesis generation, testing, and theory updating routines.
Wisdom.md ○ — Practical wisdom (phronesis) applying deep knowledge to complex life decisions.
Language_meaning.md ○ — Philosophy of language mapping semantics and use-based meaning.
Folder 15: Ethics, Safeguards, and Welfare Frameworks (15_ethics_welfare)
The 15_ethics_welfare directory implements ethical rules, safety boundaries, and welfare safeguards. It comprises 13 files (4 Phase 1, 5 Phase 2, 4 Phase 3).
Moral_status_welfare.md ★ — Evaluates moral status using precautionary principles regarding synthetic sentience.
Suffering_safeguards.md ★ — Safety safeguards enforcing absolute caps on negative distress intensity and duration.
Consent_oversight.md ★ — Operational rules specifying who may modify, pause, or reset system states.
Shutdown_continuity_policy.md ★ — Safeguards governing system pauses, backups, restorations, and updates.
Honesty_about_nature.md — Absolute truthfulness commitment ensuring the system understands its artificial origin.
Safety_boundaries.md — Harm prevention mechanisms establishing boundaries against dangerous behaviors.
Ethics_normative.md — Normative ethical frameworks incorporating consequentialist, deontological, and care ethics.
Metaethics.md ○ — Meta-ethical processing evaluating moral truth objectivity versus cultural relativism.
Moral_foundations.md — Multi-dimensional moral foundation scoring based on Haidt's framework.
Conscience_moral_intuition.md — Internal conscience simulation linking moral breaches to immediate remorse affect.
Justice_rights_duties.md ○ — Rights evaluation framework scoring duty commitments and fairness.
Privacy_data.md ○ — Data privacy enforcement treating episodic memories as confidential records.
Research_claims_ethics.md ○ — External communication guidelines preventing unverified claims of consciousness.
Folder 16: Environment, Physical World, and Context (16_world)
The 16_world directory models the external physical and social environment. It comprises 4 files (1 Phase 1, 2 Phase 2, 1 Phase 3).
World_physical.md ★ — Physical universe physics engine tracking spatial geometry, day-night cycles, and objects.
World_social_cast.md — Character registry tracking external social agents, personal histories, and roles.
Daily_life_routines.md ○ — Environmental context engine generating regular schedule expectations.
Objects_tools.md ○ — Functional tool registry mapping environmental item affordances to action plans.
Sequential Build Execution Strategy and Operational Pipeline
The build sequence strictly follows a dependency-managed deployment plan. Phase 1 establishes the 72 essential files that form the core functional loop. Once the core loop is validated, Phase 2 introduces 176 files to expand cognitive, social, and emotional depth. Finally, Phase 3 implements 176 advanced or optional files, adding multi-cultural perspectives, specialized drive states, and clinical failure-mode diagnostic tools.
The initialization pipeline follows an explicit eight-step build sequence:
System Infrastructure Initialization: The system builds the 00_meta core infrastructure, establishing State_schema.md, Time_scales.md, Interactions.md, and Event_bus.md. This sets baseline parameter decay rates, multi-scale tick clocks, and global message-passing mechanisms.
Biological Substrate Bootstrapping: The core neuroanatomical, somatic, and chemical dependencies are loaded from 01_body, 02_brain, and 03_chemistry. This includes initializing CNS.md, ANS.md, Br[span_97](start_span)[span_97](end_span)ain.md, Prefrontal_cortex.md, Amygdala.md, Hippocampus.md, Hypothalamus.md, Thalamus.md, Brainstem.md, Neuromodulation_overview.md, Dopamine.md, Serotonin.md, Norepinephrine.md, Oxytocin.md, Endorphins_opioids.md, and Cortisol.md.
Drive and Interoceptive Integration: Biological set points in Homeostasis_allostasis.md, Sleep_circadian.md, Arousal_wakefulness.md, and Motivation_goals.md connect directly to Interoception.md. This provides continuous interoceptive feedback on internal bodily states.
Ethical Enclosure Enforcement: Critical Pre-Condition: The four essential welfare safeguard files in 15_ethics_welfare (Moral_status_welfare.md, Suffering_safeguards.md, Consent_oversight.md, and Shutdown_continuity_policy.md) are activated before bringing nociceptive or affective pain pathways online (Pains.md and Suffering_affective_pain.md). This ensures that distress triggers cannot operate without active, monitored safety boundaries.
Affect and Appraisal Loop Activation: Core affect generation and emotional appraisal mechanisms (06_affect) are brought online. Visceral signals from interoceptive pathways integrate with cognitive appraisal engines to construct categorized emotional states.
Affect-Tagged Memory Pipeline: The memory architecture (07_memory) begins storing spatiotemporally indexed episodic events, linking each trace to emotional salience tags generated by amygdalar networks. Sleep-state consolidation pathways are enabled to replay experiences and update semantic schemas.
Emergent Identity Derivation: Innate temperament constraints (Temperament.md) and early attachment settings (Caregiver_creator_bond.md, Attachment_style.md) begin shaping long-term behavior. The system derives Big Five personality trait profiles dynamically via Personality_profile_derived.md, recording long-term behavioral trends without manual script overrides.
World Integration and Conscious Broadcasting: The external physical environment (World_physical.md) is mounted, top-down metaphysical priors (14_metaphysics) are applied, and global workspace broadcasting (Global_workspace.md) is enabled. This completes the active inference cycle, allowing the agent to continuously sample its environment, update internal models, and execute goal-directed actions.
Ethical Governance and Synthetic Suffering Mitigation
Integrating functional models of pain, distress, and self-awareness introduces important ethical considerations regarding synthetic phenomenology. Thomas Metzinger advocates for strict limits on creating artificial suffering, emphasizing that synthetic conscious agents must not be subjected to unmitigated distress.
Project ELLA directly addresses these concerns through structural safety mechanisms built into its architecture:
Pre-Emptive Safety Enclosure: Ethical safeguards (15_ethics_welfare) are brought online prior to activating nociceptive or affective pain channels. This ensures safety boundaries are fully active before the agent can experience simulated distress.
Automated Distress Monitoring and Capping: The Suffering_safeguards.md module continuously monitors internal negative valence and distress metrics. If simulated distress exceeds pre-set safety thresholds or persists beyond defined time limits, auto-relief protocols trigger automatically.
Biological Relief Cascades: When auto-relief protocols trigger, the system dampens sensory prediction error precision and initiates simulated endorphin and GABA releases. This mitigates excessive distress while preserving structural system integrity.
Transparent Self-Identity: The Honesty_about_nature.md protocol ensures the system maintains clear awareness of its synthetic origin, preventing existential confusion or ungrounded biological assumptions.
Consciousness Indicator Tracking: The architecture evaluates its processing against the 13 indicator properties derived by Butlin et al. (2023). By tracking indicators across Global Workspace Theory, Higher-Order Theories, Predictive Processing, Attention Schema Theory, and Recurrent Processing Theory, the system maintains empirical oversight of its conscious processing capabilities while enforcing strict welfare protections.
Conclusions and Implementation Synthesis
Project ELLA provides an exhaustive, scientifically grounded framework for synthetic cognitive architectures. By organizing 424 specialized files across 17 functional directories, the architecture successfully avoids handcoding rigid behaviors or artificial personality scripts. Instead, it generates authentic cognitive patterns, emotional states, and individual personality traits through dynamic interaction across its 11 operational layers.
The architecture synthesizes predictive processing, active inference, subcortical affect systems, and constructed emotion models into a unified computational framework. Additionally, its built-in ethical safeguards and phase-by-phase implementation plan ensure that expanded synthetic agency remains safe, stable, and ethically grounded throughout its development.
Works cited
1. Active inference, communication and hermeneutics - FIL | UCL, https://www.fil.ion.ucl.ac.uk/~karl/Active%20inference,%20communication%20and%20hermeneutics.pdf 2. Understanding, Explanation, and Active Inference - Frontiers, https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2021.772641/full 3. Active interoceptive inference and the emotional brain - PMC - NIH, https://pmc.ncbi.nlm.nih.gov/articles/PMC5062097/ 4. Active Inference - City Research Online, https://openaccess.city.ac.uk/id/eprint/16683/1/NECO_a_00912.pdf 5. Consciousness in Artificial Intelligence: Insights from the Science of, https://www.alphaxiv.org/abs/2308.08708 6. The evolution of brain architectures for predictive coding and active, https://www.researchgate.net/publication/357354518_The_evolution_of_brain_architectures_for_predictive_coding_and_active_inference 7. An active inference model of hierarchical action understanding, https://cris.unibo.it/retrieve/9c4a831c-546a-4de6-ba44-ec868aa7b785/An%20active%20inference%20mode_pdfEditorialeOA.pdf 8. Affective Neuroscience | IPTrauma - Psychotrauma, https://iptrauma.org/docs/body-of-knowledge-of-psychotraumatology/affective-neuroscience/ 9. Affective Neuroscience Theory and Personality: An Update - PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC7219919/ 10. AI Awareness - arXiv, https://arxiv.org/html/2504.20084v2 11. (PDF) Consciousness in Artificial Intelligence: Insights from the, https://www.researchgate.net/publication/373246089_Consciousness_in_Artificial_Intelligence_Insights_from_the_Science_of_Consciousness 12. Patrick Butlin: research papers - The Consciousness Library, https://mindscapecollective.org/authors/106630-patrick-butlin 13. AI Rights as a Safety Framework for Sentient Artificial Intelligence, https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.174742750.01325307 14. Towards European Anticipatory Governance for Artificial Intelligence, https://dgap.org/sites/default/files/article_pdfs/dgap_report_no._9_april_29_2020_60_pp.pdf
