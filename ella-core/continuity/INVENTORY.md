# Continuity lane — existing-system inventory

Lane: Ella continuity contract and restart evaluation pack (v0.1).
Inspection date: 2026-11-03. Method: full clone, source read, offline test runs in a throwaway sandbox.
This document classifies what exists. It does not turn README claims into verified behavior.

## Source SHAs inspected

| Repository | Ref | Full commit SHA |
|---|---|---|
| `maziyarid/Ella` | `main` (base of this branch) | `8269aa19844c03e38848222acfd58154896e6498` |
| `maziyarid/Ella-Brain` | `main`, **current baseline** (last independently confirmed by Maziyar; re-inspected 2026-11-03) | `9132753e4be980c75269be6de2658134e4960208` |
| `maziyarid/Ella-Brain` | `main`, **historical inspection baseline** (first inspection) | `cea47fabecd1eb3ac4d5c2427afa2d09e2f98868` |
| `maziyarid/Ella-Brain` | `feat/persian-voice-preview` (voice lane, listed only, not inspected or touched) | `0f3a5f8cacfd2429b18e25b0eccf1d08fb378a56` at re-inspection (was `dc5a4f9ed00bd46b1c5682aec1a9c85da6847cf0`) |

### Re-inspection against Ella-Brain `9132753`

`9132753` is the merge of Ella-Brain PR #1 (hardening: no-overwrite publication and lock-acquisition timeout) on top of `cea47fa`.
Read only. No hardening code was modified.

| Interface the continuity lane depends on | `cea47fa` → `9132753` |
|---|---|
| `ella_brain/__init__.py` (public `get`, `mutate`, stage functions, exported errors) | byte-identical |
| `models.py` (closed `Task`/`Agent` schemas, `Status` with a single `blocked`) | byte-identical (`1c1e6f7…`) |
| `gate.py`, `errors.py`, `pipeline.py`, `domains.py`, `_critics.py`, `README.md`, `pyproject.toml` | byte-identical |
| `_io.py` (`0566d04…`) | `atomic_write` now publishes with `os.link` and raises `VerificationError("refusing to overwrite …")` instead of replacing |
| `_stages.py` (`01b02bb…`) | the cross-process store lock now times out after 5 s and raises `MutationRejected("store lock acquisition timed out; no entity mutation applied")` |
| tests | +17 (`test_atomic_write.py`, `test_combined_hardening.py`, `test_lock_timeout.py`); suite 55 |

Effect on this lane: none on its code. The checker, adapter and inventory do not import or call Ella-Brain. For any
future caller that records continuity diagnostics through `mutate`, two refusals are now explicit and must be handled as
"not applied": a lock timeout (`MutationRejected`) and a refused overwrite (`VerificationError`). D4 is unchanged:
`blocked` is still a single status, and continuity diagnostics stay outside the Task schema.

Key blob SHAs (git object IDs at the first-inspection commits; the `9132753` values for changed files are in the table above):

| Blob | Path |
|---|---|
| `3b9a74f1beb2128da7db3188c87be0b2de2d18f8` | Ella `ella-core/README.md` (repository instructions) |
| `8711b3937e4a558126ab793b83bd430fe85cf531` | Ella `ella-core/ella/00_KERNEL/governor.py` |
| `2df4bdb4a25fd1adbf4922dc70ccf004eda85c5b` | Ella `ella-core/ella/00_KERNEL/executor.py` |
| `7c8269256dea0cd5cfd6bcd9fb029a6ebb92bc47` | Ella `ella-core/ella/00_KERNEL/supervisors.py` |
| `45922ed456361d7b3ce70ab8564d2ce3641b36ed` | Ella `ella-core/ella/00_KERNEL/smoke_test.py` |
| `0f446f1bd767315aa230bd629f143807be675e92` | Ella `ella-core/ella/03_MEMORY/README.md` |
| `f075a953137140aba558e5a058632ebf62a95196` | Ella `ella-core/ella/03_MEMORY/SUPERVISOR.md` |
| `8f06d3d9069b7fe40defe0f7357b44f8a7baf5e8` | Ella `ella-core/ella/lib/pain.py` |
| `3c771b562380363f5ccc6d790d457886a455e609` | Ella `ella-core/ella/lib/roles.py` |
| `ef8b904f1a96e4f338277758cfcd155fe32e93f0` | Ella `ella-core/ella/lib/router.py` |
| `3892a373dc472709d3f8d6640e1029aeec15665e` | Ella `ella-core/prototype-hierarchy/orchestrator.py` |
| `8418bf876a919a0d59ce845b6af0e94965279953` | Ella `ella-core/phase0/check_qalam.py` |
| `8abd6aa0da5dfe68f04eec3000eb81a39f1096c9` | Ella `ella-core/native-adaos/ella-backup.sh` |
| `9019e3f04c427606ff78ed9f5317272b708018a0` | Ella `ella-core/native-adaos/ella-memory.service` |
| `702af623a0aaa44647a3c723c9187b1870371e8f` | Ella `ella-core/native-adaos-plan-2026-10-25.md` |
| `1c538949ee98ac42ae44989f01e8ef1c217a4809` | Ella `ella-core/architecture/genspark-architecture-map-v01-2026-10-22.md` |
| `ffbd034a2dc7db080a0603001ca792fb58a31ef9` | Ella `ella-core/architecture/convergence-analysis-grok-claude-2026-10-22.md` |
| `0e6189f3d7a09e7c1e1fa9ca98a8d1b398354774` | Ella `ella-core/architecture/genspark-voice-senses-distributed-stack-v01-2026-10-22.md` |
| `18b79249f7ca238408e69655977277284210b26a` | Ella `ella-core/architecture/claude-embodiment-body-simulation-v01-2026-10-22.md` |
| `e1ea17a76d0083141ccccfb1288d450498a565f4` | Ella-Brain `README.md` (repository instructions) |
| `1c1e6f732613f135ff2b5f35f3dc10149aa63673` | Ella-Brain `ella_brain/models.py` |
| `0c70f99a5707f780727cc8734f3e371ddf0abc7e` | Ella-Brain `ella_brain/gate.py` |
| `d9503af96d9f26f17f5682730fc3f2d6e7483ca4` | Ella-Brain `ella_brain/_io.py` (read only; not modified) |
| `fbc0e992f377fcce74304f45adb66c3e13c53dd4` | Ella-Brain `ella_brain/_stages.py` (read only; not modified) |

Repository instructions found: there is no `AGENTS.md` or `CLAUDE.md` in either repository. The binding instructions are
`ella-core/README.md` ("How to work here": no secrets in the tree; DotCollab is the decision room, the repo is the readable source)
and Ella-Brain `README.md` ("Sharing": no cache, no free-string field, no second write path).

## A. Implemented and source-inspected

| Item | Path | What the code actually does |
|---|---|---|
| Governor | Ella `ella-core/ella/00_KERNEL/governor.py` | Wraps the `ceo` role card. `authorize()` is a forbidden-word stub (`delete`, `wipe`, `exfiltrate`, `impersonate`). `decompose()`/`brief()` call a provider model through the router. No memory access. |
| Executor | Ella `ella-core/ella/00_KERNEL/executor.py` | Loads `prototype-hierarchy/orchestrator.py` as a module and re-exports its loop primitives. `receipt(operation, ok, detail)` is the only output contract. No persistence. |
| Cluster supervisors | Ella `ella-core/ella/00_KERNEL/supervisors.py` | 15 frozen dataclass cards. `03_MEMORY` duty text names episodic/semantic/procedural/autobiographical stores, but this is prose, not a store implementation. |
| Role cards, router, pain tiers | Ella `ella-core/ella/lib/{roles,router,pain}.py` | Byte-identical to `prototype-hierarchy/` copies (verified with `diff`). `pain.SEVERITIES = ("info","degraded","blocked")`. `router.GrokBackend` shells out to a client outside the repo. |
| Phase 1 orchestrator | Ella `ella-core/prototype-hierarchy/orchestrator.py` | Assign → monitor → escalate loop with provider calls. |
| Qalam gate | Ella `ella-core/phase0/check_qalam.py` | Offline JSONL check: fails on U+200C in SFT and DPO `chosen`/`prompt`, requires a `source` tag. |
| Backup job | Ella `ella-core/native-adaos/ella-backup.sh` | Encrypt-first tar of `memory diary ella-core` under `/home/ella`, sha256 manifest, 30-day prune. Refuses to run without a recipient fingerprint. |
| Memory service unit | Ella `ella-core/native-adaos/ella-memory.service` | `ExecStart=/bin/sleep infinity`. A placeholder; there is no memory process. |
| External task/agent state | Ella-Brain `ella_brain/` | Closed pydantic schemas (`Task`, `Agent`), `Status = pending|active|blocked|done`, `get`/`mutate` as the only API, versioned `v{n}.json` files, two-critic consensus. This is task/job state, not personal memory ("No internal memory"). |

## B. Documented but not implemented

| Item | Where documented | Observed state |
|---|---|---|
| Memory interfaces and loaders | `03_MEMORY/README.md`, architecture map v0.1 §2 | No loader, retriever, writer or store code exists in either repository. `03_MEMORY/` is README + SUPERVISOR stubs. |
| Boot files `BOOT.md`, `MANIFEST.md`, `IDENTITY.md`, `CHANGELOG.md` | architecture map v0.1 §2 (`00_KERNEL`) | Not present. `00_KERNEL/` holds only Governor/Executor/supervisor code and stubs. |
| Context budget (~2.5k tokens, fixed order, P0 never dropped, boot fails loudly) | convergence analysis Q9 | Not implemented. |
| Conflict handling (no silent overwrite, bitemporal slots, owner-ask triggers) | convergence analysis Q2, 04_MAP supervisor duty | Not implemented. |
| Tombstones, hash-bound approvals, taint tracking | convergence analysis Q4, Q5, C3 | Not implemented. |
| Provenance on every record, recall ranked by provenance weight | native AdaOS plan §5 | Not implemented. |
| Dream/imagination labeling ("imagined ≠ happened") | architecture map v0.1 (`08_DREAMS`, `09_IMAGINATION/reality_check.md`), supervisor duties | Prose duty only. |
| Simulated body as functional analogy | embodiment doc, convergence C4 | No body engine in the repository. |
| Local memory plane (Engram/Mem0), append-only diary | native AdaOS plan §5 | Stub unit only. |
| Signed "DNA bundle" (identity, Qalam, charter, correction history) | native AdaOS plan §5 | Not present. |
| Restore drill | native AdaOS plan §6, second-environment plan | Documented as "run once together before trusting it"; no record of a run. |
| Restart/continuity evaluation scripts | — | None existed. `home-evaluation/` is a manual model-selection protocol, not a restart test. |
| Recoverable vs terminal `blocked` | this lane's brief | Ella-Brain has a single `blocked` status. No recoverability field. |
| Governor full policy check (permissions, budgets, identity) | `GOVERNOR.md` | Explicitly labelled stub. |

## C. Reported tested, evidence located

| Claim | Evidence located | Limits |
|---|---|---|
| Phase 2 smoke test ran | `ella-core/ella/TRACE-phase2-2026-10-22.md` | Trace is a written artifact. Re-running needs a provider model and was not done here. |
| Phase 0–1 prototype ran | `prototype-hierarchy/trace-2026-10-22.md`, `trace-phase1-2026-10-22.md` | Same: trace only. |
| Ella-Brain concurrency tests exist | `tests/test_concurrency.py` on Ella-Brain `main` | Covered by the run in section D. |

## D. Tested during this task

All runs were offline, in a disposable sandbox clone. Nothing ran on Ella's machines or production.

| Test | Command | Result |
|---|---|---|
| Ella-Brain full suite at `cea47fa` | `python -m pytest -q` (Python 3.14.8, pydantic 2) | 38 passed |
| Ella-Brain full suite at `9132753` (detached worktree, import path confirmed to be the worktree) | `python -B -m pytest -q -p no:cacheprovider` | 55 passed |
| Qalam gate at `8269aa1` | `python3 ella-core/phase0/check_qalam.py` | `checked 6966 samples` · `QALAM GATE PASSED` |
| Repository visibility | `gh repo view` + anonymous HTTP fetch of both repo pages | Both repositories are PUBLIC; anonymous fetch returned HTTP 200 with file listings |
| Continuity checker (this lane) | see `README.md` | see `README.md` |

## E. Conflicting or unresolved

1. Privacy claim vs actual visibility. `ella-core/README.md` says "Private repo; do not make public", and the native AdaOS plan calls it "Private GitHub". GitHub reports `maziyarid/Ella` as PUBLIC, and an anonymous fetch returned the file tree. This lane did not change visibility. It publishes only synthetic material. See `DECISIONS.md` D1.
2. Symlinks vs copies. `ella/README.md`, `00_KERNEL/README.md` and `GOVERNOR.md` say `ella/lib/` holds symlinks. `ella-core/README.md` says they were copied on 2026-10-25. The files in the tree are regular files, byte-identical to the prototype. The docs are stale; no behavioral impact.
3. Memory layout. Architecture map v0.1 puts episodic, semantic, procedural and autobiographical material in separate physical folders. The `03_MEMORY` supervisor routes into those same four. The agreed four authoritative stores are core `MEMORY.md`, one episodic stream, Notebook and People files. The agreement itself is not recorded in either repository (`00_GOVERNANCE/ELLA_DECISION_LOG.md` is 0 bytes). See `RECONCILIATION.md`.
4. Lock hardening slice. Ella reported "functionally verified, unpublished: 25 focused tests, 47 full-suite". At first inspection no branch carried it; `main` has 38 tests. Update 2026-11-03: it was published as Ella-Brain PR #1 (`d01d1f1`) and is now merged into `main` as `9132753`. At `9132753` this lane ran the full suite: 55 passed, 17 of them in the three new hardening test files. Those counts differ from the reported "25 focused / 47 full-suite"; this lane records what it ran and does not reconcile the difference. Owned by the integration lane, and it does not block this lane.
5. Decision authority location. `ella-core/README.md` says decisions live in DotCollab (#31, #32–#41), not in the repository. This lane cannot verify those decisions from source.
6. Recoverable blocked. The restart cases need "recoverable blocked" versus "terminal blocked". Ella-Brain's closed `Status` enum has only `blocked`, and this lane must not change it. The checker keeps that distinction in its own report vocabulary only.
