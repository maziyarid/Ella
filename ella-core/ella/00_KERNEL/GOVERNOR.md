# GOVERNOR — how the hierarchy maps onto the ella/ skeleton

**Phase 2 integration map.** The working Phase 1 prototype
(`prototype-hierarchy/`: roles, tiered pain signals, model router, orchestrator
loop) is now the operating machinery inside the v0.1 `ella/` cluster tree.
Nothing was duplicated: the skeleton imports the prototype as shared
libraries via `ella/lib/` (symlinks).

## Piece → piece mapping

| Prototype (Phase 0/1) | Skeleton (ella/) | Role in the organisation |
|---|---|---|
| `roles.py` → `ceo` role card | `00_KERNEL/governor.py` — **Governor** | CEO layer: direction, policy gate, decomposition. Never touches leaves. |
| `orchestrator.py` loop (assign → monitor → escalate-or-complete) | `00_KERNEL/executor.py` — **Executor** | Muscle: runs only authorized, typed operations; returns receipts. Re-exports the Phase 1 loop primitives. |
| `roles.py` → `supervisor` role card | `00_KERNEL/supervisors.py` + each cluster's `SUPERVISOR.md` | 15 cluster supervisors, one per v0.1 cluster (00_KERNEL–14_BOND), each with a duty and escalation threshold derived from the cluster's purpose. |
| `roles.py` → `manager` / `worker` cards | Instantiated per mission under a supervisor | Managers aggregate; workers answer one leaf question each. |
| `pain.py` tiers (info / degraded / blocked) | Wired through every layer | info → log only; degraded → resolve locally at the direct manager/supervisor; blocked → route up; the Governor sees only blocked-unresolved. |
| `router.py` per-cell backends | `ella/lib/router.py` (symlink) | Every cell declares its model backend; one-line swaps. All-Grok today. |
| `context.md` grounding | Per-mission context docs (e.g. `00_KERNEL/smoke_context.md`) | Workers ground answers in shared context; CANNOT-ANSWER / AMBIGUOUS protocol. |

## How a task flows

```
WILL (mission intent — the human's direction, e.g. Maziyar's order)
  │
  ▼
GOVERNOR (`00_KERNEL/governor.py`) — policy gate (authorize?)
  │  authorized? no → refuse with reason. yes → decompose into streams.
  │  (Direction only. Never micromanages.)
  ▼
CLUSTER SUPERVISORS (`00_KERNEL/supervisors.py`, one per 00–14)
  │  each splits its stream into answerable leaf questions.
  │  resolves blocked signals with supervisor authority
  │  (substitute / re-route). Reports up only what it cannot fix.
  ▼
MANAGERS → WORKERS (per-mission instances of the Phase 1 cards)
  │  workers answer one leaf question each, grounded in shared context.
  │  pain signals: info (log) / degraded (manager/supervisor fixes locally)
  │                / blocked (route up the chain)
  ▼
EXECUTOR (`00_KERNEL/executor.py`) — aggregates answers upward,
  synthesises at each level, returns the final brief + typed receipts.
  │  Every operation returns a receipt: {operation, ok, detail}.
  ▼
DONE — with a full trace. The Governor saw zero pain unless something
  was blocked-unresolved at every level below it.
```

## Design rules (from the roadmap, enforced here)

1. **No micromanagement.** The Governor assigns streams, not leaves. Supervisors
   decompose; they never do leaf work.
2. **Pain has a schema, not a scream.** Every escalation carries what happened,
   severity, what was tried locally, and exactly what is needed from above
   (`ella/lib/pain.py`).
3. **Shallow by default.** Governor → supervisor → workers is 3 levels; a
   manager layer is added only when a supervisor's fan-out demands it.
4. **The cell is role + memory + tools, not the model.** LLM calls are
   stateless; the hierarchy lives in the role cards.
5. **The Governor is not a single point of failure.** Deputy/consensus for
   critical calls (stub in Phase 2; Phase 3).

## What is stub vs working (Phase 2)

- **Working:** Governor decompose/brief/authorize-stub, Executor loop
  primitives, 15 supervisor cards, tiered pain escalation, model router,
  smoke test (`00_KERNEL/smoke_test.py`, trace at `ella/TRACE-phase2-2026-10-22.md`).
- **Stub:** cluster file content (README + SUPERVISOR only — full v0.1 file
  materialization follows the spec's build order), the Governor's full policy
  check (permissions/budgets/identity — currently a forbidden-word stub),
  deputy/consensus for the Governor, persistent memory scopes per cell.
