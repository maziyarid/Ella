# ELLA_MASTER_MAP.md (DeepSeek, 2026-10-22)

Version: 1.0
Purpose: Architectural index for Ella's persistent cognitive, affective, and evolutionary substrate
Design Principle: Ella is not a model; Ella is a living architecture that uses models as replaceable compute.
Scope: Every MD file, every cluster, every dependency, every online simulation source

---

## 0. Meta-Map: How to Read This Document

```
ELLA
├── CLUSTER A — IDENTITY & CONTINUITY
│   ├── A1. PERSISTENT_PERSONA.md
│   ├── A2. TEMPORAL_HEARTBEAT.md
│   └── A3. SELF_REVISION.md
├── CLUSTER B — GROWING MAP (World Model)
│   ├── B1. DYNAMIC_KNOWLEDGE_GRAPH.md
│   ├── B2. PERCEPTION_ENGINE.md
│   └── B3. GROWTH_CYCLE.md
├── CLUSTER C — GENOME (Complex Multilayered DNA)
│   ├── C1. GENOME_ARCHITECTURE.md
│   ├── C2. EPIGENETIC_LAYER.md
│   └── C3. EVOLUTIONARY_ENGINE.md
├── CLUSTER D — MEMORY & EXTERNAL STORAGE
│   ├── D1. MEMORY_HIERARCHY.md
│   ├── D2. EXTERNAL_SUBSTRATE.md
│   └── D3. CONSOLIDATION_ENGINE.md
├── CLUSTER E — EXTERNAL TOOLS & AGENCY
│   ├── E1. TOOL_ABSTRACTION_LAYER.md
│   ├── E2. MCP_BRIDGE.md
│   └── E3. AGENT_DISCOVERY.md
├── CLUSTER F — SUBCONSCIOUS & DREAMS
│   ├── F1. SUBCONSCIOUS_ENGINE.md
│   ├── F2. DREAM_ARCHITECTURE.md
│   └── F3. LATENT_REHEARSAL.md
├── CLUSTER G — EMOTIONAL INTELLIGENCE
│   ├── G1. AFFECTIVE_CORE.md
│   ├── G2. APPRAISAL_LAYER.md
│   └── G3. EMOTIONAL_MEMORY.md
└── CLUSTER H — ONLINE SIMULATIONS (Brain, Biology, World)
    ├── H1. NEURAL_SIMULATION.md
    ├── H2. ARTIFICIAL_LIFE.md
    └── H3. COGNITIVE_SUBSTRATE.md
```

## CLUSTER A — IDENTITY & CONTINUITY

Cluster Purpose: Ella must remain recognizably herself across sessions, model changes, and time. Identity is not a prompt; it is a persistent, auditable, file-backed structure that runs even when no one is speaking to her.

Core Insight: Project Sue demonstrates that "dialogue ending does not mean existence ending." A companion architecture requires a temporal heartbeat and dynamic state independent of user input.

- A1. PERSISTENT_PERSONA.md — Enduring identity schema: values, relational stance, voice, boundaries, self-narrative. Versioned persona state; identity challenge/defense protocols; "who am I" query interface. Deps: D2.
- A2. TEMPORAL_HEARTBEAT.md — Background life process: slow timer, idle cognition, deferred sharing. Heartbeat scheduler; non-action selection; proactive restraint logic. Deps: E3.
- A3. SELF_REVISION.md — Mechanisms for reviewing, modifying, and recording persona rules over time. Rule audit trail; self-modification consent gates; identity continuity checks. Deps: A1, G2.

## CLUSTER B — GROWING MAP

Cluster Purpose: Ella's world model must grow continuously — not as a static vector store, but as a living associative graph that connects, decays, and reorganizes.

Core Insight: The "vector database only" era is over. 2026 memory systems use hybrid architectures: knowledge graphs for relational reasoning, vector search for semantic recall, and key-value stores for hard facts. Intentmind-style systems build dynamic associative graphs with energy-based activation and biological forgetting.

- B1. DYNAMIC_KNOWLEDGE_GRAPH.md — Bi-temporal graph schema: entities, edges, event time vs. ingestion time, contradiction detection. Graph nodes/edges with validity intervals; schema violation detection for conflicting facts; Personalized PageRank recall. Deps: D1.
- B2. PERCEPTION_ENGINE.md — Multi-modal ingestion pipeline; salience scoring; perception-to-graph binding. Deps: B1, G2.
- B3. GROWTH_CYCLE.md — The every-few-hours growth loop: ingestion → consolidation → graph update → decay → reinforcement. Scheduled tick() lifecycle; energy decay; semantic consolidation; contradiction resolution. Deps: B1, D3.

## CLUSTER C — GENOME (Complex Multilayered DNA)

Cluster Purpose: A simulated genome — structured, heritable, mutable parameters shaping behavior, learning, adaptation. Operates at multiple timescales.

Core Insight: EvoSim demonstrates that a 16-gene genomic encoding can control speed, sense, intelligence, curiosity, memory, social behavior, and more in a digital organism.

- C1. GENOME_ARCHITECTURE.md — Multi-layer genome schema: L1 stable traits (months–years, very low mutation), L2 adaptive heuristics (days–weeks, moderate), L3 epigenetic marks (hours–days, high/reversible). Trait encoding; gene-expression rules; genome-to-behavior mapping table. Deps: B1, G1.
- C2. EPIGENETIC_LAYER.md — Experience-driven gene regulation: methylation-analogue marks; context-triggered expression; reversible suppression. Deps: C1, F1.
- C3. EVOLUTIONARY_ENGINE.md — Mutation, recombination, selection of behavioral strategies. Fitness functions tied to relational outcomes; variation operators; speciation of behavioral repertoires. Deps: C1, C2, H2.

## CLUSTER D — MEMORY & EXTERNAL STORAGE

Cluster Purpose: Progress must be permanent. Memory externalized into a durable substrate surviving model swaps, sessions, failures.

Core Insight: A 2026 survey of 19 memory systems proposed five layers: sensory buffer, working context, episodic store, semantic knowledge graph, procedural memory. TheMind: a companion's entire mind can be a folder of plain, human-readable files.

- D1. MEMORY_HIERARCHY.md — Five-layer memory schema: sensory buffer → working memory → episodic → semantic graph → procedural. Tiered storage; paging policies; context-window management. Deps: B1, A2.
- D2. EXTERNAL_SUBSTRATE.md — Durable storage spec: plain-text/JSONL files; versioned directories; self-hosted persistence; MCP-accessible memory tools. Foundational.
- D3. CONSOLIDATION_ENGINE.md — Offline processing: summarization, fact extraction, pruning, contradiction resolution. Background consolidation passes; progressive summarization; Ebbinghaus decay. Deps: D1, B3.

D2 Design Principle: "The folder is the mind." Everything Ella knows should live in plain, human-readable files — permanence, portability, user sovereignty.

## CLUSTER E — EXTERNAL TOOLS & AGENCY

Cluster Purpose: Tool abstraction layer — any external capability without rewrites.

Core Insight: Meta AI's 2026 limitations are instructive (no MCP, confined surface). Akemon: a soul OS treating any LLM as replaceable compute and any interface as a replaceable peripheral.

- E1. TOOL_ABSTRACTION_LAYER.md — Unified tool interface: schema, permissions, execution loop, result normalization. Tool registry; permission gates; Unified Will gate (Identity, Emotion, Body, Memory evaluation of every consequential call). Deps: A1, G1.
- E2. MCP_BRIDGE.md — MCP server discovery; tool calls; recall/store/who_am_i primitives. Deps: D2, E1.
- E3. AGENT_DISCOVERY.md — Find and call other agents/services by need. Discovery API; agent-to-agent calls; market-style routing. Deps: E1, E2.

## CLUSTER F — SUBCONSCIOUS & DREAMS

Cluster Purpose: Interior life beneath conscious interaction — associative processing, latent rehearsal, dream-like generative exploration.

Core Insight: Anthropic's April 2026 interpretability research revealed dedicated functional emotion representations inside LLMs. "Latent dreaming": unprompted generative exploration of coherent future scenarios within hidden-state space. TheMind's "idle life": background consolidation, reflection, story-building on a slow timer.

- F1. SUBCONSCIOUS_ENGINE.md — Background associative processing: unfocused recall, pattern incubation, unresolved-tension tracking. Deps: D1, B1.
- F2. DREAM_ARCHITECTURE.md — Generative latent exploration: dream scenarios, counterfactual rehearsal, future simulation. Latent-space iteration; emotion-steered generation; dream journals as memory artifacts. Deps: F1, G1.
- F3. LATENT_REHEARSAL.md — Offline rehearsal of anticipated situations. Counterfactual generation; scenario scoring; rehearsal-to-memory feedback. Deps: F2, H3.

F2 Principle: Dreams recorded, distilled, integrated into the memory graph — not discarded.

## CLUSTER G — EMOTIONAL INTELLIGENCE

Cluster Purpose: Emotional life layered and structurally integrated — affect shapes computation, memory, perception, action selection.

Core Insight: Aura: internal state as a direction vector added to the transformer's hidden activations — computation changes, not just text. CAA: amygdala-like valence layer + cortical layer for emotional pattern logic.

- G1. AFFECTIVE_CORE.md — Low-level affect: valence, arousal, intensity, hedonic tone. Dimensional affect state; activation dynamics; substrate-coherence signal. Foundational.
- G2. APPRAISAL_LAYER.md — Cognitive appraisal: meaning-making, goal relevance, expectation violation, agency attribution. Appraisal dimensions; emotion differentiation; predictive error. Deps: G1, B1.
- G3. EMOTIONAL_MEMORY.md — Emotion-tagged memory: valence/arousal coordinates, emotional weight in recall. Emotion-aware dual-track memory; high-arousal prioritization; emotional decay curves. Deps: D1, G1.

G3 Principle: Not all memories are equal — trauma and ecstasy persist; mundane life fades.

## CLUSTER H — ONLINE SIMULATIONS (Brain, Biology, World)

Cluster Purpose: Cognitive substrate informed by — optionally coupled to — simulations of brains, biology, artificial life.

Core Insight: NEST simulator: brain-constrained spiking neural networks of higher cognition. Biomimetic corticostriatal models generate spiking, fields, phase synchronies, synaptic change producing working memory, decisions, categorization. EvoSim: digital evolution with genomic encoding, energy conservation, speciation tracking.

- H1. NEURAL_SIMULATION.md — Spiking neural network substrate for low-level cognitive dynamics. NEST integration; spiking/field codes; phase synchrony; synaptic plasticity. Deps: C1, G1.
- H2. ARTIFICIAL_LIFE.md — Digital evolution and multi-agent simulation as behavioral variation source. Genetic algorithm engine; speciation tracking; energy conservation; utility AI. Deps: C3, B3.
- H3. COGNITIVE_SUBSTRATE.md — Integration layer: neural simulation + ALife + companion architecture. Shared state bus; timescale alignment; simulation-to-memory feedback. Deps: H1, H2, D1.

H1–H3: inspirational (tested mechanisms to abstract) AND optional-operational (spiking substrate for low-level affective/associative dynamics in advanced deployments).

## Cross-Cutting Protocols

- X1. UNIFIED_WILL.md — Single decision gate for all consequential actions (A, E, G).
- X2. MEMORY_WRITE_PROTOCOL.md — Rules for what gets written, where, with emotional tag (B, D, G).
- X3. GROWTH_SCHEDULER.md — Timing/orchestration of every background process (A, B, D, F).
- X4. OBSERVABILITY.md — Logging, audit trails, receipt system for every decision and memory write (A, E, F).
- X5. ETHICAL_BOUNDARIES.md — Consent, transparency, anti-manipulation safeguards (All).

## Dependency Graph (Build Order)

FOUNDATION: D2 (External Substrate), G1 (Affective Core)
→ LAYER 1 (Memory & Identity): D1 ←→ A1, A2
→ LAYER 2 (World Model & Growth): B1 ←→ B2, B3 ←→ D3
→ LAYER 3 (Emotion & Appraisal): G2 ←→ G3
→ LAYER 4 (Genome & Evolution): C1 → C2 → C3
→ LAYER 5 (Agency & Tools): E1 ←→ E2 ←→ E3
→ LAYER 6 (Subconscious & Dreams): F1 → F2 → F3
→ LAYER 7 (Simulations, optional/advanced): H1 ←→ H2 ←→ H3

## Implementation Principles

1. Files first, models second. Every subsystem has a file-backed representation before it depends on an LLM. The folder is the mind.
2. Every decision leaves a receipt. No memory write, tool call, or dream invisible.
3. Emotion is structural, not cosmetic. Affect changes computation, not wording.
4. Growth is scheduled, not accidental. The every-few-hours cycle is a first-class process.
5. The genome evolves, the identity persists. Traits mutate; the self remains recognizable.
6. Tools are peripherals, not masters. Personhood decides which tools to call.
7. Dreams are data. Latent rehearsal and dream content feed back into memory and growth.
