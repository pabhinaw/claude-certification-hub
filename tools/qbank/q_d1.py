from qlib import Q

# ======================= D1 · Agentic Architecture & Orchestration =======================

# --- Agent loop & stop_reason ---
Q("D1", "G", "Agent loop", """
An agent loop must decide whether to keep executing tools or return a final answer. Which signal should the code use?""",
  "The response's stop_reason: continue while it is tool_use, finish on end_turn",
  "stop_reason is the structured, reliable signal. tool_use means Claude is waiting for tool results; end_turn means it has finished.",
  [("Whether the reply text contains a phrase such as 'Task complete'", "Parsing prose is brittle: wording varies and can appear mid-task."),
   ("Whether the response contains any text block at all", "Responses can contain text and tool_use blocks together; text doesn't mean the task is done."),
   ("A fixed number of iterations chosen per task type", "An iteration cap is a safety limit, not a completion signal.")], level=1)

Q("D1", "S1", "Agent loop", """
A support agent's response has stop_reason "tool_use" with two tool_use blocks. What must the application send in the next request?""",
  "The assistant turn as returned, then a user turn containing a tool_result for each tool_use_id",
  "Every tool_use block needs a matching tool_result (same tool_use_id), sent in a user message after the assistant turn.",
  [("Only the result of the first tool, since Claude processes one tool at a time", "Claude can request several tools in one turn; all of them need results."),
   ("A new user message summarising both results in plain text, without the assistant turn", "Dropping the assistant turn breaks the tool_use / tool_result pairing."),
   ("Nothing: the API executes client tools automatically and continues", "Client tools are executed by your code, not by the API.")], level=1)

Q("D1", "G", "Agent loop", """
A response comes back with stop_reason "max_tokens" in the middle of a long answer. What is the best handling?""",
  "Treat the output as truncated: raise max_tokens or continue the generation, and never treat it as a finished answer",
  "max_tokens means the output hit your cap, so the answer may be incomplete.",
  [("Treat it like end_turn and show the answer to the user", "The answer is cut off, so showing it as final is a correctness bug."),
   ("Retry the identical request until a different stop_reason appears", "The same limit will usually produce the same truncation."),
   ("Switch to the Message Batches API, which has no output limit", "Batch requests use the same per-request max_tokens behaviour.")])

Q("D1", "S1", "Agent loop", """
A tool call fails with a database timeout. The developer currently skips sending anything back and just calls the model again. What should happen instead?""",
  "Send a tool_result for that tool_use_id with is_error set to true and a structured description of the failure",
  "Claude needs to know the call failed and why, so it can retry, choose another path or escalate.",
  [("Send an empty tool_result so the conversation stays valid", "An empty result looks like success with no data, which leads to confident wrong answers."),
   ("Remove the tool_use block from the assistant turn and resend", "Rewriting history hides the failure and can confuse later turns."),
   ("End the session immediately with an error page", "Many failures are recoverable; the agent should get the chance to retry or escalate.")])

Q("D1", "G", "Agent loop", """
Why should every agent loop have a maximum-iteration limit, and what should happen when it is reached?""",
  "To prevent runaway loops; reaching it should trigger a handled outcome such as escalation with a summary",
  "The cap is a safety net. Hitting it is an event to handle, not a silent exit.",
  [("To save tokens; when reached, the last response is returned as the answer", "The last response may be mid-task, so returning it silently hides the failure."),
   ("It isn't needed if stop_reason is checked correctly", "Agents can still loop, for example by retrying a failing tool repeatedly."),
   ("To make sure the agent finishes within one API call", "Agents legitimately need many calls; the cap bounds them, it doesn't force one.")])

Q("D1", "G", "Agent loop", """
Claude returns stop_reason "refusal" in an automated pipeline. What is the most appropriate design response?""",
  "Handle it as a distinct outcome: log it and route the item for human review rather than blindly retrying",
  "A refusal is a deliberate safety stop; it needs its own handling path.",
  [("Retry with the same input until the model complies", "Repeated retries of a refused request are not an appropriate fix."),
   ("Treat it as end_turn and store the text as the result", "Storing a refusal as a normal result corrupts downstream data."),
   ("Increase max_tokens so the model can finish", "Refusal is unrelated to the token limit.")])

# --- Stateless API ---
Q("D1", "S1", "Stateless API", """
A chat assistant answers the first question correctly but on the second turn has no idea what the user said earlier. The server stores each user message in a database. What is the most likely bug?""",
  "The second request doesn't include the earlier user and assistant messages in the messages array",
  "The Messages API is stateless: each request must contain the conversation history the model should consider.",
  [("The model's context window is too small for two turns", "Two short turns are far below any context limit."),
   ("Prompt caching is disabled", "Caching affects cost and latency, not what the model can see."),
   ("The system prompt should tell Claude to remember previous turns", "No instruction can make the model see messages that weren't sent.")], level=1)

Q("D1", "G", "Stateless API", """
Where does conversation state live in an application built on the Claude Messages API?""",
  "In the application, which resends the relevant history with every request",
  "The API keeps no conversation state between calls; your application owns it.",
  [("On Anthropic's servers, keyed by API key", "The Messages API doesn't store conversations between requests."),
   ("In the model's weights, updated after each turn", "Models are not updated by individual conversations."),
   ("In the prompt cache, which acts as memory", "The cache only reuses identical prefixes you send; it isn't memory.")], level=1)

Q("D1", "S1", "Stateless API", """
A long-running support conversation is approaching the context limit. Which approach keeps the agent accurate on key facts?""",
  "Keep a compact, structured case-facts block (IDs, amounts, decisions) in every request and summarise or trim older turns",
  "Critical facts are preserved verbatim while bulky history is reduced.",
  [("Drop the oldest half of the messages without any summary", "Blind truncation loses identifiers and decisions the agent still needs."),
   ("Ask the user to start a new chat and repeat their problem", "That's a poor experience and loses the verified state."),
   ("Rely on progressive summaries only, regenerated every few turns", "Repeated summarising gradually drops exact values such as amounts and IDs.")])

# --- Coordinator / subagents ---
Q("D1", "S3", "Subagents", """
A search subagent keeps re-running searches the coordinator already completed, wasting time and tokens. What is the best fix?""",
  "Include the coordinator's relevant findings and already-searched sources in the delegation brief",
  "Subagents start with isolated context; they only know what the brief tells them.",
  [("Give the subagent read access to the coordinator's full conversation", "Floods its context and breaks isolation."),
   ("Add a cache in front of the search API", "Saves cost but doesn't stop redundant reasoning steps."),
   ("Use a smaller model for the subagent", "Doesn't address missing context.")])

Q("D1", "S3", "Subagents", """
What is the main architectural benefit of delegating broad exploration to subagents in a multi-agent research system?""",
  "Each subagent spends its own context on exploration and returns only a condensed result, keeping the coordinator's context clean",
  "Context isolation is the key benefit; the coordinator receives summaries instead of raw dumps.",
  [("Subagents share one context window, so information is never duplicated", "Subagents have separate contexts; that's the point."),
   ("Subagents are always cheaper because they use smaller models automatically", "Model choice is configurable, not automatic."),
   ("Subagents remove the need for a coordinator to synthesise results", "The coordinator still owns synthesis and conflict handling.")])

Q("D1", "S3", "Subagents", """
Which delegation brief is most likely to produce a useful subagent result?""",
  "Objective, known facts, scope limits, required output structure, and what to do if blocked",
  "A complete, structured brief compensates for the subagent's isolated context.",
  [("A one-line task title so the subagent can interpret it freely", "Too little context leads to generic or off-target results."),
   ("The coordinator's full conversation history, so nothing is missed", "Dumping everything floods the subagent's context and dilutes the task."),
   ("Only the output format, since the subagent can search for the rest", "Without the objective and known facts it repeats work or drifts.")])

Q("D1", "S3", "Subagents", """
Subagents in a research system return long raw web pages to the coordinator, and the coordinator's quality drops on later steps. Best fix?""",
  "Have subagents return condensed, structured findings with sources instead of raw content",
  "Accumulating raw tool output degrades the coordinator's context. Summaries with provenance keep it focused.",
  [("Give the coordinator a larger context window", "More room delays the problem but keeps irrelevant content in context."),
   ("Have the coordinator re-read every page itself", "That defeats the purpose of delegation."),
   ("Run all subagents sequentially instead of in parallel", "Ordering doesn't change how much raw content arrives.")])

Q("D1", "S4", "Subagents", """
A team builds a single agent with 22 tools covering search, code changes, tickets and deployments. Tool selection errors are frequent. Which redesign is most effective?""",
  "Split responsibilities into specialised subagents, each with the few tools it needs",
  "Fewer, more relevant tools per agent improve selection accuracy and apply least privilege.",
  [("Add a paragraph to the system prompt listing when to use each tool", "Helpful but weaker than reducing the choice set."),
   ("Rename the tools with numeric prefixes so they sort clearly", "Names alone don't fix overlapping responsibilities."),
   ("Set tool_choice to any so a tool is always called", "Forcing a call doesn't help choose the right one.")])

Q("D1", "S3", "Subagents", """
Two subagents return conflicting figures for the same metric. What should the coordinator do?""",
  "Keep both with their sources and dates and flag the conflict in the synthesis",
  "Annotating conflicts preserves provenance and lets readers judge.",
  [("Pick the figure from the subagent that ran last", "Order of completion says nothing about accuracy."),
   ("Average the two figures", "Averaging can produce a number no source supports."),
   ("Drop the metric so the report has no inconsistencies", "Hiding information isn't a fix; it removes value.")])

Q("D1", "S4", "Subagents", """
The main agent never delegates to a well-designed "security-reviewer" subagent defined with the Agent SDK. Which two things should you check first?""",
  "That the parent is allowed to use the subagent tool, and that the subagent's description clearly says when to use it",
  "Delegation needs the subagent tool to be permitted, and the description drives when the parent chooses it.",
  [("That the subagent uses the same model as the parent, and that hooks are disabled", "Model choice and hooks don't prevent delegation."),
   ("That the subagent has every tool the parent has", "Subagents should get fewer tools; this isn't why delegation fails."),
   ("That max_tokens is above 8,000 and caching is enabled", "Neither setting controls delegation.")])

# --- Decomposition ---
Q("D1", "S6", "Decomposition", """
Invoices must always be extracted, validated, then summarised, in that order, with no variation. Which design fits best?""",
  "A fixed pipeline (prompt chain) with each step as a defined stage",
  "Predictable work with known steps suits a fixed pipeline: simpler, cheaper and easier to test.",
  [("A coordinator that dynamically plans subtasks for each invoice", "Dynamic planning adds cost and variability where none is needed."),
   ("One prompt asking Claude to do all three steps however it likes", "Loses the ability to validate between steps."),
   ("Three independent subagents running in parallel", "The steps depend on each other, so they can't run in parallel.")])

Q("D1", "S3", "Decomposition", """
An investigation agent starts with a plan of four checks. After the first check it discovers the fault is in a third-party dependency. What should a well-designed agent do?""",
  "Adapt: generate new subtasks for the dependency and drop checks that are no longer relevant",
  "Open-ended investigation needs dynamic decomposition that responds to findings.",
  [("Finish the original four checks before considering the new finding", "Running a fixed plan regardless of findings wastes effort and misses the cause."),
   ("Stop and report that the plan has failed", "The finding is progress, not failure."),
   ("Restart the whole investigation with a new plan from scratch", "Discards useful work already done.")])

Q("D1", "S3", "Decomposition", """
A coordinator splits "impact of remote work on productivity" into two subtopics only. Reports keep missing major angles. Where is the fix?""",
  "In the coordinator: check coverage against the question and spawn follow-up subtasks for gaps",
  "Overly narrow decomposition is a coordinator responsibility.",
  [("In the subagents: ask each to research more broadly", "Subagents can't know what the coordinator never assigned."),
   ("In the final report: add a disclaimer about scope", "A disclaimer doesn't fix missing coverage."),
   ("In the search tool: return more results per query", "More results on two subtopics don't add new angles.")])

Q("D1", "G", "Decomposition", """
Which statement best describes when to choose dynamic decomposition over a fixed pipeline?""",
  "When the needed steps depend on what is discovered along the way",
  "Dynamic decomposition is for open-ended tasks whose path can't be known up front.",
  [("Whenever the task involves more than three steps", "Many-step tasks can still be fully predictable."),
   ("Whenever the cheapest model is being used", "Model choice doesn't determine the decomposition style."),
   ("Whenever the output must follow a strict schema", "Output format is independent of how work is decomposed.")], level=1)

Q("D1", "S2", "Decomposition", """
A refactoring task across a large codebase has an unknown number of affected modules. Which approach is most efficient?""",
  "Explore first to discover affected modules, then create per-module subtasks based on the findings",
  "Discovery-driven decomposition fits unknown scope.",
  [("Assign one subtask per top-level folder regardless of content", "Fixed splits ignore where the change actually applies."),
   ("Ask Claude to change every file in one pass", "Unscoped changes across a large codebase are risky and flood context."),
   ("Estimate the number of modules and create that many placeholder tasks", "Guessed tasks don't match real dependencies.")])

# --- Prerequisites & gates ---
Q("D1", "S1", "Prerequisites", """
Policy: identity must be verified before an account address can be changed. Logs show the agent occasionally changes addresses first. Most reliable fix?""",
  "Block the change-address tool in code (or a PreToolUse hook) until verification has succeeded, returning a precondition error",
  "Order that matters must be enforced deterministically.",
  [("State the rule in the system prompt in capital letters", "Raises the odds but guarantees nothing."),
   ("Add a few-shot example showing verification first", "Examples influence behaviour; they don't enforce it."),
   ("Lower the temperature", "Randomness isn't the cause; nothing enforces the rule.")])

Q("D1", "S1", "Prerequisites", """
When a gated tool is called too early, what should the gate return to the model?""",
  "A tool_result with is_error true, a precondition category, and the tool to call first",
  "A structured, actionable error lets the agent self-correct.",
  [("A success result with no data", "Fake success misleads the agent."),
   ("Nothing, and the session should stop", "Stopping wastes a recoverable situation."),
   ("A generic 'Error' string", "Doesn't tell the agent what to do next.")])

Q("D1", "S1", "Prerequisites", """
Which approach gives the strongest guarantee that a refund tool can never be executed before identity verification, at any point in a conversation?""",
  "A code gate or PreToolUse hook that checks verification state on every refund call",
  "Only a check on every call covers all turns, retries and long conversations.",
  [("Force verify_customer with tool_choice on the first turn", "Forcing controls one turn; later out-of-order calls are still possible."),
   ("List verify_customer first in the tools array", "Tool order in the array doesn't enforce call order."),
   ("Describe the dependency in the refund tool's description", "Descriptions guide; they don't enforce.")])

Q("D1", "S1", "Prerequisites", """
An agent should not even consider the refund tool until an order has been looked up. Which technique directly achieves that?""",
  "Progressive exposure: add the refund tool to the tools list only after the lookup succeeds",
  "If the tool isn't offered, it can't be chosen.",
  [("Set disable_parallel_tool_use to true", "That limits parallel calls, not which tools are available."),
   ("Use tool_choice none for the first turn", "That blocks all tools, including the lookup."),
   ("Put a warning in the refund tool's description", "The tool remains selectable.")])

# --- Termination guarantee ---
Q("D1", "S1", "Termination", """
Requirement: every support session must end either resolved or escalated to a person. Where should this be guaranteed?""",
  "At the orchestration layer: after the loop ends for any reason, check for a resolution or escalation record and escalate if neither exists",
  "A check outside the model covers every exit path: normal end, cap, error, refusal or timeout.",
  [("In the system prompt: 'Never end a conversation without resolving or escalating'", "Prompts can't guarantee behaviour on every exit path."),
   ("By raising the iteration cap so the agent always has time to finish", "More time doesn't guarantee an outcome."),
   ("By forcing escalate_to_human with tool_choice on every turn", "That would escalate everything, including easy cases.")])

Q("D1", "S1", "Termination", """
An exception is thrown in the middle of an agent session and the process exits. With a well-designed orchestration layer, what happens?""",
  "The safeguard detects that no resolution was recorded and creates an escalation with a handoff summary",
  "The guarantee must cover crashes too, not only clean exits.",
  [("Nothing; exceptions are outside the scope of agent design", "Unhandled failures are exactly where customers get lost."),
   ("The model retries the session automatically from the start", "The model doesn't run your process lifecycle."),
   ("The user is asked to repeat their request in a new session", "That loses context and is a poor experience.")])

Q("D1", "S1", "Termination", """
A Claude Code or Agent SDK agent tends to stop before running the required checks. Which hook can enforce "don't finish until checks pass"?""",
  "A Stop hook that blocks stopping until the condition is met",
  "Stop hooks run when the agent tries to finish and can send it back to work.",
  [("A PostToolUse hook on the Read tool", "Runs after reads; doesn't control finishing."),
   ("A SessionStart hook", "Runs at the beginning, not at the end."),
   ("A permissions deny rule for the Stop event", "Permission rules govern tool use, not lifecycle events.")])

# --- Handoffs ---
Q("D1", "S1", "Handoff", """
An agent escalates a billing dispute to a human. Which handoff content is most useful?""",
  "Verified identity status, facts established, actions already taken, authorisation limits, open questions and the reason for escalation",
  "A structured package lets the human continue without repeating work or re-verifying.",
  [("The full raw transcript only", "Forces the human to re-read everything to find the key facts."),
   ("A one-line summary: 'Customer unhappy about billing'", "Too little; the human must start over."),
   ("The model's internal reasoning for each turn", "Not a substitute for structured facts and status.")])

Q("D1", "S1", "Handoff", """
Why include authorisation state (e.g. "verified via OTP", "refund limit reached") in a handoff package?""",
  "So the receiving agent or human doesn't repeat checks or act beyond what's been approved",
  "Authorisation state prevents duplicate verification and unauthorised actions.",
  [("Because the API requires it for escalation calls", "No API requires this; it's a design best practice."),
   ("To make the handoff longer and more complete", "Length isn't the goal; actionable state is."),
   ("So the model can re-verify the customer automatically", "The point is to avoid unnecessary re-verification.")])

Q("D1", "S3", "Handoff", """
A research pipeline passes work from a gathering stage to a writing stage. What should the handoff contain?""",
  "Structured findings with source, date and confidence for each claim, plus known gaps",
  "Provenance and gaps travel with the findings so the writer can cite accurately.",
  [("Raw search results so the writer can decide what matters", "Pushes filtering work and context load downstream."),
   ("Only the final conclusions, without sources", "Loses traceability."),
   ("A list of URLs visited", "URLs alone don't carry the findings.")])

# --- Hooks ---
Q("D1", "S1", "Hooks", """
Policy: the agent may apply discount codes up to 20%; anything higher needs a manager. The agent occasionally applies 30% codes. Which fix is deterministic?""",
  "A PreToolUse hook on apply_discount that denies values above 20% and returns guidance to request approval",
  "The check runs before every call, regardless of what the model decides.",
  [("A sentence in the system prompt stating the 20% limit", "Advisory only."),
   ("A PostToolUse hook that emails a manager after the discount is applied", "Notifies after the fact; doesn't prevent it."),
   ("Lowering the temperature so the model is more conservative", "Not an enforcement mechanism.")])

Q("D1", "S1", "Hooks", """
Tool results from a CRM include full customer phone numbers that the agent never needs. Which mechanism removes them reliably before the model sees them?""",
  "A PostToolUse hook (or code wrapper) that redacts those fields from the tool result",
  "Post-processing tool output deterministically minimises the data that reaches the model.",
  [("A system prompt telling the model to ignore phone numbers", "The data still enters context."),
   ("A PreToolUse hook that blocks the CRM tool", "Blocks the needed lookup entirely."),
   ("Lowering max_tokens", "Unrelated to what data enters context.")])

Q("D1", "G", "Hooks", """
Which statement about prompts and hooks is accurate?""",
  "Prompt instructions are probabilistic; hooks are deterministic code that runs every time",
  "That's why must/never rules belong in hooks.",
  [("Hooks are suggestions the model may ignore", "Hooks are executed by the harness, not interpreted by the model."),
   ("Prompts are enforced if written in capital letters", "Emphasis doesn't make instructions deterministic."),
   ("Hooks only run in interactive sessions", "Hooks run in SDK and non-interactive runs too.")], level=1)

Q("D1", "S4", "Hooks", """
In a Claude Code command hook on PreToolUse, which exit code blocks the tool call and sends the hook's stderr back to Claude?""",
  "Exit code 2",
  "Exit 2 is the blocking signal; stderr is fed back as feedback.",
  [("Exit code 1", "Exit 1 is a non-blocking error; the tool call proceeds."),
   ("Exit code 0", "Exit 0 means success."),
   ("Any non-zero exit code", "Only exit 2 blocks.")], level=1)

Q("D1", "S4", "Hooks", """
An audit requirement says every file write by the agent must be logged with path and timestamp. Best mechanism?""",
  "A PostToolUse hook matching write and edit tools that appends to an audit log",
  "Runs after every successful write, independent of the model.",
  [("Ask the model to report each write in its final answer", "Self-reporting can be incomplete."),
   ("A custom slash command /log-writes", "Requires someone to remember to run it."),
   ("A rule file describing the logging format", "Rules are advisory.")])

# --- Sessions ---
Q("D1", "S2", "Sessions", """
A code-review session from yesterday is resumed. Since then, 4 of 60 files have changed. What is the best approach?""",
  "Resume with a concise summary of prior findings and re-analyse only the 4 changed files",
  "Targeted re-analysis plus context injection avoids repeated work and stale conclusions.",
  [("Re-review all 60 files to be safe", "Wastes effort and context."),
   ("Resume and trust all previous findings", "Findings for the changed files may now be wrong."),
   ("Start a brand-new session with no prior context", "Loses valid findings for 56 unchanged files.")])

Q("D1", "S2", "Sessions", """
You want to try a risky alternative design from an existing session without disturbing the original line of work. Which option fits?""",
  "Fork the session",
  "Forking branches from the same starting point while leaving the original intact.",
  [("Resume the session and try the alternative in place", "Mixes both lines of work in one history."),
   ("Clear the session and start over", "Loses the shared starting context."),
   ("Use /compact before trying the alternative", "Compacting summarises; it doesn't branch.")])

Q("D1", "S2", "Sessions", """
A session's history is very long and mostly about an approach that was abandoned. What is the best way to continue?""",
  "Start fresh with a short summary of the current state, decisions and open items",
  "Stale, noisy context hurts quality; a clean summary carries what matters.",
  [("Resume the full session as is", "Keeps the abandoned approach in context."),
   ("Fork the session", "The fork still carries the noisy history."),
   ("Resume and ask Claude to ignore earlier turns", "The tokens are still in context.")])

Q("D1", "S4", "Sessions", """
Which practice makes long-running agent work most resilient to crashes and context resets?""",
  "Periodically writing progress, decisions and next steps to a state file the agent can reload",
  "External state survives crashes and compaction.",
  [("Relying on the conversation history alone", "History is lost or compacted."),
   ("Increasing the context window", "Doesn't survive a crash."),
   ("Disabling /compact", "Context still fills; crashes still happen.")])

# --- Agent SDK ---
Q("D1", "S4", "Agent SDK", """
An Agent SDK agent ignores the team's CLAUDE.md and project skills. What is the most likely cause?""",
  "Filesystem settings weren't loaded; setting_sources must include the project source",
  "The SDK loads project settings such as CLAUDE.md and skills only when configured to.",
  [("CLAUDE.md is only read by the Claude desktop app", "Claude Code and the SDK can load it."),
   ("Skills must be embedded in the system prompt", "Skills load from the filesystem when enabled."),
   ("The model needs extended thinking enabled", "Unrelated to loading settings.")])

Q("D1", "S4", "Agent SDK", """
What is the key difference between building with the Client SDK (Messages API) and the Agent SDK?""",
  "With the Agent SDK the harness runs the tool loop and provides built-in tools; with the Client SDK you write the loop",
  "That's the core trade-off: control versus built-in agent capabilities.",
  [("The Agent SDK can't use custom tools", "It supports custom tools and MCP servers."),
   ("The Client SDK can't call tools", "The Messages API supports tool use; you run the loop."),
   ("The Agent SDK doesn't use Claude models", "It's built on Claude.")], level=1)

Q("D1", "S4", "Agent SDK", """
You need a read-only analysis agent that must never modify files. Which configuration is most appropriate?""",
  "Restrict allowed tools to read-only ones such as Read, Grep and Glob",
  "Least-privilege tool access enforces read-only behaviour.",
  [("Tell the agent in the prompt not to edit files", "Advisory only."),
   ("Allow all tools but lower max_tokens", "Doesn't prevent writes."),
   ("Use acceptEdits permission mode", "That auto-approves edits, the opposite of what's needed.")])

Q("D1", "S5", "Hooks", """
In an automated CI agent, a rule says the agent must never modify files under .github/workflows/. Which mechanism is most reliable?""",
  "A PreToolUse hook or permission deny rule covering edits to that path",
  "Deterministic enforcement applies even in unattended runs.",
  [("A note in the CI prompt", "Advisory only."),
   ("A code review after the run", "Detects the change too late."),
   ("Running the job with fewer iterations", "Doesn't prevent the edit.")])
