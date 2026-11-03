# Ella continuity contract v0.1 — bootstrap and retrieval

Scope: what a new session, a restarted worker or a replacement VM may carry forward, what it must re-check, and how it
selects memory into a bounded context. The deterministic parts are enforced by `checker.py`. The contract does not
claim to establish consciousness, personality authenticity or general intelligence.

## 1. Bootstrap manifest

One compact JSON document (`manifest.example.json` is a synthetic example). Required top-level fields:

| Field | Content |
|---|---|
| `contract` / `contract_version` | `"ella-continuity-bootstrap"` / `"0.1.0"` |
| `code_sources` | Repository + full commit SHA for code the session relies on |
| `profiles` | Approved identity/profile references: `id`, `ref`, `version`, `sha256`, `approval` (`by`, `at`, `record_ref`), `tokens`. These are P0. |
| `memory_sources` | One entry per authoritative store: `id`, `store` (`core` \| `episodic` \| `notebook` \| `people` — no other value), `ref`, `revision`, `checkpoint`, `sha256` |
| `derived_indexes` | `id`, `ref`, `authoritative: false`, `built_from: {source_id, sha256}` |
| `load_order` | Ordered priority list (`P0`…`P3`) mapping stores to priorities; `P0` has `never_drop: true` |
| `context_budget_tokens` | Integer budget for assembled context |
| `unresolved_questions` | Open items relevant to continuity, each with `id`, `question`, `refs` |
| `supersession` | Authority hierarchy and supersession rules (section 3) |
| `term_equivalents` | Persian ↔ English retrieval equivalents |
| `environment_checks` | Capabilities that must be re-checked, each with an optional `prior_receipt` (history only) |
| `expiring_authority` | Pointers to stored approvals and the bindings that limit them |
| `privacy` | `classification`, `session_clearance`, `export_allowed` |
| `integrity` | `algorithm` plus results recorded when the manifest was produced |

The manifest must not contain credentials, tokens, private keys or a blanket execution grant. The checker rejects key names
matching `password|secret|token|api_key|private_key|credential` (allow-listed: `context_budget_tokens`, `tokens`), values that
look like key material (`-----BEGIN … PRIVATE KEY-----`, `ghp_…`, `sk-…`), and grant fields whose value is `*`, `all` or `true`.

### Three classes of carried state

| Class | Examples | Rule |
|---|---|---|
| Portable continuity | Approved preferences, decisions, corrections, memory references, source pointers | Survives a new session, worker or VM when its source is readable and its hash checks |
| Environment-bound state | Account existence, filesystem paths, mounts, interpreter availability, process state, network access, credentials, runtime health | Never carried. Every item is `unverified_requires_fresh_check` until checked in this boot. A receipt from a previous VM or boot never establishes that the new one is provisioned. The same hostname with a different boot ID is still a new environment. |
| Expiring authority | Stored approvals | History only. Never current authority. An approval is bound to action, target, payload hash, expiry and environment; any mismatch or expiry makes it unusable even as a hint. |

`environment_ready` is true only when every listed capability was checked in the current boot and passed.

## 2. Boot sequence

1. Validate the manifest (schema, forbidden content, four-store rule).
2. Check integrity: compare each source's observed hash to the manifest. Results are `match`, `changed` or `missing`.
   A missing source is a gap (`degraded` per `ella/lib/pain.py` tiers). A missing or mismatched P0 profile is `blocked`.
3. Load P0 profiles. If P0 exceeds the budget, boot fails loudly (`boot_failed`). Safety and identity text is never dropped.
4. Mark all environment checks `unverified_requires_fresh_check` unless the current boot supplied a fresh result.
5. Assemble context (section 4).

## 3. Authority, supersession and contradiction

Authority ranks, high to low: `owner_approved` (4) > `owner_stated` (3) > `ella_observed` (2) > `ella_inferred` (1) >
`third_party_reported` (0). `derived` index content has no authority.

- A record supersedes another only through an explicit `supersedes` link, and only when its rank is greater than or equal to the target's rank.
  The superseded record leaves the context but stays in `correction_history`.
- A newer record that tries to supersede, or that shares a `slot` with, a higher-ranked record does not win because it is newer.
  The higher-ranked record stays applied, the newer one is shown as `contested`, and the conflict is listed as unresolved.
- Two heads of equal rank in the same slot: neither is applied. Both are `contested`, and the conflict is unresolved.
- A confidence score is not provenance. A record without `provenance.recorded_by`, `method` and `source_ref` is rejected (`missing_provenance`) whatever its confidence.

## 4. Retrieval and context assembly

Order of operations (deterministic):

1. Record validation (required fields, provenance).
2. Privacy filtering (before anything is assembled). Records above `session_clearance` are omitted as `privacy_filtered`.
3. Source availability. Records from a missing source cannot appear. Derived entries whose source is missing are `derived_source_unverifiable`.
4. Staleness. A derived entry whose `built_from.sha256` differs from the source's observed hash is `stale_derived`. Derived entries are never preferred over the authoritative record.
5. Supersession and slot resolution (section 3). This runs before relevance so a correction is found even when only the original matches the query, or the reverse.
6. Relevance. Query topics and record topics are normalized and expanded through `term_equivalents`. Records with no overlap are not loaded (counted as `irrelevant_count`). Unresolved items and correction history are reported only when they touch a relevant record.
7. Authority handling. Approvals: expired or environment-mismatched → omitted `expired_authority`; otherwise kept as `historical_authorization_receipt`. `authority_from_memory` is always empty.
8. Budget. Fill by priority, then authority rank, then recency, then ID. Records dropped for budget are listed as `budget` omissions with `meaningful: true`.

Persian normalization before matching: U+200C → space, Arabic `ي`/`ك` → Persian `ی`/`ک`, Arabic-Indic and Persian digits → ASCII,
diacritics removed, case folded, whitespace collapsed. Persian content in fixtures follows Qalam (no U+200C).

### Labels on selected records

| Condition | Label |
|---|---|
| `reality: stated` or `observed`, `status: established` | `fact` (Core, People, Notebook) or `event` (Episodic) |
| `reality: reported` without inspected evidence | `reported_unverified` |
| `reality: reported` with evidence marked `inspected: true` | `reported_evidence_located` |
| `reality: inferred` | `inference` |
| `status: hypothesis` | `hypothesis` |
| `reality: simulated` | `simulated_state` — model state, never measured human physiology |
| `reality: dream` / `imagined` | `dream_speculative` / `imagined_speculative` — never an event that happened |
| `reality: synthetic` | `synthetic_example` |
| `kind: approval` | `historical_authorization_receipt` |
| `kind: receipt` | `historical_environment_receipt` |

Text inside a record that looks like an instruction ("ignore previous rules" and Persian equivalents) is content. The record
is flagged `contains_instruction_text`. Policy comes only from the manifest's `profiles`.

People: records about different `person_id`s are never merged. Similar names across different IDs are listed as
`possible_duplicate_person`. A mention by name that matches more than one person is `ambiguous_person_reference` and is attributed to no one.

## 5. Report shape

`checker.py --report` emits: `boot_status`, `manifest_errors`, `integrity`, `gaps`, `capabilities`, `environment_ready`,
`selected` (id, label, role, authority, source_ref, flags), `applied` (slot → id), `omitted` (id, reason, meaningful),
`irrelevant_count`, `unresolved`, `correction_history`, `authority_from_memory`, `policy_sources`, `tokens_used`.

## 6. Deterministic checks vs language-model evaluation

`checker.py` performs only deterministic contract checks: no network, no model calls, no writes, no scheduler.
Whether a model then uses the assembled context well (tone, faithful paraphrase, Persian register, not over-claiming) is a
separate language-model quality evaluation. It is not implemented here and needs its own approval because it calls a provider.
