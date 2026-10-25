# ella/ — the Ella Core skeleton with a working hierarchy (Phase 2)

The v0.1 cluster tree (`00_KERNEL`–`14_BOND`, per
`architecture/genspark-architecture-map-v01-2026-10-22.md`) with the Phase 1
hierarchy prototype integrated as its operating machinery.

## Layout

```
ella/
├── README.md                  (this file)
├── TRACE-phase2-2026-10-22.md (smoke-test trace)
├── lib/                       (shared prototype libraries — symlinks,
│                               imported not duplicated)
│   ├── roles.py  -> ../../prototype-hierarchy/roles.py
│   ├── pain.py   -> ../../prototype-hierarchy/pain.py
│   └── router.py -> ../../prototype-hierarchy/router.py
├── 00_KERNEL/
│   ├── README.md              (cluster duty stub)
│   ├── SUPERVISOR.md          (00_KERNEL's supervisor card)
│   ├── GOVERNOR.md            (the integration map — read this first)
│   ├── governor.py            (Governor = CEO layer)
│   ├── executor.py            (Executor = orchestrator loop)
│   ├── supervisors.py         (15 cluster supervisor cards as data)
│   ├── smoke_test.py          (Phase 2 smoke test)
│   └── smoke_context.md       (grounding doc for the smoke test)
├── 01_GENOME/ … 14_BOND/      (README.md duty stub + SUPERVISOR.md each)
```

## The integration in one paragraph

The **Governor** (`00_KERNEL/governor.py`) is the CEO layer: it takes the
Will (a mission), passes a policy gate, and decomposes it into
supervisor-owned streams — direction without micromanagement. The 15
**cluster supervisors** (`00_KERNEL/supervisors.py`, one per v0.1 cluster)
split streams into leaf questions and resolve blocked pain with supervisor
authority. The **Executor** (`00_KERNEL/executor.py`) runs the Phase 1
orchestrator loop — assign → monitor → escalate-or-complete — and returns
typed receipts. Pain signals (`ella/lib/pain.py` tiers) are the only thing
that travels upward; the Governor sees only blocked-unresolved.

## Status

Phase 2 structural integration: **working** for Governor/Executor/
supervisors/pain/router + smoke test. Cluster file content remains stubs —
full v0.1 materialization follows the spec's build order (memory and
retrieval quality before file count).
