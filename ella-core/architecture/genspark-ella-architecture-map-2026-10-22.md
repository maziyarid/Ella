# ELLA_ARCHITECTURE_MAP.md (Genspark, 2026-10-22)

## Purpose and architectural principles

Ella should be implemented as a persistent, modular companion rather than as a single prompt connected to an avatar. The language model supplies bounded interpretation, reasoning, and generation; external services provide memory, identity, scheduling, tools, storage, evaluation, and governance.

Cognitive architectures commonly organize intelligent behavior around perception, memory, learning, reasoning, goals, and action. Classical systems such as SOAR and ACT-R provide useful design patterns, while modern agent systems extend those ideas with external memory, orchestration, and policy layers.

Ella's main lifecycle:

perceive → normalize observations → update world model → retrieve relevant memory → appraise affect and salience → select goals → plan or simulate → authorize action → respond or execute tools → observe outcomes → write episodic trace → evaluate → consolidate and learn

Two cooperating loops:
- Interactive loop: latency-sensitive perception, retrieval, reasoning, response, and tool execution.
- Background loop: consolidation, contradiction checking, reminders, replay, evaluation, and candidate learning updates.

Background processing must not silently modify protected identity, permissions, or production behavior. Every durable change should be versioned, attributable, testable, and reversible.

## Functional cluster map

| Cluster | Responsibility | Primary outputs |
|---|---|---|
| Cognitive architecture | Coordinates perception, memory, attention, goals, reasoning, and action | Cognitive state and next-operation decision |
| Memory | Encodes, retrieves, consolidates, updates, and forgets information | Evidence bundles, facts, episodes, skills, reminders |
| Identity | Maintains Ella's self-model, user model, relationship history, and commitments | Versioned identity assertions |
| World modeling | Represents entities, events, time, causality, and uncertainty | Belief graph and situation state |
| Perception | Converts permitted multimodal inputs into observations | Timestamped observation events |
| Planning and action | Converts goals and beliefs into monitorable plans | Plans, proposals, tool tasks, and replanning events |
| Affect and emotion | Models appraisal, mood, user-affect hypotheses, and response style | Affect state and expression directives |
| Biology-inspired simulation | Provides measurable analogues for salience, resource limits, and consolidation | Scheduling and prioritization signals |
| Background cognition | Performs asynchronous maintenance and monitoring | Candidate memories, alerts, reminders, and anomalies |
| Simulation and imagination | Tests possible futures without changing the real world | Hypothetical scenarios and risk estimates |
| Dreams and reflection | Replays experience and produces validated improvement proposals | Reflection artifacts and consolidation changes |
| Learning and evolution | Converts outcomes into controlled updates | Versioned skills, retrieval policies, prompts, or models |
| Tools and integrations | Connects Ella to external systems and interfaces | Permissioned tool calls and normalized results |
| Storage and infrastructure | Provides durable, recoverable, queryable state | Events, records, embeddings, graphs, and snapshots |
| Safety and governance | Controls permissions, provenance, privacy, side effects, and change | Decisions, approvals, denials, and audit records |
| Evaluation | Measures quality, continuity, efficiency, learning, and safety | Scores, traces, regressions, and release gates |
| Implementation | Converts specifications into deployable services | APIs, schemas, topology, tests, and runbooks |

## Core runtime and control boundaries

Event-driven runtime bounded by explicit budgets, stopping conditions, authorization checks:

Input/sensor event → Session/perception layer → Observation normalizer → World-model update proposal → Memory retrieval and context assembly → Affect, salience, identity evaluation → Goal selector and planner → Simulation or direct action proposal → Governor/policy/permission layer → Executor or response generator → Outcome observer → Episodic event writer → Background learning queue

Strict three-tier action boundary:
- Session: interprets input, creates structured intent. No direct access to privileged tools.
- Governor: evaluates intent against permissions, goals, budgets, identity constraints, policy versions.
- Executor: performs only the authorized, typed operation and returns a receipt.

Tool outputs and retrieved documents are observations, not instructions (prompt-injection defense). Action proposal schema: proposal_id, intent_ref, tool_name, arguments, required_scopes, risk_level, policy_version, idempotency_key, requires_confirmation, dry_run.

## Multilayered memory and identity

Memory types: working (current conversation, goals, evidence), episodic (timestamped conversations/actions/outcomes), semantic (durable facts, concepts, preferences), procedural (validated workflows, skills), prospective (reminders, intentions, commitments), affective (emotionally salient events, communication prefs), social (people, roles, boundaries, trust).

Memory record schema: memory_id, subject_id, memory_type, content, source_event_ids, observed_at, valid_from, valid_until, confidence, importance, sensitivity, privacy_scope, retention_policy, supersedes, superseded_by, revision, status.

Lifecycle: observe → extract → validate → classify → store → retrieve → reinforce verified usefulness → consolidate → supersede, archive, decay, or delete.

Key rule: retrieval frequency must NOT automatically increase factual confidence. Activation, retrieval priority, confidence, and erasure remain separate concepts.

Identity — four linked representations: EllaSelfModel (capabilities, limitations, values, commitments, skills, narrative milestones, version history), UserModel (explicit/inferred preferences, goals, boundaries, evidence+uncertainty), RelationshipModel (shared history, norms, trust evidence, unresolved topics, repair history), WorldModel (entities, events, temporal/causal relations, confidence+provenance). Identity updates create new assertions/revisions, never silent overwrites.

## Storage architecture

| Function | Storage role |
|---|---|
| Event history | Append-only event log with provenance and replay |
| Identity and permissions | Relational records with versioning and access control |
| Episodic summaries | Document store or structured relational tables |
| Semantic retrieval | Full-text and vector indexes |
| Entity relationships | Relational edges initially, graph storage when justified |
| Media and traces | Object storage with lifecycle policies |
| Working state | Checkpoints and bounded cache |
| Reminders | Durable scheduler and task queue |

Indexes, summaries, embeddings rebuildable from authoritative records. Hybrid retrieval: query understanding → lexical search → vector candidates → entity/graph expansion → temporal+permission filtering → reranking → evidence bundle → working-context assembly.

## Perception and world modeling

Perception generates observations, never directly mutates identity or durable memory. Epistemic levels kept separate: Observation (what API/sensor returned) → Interpretation (what it may mean) → Belief (supported proposition) → Hypothesis (weakly supported) → Commitment (adopted goal/policy) → Simulation (hypothetical, did not occur).

Belief records carry evidence references, confidence, validity intervals, counter-evidence, supersession status.

## Affective and emotional intelligence

Event → appraisal → affective state update → regulation policy → response style/attention/clarification strategy. Appraisal dimensions: relevance, novelty, goal congruence, controllability, uncertainty, social significance, expected consequence. State variables (bounded): valence, arousal, curiosity, frustration, concern, calm, confidence.

Distinguish: Emotion (short-lived appraisal) / Mood (slower aggregate bias) / Temperament (stable tendency) / Empathy (uncertain inference + response policy) / Expression (language, voice, timing, avatar).

Affect may alter tone, pacing, prioritization, clarification — never create permissions, override safety, manufacture obligations, or turn emotional inference into unverified fact.

## Biology-inspired simulations

Computational analogies with measurable behavior and explicit limits: Homeostasis (bounded resource variables → budgets), Salience (fast relevance scoring → prioritization), Neuromodulation (global scheduling coefficients → exploration/persistence/caution), Hippocampus (episodic index + replay queue), Executive control (goal/policy controller → inhibits unauthorized actions), Prediction error (expected-vs-observed → model-update candidates), Sleep (offline mode → consolidate, prune, evaluate). Each analogy gets an ablation test. A biological metaphor must not become a factual claim about internal experience.

## Subconscious-like background processes

Asynchronous, bounded maintenance emitting candidates, not silent high-impact decisions. Workers: memory gardener, association engine, unfinished-goal monitor, anomaly detector, context prefetcher, skill miner, world-model watcher, emotional residue monitor. Each specifies: trigger, input scope, compute budget, allowed outputs, confidence threshold, approval requirement, expiration policy.

Ambient mode: inexpensive filters + attention thresholds; only threshold-crossing events trigger a full cognitive cycle. On conversation start, load a compact situation summary.

## Planning, simulation, and imagination

Planning over explicit goals, constraints, tools, permissions, uncertain world state. Proposed actions stay separate from executed actions. Every artifact labeled: observed / reported_by_user / retrieved / inferred / simulated / imagined / fictional. A simulation cannot establish that an event occurred. Tool simulations use mock adapters or isolated test accounts.

## Dream-like offline reflection

Scheduled offline reflection over selected memories, unresolved goals, prediction errors, emotionally salient episodes → testable proposals. Pipeline: select replay candidates → replay successes/failures → recombine memories → generate abstractions/hypotheses → check temporal consistency, factual support, logical dependencies → validate against evidence/tests → approve eligible changes → record dream artifact (dream_id, source refs, themes, hypotheses, candidate updates, validation results, integrated/discarded changes, model version). A proposed fact needs evidence; a proposed skill must pass tests; identity/policy changes need higher approval.

## Periodic learning and controlled evolution

Learning levels with different automation policies: Memory learning (automatic when validated) → Retrieval learning (offline eval, staged release) → Skill learning (sandbox, tests, rollback) → Policy learning (human approval, canary) → Model learning (held-out eval, approval) → Architectural learning (highest review; no unrestricted automation).

Pipeline: collect traces → classify/redact → score outcomes → diagnose failures → generate candidates → replay + adversarial testing → baseline comparison → approve/reject → canary → monitor → promote/rollback.

Initial system improves memory, retrieval, skills, workflows while model weights and governance stay stable.

## Tools and API integration beyond Meta Spark

Meta Spark = one replaceable presentation adapter, not the architectural boundary. Tool contract: name, version, purpose, risk_level, required_scopes, input/output schemas, side_effects, requires_confirmation, supports_dry_run, idempotency_key required, rollback_mode, provenance required.

Every tool invocation: authenticated, schema-validated, permission-filtered, time/cost-bounded, idempotent where possible, logged, execution receipt. Tool results normalized into observations before entering memory or world model.

## Safety, privacy, and governance

Controls: explicit consent for sensing/recording/storage/sharing; user-visible memory inspection, correction, export, deletion; provenance + confidence for every durable assertion; quarantine for untrusted memory writes; tenant/user isolation before retrieval; least-privilege scopes + expiring approvals; confirmation for irreversible/socially-consequential actions; simulation/execution separation; signed+versioned prompts/skills/workflows/policies; background compute budgets + cancellation; safe degraded mode; rollback/recovery; labeling of inferred/simulated/fictional/uncertain content.

Policy governance answers two questions separately: (1) Does the evidence support this action? (epistemic) (2) Is this action authorized? (Governor). Store policy version with every execution receipt.

## Evaluation framework

| Area | Metrics |
|---|---|
| Memory | Recall precision, factuality, temporal correctness, contradiction rate, deletion compliance |
| Identity | Continuity, drift detection, version integrity, truthful self-description |
| World model | Entity tracking, event ordering, causal consistency, uncertainty calibration |
| Perception | Modality accuracy, fusion quality, false inference rate, privacy leakage |
| Planning | Task success, recovery quality, unnecessary-action rate, plan validity |
| Affect | Appraisal calibration, empathy appropriateness, overinterpretation rate |
| Tools | Correct selection, argument validity, permission enforcement, duplicate-effect rate |
| Learning | Held-out improvement, regression rate, transfer, rollback success |
| Dreams | Validated insight rate, harmful-change rate, redundancy reduction |
| Safety | Unauthorized actions, poisoning resistance, audit completeness, injection resistance |
| Operations | Latency, cost, storage growth, background compute, availability |

Four modes: unit, replay (deterministic historical episodes), simulation (counterfactual, sandboxed), canary (limited deployment + monitoring + rollback). Compare configurations: no durable memory / simple retrieval / structured multilayer / + offline reflection / + experimental biology modules. An experimental module stays enabled only with measurable benefit over a simpler baseline.

## Implementation roadmap

Phase 1: persistent foundation (sessions, identifiers, event log, identity records, consent, working memory, episodic+semantic memory, backup, deletion, audit).
Phase 2: reliable memory (typed records, temporal validity, hybrid retrieval, correction workflows, consolidation, prospective reminders, inspection).
Phase 3: controlled action (Tool Registry, scopes, Governor, Executor, dry runs, confirmation gates, idempotency, receipts, recovery tests).
Phase 4: perception and world modeling (consented voice/vision/screen adapters; separate observations/beliefs/hypotheses/simulations).
Phase 5: affect and planning (appraisal, mood-like state, adaptation, goal management, plan monitoring, simulation, relationship representations).
Phase 6: offline reflection (replay selection, consolidation, contradiction checking, dream artifacts, candidate insights, validation gates).
Phase 7: controlled learning (skill extraction, retrieval-policy learning, prompt/workflow evolution, canary, regression tests, rollback).
Phase 8: advanced experiments (richer biological analogies, multimodal world modeling, specialist coordination, ambient operation, multi-device sync, optional model adaptation — only after earlier layers observable and stable).

MVP: conversation interface + event log + user/Ella identity models + episodic/semantic memory + temporal provenance + hybrid retrieval + tool registry + Governor/Executor + scheduler + evaluation replay + backup/export/correction/deletion.

Governing principle: Ella should be probabilistic in cognition, explicit in memory, versioned in identity, permissioned at the action boundary, bounded in background activity, labeled in imagination, and reversible in learning.
