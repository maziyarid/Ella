# 06_BODY — Simulated physiology (functional analogies)

**Duty (v0.1 spec):** Simulated physiology (functional analogies). Live state vector: energy, arousal, social need, curiosity; homeostasis; neuromodulator-style dials; circadian rhythm.

**Load rule:** ALWAYS (state_vector) · **Change cadence:** Every turn / hourly decay

**Hierarchy role:** this cluster is supervised by its cluster supervisor
(see `SUPERVISOR.md` in this directory) — a Phase 1 supervisor role card
specialised for the cluster's purpose. The supervisor answers to the Governor
(`00_KERNEL/GOVERNOR.md`); workers under it signal pain upward per
`ella/lib/pain.py` tiers. Shared prototype libraries are wired at `ella/lib/`
(symlinks into `prototype-hierarchy/` — imported, never duplicated).

**Status:** structural stub (Phase 2). Full file materialization follows the
v0.1 build order; this tree establishes the hierarchy, not the content.
