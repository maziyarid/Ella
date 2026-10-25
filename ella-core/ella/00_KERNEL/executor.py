"""Phase 2 — Executor: the orchestrator loop (assign -> monitor -> escalate-or-complete).

From the architecture map: the Executor "performs only the authorized, typed
operation and returns a receipt." It is the muscle; the Governor is the
judgment. The Executor never invents direction — it runs the loop the
Governor authorized.

Prototype mapping: Executor == the Phase 1 orchestrator loop
(prototype-hierarchy/orchestrator.py): parallel leaf assignment, monitoring
with timeout conversion to pain signals, tiered escalation, aggregation back
up. Imported, not duplicated: this module loads the Phase 1 orchestrator as
a library and re-exports its loop primitives under Executor names.
"""
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_LIB = os.path.join(_HERE, "..", "lib")
_PROTO = os.path.abspath(os.path.join(_HERE, "..", "..", "prototype-hierarchy"))
for _p in (_LIB, _PROTO):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_spec = importlib.util.spec_from_file_location(
    "phase1_orchestrator", os.path.join(_PROTO, "orchestrator.py"))
_phase1 = importlib.util.module_from_spec(_spec)
sys.modules["phase1_orchestrator"] = _phase1
_spec.loader.exec_module(_phase1)

# Loop primitives, re-exported (import, don't duplicate).
assign = _phase1.run_worker          # assign a leaf question to a worker cell
monitor = _phase1.cell_call          # one monitored LLM call for any cell
signal_pain = _phase1.emit_pain      # structured escalation (pain.py tiers)
parse = _phase1.parse_fields         # robust KEY: value parsing
load_context = _phase1.load_context  # shared grounding document
WORKER_TIMEOUT_S = _phase1.WORKER_TIMEOUT_S
WorkerTimeout = _phase1.WorkerTimeout

# Shared run state (single Executor per process, like the prototype).
TRACE = _phase1.TRACE
CALLS = _phase1.CALLS
PAIN_COUNT = _phase1.PAIN_COUNT


def receipt(operation: str, ok: bool, detail: str = "") -> dict:
    """Typed operation receipt — the Executor's only output contract."""
    return {"operation": operation, "ok": ok, "detail": detail}
