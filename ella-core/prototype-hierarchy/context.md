# Shared context — hierarchical multi-agent LLM systems

All worker cells are grounded in this document. Answer ONLY from what is
written here plus general knowledge. If a question asks about something NOT
in this document and NOT in general knowledge, reply CANNOT-ANSWER.
If a question does not name a specific paper, reply AMBIGUOUS: <what is missing>.

## Paper 1 — MetaGPT (Hong et al., 2023, arXiv:2308.00352)

MetaGPT is a multi-agent framework that assigns GPT models human-like roles
(product manager, architect, project manager, engineer, QA engineer) and makes
them collaborate by following Standardized Operating Procedures (SOPs) —
the same structured workflows human software teams use. Agents communicate
through structured artifacts (PRDs, system designs, API specs, code) rather
than free chat, which cuts down on compounding errors. An "executable
feedback" loop lets the engineer agent run the code and fix it. On software
benchmarks it strongly outperformed single-agent and free-chat multi-agent
baselines.
DESIGN LESSON: give agents specialised roles with structured handoffs (SOPs +
artifacts) instead of free-form chat — structure is what makes the
organisation smarter than the sum of its agents.

## Paper 2 — DyLAN (Liu et al., 2023, arXiv:2310.02170)

DyLAN (Dynamic LLM-Agent Network) builds the agent team dynamically per task
instead of fixing it in advance. In each round, an LLM ranker scores every
agent's contribution (Agent Importance Score) and only the top performers
continue; an early-stopping mechanism ends collaboration once marginal gains
vanish. Final answers use a Byzantine-consensus vote over the surviving
agents. This cut token cost substantially while beating static teams on
reasoning and code benchmarks.
DESIGN LESSON: don't fix the team — rank agents by live contribution,
drop the dead weight each round, and stop early. Dynamic membership beats a
static org chart.

## Paper 3 — AutoGen (Wu et al., 2023, Microsoft, arXiv:2308.08155)

AutoGen is a framework for building LLM applications with conversable
agents: each agent can send/receive messages, call tools, execute code, and
involve humans. Its key organisational pattern is GroupChat with a
GroupChatManager — a dedicated orchestrator agent that picks the next speaker
each turn, keeping multi-agent discussion coherent. Agents are customisable
(AssistantAgent, UserProxyAgent) and the human can step in at any point.
DESIGN LESSON: put one explicit orchestrator (the GroupChatManager) in charge
of turn-taking — a hierarchy with a named coordinator beats peer-to-peer
chatter for keeping many agents aligned.
