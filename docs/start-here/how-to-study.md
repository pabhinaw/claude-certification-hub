# How to Study Effectively

Claude certification exams are **scenario-based**. You are given a business situation and several options that all *sound* reasonable. Memorising facts gets you part of the way; the rest comes from recognising **which design principle the question is testing**.

## 1. Learn principles, then attach facts

For every topic, write down the *principle* first, then the facts that support it.

| Principle | Facts that hang off it |
|---|---|
| Guarantees belong in code, not prompts | hooks, `tool_choice`, JSON schemas, permission rules, prerequisite gates |
| The API is stateless | resend `messages` every turn; state lives in *your* application |
| Context is a scarce resource | subagents, scratchpad files, `/compact`, targeted reads, case-facts blocks |
| Put configuration at the narrowest correct scope | project vs user `.mcp.json`, `.claude/rules/` with globs, settings hierarchy |
| Don't let the model fabricate | optional/nullable fields, "unknown" enums, escalation paths |

## 2. Use the "eliminate two" technique

Most questions have two clearly weaker options. Typical red flags:

* "Add an instruction to the system prompt telling Claude to *always*…" when a *guarantee* is needed
* "Increase the context window / use a bigger model" as the fix for a design problem
* "Parse Claude's text to decide whether the task is finished" instead of checking `stop_reason`
* "Have the same instance review its own output" instead of an independent reviewer
* "Retry until it works" when the information is simply missing

Then choose between the remaining two by asking: *which one is more reliable, more targeted, and at the correct scope?*

## 3. Active recall beats re-reading

* After each domain page, close it and write the 5 key decision rules from memory.
* Use the collapsible **Check yourself** boxes at the end of every domain page.
* Re-attempt missed practice questions 48 hours later.

## 4. Build something small

Reading about hooks is not the same as seeing a PostToolUse hook fail your build. The three [labs](../labs/index.md) take about 1–2 hours each, and they are the fastest way to make L3 concepts stick.

## 5. Weight your time by the blueprint

Spend time roughly in proportion to domain weight (27 / 20 / 20 / 18 / 15%), then add extra time for your personal weak areas. See [Study Plans](../architect/study-plan.md).
