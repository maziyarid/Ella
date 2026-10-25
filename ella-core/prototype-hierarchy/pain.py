"""Phase 1 — pain-signal schema + severity tiers.

Tiers:
  info     -> log only. No routing, no interruption. (e.g. low confidence note)
  degraded -> route to the DIRECT manager. The manager MUST resolve locally
              (re-scope the question / retry the worker). It may NOT escalate
              further unless local attempts are exhausted — then it re-emits
              the signal as blocked.
  blocked  -> route up the chain. Each level attempts ONE local resolution,
              then escalates. The CEO only ever sees blocked-unresolved.

Timeouts: a worker LLM call that exceeds WORKER_TIMEOUT_S raises WorkerTimeout,
which the orchestrator converts into a blocked pain signal automatically.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json

SEVERITIES = ("info", "degraded", "blocked")

TIER_HANDLING = {
    "info": "log only — no routing, no interruption",
    "degraded": ("route to direct manager; manager MUST resolve locally "
                 "(re-scope / retry); escalate only if local attempts exhausted, "
                 "re-emitted as blocked"),
    "blocked": ("route up the chain; each level attempts one local resolution, "
                "then escalates; CEO sees only blocked-unresolved"),
}

WORKER_TIMEOUT_S = 40


@dataclass
class PainSignal:
    frm: str
    to: str
    severity: str
    what_happened: str
    tried_locally: list = field(default_factory=list)
    needed_from_above: str = ""
    ts: str = ""

    def __post_init__(self):
        assert self.severity in SEVERITIES, f"bad severity: {self.severity}"
        if not self.ts:
            self.ts = datetime.now(timezone.utc).strftime("%H:%M:%S")

    def to_json(self) -> str:
        d = asdict(self)
        d["type"] = "PAIN_SIGNAL"
        d["version"] = "1"
        return json.dumps(d, ensure_ascii=False)
