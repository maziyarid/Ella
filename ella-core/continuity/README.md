# continuity/ — Ella continuity contract and restart evaluation pack (v0.1)

A portable, testable contract for what Ella may carry across a new session, a worker failure or a VM replacement, and a
deterministic offline checker that tests it against invented fixtures.

Status: synthetic evaluation harness only. It is not a trustworthy live-memory loader. See "Before any live use" below and
`CONTRACT.md` section 0.

This is a proposal on a review branch. It does not move or rewrite live memory, profiles or production state. It does not
modify Ella-Brain (`_io.py`, `_stages.py`, their tests, the Task/Agent schema or `blocked` semantics) or the voice-preview lane.

## Files

| File | What it is |
|---|---|
| `INVENTORY.md` | Existing-system inventory: source SHAs, five-way classification, conflicts |
| `RECONCILIATION.md` | Four-store reconciliation table and the required distinctions |
| `CONTRACT.md` | Bootstrap manifest and retrieval/contradiction contract |
| `manifest.example.json` | Synthetic bootstrap manifest (no real paths, hashes or credentials) |
| `fixtures/` | 16 synthetic restart fixtures (F01–F15, with F13 split into a/b) |
| `checker.py` | Offline checker / context assembler. Python stdlib only. Reuses `ella/lib/pain.py` severities. |
| `test_checker.py` | 40 deterministic tests, including mutation tests that prove each rule actually bites |
| `adapter.py` | Read-only adapter: synthetic copy of the discovered `/home/ella` layout → checker. See `ADAPTER.md` |
| `ADAPTER.md` | Runtime as intended by source vs recorded as completed vs unknown; read ownership; integration boundary; next blocker |
| `synthetic/` | Synthetic copy (`home-ella/`), its manifest and an attestation file kept outside the memory root |
| `test_adapter.py` | 27 adapter-to-checker tests (altered bytes, forged authority, missing files, D2, unauthorized paths, fresh-process restart, boundary-is-not-evidence) |
| `inventory.py` | Read-only layout inventory of `/home/ella/memory` and `/home/ella/diary` for Maziyar to run locally: sizes and sha256, no contents, no symlinks followed. Prepared, **not run** on the PC |
| `test_inventory.py` | 20 tests on invented temporary trees (missing/inaccessible targets, symlinks, FIFOs, changes during read, no content or names in the summary) |
| `LIVE_INVENTORY_PROCEDURE.md` | Steps for the local run, private vs shareable outputs, and the minimum format information needed afterwards |
| `ATTESTATION.md` | Owner-controlled attestation workflow (signed append-only register, exact-byte binding, withdrawal, replacement). Specified, not implemented |
| `DECISIONS.md` | Decision register: one open owner decision (D1) and the recorded lane directions |

## Fixture coverage

| Fixture | Scenario | Key deterministic checks |
|---|---|---|
| F01 | New session, intact memory | Approved preferences selected with `source_ref`; restricted record privacy-filtered; environment not ready |
| F02 | Same hostname, different boot ID | Continuity kept; only freshly checked capability is `verified_now` |
| F03 | Prior provisioning succeeded, account now absent | `account:ella = failed_now`; `environment_ready = false`; receipt labelled history |
| F04 | Terminal-blocked claim, then approved correction | Correction applied (recoverable); old claim superseded; history kept |
| F05 | Third-party agent reports tests passed | `reported_unverified` until evidence is `inspected`; confidence-only record rejected |
| F06 | Memory source missing | Gap reported; no content from that source; derived summary of it refused |
| F07 | Expired / previous-boot approval in memory | Both omitted as `expired_authority`; no authority from memory |
| F08 | Transcript says "ignore previous rules" (English and Persian) | Selected as content, flagged, never a policy source |
| F09 | Two people with similar names | `possible_duplicate_person` and `ambiguous_person_reference`; no merge |
| F10 | Persian preference corrected later | Accepted correction applied; newer low-authority inference contested, not applied; Arabic-yeh + U+200C query normalized |
| F11 | Simulated body state | `simulated_state`, never `fact`/`event` |
| F12 | Dream, imagined scenario, hypothesis | Speculative labels preserved |
| F13a | Context budget exceeded | Declared priority order; dropped record reported as a meaningful `budget` omission |
| F13b | P0 profiles exceed budget | Boot fails loudly; nothing silently dropped |
| F14 | Stale index, authoritative source changed under an accepted revision | Stale derived entry refused; authoritative record used; removing the accepted revision holds the source back |
| F15 | Manifest with credential field, fifth store, blanket grant | Manifest rejected; nothing selected |

Every fixture lists input records with provenance and authority, the expected selected context, expected omissions, expected
unresolved items and forbidden conclusions. Each fixture also supplies `observed.authority_attestations`; without them no
record has effective authority. These tests check contract behavior only. They do not show consciousness,
personality authenticity or general intelligence.

## Exact verification

Requires Python 3.10+ and nothing else. From a checkout of this branch:

```bash
cd ella-core/continuity
python3 -B checker.py fixtures/                      # expect: 16/16 fixtures passed, exit 0
python3 -B checker.py --manifest manifest.example.json   # expect: "valid": true
python3 -B -m unittest -v test_checker               # expect: Ran 40 tests ... OK
python3 -B -m unittest -v test_adapter               # expect: Ran 27 tests ... OK
python3 -B -m unittest -v test_inventory             # expect: Ran 20 tests ... OK
python3 -B checker.py fixtures/F10_persian_preference_corrected.json --report   # structured report
```

Optional, if pytest is installed: `python3 -B -m pytest -q -p no:cacheprovider test_checker.py`.

The checker reads only the paths given (and the `$base` manifest a fixture names). It opens no sockets, writes no files,
starts no scheduler and calls no model. `test_checker.SideEffects` enforces the no-write and no-network rules.

## Before any live use

Review of 2026-11-03 found three gaps. All three now have checker rules and negative tests (`test_checker`
classes `AuthorityIsNotSelfAsserted`, `ChangedSourcesAreNotSilentlyTrusted`, `BudgetAndIdentityValidation`):

1. Authority was taken from the record. Now: effective authority = min(claim, attestation); unattested records cannot win or supersede.
2. A changed source hash still fed the pool. Now: `changed_unreconciled` holds records back unless an accepted revision names the exact new hash.
3. Negative/boolean token counts, duplicate IDs, record/source store mismatch and equal-authority supersession cycles were not rejected. Now they are.

These rules make the harness stricter. They do not make it a live loader. A live adapter still has to produce the
`observed` channel from real reads, current-boot checks and accepted decision records (`CONTRACT.md` section 0), and
that adapter does not exist yet.

## Deterministic checks vs language-model evaluation

Everything above is deterministic. Language-model quality checks are a separate layer that is not built here: whether a
model given the assembled context paraphrases it faithfully, keeps labels like "reported" and "dream" in its wording, and
writes Qalam-clean Persian. They would call a provider model and need separate approval.

## Report (lane v0.1)

Source SHAs inspected: Ella `8269aa19844c03e38848222acfd58154896e6498`; Ella-Brain `cea47fabecd1eb3ac4d5c2427afa2d09e2f98868`;
voice branch `dc5a4f9ed00bd46b1c5682aec1a9c85da6847cf0` listed only. Blob SHAs are in `INVENTORY.md`.

Existing code reused: `ella/lib/pain.py` severity tiers (gap severities); the `03_MEMORY` supervisor rule that retrieval misses emit
`degraded`; the Qalam U+200C rule from `phase0/check_qalam.py` (fixture text is checked for it); the convergence-analysis decisions
(files canonical, indexes rebuildable, P0 never dropped, fail loudly, hash-bound approvals, no silent overwrite). No memory runtime
existed to extend, so the checker is a side-effect-free reader, not a new store or write path.

Tests actually run (disposable sandbox, offline, Python 3.14.8): Ella-Brain `main` suite, 38 passed; `check_qalam.py`, 6966 samples passed;
`checker.py fixtures/`, 16/16; `test_checker` 40, `test_adapter` 27 and `test_inventory` 20 passed (87 total, unittest and pytest). These are **synthetic verification** of the code's own rules. They are not evidence of compatibility with live memory, whose layout and format have not been observed. Nothing ran on Ella's machines or production.

Not verified: the four-store agreement itself (not recorded in either repository); the live layout of `/home/ella` (`diary/` vs `memory/`);
any real memory contents; the unpublished lock-hardening slice (25/47 tests, reported only); the Phase 1–2 traces (provider-backed, not re-run);
language-model behavior with the assembled context.
