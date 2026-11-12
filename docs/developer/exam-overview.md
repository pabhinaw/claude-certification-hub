# CCDV-F Exam Overview

| Item | Detail |
|---|---|
| Full name | Claude Certified Developer – Foundations |
| Code | **CCDV-F** |
| Questions | **53** |
| Question types | **Multiple choice** (one correct answer) and **multiple response** (the question states how many to select) |
| Time | **120 minutes** (allow extra for check-in) |
| Passing score | **720** on a scaled range of 100–1000 |
| Price | about $125 USD (before partner discounts) |
| Delivery | Pearson VUE: online proctored or at a test centre |
| Validity | 12 months |
| Result | Pass/fail with a scaled score; percentage correct by domain is shown for information only |
| Prerequisites | None formal |

Details can change. Confirm them in the [official exam guide](https://anthropic-partners.skilljar.com/page/partner-certifications) before you book.

## Recommended background

* 1–5 years of software engineering
* About six months working with Claude or similar LLM systems
* Python and/or TypeScript, REST APIs, JSON, command-line tools, version control
* Working understanding of LLM fundamentals, agents, context management and MCP

## The official blueprint

The exam guide (version 1.0, effective July 2026) lists eight domains and 25 weighted skills. The table below summarises them in my own words, with a link to where each is taught here. **The guide itself is the authority**: read it in full before you book.

| Domain and skill | Weight | Study here |
|---|---|---|
| **Applications & Integration** | **33.1%** | |
| Claude application design: how instructions are read on each surface, content boundaries, schemas, session hygiene, plugins | 8.6% | [Application Design](domains/d1-application-design.md) |
| Software engineering foundations: REST, JSON, async, version control, SDLC, code review, refactoring | 7.4% | [Engineering Foundations](domains/d1-engineering-foundations.md) |
| Claude API mechanics: messages, tools, streaming, vision, thinking, caching, batches, cloud platforms | 6.8% | [API Mechanics](domains/d1-api-mechanics.md) |
| Configuration management: `CLAUDE.md`, settings, model pinning, prompt versioning, plugin dependencies | 4.1% | [Application Design](domains/d1-application-design.md) |
| Understanding requirements: business needs into functional and infrastructure requirements | 3.4% | [Engineering Foundations](domains/d1-engineering-foundations.md) |
| Systems life cycle: develop, implement, operate, maintain | 2.8% | [Engineering Foundations](domains/d1-engineering-foundations.md) |
| **Model Selection & Optimisation** | **16.8%** | |
| Technical fundamentals: SDKs over REST, WebSockets | 6.1% | [Engineering Foundations](domains/d1-engineering-foundations.md) |
| LLM fundamentals: tokens, context, sampling, non-determinism, fast mode, thinking, effort, zero/one/multi-shot | 5.2% | [Model Selection](domains/d2-model-selection.md) |
| Cost and token management: budgeting, usage tracking, cost modelling, caching and cache checkpoints | 2.8% | [Model Selection](domains/d2-model-selection.md) |
| Model selection and trade-offs: tiers, quality/latency/cost, changes between releases | 2.7% | [Model Selection](domains/d2-model-selection.md) |
| **Agents & Workflows** | **14.7%** | |
| Agent construction: Agent SDK, custom loops and harnesses, self-hosted vs managed, hooks | 5.3% | [Agents & Workflows](domains/d3-agents-workflows.md) |
| Agent patterns and frameworks: tool loops, sub-agents, memory, context; Strands, LangGraph, PydanticAI | 4.9% | [Agents & Workflows](domains/d3-agents-workflows.md) |
| Agent architecture: agents vs workflows, supervisor hierarchies, sub-agents | 4.5% | [Agents & Workflows](domains/d3-agents-workflows.md) |
| **Prompt & Context Engineering** | **11.0%** | |
| Prompt engineering: clarity, few-shot, placement, output constraints, refinement, input sanitisation | 4.6% | [Prompt & Context](domains/d4-prompt-context.md) |
| Context engineering: window management, pruning, compaction, isolation with sub-agents | 3.8% | [Prompt & Context](domains/d4-prompt-context.md) |
| Output handling: structured output, validation, defensive parsing, scepticism | 2.6% | [Prompt & Context](domains/d4-prompt-context.md) |
| **Tools & MCPs** | **10.6%** | |
| Tool implementation: descriptions, errors, harness dispatch, client vs server tools, approval, scoping | 4.4% | [Tools & MCPs](domains/d5-tools-mcp.md) |
| Agentic customisation: choosing built-in tools, custom tools, skills or MCP | 4.1% | [Tools & MCPs](domains/d5-tools-mcp.md) |
| MCP server development: authoring, deploying, primitives, transports, client vs server | 2.1% | [Tools & MCPs](domains/d5-tools-mcp.md) |
| **Security & Safety** | **8.1%** | |
| AI application security: injection, jailbreaks, untrusted input, leakage, PII, access | 3.2% | [Security & Safety](domains/d6-security-safety.md) |
| Guardrails and safe deployment: layered guardrails, secure by design, least privilege | 2.3% | [Security & Safety](domains/d6-security-safety.md) |
| Identity, secrets and key management | 1.6% | [Security & Safety](domains/d6-security-safety.md) |
| Hooks as guardrails | 1.0% | [Security & Safety](domains/d6-security-safety.md) |
| **Claude Code**: components, sessions, commands, headless/streaming/auto modes, `CLAUDE.md`, settings | **3.1%** | [Claude Code · Evals](domains/d7-claude-code-evals.md) |
| **Eval, Testing & Debugging**: error types, recovery, trace analysis, integration vs model | **2.6%** | [Claude Code · Evals](domains/d7-claude-code-evals.md) |

## What the weights tell you

* **Plain engineering is a fifth of the exam.** Software engineering foundations (7.4%), technical fundamentals (6.1%), requirements (3.4%) and life cycle (2.8%) add up to almost 20%, with no Claude-specific trivia in them.
* **Application design is the single biggest skill** (8.6%): knowing how Claude reads instructions on each surface, and keeping content, sessions and plugins in order.
* **Choosing the right extension mechanism** (4.1%) is worth nearly as much as tool implementation itself.
* **Claude Code and debugging together are about three questions.** Learn the tables; don't over-invest.

With 53 questions, each one is worth about 1.9% of the paper, so a 3.4% skill is roughly two questions. These are my estimates for planning, not an official count.

## Official resources

| Resource | What it is |
|---|---|
| [Certifications page](https://anthropic-partners.skilljar.com/page/partner-certifications) | Exam guide, policies and registration for every Claude certification |
| [Exam registration](https://anthropic-partners.skilljar.com/claude-certified-developer-foundations-certification) | Booking for CCDV-F |
| [Developer – Foundations prep path](https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations) | Five official courses, about 13 hours in total |
| [Developer learning path](https://anthropic-partners.skilljar.com/path/claude-developer) | Nine broader courses on the platform, Claude Code, MCP, skills and sub-agents |
| [Certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) | Retakes, renewal, ID rules, delivery |

The five prep courses, and the part of this track that matches each:

| Official course | Length | Matching pages here |
|---|---|---|
| MSO Foundations | 57 min | [Model Selection](domains/d2-model-selection.md) · [Engineering Foundations](domains/d1-engineering-foundations.md) |
| Production-Grade Prompting, Agents & Tool Use | 209 min | [API Mechanics](domains/d1-api-mechanics.md) · [Prompt & Context](domains/d4-prompt-context.md) · [Agents](domains/d3-agents-workflows.md) |
| Claude Code, MCP & Integration | 142 min | [Tools & MCPs](domains/d5-tools-mcp.md) · [Application Design](domains/d1-application-design.md) · [Claude Code](domains/d7-claude-code-evals.md) |
| Production Engineering, Evals & Security | 211 min | [Security](domains/d6-security-safety.md) · [Evals](domains/d7-claude-code-evals.md) · [Application Design](domains/d1-application-design.md) |
| Accelerators & IP Contribution | 155 min | [Engineering Foundations](domains/d1-engineering-foundations.md) (platforms, versioning) |

!!! tip "Use both"
    The official courses are the primary source. This hub is the revision layer: condensed pages, decision rules, practice questions and timed mocks. If the two ever disagree, trust the official material and [tell me](../about/index.md).

## Policies worth knowing

* **Closed book.** No notes, documentation or AI assistants.
* **Retakes:** wait 14 days after a first unsuccessful attempt, 30 after a second, 90 after a third; at most four attempts in a rolling 12 months.
* **Rescheduling:** allowed up to a cut-off before the appointment, after which the fee is forfeited. The published cut-off differs between documents, so check your booking confirmation.
* **ID:** government-issued, unexpired, and the name must match your registration exactly.
* **Confidentiality:** you accept a non-disclosure agreement before the exam. Exam content must not be recorded or shared.
* **Renewal:** the credential lasts 12 months; on-time renewal is a free, non-proctored assessment.

## Multiple-response questions

Some items ask you to choose more than one option, and the question says how many ("Select TWO"). Treat them carefully:

* Select **exactly** the number asked for.
* Judge **each option on its own** as true or false, instead of hunting for a pair.
* Assume there is no partial credit, so each correct option matters.

The [mock exams](mock-exams.md) include multiple-response items so you can practise the format.

## What a score target means

The pass mark is 720 on a scaled score. A scaled score is **not** a percentage, and nobody outside the exam provider can convert practice results into it. As a working guide, if you aim high (around 900), prepare until you are scoring **90% or better on fresh mock questions at the first attempt** and can explain why each wrong option is wrong. That standard, more than any number, is what readiness looks like.

!!! tip "How it differs from Architect"
    Architect asks *which design is best*. Developer is more **code-first**: request and response shapes, SDK behaviour, streaming, error handling, caching, model choice, cost and secrets.
