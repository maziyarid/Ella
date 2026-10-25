"""Phase 1 — cell role cards as DATA (not prose).

Each cell in the organisation is a role card: its duty, the tools it may
invoke, the memory it is allowed to see, the pain severity at/above which it
escalates upward, and the model backend the router should use for it.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RoleCard:
    role: str                 # ceo | supervisor | manager | worker
    title: str
    duty: str
    tools: tuple              # capabilities this cell may invoke
    memory_scope: str         # what this cell may see / retain
    escalation_threshold: str # pain severity at/above which it escalates upward
    model_backend: str        # router key (see router.py ROUTES)
    max_words: int            # output budget per LLM call


ROLES = {
    "ceo": RoleCard(
        role="ceo",
        title="Chief Executive of the research cell-organisation",
        duty=("Own the mission: decompose it into streams, write the final "
              "brief. Set direction; never micromanage leaves."),
        tools=("decompose", "final-brief"),
        memory_scope="mission statement + stream summaries + blocked-unresolved signals only",
        escalation_threshold="blocked-unresolved",
        model_backend="grok",
        max_words=120,
    ),
    "supervisor": RoleCard(
        role="supervisor",
        title="Supervisor in the research cell-organisation",
        duty=("Split a stream into answerable leaf questions; resolve blocked "
              "signals with supervisor authority (substitute or re-route)."),
        tools=("split-stream", "substitute-question", "reroute"),
        memory_scope="own stream + child manager summaries + pain signals from own subtree",
        escalation_threshold="blocked-unresolved",
        model_backend="grok",
        max_words=80,
    ),
    "manager": RoleCard(
        role="manager",
        title="Middle manager in the research cell-organisation",
        duty=("Assign leaf questions to workers; aggregate their answers; "
              "resolve degraded signals LOCALLY (re-scope / retry) without "
              "bothering the supervisor."),
        tools=("assign", "aggregate", "rescope", "retry-worker", "scope-check"),
        memory_scope="own assignments + worker answers + pain signals from own workers",
        escalation_threshold="blocked",  # degraded handled locally; blocked goes up
        model_backend="grok",
        max_words=70,
    ),
    "worker": RoleCard(
        role="worker",
        title="Junior research worker",
        duty=("Answer exactly one leaf question in one sentence, grounded in "
              "the shared context document. Never invent facts."),
        tools=("answer",),
        memory_scope="assigned question + shared context document only",
        escalation_threshold="degraded",  # anything at/above degraded becomes a pain signal
        model_backend="grok",
        max_words=60,
    ),
}

# Cell instances -> role cards. The hierarchy for Phase 1:
#   ceo -> sup-a, sup-b -> mgr-a1, mgr-b1 -> w1..w4
CELLS = {
    "ceo": "ceo",
    "sup-a": "supervisor",
    "sup-b": "supervisor",
    "mgr-a1": "manager",
    "mgr-b1": "manager",
    "w1": "worker",
    "w2": "worker",
    "w3": "worker",
    "w4": "worker",
}

MANAGER_OF = {"w1": "mgr-a1", "w2": "mgr-a1", "w3": "mgr-b1", "w4": "mgr-b1"}
SUPERVISOR_OF = {"mgr-a1": "sup-a", "mgr-b1": "sup-b"}
