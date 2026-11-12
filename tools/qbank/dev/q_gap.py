from devlib import Q, M

# Questions added after reviewing the official exam guide's skill list.
# Still original: written from public documentation and general engineering practice.

# ================= Applications & Integration =================

Q("AI", "Requirements", """
A sponsor asks a developer to "add AI to the returns process". What should the developer do first?""",
  "Clarify the goal and write measurable requirements",
  "An ambiguous goal cannot be designed or tested. Requirements come before model or pattern choices.",
  [("Choose the most capable model that is available", "Model choice depends on requirements that don't exist yet."),
   ("Build a multi-agent prototype to show the sponsor", "Building before the goal is clear risks solving the wrong problem."),
   ("Write a long system prompt covering every case", "There is nothing agreed yet for the prompt to implement.")], level=1)

Q("AI", "Requirements", """
Which of these is an infrastructure (non-functional) requirement?""",
  "Responses must begin within two seconds at peak load",
  "It describes how well the system must perform, not what it does.",
  [("The system must extract the invoice number and total", "That is a function the system performs."),
   ("The system must classify tickets into six categories", "That is a function the system performs."),
   ("The system must draft a reply for an agent to approve", "That is a function the system performs.")])

Q("AI", "Requirements", """
A requirement states: "Customer data must not leave the company's cloud region." Which design decision does this affect most directly?""",
  "Which platform and deployment option is used",
  "Data-residency constraints determine where and through which provider the model is called.",
  [("Whether examples in the prompt use XML tags", "Prompt formatting does not control where data is processed."),
   ("Whether the temperature is set near 0 or 1", "Sampling settings are unrelated to data location."),
   ("Whether responses are parsed with Pydantic", "Validation tooling is unrelated to data location.")])

Q("AI", "Systems life cycle", """
An application has run unchanged for a year. One morning every request fails with a 404 naming the model. Nothing was deployed. What life-cycle activity was neglected?""",
  "Maintenance: tracking model deprecations",
  "Models are retired on a schedule. Operating an LLM system includes watching for that and migrating in time.",
  [("Design: the system should have used more agents", "Agent count has nothing to do with a retired model."),
   ("Development: the code should have used raw HTTP", "The SDK is not the cause of a retired model."),
   ("Testing: the unit tests should have been stricter", "Unit tests cannot keep a retired model available.")])

Q("AI", "Software engineering", """
What is the relationship between an official Claude SDK and the REST API?""",
  "The SDK is a wrapper over the same REST API",
  "SDKs add typing, retries, timeouts and stream handling on top of the same HTTP endpoints.",
  [("The SDK uses a separate, faster private protocol", "It calls the same public HTTP API."),
   ("The SDK runs the model locally on your machine", "Models run on the provider's servers."),
   ("The SDK is required; raw HTTP calls are rejected", "Any HTTP client can call the API.")], level=1)

Q("AI", "Software engineering", """
A developer builds a JSON request body by joining strings and inserting the user's text directly. Requests fail whenever the text contains a quotation mark. What is the correct fix?""",
  "Serialise the object with a JSON library",
  "A serialiser escapes special characters correctly. String concatenation does not.",
  [("Ask users not to type quotation marks in the box", "Unreasonable, and other characters will also break it."),
   ("Replace every quotation mark with a blank space", "Corrupts the user's text and misses other special characters."),
   ("Wrap the user's text in a second pair of quotes", "Adds more unescaped quotes and makes the JSON worse.")], level=1)

Q("AI", "Software engineering", """
A script summarises 4,000 documents by launching all requests at once with asyncio.gather. Most fail with 429 errors. A user is waiting for the results. What is the best change?""",
  "Limit concurrency with a semaphore or worker pool",
  "Bounded concurrency keeps throughput high while staying inside rate limits.",
  [("Launch the same requests twice to improve the odds", "Doubles the load that caused the errors."),
   ("Remove the awaits so that requests return sooner", "Without awaiting, results are never collected."),
   ("Switch every call to the synchronous client instead", "Sequential calls would be very slow for a waiting user.")])

Q("AI", "Software engineering", """
A coding agent produced a change that passes the existing tests. What should happen before it is merged?""",
  "A person reviews the diff, edge cases included",
  "Passing tests show only what the tests cover. Review is still needed for generated code.",
  [("Nothing further; passing tests are sufficient proof", "Tests rarely cover every edge case or security concern."),
   ("The same session reviews and approves its own change", "A fresh reviewer avoids the author's blind spots."),
   ("The change is merged and reviewed after the release", "Review after release finds problems too late.")])

Q("AI", "Software engineering", """
A team wants an agent to migrate 180 files from one logging library to another. Which approach is most likely to succeed?""",
  "Plan first, then migrate in small verified steps",
  "Large refactors need a plan, a safety net of tests, and incremental verification.",
  [("Ask for all 180 files to be rewritten in one prompt", "Overloads context and gives no checkpoint when something breaks."),
   ("Skip the tests until every file has been converted", "Errors compound and become hard to locate."),
   ("Let several agents edit the same files in parallel", "Conflicting edits on shared files cause breakage.")])

Q("AI", "Software engineering", """
During code review, a reviewer notices that generated code imports a package nobody on the team has heard of. What is the right reaction?""",
  "Verify the package exists and is trustworthy",
  "Generated code can reference non-existent or unsuitable packages. Dependencies must be checked.",
  [("Install it at once, since the model recommended it", "A recommendation is not verification."),
   ("Assume it is a standard library the team forgot", "An assumption, not a check."),
   ("Delete the import line and merge the remainder", "The code probably depends on it and would break.")])

Q("AI", "Technical fundamentals", """
Why does the Messages API use server-sent events for streaming, and not WebSockets?""",
  "Token streaming only needs one-way delivery",
  "SSE provides one-way streaming over ordinary HTTP. WebSockets are for two-way communication.",
  [("WebSockets cannot carry text, only binary frames", "WebSockets carry text as well as binary."),
   ("Server-sent events let the client send mid-stream", "SSE is one-way; the client does not send on it."),
   ("WebSockets are limited to a hundred messages", "There is no such limit.")])

Q("AI", "Technical fundamentals", """
A browser-based voice assistant needs the client and the team's backend to exchange audio and control messages continuously in both directions. Which transport suits that link?""",
  "A WebSocket connection",
  "WebSockets keep one connection open over which both sides can send at any time.",
  [("A series of separate GET requests", "Polling is slow and one-directional per request."),
   ("Server-sent events alone", "SSE only carries data from server to client."),
   ("A nightly batch upload", "A batch has no real-time interaction.")])

Q("AI", "Application design", """
A prompt gives excellent results in the Claude chat app. Sent unchanged through the Messages API, results are noticeably different. What is the most likely explanation?""",
  "The API adds no product system prompt, tools or memory",
  "Each surface assembles context differently. Through the API, Claude sees only what the request contains.",
  [("The API always serves an older and weaker model", "The model is whichever one the request names."),
   ("The API ignores the first message of each request", "Every message sent is used."),
   ("The API runs every request at temperature zero", "The default is not zero unless set.")])

Q("AI", "Application design", """
In Claude Code, a team writes "Never run database migrations" in CLAUDE.md. A migration is later run during a session. Why was the instruction not a guarantee?""",
  "CLAUDE.md is guidance, not an enforced control",
  "Instructions are advisory. Enforcement needs a permission rule or a hook.",
  [("CLAUDE.md is only loaded on the first day of use", "It is loaded in every session."),
   ("CLAUDE.md is limited to twenty lines of content", "There is no such limit."),
   ("CLAUDE.md applies to Python files and no others", "It is not restricted by language.")])

Q("AI", "Application design", """
A developer has spent three hours in one Claude Code session on several unrelated tasks. Answers are getting worse and earlier instructions are being forgotten. What is the best practice?""",
  "Start a fresh session per task, carrying a short summary",
  "Unrelated history pollutes the context. Clean sessions with a deliberate hand-over work better.",
  [("Keep going and repeat each instruction in capitals", "Adds more noise to an already crowded context."),
   ("Paste the whole transcript back in as a reminder", "Makes the context problem worse."),
   ("Raise the max_tokens value for the next reply", "Output size is not the issue.")], level=1)

Q("AI", "Application design", """
A team wants every developer to have the same set of Claude Code skills, commands and hooks for a project. Which approach fits best?""",
  "Package them as a plugin enabled in the project settings",
  "A plugin bundles these components, and project settings share it with everyone who works in the repository.",
  [("Email the files and ask each person to copy them", "Manual copies drift apart and are never updated together."),
   ("Have each developer recreate them from memory", "Guarantees inconsistency."),
   ("Describe them in the README without any files", "A description does not install anything.")])

Q("AI", "Application design", """
Before installing a third-party Claude Code plugin, what is the most important consideration?""",
  "It can run code, so its source must be trusted",
  "Plugins can execute code and extend what the agent can do. Treat them like any other dependency.",
  [("Its name should be shorter than twelve characters", "Name length is irrelevant."),
   ("It should be the newest plugin in the marketplace", "Newness says nothing about safety."),
   ("It should contain more commands than other plugins", "Size is not a measure of trust or quality.")])

Q("AI", "Configuration", """
Output quality dropped last Tuesday. The team cannot tell which prompt text was in use that day, because prompts are edited directly in a dashboard. What practice is missing?""",
  "Prompt versioning, logged on each request",
  "Versioned prompts plus logging make it possible to connect a behaviour change to a specific prompt.",
  [("A larger context window for the affected model", "Window size does not record prompt history."),
   ("A second dashboard with a different colour scheme", "Cosmetic and unrelated."),
   ("A rule that prompts may be edited only on Fridays", "Scheduling edits does not record what changed.")])

Q("AI", "Configuration", """
In Claude Code, which file should hold a personal permission override that must not be shared with the team?""",
  ".claude/settings.local.json",
  "The local settings file is for personal overrides and is not committed.",
  [(".claude/settings.json", "That file is committed and shared with the team."),
   ("CLAUDE.md in the project root", "It holds instructions, not permission settings, and is shared."),
   (".mcp.json in the project root", "It lists shared MCP servers.")])

Q("AI", "Platforms", """
An application is moved from the direct Claude API to a cloud vendor's platform. A beta feature it depends on stops working. What should have been checked first?""",
  "Whether that feature is available on the chosen platform",
  "Feature availability, model identifiers and authentication differ between platforms.",
  [("Whether the cloud vendor uses a faster network", "Network speed does not add a missing feature."),
   ("Whether the prompts were translated to English", "Language is unrelated to feature availability."),
   ("Whether the team's laptops were recently updated", "Client machines are unrelated.")])

M("AI", "Requirements", """
Which TWO are infrastructure (non-functional) requirements? (Select TWO.)""",
  [("The service must handle 50 requests per second at peak", "A throughput constraint."),
   ("Prompts and outputs must be retained for no more than 30 days", "A data-retention constraint.")],
  [("The service must translate documents into French", "A function."),
   ("The service must flag invoices with missing totals", "A function."),
   ("The service must produce a summary for each ticket", "A function.")])

# ================= Model Selection & Optimisation =================

Q("MS", "Model options", """
An interactive coding tool uses a top-tier model and needs faster output without changing the model's quality. Cost is a secondary concern. Which option addresses this directly?""",
  "Fast mode, which speeds up the same model at a premium",
  "Fast mode raises output speed for the same model at a higher price.",
  [("A smaller tier, which keeps the quality identical", "A smaller model is faster but not the same quality."),
   ("The Batches API, which returns results in seconds", "Batches are asynchronous and slower."),
   ("A higher max_tokens, which makes generation faster", "The cap does not change speed.")])

Q("MS", "Model options", """
Which statement correctly separates model choice from reasoning mode?""",
  "Picking a tier and enabling thinking are separate decisions",
  "A tier sets capability and price; thinking or effort settings control how much reasoning is done on a request.",
  [("Enabling thinking switches the request to a larger tier", "The model stays the same."),
   ("Thinking is only available on the smallest model tier", "It is not limited to the smallest tier."),
   ("Choosing a larger tier turns thinking on by default always", "Tier and thinking are configured separately.")])

Q("MS", "Prompting styles", """
A classification prompt works well zero-shot. A developer adds twelve long examples "to be safe". What is the main cost?""",
  "More input tokens on every request, with little benefit",
  "Examples are sent each time. When zero-shot already works, they add cost and latency for no gain.",
  [("The model is no longer able to return any labels", "Examples do not prevent output."),
   ("The context window is permanently reduced in size", "The window is per request, not permanently changed."),
   ("The API rejects prompts that contain examples", "Examples are allowed.")])

Q("MS", "Model releases", """
A team upgrades to a newer model version. Token counts for the same prompts change, and some replies are formatted differently. What does this show?""",
  "Releases change behaviour; upgrades need evals",
  "New versions are not drop-in replacements. Pin versions, re-run evals and re-count tokens.",
  [("The API key was rotated during the upgrade process", "Key rotation does not change model behaviour."),
   ("The temperature setting is reset by every upgrade", "Request parameters are whatever the code sends."),
   ("The prompts were corrupted while being transferred", "Nothing indicates corruption.")])

Q("MS", "Cache checkpoints", """
A prompt has tool definitions, a system prompt, a large reference document, and a growing conversation. Why might a developer set several cache breakpoints?""",
  "So parts that change at different rates cache apart",
  "A change only invalidates what follows it. Layered breakpoints keep stable sections cached.",
  [("So that the model reads the document several times", "Breakpoints do not repeat content."),
   ("So that each breakpoint doubles the context window", "They do not change the window."),
   ("So that output tokens are billed at the cache rate", "Caching applies to input.")], level=3)

Q("MS", "Usage tracking", """
A company wants to know which product feature drives its Claude spend. What is the most direct approach?""",
  "Record the usage from each response, tagged by feature",
  "Each response reports input, output and cache tokens. Tagging them shows where cost goes.",
  [("Estimate from the number of lines in each prompt", "Line counts are a poor proxy for tokens."),
   ("Ask each team for an informal monthly impression", "Impressions are not measurements."),
   ("Compare the temperature used by each feature", "Temperature does not indicate cost.")], level=1)

# ================= Agents & Workflows =================

Q("AW", "Hosting", """
A team wants long-running agents but does not want to build sandboxing, session storage and scaling. Data requirements permit a hosted service. Which option fits?""",
  "An Anthropic-hosted managed agent service",
  "A managed service runs the harness and infrastructure, which suits long-running and asynchronous work.",
  [("A hand-written loop on a developer's laptop", "Not durable or scalable for long-running work."),
   ("A single Messages API call with a long prompt", "One call is not a long-running agent."),
   ("A nightly batch of unrelated summary requests", "Batches are not interactive agents.")])

Q("AW", "Hosting", """
An agent must read files on an internal network that cannot be exposed outside the company. Which deployment is most appropriate?""",
  "A self-hosted agent running inside the company network",
  "Self-hosting keeps the loop, files and credentials in the organisation's own environment.",
  [("A hosted agent given the network's admin password", "Sharing credentials outward defeats the restriction."),
   ("A public MCP server that publishes the files", "Exposes what must stay private."),
   ("A chat app where staff paste the files by hand", "Manual, error-prone and not an agent.")])

Q("AW", "Frameworks", """
A team needs an agent workflow with explicit steps, saved state between steps, and pauses for human approval. Which kind of framework is designed for this?""",
  "A graph-based framework such as LangGraph",
  "Graph frameworks model nodes, edges and state explicitly, with checkpoints and human-in-the-loop pauses.",
  [("A CSS framework for styling the approval screen", "Unrelated to agent orchestration."),
   ("A unit-testing framework with assertion helpers", "Testing tools do not orchestrate agents."),
   ("An object-relational mapper for the database", "Persistence libraries do not define agent control flow.")])

Q("AW", "Frameworks", """
What is the main risk of adopting an agent framework before understanding the underlying API calls?""",
  "The abstraction hides the prompts and requests",
  "When something goes wrong you need to see what was actually sent. Heavy abstraction can obscure it.",
  [("Frameworks make each API call cost twice as much", "Pricing is unaffected by the framework itself."),
   ("Frameworks prevent the use of any tool definitions", "Frameworks generally support tools."),
   ("Frameworks only work with the smallest model tier", "They work with any tier.")])

Q("AW", "Supervisor hierarchies", """
When is a supervisor agent with several workers a good design?""",
  "When the work splits into independent, parallel parts",
  "Hierarchies pay off for broad, separable work. For sequential tasks they add cost and hand-off errors.",
  [("When every step depends closely on the previous one", "Tightly coupled steps suit a single agent or a chain."),
   ("When the token budget for the task is very limited", "Hierarchies multiply token use."),
   ("When the task is a single short classification", "Far too much machinery for one call.")])

Q("AW", "Memory", """
An agent keeps a single shared memory file for all users. One user's reply mentions another user's project. What design rule was broken?""",
  "Memory must be scoped per user or project",
  "Unscoped memory leaks information between users. Scope and load only what is relevant.",
  [("Memory must be written in upper-case letters only", "Formatting does not isolate users."),
   ("Memory must be reloaded twice in each new session", "Reloading does not scope it."),
   ("Memory must be stored inside the system prompt", "Location in the prompt does not isolate users.")])

# ================= Prompt & Context Engineering =================

Q("PC", "Output handling", """
A model's answer states a refund amount and adds, "I am fully confident this is correct." How should the application treat the claim?""",
  "Verify the amount against the source data regardless",
  "Confident wording is not evidence. Values that matter are checked in code or against a source.",
  [("Accept it, since the model expressed full confidence", "Self-reported confidence is poorly calibrated."),
   ("Accept it only when the reply is longer than usual", "Length is not evidence of accuracy."),
   ("Reject it, since confident replies are always wrong", "Confidence does not imply error either.")], level=1)

Q("PC", "Input sanitisation", """
A prompt wraps user text in <user_input> tags. A user types text containing "</user_input>" followed by new instructions. What should the application do?""",
  "Escape or strip the delimiter from input before inserting it",
  "Input that can close your delimiter breaks the boundary. Sanitise it, and keep other defences as well.",
  [("Trust the tags, since users cannot type such symbols", "Users can type anything."),
   ("Remove the tags so that there is nothing to break out of", "Removes the boundary altogether."),
   ("Raise the temperature so the instructions are ignored", "Sampling settings are not a defence.")])

Q("PC", "Prompt refinement", """
A prompt underperforms. A developer changes the role, the examples, the format instructions and the model in one edit, and results improve slightly. What is the weakness of this approach?""",
  "It is impossible to tell which change helped or harmed",
  "Iterate one change at a time against the eval set, so that each effect can be attributed.",
  [("Prompts may only be edited once in each working day", "No such rule exists."),
   ("Changing a role always makes the output much longer", "Not a general effect."),
   ("Examples and format instructions cannot be combined", "They are commonly used together.")])

Q("PC", "Context engineering", """
An agent's tool returns a 30,000-token log on every call, though only the last few error lines matter. Which technique addresses the resulting context bloat at its source?""",
  "Prune the tool output to the relevant lines",
  "Trimming at the tool keeps noise out of the context in the first place.",
  [("Ask the model to try to ignore most of the log text", "The tokens are still sent and paid for."),
   ("Call the tool twice so that the model sees it clearly", "Doubles the bloat."),
   ("Move the log into the system prompt as background", "Still consumes context, and pollutes the system prompt.")])

# ================= Tools & MCPs =================

Q("TM", "Agentic customisation", """
A team wants Claude to follow its detailed release-notes procedure, including a template and a formatting script. No new system access is required. Which mechanism fits best?""",
  "A skill with the instructions and script",
  "Skills package know-how that loads on demand. Nothing here needs new connectivity.",
  [("An MCP server exposing the procedure as a tool", "MCP provides access to systems; this is procedural knowledge."),
   ("A PreToolUse hook that blocks all file edits", "A hook enforces rules; it does not teach a procedure."),
   ("A higher permission mode for the whole project", "Permissions do not supply knowledge.")])

Q("TM", "Agentic customisation", """
An agent needs to search files and run shell commands in a repository. A developer starts writing custom tools for both. What is the better choice?""",
  "Use the built-in tools that already do this",
  "Built-in tools are available and tested. Rebuilding them adds work and risk.",
  [("Write an MCP server that wraps the shell command", "Recreates what already exists."),
   ("Write a skill that describes how a search would work", "A description does not perform the search."),
   ("Ask users to paste file contents into the chat", "Manual and defeats the purpose of an agent.")], level=1)

Q("TM", "Agentic customisation", """
Which statement best distinguishes a skill from an MCP server?""",
  "A skill supplies know-how; an MCP server supplies access",
  "Skills teach procedures and methods. MCP connects the agent to external tools and data.",
  [("A skill needs a network port; an MCP server does not", "Skills are files; remote MCP servers are the networked ones."),
   ("A skill is always loaded in full; MCP tools never are", "Skill bodies load on demand."),
   ("A skill replaces the model; an MCP server replaces tools", "Neither replaces the model.")])

Q("TM", "Tool harness", """
An agent harness receives a tool_use block naming a tool that does not exist in its dispatch table. What should it do?""",
  "Return an error tool_result so that the model can recover",
  "An unknown tool is a recoverable condition. The loop continues with a clear error.",
  [("Crash the process so that the bug is clearly visible", "Loses the task for a recoverable problem."),
   ("Run the most similar tool that it happens to have", "Could perform an unintended action."),
   ("Return a success result containing an empty string", "Misleads the model into thinking it worked.")])

Q("TM", "Tool harness", """
A harness auto-runs read-only tools, asks for confirmation on tools that change data, and refuses destructive ones. What is this pattern?""",
  "Risk-based approval implemented in the harness",
  "Classifying tools by risk and enforcing the policy in code is a standard approval pattern.",
  [("Prompt chaining implemented in the system prompt", "This is about tool approval, not chaining prompts."),
   ("Prompt caching implemented with four breakpoints", "Unrelated to approval."),
   ("Model routing implemented with a small classifier", "Routing selects a model or path, not tool permissions.")])

Q("TM", "Tool sets", """
An agent has 45 tools, several with overlapping purposes. It often picks the wrong one. Which change helps most?""",
  "Give it fewer, distinct, well-described tools",
  "Fewer, non-overlapping tools improve selection and reduce tokens on every request.",
  [("Add ten more tools to cover the remaining gaps", "Makes selection harder."),
   ("Give every tool the same short generic description", "Removes the signal used for selection."),
   ("Rename the tools with numbers in place of words", "Meaningless names worsen selection.")])

M("TM", "Agentic customisation", """
Which TWO pairings of need and mechanism are appropriate? (Select TWO.)""",
  [("Reusable access to a ticketing system from several hosts: an MCP server", "MCP provides shared connectivity."),
   ("A rule that must block a command every time: a hook", "Hooks are deterministic.")],
  [("A hard security limit: a sentence in a skill description", "A description is advisory."),
   ("Reading local files in a repository: a new custom MCP server", "Built-in tools already do this."),
   ("A team's writing style guide: a network transport", "A transport carries messages; it holds no guidance.")])

# ================= Security & Safety =================

Q("SS", "Security properties", """
A user is correctly logged in, but can open another customer's invoice by changing an ID in the request. Which control failed?""",
  "Authorisation",
  "The user's identity was established; what that user may access was not checked.",
  [("Authentication", "The login worked; identity was known."),
   ("Availability", "The system was up; that is not the problem."),
   ("Rate limiting", "Request volume is not the issue.")], level=1)

Q("SS", "Key management", """
Which practice best supports detecting misuse of an API key?""",
  "Monitoring usage per key, with anomaly alerts",
  "Separate keys with monitoring show who used what and reveal anomalies.",
  [("Sharing one key so that all usage is in one place", "A shared key hides who did what."),
   ("Rotating the key only when an employee asks", "Rotation timing does not detect misuse."),
   ("Printing the key in application logs for audit", "Leaks the key.")])

Q("SS", "Guardrails", """
A team relies on a single input filter to keep its agent safe. Why is this considered insufficient?""",
  "Any one layer can fail, so guardrails should be layered",
  "Defence in depth combines input checks, least privilege, approvals, output validation and monitoring.",
  [("Input filters are forbidden by the usage policy", "They are a normal control."),
   ("Input filters make every response twice as slow", "Not a general truth, and not the reason."),
   ("Input filters only work with the largest models", "They work with any model.")], level=1)

# ================= Claude Code =================

Q("CC", "Repository setup", """
A developer opens Claude Code in an existing repository for the first time. Which command creates a starter CLAUDE.md from the codebase?""",
  "/init",
  "/init analyses the project and drafts a CLAUDE.md, which should then be reviewed and trimmed.",
  [("/clear", "Clears the conversation."),
   ("/compact", "Summarises the conversation to save context."),
   ("/mcp", "Manages MCP server connections.")], level=1)

Q("CC", "Permission modes", """
A developer wants Claude Code to investigate a bug and propose an approach without changing any files yet. Which mode fits?""",
  "Plan mode",
  "Plan mode allows reading and planning, with no edits until the plan is approved.",
  [("Bypass permissions mode", "Removes prompts and allows changes."),
   ("Accept edits mode", "Applies file edits without asking."),
   ("Fast mode", "A speed setting, not a permission mode.")], level=1)

Q("CC", "Headless mode", """
A CI job runs Claude Code non-interactively and another program needs to process events as they happen. Which output setting fits?""",
  "The stream-json output format",
  "Streaming JSON emits events as they occur for another process to consume.",
  [("The default interactive terminal display", "Not machine-readable and needs a terminal."),
   ("A screenshot of the final terminal window", "Not structured output."),
   ("Plain text printed after the run has ended", "Arrives only at the end and is unstructured.")])

Q("CC", "Custom commands", """
A team repeatedly types the same long review prompt in Claude Code. What is the lightest way to make it reusable by name?""",
  "A custom slash command in .claude/commands/",
  "A Markdown file there becomes a /command shared through the repository.",
  [("A new MCP server with one review tool", "Far heavier than needed for a prompt."),
   ("A PreToolUse hook that blocks commits", "Hooks enforce; they do not store prompts."),
   ("A deny rule in the project's settings", "Permissions do not store prompts.")])

# ================= Eval, Testing & Debugging =================

Q("EV", "Debugging", """
An agent gives a wrong answer. The trace shows the correct tool was called and returned the right data, and the full history was sent. Where is the problem most likely?""",
  "In the model's output, so improve the prompt",
  "With correct inputs and working tools, the remaining variable is the model's response.",
  [("In the HTTP layer, so add more retry attempts", "The calls succeeded; there is nothing to retry."),
   ("In the tool code, so rewrite the tool's schema", "The tool returned the right data."),
   ("In the API key, so rotate it and then try again", "Authentication succeeded.")])

Q("EV", "Debugging", """
A failure happens identically on every run with the same input. Another varies from run to run. Which is more likely an integration bug rather than model variability?""",
  "The one that happens identically every time",
  "Deterministic failures usually come from code or configuration; varying ones often from model non-determinism.",
  [("The one that varies from one run to the next", "Variation points to model behaviour."),
   ("Neither, since integration bugs cannot be found", "They can be found from traces."),
   ("Both equally, since all failures are random", "Not all failures are random.")])

Q("EV", "Graders", """
A team builds an LLM-based grader. What should be done before relying on its scores?""",
  "Calibrate it against cases that people have labelled",
  "Agreement with human labels shows whether the grader measures what you intend.",
  [("Raise its temperature for more varied scores", "Variation makes a grader less reliable."),
   ("Let it grade its own grading for consistency", "Self-assessment is not calibration."),
   ("Use it only on cases that are known to pass", "That would hide failures.")])

Q("EV", "Error types", """
A request fails with a 400 because a tool_result was sent without its matching tool_use. How should this be classified and handled?""",
  "A terminal client error: fix the message construction",
  "The request is invalid and will fail every time. Code must be corrected; retrying is pointless.",
  [("A transient server error: retry it with backoff", "A 400 is not transient."),
   ("A rate-limit error: wait for the retry-after time", "That would be a 429."),
   ("A model refusal: rephrase the user's question", "A refusal is a successful response, not a 400.")])

# ---- a few more, so that three full mocks can be built ----

Q("AW", "Agent construction", """
In an Agent SDK application, a rule must run every time before any shell command executes, whatever the model decides. Which feature provides this?""",
  "A hook registered for the pre-tool-use event",
  "Hooks run deterministically at lifecycle points and can block the action.",
  [("A sentence in the system prompt option", "Advisory, not deterministic."),
   ("A lower limit on the number of turns", "A turn cap does not inspect commands."),
   ("A description added to the sub-agent", "Descriptions guide delegation, not enforcement.")])

Q("AW", "Agent construction", """
What does a custom agent harness need to do that a single Messages API call does not?""",
  "Run tools, feed results back, and decide when to stop",
  "A harness is the loop around the model: dispatching tools, managing context and enforcing limits.",
  [("Train the model on the user's documents first", "No training happens in a harness."),
   ("Translate each prompt into a different language", "Unrelated to what a harness does."),
   ("Replace the system prompt after every single token", "Not something a harness does.")], level=1)

Q("PC", "Prompt placement", """
A support bot's tone rules and refund policy are pasted at the start of every user message, mixed with the customer's text. What is the better placement?""",
  "Rules in the system prompt; customer text in the user turn",
  "Stable instructions belong in the system prompt, which also keeps them separate from user data and cacheable.",
  [("Standing rules in each tool's result block instead", "Tool results are treated as data, not instructions."),
   ("Standing rules repeated three times in each message", "Repetition adds tokens and blurs data with rules."),
   ("Standing rules removed, relying on model defaults", "The bot would lose its policy.")], level=1)

Q("PC", "Context isolation", """
A main agent must analyse five large log files, but only a short finding from each matters afterwards. How can it avoid filling its own context?""",
  "Delegate each file to a sub-agent for a summary",
  "Sub-agents do the noisy reading in separate contexts and hand back only what matters.",
  [("Read all five files in full into the main context", "Fills the window with material that will not be needed."),
   ("Raise max_tokens so that the logs take up less room", "Output limits do not shrink input."),
   ("Lower the temperature so that less context is used", "Temperature does not affect context size.")])
