# Commonly Missed Topics <span class="level-badge">L4</span>

These five objectives are where experienced candidates most often lose marks: they *feel* familiar, but the exam wants a specific, deterministic answer. This list comes from the author's own score report (see [My Exam Journey](../about/my-journey.md)) and from community feedback.

| Rank | Objective | Why people miss it |
|---|---|---|
| 1 | `tool_choice` + **sequencing** multi-tool workflows | they know `tool_choice` but not how to guarantee *order* |
| 2 | **Human review routing** | default instinct is "random sample X%" |
| 3 | **Extraction schemas** that avoid fabrication | making fields required "for completeness" |
| 4 | **Iterative refinement** workflows | giving vague, unbatched feedback |
| 5 | **Session resumption** | re-running everything or trusting stale context |

---

## 1. tool_choice + sequencing

**The gap:** knowing that `tool_choice` *can* force a tool, but not combining it with ordering guarantees.

**Remember the toolkit:**

| Goal | Mechanism |
|---|---|
| A tool call must happen (no prose reply) | `tool_choice: {"type":"any"}` |
| *This specific* tool must be called (structured output, or step 1) | `tool_choice: {"type":"tool","name":"X"}` |
| B must never run before A | gate B in code or a PreToolUse hook → structured *precondition* error naming A |
| Step 1 must be A | force A on the first request, then switch to `auto` |
| B shouldn't even be considered yet | expose B in `tools` only after A's output exists |
| Avoid A and B in the same turn | `disable_parallel_tool_use: true` |

**Spot it in a question:** *"…sometimes calls `create_shipment` before `validate_address`…"* or *"…downstream parser fails when Claude replies in text…"*. Look for the option that **forces and/or gates**; reject "update the prompt" options.

[Full explanation → D2](domains/d2-tool-design-mcp.md#tool_choice-and-tool-sequencing)

---

## 2. Human review routing

**The gap:** treating review as quality *sampling* instead of risk *routing*.

**The answer shape:** route to humans based on **(a) field-level confidence** (calibrated against labelled data), **(b) document characteristics** (scan quality, template, source history), **(c) field-level ambiguity** (conflicts, partial legibility, null-but-expected), weighted by **field criticality**. Then use **stratified** (not simple random) sampling of auto-accepted items to monitor quality and recalibrate.

**Wrong-answer smell:** "randomly sample 10%", "review everything below 90% overall accuracy", "trust the model's single overall confidence score".

[Full explanation → D5](domains/d5-context-reliability.md#human-review-routing)

---

## 3. Extraction schemas that don't force guesses

**The gap:** forgetting that a *required* field with no source value **invites fabrication**.

**Pattern:** nullable types for optional data · enums with `unknown`/`not_stated` · `other` + free-text detail · descriptions that say "null if absent, never infer" · few-shot examples showing `null`.

[Full explanation → D4](domains/d4-prompt-structured-output.md#schema-design-that-prevents-fabrication)

---

## 4. Iterative refinement

**The gap:** sending "still not right, try again".

**Pattern:** concrete **input → expected output** examples; **targeted** feedback naming the exact failure; **batch interacting issues** into one message so they're evaluated together, but handle **independent** issues sequentially; use tests as the oracle; use the interview pattern for unclear requirements.

[Full explanation → D3](domains/d3-claude-code.md#iterative-refinement)

---

## 5. Session resumption

**The gap:** choosing between "start over" and "just resume" when the best answer is in between.

**Pattern:** resume, **inject a concise summary** of prior findings/decisions, and **re-analyse only what changed** since the last session (for example files in `git diff`). Start fresh with a summary when the old context is long or stale; fork to explore alternatives.

[Full explanation → D1](domains/d1-agentic-architecture.md#session-state-resume-fork-or-fresh-start)
