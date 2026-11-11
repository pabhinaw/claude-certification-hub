# Architect → Developer Bridge

If you've completed the Architect track, much of CCDV-F is already familiar. Use this map to spend time only on what's new.

## Overlap map

| CCDV-F domain | Already covered in Architect | New or deeper for Developer |
|---|---|---|
| Applications & Integration (33.1%) | statelessness, sync vs batch, structured output | **SDK mechanics**, streaming, error codes and retries, rate limits, request/response shapes, configuration management, application design patterns |
| Model Selection & Optimisation (16.8%) | model fit per task (light) | **model trade-offs in depth**, token counting, **prompt caching** mechanics, cost estimation, latency |
| Agents & Workflows (14.7%) | ✅ most of D1 | frameworks/SDK specifics, implementation details |
| Prompt & Context Engineering (11.0%) | ✅ D4 + D5 | output handling in code |
| Tools & MCPs (10.6%) | ✅ D2 | **building an MCP server**, agentic customisation |
| Security & Safety (8.1%) | hooks, permissions | **secrets and key management**, prompt-injection defences, guardrails in app code |
| Claude Code (3.1%) | ✅ D3 | — |
| Eval, Testing & Debugging (2.6%) | review patterns | debugging techniques, eval design |

## Suggested study order (after CCAR-F)

1. **API mechanics hands-on** (week 1): streaming, errors and retries, token counting, prompt caching, batches end to end.
2. **Model selection and cost** (week 1–2): build a small cost/latency comparison across model tiers on the same task.
3. **Build an MCP server** (week 2): expose two tools and one resource; connect it to Claude Code.
4. **Security** (week 2): key handling, least-privilege tools, untrusted input and prompt injection, output validation.
5. **Review** (week 3): Developer practice questions (coming soon) and official materials.
