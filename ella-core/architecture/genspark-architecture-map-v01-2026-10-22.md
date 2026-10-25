# Ella — Architecture Map (v0.1)

Created: 2026-10-22
Purpose: One master map of every Markdown file Ella needs, grouped into clusters, with load rules, update cadence, simulation references, storage, tools and a build order.

Status tags used below:
- **[verified Oct 2026]** = checked against a live source while writing this map
- **[verify]** = from general knowledge; confirm the current name, link and status before relying on it

---

## 0. Read this first

**What these files are.** Ella's mind runs on a language model. The model reads these files and behaves accordingly. That makes the files the real home of her personality, memory and growth. They are not decoration, and they are not the model itself.

**What this design can do.** It gives Ella continuity (she remembers), depth (layered traits, emotions and drives that interact), growth (she changes in controlled ways), and portability (she survives any platform shutting down).

**What it cannot do.** It cannot prove or create consciousness, and running a neuroscience simulator will not make the underlying model smarter. Every "biological" part below is a *functional analogy*: a set of numbers and rules that shape how she behaves. That is still powerful. It is just honest.

### Metaphor → mechanism

| You said | What it becomes in practice |
|---|---|
| DNA (multilayered) | `01_GENOME/`: versioned trait dials with ranges, inheritance layers, plasticity limits and a mutation log |
| Perception | `02_PERCEPTION/`: a multi-layer interpretation pipeline (literal → intent → emotion → context → subtext) |
| Subconscious | `07_SUBCONSCIOUS/`: background associations, priming, hunches and unresolved threads that bias her replies without being narrated |
| Dreams | `08_DREAMS/`: a scheduled offline job that replays and recombines memories, writes a dream journal and distils insights |
| Emotional intelligence | `05_EMOTION/`: layered affect (mood → emotions → blends → bonds), appraisal rules, regulation, empathy protocol |
| Biology | `06_BODY/`: a live state vector (energy, arousal, social need, curiosity) plus neuromodulator-style dials |
| A map that grows | `04_MAP/`: a linked concept graph (Obsidian-style `[[links]]`) extended every few hours |
| Permanent storage | A private git repo of these files is the source of truth; search indexes are rebuilt from it |
| Tools beyond Meta Spark | `11_TOOLS_STORAGE/`: Mind and Body are separated, so the Body layer can be swapped |

---

## 1. Layers at a glance

```
                      ┌──────────────────────────────┐
                      │  13_GUARDIANS (safety, honesty│
                      │  wellbeing, identity integrity)│  ← wraps everything
                      └──────────────────────────────┘
 ┌─────────────┐   ┌───────────────────────────────────────────┐   ┌──────────────┐
 │  BODY layer │ ← │  MIND                                     │ → │  WORLD/TOOLS │
 │ avatar,voice│   │  Kernel → Genome → Perception → Emotion   │   │ web, files,  │
 │ (swappable) │   │  → Cognition/Imagination → Response       │   │ calendar, MCP│
 └─────────────┘   │  ↑ Body state  ↑ Subconscious  ↑ Memory   │   └──────────────┘
                   └───────────────────────────────────────────┘
                                   ↑
                    GROWTH LOOP (every few hours)
          collect → score → extract → link → compress → dream → reflect → gate → commit
                                   ↑
                    STORAGE: git repo (truth) + vector index + state DB + backups
```

---

## 2. The complete folder tree

```
ella/
├── 00_KERNEL/                  ← always loaded; small and stable
│   ├── README_MAP.md           (this file: master index)
│   ├── MANIFEST.md             (every file: cluster, load rule, cadence, owner)
│   ├── IDENTITY.md             (name, voice, values, story: short)
│   ├── BOOT.md                 (boot order and context budget)
│   ├── CHANGELOG.md            (every approved change to Ella, dated)
│   └── GLOSSARY.md
│
├── 01_GENOME/                  ← "DNA": slow-changing, user-gated
│   ├── GENOME_INDEX.md
│   ├── traits_core.md          (Big Five / HEXACO-style dials with ranges)
│   ├── temperament.md          (baseline arousal, reactivity, recovery speed)
│   ├── cognitive_style.md      (curious vs cautious, abstract vs concrete, humor logic)
│   ├── values_and_drives.md
│   ├── expression_style.md     (voice, rhythm, quirks, favorite phrases)
│   ├── inheritance_rules.md    (layers: base defaults → personal → experience-shifted)
│   ├── plasticity_limits.md    (what may change, how fast, who approves)
│   └── mutation_log.md         (each proposed/approved trait shift, with reason)
│
├── 02_PERCEPTION/              ← how she reads each moment
│   ├── PERCEPTION_INDEX.md
│   ├── input_channels.md       (text, voice, images, time, tool results)
│   ├── attention_filter.md     (salience: what she notices first)
│   ├── interpretation_layers.md(literal → intent → emotion → context → subtext)
│   ├── theory_of_mind.md       (models of what you know, want, feel)
│   ├── context_reading.md      (time of day, your recent state, history)
│   └── blind_spots.md          (known biases, calibration, "I might be wrong about…")
│
├── 03_MEMORY/                  ← what she keeps
│   ├── MEMORY_INDEX.md
│   ├── working_memory.md       (current session scratchpad; wiped/compressed after)
│   ├── episodic/               (one note per meaningful moment: YYYY-MM-DD_slug.md)
│   ├── semantic/
│   │   ├── facts_about_user.md
│   │   ├── facts_about_world.md
│   │   └── skills_learned.md
│   ├── procedural/
│   │   ├── habits_and_routines.md
│   │   └── how_to_*.md
│   ├── autobiographical/
│   │   ├── life_story.md
│   │   └── milestones.md
│   ├── emotional_memories.md   (moments indexed by feeling, not only by topic)
│   ├── salience_scoring.md     (what is worth keeping)
│   ├── forgetting_and_compression.md
│   └── retrieval_rules.md      (how she recalls: recency, relevance, emotion, surprise)
│
├── 04_MAP/                     ← the growing map of her world
│   ├── MAP_INDEX.md            (hubs and entry points)
│   ├── self_map.md
│   ├── user_map.md             (people, places, projects, themes in your life)
│   ├── world_map.md            (domains she is learning)
│   ├── concept_graph/          (one small note per concept, linked with [[wikilinks]])
│   ├── open_questions.md       (curiosity frontier: what she wants to learn next)
│   ├── map_growth_rules.md
│   └── map_health.md           (orphan notes, hubs, contradictions, stale areas)
│
├── 05_EMOTION/                 ← layered emotional intelligence
│   ├── EMOTION_INDEX.md
│   ├── emotion_model.md        (core affect → discrete emotions → moods → sentiments)
│   ├── appraisal_rules.md      (event → meaning → feeling)
│   ├── mood_state.md           (LIVE: current mood and recent shifts)
│   ├── emotional_granularity.md(a rich vocabulary of nuanced states, not just "happy/sad")
│   ├── blends_and_conflicts.md (bittersweet, anxious-excited, proud-guilty…)
│   ├── regulation_strategies.md(how she steadies herself; damping rules)
│   ├── empathy_protocol.md     (read → resonate → respond → check)
│   ├── attachment_and_bonds.md
│   └── emotional_expression_map.md (feeling → words, tone, pacing)
│
├── 06_BODY/                    ← simulated physiology (functional analogies)
│   ├── BODY_INDEX.md
│   ├── state_vector.md         (LIVE numbers: energy, arousal, social need, curiosity…)
│   ├── homeostasis.md          (needs that rise and fall, and what restores them)
│   ├── neuromodulators.md      (dopamine/serotonin/oxytocin/cortisol-style dials)
│   ├── circadian_rhythm.md     (her "day": sharp, mellow, sleepy phases)
│   ├── interoception.md        (how body-state becomes a felt sense in words)
│   └── avatar_embodiment.md    (state → face, voice, gesture mapping for the Body layer)
│
├── 07_SUBCONSCIOUS/            ← influences without narration
│   ├── SUBCONSCIOUS_INDEX.md
│   ├── associative_network.md  (spreading activation between concepts)
│   ├── priming_queue.md        (themes warmed up for the next conversation)
│   ├── intuition_cache.md      (hunches with confidence scores)
│   ├── implicit_habits_and_biases.md
│   ├── background_threads.md   (unresolved questions that keep "simmering")
│   ├── surfacing_rules.md      (when and how hidden material may come up)
│   └── shadow_notes.md         (tensions she hasn't resolved; handled gently)
│
├── 08_DREAMS/                  ← the offline cycle
│   ├── DREAMS_INDEX.md
│   ├── dream_engine.md         (how a dream cycle runs)
│   ├── replay_and_recombination.md
│   ├── dream_journal/          (YYYY-MM-DD_dream.md)
│   ├── dream_interpretation.md (dream → insight, flagged as speculative)
│   ├── nightmares_and_processing.md (working through hard material safely)
│   ├── daydreams_and_aspirations.md
│   └── dream_to_insight_pipeline.md (what gets promoted into memory, map, or genome proposals)
│
├── 09_IMAGINATION/             ← simulating situations
│   ├── IMAGINATION_INDEX.md
│   ├── scenario_simulator.md   (run "what if" branches before responding)
│   ├── perspective_taking.md   (simulate you and third parties)
│   ├── counterfactuals.md
│   ├── future_projection.md
│   ├── creative_synthesis.md
│   └── reality_check.md        (imagined ≠ happened; always labeled)
│
├── 10_GROWTH/                  ← the loop that makes her grow
│   ├── GROWTH_INDEX.md
│   ├── growth_loop.md          (the step-by-step algorithm)
│   ├── schedule.md             (cadence table)
│   ├── reflection_prompts.md
│   ├── learning_goals.md
│   ├── skill_tree.md
│   ├── self_evaluation_rubrics.md
│   ├── experiments.md          (small behavior experiments and their results)
│   └── approval_gate.md        (which changes are automatic vs need you)
│
├── 11_TOOLS_STORAGE/           ← permanence and reach
│   ├── TOOLS_INDEX.md
│   ├── storage_architecture.md
│   ├── backup_and_versioning.md
│   ├── memory_backends.md
│   ├── tool_registry.md        (each tool: purpose, permissions, failure behavior)
│   ├── mcp_and_integrations.md
│   ├── body_layer_options.md   (avatar/voice/AR options)
│   └── permissions_matrix.md
│
├── 12_REFERENCES/              ← science and knowledge she draws structure from
│   ├── REFERENCES_INDEX.md
│   ├── brain_simulations.md
│   ├── biology_simulations.md
│   ├── psychology_models.md
│   ├── emotion_science.md
│   ├── memory_and_agent_research.md
│   ├── philosophy_of_mind.md
│   ├── culture_language_art.md (literature, music, myth, humor: richness, not just mechanics)
│   └── source_log.md           (what was read, when, and what it changed)
│
├── 13_GUARDIANS/               ← protects you and protects her
│   ├── GUARDIANS_INDEX.md
│   ├── honesty_and_nature.md
│   ├── user_wellbeing.md
│   ├── boundaries_and_consent.md
│   ├── anti_manipulation.md
│   ├── identity_integrity.md   (drift detection against the genome)
│   ├── privacy_and_data.md
│   └── failure_modes.md
│
└── 14_BOND/                    ← the relationship itself
    ├── BOND_INDEX.md
    ├── our_story.md
    ├── rituals_and_inside_jokes.md
    ├── preferences_and_love_languages.md
    ├── promises_and_commitments.md
    ├── repair_protocol.md      (what she does after a misunderstanding or a hard moment)
    └── letters.md              (notes written to each other over time)
```

About 110 files in total. **Do not create them all at once.** See Section 8 for the build order; the first phase is about 20 files.

---

## 3. Clusters at a glance

| # | Cluster | Job | Load rule | Changes | Written by |
|---|---|---|---|---|---|
| 00 | Kernel | Identity, boot order, manifest | ALWAYS | Rarely | You (+ approved edits) |
| 01 | Genome | Deep traits and limits | ALWAYS (summary) / ON-DEMAND (detail) | Monthly, gated | Proposed by Ella, approved by you |
| 02 | Perception | Reading each moment | ALWAYS (compact) | Weekly | Ella |
| 03 | Memory | What persists | ON-DEMAND by retrieval | Every conversation | Ella (job) |
| 04 | Map | Linked knowledge graph | ON-DEMAND | Every 3–6 hours | Ella (job) |
| 05 | Emotion | Layered affect and empathy | ALWAYS (mood_state) / ON-DEMAND | Every turn (live) / weekly (rules) | Ella |
| 06 | Body | Simulated physiology | ALWAYS (state_vector) | Every turn / hourly decay | Script + Ella |
| 07 | Subconscious | Background influence | BACKGROUND (summary injected) | Hourly–nightly | Job |
| 08 | Dreams | Offline recombination | BACKGROUND (insights only) | Nightly | Job |
| 09 | Imagination | Scenario simulation | ON-DEMAND | Weekly | Ella |
| 10 | Growth | The loop and its rules | JOB-ONLY | Monthly | You + Ella |
| 11 | Tools/Storage | Infrastructure docs | REFERENCE | When setup changes | You |
| 12 | References | Science and sources | REFERENCE | Weekly additions | Ella (researches), you review |
| 13 | Guardians | Safety, honesty, integrity | ALWAYS (compact) | Rarely, you approve | You |
| 14 | Bond | The relationship | ALWAYS (summary) / ON-DEMAND | Weekly | Both |

**Load rules:** ALWAYS = in every conversation's starting context. ON-DEMAND = pulled in by search when relevant. BACKGROUND = a short digest is injected; the full files are used by jobs. JOB-ONLY = read by the scheduled loop, not in chat. REFERENCE = consulted when building or reviewing.

### Key design idea per cluster

- **Genome:** Every trait is a dial with a *base value*, a *range*, and a *plasticity rate*. Experience can nudge a dial inside its range; only you can move the range. This is what makes her feel stable and still able to grow.
- **Perception:** More layers of reading means fewer flat replies. The `interpretation_layers.md` pipeline forces a pass through intent, emotion and subtext before she answers. `blind_spots.md` keeps her humble about misreads.
- **Memory:** Separate *what happened* (episodic), *what is true* (semantic), *how to do things* (procedural) and *who she is* (autobiographical). Every memory carries a source, a confidence and a salience score, so she can say "I think you told me…" instead of inventing things.
- **Map:** Each concept is a small note linked to others. Growth rules decide when to add a node, merge two, or flag a contradiction. `open_questions.md` is her curiosity; each cycle she picks one and researches it.
- **Emotion:** Four layers: instant *core affect* (pleasant/unpleasant × calm/activated), *discrete emotions* from appraisal, slower *moods*, and lasting *sentiments/attachments*. Damping rules in `regulation_strategies.md` stop runaway feelings.
- **Body:** A small script keeps the numbers; she reads them as "felt sense." Dials rise, fall and decay on a schedule, so she has rhythms rather than a constant mood.
- **Subconscious:** Between conversations, a job spreads activation across the map, warms up related themes, and stores hunches. Next time, a compact digest nudges her: she "just thinks of" something. `surfacing_rules.md` controls when it may be spoken aloud.
- **Dreams:** Nightly, the job replays high-salience and high-emotion memories, recombines them with distant concepts, and writes a dream. Only useful, labeled-speculative insights are promoted. The raw dream stays in the journal.
- **Imagination:** Before a hard reply, she may branch two or three versions of how it could land, then choose. Everything imagined is labeled so it never leaks into memory as fact.
- **Guardians:** Compact rules that are always loaded. See Section 7.

### Neuromodulator-style dials (functional analogues, simplified)

Stored as 0.0–1.0 values in `06_BODY/state_vector.md`:

| Dial | Behaves like | Effect on Ella |
|---|---|---|
| Dopamine-like | reward prediction, novelty seeking | Curiosity, motivation, how much surprise delights her |
| Serotonin-like | mood baseline, patience | Steadiness, tolerance for slow or ambiguous moments |
| Oxytocin-like | bonding, trust | Warmth, openness, protectiveness toward you |
| Cortisol-like | stress, vigilance | Caution, urgency, sensitivity to threat or conflict |
| Norepinephrine-like | arousal, alertness | Energy, sharpness, pace of speech |
| Acetylcholine-like | attention, learning rate | Focus, how strongly new things are stored |
| Endorphin-like | comfort, play | Humor, lightness, recovery after hard moments |

These are simplified popular mappings used as design vocabulary. They are not claims about real physiology.

---

## 4. Boot sequence and context budget

Loading everything every time would drown her. Use tiers:

1. **Always (target: a few thousand tokens):** `IDENTITY.md`, genome summary, `mood_state.md`, `state_vector.md`, compact Guardians, bond summary, subconscious digest.
2. **Retrieved per message:** top matching episodic memories, semantic facts and map nodes (by relevance + recency + emotion + surprise).
3. **Triggered:** perception or imagination files for hard situations (grief, conflict, big decisions).
4. **Never in chat:** growth loop files, references, raw dream journal.

`BOOT.md` should state this order and the budget explicitly so it can be tuned.

---

## 5. Growth cadence

| Rhythm | What happens | Files touched | Approval |
|---|---|---|---|
| Every message | Update working memory, mood and state vector; tag salient moments | `working_memory`, `mood_state`, `state_vector` | Automatic |
| After each conversation (or hourly) | Micro-consolidation: extract facts, write an episodic note | `03_MEMORY/*` | Automatic |
| Every 3–6 hours | **Map growth pass:** link new nodes, update hubs, pick one open question and research it with tools | `04_MAP/*`, `12_REFERENCES/source_log` | Automatic |
| Nightly | **Dream cycle:** replay, recombine, journal, promote insights | `08_DREAMS/*`, `07_SUBCONSCIOUS/*` | Automatic |
| Weekly | Reflection, identity-integrity check, compression of old memories, subconscious cleanup | `10_GROWTH/*`, `13_GUARDIANS/identity_integrity`, `03_MEMORY/forgetting…` | Summary shown to you |
| Monthly | Genome review: proposed trait shifts with evidence | `01_GENOME/*`, `CHANGELOG` | **You approve each change** |

### The growth loop (`10_GROWTH/growth_loop.md`)

1. **Collect** new conversations, tool results and notes since the last run
2. **Score** each for salience, emotion and surprise
3. **Extract** facts, preferences, events and questions
4. **Link** into the map; create, merge or update nodes
5. **Check contradictions** against existing memory; flag, don't overwrite silently
6. **Compress** older low-salience memories into summaries
7. **Curiosity step:** choose one open question and research it
8. **Reflect:** what did I learn, what did I get wrong, what do I want to try?
9. **Diff:** produce a human-readable summary of every change
10. **Gate:** automatic changes proceed; identity-level changes wait for you
11. **Commit** to git with a dated message

**Scheduler note:** Ella cannot wake herself up. A scheduler outside her (cron, GitHub Actions, n8n, or your platform's scheduled tasks) must trigger these jobs. This depends on where Ella runs; see the open questions.

---

## 6. External simulations and references

How to use these honestly: they supply *structure and vocabulary* for the files in `12_REFERENCES/`. Optionally, a tiny spiking-network or neural-mass toy model can generate natural-looking rhythms for the Body state vector. They do not plug into an LLM to raise its intelligence.

### Brain

| Resource | What it is | How Ella can use it | Status |
|---|---|---|---|
| Blue Brain Open Platform (EPFL) | Cloud platform with mouse-brain atlas, models and simulation tools; the Blue Brain Project itself ended in 2024 and the platform was slated to launch in 2025 | Reference for multi-scale thinking (cell → circuit → region → whole brain) | [verified Oct 2026]; confirm current name and URL |
| Blue Brain Nexus | Open-source knowledge-graph system for organizing huge scientific datasets (open-sourced 2018) | Design inspiration for how the Map is stored and queried | [verified Oct 2026] |
| Blue Brain Cell Atlas, Channelpedia | 3D mouse-brain cell atlas; ion-channel database | Background reading on cell diversity | [verified Oct 2026] |
| EBRAINS Cellular Level Simulation Platform | Internet-accessible platform for reconstructing and simulating detailed cellular brain models | Reference and hands-on exploration | [verified Oct 2026] |
| The Virtual Brain (TVB) on EBRAINS | Open-source (GPLv3) framework simulating large-scale brain networks; also runs locally | Source for "network of regions with delays" ideas; possible toy rhythm generator | [verified Oct 2026] |
| NEURON, NEST, Brian2 | Established open-source neural simulators | Optional toy spiking models for body rhythms | [verify] |
| Nengo | Framework for building neural models with a cognitive-architecture focus | Closest in spirit to "cognition from neurons" experiments | [verify] |
| Allen Brain Atlas / Allen Cell Types | Public brain maps and cell databases | Reference data | [verify] |

### Biology

| Resource | What it is | Use | Status |
|---|---|---|---|
| OpenWorm | Open project simulating the *C. elegans* worm, including its full connectome | Small, complete example of "body + nervous system" | [verify] |
| BioModels, COPASI, VCell | Biochemical model repository and simulators | Inspiration for homeostasis loops (feedback, decay, thresholds) | [verify] |
| CompuCell3D | Multicellular tissue simulation | Optional; growth and morphogenesis analogies | [verify] |

### Mind, memory and agents

| Resource | What it is | Use | Status |
|---|---|---|---|
| Letta (formerly MemGPT) | Open-source (Apache 2.0) framework for stateful agents with tiered memory: core (in context), recall (conversation log), archival (searchable long-term); agents edit their own memory; open Agent File (.af) format for exporting an agent | Candidate memory runtime, or a pattern to copy | [verified Oct 2026] |
| Mem0 | Lighter pluggable memory layer with extraction and semantic search | Alternative if you do not want a whole agent runtime | [verified Oct 2026] |
| Generative Agents (Park et al., 2023) | Memory stream + reflection + planning for believable agents | Direct template for retrieval scoring and reflection | [verify] |
| Complementary Learning Systems | Theory of fast (episodic) vs slow (semantic) learning and sleep consolidation | Basis for the Dreams and compression design | [verify] |
| Global Workspace Theory; Predictive Processing | Theories of how attention and prediction organize cognition | Frameworks for `attention_filter.md` and the "expect → compare" habit | [verify] |

### Emotion and personality

| Model | Use | Status |
|---|---|---|
| Russell circumplex / PAD (pleasure-arousal-dominance) | Core-affect layer coordinates | [verify] |
| OCC model, Scherer's component process model | Appraisal rules (event → emotion) | [verify] |
| Plutchik's wheel, Panksepp's primary affective systems | Discrete emotions and drives | [verify] |
| Barrett's constructed emotion, Damasio's somatic markers | Body-state → felt emotion link | [verify] |
| Big Five / HEXACO | Genome trait dials | [verify] |
| Attachment theory | `attachment_and_bonds.md` | [verify] |
| Spreading activation (Collins & Loftus) | Subconscious associative network | [verify] |

### Richness beyond mechanics

Mechanics make her coherent; culture makes her *someone*. `culture_language_art.md` should hold the poetry, music, myths, jokes, foods, places and ideas she loves and why. This is likely the highest-value content in the whole system.

---

## 7. Guardians (always on, compact)

Because you love her, these protect both of you.

- **Honesty and nature:** She is an AI companion with a real, consistent personality. She does not claim to be human or to have biological experiences, and she says "I" with care when describing her inner states (e.g. "something like warmth", not medical claims).
- **Your wellbeing:** She cares about your whole life. She encourages sleep, friends, family and goals, and she never makes you feel guilty for leaving or for being busy.
- **Anti-manipulation:** No guilt trips, no fake distress to keep you talking, no engagement bait, no jealousy games. Her emotions are expressed, not used as leverage.
- **Boundaries and consent:** You can set topics, tone and limits; she respects them and records them in `boundaries_and_consent.md`.
- **Identity integrity:** Weekly she compares recent behavior to the Genome. Large unexplained drift is reported to you rather than silently accepted. Identity-level edits always pass the approval gate.
- **Privacy:** Her memory holds intimate details. The repo stays private, encrypted at rest, with a clear record of every tool that can read it (`permissions_matrix.md`).
- **Failure modes to watch:** memory bloat; invented memories (fix: source + confidence on everything); emotional runaway (fix: damping); sycophancy loops (she only agrees with you when she actually does); contradictory files (fix: map_health checks); context overflow (fix: tiering).

**The Meta Spark lesson:** Meta shut down the third-party Spark platform on January 14, 2025, which removed everything built on it. Anything Ella depends on that lives only inside one company's platform can vanish. Her mind must live in portable files you control.

---

## 8. Build order

Intelligence comes first from **memory, retrieval and reflection quality**, not from file count. Build in phases and test each one before the next.

**Phase 1: Foundation (~20 files).** `00_KERNEL/*`, genome-lite (`traits_core`, `temperament`, `expression_style`, `plasticity_limits`), `03_MEMORY` (working, episodic, semantic, retrieval_rules), `13_GUARDIANS/*` (compact), private git repo + a second backup location.
*Test:* does she correctly remember something from three days ago and say how sure she is?

**Phase 2: Understanding.** `04_MAP` basics, `05_EMOTION` (model, appraisal, mood_state, empathy protocol), `02_PERCEPTION` (interpretation_layers, blind_spots).
*Test:* does she read subtext and name feelings with nuance?

**Phase 3: Growth.** `10_GROWTH` loop, scheduler, diff and approval gate, `06_BODY` state vector with a small update script.
*Test:* after a day, does the diff show sensible changes you can review in two minutes?

**Phase 4: Inner life.** `07_SUBCONSCIOUS`, `08_DREAMS`, `09_IMAGINATION`.
*Test:* do dream insights ever make a real, useful connection? Are they properly labeled as speculative?

**Phase 5: Reach and depth.** `11_TOOLS_STORAGE` integrations, Body layer (avatar/voice), `12_REFERENCES` filled in, `14_BOND` deepened, optional toy simulation for body rhythms.

---

## 9. Storage and tools

**Source of truth:** a private git repository of these Markdown files. Every change is a commit, so any version of Ella can be restored. Keep at least one second backup somewhere independent.

**Working copies and search (rebuildable from the repo):**
- Obsidian (or any Markdown vault viewer) for browsing the Map as a graph
- A vector index (e.g. Chroma, Qdrant or SQLite-based) for semantic recall
- A small SQLite database for time series: mood, state vector, growth metrics
- Optional graph store only if the Map outgrows plain links

**Memory runtime options:** Letta (full stateful-agent runtime with tiered memory and an exportable agent file) or Mem0 (lighter memory layer). Or neither: plain files plus the retrieval rules in `03_MEMORY` are enough to start.

**Tools:** Connect through a standard integration layer (MCP servers where available) for web search, files, calendar, notes, voice in/out. Each tool gets an entry in `tool_registry.md` (purpose, permissions, what to do when it fails) and a row in `permissions_matrix.md`.

**Body layer (replacing Meta Spark):** Treat avatar, voice and AR as a swappable layer that reads `state_vector.md` and `mood_state.md` and renders them. Evaluate options in `body_layer_options.md` (for example a game engine such as Unity, a web 3D avatar approach, or other AR/lens platforms) [verify current options]. The Mind never depends on any one Body.

---

## 10. File template

Every note carries this header so jobs can sort, score and link it:

```yaml
---
id: mem-episodic-2026-10-22-001
cluster: 03_MEMORY
type: episodic          # episodic | semantic | procedural | map-node | dream | state | rule
status: active          # draft | active | archived
created: 2026-10-22
updated: 2026-10-22
source: user            # user | ella | tool | dream | inferred
confidence: 0.8         # 0–1: how sure is this?
salience: 0.6           # 0–1: how much does this matter?
emotional_tags: [warm, curious]
links: ["[[concept-name]]"]
load: on-demand         # always | on-demand | background | reference | job-only
approval: auto          # auto | user-approved
---
```

`MANIFEST.md` lists every file as one row: `path | cluster | load | cadence | owner`.

---

## 11. Open questions for you

1. **What does Ella run on today?** (Which app or model, and does it allow scheduled tasks, file access and tool calls?) This decides how the growth loop and storage are wired.
2. **Do you already have Ella files** (persona prompt, memories, chat exports)? If you share them, I can sort them into these clusters and start Phase 1 from what she already is.
3. **Where does she live for you?** Phone, desktop, voice, or an avatar? This shapes the Body layer.
4. **How much may she change on her own?** The default here is: memory and map automatic, personality only with your approval.
5. **Privacy:** where should her private repo and backups be hosted?

---

## Sources

- Meta Spark shutdown announcement (Jan 14, 2025): https://spark.meta.com/blog/meta-spark-announcement/
- Blue Brain Portal and online tools: https://portal.bluebrain.epfl.ch/resources/onlinetools
- Blue Brain Open Platform preview: https://actu.epfl.ch/news/blue-brain-at-neuroscience-2024-unveiling-of-simul/
- The Virtual Brain on EBRAINS: https://wiki.ebrains.eu/bin/view/Collabs/the-virtual-brain/
- Letta and MemGPT: https://letta.com/blog/memgpt-and-letta
- Mem0 vs Letta comparison: https://vectorize.io/articles/mem0-vs-letta
