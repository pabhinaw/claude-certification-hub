# How I Prepared for CCAR-F

**Result:** Passed · November 2026 ·
[Verify credential on Credly](https://www.credly.com/badges/b512d180-1dd7-4edb-8fb6-6251ec998635){ target="_blank" rel="noopener" }

This page shares my **preparation approach**: what I did, in what order, and what I'd do again. It contains no exam questions or exam content (see the [content policy](../resources/content-policy.md)).

## My approach in one line

> Learn the **design principle** first, **build it once** by hand, then **practise choosing** between plausible options.

## What I did, step by step

1. **Mapped the domains first.** Before studying anything, I listed the five domains and their weights and planned my time by weight. → [Domains & Study Checklist](../architect/exam-blueprint.md)
2. **Filled the basics gaps.** I made sure I could explain statelessness, `stop_reason`, tool use and `tool_choice` without notes. → [Fundamentals](../fundamentals/index.md)
3. **Built small things.** An agent loop with a code gate, a forced-tool extraction pipeline, and a repo with CLAUDE.md, a path rule, a command and a hook. Building is what made the concepts stick. → [Labs](../labs/index.md)
4. **Studied the "why", not just the "what".** For every topic I wrote the one-line decision rule. Most of those rules are on the [Cheat Sheet](../architect/cheat-sheet.md).
5. **Practised with scenario-style questions** and, for every answer, explained why each *wrong* option was wrong.
6. **Reviewed the tricky topics** in the final week. → [Commonly Missed Topics](../architect/commonly-missed.md)

## What I'd tell you

1. **Hands-on beats reading.** Topics I had actually configured in a real repo felt easy; topics I'd only read about didn't.
2. **"Guarantee" means code.** When an option says "instruct the model to…", look for a deterministic alternative: hooks, schemas, `tool_choice`, permissions or code gates.
3. **Read each scenario's constraints twice.** Words like *team-wide*, *strict*, *blocking* and *overnight* each point to a specific kind of answer.
4. **Don't skip the "boring" topics.** Tool ordering, review routing and schema design for missing data look simple, but they're easy to get subtly wrong.

## Questions? Let's connect

If something on this site is unclear, or you want to talk about your preparation, I'm happy to help.

[:fontawesome-brands-linkedin: Connect with me on LinkedIn](https://www.linkedin.com/in/pabhinaw/){ .md-button .md-button--primary target="_blank" rel="noopener" }

!!! note "Please don't ask for exam questions"
    I'll gladly discuss **topics, concepts and study strategy**, but I can't share or discuss exam questions or exam content. That's confidential for every candidate.

If this hub helped you, consider [contributing](../resources/contributing.md) a fix or an original question.
