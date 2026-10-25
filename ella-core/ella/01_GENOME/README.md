# 01_GENOME — Deep traits and limits

**Duty (v0.1 spec):** Deep traits and limits. Versioned trait dials (base value, range, plasticity rate), temperament, cognitive style, values, expression style, inheritance rules, mutation log.

**Load rule:** ALWAYS (summary) / ON-DEMAND (detail) · **Change cadence:** Monthly, user-gated

**Hierarchy role:** this cluster is supervised by its cluster supervisor
(see `SUPERVISOR.md` in this directory) — a Phase 1 supervisor role card
specialised for the cluster's purpose. The supervisor answers to the Governor
(`00_KERNEL/GOVERNOR.md`); workers under it signal pain upward per
`ella/lib/pain.py` tiers. Shared prototype libraries are wired at `ella/lib/`
(symlinks into `prototype-hierarchy/` — imported, never duplicated).

**Status:** structural stub (Phase 2). Full file materialization follows the
v0.1 build order; this tree establishes the hierarchy, not the content.
