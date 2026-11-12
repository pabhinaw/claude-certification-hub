# Question Bank · Tools & MCPs

**21 original questions** (2 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Agentic customisation · MCP architecture · MCP configuration · MCP primitives · MCP server development · MCP vs API client · Tool control · Tool harness · Tool implementation · Tool sets

---

<p class="qb-meta"><span class="qb-id">TM-001</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

When Claude decides to use a client tool, what actually executes the tool?

- **A.** Your application code, which returns the result
- **B.** The user's browser, through an injected script
- **C.** Claude, by calling your function over the network
- **D.** The Anthropic API, using credentials in the prompt

??? success "Answer: A"
    **Why A is right:** Claude emits a request; your code runs it.

    **Why the others are wrong:**

    * **B:** Nothing is injected into a browser.
    * **C:** Claude does not call into your systems.
    * **D:** Client tools are not executed by the API.

---

<p class="qb-meta"><span class="qb-id">TM-002</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which three parts make up a tool definition in the Messages API?

- **A.** name, source code and programming language
- **B.** name, description and input_schema
- **C.** name, return type and timeout in seconds
- **D.** name, endpoint URL and authentication token

??? success "Answer: B"
    **Why B is right:** Name identifies it, description tells Claude when to use it, and input_schema defines its arguments.

    **Why the others are wrong:**

    * **A:** Claude never sees or runs your code.
    * **C:** These are not parts of the definition.
    * **D:** The API never calls your endpoint, so it needs neither.

---

<p class="qb-meta"><span class="qb-id">TM-003</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool wraps an internal API that returns a 4,000-line JSON document. Agent answers become slow and miss key details. What should the tool do?

- **A.** Return the document encoded as base64 text
- **B.** Return nothing and describe the data in the prompt
- **C.** Return only the fields that the task needs
- **D.** Return the full document twice, for extra emphasis

??? success "Answer: C"
    **Why C is right:** Trimming results saves context and keeps the important data visible.

    **Why the others are wrong:**

    * **A:** Still large, and now unreadable.
    * **B:** The agent then has no data.
    * **D:** Doubles the waste.

---

<p class="qb-meta"><span class="qb-id">TM-004</span><span>Tool control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool must receive arguments that match its schema exactly, with no missing required fields or wrong types. Which setting provides this?

- **A.** tool_choice set to auto on the request
- **B.** A longer description for each parameter
- **C.** strict: true on the tool definition
- **D.** A temperature of 0 on the request

??? success "Answer: C"
    **Why C is right:** Strict tool use constrains the generated input to the schema.

    **Why the others are wrong:**

    * **A:** auto only lets Claude decide whether to call a tool.
    * **B:** Helpful, but not a guarantee.
    * **D:** Reduces variation without guaranteeing conformance.

---

<p class="qb-meta"><span class="qb-id">TM-005</span><span>Tool control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Two tools must never be called in the same turn, because the second depends on the first's result. Which setting helps?

- **A.** stream set to true for the request
- **B.** disable_parallel_tool_use set to true
- **C.** max_tokens set to 1 for the request
- **D.** tool_choice set to none for the request

??? success "Answer: B"
    **Why B is right:** It limits Claude to one tool call per turn, so results can be fed back in order.

    **Why the others are wrong:**

    * **A:** Streaming does not affect parallel tool calls.
    * **C:** That prevents any useful response.
    * **D:** That prevents any tool call.

---

<p class="qb-meta"><span class="qb-id">TM-006</span><span>MCP architecture</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

In the Model Context Protocol, which component exposes tools, resources and prompts?

- **A.** The language model
- **B.** The host application
- **C.** The MCP server
- **D.** The MCP client

??? success "Answer: C"
    **Why C is right:** Servers expose capabilities; clients inside a host application connect to them.

    **Why the others are wrong:**

    * **A:** The model uses tools but does not expose them.
    * **B:** The host contains clients; it does not define the server's capabilities.
    * **D:** The client consumes capabilities.

---

<p class="qb-meta"><span class="qb-id">TM-007</span><span>MCP primitives</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A server needs to offer a read-only product catalogue that applications can load as context. Which MCP primitive fits best?

- **A.** A prompt
- **B.** A tool
- **C.** A transport
- **D.** A resource

??? success "Answer: D"
    **Why D is right:** Resources are application-controlled, read-only data addressed by URI.

    **Why the others are wrong:**

    * **A:** Prompts are user-selected templates.
    * **B:** Tools are model-invoked actions; a static catalogue need not be one.
    * **C:** A transport is how messages travel, not a primitive.

---

<p class="qb-meta"><span class="qb-id">TM-008</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A Python MCP server using the stdio transport works in the Inspector, but after a developer adds print() statements for debugging, clients report protocol errors. Why?

- **A.** The server exceeded its limit of tools per process
- **B.** print() is not supported by the MCP Python SDK
- **C.** Debug output needs a separate API key to be sent
- **D.** stdout carries the protocol, so printing corrupts it

??? success "Answer: D"
    **Why D is right:** On stdio, logs must go to stderr.

    **Why the others are wrong:**

    * **A:** Unrelated to printing.
    * **B:** print works; it writes to the wrong place.
    * **C:** No key is involved.

---

<p class="qb-meta"><span class="qb-id">TM-009</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a server built with the Python SDK's FastMCP, what does the model see as a tool's description?

- **A.** The text that the function returns
- **B.** The first comment line in the module
- **C.** The name of the Python file
- **D.** The function's docstring

??? success "Answer: D"
    **Why D is right:** FastMCP builds the description from the docstring and the schema from type hints.

    **Why the others are wrong:**

    * **A:** Return values are results, not descriptions.
    * **B:** Comments are not used.
    * **C:** The file name is not exposed as a description.

---

<p class="qb-meta"><span class="qb-id">TM-010</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which is the most sensible first step to test a newly written MCP server?

- **A.** Rewrite the tool descriptions several times
- **B.** Ask a model whether the server looks correct
- **C.** Call each tool manually in the MCP Inspector
- **D.** Deploy to production and watch the user reports

??? success "Answer: C"
    **Why C is right:** The Inspector exercises the server directly, without a model in the way.

    **Why the others are wrong:**

    * **A:** Descriptions matter only once the server works.
    * **B:** An opinion is not a test.
    * **D:** Testing in production comes far too late.

---

<p class="qb-meta"><span class="qb-id">TM-011</span><span>MCP vs API client</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

One internal application needs to call one endpoint of a pricing service. A developer proposes building an MCP server for it. What is the simpler appropriate design?

- **A.** A normal tool backed by the app's own client
- **B.** An MCP server for each field in the pricing response
- **C.** A remote MCP server with OAuth and a public URL
- **D.** A fine-tuned model that has memorised the prices

??? success "Answer: A"
    **Why A is right:** With a single consumer, MCP adds a process and protocol for no reuse benefit.

    **Why the others are wrong:**

    * **B:** Multiplies the complexity.
    * **C:** Heavy infrastructure for one internal call.
    * **D:** Prices change and must be looked up.

---

<p class="qb-meta"><span class="qb-id">TM-012</span><span>MCP vs API client</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Claude Code, a desktop assistant and two internal agents all need the same issue-tracker integration. Which design avoids writing it four times?

- **A.** Four copies of the client code, one for each host
- **B.** A shared system prompt describing the tracker's API
- **C.** A nightly export of the tracker to a spreadsheet
- **D.** One MCP server that each host connects to

??? success "Answer: D"
    **Why D is right:** MCP lets one implementation be reused by every compatible host.

    **Why the others are wrong:**

    * **A:** The duplication the question wants to avoid.
    * **B:** A description cannot perform the calls.
    * **C:** Stale data and no ability to act.

---

<p class="qb-meta"><span class="qb-id">TM-013</span><span>MCP configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A project's .mcp.json is committed so that the whole team gets the same server. How should the server's API token be supplied?

- **A.** By variable expansion, e.g. ${TRACKER_TOKEN}
- **B.** In the server's name, so that it is easy to find
- **C.** As a literal string in the committed file
- **D.** In the project's CLAUDE.md under a heading

??? success "Answer: A"
    **Why A is right:** The file is shared; each person supplies the secret from their own environment.

    **Why the others are wrong:**

    * **B:** Names are not a place for secrets.
    * **C:** Publishes the secret to everyone with repository access.
    * **D:** Also committed, and read into context.

---

<p class="qb-meta"><span class="qb-id">TM-014</span><span>MCP primitives</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about MCP primitives are correct? (Select TWO.)

- **A.** Tools are actions the model can decide to invoke
- **B.** Prompts are reusable templates that a user selects
- **C.** Prompts are executed automatically on every request
- **D.** Resources are actions that modify external systems
- **E.** Tools can only be offered over the stdio transport

??? success "Answer: A and B"
    **Why A is right:** Tools are model-controlled.

    **Why B is right:** Prompts are user-controlled.

    **Why the others are wrong:**

    * **C:** They are chosen, not automatic.
    * **D:** Resources are read-only data.
    * **E:** Tools work over any transport.

---

<p class="qb-meta"><span class="qb-id">TM-015</span><span>Agentic customisation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants Claude to follow its detailed release-notes procedure, including a template and a formatting script. No new system access is required. Which mechanism fits best?

- **A.** A skill with the instructions and script
- **B.** An MCP server exposing the procedure as a tool
- **C.** A PreToolUse hook that blocks all file edits
- **D.** A higher permission mode for the whole project

??? success "Answer: A"
    **Why A is right:** Skills package know-how that loads on demand. Nothing here needs new connectivity.

    **Why the others are wrong:**

    * **B:** MCP provides access to systems; this is procedural knowledge.
    * **C:** A hook enforces rules; it does not teach a procedure.
    * **D:** Permissions do not supply knowledge.

---

<p class="qb-meta"><span class="qb-id">TM-016</span><span>Agentic customisation</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

An agent needs to search files and run shell commands in a repository. A developer starts writing custom tools for both. What is the better choice?

- **A.** Use the built-in tools that already do this
- **B.** Write an MCP server that wraps the shell command
- **C.** Write a skill that describes how a search would work
- **D.** Ask users to paste file contents into the chat

??? success "Answer: A"
    **Why A is right:** Built-in tools are available and tested. Rebuilding them adds work and risk.

    **Why the others are wrong:**

    * **B:** Recreates what already exists.
    * **C:** A description does not perform the search.
    * **D:** Manual and defeats the purpose of an agent.

---

<p class="qb-meta"><span class="qb-id">TM-017</span><span>Agentic customisation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which statement best distinguishes a skill from an MCP server?

- **A.** A skill replaces the model; an MCP server replaces tools
- **B.** A skill supplies know-how; an MCP server supplies access
- **C.** A skill is always loaded in full; MCP tools never are
- **D.** A skill needs a network port; an MCP server does not

??? success "Answer: B"
    **Why B is right:** Skills teach procedures and methods. MCP connects the agent to external tools and data.

    **Why the others are wrong:**

    * **A:** Neither replaces the model.
    * **C:** Skill bodies load on demand.
    * **D:** Skills are files; remote MCP servers are the networked ones.

---

<p class="qb-meta"><span class="qb-id">TM-018</span><span>Tool harness</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent harness receives a tool_use block naming a tool that does not exist in its dispatch table. What should it do?

- **A.** Run the most similar tool that it happens to have
- **B.** Return an error tool_result so that the model can recover
- **C.** Crash the process so that the bug is clearly visible
- **D.** Return a success result containing an empty string

??? success "Answer: B"
    **Why B is right:** An unknown tool is a recoverable condition. The loop continues with a clear error.

    **Why the others are wrong:**

    * **A:** Could perform an unintended action.
    * **C:** Loses the task for a recoverable problem.
    * **D:** Misleads the model into thinking it worked.

---

<p class="qb-meta"><span class="qb-id">TM-019</span><span>Tool harness</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A harness auto-runs read-only tools, asks for confirmation on tools that change data, and refuses destructive ones. What is this pattern?

- **A.** Prompt chaining implemented in the system prompt
- **B.** Risk-based approval implemented in the harness
- **C.** Prompt caching implemented with four breakpoints
- **D.** Model routing implemented with a small classifier

??? success "Answer: B"
    **Why B is right:** Classifying tools by risk and enforcing the policy in code is a standard approval pattern.

    **Why the others are wrong:**

    * **A:** This is about tool approval, not chaining prompts.
    * **C:** Unrelated to approval.
    * **D:** Routing selects a model or path, not tool permissions.

---

<p class="qb-meta"><span class="qb-id">TM-020</span><span>Tool sets</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent has 45 tools, several with overlapping purposes. It often picks the wrong one. Which change helps most?

- **A.** Rename the tools with numbers in place of words
- **B.** Give it fewer, distinct, well-described tools
- **C.** Give every tool the same short generic description
- **D.** Add ten more tools to cover the remaining gaps

??? success "Answer: B"
    **Why B is right:** Fewer, non-overlapping tools improve selection and reduce tokens on every request.

    **Why the others are wrong:**

    * **A:** Meaningless names worsen selection.
    * **C:** Removes the signal used for selection.
    * **D:** Makes selection harder.

---

<p class="qb-meta"><span class="qb-id">TM-021</span><span>Agentic customisation</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO pairings of need and mechanism are appropriate? (Select TWO.)

- **A.** Reusable access to a ticketing system from several hosts: an MCP server
- **B.** A team's writing style guide: a network transport
- **C.** A rule that must block a command every time: a hook
- **D.** A hard security limit: a sentence in a skill description
- **E.** Reading local files in a repository: a new custom MCP server

??? success "Answer: A and C"
    **Why A is right:** MCP provides shared connectivity.

    **Why C is right:** Hooks are deterministic.

    **Why the others are wrong:**

    * **B:** A transport carries messages; it holds no guidance.
    * **D:** A description is advisory.
    * **E:** Built-in tools already do this.

---
