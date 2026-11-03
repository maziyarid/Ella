# Read-only continuity adapter v0.1 — runtime boundary

Inspected 2026-11-03 at Ella `8269aa1`, Ella-Brain `cea47fa`, plus Ella-Brain `hardening/combined-no-overwrite-lock-timeout`
at `d01d1f1` (Ella-Brain PR #1, listed only). Nothing was run on the AdaOS PC: SSH to it is recorded as unreachable
(`setup-adaos-native.sh`, 2026-10-24), so everything about the live machine below comes from source and recorded run notes.

## The everyday runtime: intended, recorded, unknown

No current service state and no current everyday model has been observed. The three columns below come from different
kinds of evidence and must not be merged.

| Item | Intended by `setup-adaos-native.sh` v2.1 (source) | Recorded as completed (v1 run note in the script header, 2026-10-25 12:42) | Unknown on the PC today |
|---|---|---|---|
| Machine | AdaOS (Xubuntu 26), i5-4460 (plan §2–4) | The script ran on AdaOS | Whether it is running now, and its current OS state |
| `ella` user and `/home/ella/{models,memory,diary,ella-core,backups}` (mode 700) | Step 1–2 | Steps 1–4 "OK" (the note does not list per-step detail) | Current existence, ownership, mode and contents |
| Ollama and its service | Step 3: upstream installer, then `systemctl enable ollama`. The upstream installer writes an `ollama.service` that runs as user `ollama` ([Ollama install.sh](https://raw.githubusercontent.com/ollama/ollama/main/scripts/install.sh)) | Step 3 is inside "steps 1–4 OK" | Whether the service is installed, enabled or running, and on which address |
| Models | Step 4: `qwen3:4b` as the everyday model, `qwen2.5-coder:7b` for heavier work | **`qwen2.5:7b` pulled** and the smoke test answered "Ella is here." (v1 predates the 4B switch) | Whether `qwen3:4b` or the coder model is present; which model is used day to day |
| llama.cpp fallback | Step 5: two GGUF parts, failure tolerated | **Failed** (404) and stopped the v1 run | — |
| Ella units (`ella-model`, `ella-memory`, `ella-backup` + timer) | Step 6: install all; enable the backup timer; leave `ella-model` disabled | **Not installed**: the run stopped before step 6 | Whether a later run installed them |
| v2.1 of the script | — | **No recorded run** | Whether it was ever run |
| Memory process | `ella-memory.service` is `ExecStart=/bin/sleep infinity` (a stub even if installed) | — | — |

Elsewhere in the repositories:

| Item | Evidence | What it is |
|---|---|---|
| Kernel / Phase 1 runtime | `00_KERNEL/smoke_test.py`, `lib/router.py` | Muse-side and provider-backed (`GrokBackend`). Context is a string prefix (`SHARED CONTEXT: …`) built from `smoke_context.md`. It is not the offline runtime. |
| Ella-Brain | its README | External task/agent state (`get`/`mutate`). "No internal memory." It does not own memory reads. |

## Discovered layout vs synthetic proposal

Intended by source (not observed): `setup-adaos-native.sh` step 2 creates `/home/ella/{models,memory,diary,ella-core,backups}`, owner `ella`, mode
`700`. `ella-backup.sh` tars `memory diary ella-core`. **Nothing in either repository defines what files live inside `memory/` or
`diary/`, or how they are formatted.**

Ollama behavior (upstream, not Ella code): the `ollama run` REPL keeps the invoking user's last 100 typed inputs in
`~/.ollama/history`, as plain text without timestamps, and it does not save replies ([DoubleAgent notes on Ollama](https://seanthegeek.net/doubleagent/research/ollama.html)).
If the REPL is how Ella is used, this file would be the only conversation trace the source accounts for. Whether it exists on the PC, and under which user, is unknown. It is not a diary in any case.

Synthetic copy (`synthetic/home-ella/`). Everything inside it is a **proposal** used to exercise the adapter:

| Path in copy | Role in the copy | Discovered or proposed |
|---|---|---|
| `memory/MEMORY.md` | Core. Records only inside fenced ` ```ella-record ` blocks; prose is hashed and never parsed | Directory discovered; file and format proposed |
| `diary/*.jsonl` | The single Episodic stream (D2) | Directory discovered; format proposed |
| `memory/notebook/`, `memory/people/` | Notebook and People | Proposed |
| `memory/events.log` | Legacy memory log: hashed and counted, never loaded | Stand-in for the plan's "memory log" |
| `.ollama/history` | Legacy REPL history: hashed and counted, never loaded | Real Ollama behavior, synthetic content |
| `profiles/*.md` | P0 profiles | Proposed. No DNA bundle or profile exists on disk per source |
| `models/`, `backups/`, `ella-core/` | Never read | Discovered |

## Who owns each read

| Read | Owner today | Owner with this adapter |
|---|---|---|
| `memory/`, `diary/` bytes | By source, only `ella-backup.sh` (tar, as `ella`). Its units were not installed in the recorded run; current state unknown | `adapter.py`, as a second reader, read-only. It would have to run as `ella` if `/home/ella` is mode 700 as intended. |
| Authority / decisions | No one. `00_GOVERNANCE/ELLA_DECISION_LOG.md` is 0 bytes; decisions live in DotCollab | A separate attestation file **outside** the memory root, bound to each record's `record_sha256`. A file inside the root is refused. |
| P0 profiles | No one; there are no files | `adapter.py` hashes them against the manifest; a mismatch blocks boot |
| Context selection | No one | `checker.assemble`, called by the adapter (one selection authority, no parallel loader) |
| Model weights, chat | By source intent, upstream `ollama.service` (user `ollama`); current state unknown | Unchanged. The adapter never talks to it. |

## The integration boundary

The adapter ends at `context_block`: a budget-bounded, labelled text with a hash. If the intended Ollama runtime is in place, it accepts outside
context in these ways (from the [Ollama API reference](https://raw.githubusercontent.com/ollama/ollama/main/docs/api.md)):

1. `POST 127.0.0.1:11434/api/chat` with a first message `{"role": "system", "content": context_block}`.
2. `POST /api/generate` with `"system": context_block` (this overrides the Modelfile system prompt).
3. In the REPL, `/set system <text>`. This is manual and single-line, and REPL history would then record the context as a typed input.
4. A Modelfile `SYSTEM` plus `ollama create`. This writes a new model into Ollama's store, so it is out of scope.

There is **no Ella-owned caller** that does (1) or (2) today. `ollama run` is the only interface the source names. This lane
stops at the boundary: the adapter makes no HTTP call, and (1) would be a model call that needs separate approval.

## Guarantees and how they are tested (`test_adapter.py`)

These tests run against the invented copy in `synthetic/`. They show that the adapter enforces its own rules; they say
nothing about compatibility with the real `/home/ella`, whose contents and format have not been observed.

| Guarantee | Test |
|---|---|
| Hashes come from bytes this process read (file: sha256 of bytes; directory: sha256 of sorted `relpath\0filehash` lines) | `Baseline.test_hashes_are_derived_from_bytes…` |
| A changed byte leads to `changed_unreconciled` and the source is held back | `AlteredBytes.test_altered_source_is_held_back` |
| An accepted revision does not rescue an altered record (attestation is bound to the record hash) | `AlteredBytes.test_accepted_revision_does_not_rescue…` |
| A forged `owner_approved` claim, a self-attestation field, a wrong-hash attestation, or an attestation file inside the memory root gains no authority | `ForgedAuthority.*` |
| A record cannot choose its own source or store | `ForgedAuthority.test_record_cannot_choose_its_source_or_store` |
| Missing source, attestation file or profile: reported as a gap, block or absence, with no content invented | `MissingAndUnauthorized.*` |
| Paths outside the authorized roots, `..`, absolute paths, `models/`, `backups/` and symlinks out of the copy are not read | `MissingAndUnauthorized.test_unauthorized_refs…`, `…symlink…` |
| Unregistered files are reported by name and size and never opened | `…unregistered_files…` |
| `diary/` is the only Episodic stream; anything else is refused or flagged as ambiguous; legacy logs never load | `EpisodicStream.*`, `Baseline.test_prose_and_legacy…` |
| Fresh process: identical output across two processes, no files written, no cache, new bytes seen immediately | `FreshProcessRestart.*` |
| No writes, sockets, subprocesses, renames or deletes | `SideEffects.*` |
| Output is a valid checker input | `Baseline.test_output_is_a_valid_checker_input` |
| Refuses `/home/ella` and any root without `.synthetic-copy` | `…refuses_unmarked_and_live_roots` |

Building the adapter also exposed a checker gap, which is now fixed. A slot whose only record had no attestation was still "applied". It is now
`slot_without_attested_authority` (`test_checker.AuthorityIsNotSelfAsserted.test_sole_unattested_record_in_a_slot_is_not_applied`).

## Run

```bash
cd ella-core/continuity
python3 -B adapter.py --root synthetic/home-ella --manifest synthetic/manifest.json \
  --attestations synthetic/attestations.json --topics tea date --now 2026-11-03T12:00:00Z
python3 -B -m unittest -v test_checker test_adapter test_inventory   # expect: Ran 87 tests ... OK
```

## Next concrete blocker

The contents and format of `/home/ella/memory` and `/home/ella/diary` have never been observed. SSH has been unreachable
since 2026-10-24, and no run of v2.1 is recorded, so it is not known whether these directories exist, what they hold, or
who writes them.

1. **Layout and byte identity.** `inventory.py` with `LIVE_INVENTORY_PROCEDURE.md` is ready for Maziyar to review and run
   locally. The private inventory stays on the PC; only the sanitized summary is shared, after his review.
2. **Format.** For each file family, a locally prepared description or a synthetic example (procedure §4). Real contents are
   not requested.
3. **Owner approval.** The signed register in `ATTESTATION.md`, together with a verifier that fails closed. The adapter's
   current attestation file is a boundary only (`owner_approval_evidence: none`).

Until 2 and 3 exist, every real record stays unapplied.
