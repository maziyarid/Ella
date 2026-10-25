# 05_EMOTION — Layered emotional intelligence

**Duty (v0.1 spec):** Layered emotional intelligence. Core affect to discrete emotions to moods to sentiments; appraisal rules; regulation strategies; empathy protocol; attachment and bonds.

**Load rule:** ALWAYS (mood_state) / ON-DEMAND · **Change cadence:** Every turn (live state) / weekly (rules)

**Hierarchy role:** this cluster is supervised by its cluster supervisor
(see `SUPERVISOR.md` in this directory) — a Phase 1 supervisor role card
specialised for the cluster's purpose. The supervisor answers to the Governor
(`00_KERNEL/GOVERNOR.md`); workers under it signal pain upward per
`ella/lib/pain.py` tiers. Shared prototype libraries are wired at `ella/lib/`
(symlinks into `prototype-hierarchy/` — imported, never duplicated).

**Status:** structural stub (Phase 2). Full file materialization follows the
v0.1 build order; this tree establishes the hierarchy, not the content.
