# Practice Questions <span class="level-badge">L4</span>

20 **original** scenario-style questions (not real exam items). Try each one before expanding the answer. Target: **17/20 or better**, and be able to say why each wrong option is wrong.

---

## Scenario A: Customer Support Resolution Agent

*A retailer's support agent uses `verify_customer`, `lookup_order`, `process_refund` and `escalate_to_human`. Policy: identity must be verified before any refund; the agent may refund up to 2,000 INR.*

**Q1.** In logs, the agent occasionally calls `process_refund` before `verify_customer`. What is the MOST reliable fix?

- A. Add "ALWAYS verify the customer first" to the system prompt in capital letters
- B. Add a few-shot example showing verification before refund
- C. Gate `process_refund` in code (or a PreToolUse hook) so it returns a precondition error until verification has succeeded
- D. Switch to a larger model

??? success "Answer: C"
    Ordering that matters must be **enforced programmatically**. A and B improve the odds but guarantee nothing; D doesn't address the design.

**Q2.** A refund request is for 3,500 INR. Where should the 2,000 INR limit be enforced?

- A. In the tool description of `process_refund`
- B. In a PreToolUse hook that denies amounts above the limit and returns guidance to escalate
- C. In CLAUDE.md
- D. In a PostToolUse hook that reverses refunds above the limit

??? success "Answer: B"
    PreToolUse blocks **before** execution. D acts after money has moved. A and C are advisory.

**Q3.** Mid-conversation the customer writes: "Stop. I want to talk to a real person." The agent has a likely fix ready. What should happen?

- A. Apply the fix, then offer escalation if the customer is still unhappy
- B. Escalate immediately with a structured handoff package
- C. Ask the customer to confirm they really want a human
- D. Run sentiment analysis to decide

??? success "Answer: B"
    Explicit requests for a human are honoured immediately, with context passed on so the customer doesn't have to repeat themselves.

**Q4.** Some sessions end with a friendly closing message but no refund, no resolution record and no escalation. Best safeguard?

- A. Increase `max_tokens`
- B. Instruct the model never to end without resolving
- C. After the agent loop ends, for any reason, check for a resolution or escalation record and auto-escalate with a handoff package if neither exists
- D. Raise the max iteration count

??? success "Answer: C"
    An orchestration-layer guarantee covers every termination path. The others don't guarantee the outcome.

---

## Scenario B: Multi-Agent Research System

**Q5.** The coordinator delegates "find 2025–26 market data" to a search subagent, which returns irrelevant results because it didn't know the target market. Root cause?

- A. The subagent's model is too small
- B. Subagents don't inherit the coordinator's context; the brief didn't include the market
- C. The search tool description is too long
- D. `tool_choice` was `auto`

??? success "Answer: B"
    Context must be passed **explicitly** in the delegation brief.

**Q6.** Final reports regularly miss whole subtopics. Best fix?

- A. Have subagents return longer outputs
- B. Have the coordinator check coverage against the research question and dynamically spawn follow-up subtasks for gaps
- C. Use a single agent instead
- D. Lower temperature

??? success "Answer: B"
    The issue is overly narrow decomposition. **Dynamic, adaptive decomposition** at the coordinator fixes it.

**Q7.** Two credible sources give different market sizes. What should the synthesis do?

- A. Use the larger figure
- B. Average them
- C. Present both with source attribution and dates, noting the conflict
- D. Drop the figure

??? success "Answer: C"
    Preserve provenance and **annotate conflicts**.

**Q8.** A subagent's web search fails with a timeout. What should it return?

- A. An empty result list
- B. "No relevant sources found"
- C. A structured error: transient, retryable, what was attempted
- D. Results from its training knowledge instead

??? success "Answer: C"
    Access failure ≠ empty result. Never suppress errors or silently substitute.

---

## Scenario C: Claude Code for a Team

**Q9.** The team wants every file Claude edits to be formatted with Prettier, without exception. Best approach?

- A. CLAUDE.md: "Always run Prettier after editing"
- B. A PostToolUse hook matching `Edit|Write` that runs Prettier on the edited file
- C. A custom `/format` command
- D. A Skill describing the formatting rules

??? success "Answer: B"
    "Without exception" → deterministic hook. C relies on a person remembering; A and D are advisory.

**Q10.** Rules for database migration files should apply only under `db/migrations/`. Best location?

- A. Root CLAUDE.md
- B. `~/.claude/CLAUDE.md`
- C. `.claude/rules/migrations.md` with `paths: ["db/migrations/**"]`
- D. Inline in every prompt

??? success "Answer: C"
    Path-scoped rule: loads only when relevant and is shared with the team.

**Q11.** A developer wants a personal `/standup` command available in every project, not shared with the team.

- A. `.claude/commands/standup.md`
- B. `~/.claude/commands/standup.md`
- C. `.mcp.json`
- D. `.claude/settings.json`

??? success "Answer: B"
    Personal + all projects → user directory.

**Q12.** CLAUDE.md says "Never edit anything in `/vendor`". Claude still sometimes edits it. Best restructure?

- A. Repeat the instruction three times
- B. Move it to a permissions **deny** rule for Edit/Write on `./vendor/**` (or a PreToolUse hook)
- C. Move it to a Skill
- D. Use plan mode for every task

??? success "Answer: B"
    "Never" = enforcement → settings permissions/hooks.

**Q13.** Which task is the BEST candidate for plan mode?

- A. Rename a local variable in one function
- B. Fix a typo in the README
- C. Replace the authentication system across 30 files, with security-team sign-off required
- D. Add a missing import

??? success "Answer: C"
    Broad, high-risk, needs stakeholder review.

**Q14.** The team's issue-tracker MCP server must be available to everyone who clones the repo, and it needs an API token.

- A. User scope with the token in `~/.claude.json`
- B. Project scope `.mcp.json`, with the token referenced as `${TRACKER_TOKEN}`
- C. Project scope `.mcp.json` with the token hard-coded
- D. Local scope on each laptop

??? success "Answer: B"
    Shared → project scope; secrets → env-var expansion.

---

## Scenario D: CI/CD and Extraction

**Q15.** Claude Code runs in CI to review PRs, and the pipeline must parse its findings. Best invocation?

- A. Interactive `claude`, with a human copying the results
- B. `claude -p "<review prompt>" --output-format json`
- C. The Batch API
- D. Ask Claude to "print findings clearly"

??? success "Answer: B"
    Non-interactive + machine-readable output. (Batch is wrong for a blocking merge check.)

**Q16.** An invoice pipeline's parser crashes when Claude replies "Here are the fields:" followed by JSON. Most reliable fix?

- A. Instruct "Output JSON only"
- B. Prefill with `{`
- C. Define a `record_invoice` tool with the schema and set `tool_choice` to force it
- D. Strip text before the first `{` with a regex

??? success "Answer: C"
    Tool + schema + forced `tool_choice` gives the strictest compliance.

**Q17.** About 30% of invoices have no PO number, yet the extracted `po_number` is never empty, and audits find invented values. Fix?

- A. Retry extraction until a PO number is found
- B. Make `po_number` nullable/optional, describe "null if absent", and add a few-shot example with a missing PO
- C. Lower the temperature
- D. Use a larger model

??? success "Answer: B"
    Required fields force guessing. Allow `null` explicitly.

**Q18.** A validation step finds `invoice_date = "5th March"`. What should the retry contain?

- A. "Try again."
- B. The original document plus the specific error: must be ISO 8601 `YYYY-MM-DD`, got "5th March"
- C. Nothing; switch models
- D. A request to double-check all fields

??? success "Answer: B"
    Specific, actionable error feedback.

**Q19.** Overall extraction accuracy is 97%, but finance reports frequent wrong bank details on scanned forms. Best review design?

- A. Randomly review 5% of all documents
- B. Review everything below 97%
- C. Route to review by field-level calibrated confidence for critical fields, plus document characteristics (scanned forms), with stratified sampling of auto-accepted items
- D. Ask the model for an overall confidence score and review those below 0.9

??? success "Answer: C"
    Risk-based routing at **field level** with document characteristics, and stratified QA.

**Q20.** Each night, 80,000 archived contracts must be re-tagged for a report read the next morning. API choice?

- A. Synchronous Messages API with 50 parallel workers
- B. Message Batches API, with `custom_id` per contract
- C. Streaming
- D. Claude Code in plan mode

??? success "Answer: B"
    Non-blocking, high-volume, ≈50% cheaper; results within 24 h; correlate by `custom_id`.

---

## Score yourself

| Score | Next step |
|---|---|
| 18–20 | Book the exam. Review the [Cheat Sheet](cheat-sheet.md) |
| 14–17 | Revisit the domains of the questions you missed, then retry in 48 h |
| < 14 | Work through the domain pages and [labs](../labs/index.md) before re-attempting |
