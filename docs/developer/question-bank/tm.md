# Question Bank · Tools & MCPs

**14 original questions** (1 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** MCP architecture · MCP configuration · MCP primitives · MCP server development · MCP vs API client · Tool control · Tool implementation

---

<p class="qb-meta"><span class="qb-id">TM-001</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

When Claude decides to use a client tool, what actually executes the tool?

- **A.** The Anthropic API, using credentials in the prompt
- **B.** Your application code, which returns the result
- **C.** The user's browser, through an injected script
- **D.** Claude, by calling your function over the network

??? success "Answer: B"
    **Why B is right:** Claude emits a request; your code runs it.

    **Why the others are wrong:**

    * **A:** Client tools are not executed by the API.
    * **C:** Nothing is injected into a browser.
    * **D:** Claude does not call into your systems.

---

<p class="qb-meta"><span class="qb-id">TM-002</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which three parts make up a tool definition in the Messages API?

- **A.** name, source code and programming language
- **B.** name, return type and timeout in seconds
- **C.** name, description and input_schema
- **D.** name, endpoint URL and authentication token

??? success "Answer: C"
    **Why C is right:** Name identifies it, description tells Claude when to use it, and input_schema defines its arguments.

    **Why the others are wrong:**

    * **A:** Claude never sees or runs your code.
    * **B:** These are not parts of the definition.
    * **D:** The API never calls your endpoint, so it needs neither.

---

<p class="qb-meta"><span class="qb-id">TM-003</span><span>Tool implementation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool wraps an internal API that returns a 4,000-line JSON document. Agent answers become slow and miss key details. What should the tool do?

- **A.** Return nothing and describe the data in the prompt
- **B.** Return the document encoded as base64 text
- **C.** Return only the fields that the task needs
- **D.** Return the full document twice, for extra emphasis

??? success "Answer: C"
    **Why C is right:** Trimming results saves context and keeps the important data visible.

    **Why the others are wrong:**

    * **A:** The agent then has no data.
    * **B:** Still large, and now unreadable.
    * **D:** Doubles the waste.

---

<p class="qb-meta"><span class="qb-id">TM-004</span><span>Tool control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool must receive arguments that match its schema exactly, with no missing required fields or wrong types. Which setting provides this?

- **A.** A longer description for each parameter
- **B.** A temperature of 0 on the request
- **C.** tool_choice set to auto on the request
- **D.** strict: true on the tool definition

??? success "Answer: D"
    **Why D is right:** Strict tool use constrains the generated input to the schema.

    **Why the others are wrong:**

    * **A:** Helpful, but not a guarantee.
    * **B:** Reduces variation without guaranteeing conformance.
    * **C:** auto only lets Claude decide whether to call a tool.

---

<p class="qb-meta"><span class="qb-id">TM-005</span><span>Tool control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Two tools must never be called in the same turn, because the second depends on the first's result. Which setting helps?

- **A.** stream set to true for the request
- **B.** tool_choice set to none for the request
- **C.** max_tokens set to 1 for the request
- **D.** disable_parallel_tool_use set to true

??? success "Answer: D"
    **Why D is right:** It limits Claude to one tool call per turn, so results can be fed back in order.

    **Why the others are wrong:**

    * **A:** Streaming does not affect parallel tool calls.
    * **B:** That prevents any tool call.
    * **C:** That prevents any useful response.

---

<p class="qb-meta"><span class="qb-id">TM-006</span><span>MCP architecture</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

In the Model Context Protocol, which component exposes tools, resources and prompts?

- **A.** The MCP server
- **B.** The language model
- **C.** The host application
- **D.** The MCP client

??? success "Answer: A"
    **Why A is right:** Servers expose capabilities; clients inside a host application connect to them.

    **Why the others are wrong:**

    * **B:** The model uses tools but does not expose them.
    * **C:** The host contains clients; it does not define the server's capabilities.
    * **D:** The client consumes capabilities.

---

<p class="qb-meta"><span class="qb-id">TM-007</span><span>MCP primitives</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A server needs to offer a read-only product catalogue that applications can load as context. Which MCP primitive fits best?

- **A.** A resource
- **B.** A transport
- **C.** A prompt
- **D.** A tool

??? success "Answer: A"
    **Why A is right:** Resources are application-controlled, read-only data addressed by URI.

    **Why the others are wrong:**

    * **B:** A transport is how messages travel, not a primitive.
    * **C:** Prompts are user-selected templates.
    * **D:** Tools are model-invoked actions; a static catalogue need not be one.

---

<p class="qb-meta"><span class="qb-id">TM-008</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A Python MCP server using the stdio transport works in the Inspector, but after a developer adds print() statements for debugging, clients report protocol errors. Why?

- **A.** Debug output needs a separate API key to be sent
- **B.** stdout carries the protocol, so printing corrupts it
- **C.** The server exceeded its limit of tools per process
- **D.** print() is not supported by the MCP Python SDK

??? success "Answer: B"
    **Why B is right:** On stdio, logs must go to stderr.

    **Why the others are wrong:**

    * **A:** No key is involved.
    * **C:** Unrelated to printing.
    * **D:** print works; it writes to the wrong place.

---

<p class="qb-meta"><span class="qb-id">TM-009</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a server built with the Python SDK's FastMCP, what does the model see as a tool's description?

- **A.** The first comment line in the module
- **B.** The function's docstring
- **C.** The name of the Python file
- **D.** The text that the function returns

??? success "Answer: B"
    **Why B is right:** FastMCP builds the description from the docstring and the schema from type hints.

    **Why the others are wrong:**

    * **A:** Comments are not used.
    * **C:** The file name is not exposed as a description.
    * **D:** Return values are results, not descriptions.

---

<p class="qb-meta"><span class="qb-id">TM-010</span><span>MCP server development</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which is the most sensible first step to test a newly written MCP server?

- **A.** Ask a model whether the server looks correct
- **B.** Deploy to production and watch the user reports
- **C.** Call each tool manually in the MCP Inspector
- **D.** Rewrite the tool descriptions several times

??? success "Answer: C"
    **Why C is right:** The Inspector exercises the server directly, without a model in the way.

    **Why the others are wrong:**

    * **A:** An opinion is not a test.
    * **B:** Testing in production comes far too late.
    * **D:** Descriptions matter only once the server works.

---

<p class="qb-meta"><span class="qb-id">TM-011</span><span>MCP vs API client</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

One internal application needs to call one endpoint of a pricing service. A developer proposes building an MCP server for it. What is the simpler appropriate design?

- **A.** A fine-tuned model that has memorised the prices
- **B.** A remote MCP server with OAuth and a public URL
- **C.** An MCP server for each field in the pricing response
- **D.** A normal tool backed by the app's own client

??? success "Answer: D"
    **Why D is right:** With a single consumer, MCP adds a process and protocol for no reuse benefit.

    **Why the others are wrong:**

    * **A:** Prices change and must be looked up.
    * **B:** Heavy infrastructure for one internal call.
    * **C:** Multiplies the complexity.

---

<p class="qb-meta"><span class="qb-id">TM-012</span><span>MCP vs API client</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Claude Code, a desktop assistant and two internal agents all need the same issue-tracker integration. Which design avoids writing it four times?

- **A.** A nightly export of the tracker to a spreadsheet
- **B.** A shared system prompt describing the tracker's API
- **C.** One MCP server that each host connects to
- **D.** Four copies of the client code, one for each host

??? success "Answer: C"
    **Why C is right:** MCP lets one implementation be reused by every compatible host.

    **Why the others are wrong:**

    * **A:** Stale data and no ability to act.
    * **B:** A description cannot perform the calls.
    * **D:** The duplication the question wants to avoid.

---

<p class="qb-meta"><span class="qb-id">TM-013</span><span>MCP configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A project's .mcp.json is committed so that the whole team gets the same server. How should the server's API token be supplied?

- **A.** By variable expansion, e.g. ${TRACKER_TOKEN}
- **B.** As a literal string in the committed file
- **C.** In the project's CLAUDE.md under a heading
- **D.** In the server's name, so that it is easy to find

??? success "Answer: A"
    **Why A is right:** The file is shared; each person supplies the secret from their own environment.

    **Why the others are wrong:**

    * **B:** Publishes the secret to everyone with repository access.
    * **C:** Also committed, and read into context.
    * **D:** Names are not a place for secrets.

---

<p class="qb-meta"><span class="qb-id">TM-014</span><span>MCP primitives</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about MCP primitives are correct? (Select TWO.)

- **A.** Resources are actions that modify external systems
- **B.** Tools are actions the model can decide to invoke
- **C.** Tools can only be offered over the stdio transport
- **D.** Prompts are reusable templates that a user selects
- **E.** Prompts are executed automatically on every request

??? success "Answer: B and D"
    **Why B is right:** Tools are model-controlled.

    **Why D is right:** Prompts are user-controlled.

    **Why the others are wrong:**

    * **A:** Resources are read-only data.
    * **C:** Tools work over any transport.
    * **E:** They are chosen, not automatic.

---
