# Exam Blueprint & Objectives

This page is your **master checklist**. It lists every task statement by domain, then the more detailed *objectives*, written as they appear on CCAR-F score reports, each mapped to the domain page that teaches it.

## Weights

| Domain | Weight | ≈ Questions (of 60) |
|---|---|---|
| D1 · Agentic Architecture & Orchestration | 27% | ~16 |
| D3 · Claude Code Configuration & Workflows | 20% | ~12 |
| D4 · Prompt Engineering & Structured Output | 20% | ~12 |
| D2 · Tool Design & MCP Integration | 18% | ~11 |
| D5 · Context Management & Reliability | 15% | ~9 |

Question counts are estimates from the weights; the real exam assigns questions through scenarios.

## Task statements

=== "D1 · Agentic (27%)"

    | # | Task statement |
    |---|---|
    | 1.1 | Agentic loops: branch on `stop_reason`, return tool results, never parse prose to decide termination |
    | 1.2 | Coordinator–subagent (hub-and-spoke) orchestration with isolated subagent context |
    | 1.3 | Subagent invocation and configuration: allowed tools, agent definitions, explicit context passing |
    | 1.4 | Multi-step workflows: programmatic prerequisite enforcement, structured handoffs, guaranteed termination |
    | 1.5 | Agent SDK hooks: PreToolUse / PostToolUse for policy and compliance |
    | 1.6 | Task decomposition: fixed pipelines vs dynamic, adaptive decomposition |
    | 1.7 | Session state: resume vs fork vs fresh-start-with-summary |

=== "D2 · Tools & MCP (18%)"

    | # | Task statement |
    |---|---|
    | 2.1 | Tool interfaces: descriptions as the primary selection mechanism; disambiguation |
    | 2.2 | Structured tool errors: `is_error`, error category, retryability, next action |
    | 2.3 | Tool distribution and `tool_choice`: right number of tools per agent; forced vs auto; sequencing |
    | 2.4 | MCP integration: scopes, env-var expansion, resources, discovery |
    | 2.5 | Built-in tools: Grep vs Glob vs Read; Edit uniqueness |

=== "D3 · Claude Code (20%)"

    | # | Task statement |
    |---|---|
    | 3.1 | CLAUDE.md hierarchy, `@` imports, `.claude/rules/` |
    | 3.2 | Custom slash commands and Skills: project vs user locations, frontmatter |
    | 3.3 | Path-specific rules with glob patterns |
    | 3.4 | Plan mode vs direct execution |
    | 3.5 | Iterative refinement: examples, test-driven iteration, batching issues |
    | 3.6 | CI/CD integration: `-p`, JSON output, session isolation |

=== "D4 · Prompt & Output (20%)"

    | # | Task statement |
    |---|---|
    | 4.1 | Explicit, categorical criteria instead of vague instructions |
    | 4.2 | Few-shot prompting for format consistency and ambiguous cases |
    | 4.3 | Structured output via tool use + JSON schema + `tool_choice`; nullable/optional fields |
    | 4.4 | Validation and retry loops; structured error feedback |
    | 4.5 | Batch processing: when to use the Message Batches API |
    | 4.6 | Multi-instance / independent review |

=== "D5 · Context (15%)"

    | # | Task statement |
    |---|---|
    | 5.1 | Context preservation: summarisation risks, lost-in-the-middle, case-facts blocks |
    | 5.2 | Escalation patterns: when to escalate immediately vs investigate |
    | 5.3 | Error propagation: keep structured error context; never suppress |
    | 5.4 | Large codebases: scratchpads, subagents, state exports, `/compact` |
    | 5.5 | Human review workflows: stratified sampling, field-level confidence |
    | 5.6 | Information provenance: claim–source maps, conflicts, dates |

## Detailed objectives (as worded on score reports)

Use the checkboxes as a self-assessment. Tick an objective only when you could explain it to someone else.

### D1 · Agentic Architecture & Orchestration

- [ ] Explain how the agentic loop uses model responses and `stop_reason` signals to decide whether to continue tool execution or terminate. → [D1](domains/d1-agentic-architecture.md#the-agentic-loop)
- [ ] Explain why conversation history must be explicitly included in each API request in a stateless API. → [Messages API](../fundamentals/messages-api.md#the-api-is-stateless-you-own-the-conversation)
- [ ] Decompose complex tasks into dynamically generated subtasks that adapt to new information. → [D1](domains/d1-agentic-architecture.md#task-decomposition-fixed-vs-dynamic)
- [ ] Design orchestration-layer safeguards ensuring every session ends with a completed resolution or human escalation. → [D1](domains/d1-agentic-architecture.md#guaranteed-termination-resolution-or-escalation)
- [ ] Design structured handoff packages that preserve context, findings and authorisation state. → [D1](domains/d1-agentic-architecture.md#structured-handoff-packages)
- [ ] Apply PreToolUse and PostToolUse hook patterns to enforce business rules not delegated to model discretion. → [D1](domains/d1-agentic-architecture.md#hooks-deterministic-policy-enforcement)
- [ ] Apply session resumption techniques, including targeted re-analysis of changed files and context injection. → [D1](domains/d1-agentic-architecture.md#session-state-resume-fork-or-fresh-start)

### D2 · Tool Design & MCP Integration

- [ ] Improve tool selection reliability with use-case examples, input formats and disambiguation guidance. → [D2](domains/d2-tool-design-mcp.md#tool-descriptions-the-1-selection-signal)
- [ ] Implement MCP tool error handling that returns structured, type-specific errors with recoverability and next actions. → [D2](domains/d2-tool-design-mcp.md#structured-tool-errors)
- [ ] Configure `tool_choice` to guarantee invocation when structured output is required, and **sequence multi-tool workflows so prerequisite data is obtained first**. → [D2](domains/d2-tool-design-mcp.md#tool_choice-and-tool-sequencing)
- [ ] Integrate MCP servers: correct scope, auth via env-var expansion, verify tool discovery. → [D2](domains/d2-tool-design-mcp.md#mcp-integration)
- [ ] Configure MCP servers at the correct scope: project for shared team tooling, user for personal or experimental. → [D2](domains/d2-tool-design-mcp.md#mcp-integration)

### D3 · Claude Code Configuration & Workflows

- [ ] Select the correct mechanism (CLAUDE.md, `.claude/rules/` with globs, Skills, hooks, settings permissions) for the guidance type. → [D3](domains/d3-claude-code.md#choosing-the-right-mechanism)
- [ ] Distinguish instructions that must be enforced by settings or hooks from those that belong in CLAUDE.md. → [D3](domains/d3-claude-code.md#advice-vs-enforcement)
- [ ] Select how to provide project context: `@` references, CLAUDE.md or inline description. → [D3](domains/d3-claude-code.md#providing-context-references-vs-claudemd-vs-inline)
- [ ] Create and deploy custom slash commands in the correct project or user directory. → [D3](domains/d3-claude-code.md#custom-slash-commands-and-skills)
- [ ] Determine when to use plan mode versus direct execution. → [D3](domains/d3-claude-code.md#plan-mode-vs-direct-execution)
- [ ] Implement PostToolUse hooks that enforce formatting, linting or tests after every edit. → [D3](domains/d3-claude-code.md#hooks-for-code-quality)
- [ ] Structure iterative refinement with concrete I/O examples, targeted feedback and batched issue descriptions. → [D3](domains/d3-claude-code.md#iterative-refinement)
- [ ] Apply systematic codebase exploration with Grep, Glob and Read while managing context. → [D3](domains/d3-claude-code.md#exploring-a-codebase-systematically)

### D4 · Prompt Engineering & Structured Output

- [ ] Select the most reliable structured-output method (tool use + schema, prompt formatting, prefill) for the required strictness. → [D4](domains/d4-prompt-structured-output.md#choosing-a-structured-output-method)
- [ ] Implement tool use with JSON schemas and configure `tool_choice` to guarantee invocation. → [D4](domains/d4-prompt-structured-output.md#choosing-a-structured-output-method)
- [ ] Design extraction schemas with optional fields, nullable values and enums that represent missing or ambiguous data without fabrication. → [D4](domains/d4-prompt-structured-output.md#schema-design-that-prevents-fabrication)
- [ ] Apply extraction accuracy patterns: schemas, normalisation instructions, few-shot examples. → [D4](domains/d4-prompt-structured-output.md#few-shot-examples)
- [ ] Design feedback loops that capture structured error metadata to improve prompts, schemas or examples. → [D4](domains/d4-prompt-structured-output.md#validation-retry-and-feedback-loops)
- [ ] Select synchronous Messages API vs asynchronous Message Batches API. → [D4](domains/d4-prompt-structured-output.md#batch-vs-synchronous)

### D5 · Context Management & Reliability

- [ ] Apply context management strategies (subagent isolation, scratchpad files, targeted reading) across long sessions. → [D5](domains/d5-context-reliability.md#long-running-work-and-large-codebases)
- [ ] Apply escalation criteria: honour a human request immediately vs attempt autonomous resolution. → [D5](domains/d5-context-reliability.md#escalation-decisions)
- [ ] Design human review routing using confidence scores, document characteristics and field-level ambiguity rather than random sampling. → [D5](domains/d5-context-reliability.md#human-review-routing)
