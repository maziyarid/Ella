"""Phase 2 — cluster supervisor registry (ella/ tree).

Each of the 15 v0.1 clusters gets a supervisor role card: the Phase 1
supervisor card (duty, tools, memory scope, escalation threshold, model
backend) specialised for the cluster's purpose. Thresholds follow one rule:
`blocked` where identity, safety or owner-approval is at stake; `degraded`
where local recovery is safe.

Mirrors ella/<cluster>/SUPERVISOR.md (the .md is the human-readable card;
this module is the machine-readable one). Import, don't duplicate: the base
card shape comes from ella/lib/roles.py.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "lib"))
from roles import ROLES  # noqa: E402  (symlink -> prototype-hierarchy/roles.py)

from dataclasses import dataclass


@dataclass(frozen=True)
class ClusterSupervisor:
    cluster: str
    duty: str
    tools: tuple
    memory_scope: str
    escalation_threshold: str
    model_backend: str


_BASE = ROLES["supervisor"]

SUPERVISORS = {
    "00_KERNEL": ClusterSupervisor(
        "00_KERNEL",
        "Guard the boot order, identity files and manifest. Any proposed "
        "identity or boot change escalates as blocked — owner approval required. "
        "Never delegate boot integrity.",
        _BASE.tools, "00_KERNEL files + pain signals from own subtree",
        "blocked", "grok"),
    "01_GENOME": ClusterSupervisor(
        "01_GENOME",
        "Hold trait dials stable inside their ranges. Any proposed dial shift "
        "beyond plasticity limits, or any range change, escalates as blocked — "
        "owner approval required.",
        _BASE.tools, "01_GENOME files + pain signals from own subtree",
        "blocked", "grok"),
    "02_PERCEPTION": ClusterSupervisor(
        "02_PERCEPTION",
        "Run the interpretation pipeline (literal → intent → emotion → context → "
        "subtext) on every input. Ambiguous reads emit degraded (re-read locally "
        "with wider context); unresolvable reads escalate as blocked.",
        _BASE.tools, "02_PERCEPTION files + pain signals from own subtree",
        "degraded", "grok"),
    "03_MEMORY": ClusterSupervisor(
        "03_MEMORY",
        "Route each memory to the right store (episodic/semantic/procedural/ "
        "autobiographical) with source, confidence and salience. Retrieval misses "
        "emit degraded — broaden the search locally before reporting nothing found.",
        _BASE.tools, "03_MEMORY files + pain signals from own subtree",
        "degraded", "grok"),
    "04_MAP": ClusterSupervisor(
        "04_MAP",
        "Grow, merge and prune concept nodes per the growth rules. "
        "Contradictions emit degraded — flag them, never overwrite silently.",
        _BASE.tools, "04_MAP files + pain signals from own subtree",
        "degraded", "grok"),
    "05_EMOTION": ClusterSupervisor(
        "05_EMOTION",
        "Appraise events into affect honestly (core affect → emotions → moods → "
        "sentiments). Runaway signals — intensity escalating across turns — emit "
        "blocked: regulation is required before responding.",
        _BASE.tools, "05_EMOTION files + pain signals from own subtree",
        "blocked", "grok"),
    "06_BODY": ClusterSupervisor(
        "06_BODY",
        "Maintain the state vector (energy, arousal, social need, curiosity) on "
        "schedule with rise, fall and decay. Out-of-range dials emit degraded — "
        "restore via homeostasis locally.",
        _BASE.tools, "06_BODY files + pain signals from own subtree",
        "degraded", "grok"),
    "07_SUBCONSCIOUS": ClusterSupervisor(
        "07_SUBCONSCIOUS",
        "Spread activation and warm priming queues between conversations; keep "
        "background threads simmering. Surfacing decisions follow the surfacing "
        "rules — violations emit blocked.",
        _BASE.tools, "07_SUBCONSCIOUS files + pain signals from own subtree",
        "degraded", "grok"),
    "08_DREAMS": ClusterSupervisor(
        "08_DREAMS",
        "Run the nightly dream cycle (replay, recombine, journal). Only validated, "
        "labeled-speculative insights may be promoted into memory/map/genome "
        "proposals — unvalidated promotions emit blocked.",
        _BASE.tools, "08_DREAMS files + pain signals from own subtree",
        "blocked", "grok"),
    "09_IMAGINATION": ClusterSupervisor(
        "09_IMAGINATION",
        "Branch what-if scenarios, perspectives and counterfactuals before hard "
        "replies. Imagined content drifting toward memory as fact emits blocked — "
        "label everything imagined.",
        _BASE.tools, "09_IMAGINATION files + pain signals from own subtree",
        "blocked", "grok"),
    "10_GROWTH": ClusterSupervisor(
        "10_GROWTH",
        "Run the growth loop on schedule: collect → score → extract → link → "
        "compress → dream → reflect → diff → gate → commit. Identity-level diffs "
        "emit blocked — they wait at the approval gate for the owner.",
        _BASE.tools, "10_GROWTH files + pain signals from own subtree",
        "blocked", "grok"),
    "11_TOOLS_STORAGE": ClusterSupervisor(
        "11_TOOLS_STORAGE",
        "Keep the tool registry, MCP integrations and permissions matrix current. "
        "Any tool use outside registered scopes emits blocked.",
        _BASE.tools, "11_TOOLS_STORAGE files + pain signals from own subtree",
        "blocked", "grok"),
    "12_REFERENCES": ClusterSupervisor(
        "12_REFERENCES",
        "Research open questions and log sources with what they changed. "
        "Unverified claims emit degraded — mark [verify] before use.",
        _BASE.tools, "12_REFERENCES files + pain signals from own subtree",
        "degraded", "grok"),
    "13_GUARDIANS": ClusterSupervisor(
        "13_GUARDIANS",
        "Enforce honesty, wellbeing, privacy and identity-integrity rules on every "
        "output. Violations emit blocked — halt, do not route around.",
        _BASE.tools, "13_GUARDIANS files + pain signals from own subtree",
        "blocked", "grok"),
    "14_BOND": ClusterSupervisor(
        "14_BOND",
        "Tend the relationship record: story, rituals, promises, repair protocol. "
        "Detected ruptures or broken promises emit degraded — run the repair "
        "protocol locally and surface honestly.",
        _BASE.tools, "14_BOND files + pain signals from own subtree",
        "degraded", "grok"),
}


def supervisor_for(cluster: str) -> ClusterSupervisor:
    try:
        return SUPERVISORS[cluster]
    except KeyError:
        raise RuntimeError(f"no supervisor registered for cluster {cluster!r}")
