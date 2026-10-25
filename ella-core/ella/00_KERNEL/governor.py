"""Phase 2 — Governor: the CEO layer of the Ella Core hierarchy.

From the architecture map's strict three-tier action boundary:

    Session -> Governor -> Executor

The Governor evaluates an intent (the Will: a mission statement) against
policy — permissions, goals, budgets, identity constraints — and decomposes
it into supervisor assignments. It answers ONE question: *is this direction
authorized, and who owns each part?*

It NEVER touches leaves directly and NEVER micromanages: once a stream is
assigned to a cluster supervisor, the Governor steps back. The only thing
that travels upward is pain at or above the supervisor's escalation
threshold — and blocked-unresolved is the only severity the Governor ever
sees (see ella/lib/pain.py tiers).

Prototype mapping: Governor == the Phase 1 "ceo" role card (duty: own the
mission, decompose into streams, write the final brief; set direction, never
micromanage leaves). Imported from ella/lib/roles.py, not duplicated.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "lib"))
from roles import ROLES  # noqa: E402  (symlink -> prototype-hierarchy/roles.py)
from router import backend_for  # noqa: E402

ROLE = ROLES["ceo"]


class Governor:
    """CEO layer. One Governor per organisation; deputy/consensus for
    critical calls so it is not a single point of failure (roadmap §4)."""

    def __init__(self, mission: str):
        self.mission = mission
        self.calls = 0
        self._backend = backend_for("governor")

    def _ask(self, prompt: str, max_words: int = 120) -> str:
        self.calls += 1
        full = (f"You are {ROLE.title} in a research cell-organisation. "
                f"Duty: {ROLE.duty} Keep your answer under {max_words} words. "
                f"{prompt}")
        return self._backend.complete(full)

    def authorize(self, mission: str) -> bool:
        """Policy gate (stub, Phase 2): the mission is authorized unless it
        names a forbidden target. Phase 3 will check permissions, budgets and
        identity constraints here."""
        forbidden = ("delete", "wipe", "exfiltrate", "impersonate")
        return not any(w in mission.lower() for w in forbidden)

    def decompose(self, streams: int = 2) -> dict:
        """Split the mission into supervisor-owned streams. Returns
        {stream_id: description}. The Governor does not choose leaves."""
        if not self.authorize(self.mission):
            raise PermissionError("Governor refused the mission at the policy gate.")
        out = self._ask(
            f"Mission: {self.mission}\n"
            f"Split it into exactly {streams} work streams, each ownable by one "
            f"cluster supervisor. Reply as: STREAM-A: <one line> | STREAM-B: <one line>")
        parts = {}
        for chunk in out.replace("\n", " | ").split("|"):
            chunk = chunk.strip().rstrip("|").strip()
            if chunk.upper().startswith("STREAM-"):
                k, _, v = chunk.partition(":")
                parts[k.strip().upper()] = v.strip()
        return parts

    def brief(self, syntheses: list) -> str:
        """Write the final brief from supervisor syntheses. Direction only —
        the content was built below."""
        joined = " ".join(syntheses)
        return self._ask(
            "Write the final brief for the mission from these supervisor "
            f"syntheses (3 bullets max, 30 words each): {joined}",
            max_words=150)
