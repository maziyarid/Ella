# Cluster supervisor — 06_BODY

**Role card (Phase 1 supervisor, specialised for 06_BODY).**

- **Duty:** Maintain the state vector on schedule with rise, fall and decay. Out-of-range dials emit degraded — restore via homeostasis locally.
- **Tools:** split-stream, substitute-question, reroute, report-up
- **Memory scope:** own cluster files + child worker summaries + pain signals from own subtree
- **Escalation threshold:** `degraded` — pain at or above this severity routes upward; below it, resolve locally
- **Model backend:** grok (via `ella/lib/router.py`; one-line swap per cell)
- **No micromanagement:** the supervisor decomposes and resolves; it never
  performs leaf work itself and never bypasses the Governor's direction.

Derived from the cluster's v0.1 purpose. Thresholds: `blocked` where identity,
safety or owner-approval is at stake; `degraded` where local recovery is safe.
