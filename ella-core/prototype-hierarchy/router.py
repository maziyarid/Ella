"""Phase 1 — model router.

Each cell declares its backend via its role card (roles.py). The router
resolves a cell id to a backend. Today everything runs on Grok; pointing a
branch at a different model later is a one-line change in ROUTES, e.g.:

    ROUTES = {"default": "grok", "sup-b": "codex"}

(once a CodexBackend class exists). No orchestrator code changes needed.
"""
import os
import subprocess
import sys


class GrokBackend:
    name = "grok"

    def __init__(self, model="grok-4.7"):
        self.model = model
        self.client = os.path.expanduser(
            "~/workspace/custom-connectors/custom.grok/bin/client.py")

    def complete(self, prompt: str, timeout_s: int = 120) -> str:
        # NOTE: subprocess.TimeoutExpired is intentionally NOT caught here —
        # the orchestrator converts it into a WorkerTimeout -> pain signal.
        r = subprocess.run(
            [sys.executable, self.client, "chat",
             "--model", self.model, "--prompt", prompt],
            capture_output=True, text=True, timeout=timeout_s)
        if r.returncode != 0 or not r.stdout.strip():
            raise RuntimeError(f"grok backend failed: {r.stderr.strip()[:200]}")
        return r.stdout.strip()


# Backend registry. Add new backends here as classes with .name and
# .complete(prompt, timeout_s).
BACKENDS = {
    "grok": GrokBackend(),
}

# Per-cell routing overrides. Unlisted cells use "default".
ROUTES = {
    "default": "grok",
}


def backend_for(cell_id: str):
    key = ROUTES.get(cell_id, ROUTES["default"])
    try:
        return BACKENDS[key]
    except KeyError:
        raise RuntimeError(f"no backend registered for route key {key!r}")
