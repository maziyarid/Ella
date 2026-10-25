# 00_KERNEL — Identity, boot order, manifest

**Duty (v0.1 spec):** Identity, boot order, manifest. Always loaded; small and stable. Holds the master map, boot order, identity, changelog and glossary.

**Load rule:** ALWAYS · **Change cadence:** Rarely (owner-approved edits)

**Hierarchy role:** this cluster is supervised by its cluster supervisor
(see `SUPERVISOR.md` in this directory) — a Phase 1 supervisor role card
specialised for the cluster's purpose. The supervisor answers to the Governor
(`00_KERNEL/GOVERNOR.md`); workers under it signal pain upward per
`ella/lib/pain.py` tiers. Shared prototype libraries are wired at `ella/lib/`
(symlinks into `prototype-hierarchy/` — imported, never duplicated).

**Status:** structural stub (Phase 2). Full file materialization follows the
v0.1 build order; this tree establishes the hierarchy, not the content.
