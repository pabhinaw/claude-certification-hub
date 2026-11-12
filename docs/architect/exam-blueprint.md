# Domains & Study Checklist

Use this page as your **master checklist**. It lists the five publicly reported exam domains with their weights, then the competencies this hub teaches in each one, **written in our own words** as study goals.

!!! info "About this checklist"
    This is not a copy of Anthropic's exam guide or of any score report. The official exam guide is available to registered candidates through Anthropic's Partner Academy, and that is the authoritative source. This list is our own study map, built from public documentation and community-reported domain weights.

## Domain weights

| Domain | Weight | ≈ Share of 60 questions |
|---|---|---|
| D1 · Agentic Architecture & Orchestration | 27% | ~16 |
| D3 · Claude Code Configuration & Workflows | 20% | ~12 |
| D4 · Prompt Engineering & Structured Output | 20% | ~12 |
| D2 · Tool Design & MCP Integration | 18% | ~11 |
| D5 · Context Management & Reliability | 15% | ~9 |

Question counts are estimates based on the weights.

## Competency checklist

Tick an item only when you could **explain it to someone else and pick it out of four plausible options**.

### D1 · Agentic Architecture & Orchestration

- [ ] Run an agent loop driven by `stop_reason`, and know what each value means → [D1](domains/d1-agentic-architecture.md#the-agentic-loop)
- [ ] Explain why every API call must carry the conversation history → [Messages API](../fundamentals/messages-api.md#the-api-is-stateless-you-own-the-conversation)
- [ ] Choose between a fixed pipeline and adaptive task decomposition → [D1](domains/d1-agentic-architecture.md#task-decomposition-fixed-vs-dynamic)
- [ ] Guarantee every session ends either resolved or handed to a person → [D1](domains/d1-agentic-architecture.md#guaranteed-termination-resolution-or-escalation)
- [ ] Design handoff summaries that carry findings, actions and authorisation status → [D1](domains/d1-agentic-architecture.md#structured-handoff-packages)
- [ ] Enforce business rules with hooks instead of instructions → [D1](domains/d1-agentic-architecture.md#hooks-deterministic-policy-enforcement)
- [ ] Resume work efficiently after files have changed → [D1](domains/d1-agentic-architecture.md#session-state-resume-fork-or-fresh-start)
- [ ] Configure subagents with the Agent SDK → [Agent SDK Basics](../fundamentals/agent-sdk-basics.md)

### D2 · Tool Design & MCP Integration

- [ ] Write tool descriptions that make Claude choose the right tool → [D2](domains/d2-tool-design-mcp.md#tool-descriptions-the-1-selection-signal)
- [ ] Return tool errors that tell the agent what happened and what to do next → [D2](domains/d2-tool-design-mcp.md#structured-tool-errors)
- [ ] Use `tool_choice` to guarantee a call, and enforce the **order** of dependent calls → [D2](domains/d2-tool-design-mcp.md#tool_choice-and-tool-sequencing)
- [ ] Place MCP servers at the right scope and keep secrets out of Git → [D2](domains/d2-tool-design-mcp.md#mcp-integration)
- [ ] Know when to use MCP resources and prompts as well as tools → [D2](domains/d2-tool-design-mcp.md#mcp-tools-resources-and-prompts)

### D3 · Claude Code Configuration & Workflows

- [ ] Pick the right mechanism: CLAUDE.md, rules, commands, skills, hooks or permissions → [D3](domains/d3-claude-code.md#choosing-the-right-mechanism)
- [ ] Separate advice (CLAUDE.md) from enforcement (hooks and permissions) → [D3](domains/d3-claude-code.md#advice-vs-enforcement)
- [ ] Choose between `@` references, CLAUDE.md and inline context → [D3](domains/d3-claude-code.md#providing-context-references-vs-claudemd-vs-inline)
- [ ] Put commands and skills in the right project or personal folder → [D3](domains/d3-claude-code.md#custom-slash-commands-and-skills)
- [ ] Decide when plan mode is worth it → [D3](domains/d3-claude-code.md#plan-mode-vs-direct-execution)
- [ ] Automate formatting, linting and tests with hooks → [D3](domains/d3-claude-code.md#hooks-for-code-quality)
- [ ] Give feedback that makes iterations converge → [D3](domains/d3-claude-code.md#iterative-refinement)
- [ ] Explore a large codebase without flooding context → [D3](domains/d3-claude-code.md#exploring-a-codebase-systematically)

### D4 · Prompt Engineering & Structured Output

- [ ] Choose the most reliable way to get structured output → [D4](domains/d4-prompt-structured-output.md#choosing-a-structured-output-method)
- [ ] Design schemas that let "missing" be a valid answer → [D4](domains/d4-prompt-structured-output.md#schema-design-that-prevents-fabrication)
- [ ] Use few-shot examples and normalisation rules for consistency → [D4](domains/d4-prompt-structured-output.md#few-shot-examples)
- [ ] Build retry and feedback loops that actually improve results → [D4](domains/d4-prompt-structured-output.md#validation-retry-and-feedback-loops)
- [ ] Choose between synchronous calls and the Message Batches API → [D4](domains/d4-prompt-structured-output.md#batch-vs-synchronous)
- [ ] Use prompt caching correctly → [D4](domains/d4-prompt-structured-output.md#prompt-caching)

### D5 · Context Management & Reliability

- [ ] Keep long-running work coherent with subagents, scratchpads and targeted reads → [D5](domains/d5-context-reliability.md#long-running-work-and-large-codebases)
- [ ] Decide when to escalate immediately and when to keep working → [D5](domains/d5-context-reliability.md#escalation-decisions)
- [ ] Route human review by risk rather than at random → [D5](domains/d5-context-reliability.md#human-review-routing)
- [ ] Keep claims traceable to sources and dates → [D5](domains/d5-context-reliability.md#information-provenance)


## What is and isn't in scope

The official guide publishes both lists. Summarised in my own words:

| In scope | Out of scope |
|---|---|
| Agentic loops, multi-agent orchestration, sub-agent context | Fine-tuning, model internals and training methods |
| Tool interface design; MCP tools, resources and server configuration | Deploying or hosting MCP servers |
| Error handling, propagation and escalation decisions | Authentication protocols, key rotation, billing and account management |
| `CLAUDE.md`, commands, skills, plan mode, iterative refinement | Cloud-provider-specific configuration |
| Structured output through tool use, few-shot prompting, batch processing | Streaming and server-sent events; rate limits and pricing arithmetic |
| Context-window optimisation, human review, provenance | Prompt-caching internals; token counting; vision; computer use; embeddings and vector databases |

Two consequences for your study time:

* Several topics in the right-hand column **are** tested on the Developer exam. This hub teaches them in the [Developer track](../developer/index.md), and the short prompt-caching section on the D4 page is background, not a priority, for CCAR-F.
* Everything in the left-hand column has a checklist item above. If you can tick them all honestly, you have covered the published scope.

## Official courses

| Resource | Link |
|---|---|
| Architect – Foundations prep courses | <https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses> |
| Architect learning path | <https://anthropic-partners.skilljar.com/path/claude-architect> |
| All recommended courses, by domain | [Official Links](../resources/official-links.md#courses-for-the-architect-exam-ccar-f) |
