# CCAR-F Exam Overview

## Key facts

| Item | Detail |
|---|---|
| Full name | Claude Certified Architect – Foundations |
| Exam code | **CCAR-F** (older materials say **CCA-F**; same credential) |
| Launched | 12 March 2026, with the Claude Partner Network |
| Questions | **60**, scenario-based: multiple choice and **multiple response** (the question says how many to select) |
| Time | **120 minutes** (about 2 minutes per question) |
| Structure | **4 scenarios** drawn at random from a published bank of **6** |
| Passing score | **720** on a 100–1000 scaled score |
| Validity | 12 months |
| Price | about $125 USD (before partner discounts) |
| Delivery | Pearson VUE, online proctored or at a test centre; registration via Anthropic's Partner Academy |
| Eligibility | currently open to people at organisations in the **Claude Partner Network** |
| Recommended experience | about 6 months hands-on with the Claude API, Agent SDK, Claude Code and MCP |
| Aids | none: you cannot have Claude or docs open during the exam |

!!! info "Official exam guide"
    The exam guide (version 1.0, effective July 2026) is the authority on scope. It lists every task statement, the six scenarios, and what is in and out of scope. Find it on the [certifications page](https://anthropic-partners.skilljar.com/page/partner-certifications) and read it before you book. This hub's [Domains & Study Checklist](exam-blueprint.md) is mapped to it.

## What the exam really measures

Reviewers who have taken it describe it less as a recall test and more as a check on whether you have **actually shipped agentic systems and learned from what broke**. The examples below are **our own illustrations** of that style, not exam questions:

* *"The agent sometimes ends without resolving the case or escalating. What is the most reliable fix?"*
* *"Where should a team-wide MCP server be configured, and how should its token be supplied?"*
* *"Which approach best reduces fabricated values in extracted fields?"*

All four options usually sound plausible. The best one is typically the **most deterministic, most targeted, at the correct scope, and cheapest in context**.

## Scoring

* The score report shows your scaled score and a per-area breakdown. That is useful for spotting weak areas even after you pass.
* Scaled scoring means you cannot convert directly to "number of questions needed". Aim for **85% or better on practice** to have margin.

## The six scenarios (summary)

| # | Scenario | Domains it mostly draws on |
|---|---|---|
| 1 | Customer Support Resolution Agent | D1, D2, D5 |
| 2 | Code Generation with Claude Code | D3, D5 |
| 3 | Multi-Agent Research System | D1, D2, D5 |
| 4 | Developer Productivity with Claude | D2, D3, D1 |
| 5 | Claude Code for Continuous Integration | D3, D4 |
| 6 | Structured Data Extraction | D4, D5 |

Full breakdown, with architectures and typical traps: [The Six Scenarios](scenarios.md).
