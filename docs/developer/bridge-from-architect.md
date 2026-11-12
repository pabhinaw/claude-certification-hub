# Architect → Developer Bridge

If you've completed the Architect track, a good part of CCDV-F is familiar. Use this map to spend time only on what's new.

## Overlap map

| CCDV-F domain | Already covered in Architect | New or deeper for Developer | Go to |
|---|---|---|---|
| Applications & Integration (33.1%) | Statelessness, sync vs batch, structured output | **Request/response shapes, stop reasons, streaming events, error codes and retries, rate limits, token counting, schema and configuration practice, reliability engineering** | [Part 1](domains/d1-api-mechanics.md) · [Part 2](domains/d1-application-design.md) |
| Model Selection & Optimisation (16.8%) | Model fit per task (light) | **Tokens, sampling, non-determinism, tier trade-offs, prompt-caching mechanics, cost arithmetic, latency levers** | [Deep-dive](domains/d2-model-selection.md) |
| Agents & Workflows (14.7%) | ✅ Most of D1 | The loop **in code**, stop conditions, Agent SDK options | [Deep-dive](domains/d3-agents-workflows.md) |
| Prompt & Context Engineering (11.0%) | ✅ D4 + D5 | Validation layers, defensive parsing, bounded retries with feedback | [Deep-dive](domains/d4-prompt-context.md) |
| Tools & MCPs (10.6%) | ✅ D2 | **Building an MCP server**, MCP server vs application-side client, server tools | [Deep-dive](domains/d5-tools-mcp.md) |
| Security & Safety (8.1%) | Hooks, permissions | **Injection threat models, secrets and key management, identity and access control, PII** | [Deep-dive](domains/d6-security-safety.md) |
| Claude Code (3.1%) | ✅ D3 | — | [Summary](domains/d7-claude-code-evals.md) |
| Eval, Testing & Debugging (2.6%) | Review patterns | Graders, regression testing, tracing, a debugging order | [Summary](domains/d7-claude-code-evals.md) |

## What that means for your time

| Effort | Domains | Share of exam |
|---|---|---|
| **Learn properly** (mostly new) | Applications & Integration, Model Selection, Security | about 58% |
| **Top up** (know the design, add the code) | Agents, Prompt & Context, Tools & MCP | about 36% |
| **Skim** | Claude Code, Evals | about 6% |

## The shift in thinking

| Architect asks | Developer asks |
|---|---|
| Which design is most reliable? | What exactly do you send, and what comes back? |
| Should this be enforced in code? | Which parameter, hook or check enforces it? |
| Batch or synchronous? | What does a batch cost, how are results matched, when does it expire? |
| How do we control context? | What does `usage` show, and why did the cache miss? |

The principles you learned still decide most questions: **guidance versus guarantee, least privilege, simplest design that works, surface errors**. The Developer exam adds the mechanics underneath them.

Next: the [10-Day Study Plan](study-plan-10-day.md).
