# Developer Cheat Sheet

One page for the last two days. If a line here surprises you, go back to the deep-dive.

## Messages API

| | |
|---|---|
| Required | `model`, `max_tokens`, `messages` |
| System prompt | Top-level `system`, never a role in `messages` |
| State | **None.** Resend history every call |
| Response `content` | A **list of blocks**; check each `type` |
| `max_tokens` | Cap on output, not a target |
| Headers | `x-api-key`, `anthropic-version`, `content-type` |

## `stop_reason`

| Value | Do |
|---|---|
| `end_turn` | Use it |
| `max_tokens` | Truncated: raise cap / continue; **don't parse** |
| `stop_sequence` | See `stop_sequence` field |
| `tool_use` | Run tool → `tool_result` → call again |
| `pause_turn` | Send content back to continue (server tools) |
| `refusal` | Handle; don't blindly retry |
| `model_context_window_exceeded` | Treat as truncated |

## Errors

| Code | Type | Action |
|---|---|---|
| 400 | `invalid_request_error` | Fix request |
| 401 | `authentication_error` | Fix key |
| 403 | `permission_error` | Fix permissions |
| 404 | `not_found_error` | Fix model / resource ID |
| 413 | `request_too_large` | Shrink request |
| **429** | `rate_limit_error` | **Retry** after `retry-after` |
| **500** | `api_error` | **Retry** with backoff |
| **529** | `overloaded_error` | **Retry** with backoff |

SDK defaults: **2 retries**, **10-minute timeout**. Log the **request ID**. Errors can arrive **mid-stream** after a 200.

## Streaming

`message_start` → (`content_block_start` → `content_block_delta`… → `content_block_stop`)… → `message_delta` (**stop_reason, usage**) → `message_stop`. Ignore `ping`. Tool input = accumulate `partial_json`, parse at block stop. Streaming helps **perceived** latency only.

## Rate limits and tokens

* RPM / ITPM / OTPM, per organisation and model class; **token bucket**; 429 + `retry-after`
* Cache reads mostly **don't count** toward ITPM
* `count_tokens`: free, separate limit, an estimate, same inputs as a request

## Batches

50% cheaper · asynchronous (most within an hour, expire at 24 h) · up to 100,000 requests · match by **`custom_id`** · results not ordered · combine with caching. **Never for a waiting user.**

## Model selection

| Tier | Use |
|---|---|
| Haiku | Fast, cheap: classify, route, extract, screen, sub-agents |
| Sonnet | Balanced default for production |
| Opus and above | Hardest reasoning; errors are costly |

Three dials: **model tier**, **thinking / effort**, **speed** (fast mode = same model, faster, premium price, not with batch). Zero-shot → one-shot → multi-shot: more consistency, more input tokens (cache them). New release ≠ drop-in: pin, read notes, re-run evals.

Decide with **your evals**. Mix tiers (route small → escalate). Output tokens cost several times input. Temperature 0 ≠ deterministic. Context window = input + output, per request, not memory. Thinking = output tokens + time; skip for simple tasks.

## Prompt caching

| | |
|---|---|
| Write | 1.25× (5 min) / 2× (1 h) |
| Read | 0.1× |
| TTL | 5 min, refreshed on hit |
| Breakpoints | Max 4 |
| Order | tools → system → messages |
| Rule | **Identical prefix**, above a minimum size |

**Static first, dynamic last.** Misses: timestamp/user data in prefix · tools changed · TTL expired · too short · unstable serialisation. Check `cache_read_input_tokens`.

## Cost and latency levers

Cost: trim prompt/output → cache → batch → smaller model → manage context.
Latency: smaller model · shorter output · stream (perceived) · cache · parallelise · less thinking.

## Application design

* Simplest pattern first: single call → chain / route / parallel → agent
* Key and calls on the **backend**; state in **your** store
* Schema at every boundary: enums + `other`, nullable for absent data, flat
* Schema = **shape**; add **semantic** checks
* Bounded retries + backoff, timeouts, **idempotent** side effects, fallback
* Model ID, prompts, limits in **versioned config**; **pin** the model version
* Every prompt/model change → **eval set** → staged rollout → monitor

## Engineering foundations

* Business goal → **functional** (what it does) + **infrastructure** (latency, volume, cost, data rules) → measurable tests
* Life cycle: design → develop → test/eval → deploy → operate → **maintain** (deprecations, behaviour changes)
* SDK = wrapper over the same REST API (typing, retries, timeouts, stream helpers)
* JSON: double quotes, no comments or trailing commas; build with a serialiser; `null` ≠ missing ≠ `""`
* Sync (short) · SSE streaming (one-way, user watching) · async job / batch (bulk) · **WebSocket (two-way)**
* Async: bound concurrency (semaphore), handle partial failure, keep IDs for ordering
* Git for prompts, schemas, tools, evals, `CLAUDE.md`; CI runs tests **and** evals
* Review generated code: run it, check edges and security, verify packages exist, separate reviewer
* Big refactor: plan → tests → small steps on a branch → verify each
* Cloud platforms: auth, model IDs and feature availability differ. Check before relying on a feature

## Instruction surfaces

| Surface | Instructions live in |
|---|---|
| Messages API | `system` + messages; nothing else exists |
| Agent SDK | `system_prompt`; project files only if opted in |
| Claude Code | `CLAUDE.md`, rules, skills, commands + its own system prompt, tools, settings |
| claude.ai / desktop | Preferences, Project instructions and knowledge, styles, skills |

**Instructions are advisory; configuration is enforced.** Test on the surface you ship. One task per session; compact at breakpoints; restart after repeated failed corrections. Plugins bundle skills, commands, agents, hooks, MCP: trusted sources only, pinned, shared through project settings.

## Agents

* Loop on `stop_reason == "tool_use"`; append full assistant content; return **all** `tool_result`s in one user message, matched by `tool_use_id`
* Failures → `is_error: true` with a useful message
* Safety nets: turn cap, token/cost budget, timeout, repeat detection → escalate
* Approval gates for irreversible actions, **in code**
* Sub-agents: isolated context, pass everything explicitly, return summaries
* Supervisor + workers: for broad, separable work; costs many more tokens
* Memory: scoped (user/project), store decisions not transcripts, treat as data
* Self-hosted (your loop / Agent SDK: full control, private network) vs managed (hosted harness, long-running, stateful sessions)
* Frameworks: LangGraph (graph + state + checkpoints) · PydanticAI (typed, validated) · Strands (model-driven). Keep prompts visible
* **Must / never / always → code, not prompt**

## Structured output and validation

| Method | Guarantee |
|---|---|
| Prompt + parse | None |
| Forced tool (+ `strict`) | Tool called; schema-conformant input |
| `output_config` JSON schema | Valid JSON matching schema |

Still check `stop_reason` (truncation, refusal) and meaning. Retry **with the error**, **bounded**, then fall back. Absent data → nullable, not more retries.

## Context

Drift grows with length. Pin exact facts · summarise old turns · clear old tool results · retrieve only what's relevant · sub-agents for noisy work · fresh session with a hand-over. Documents first, question last.

## Tools and MCP

* Tool = `name` + `description` + `input_schema`; **your code executes**
* `tool_choice`: `auto` / `any` / `tool` / `none`; `strict: true`; `disable_parallel_tool_use`
* Server tools run on the platform (`pause_turn`)
* MCP: host → client → server, JSON-RPC 2.0
* **Tools** (model) · **Resources** (app, read-only) · **Prompts** (user)
* stdio (local) / Streamable HTTP (remote)
* FastMCP: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`; docstring = description; **logs to stderr**
* Test with the **Inspector**; scopes local / project (`.mcp.json`) / user; secrets via `${VAR}`
* **Reused by several hosts → MCP server. One app, one call → plain tool.**
* **Access → tool / MCP. Know-how → skill. Already exists → built-in tool. Enforce → hook. Isolate → sub-agent. Always-on facts → `CLAUDE.md`.**
* Harness: dispatch by name (unknown tool → error result), approve by risk, small distinct tool sets

## Security

* Direct injection (user is attacker) vs indirect (content is attacker)
* Layers: screen input → separate data from instructions → **least privilege** → approval → validate output → monitor
* Untrusted content in `tool_result` / tags; never your instructions in tool results
* Deterministic guardrails: `PreToolUse` hook, deny rules, validation
* Keys: backend only, secret store, per-environment, rotate; leaked → **revoke first**; never in prompts
* Identity from the **session**; authorisation **inside the tool**
* Model output is untrusted: no `eval`, parameterised SQL, escape HTML
* Minimise and redact PII, including in logs
* Authentication (who) ≠ authorisation (what they may do); monitor key and tool use
* Sanitise input (length, format, delimiter break-outs); don't trust confident-sounding output, verify it

## Claude Code and evals

`/init` creates `CLAUDE.md` · auto memory = Claude's own notes · modes: default / accept edits / plan / auto / bypass · headless `-p`, `--output-format json` or `stream-json` · custom commands in `.claude/commands/`.

`CLAUDE.md` (always) · rules (path-scoped) · skills (on demand) · commands (`/name`) · hooks (enforce) · `.mcp.json` · settings (allow / ask / **deny wins**) · `-p` for CI · `--continue` / `--resume` · `/compact` / `/clear`.

Evals: define success → realistic test set → grader (code / LLM / human) → run on every change → add production failures. Trace everything. Debug in order: HTTP error → `stop_reason` → context sent → tool behaviour → prompt. **Integration or model?** Same failure every time → code; varies run to run → model. Calibrate LLM graders against human labels.

## Words that decide questions

| If the question says… | Think… |
|---|---|
| *must, always, never, guarantee* | Code, hook, schema; not prompt wording |
| *most cost-effective*, overnight, bulk | Batch + caching, smaller tier |
| *real-time*, user waiting | Streaming, smaller tier; not batch |
| *intermittent*, *sometimes fails to parse* | `stop_reason`, validation |
| *shared across teams/tools* | Project scope, MCP server, version control |
| *untrusted*, web page, email | Indirect injection → least privilege |
| *simplest*, *first step* | The smallest change that addresses the cause |
