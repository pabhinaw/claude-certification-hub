# Glossary

Agent
:   A system where Claude repeatedly decides on actions (tool calls), observes the results, and continues until the goal is met.

Agentic loop
:   The code loop that calls Claude, runs requested tools, returns results, and repeats while `stop_reason == "tool_use"`.

Agent SDK (Claude Agent SDK)
:   Anthropic's library (Python / TypeScript) for building agents with the same harness that powers Claude Code: tools, subagents, hooks, sessions, permissions.

Batch API (Message Batches)
:   Asynchronous bulk processing at about 50% lower cost, with results within 24 hours; requests are matched by `custom_id`.

CLAUDE.md
:   A Markdown memory file that Claude Code loads automatically to learn project conventions. Advisory, not enforced.

Context window
:   Maximum tokens (input + output) Claude considers in one request.

Coordinator / orchestrator
:   The agent that breaks down a task, delegates to subagents and assembles results (hub-and-spoke).

Escalation
:   Handing a case to a human. A first-class outcome in a well-designed agent, not a failure.

Few-shot prompting
:   Including worked examples in the prompt to show the desired format or judgement.

Handoff package
:   A structured summary passed between agents or to a human: facts found, actions taken, open questions, authorisation state.

Hook
:   A user-defined command or script that runs at a lifecycle event (e.g. PreToolUse, PostToolUse, Stop). Deterministic enforcement.

Lost in the middle
:   The tendency of models to use information in the middle of long contexts less reliably.

MCP (Model Context Protocol)
:   Open standard for connecting AI applications to tools, resources and prompts via servers.

Plan mode
:   A Claude Code mode where Claude researches and proposes a plan without modifying files.

Prefill
:   Starting the assistant's reply with given text to steer the format. (Forced `tool_choice` uses an internal prefill.)

Prompt caching
:   Reusing a stable prompt prefix across requests to reduce cost and latency.

Scratchpad file
:   A file an agent writes notes to, so findings survive context compaction or new sessions.

Skill
:   A folder with `SKILL.md` (plus optional scripts/resources) that Claude loads on demand when a task matches its description.

`stop_reason`
:   Field in each response explaining why generation stopped: `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn`, `refusal`.

Stratified sampling
:   Sampling for human review *within* subgroups (document type, confidence band, field) so rare but risky cases get reviewed.

Subagent
:   An agent launched by another agent with its own isolated context and (often) restricted tools.

`tool_choice`
:   Request parameter controlling whether Claude may, must, or must not call tools: `auto`, `any`, `tool`, `none`.

`tool_result`
:   The content block your app sends back after running a tool; references the `tool_use_id`, may set `is_error`.
