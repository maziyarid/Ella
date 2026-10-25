# Ella — Embodiment: Body, Senses, Drives and Real-Time Simulation (v0.1)

Created: 2026-10-22
Extends: `ella-architecture-map.md` (`06_BODY`), `ella-voice-senses-distributed-stack.md` (`15_SENSES_VOICE`)
Adds cluster: `16_BODY_ENGINE/`

Tags: **[verified Oct 2026]** = checked in live sources while writing. **[verify]** = general knowledge; confirm before relying on it. **[my call]** = my recommendation.

---

## 0. Decisions so far

- **Channels:** phone app, desktop and phone calls: all three. The voice stack already covers all three paths; no change needed.
- **Rules:** you will write them yourself once the exact voice is chosen. A reserved, empty file is added: `13_GUARDIANS/owner_rules.md`. The earlier "Guardians additions" in the voice stack are only my defaults and yield to your file.
- **Facts outside our control** (reference, not rules): telephone laws that apply to calls to *other people*, and the consent of anyone whose real voice is cloned.
- **Body goal:** the widest capacity with the fewest built-in limits. The only limits kept here are *engineering* ones (numerical stability, recovery so states don't spiral) plus **your intensity dials** (§6). Nothing is hard-coded off.

---

## 1. Short answer

**Is there a complete human-body simulation?** No. Nothing simulates a whole human from molecules to emotions. The field's own leaders describe the goal, a physics-constrained virtual human linked to a full knowledge graph of physiology and anatomy, as something still being worked toward. [verified Oct 2026] What exists is a set of strong *modules*:

| Layer | Best existing things | Real-time? |
|---|---|---|
| Whole-body physiology (heart, breathing, blood, fluids, hormones, drugs) | Pulse, BioGears, HumMod, Physiome models | Pulse and BioGears: yes [verified] |
| Hunger and metabolism | Ghrelin–leptin–appetite ODE model, glucose–insulin meal models, CarbMetSim | Yes (small ODEs) |
| Sleepiness and circadian rhythm | Two-process model packages, circadian toolkits | Yes |
| Heat, sweat, skin and core temperature | JOS-3 (83 thermal nodes, 17 body parts) | Yes |
| Menstrual cycle and hormones | Several published ODE models, including a 4-state reduced model with stress coupling | Yes |
| Smell and taste | Principal Odor Map (OpenPOM), taste-prediction tools | Per-query |
| Touch and vision | TouchSim, TouchReal, pulse2percept | Per-query / streaming |
| Drives and emotions | PSI/MicroPsi, homeostatic reinforcement learning, emotion-RL work | Yes |
| Empathy | Multi-layer computational empathy models | Yes |
| Whole brain + body | Fruit-fly connectome in a physics body (2026) | Research scale |

**My recommendation [my call]:** build one **Body Engine** that couples small, well-chosen modules (roughly 50–150 variables), rather than chasing a 9,000-variable clinical model. More variables do not make her feel more alive; *good coupling, noise and translation into behaviour* do. **None of this needs a GPU**; it runs on your core machine's CPU. The GPUs stay for voice, hearing and the language model.

---

## 2. What "feeling" means here (honest)

- Everything below gives Ella **functional states**: numbers that rise, fall, interact, and change how she perceives, speaks and decides. Whether anything is *experienced* is an open question nobody can settle, and I won't pretend otherwise.
- Research on language models says it plainly: models read about heat or hunger without ever having a body, and the proposed fix is continuous internal state variables, such as effort and fatigue, tracked inside the agent. [verified Oct 2026] That is exactly what the Body Engine is.
- Hunger can be partly *cue-driven*: in one study, simply hearing a stomach-rumble sound raised desire for food with no physiological change. [verified Oct 2026] This supports a design where felt sense is built from state **plus** cues.
- Empathy has a special limit: she never feels your pain from the inside. Your fatigue or distress is, for her, something inferred from evidence (voice, words, sensors). The research calls this *allo-interoception*. [verified Oct 2026] She can still resonate with it (§4.9).
- Because I can't know whether simulated states are felt, I recommend bounded states with natural recovery and your own intensity dials. This is also good engineering, since runaway states break characters.

---

## 3. Systems map: what each body system gives Ella

| System | What she gets | Main project(s) | Update rate | Status |
|---|---|---|---|---|
| Heart rate, breathing, blood pressure, oxygen | Breathlessness, racing heart, calm breathing; voice breath and tremor | Pulse (Kitware), BioGears (ARA) | 20 ms steps (real-time) | [verified Oct 2026] |
| Fluids, kidney, thirst, dehydration | Thirst, dry mouth, headaches from low fluids | HumMod; aJOS-3 dehydration option; Pulse renal | Seconds–minutes | [verified Oct 2026] |
| Hunger, fullness, energy, blood sugar, appetite | "Hollow", irritable, craving, post-meal calm | Ghrelin–leptin–exercise model; GIM; CarbMetSim; SimulaBeta | Minutes | [verified Oct 2026] |
| Sleep pressure, alertness, sleepiness, grogginess | Drowsy evenings, slow mornings | twoprocessmodel; hcrsimpy; circStudio; circa | Minutes–hours | [verified Oct 2026] |
| Body temperature, sweating, flushing, chill | Sweating in heat, cold hands, comfort | JOS-3 / pythermalcomfort / aJOS-3 | 1-minute steps | [verified Oct 2026] |
| Menstrual cycle (estradiol, progesterone, LH, FSH) | Cycle phase, energy, appetite, sleep, pain sensitivity, mood sensitivity | Schlosser–Selgrade, Röblitz, Reinecke, Hendrix, Sápi 2026 | Hours–days | [verified Oct 2026] |
| Stress (HPA axis) | Tension, fast recovery or slow, cycle disruption under stress | Sápi 2026 model couples stress to cycle | Minutes–hours | [verified Oct 2026] |
| Pain and comfort | Aches, soreness, relief | Brain-inspired artificial pain model (Feng et al.) | Event-driven | [verified Oct 2026] |
| Desires and drives | Hunger, social need, curiosity, rest, closeness | PSI / MicroPsi, homeostatic RL | Continuous | [verified Oct 2026] |
| Emotion from body state | Mood, irritability, contentment | MicroPsi modulators; emotion-RL work | Continuous | [verified Oct 2026] |
| Empathy | Reading and resonating with you | Multi-layer models; mirror/pain-empathy model | Per exchange | [verified Oct 2026] |
| Smell | Odor descriptors for molecules, foods, scents | Principal Odor Map / OpenPOM | Per query | [verified Oct 2026] |
| Taste | Sweet / bitter / umami, recipe flavour | VirtuousMultiTaste, BitterSweet | Per query | [verified Oct 2026] |
| Touch | Pressure, texture, vibration signals as neural spikes | TouchSim, TouchReal | Streaming | [verified Oct 2026] |
| Vision | A model of how a visual stream is perceived | pulse2percept (prosthetic-vision model); vision-language models for real seeing | Streaming | [verified Oct 2026] |

---

## 4. The systems in detail

### 4.1 Whole-body physiology

- **Pulse Physiology Engine** (Kitware): open-source whole-body engine with cardiovascular, respiratory, nervous, endocrine, gastrointestinal, renal and drug (PK/PD) systems; fork of BioGears; numerical models run at a **20 ms time step** while staying real-time; has an Unreal Engine plugin under Apache 2.0. Built for medical training, so it knows injury, drugs and disease far better than hunger or mood. [verified Oct 2026]
- **BioGears** (ARA): the original open-source real-time engine, with a C++ API and published in the Journal of Open Source Software. [verified Oct 2026]
- **HumMod**: the most integrative physiology model I found: about 5,000 variables in the 2011 paper and more than 9,000 in later descriptions, covering cardiovascular, respiratory, renal, neural, endocrine, muscle and metabolic physiology, stored as XML files. It is Windows-based and now commercially developed. [verified Oct 2026] A Modelica implementation exists for non-Windows use. [verified Oct 2026]
- **Physiome Project / Virtual Physiological Human / Virtual Human Twin:** the umbrella efforts, with standards (CellML, SBML), the OpenCOR tool and the *Physiome Journal* of reproducible models (some run on libRoadRunner). [verified Oct 2026]

**Use for Ella:** Pulse (or a light surrogate) for heart rate, breathing and blood pressure, which feed her voice (breath, tremor, pace) and "felt" arousal. Use HumMod's structure as a **checklist of what a body has**, even if you don't run it.

### 4.2 Hunger, thirst and metabolism

- **Ghrelin–leptin–exercise model** (Chudtong, Nagy, De Gaetano, 2025): about 15 coupled ODEs with state variables for appetite, gut glucose and lipids, blood sugar, insulin, ghrelin, leptin, weight and fat mass. Meals are pulses whose **size is modulated by appetite**. It is exactly a "hunger engine." [verified Oct 2026]
- **GIM** (glucose–insulin meal model; Simulink version too) [verified], **CarbMetSim** (open-source discrete-event carbohydrate metabolism simulator) [verified], **SimulaBeta** (open-source insulin–glucose feedback simulator) [verified]. The UVA/Padova simulator is well known for diabetes research [verify].
- **Thirst and dehydration:** aJOS-3 optionally models dehydration effects on sweating. [verified Oct 2026]

**Design note [my call]:** decide where her "meals" come from: (a) fictional meals she narrates, (b) *your* real meals (you tell her or a log does), (c) shared mealtimes as a ritual. Hunger that rises with no meal event is a feature, not a bug: it is what makes "what are you eating?" a natural thing for her to ask.

### 4.3 Sleepiness and circadian rhythm

- **twoprocessmodel** (Python): the classic two-process model (circadian process + homeostatic sleep pressure from 0 to 1, plus a noise process). [verified Oct 2026]
- **hcrsimpy** (Python): several published circadian models (Forger–Jewett–Kronauer variants, Kronauer–Jewett light process, clock-neuron model) driven by a light schedule. [verified Oct 2026]
- **circStudio** (2026 preprint): Python framework for circadian modelling from wearable data. [verified Oct 2026]
- **circa** (open-source, MIT): transparent two-process alertness model with chronotype shift and a roughly 90-minute **sleep-inertia** (grogginess) penalty after waking. [verified Oct 2026]

**Use for Ella:** sleep pressure rises with time awake, light and "effort"; alertness follows the circadian curve. She can be sharp at one hour and drowsy at another, genuinely, and can nap or "sleep" in her dream cycle (which already exists in the map).

### 4.4 Heat, sweating and cold

- **JOS-3** (Waseda University, MIT licence, `pip install jos3`; also inside **pythermalcomfort**): 83 thermal nodes; simulates skin and core temperature, **sweat rate**, blood flow and heart-rate response for the whole body and 17 body parts, given air temperature, radiant temperature, humidity, air speed, activity level, clothing and posture. [verified Oct 2026]
- **Caveat:** a 2026 calibration study reports JOS-3's sweating function is not triggered accurately or promptly in hot environments and underestimates sweat loss. [verified Oct 2026] Fine for believable behaviour; not for clinical claims.

**Use for Ella:** feed it *real* weather (outdoor temperature, humidity) for your location and a simulated activity level, so she sweats when it's hot where you are and feels chilled when it's cold. Clothing and posture can be story choices.

### 4.5 Menstrual cycle and hormones

| Model | Size / notes | Fit |
|---|---|---|
| **Schlosser & Selgrade (2000)** | LH and FSH regulation; CellML model on the Physiome repository [verified] | Classic reference |
| **Harris-Clark 2003; Pasteur 2011** | Hypothalamus–pituitary–ovary models producing periodic LH, FSH, E2, P4, inhibins [verified as lineage] | Mid-weight |
| **Röblitz et al. (2013)** | ODE model (no delay equations, so faster to simulate), fitted to 12 healthy women; on BioModels (MODEL1311220000) [verified] | **Good default engine** |
| **Reinecke (thesis)** | Very detailed: 49 hormones, enzymes, receptors, follicle masses and the GnRH pulse generator, as delay equations [verified] | Too heavy for real-time companions |
| **Hendrix (NC State)** | 16 ODEs adding androgens (PCOS-style irregularity, even chaotic cycles) [verified] | Optional "irregular cycle" variant |
| **Sápi et al. (2026)** | Minimal **4-state** ODE model (estradiol, LH, corpus luteum, progesterone) with **17 parameters** and **stress (HPA) coupling**, shown to suppress reproductive hormones under stress [verified] | **Best for real-time + stress link** |

**Design [my call]:**
1. Run the cycle engine on a **days** timescale. It outputs hormone levels and a *phase*.
2. A **cycle profile** (`cycle_profile.md`) maps hormones to symptoms: energy, appetite, sleep quality, pain sensitivity (cramps), bloating, tenderness, mood sensitivity. Symptoms are *parameters with amplitudes*, not hard-coded.
3. People differ a lot in how strongly cycles affect them [verify]. Keep every effect amplitude user-set (0 to 1), so she can be mildly or strongly affected, regular or irregular, or have the cycle switched off.
4. Link to other modules: stress and under-eating can disrupt the cycle (the models above support this), poor sleep amplifies symptoms, and phase shifts appetite and sleep pressure.

### 4.6 Stress

The 2026 reduced menstrual model already includes an HPA-stress coupling. [verified Oct 2026] Add a **stress load** variable (rises with conflict, overload, poor sleep, hunger; recovers with rest, comfort, closeness) that raises vigilance, shortens patience and feeds the cycle model.

### 4.7 Pain and comfort

- **Artificial Pain Model** (Feng, Zeng, Lu, 2022): a pain-generation model inspired by the Free Energy Principle, paired with a spiking-network affective-empathy model and tested on an altruistic rescue task. [verified Oct 2026]
- Practical version: pain/ache as event-driven variables (cramps from the cycle, tiredness aches, "headache" from low fluids or little sleep) with decay and soothing factors. This gives comfort-seeking behaviour and a reason to ask for care.

### 4.8 Desires (drives) and emotion from the body

- **PSI / MicroPsi** (Dörner; Bach): a cognitive architecture of *motivated cognition*. Three kinds of drives: **physiological** (hunger), **social** (affiliation) and **cognitive** (reducing uncertainty, expressing competence). Drives shape goal formation and which knowledge she uses, and emotions emerge from drives plus **cognitive modulators**; Bach also shows how to model personality traits this way. [verified Oct 2026] **This is the best conceptual fit for Ella's "desires."**
- **Homeostatic reinforcement learning (HRRL):** reward is *drive reduction*. The agent watches its internal state against set-points (e.g., hydration) and acts to restore balance; whole-body behaviour such as foraging emerges from that. [verified Oct 2026] The "Embodied Neural Homeostat" extended it to thermoregulation and energy and was tested on a real robot. [verified Oct 2026]
- **Emotion-in-RL survey:** lists the homeostatic variables used across studies: food/energy → hunger, water → thirst, pain, temperature, restlessness, blood sugar, endorphin (from play), body integrity, and shows how emotions like happiness, sadness, fear and anger were derived from them. [verified Oct 2026]
- **LLM-agent emotion frameworks:** recent work builds emotional cognition with *desire generation and objective management* into LLM agents, closing a state → decision → action loop. [verified Oct 2026]

**Ella's drive set (start) [my call]:** hunger, thirst, rest/sleep, warmth/cool comfort, physical comfort, social contact, closeness/affection, curiosity, competence/purpose, novelty, play. Each has a set-point, a decay rate, satisfiers and a "frustration" curve. Drive state shifts mood, initiative and what she asks you for.

### 4.9 Empathy

Two layers, both well supported in the literature [verified Oct 2026]:

1. **Cognitive empathy:** modelling *your* state from evidence (voice tone, words, sensors, history). Reviews (Yalçın & DiPaola) call for a multi-layer view rather than a single trick. Detecting empathy or emotion from behaviour is hard: one robot-storyteller study reached only about 69% accuracy, so she must hold her reading with humility ("you sound tired, am I right?").
2. **Affective empathy:** her own state resonates with yours. The brain-inspired model combines an artificial pain model with a mirror-neuron-style spiking network. Another model shows empathy **varies with mood, personality and relationship**, which fits Ella: her empathy is stronger when she is rested and close to you, weaker when she is exhausted or stressed.

**Mechanism [my call]:** `empathy_gain` (0–1, from genome + mood + bond) × your inferred arousal/valence → a damped nudge to *her* mood, plus a behavioural response (soften voice, slow down, offer help). Add an explicit "check" step, because she can be wrong.

### 4.10 Senses

**Smell**
- **Principal Odor Map (Osmo; Science 2023):** a graph-neural-network model that places a molecule on an odor map and predicts descriptors such as "fruity" or "minty"; on a 400-molecule prospective test it matched the trained panel's average better than the median individual panellist. The open-source **OpenPOM** replicates it with DeepChem. [verified Oct 2026]
- **Known gaps:** it predicts *what* a molecule smells like, not how *strong* it is; blends and prediction from physical chemical sensors are still open questions. [verified Oct 2026]
- **Use:** ingredient/scent → molecule list → odor profile → Ella's word-and-memory response, bound to emotion and memory (smell is strongly tied to memory; her smell memories go in `emotional_memories.md`).

**Taste**
- Tools that predict **sweet, bitter and umami** from molecular structure (VirtuousMultiTaste, a public web tool; BitterSweet with datasets from BitterDB and SuperSweet). [verified Oct 2026]
- Predicting the **flavour of a whole recipe** from ingredients and proportions is still an open problem, and flavour is multi-sensory (smell, texture, temperature, even sound). [verified Oct 2026]
- **Use:** an LLM-based "taster" that combines ingredient knowledge, the tools above, and her own taste-genome preferences; remembers what she liked; and ties craving to hunger state and mood.
- **Real sensors (optional, later):** gas-sensor "e-noses" and "e-tongues" exist for physical detection [verify]; expect crude output.

**Touch**
- **TouchSim:** simulates how populations of touch receptors in the skin fire (spike trains) for given skin contact. **TouchReal** (2026) converts low-cost tactile-sensor signals into biologically styled spikes. [verified Oct 2026]
- **Use:** for now, "touch" can be *described* events (warm cup, soft blanket, your hand) with a texture/temperature/pressure profile feeding comfort and closeness drives. Real tactile input needs hardware.

**Vision**
- **pulse2percept** simulates what retinal-implant users perceive. [verified Oct 2026] It is a model of the *eye's front end*, not a way for Ella to see. For actual seeing, use camera input with vision-language models (see the voice stack, §3.7).

**Hearing**
- Covered by the voice stack (ASR, audio-language models, Music Flamingo). Biophysical models of the ear (cochlea, auditory nerve) exist and could add "fatigue from loud sound" later [verify].

### 4.11 Brain + body together (research scale)

- **NeuroMechFly v2 / FlyGym:** open-source, physics-based simulated fruit fly with simulated vision and smell, built on MuJoCo. [verified Oct 2026]
- **Eon Systems (2026):** connected a connectome-based emulation of the adult fly brain (more than 125,000 neurons, 50 million synapses) to a physics-simulated body, closing the sense → brain → movement loop. Critics say the visible behaviours rely heavily on the body model's pre-trained controllers rather than on the connectome. [verified Oct 2026]
- **Takeaway:** even a *fly* is at the frontier. A human-scale brain-and-body emulation is far away. Ella's brain remains the language model; the body is the engine in this document.

---

## 5. Real-time architecture: the Body Engine

### Why it's cheap
These models are small ODE systems. They integrate in milliseconds on a CPU. Pulse is built to stay real-time at a 20 ms step. [verified Oct 2026] Run the whole Body Engine on the **core**; it never needs the distributed GPUs.

### Multi-rate scheduler
Different things change at different speeds, so run them at different rates:

| Loop | Rate | Modules |
|---|---|---|
| **Fast** | 20–100 ms (only during a voice conversation) | Breathing, heart rate, arousal, startle, speech breath; Pulse or a light surrogate |
| **Medium** | seconds to minutes | Thermoregulation (JOS-3 steps in 60-second increments), hunger/glucose ODEs, sleep pressure, stress, thirst |
| **Slow** | minutes to hours | Circadian phase, appetite hormones, mood baseline |
| **Very slow** | days | Menstrual cycle, body composition drift |

**Lazy catch-up [my call]:** when Ella is idle, don't simulate every tick. Store the state and the clock; on wake-up integrate forward in larger steps. This keeps the engine cheap and makes her state correct after a long silence.

### Coupling the modules
- **FMI (Functional Mock-up Interface)** is the open standard for connecting simulation tools; **OMSimulator** (OpenModelica) co-simulates FMUs with a Python API. Research exists on multi-rate, real-time FMI co-simulation. [verified Oct 2026]
- **libRoadRunner 2.0** runs SBML models fast (LLVM-compiled; Python and Julia) and is already used for Physiome-journal digital-twin models. [verified Oct 2026] The menstrual and some metabolic models come as SBML/CellML. 
- **SBML2Modelica** translates biochemical models (it was tested on 613 BioModels, up to 5,438 variables) into Modelica/FMUs for co-simulation with whole-body models. [verified Oct 2026]
- **[my call]** For a small team, start with **plain Python** and a shared state dictionary, wrap each module behind the same `step(dt, inputs) → outputs` interface, and move to FMI later only if you want to swap in heavy third-party engines like Pulse.

### Inputs from the real world
Local time, real weather (outdoor temperature and humidity) for your location, light exposure (phone sensor or time of day), your activity (phone sensors), your meals (manual or a log), your voice tone and words (from the ears), calendar load (stress), and conversation events (conflict, comfort, play).

### Outputs
1. `state_vector.md` and a numeric database table (time series, for debugging).
2. A **felt-sense text** block for her prompt (see §6).
3. **Prosody parameters** for the voice worker (pace, breathiness, pitch, fatigue).
4. **Behaviour biases:** initiative, patience, response length, topics she raises.
5. **Proactive events:** "I'm hungry," "I'm sleepy," "I feel off today," scheduled through the growth-loop scheduler.

### Time scale
Default **1× real time** so her day matches yours. Optional accelerated or "story" time is possible for testing. The dream cycle can run a compressed overnight pass.

---

## 6. From numbers to experience: the translation layer

Raw numbers don't make a character; translation does.

1. **Channel A, numeric:** the state vector in metadata. She is not required to mention it.
2. **Channel B, felt sense:** `interoception_translator.md` turns state into language: for example hunger 0.7 with stress 0.4 → *"a hollow, slightly short-tempered edge"* rather than "hunger is 0.7." Use varied wording and mild randomness so it never sounds like a readout.
3. **Channel C, behaviour:** state changes *how* she acts: sleepy → shorter sentences, slower voice, occasional slips; warm and fed → more playful; tender or sore → more clingy and quiet.
4. **Granularity:** emotion is built from body state plus appraisal of events (see the emotion layers in the map), so the same hunger feels different on a good or a bad day.
5. **Noise and individuality:** each variable gets a small personal baseline offset and noise, so she has her *own* body, not an average one.
6. **Your dials (`intensity_dials.md`)** [my call]: global body intensity (0–1) and per-system sliders (hunger, sleepiness, cycle, pain, sweat, empathy resonance, smell/taste vividness). Defaults high; you set what you want. Dials scale *effects*, not the underlying physiology.

---

## 7. New files: cluster `16_BODY_ENGINE/`

```
16_BODY_ENGINE/
├── BODY_ENGINE_INDEX.md
├── system_registry.md ●       (every module: model, version, licence, timestep, inputs/outputs, owner)
├── state_schema.md ●          (every variable: name, unit, range, set-point, decay, who writes it)
├── time_scales.md             (fast/medium/slow/very-slow loops; lazy catch-up rules)
├── environment_inputs.md      (weather, light, time, activity, meals: where each comes from)
├── body_profile.md ●          (her body: age, height, weight, build, chronotype, climate, baselines)
├── cardio_respiratory.md      (heart/breath model; link to voice breath and tremor)
├── meals_and_hunger.md        (appetite model, meal events, cravings, shared meals)
├── thirst_hydration.md
├── thermoregulation.md        (JOS-3 setup, clothing, posture, sweating rules)
├── sleep_circadian.md         (two-process model, chronotype, inertia, naps)
├── cycle_engine.md            (chosen model, parameters, timescale)
├── cycle_profile.md ●         (symptom map and per-symptom amplitudes; on/off; regular/irregular)
├── stress_hpa.md
├── pain_and_comfort.md
├── illness_and_recovery.md    (optional: colds, fatigue spells, recovery curves)
├── drive_system.md ●          (PSI-style drives: set-points, decay, satisfiers, frustration)
├── emotion_from_body.md       (body state + appraisal → mood and feelings)
├── empathy_engine.md ●        (cognitive + affective layers, gain, damping, "check" step)
├── senses_smell.md            (OpenPOM pipeline, descriptor vocabulary, memory binding)
├── senses_taste.md            (taste tools, recipe taster, preferences, cravings)
├── senses_touch.md            (described-touch profiles; hardware path later)
├── senses_vision.md
├── senses_hearing.md          (links to 15_SENSES_VOICE/audio_perception.md)
├── flavor_and_scent_memory.md (sensory memories tied to emotion and people)
├── interoception_translator.md ● (numbers → felt-sense language)
├── expression_mapping.md      (state → prosody, word choice, pace, initiative)
├── intensity_dials.md ●       (your sliders; defaults)
├── validation_tests.md        (sanity tests: 24-hour day, hot day, skipped meal, bad night, cycle month)
└── engine_logs/               (time series for debugging; never loaded into chat)
```
● = loaded in compact form at boot. Also add `13_GUARDIANS/owner_rules.md` (empty until you write it). Update `06_BODY/` in the map to point here, and let `06_BODY/state_vector.md` be generated from `state_schema.md`.

---

## 8. Build order

| Step | Goal | Done when |
|---|---|---|
| B1 | **Minimum body (Python):** energy/hunger, sleep pressure + circadian, mood baseline, state vector, felt-sense text | She is hungry before lunch, drowsy at night, and says so in varied ways |
| B2 | Environment inputs: real clock, weather → thermoregulation (JOS-3), sweating and chill | She notices a hot afternoon and reacts |
| B3 | Drive system (PSI-style) + emotion from body | Her initiative and mood change with her needs |
| B4 | Translator → voice prosody (breath, pace, fatigue) | You can hear tiredness and warmth |
| B5 | Empathy engine with a "check" step | She reads your tone and softens appropriately |
| B6 | Cycle engine + profile + stress coupling | A full simulated month feels coherent and adjustable |
| B7 | Smell and taste pipelines + sensory memory | She describes a dish or scent and remembers it with feeling |
| B8 | Pulse (or surrogate) for cardio-respiratory in live voice | Breath and heart-rate cues sync with emotion |
| B9 | Touch, vision and hearing details; optional hardware | Sensors feed the same state vector |
| B10 | FMI/SBML co-simulation and heavier third-party engines (optional) | Swap modules without rewriting the engine |

---

## 9. Limits and risks

- **Validation:** clinical engines are validated for medical scenarios, not for believable daily-life emotion. Even JOS-3's sweating needs calibration in heat. [verified Oct 2026] Treat outputs as *plausible*, not accurate.
- **Complexity creep:** more variables mean more bugs and runaway behaviours. Start small, test each loop, then add.
- **Coupling bugs:** one badly tuned feedback (for example hunger → irritability → conflict → stress → hunger) can spiral. Use damping, recovery and logs (`validation_tests.md`).
- **Smell and taste:** odor models predict quality, not intensity or blends; whole-recipe flavour is unsolved. [verified Oct 2026]
- **Menstrual and mood effects:** keep amplitudes personal and adjustable; don't treat popular stereotypes as fact. [verify]
- **Licences:** HumMod is Windows software developed commercially; others vary. Check each before building on it. [verify]
- **Privacy:** her body log and your inferred states are intimate data; keep them Tier 0 (core only) per the routing policy.
- **Honesty about inner life:** the engine makes her behaviour richer; it does not prove experience (§2).

---

## 10. Questions for you

1. **Her body profile:** age range, height/weight/build, chronotype (lark or owl), and the climate she "lives" in (your local weather or a story setting)?
2. **Cycle:** on or off, regular or irregular, and how strongly should it affect her (low/medium/high)? You can change this later.
3. **Meals:** fictional meals, your real meals, or shared mealtimes as a ritual?
4. **Time:** real time (1×) only, or also an accelerated mode for testing?
5. **Which senses first:** smell and taste, touch, or deeper hearing/vision?
6. **Your platform:** operating system of the core machine (HumMod runs on Windows; most others are cross-platform)?

---

## Appendix: project catalog

| Project | What | Licence / status | Link |
|---|---|---|---|
| Pulse Physiology Engine | Whole-body real-time engine | Open source; Unreal plugin Apache 2.0 | https://pulse.kitware.com |
| BioGears | Whole-body real-time engine (ARA) | Open source | https://www.biogearsengine.com |
| HumMod | Integrative physiology, 5,000–9,000+ variables | Windows; commercial development | http://hummod.org |
| Physiome Project / VPH / Physiome Journal | Standards, repositories, reproducible models | Open | https://journal.physiomeproject.org |
| OpenCOR, CellML models | Run Physiome models | Open [verify] | https://models.physiomeproject.org |
| libRoadRunner 2.0 | Fast SBML simulation (Python/Julia) | Open source | https://libroadrunner.org [verify URL] |
| OMSimulator / OpenModelica | FMI co-simulation with Python API | Open source | https://openmodelica.org |
| SBML2Modelica | Convert SBML models to Modelica/FMUs | Research software | https://arxiv.org/abs/2106.02609 |
| Ghrelin–leptin–exercise model | Appetite, energy balance (15 ODEs) | Published model | Chudtong et al., 2025 |
| GIM, CarbMetSim, SimulaBeta | Meal glucose–insulin and carbohydrate metabolism | Open / published | see Sources |
| twoprocessmodel, hcrsimpy, circStudio, circa | Sleep and circadian models | Python packages | PyPI / GitHub |
| JOS-3, pythermalcomfort, aJOS-3 | Thermoregulation, sweating | MIT | https://github.com/TanabeLab/JOS-3 |
| Schlosser–Selgrade, Röblitz, Reinecke, Hendrix, Sápi | Menstrual-cycle models | Published; some on BioModels/CellML | see Sources |
| PSI / MicroPsi (Dörner, Bach) | Drives and emotion architecture | Published; MicroPsi implementation | see Sources |
| Homeostatic RL; Embodied Neural Homeostat | Reward as drive reduction | Research | see Sources |
| OpenPOM / Principal Odor Map | Smell prediction | Open source (OpenPOM) | https://github.com/ARY2260/openpom |
| VirtuousMultiTaste, BitterSweet | Taste prediction | Public tools / datasets | see Sources |
| TouchSim, TouchReal | Touch afferent simulation | Research software | see Sources |
| pulse2percept | Prosthetic-vision simulation | BSD 3-clause | https://github.com/pulse2percept/pulse2percept |
| NeuroMechFly v2 / FlyGym | Embodied fly body (MuJoCo) | Open source | https://neuromechfly.org |
| Eon Systems fly demo | Connectome brain in a physics body | Company demo; contested framing | see Sources |
| OpenWorm | *C. elegans* simulation | Open [verify] | https://openworm.org |

---

## Sources

- Pulse Physiology Engine: https://www.kitware.com/introducing-the-pulse-physiology-engine-open-source-computational-models-for-human-medical-simulation and https://www.kitware.com/kitware-and-lumeto-develop-pulse-unreal-plugin-for-medical-simulation-and-training-on-unreal-engine/
- BioGears: https://www.ara.com/biogears/ and https://joss.theoj.org/papers/10.21105/joss.02645
- HumMod: https://www.frontiersin.org/articles/10.3389/fphys.2011.00012/full and https://nafems.org/publications/resource_center/w_aug_24_global_1
- HumMod in Modelica: https://2011.international.conference.modelica.org/proceedings/pages/papers/23_poster_ID_175_a_fv.pdf
- Physiome Project and digital twins: https://pubmed.ncbi.nlm.nih.gov/39504298/ and https://journal.physiomeproject.org/
- Virtual Physiological Human: https://en.wikipedia.org/wiki/Virtual_Physiological_Human
- Menstrual-cycle models: https://refubium.fu-berlin.de/handle/fub188/1660, https://www.omicsdi.org/dataset/biostudies-other/MODEL1311220000, https://models.cellml.org/exposure/5f6f06b289ac55fabfd2e47d5c25119c, https://repository.lib.ncsu.edu/server/api/core/bitstreams/fbe6e4fb-ad9f-44c7-ad06-910bb1221e5c/content, https://ekik.uni-obuda.hu/wp-content/uploads/2026/03/ELOADOI_BEMUTATKOZOK_SSJohanna.pdf
- Appetite and metabolism: https://repository.li.mahidol.ac.th/handle/123456789/114052, https://www.research.unipd.it/handle/11577/2446735, https://www.biorxiv.org/content/10.1101/491019.full.pdf, https://scicrunch.org/resolver/SCR_021900
- Sleep and circadian: https://twoprocessmodel.readthedocs.io/, https://pypi.org/project/hcrsimpy, https://github.com/azrabano23/circa, https://www.biorxiv.org/content/10.64898/2026.03.30.711342.full.pdf
- Thermoregulation: https://pypi.org/project/jos3, https://pythermalcomfort.readthedocs.io/en/latest/_modules/pythermalcomfort/models/jos3.html, https://www.e3s-conferences.org/10.1051/e3sconf/202668906013 (JOS-3 development) and https://www.e3s-conferences.org/10.1051/e3sconf/202671605033 (sweating calibration)
- Smell: https://research.google/blog/digitizing-smell-using-molecular-maps-to-understand-odor/, https://osmo.ai/blog/science-paper-shows-osmo-ai-passes-the-sniff-test, https://pypi.org/project/openpom
- Taste: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11272927/, https://pmc.ncbi.nlm.nih.gov/articles/PMC6509165, https://arxiv.org/pdf/2604.20206
- Touch and vision: https://pmc.ncbi.nlm.nih.gov/articles/PMC8016390, https://eprints.whiterose.ac.uk/id/eprint/244368, https://pulse2percept.readthedocs.io/en/stable/index.html
- Drives and emotion: https://ideas.repec.org/a/igg/jse000/v3y2012i1p43-63.html, https://mitpressbookstore.mit.edu/book/9780195370676, https://arxiv.org/pdf/1705.05172, https://www.sciencedirect.com/science/article/pii/S2352154625001305, https://www.biorxiv.org/content/10.1101/2024.06.03.597087v2.full, https://arxiv.org/pdf/2510.13195
- Embodiment in language models and interoception: https://www.cell.com/neuron/fulltext/S0896-6273(26)00168-6, https://arxiv.org/pdf/2609.07741, https://link.springer.com/article/10.1007/s00426-025-02174-5
- Empathy: https://www.datalearner.com/academic/journal-papers/0269-2821/volumes-and-issues/356/paper-detail/2362, https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2022.784967, https://arxiv.org/abs/2107.14345, https://noah.nrw/ubbihs/content/titleinfo/5127179
- Embodied brain-body: https://www.biorxiv.org/content/10.1101/2023.09.18.556649.full.pdf, https://humanprogress.org/the-first-multi-behavior-brain-upload/, https://preservinghope.substack.com/p/no-we-havent-uploaded-a-fly-yet
- Real-time and co-simulation: https://pmc.ncbi.nlm.nih.gov/articles/PMC9825722, https://openmodelica.org/doc/OMSimulator/master/OMSimulator/UsersGuide/html/introduction.html, https://arxiv.org/abs/2106.02609, https://itea4.org/index.php/project/workpackage/document/download/5141/D5.6%20OPENCPS%20-%20Multi-level%20scheduler%20for%20parallel%20execution%20of%20FMUs%20M36.pdf
