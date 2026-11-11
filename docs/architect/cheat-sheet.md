# CCAR-F Cheat Sheet

Read this the day before and the morning of the exam.

## The meta-rule

> **When asked how to *guarantee* something, pick the option enforced by code, configuration, hooks or schemas, at the narrowest correct scope, that costs the least context.**

## D1 · Agentic (27%)

* Loop on **`stop_reason`**: `tool_use` → run tools, return `tool_result`s, call again; `end_turn` → done; `max_tokens` → truncated.
* Never parse prose to decide completion. Always cap iterations, and **escalate** on the cap.
* **Every session ends resolved or escalated**, checked at the orchestration layer.
* Subagents: **isolated context**; pass context **explicitly**; return **structured summaries**; scoped tools.
* Prerequisites (verify → refund): **code gate / PreToolUse hook**, not prompt.
* Handoff package = facts + actions taken + **authorisation state** + open questions + reason + next step.
* Fixed pipeline for predictable work; **dynamic decomposition** for open-ended work.
* Resume = summary injection + **targeted re-analysis of changed files**.

## D2 · Tools & MCP (18%)

* **Descriptions drive selection**: what / when / when-not / input format / returns.
* Errors: `is_error` + **category** (transient, validation, business, permission) + **retryable** + **next action**. Access failure ≠ empty.
* `tool_choice`: `auto` · `any` (must call some tool) · `tool` (must call X) · `none`. Forced modes are incompatible with manual extended thinking.
* **Order**: force step 1 + gate the rest + progressive exposure; `disable_parallel_tool_use`.
* About 4–5 focused tools per agent beats 18 overlapping ones.
* MCP scopes: **project `.mcp.json`** (team, committed) · **user** `~/.claude.json` (personal, all projects) · **local** (default; personal, this project). Precedence local > project > user.
* Secrets: **`${ENV_VAR}`** expansion. Verify discovery with `claude mcp list` / `/mcp`.
* Grep = content · Glob = file names · Edit needs a unique match.

## D3 · Claude Code (20%)

* **Must/never → hooks or permissions. Should/prefer → CLAUDE.md or rules.**
* CLAUDE.md: user `~/.claude/` · project root · sub-directories; `@imports`.
* `.claude/rules/*.md` + `paths:` globs = conditional, path-specific guidance.
* Commands: `.claude/commands/` (team) · `~/.claude/commands/` (personal); `$ARGUMENTS`.
* Skills: `SKILL.md` description → auto-loaded when relevant.
* Settings precedence: managed > CLI > `settings.local.json` > `settings.json` > user. Deny beats allow.
* PostToolUse hook on `Edit|Write` → format, lint, test. Exit **2** = blocking feedback; exit 1 doesn't block.
* Plan mode: multi-file, uncertain, irreversible, needs review. Direct: small and clear.
* Context: CLAUDE.md (cross-session, team) · `@file` (task-specific) · inline (one-off).
* CI: `claude -p` + `--output-format json`; independent review session.

## D4 · Prompt & Output (20%)

* Vague → **explicit categorical criteria**. Don't rely on self-reported confidence.
* Few-shot: **varied formats**, edge cases **with reasoning**, missing → `null`.
* Strict structure → **tool + JSON schema + forced `tool_choice`**. Schema ≠ truth.
* Anti-fabrication: **nullable**, **optional**, `unknown`/`not_stated` enums, `other` + detail.
* Retry **with the specific error**; bounded; **never retry missing info**.
* Log error patterns → improve prompt / schema / examples.
* **Sync** if anyone waits; **Batch** (≈50% cheaper, ≤24 h, `custom_id`) for bulk.
* Review with an **independent instance**; per-file + cross-file passes.

## D5 · Context & Reliability (15%)

* Case-facts block; beware progressive summarisation, lost-in-the-middle, tool-result bloat.
* Escalate **immediately** on explicit human request; also on policy gap, over-authority, no progress. **Not** on sentiment alone.
* Propagate structured errors; never suppress.
* Long work: subagents, scratchpads, targeted reads, `/compact`, state exports.
* Review routing: **field-level calibrated confidence + doc characteristics + ambiguity + criticality**; **stratified** QA sampling.
* Provenance: claim → source, dates, annotate conflicts.
