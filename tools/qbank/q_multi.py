from qlib import M

# Multiple-response ("Select TWO") questions. The real exam includes this format.
# Original questions, written from public documentation; all data is fictional.

M("D1", "S1", "Agentic loop", """
A support agent's loop sometimes stops before the customer's issue is resolved. Which TWO loop-control practices are sound? (Select TWO.)""",
  [("Continue while stop_reason is tool_use and finish on end_turn", "stop_reason is the reliable signal for whether Claude is waiting on tools."),
   ("Append each tool result to the history before the next request", "The model needs the results to decide its next step.")],
  [("End the loop when the reply text contains the word \"resolved\"", "Parsing natural language for completion is fragile."),
   ("Use a fixed count of three iterations as the normal exit", "An arbitrary cap is a safety net, not a completion signal."),
   ("Treat any assistant text block as the end of the task", "Text can accompany a tool call; it does not mean the work is done.")])

M("D1", "S3", "Sub-agent context", """
A coordinator delegates analysis to sub-agents in a research system. Which TWO statements about sub-agents are correct? (Select TWO.)""",
  [("A sub-agent does not inherit the coordinator's conversation history", "Sub-agents start with an isolated context."),
   ("Several sub-agents can be started in parallel from one coordinator turn", "Multiple delegation calls in a single response run concurrently.")],
  [("Sub-agents share one memory, so findings need not be passed on", "There is no shared memory; context must be passed explicitly."),
   ("A sub-agent automatically receives every tool the coordinator has", "Tool access is configured per sub-agent."),
   ("Sub-agents should exchange results directly, bypassing the coordinator", "Routing through the coordinator keeps the flow observable and controlled.")])

M("D1", "S1", "Enforcement", """
Refunds must never be issued before the customer's identity is verified. Which TWO mechanisms provide deterministic enforcement? (Select TWO.)""",
  [("A prerequisite gate that blocks the refund tool until verification succeeds", "Code-level gates cannot be skipped by the model."),
   ("A hook that intercepts the refund call and denies it without a verified ID", "Hooks run every time, outside the model's control.")],
  [("A system prompt line stating that verification always comes first", "Prompt instructions have a non-zero failure rate."),
   ("Three few-shot examples showing verification before the refund", "Examples raise the likelihood but do not guarantee the order."),
   ("A lower temperature so that the agent follows the usual sequence", "Sampling settings are not enforcement.")])

M("D2", "S4", "Tool descriptions", """
An agent keeps confusing two similar tools. Which TWO changes are most likely to improve selection? (Select TWO.)""",
  [("Rewrite each description with its inputs, examples and boundaries", "Descriptions are the main signal used to choose a tool."),
   ("Rename or split the tools so that their purposes no longer overlap", "Removing overlap removes the ambiguity at its source.")],
  [("Shorten both descriptions to a single generic sentence", "Thin descriptions make selection less reliable."),
   ("Add ten more general-purpose tools to give the agent options", "More tools make selection harder."),
   ("Tell the agent in capitals to choose tools more carefully", "Emphasis adds no information about which tool fits.")])

M("D2", "S1", "Tool errors", """
A tool call fails. Which TWO properties make the error response most useful to the agent? (Select TWO.)""",
  [("A category such as transient, validation, business or permission", "The category tells the agent what kind of recovery is appropriate."),
   ("An explicit indication of whether retrying could succeed", "Without it the agent may retry pointlessly or give up too early.")],
  [("An empty result returned as if the call had succeeded", "That hides the failure and misleads the agent."),
   ("A generic message such as \"Operation failed\" with no detail", "Generic errors block sound recovery decisions."),
   ("A full internal stack trace including service credentials", "Leaks sensitive detail and adds noise.")])

M("D3", "S2", "Configuration scope", """
A team wants shared Claude Code configuration for a repository. Which TWO items belong in files committed to the project? (Select TWO.)""",
  [("Team coding conventions in the project's CLAUDE.md", "Project memory is shared through version control."),
   ("A shared MCP server definition in .mcp.json, with tokens via ${VAR}", "Project scope shares the server while keeping secrets out of the file.")],
  [("One developer's personal editor preferences", "Personal preferences belong at user level."),
   ("An API token written directly into a settings file", "Secrets must not be committed."),
   ("An experimental MCP server only one person is trying out", "Personal or experimental servers belong at user or local scope.")])

M("D3", "S5", "CI integration", """
Claude Code runs as a review step in a CI pipeline. Which TWO practices are appropriate? (Select TWO.)""",
  [("Run it non-interactively with the print flag", "Print mode avoids waiting for keyboard input."),
   ("Request JSON output so that the pipeline can parse the findings", "Structured output lets later steps consume the result reliably.")],
  [("Start an interactive session and wait for a developer to respond", "A CI job has nobody to answer prompts and would hang."),
   ("Have the session that wrote the code also approve its own change", "An independent review instance is more reliable than self-review."),
   ("Parse the findings from free-form prose with regular expressions", "Fragile compared with structured output.")])

M("D3", "S5", "CI review quality", """
A CI review step produces duplicate test suggestions and repeats findings on every push. Which TWO changes address this? (Select TWO.)""",
  [("Include the existing tests in the context given to the reviewer", "The reviewer can then avoid suggesting tests that already exist."),
   ("Pass earlier findings and ask only for new or unresolved issues", "Prior findings let a re-review report only what has changed.")],
  [("Increase the number of review runs for each push", "More runs produce more repetition."),
   ("Remove CLAUDE.md so that the reviewer starts from nothing", "Removes the project context that guides the review."),
   ("Ask the reviewer to be less talkative in general", "Vague instructions do not target the duplication.")])

M("D4", "S6", "Schema design", """
An extraction schema produces invented values for fields that are missing from some documents. Which TWO schema changes reduce fabrication? (Select TWO.)""",
  [("Allow null for fields that may be absent from the source", "A required field with no source value invites invention."),
   ("Add enum values such as \"unclear\" or \"other\" with a detail field", "An escape value avoids forcing a wrong choice.")],
  [("Mark every field as required so that nothing is skipped", "Forces the model to supply something even when nothing exists."),
   ("Remove the schema and accept free-form text instead", "Loses structure without reducing invention."),
   ("Add a field in which the model rates its own honesty", "Self-assessment does not prevent fabricated values.")])

M("D4", "S5", "Batch processing", """
A team is considering the Message Batches API. Which TWO workloads suit it? (Select TWO.)""",
  [("A weekly audit report that nobody is waiting on", "Non-blocking work fits an asynchronous, cheaper API."),
   ("Nightly generation of test suggestions for the next morning", "Results are needed hours later, not immediately.")],
  [("A pre-merge check that blocks developers until it finishes", "Batches have no latency guarantee; blocking checks need synchronous calls."),
   ("A live chat reply to a waiting customer", "A waiting user cannot tolerate batch delays."),
   ("A multi-turn tool-calling loop inside a single batch request", "A batch request is a single call; it cannot run a tool loop.")])

M("D5", "S1", "Escalation", """
Which TWO situations should lead a support agent to escalate to a human? (Select TWO.)""",
  [("The customer explicitly asks to speak to a person", "An explicit request for a human is honoured immediately."),
   ("The request falls outside anything the written policy covers", "A policy gap should be escalated, not improvised.")],
  [("The customer's message contains a negative word", "Sentiment is not a reliable escalation trigger."),
   ("The agent rates its own confidence slightly below usual", "Self-reported confidence is poorly calibrated."),
   ("A routine order-status question the agent can answer with its tools", "Routine, resolvable issues should be handled directly.")])

M("D5", "S6", "Human review", """
A team wants to reduce human review of extracted data safely. Which TWO practices support that decision? (Select TWO.)""",
  [("Measure accuracy separately by document type and by field", "An overall average can hide weak segments."),
   ("Keep sampling high-confidence results to check the real error rate", "Sampling detects errors and new patterns that confidence scores miss.")],
  [("Rely on the overall accuracy figure alone", "Aggregate metrics mask poor performance on particular types or fields."),
   ("Stop all review once the first week looks good", "Performance can drift and new document patterns appear."),
   ("Review only the items the model itself flags as wrong", "The model does not reliably flag its own errors.")])
