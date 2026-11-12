# Prompts guide, code guarantees

<p class="hub-post-meta">Prasoon Abhinaw · November 2026 · 5-minute read</p>

There's one idea that, once it clicks, makes a large share of Claude architecture decisions straightforward:

> **A prompt makes good behaviour *likely*. Code makes it *certain*.**

## The pattern you'll see everywhere

A team notices a problem: the agent refunds before verifying identity, Claude Code edits a protected folder, or an extraction sometimes comes back as prose instead of JSON. The first instinct is to strengthen the prompt: add "ALWAYS", add capital letters, add the rule twice.

That often *helps*. It never *guarantees*. Models follow instructions very well, but "very well" isn't "every time", and in production the rare miss is the one that becomes an incident.

## Where guarantees actually live

| You need… | Prompt-only answer | Guaranteed answer |
|---|---|---|
| A tool call, never prose | "Always call record_invoice" | `tool_choice` forcing the tool, or native structured outputs |
| Step A before step B | "Verify first" | A code gate or PreToolUse hook that blocks B until A succeeds |
| A business limit respected | "Never refund over 2,000" | A PreToolUse hook that denies over-limit calls |
| Files always formatted | "Run Prettier after editing" | A PostToolUse hook on Edit and Write |
| Secrets never read | "Don't open .env" | A permissions deny rule |
| Every session ends cleanly | "Always resolve or escalate" | An orchestration-layer check after the loop ends |

## So are prompts unimportant?

Not at all. Prompts decide the **quality** of everything inside the guardrails: how well Claude reasons, how clearly it writes, how it handles ambiguity. Guarantees decide the **boundaries**. Good systems use both:

* **Prompts and CLAUDE.md** for judgement, style and conventions: the *shoulds*.
* **Schemas, `tool_choice`, hooks, permissions and code gates** for invariants: the *musts*.

## A one-question test

Whenever you're about to add a rule to a prompt, ask:

> *"If Claude ignored this once, would it be an incident?"*

If yes, it's a *must*: enforce it in code, and keep the prompt sentence only as an explanation. If no, it's a *should*, and the prompt is the right place.

## Go deeper

* [D1 · Hooks: deterministic policy enforcement](../architect/domains/d1-agentic-architecture.md#hooks-deterministic-policy-enforcement)
* [D3 · Advice vs enforcement](../architect/domains/d3-claude-code.md#advice-vs-enforcement)
* [Lab 1 · Build an Agentic Loop](../labs/lab-01-agentic-loop.md)
