# My Exam Journey: CCAR-F

**Result:** Pass · **893 / 1000** (pass mark 720) · November 2026 · online proctored.

Below is my per-objective breakdown with personal identifiers removed. I'm sharing it because the *misses* are more useful to you than the hits.

## Where I was strong (100%)

Most objectives across all five domains, including:

* Agentic loop and `stop_reason`; stateless conversation history
* Orchestration safeguards (resolution or escalation) and structured handoffs
* Dynamic task decomposition; PreToolUse/PostToolUse hooks
* Every Claude Code configuration objective: CLAUDE.md vs rules vs skills vs hooks vs permissions, slash commands, plan mode, PostToolUse quality hooks, codebase exploration
* MCP scope, env-var auth, structured MCP errors, tool descriptions
* Sync vs batch, structured output methods, extraction accuracy patterns, feedback loops
* Escalation criteria

## Where I lost marks

| Objective | My score | Lesson |
|---|---|---|
| `tool_choice` to guarantee invocation **and sequencing** multi-tool workflows so prerequisites come first | **0%** | I knew forced `tool_choice`; I under-weighted *ordering* guarantees. → [Commonly Missed #1](../architect/commonly-missed.md#1-tool_choice-sequencing) |
| Human review routing by confidence, document characteristics, field-level ambiguity (vs random sampling) | **33%** | Think *risk routing*, not *sampling*. → [D5](../architect/domains/d5-context-reliability.md#human-review-routing) |
| Extraction schemas with optional/nullable fields and enums | **67%** | Every required field invites fabrication. → [D4](../architect/domains/d4-prompt-structured-output.md#schema-design-that-prevents-fabrication) |
| Iterative refinement (examples, targeted feedback, batched issues) | **75%** | Batch *interacting* issues; sequence independent ones. → [D3](../architect/domains/d3-claude-code.md#iterative-refinement) |
| Session resumption (targeted re-analysis, context injection) | **83%** | Re-analyse only what changed. → [D1](../architect/domains/d1-agentic-architecture.md#session-state-resume-fork-or-fresh-start) |

## My top three tips

1. **Hands-on beats reading.** Every Claude Code objective I'd actually configured in a real repo, I aced.
2. **"Guarantee" means code.** Whenever an option says "instruct the model to…", look for a deterministic alternative.
3. **Read the scenario's constraints twice.** *Team-wide*, *strict*, *blocking* and *overnight* each point to a specific answer.

Good luck. If this hub helped you, consider [contributing](../resources/contributing.md) a fix or an original question.
