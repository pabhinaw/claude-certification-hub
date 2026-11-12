from qlib import Q

# The hub's original 20 practice questions, converted into the bank format.

Q("D1", "S1", "Prerequisites", """
A retailer's support agent occasionally calls process_refund before verify_customer. Policy says identity must be verified first. What is the MOST reliable fix?""",
  "Gate process_refund in code (or a PreToolUse hook) so it returns a precondition error until verification has succeeded",
  "Ordering that matters must be enforced in code, not prose.",
  [("Add 'ALWAYS verify the customer first' to the system prompt in capital letters", "Improves the odds; guarantees nothing."),
   ("Add a few-shot example showing verification before refund", "Guides behaviour; doesn't enforce it."),
   ("Switch to a larger model", "Doesn't address the missing enforcement.")])

Q("D1", "S1", "Hooks", """
A refund request is for 3,500 and the agent's limit is 2,000. Where should the limit be enforced?""",
  "In a PreToolUse hook that denies over-limit calls and returns guidance to escalate",
  "PreToolUse blocks before execution.",
  [("In the tool description of process_refund", "Advisory."),
   ("In CLAUDE.md", "Advisory."),
   ("In a PostToolUse hook that reverses over-limit refunds", "Acts after money has moved.")])

Q("D5", "S1", "Escalation", """
Mid-conversation, a customer writes "Stop. I want to talk to a real person." The agent has a likely fix ready. What should happen?""",
  "Escalate immediately with a structured handoff package",
  "Explicit requests for a human are honoured immediately, with context passed on.",
  [("Apply the fix, then offer escalation if they're still unhappy", "Ignores the explicit request."),
   ("Ask the customer to confirm they really want a human", "Adds friction."),
   ("Run sentiment analysis to decide", "The explicit request is the trigger.")], level=1)

Q("D1", "S1", "Termination", """
Some support sessions end with a friendly closing message but no refund, no resolution record and no escalation. Best safeguard?""",
  "After the loop ends for any reason, check for a resolution or escalation record and auto-escalate with a handoff package if neither exists",
  "An orchestration-layer guarantee covers every exit path.",
  [("Increase max_tokens", "Unrelated to the outcome."),
   ("Instruct the model never to end without resolving", "Not a guarantee."),
   ("Raise the maximum iteration count", "More time isn't a guaranteed outcome.")])

Q("D1", "S3", "Subagents", """
A coordinator delegates "find 2025–26 market data" to a search subagent, which returns irrelevant results because it didn't know the target market. Root cause?""",
  "Subagents don't inherit the coordinator's context, and the brief didn't include the market",
  "Context must be passed explicitly.",
  [("The subagent's model is too small", "It still couldn't see missing context."),
   ("The search tool description is too long", "Not the cause."),
   ("tool_choice was set to auto", "Unrelated to context.")])

Q("D1", "S3", "Decomposition", """
Final research reports regularly miss whole subtopics. Best fix?""",
  "Have the coordinator check coverage against the question and dynamically spawn follow-up subtasks for gaps",
  "The problem is overly narrow decomposition.",
  [("Have subagents return longer outputs", "Doesn't add unassigned subtopics."),
   ("Use a single agent instead", "Loses the benefits of delegation without fixing coverage."),
   ("Lower the temperature", "Unrelated.")])

Q("D5", "S3", "Provenance", """
Two credible sources give different market sizes for the same year. What should the synthesis do?""",
  "Present both with source attribution and dates, noting the conflict",
  "Preserve provenance and annotate conflicts.",
  [("Use the larger figure", "Arbitrary."),
   ("Average them", "Unsupported figure."),
   ("Drop the figure", "Loses information.")])

Q("D5", "S3", "Error propagation", """
A research subagent's web search fails with a timeout. What should it return?""",
  "A structured error: transient, retryable, and what was attempted",
  "An access failure is not an empty result.",
  [("An empty result list", "Looks like 'nothing found'."),
   ("'No relevant sources found.'", "Misrepresents the failure."),
   ("Results from its training knowledge instead", "Silent substitution.")])

Q("D3", "S2", "Quality hooks", """
The team wants every file Claude edits to be formatted with Prettier, without exception. Best approach?""",
  "A PostToolUse hook matching Edit|Write that runs Prettier on the edited file",
  "'Without exception' means a deterministic hook.",
  [("CLAUDE.md: 'Always run Prettier after editing'", "Advisory."),
   ("A custom /format command", "Relies on a person remembering."),
   ("A Skill describing the formatting rules", "Guidance, not enforcement.")])

Q("D3", "S2", "Rules", """
Rules for database migration files should apply only under db/migrations/. Best location?""",
  ".claude/rules/migrations.md with paths: [\"db/migrations/**\"]",
  "A path-scoped rule loads only when relevant and is shared with the team.",
  [("The root CLAUDE.md", "Loads everywhere."),
   ("~/.claude/CLAUDE.md", "Personal and not path-scoped."),
   ("Inline in every prompt", "Repetitive and error-prone.")])

Q("D3", "S4", "Commands", """
A developer wants a personal /standup command available in every project, not shared with the team. Where should it go?""",
  "~/.claude/commands/standup.md",
  "Personal and all projects means the user directory.",
  [(".claude/commands/standup.md", "Shared with the team."),
   (".mcp.json", "MCP configuration."),
   (".claude/settings.json", "Settings file.")], level=1)

Q("D3", "S2", "Advice vs enforcement", """
CLAUDE.md says "Never edit anything in /vendor", yet Claude sometimes edits it. Best restructure?""",
  "Move it to a permissions deny rule for Edit and Write on ./vendor/** (or a PreToolUse hook)",
  "'Never' means enforcement.",
  [("Repeat the instruction three times", "Emphasis isn't enforcement."),
   ("Move it into a Skill", "Still guidance."),
   ("Use plan mode for every task", "Doesn't prevent the edit.")])

Q("D3", "S2", "Plan mode", """
Which task is the BEST candidate for plan mode?""",
  "Replacing the authentication system across 30 files, with security-team sign-off required",
  "Broad, high-risk, needs stakeholder review.",
  [("Renaming a local variable in one function", "Small and reversible."),
   ("Fixing a typo in the README", "Trivial."),
   ("Adding a missing import", "Trivial.")], level=1)

Q("D2", "S4", "MCP scope", """
The team's issue-tracker MCP server must be available to everyone who clones the repo, and it needs an API token. What is the right setup?""",
  "Project scope .mcp.json, with the token referenced as ${TRACKER_TOKEN}",
  "Shared means project scope; secrets go through env-var expansion.",
  [("User scope, with the token in ~/.claude.json", "Not shared."),
   ("Project scope .mcp.json with the token hard-coded", "Leaks a secret."),
   ("Local scope on each laptop", "Not shared.")])

Q("D3", "S5", "CI/CD", """
Claude Code runs in CI to review PRs, and the pipeline must parse its findings. Best invocation?""",
  "claude -p \"<review prompt>\" --output-format json",
  "Non-interactive with machine-readable output.",
  [("Interactive claude with a human copying the results", "Not automatable."),
   ("The Message Batches API", "Wrong for a blocking merge check."),
   ("Asking Claude to 'print findings clearly'", "Not reliably parseable.")])

Q("D4", "S6", "Structured output", """
An invoice pipeline's parser crashes when Claude replies "Here are the fields:" followed by JSON. Most reliable fix?""",
  "Define a record_invoice tool with the schema and set tool_choice to force it",
  "Tool plus schema plus forced tool_choice gives the strictest compliance among these options.",
  [("Instruct 'Output JSON only'", "Not a guarantee."),
   ("Prefill the reply with '{'", "Helps, but unvalidated."),
   ("Strip text before the first '{' with a regex", "Fragile.")])

Q("D4", "S6", "Schema design", """
About 30% of invoices have no PO number, yet the extracted po_number is never empty, and audits find invented values. Fix?""",
  "Make po_number nullable or optional, describe 'null if absent', and add a few-shot example with a missing PO",
  "Required fields force guessing.",
  [("Retry extraction until a PO number is found", "Retrying can't create data."),
   ("Lower the temperature", "Doesn't remove the pressure to fill a required field."),
   ("Use a larger model", "Same pressure, same problem.")])

Q("D4", "S6", "Retry loops", """
Validation finds invoice_date = "5th March". What should the retry contain?""",
  "The original document plus the specific error: must be ISO 8601 YYYY-MM-DD, got '5th March'",
  "Specific, actionable feedback.",
  [("'Try again.'", "No information."),
   ("Nothing; switch models", "Doesn't address the format."),
   ("A request to double-check all fields", "Unfocused.")])

Q("D5", "S6", "Review routing", """
Overall extraction accuracy is 97%, but finance reports frequent wrong bank details on scanned forms. Best review design?""",
  "Route to review by field-level calibrated confidence for critical fields plus document characteristics, with stratified sampling of accepted items",
  "Risk-based, field-level routing.",
  [("Randomly review 5% of all documents", "Misses targeted risk."),
   ("Review everything below 97% accuracy", "Accuracy isn't known per document at run time."),
   ("Ask the model for an overall confidence score and review below 0.9", "Hides field-level issues.")])

Q("D4", "S6", "Batch", """
Each night, 80,000 archived contracts must be re-tagged for a report read the next morning. Which API?""",
  "Message Batches API, with a custom_id per contract",
  "Non-blocking, high volume, about 50% cheaper, results within 24 hours.",
  [("Synchronous Messages API with 50 parallel workers", "Costs more for no benefit."),
   ("Streaming", "For latency of single responses."),
   ("Claude Code in plan mode", "Wrong tool.")], level=1)
