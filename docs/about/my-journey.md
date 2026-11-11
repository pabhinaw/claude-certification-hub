# My Exam Journey: CCAR-F

**Result:** Pass · **893 / 1000** (pass mark 720) · November 2026 · online proctored ·
[Verify credential on Credly](https://www.credly.com/badges/b512d180-1dd7-4edb-8fb6-6251ec998635){ target="_blank" rel="noopener" }

I'm sharing my results at **topic level** because the weak spots are more useful to you than the strong ones.

!!! note "What this page does and doesn't contain"
    Exam content is confidential, and candidates agree not to share, reproduce or discuss the questions. This page contains **no exam questions or recalled scenarios**. It only describes, in my own words, the broad topic areas where my score report showed I was strong or weak, and what I've studied since.

## Where I was strong

Across all five domains, especially:

* the agent loop, guaranteed termination and structured handoffs
* hooks for policy enforcement
* everything about Claude Code configuration: where each kind of guidance belongs, commands, plan mode and quality hooks
* MCP scopes, secrets handling and tool error design
* choosing between synchronous and batch processing, and structured-output methods
* escalation decisions

## Where I lost marks

| Topic area | My result | What I learned afterwards |
|---|---|---|
| Forcing tool calls **and enforcing the order** of dependent tool calls | weakest area | Knowing `tool_choice` isn't enough: ordering needs gates in code. → [Commonly Missed #1](../architect/commonly-missed.md#1-tool_choice-sequencing) |
| Routing extractions to human reviewers | weak | Think *risk-based routing*, not random sampling. → [D5](../architect/domains/d5-context-reliability.md#human-review-routing) |
| Schema design for missing or ambiguous data | below average | Every required field invites a guess. → [D4](../architect/domains/d4-prompt-structured-output.md#schema-design-that-prevents-fabrication) |
| Iterative refinement feedback | good, not perfect | Batch issues that interact; handle independent ones in sequence. → [D3](../architect/domains/d3-claude-code.md#iterative-refinement) |
| Resuming sessions after changes | good, not perfect | Re-analyse only what changed. → [D1](../architect/domains/d1-agentic-architecture.md#session-state-resume-fork-or-fresh-start) |

## My top three tips

1. **Hands-on beats reading.** The topics I had actually configured in a real repo were the ones I found easiest.
2. **"Guarantee" means code.** Whenever an option says "instruct the model to…", look for a deterministic alternative.
3. **Read each scenario's constraints twice.** Words like *team-wide*, *strict*, *blocking* and *overnight* each point to a specific kind of answer.

Good luck. If this hub helped you, consider [contributing](../resources/contributing.md) a fix or an original question.
