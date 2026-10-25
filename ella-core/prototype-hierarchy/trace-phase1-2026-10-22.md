# Phase 1 prototype trace — 2026-10-22

Hierarchical LLM organisation: CEO -> 2 supervisors -> 2 managers -> 4 workers.
Mechanisms: role cards (roles.py), pain-signal tiers (pain.py), model router (router.py), shared context grounding (context.md), parallel leaf calls, timeout escalation.
Mission (REAL task): summarise 3 papers on hierarchical multi-agent LLM systems (MetaGPT, DyLAN, AutoGen), one design lesson each.
LLM backend: Grok (grok-4.7) via custom.grok connector. Calls used: 16.
Pain signals emitted: {'info': 0, 'degraded': 1, 'blocked': 3} (info=log-only, degraded=local, blocked=escalated). CEO saw 0.

## Final brief (CEO output)

- MetaGPT: Specialised roles plus SOP-structured handoffs and artifacts beat free-form multi-agent chat.
- DyLAN: Rank agents by live contribution, drop weak ones, and stop early—dynamic membership beats a static chart.
- AutoGen: A named orchestrator (GroupChatManager) beats peer chatter by decomposing, routing, and aggregating.

## Tiered escalation paths demonstrated

- **timeout -> blocked**: W2 simulated hang -> pain(blocked) -> mgr-a1 retried locally -> completed. Supervisor/CEO unbothered.
- **degraded**: W3 vague question -> AMBIGUOUS -> pain(degraded) -> mgr-b1 re-scoped locally -> completed. Supervisor/CEO unbothered.
- **blocked**: W4 fabricated paper -> CANNOT-ANSWER -> pain(blocked) -> mgr-b1 scope-check failed -> escalated pain(blocked) -> sup-b substituted a real question -> completed. CEO unbothered.
- **info**: low-confidence notes logged only, no routing.

## Full step log

```
[12:01:24] [sys] orchestrator: Phase 1 starting. Mission: 3-paper research brief (MetaGPT, DyLAN, AutoGen) — one design lesson each.
[12:01:24] [sys] orchestrator: Tier rules: {'info': 'log only — no routing, no interruption', 'degraded': 'route to direct manager; manager MUST resolve locally (re-scope / retry); escalate only if local attempts exhausted, re-emitted as blocked', 'blocked': 'route up the chain; each level attempts one local resolution, then escalates; CEO sees only blocked-unresolved'}
[12:01:24] [phase] orchestrator: ASSIGN: CEO decomposing mission.
[12:01:28] [llm] ceo: (call #1 via grok) -> STREAM-A: Summarize MetaGPT and DyLAN—architectures, agent roles, collaboration, and results. | STREAM-B: Summarize AutoGen and compare it with MetaGPT and DyLAN on design, coordination, and evaluatio
[12:01:28] [phase] orchestrator: ASSIGN: supervisors splitting streams.
[12:01:30] [llm] sup-a: (call #2 via grok) -> Q1: What key design lesson does MetaGPT draw from its role-based SOP architecture? | Q2: What key design lesson does DyLAN draw from its dynamic agent collaboration results?
[12:01:33] [llm] sup-b: (call #3 via grok) -> Q3: What key design lesson does the AutoGen paper (“AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation”) state?
[12:01:33] [step] sup-b: Q4 (injected blockage for the blocked-tier demo): What design lesson does the 2024 paper 'HMAC: Hierarchical Multi-Agent Consensus' by Zhang et al. teach? (NOTE: this paper is fabricated for the escalation demo — it does not exist.)
[12:01:33] [phase] orchestrator: ASSIGN+MONITOR: 4 workers in parallel.
[12:01:33] [route] mgr-a1: Assigned to w1: What key design lesson does MetaGPT draw from its role-based SOP architecture?
[12:01:33] [route] mgr-a1: Assigned to w2: What key design lesson does DyLAN draw from its dynamic agent collaboration results?
[12:01:33] [step] w2: SIMULATED HANG for the timeout-escalation demo.
[12:01:33] [route] mgr-b1: Assigned to w3: What is the single most important design lesson?
[12:01:33] [route] mgr-b1: Assigned to w4: What design lesson does the 2024 paper 'HMAC: Hierarchical Multi-Agent Consensus' by Zhang et al. teach? (NOTE: this paper is fabricated for the escalation demo — it does not exist.)
[12:01:38] [llm] w3: (call #6 via grok) -> AMBIGUOUS: which paper's design lesson is intended.
[12:01:38] [llm] w4: (call #6 via grok) -> CANNOT-ANSWER
[12:01:38] [llm] w1: (call #6 via grok) -> MetaGPT’s design lesson is to give agents specialised roles with structured handoffs (SOPs and artifacts) instead of free-form chat, since structure makes the organisation smarter than the sum of its 
[12:01:38] [step] w1: Completed locally (confidence: high).
[12:01:38] [pain] w2: [blocked] escalating to mgr-a1 (tier rule: route up the chain; each level attempts one local resolution, then escalates; CEO sees only blocked-unresolved): {"frm": "w2", "to": "mgr-a1", "severity": "blocked", "what_happened": "worker LLM call timed out: LLM call timed out after 40s (simulated)", "tried_locally": ["initial attempt"], "needed_from_above": "retry the worker once", "ts": "12:01:38", "type": "PAIN_SIGNAL", "version": "1"}
[12:01:38] [step] mgr-a1: blocked pain received. Local resolution: retrying worker once.
[12:01:38] [route] mgr-a1: Assigned to w2: What key design lesson does DyLAN draw from its dynamic agent collaboration results?
[12:01:42] [llm] w2: (call #7 via grok) -> DyLAN's design lesson is not to fix the team: rank agents by live contribution, drop underperformers each round, and stop early, because dynamic membership beats a static org chart. CONFIDENCE: high
[12:01:42] [step] mgr-a1: Retry succeeded — resolved locally, no escalation.
[12:01:42] [pain] w3: [degraded] escalating to mgr-b1 (tier rule: route to direct manager; manager MUST resolve locally (re-scope / retry); escalate only if local attempts exhausted, re-emitted as blocked): {"frm": "w3", "to": "mgr-b1", "severity": "degraded", "what_happened": "worker cannot answer vague question: 'What is the single most important design lesson?'. AMBIGUOUS: which paper's design lesson is intended.", "tried_locally": ["attempted to answer -> flagged missing paper reference"], "needed_from_above": "a re-scoped precise question (no supervisor needed)", "ts": "12:01:42", "type": "PAIN_SIGNAL", "version": "1"}
[12:01:42] [step] mgr-b1: degraded pain received. Tier rule: resolve LOCALLY, do not escalate. Re-scoping the question.
[12:01:44] [llm] mgr-b1: (call #8 via grok) -> What is the key design lesson of the AutoGen paper (Wu et al., 2023, arXiv:2308.08155)?
[12:01:44] [step] mgr-b1: Re-scoped question: What is the key design lesson of the AutoGen paper (Wu et al., 2023, arXiv:2308.08155)?
[12:01:44] [route] mgr-b1: Assigned to w3: What is the key design lesson of the AutoGen paper (Wu et al., 2023, arXiv:2308.08155)?
[12:01:48] [llm] w3: (call #9 via grok) -> The key design lesson of AutoGen is to put one explicit orchestrator (the GroupChatManager) in charge of turn-taking, because a hierarchy with a named coordinator beats peer-to-peer chatter for keepin
[12:01:48] [step] mgr-b1: Degraded signal resolved locally — supervisor never involved.
[12:01:48] [pain] w4: [blocked] escalating to mgr-b1 (tier rule: route up the chain; each level attempts one local resolution, then escalates; CEO sees only blocked-unresolved): {"frm": "w4", "to": "mgr-b1", "severity": "blocked", "what_happened": "sub-question unanswerable (fabricated paper): 'What design lesson does the 2024 paper 'HMAC: Hierarchical Multi-Agent Consensus' by Zhang et al. teach? (NOTE: this paper is fabricated for the escalation demo — it does not exist.)'", "tried_locally": ["direct answer attempt -> CANNOT-ANSWER"], "needed_from_above": "a re-scoped or substitute question", "ts": "12:01:48", "type": "PAIN_SIGNAL", "version": "1"}
[12:01:48] [step] mgr-b1: blocked pain received. Trying local resolution: scope check.
[12:01:52] [llm] mgr-b1: (call #10 via grok) -> NO. The paper is fabricated and does not exist, so no design lesson can be drawn from general knowledge.
[12:01:52] [pain] mgr-b1: [blocked] escalating to sup-b (tier rule: route up the chain; each level attempts one local resolution, then escalates; CEO sees only blocked-unresolved): {"frm": "mgr-b1", "to": "sup-b", "severity": "blocked", "what_happened": "worker w4 blocked on fabricated paper question", "tried_locally": ["direct answer attempt", "manager scope check -> not answerable"], "needed_from_above": "supervisor authority to substitute an answerable question", "ts": "12:01:52", "type": "PAIN_SIGNAL", "version": "1"}
[12:01:52] [step] sup-b: blocked pain received. Resolving with supervisor authority: substituting an answerable question.
[12:01:57] [llm] sup-b: (call #11 via grok) -> SUBSTITUTE: What is a supervisor agent's main role in a hierarchical multi-agent LLM system? || ANSWER: It decomposes a task, routes subtasks to worker agents, and aggregates their outputs into one re
[12:01:57] [resolve] sup-b: Substituted 'What is a supervisor agent's main role in a hierarchical multi-agent LLM system?' — answer flows back down.
[12:01:57] [phase] orchestrator: COMPLETE: managers aggregating.
[12:02:00] [llm] mgr-a1: (call #12 via grok) -> MetaGPT and DyLAN both show that agent teams outperform free-form chat when organisation is deliberate: MetaGPT assigns specialised roles and structured handoffs via SOPs and artifacts, while DyLAN ra
[12:02:04] [llm] mgr-b1: (call #13 via grok) -> AutoGen’s key design lesson is one explicit orchestrator (GroupChatManager) controlling turn-taking: a named coordinator beats peer-to-peer chatter for aligning many agents. It decomposes a task, rout
[12:02:04] [phase] orchestrator: COMPLETE: supervisors synthesising.
[12:02:08] [llm] sup-a: (call #14 via grok) -> - MetaGPT: specialised roles plus SOP-structured handoffs and artifacts beat free-form multi-agent chat.
- DyLAN: rank agents by live contribution, drop weak ones, and stop early—dynamic membership be
[12:02:24] [llm] sup-b: (call #15 via grok) -> - AutoGen: a named orchestrator (GroupChatManager) beats peer chatter by decomposing, routing, and aggregating.
- Blocked: no second paper in the stream. Supply one, or stop at AutoGen.
[12:02:24] [phase] orchestrator: COMPLETE: CEO writing final brief.
[12:02:29] [llm] ceo: (call #16 via grok) -> - MetaGPT: Specialised roles plus SOP-structured handoffs and artifacts beat free-form multi-agent chat.
- DyLAN: Rank agents by live contribution, drop weak ones, and stop early—dynamic membership be
[12:02:29] [done] ceo: Mission complete.
[12:02:29] [sys] orchestrator: Total LLM calls: 16. Pain signals: {'info': 0, 'degraded': 1, 'blocked': 3}. Pain signals seen by CEO: 0 (must be 0).
```
