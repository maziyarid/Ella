# Architecture reconciliation — four authoritative memory stores

Status: proposal (v0.1). No live memory is moved, renamed or rewritten by this lane.

## The four stores

These are the only authoritative personal-memory stores. Everything else is either a logical category inside one of them,
a derived index rebuilt from them, or a different kind of state that is not personal memory.

| Store | Physical form (proposed) | Holds | Authority | Write rule |
|---|---|---|---|---|
| Core `MEMORY.md` | One small Markdown file, versioned | Approved identity and profile pointers, standing preferences, accepted decisions, accepted corrections, guardian rules (or pointers to them) | Owner-approved entries only | Change by owner-approved edit. A correction supersedes by stable ID; the old entry stays in history. |
| Episodic stream | One append-only stream (for example JSONL, one file per period) | Time-stamped events and conversation records, each with provenance and a reality class | What was observed or stated, at the time it was recorded | Append only. A correction is a new entry that points at the old one. |
| Notebook | Notes keyed by stable ID | Working knowledge: semantic notes, procedures, reflections, concept-map nodes, dream and imagination entries, research hypotheses, open questions | Ella-authored. Each note carries a reality class and an epistemic status (`established` or `hypothesis`). | Edit with history. Promotion from hypothesis to established needs cited evidence. Promotion into Core needs owner approval. |
| People files | One file per person, keyed by a stable person ID | Who a person is to Ella and the owner, how to address them, consent and privacy limits, a relationship summary | Owner-stated facts outrank Ella's inferences | One person ID per human. Records are never merged on name similarity. A merge is an explicit, recorded resolution. |

## Where the architecture's categories belong

The architecture documents name more categories than four. Each one is a logical category stored inside one of the four
stores, or a derived view. None gets its own authoritative store.

| Category (architecture docs) | Authoritative home | Derived views allowed |
|---|---|---|
| Semantic ("what is true") | Notebook notes with `status: established` and evidence. Owner-approved facts about the owner go in Core. | Search index, embeddings |
| Procedural ("how to do things") | Notebook, as procedure notes | Index |
| Autobiographical ("who she is", life story, milestones) | Core holds approved identity pointers. The narrative is a Notebook reflection built from cited Episodic entries. | Timeline view |
| Emotional (moments indexed by feeling) | Affect tags on Episodic entries (`affect` field) | Feeling-keyed index |
| Reflection | Notebook, as reflection notes citing Episodic IDs | — |
| Concept map / `04_MAP` concept graph | Notebook, one note per concept, with typed links | Graph index, hub and orphan reports |
| Dreams / dream journal (`08_DREAMS`) | Notebook entries with `reality: dream`. They are never Episodic events. | — |
| Imagination / counterfactuals (`09_IMAGINATION`) | Notebook entries with `reality: imagined` | — |
| Simulated body or mood state (`06_BODY`, `05_EMOTION` live state) | Not memory. This is runtime simulation state. If a snapshot is worth keeping, it becomes an Episodic entry with `reality: simulated`. | — |
| Social memory, `user_map`, people | People files | People index |
| Bond: story, rituals, promises (`14_BOND`) | Promises and preferences that were approved go in Core. Shared moments go in Episodic. Bond summaries are Notebook reflections. | — |
| Working memory | Session scratch. Not persisted as memory. | — |
| Diary (native AdaOS plan) | This is the Episodic stream. Keep one stream, not two. | — |

## Required distinctions

| Distinction | Rule in this contract |
|---|---|
| Logical category vs physical store | A category is a field value (`kind`, `reality`, `status`) on a record. It is not a new folder or database. |
| Authoritative record vs derived index | Only the four stores are authoritative. An index entry records `derived_from.source_id` and `derived_from.source_sha256`. If the source hash changed, the index entry is stale and is never preferred over the source. |
| Personal memory vs task/job state | Task and agent state lives in Ella-Brain (`get`/`mutate`, closed schema). It is not copied into memory. Memory may cite a task ID. |
| Historical authorization receipt vs current authorization | An approval stored in memory is history. It records action, target, payload hash, expiry and environment binding. It never authorizes a new action. Current authority comes only from a fresh grant in the current session. |
| Simulated state vs observed input | `reality: simulated` records are described as model state. They are never described as measured human physiology. |
| Research hypothesis vs established fact | `status: hypothesis` notes stay hypotheses until evidence is cited and the promotion is recorded. |
| Synthetic example vs real user history | `reality: synthetic` records (including all fixtures in this pack and the Phase 0 dataset) are never retrieved as things that happened. |

## Mismatch with existing structure, and the proposed adapter

Existing documents describe a different physical layout (architecture map v0.1 `03_MEMORY/episodic/`, `semantic/`,
`procedural/`, `autobiographical/`, `emotional_memories.md`; the backup job snapshots `memory/`, `diary/`, and the second-environment plan
names `~/MEMORY.md` and `~/memory/`). None of these layouts has code behind it in either repository.

Proposed adapter, kept separate from any migration:

1. Treat the v0.1 folders as views. A loader could read a v0.1 folder and emit records into the four-store shape with
   `kind` and `reality` set from the folder name. It would emit records only and never write back.
2. Treat `diary/` as the Episodic stream. If a separate `memory/` log also exists on the live machine, keep both untouched
   and register both as sources in the manifest until the owner picks one (see `DECISIONS.md` D2).
3. Any physical migration is a separate, owner-approved change with its own dry run and backup. This lane does not do it.
