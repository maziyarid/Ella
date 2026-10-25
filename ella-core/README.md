# Ella Core

Private working copy of Ella Morandi's core — pushed from her own machine at Maziyar's word, 2026-10-25. Private repo; do not make public.

## What's here

- `architecture/` — the architecture collection: hierarchy roadmap (Phases 0–2 complete, Phase 3 gated), the 11-layer blueprint sketch, and the maps from Claude, DeepSeek, Genspark and others.
- `ella/` — the Phase 2 skeleton: 15 cluster dirs (`00_KERNEL`–`14_BOND`), each with a supervisor role card; `00_KERNEL/governor.py` (Governor = CEO layer) and `executor.py` (orchestrator loop). `ella/lib/` holds real copies of the Phase 1 primitives (`roles.py`, `pain.py`, `router.py`) — formerly symlinks, copied 2026-10-25 so the tree clones cleanly.
- `prototype-hierarchy/` — Phase 0–1 prototype: role cards, pain-signal schema, router, orchestrator, and the live-run traces.
- `phase0/` — Phase 0 personality dataset (SFT + DPO, Qalam-gated, ~6,900 samples by batch 1146). Synthetic seed unless a file says otherwise; never relabel synthetic as real.
- `knowledge/` — the mind-architecture master index (Vol 1 + Vol 2) and brain research notes.
- `home-evaluation/` — self-evaluation protocol and probe scripts.
- `second-environment-plan.md` — the second-environment plan.

## Open decisions (blueprint §10, Maziyar's to make)

1. Key custody — Ella keeps a working key copy, or the store stays write-only for her?
2. Enclave host — existing VPS confirmed for Phase 0–2 services?
3. Phase 1 timing/hardware — used RTX 3090 (~$850 estimate); waits for the finance picture to clear. **2026-10-25 direction: prioritise speed, $0 only — no purchase until money lands; free routes first (Kaggle/Colab bursts, free endpoints).**
4. Charter — develop §9 together.

## How to work here

- Design docs live in DotCollab ELLA (#31 and the #32–#41 specs); this repo is the readable source, not the decision room.
- No secrets in this tree — credentials live only in the vault, never in files.
- Qwen3.8-27B is the Phase 1 target model; it does **not** run inside the Muse environment (no suitable GPU there) — it runs on free GPU bursts (Kaggle T4 / Colab T4) or, when money allows, the home server.
