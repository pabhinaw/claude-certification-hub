from qlib import Q

# ======================= D2 · Tool Design & MCP Integration =======================

# --- Tool descriptions ---
Q("D2", "S4", "Tool descriptions", """
Two tools, search_docs and search_tickets, are frequently confused by the agent. What is the most effective first fix?""",
  "Expand both descriptions: what each searches, when to use it, when to use the other instead, and the input format",
  "Descriptions are the main signal Claude uses to choose between tools.",
  [("Rename them search_a and search_b", "Less meaningful names make selection worse."),
   ("Merge them into one tool with a 'type' parameter, with no other change", "Can help, but the ambiguity simply moves into the parameter."),
   ("Set tool_choice to auto", "auto is already the default and doesn't disambiguate.")], level=1)

Q("D2", "G", "Tool descriptions", """
Which tool description is likely to produce the most reliable selection?""",
  "'Look up ONE order's shipping status by order ID (format ORD-#####). Use for where-is-my-order questions; not for refunds (use process_refund).'",
  "It states the purpose, scope, input format, when to use it and the alternative.",
  [("'Order tool.'", "Gives Claude almost nothing to decide with."),
   ("'Powerful, flexible tool for anything related to orders.'", "Vague and overlapping by design."),
   ("'Calls GET /v2/orders/{id} on the fulfilment service.'", "Implementation details don't say when to use it.")])

Q("D2", "S1", "Tool descriptions", """
The system prompt says "Always search the knowledge base first". The agent now calls search_kb even for order-status questions where lookup_order fits. What is the likely cause and fix?""",
  "The prompt skews selection; move selection guidance into tool descriptions and keep the system prompt neutral",
  "Keyword-heavy instructions in the system prompt can override good tool choice.",
  [("The model is too small; switch to a larger one", "Larger models still follow the instruction to search first."),
   ("lookup_order needs a shorter description", "Shortening it reduces clarity."),
   ("Use tool_choice any", "Forces some tool call; doesn't fix which one.")])

Q("D2", "S4", "Tool descriptions", """
A tool takes a date parameter, and the agent often sends values like "next Tuesday". Best fix?""",
  "Specify the format in the parameter schema and description (e.g. ISO 8601 YYYY-MM-DD, with an example)",
  "Clear input specifications reduce malformed calls.",
  [("Reject the calls silently", "The agent never learns what was wrong."),
   ("Add a system-prompt line saying dates matter", "Too vague to change the format."),
   ("Remove the date parameter", "Loses needed functionality.")])

Q("D2", "S3", "Tool descriptions", """
A research agent has web_search and internal_wiki_search. It keeps searching the public web for internal policy questions. Best fix?""",
  "Add explicit disambiguation to both descriptions, e.g. 'For company policies and internal processes use internal_wiki_search'",
  "Explicit use-case boundaries in descriptions guide selection between similar tools.",
  [("Remove web_search entirely", "Loses legitimate capability."),
   ("Lower the temperature", "Doesn't add the missing guidance."),
   ("Give internal_wiki_search a longer name", "A name alone doesn't set boundaries.")])

# --- Structured errors ---
Q("D2", "S1", "Tool errors", """
A payment tool fails because the card network is temporarily unavailable. What should the tool_result contain?""",
  "is_error true, category 'transient', retryable true, and a suggested action such as retrying shortly",
  "Type-specific, actionable errors let the agent choose the right recovery.",
  [("The text 'Error'", "Gives the agent nothing to act on."),
   ("A success result with status 'pending'", "Misrepresents the failure."),
   ("A Python stack trace", "Noisy and doesn't say whether to retry.")])

Q("D2", "S1", "Tool errors", """
A refund is rejected because the 30-day refund window has passed. How should the tool report this?""",
  "As a business-rule error that is not retryable, with guidance to explain the policy or escalate",
  "Retrying won't change a policy outcome; the agent needs to know that.",
  [("As a transient error so the agent retries", "Retrying a policy rejection wastes calls and confuses the user."),
   ("As success with amount 0", "Hides the rejection."),
   ("As a validation error asking for a new order ID", "The ID was valid; the policy blocks it.")])

Q("D2", "S3", "Tool errors", """
A database tool returns an empty list both when a customer has no orders and when the query failed due to permissions. Why is this a problem?""",
  "The agent can't distinguish 'no data' from 'couldn't access', so it may state false conclusions confidently",
  "Access failure and empty result must be reported differently.",
  [("Empty lists use more tokens than errors", "Token cost isn't the issue."),
   ("The API rejects empty tool results", "Empty results are allowed; they're just misleading here."),
   ("It isn't a problem as long as is_error is false", "is_error false is exactly what makes the failure invisible.")])

Q("D2", "G", "Tool errors", """
Which set of fields makes an MCP or tool error most useful to an agent?""",
  "Error category, whether it's retryable, a human-readable message, and a suggested next action",
  "These tell the agent what happened and what to do next.",
  [("HTTP status code only", "Too little context for a decision."),
   ("A unique error ID only", "Useful for logs, not for the agent's next step."),
   ("The full server log for the request", "Floods context without guidance.")])

Q("D2", "S4", "Tool errors", """
An agent calls create_issue without a required 'project' field. What should the tool return?""",
  "A validation error naming the missing field and the expected format, marked as retryable after correction",
  "The agent can fix the input and retry.",
  [("A permission error", "Mislabels the cause."),
   ("Nothing; the agent will notice eventually", "It won't know why the issue wasn't created."),
   ("A transient error suggesting a retry in 60 seconds", "Waiting won't fix a missing field.")])

Q("D2", "S1", "Tool errors", """
The agent receives a permission error when trying to view another customer's account. What should it do?""",
  "Stop that path and explain or escalate; don't retry or try to work around it",
  "Permission errors are non-retryable and signal a boundary.",
  [("Retry with a different tool that has broader access", "Working around access controls is unsafe."),
   ("Retry three times with backoff", "Permissions don't change with time."),
   ("Ask the customer for an admin password", "Clearly inappropriate.")])

# --- tool_choice ---
Q("D2", "S6", "tool_choice", """
A ticket-routing service needs every response to be a call to classify_ticket. Occasionally Claude asks a clarifying question instead, and routing fails. Fix?""",
  "Set tool_choice to {\"type\": \"tool\", \"name\": \"classify_ticket\"}",
  "Forcing the named tool guarantees the call.",
  [("Add 'Always call record_invoice' to the prompt", "Not a guarantee."),
   ("Set tool_choice to auto", "auto lets Claude reply without tools."),
   ("Set tool_choice to none", "Prevents tool calls entirely.")], level=1)

Q("D2", "G", "tool_choice", """
Which tool_choice setting requires Claude to call one of the provided tools but lets it choose which?""",
  "{\"type\": \"any\"}",
  "any forces some tool call without naming which.",
  [("{\"type\": \"auto\"}", "auto lets Claude decide whether to call a tool at all."),
   ("{\"type\": \"tool\", \"name\": \"...\"}", "That forces one specific tool."),
   ("{\"type\": \"none\"}", "That prevents tool use.")], level=1)

Q("D2", "G", "tool_choice", """
Manual extended thinking is enabled and a developer sets tool_choice to {"type": "tool", "name": "extract"}. What happens?""",
  "The request isn't supported: with manual extended thinking only auto and none are compatible",
  "Forced tool modes conflict with manual extended thinking.",
  [("Claude thinks first, then calls extract", "Forced modes aren't supported with manual thinking."),
   ("Thinking is silently disabled for that request", "The combination is rejected, not silently changed."),
   ("Claude ignores tool_choice and answers in text", "The combination isn't accepted.")])

Q("D2", "G", "tool_choice", """
With tool_choice set to any or to a named tool, what will you NOT get in the response?""",
  "Natural-language text before the tool_use block, because the API prefills the turn to force a tool call",
  "Forced modes skip explanatory text before the call.",
  [("A tool_use block", "A tool_use block is guaranteed."),
   ("A stop_reason", "Responses always have a stop_reason."),
   ("Usage information", "Usage is always returned.")])

Q("D2", "S6", "tool_choice", """
You need exactly one tool call per response when forcing a tool. Which setting helps?""",
  "disable_parallel_tool_use: true",
  "With any or tool, it ensures exactly one tool call.",
  [("max_tokens: 1", "Truncates output; doesn't control tool count."),
   ("temperature: 0", "Doesn't limit parallel tool calls."),
   ("tool_choice none", "Prevents tools entirely.")])

Q("D2", "S1", "tool_choice", """
A support agent should usually chat but must use tools when needed. What is the right tool_choice?""",
  "auto",
  "auto lets Claude decide when tools are needed: the normal setting for conversational agents.",
  [("any", "Would force a tool call even for simple chat."),
   ("tool with lookup_order", "Forces one tool on every turn."),
   ("none", "Would prevent necessary tool calls.")], level=1)

# --- Sequencing ---
Q("D2", "S4", "Sequencing", """
A workflow requires validate_address → quote_rates → create_shipment. The agent sometimes skips validation. Which combination is strongest?""",
  "Force validate_address on the first turn, then gate later tools in code so they return precondition errors if earlier steps are missing",
  "Forcing fixes the common skip; gating covers every later turn.",
  [("Describe the order in each tool's description", "Guidance only."),
   ("Order the tools array as validate, quote, create", "Array order doesn't enforce call order."),
   ("Set tool_choice any on every turn", "Forces a call, not the right one or the right order.")])

Q("D2", "S4", "Sequencing", """
Claude requests get_customer and get_orders in the same turn, but get_orders needs the customer ID from get_customer. What helps most?""",
  "disable_parallel_tool_use plus a gate that rejects get_orders until a customer ID exists",
  "Prevents simultaneous calls and enforces the dependency.",
  [("Increase max_tokens", "Unrelated to tool ordering."),
   ("Run both calls and discard the get_orders result if it fails", "Wasteful and error-prone."),
   ("Merge both tools into one", "Sometimes reasonable, but it loses separation and doesn't address the general pattern.")])

Q("D2", "S1", "Sequencing", """
Why is forcing the first tool with tool_choice NOT enough on its own to guarantee correct ordering in a long conversation?""",
  "tool_choice applies per request; later turns use auto, where out-of-order calls are still possible",
  "Ordering across a whole session needs a gate on every call.",
  [("Because tool_choice is ignored after the first request in a session", "It's honoured on each request where it's set."),
   ("Because forced tools can't receive tool_result blocks", "They can."),
   ("Because tool_choice only works with streaming", "It works with or without streaming.")])

Q("D2", "S4", "Sequencing", """
With extended thinking enabled, how do you enforce that tool B never runs before tool A?""",
  "Keep tool_choice auto and enforce the order with a code gate or PreToolUse hook",
  "Forced tool modes aren't compatible with manual thinking, so enforcement must live in code.",
  [("Use tool_choice tool for A on every turn", "Not supported with manual thinking."),
   ("Disable thinking for every request", "Gives up a needed capability unnecessarily."),
   ("Rely on the thinking process to plan the order", "Better reasoning still isn't a guarantee.")])

Q("D2", "S1", "Sequencing", """
After a gate returns a precondition error ("call verify_customer first"), what typically happens next in a well-designed loop?""",
  "Claude reads the structured error and calls verify_customer, then retries the original action",
  "Structured errors enable self-correction.",
  [("The session ends automatically", "The error is recoverable."),
   ("The API retries the call itself", "The API doesn't run client tools."),
   ("The gate is disabled for the rest of the session", "The gate should apply on every call.")])

# --- Tool count ---
Q("D2", "S4", "Tool count", """
An agent with 18 overlapping tools makes frequent wrong selections. What does good practice suggest?""",
  "Give each agent a small, focused tool set (about 4–5 relevant tools), splitting work across specialised agents",
  "Fewer, distinct tools improve routing.",
  [("Add more tools so each one is more specific", "More choice usually worsens selection."),
   ("Sort the tools alphabetically", "Ordering doesn't fix overlap."),
   ("Raise the temperature to encourage exploration", "Increases randomness, not accuracy.")])

# --- MCP scopes & auth ---
Q("D2", "S4", "MCP scope", """
Every engineer who clones the repo should automatically get the team's issue-tracker MCP server. Where should it be configured?""",
  "Project scope: .mcp.json in the repository root, committed to version control",
  "Project scope is the shared, versioned location.",
  [("User scope in each engineer's ~/.claude.json", "Not shared through the repo."),
   ("Local scope (the default)", "Private to one person and one project."),
   ("In CLAUDE.md as a server URL", "CLAUDE.md is guidance, not MCP configuration.")], level=1)

Q("D2", "S4", "MCP scope", """
A developer wants to try an experimental MCP server across all of their own projects without affecting teammates. Which scope?""",
  "User scope",
  "User scope applies to all of that person's projects and isn't shared.",
  [("Project scope", "Would share it with the team via the repo."),
   ("Local scope", "Applies to one project only."),
   ("Enterprise managed config", "Organisation-wide; far too broad.")])

Q("D2", "S4", "MCP auth", """
The shared .mcp.json needs an API token. What is the right way to supply it?""",
  "Reference an environment variable such as ${TRACKER_TOKEN}, set by each user outside the repo",
  "Env-var expansion keeps secrets out of version control.",
  [("Hard-code the token so it works for everyone", "Leaks a secret into the repo."),
   ("Put the token in CLAUDE.md", "Also committed, and not configuration."),
   ("Email the token to the team", "Insecure and still requires manual setup.")], level=1)

Q("D2", "S4", "MCP discovery", """
After adding an MCP server, Claude never uses its tools. What should you check first?""",
  "Whether the server is connected and its tools are discovered (e.g. claude mcp list or /mcp), including required environment variables",
  "Many 'ignored tool' issues are really connection or configuration problems.",
  [("Whether the tool descriptions are long enough", "Check discovery before tuning descriptions."),
   ("Whether the model supports MCP", "MCP is handled by the client harness."),
   ("Whether prompt caching is on", "Unrelated.")])

Q("D2", "S4", "MCP scope", """
The same server name is defined at local, project and user scope with different URLs. Which one does Claude Code use?""",
  "The local-scope definition",
  "Precedence is local, then project, then user.",
  [("The project-scope definition", "Local overrides project."),
   ("The user-scope definition", "User has the lowest of the three."),
   ("All three, merged", "The winning entry is used; definitions aren't merged.")])

# --- MCP primitives & transports ---
Q("D2", "S4", "MCP primitives", """
An agent spends many calls listing and searching just to learn which runbooks exist. Which MCP feature fits best?""",
  "Expose the runbook catalogue as a resource",
  "Resources provide read-only context such as catalogues in one read.",
  [("Add more search tools", "Increases exploratory calls."),
   ("Expose it as a prompt", "Prompts are user-invoked templates."),
   ("Increase the agent's iteration cap", "Allows more waste rather than removing it.")])

Q("D2", "S4", "MCP primitives", """
A team wants a reusable, parameterised workflow ("summarise incident {id}") that engineers trigger deliberately. Which MCP primitive fits?""",
  "A prompt",
  "Prompts are user-selected templates, often surfaced as slash commands.",
  [("A tool", "Tools are chosen by the model, not deliberately triggered by users."),
   ("A resource", "Resources are read-only context, not workflows."),
   ("A hook", "Hooks are a Claude Code feature, not an MCP primitive.")])

Q("D2", "S4", "MCP transports", """
A company wants one centrally hosted MCP server used by many engineers. Which transport is the natural fit?""",
  "HTTP (streamable HTTP) as a remote server",
  "Remote, shared servers use HTTP; stdio is for local processes.",
  [("stdio", "Runs as a local process on each machine."),
   ("A shared network drive containing the server script", "Not an MCP transport."),
   ("Email-based polling", "Not an MCP transport.")])

# --- Built-in tools ---
Q("D2", "S2", "Built-in tools", """
You need to find every file named *.test.ts under src/. Which built-in tool fits?""",
  "Glob",
  "Glob matches file paths by pattern.",
  [("Grep", "Grep searches file contents."),
   ("Read", "Read opens a known file."),
   ("Edit", "Edit modifies files.")], level=1)

Q("D2", "S2", "Built-in tools", """
An Edit call fails because the target string appears three times in the file. What is the right recovery?""",
  "Include more surrounding context so the match is unique (or use Read plus Write for larger changes)",
  "Edit requires a unique match.",
  [("Retry the same Edit", "It will fail the same way."),
   ("Use Glob to find the string", "Glob matches file names."),
   ("Delete the file and recreate it from memory", "Risky and loses content.")])

Q("D2", "S2", "Built-in tools", """
What is the most context-efficient way to locate where a function named calculateTax is defined in a large repo?""",
  "Grep for the function name, then Read only the matching file or section",
  "Search first, read narrowly.",
  [("Read every file in src/", "Floods context."),
   ("Glob for *.ts and read the results", "Still reads far too much."),
   ("Ask Claude to recall where it probably is", "Guessing isn't evidence.")])
