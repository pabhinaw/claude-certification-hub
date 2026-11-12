# Question Bank · Agents & Workflows

**24 original questions** (2 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Agent SDK · Agent construction · Agent loop · Frameworks · Hosting · Human approval · Memory · Patterns · Runaway loops · Stop conditions · Sub-agents · Supervisor hierarchies · Workflow vs agent

---

<p class="qb-meta"><span class="qb-id">AW-001</span><span>Workflow vs agent</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is the defining difference between a workflow and an agent?

- **A.** A workflow uses one model; an agent always uses several
- **B.** Code fixes a workflow's steps; an agent's model chooses
- **C.** A workflow runs in batch; an agent always runs in real time
- **D.** A workflow cannot call tools; an agent always calls tools

??? success "Answer: B"
    **Why B is right:** The distinction is who controls the sequence of actions.

    **Why the others are wrong:**

    * **A:** Either can use one or many models.
    * **C:** Timing mode is unrelated.
    * **D:** Workflows can use tools too.

---

<p class="qb-meta"><span class="qb-id">AW-002</span><span>Agent loop</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

In a hand-written agent loop, what should decide whether to make another call to Claude?

- **A.** Whether exactly ten iterations have been completed
- **B.** Whether the response's stop_reason is tool_use
- **C.** Whether the response is shorter than the previous one
- **D.** Whether the response text contains the word "done"

??? success "Answer: B"
    **Why B is right:** tool_use means Claude is waiting for results. Any other value ends or interrupts the loop.

    **Why the others are wrong:**

    * **A:** A fixed count is a safety cap, not a completion signal.
    * **C:** Length says nothing about completion.
    * **D:** Text matching is fragile and easily wrong.

---

<p class="qb-meta"><span class="qb-id">AW-003</span><span>Agent loop</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Claude's response contains two tool_use blocks. How should the application reply?

- **A.** Two separate user messages, each with one tool_result
- **B.** Only the first result; Claude will ask again for the second
- **C.** One user message with two ID-matched tool_result blocks
- **D.** One assistant message containing both of the results

??? success "Answer: C"
    **Why C is right:** All results for a turn go back together, each linked to its request by ID.

    **Why the others are wrong:**

    * **A:** Results for one assistant turn belong in a single user message.
    * **B:** Every tool_use needs a result or the request is invalid.
    * **D:** Tool results are sent in a user message.

---

<p class="qb-meta"><span class="qb-id">AW-004</span><span>Agent loop</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool raises an exception inside an agent loop. What is the best way to handle it?

- **A.** Let the exception end the process so that it is noticed
- **B.** Return a made-up success value to keep the flow simple
- **C.** Return a tool_result with is_error true and a reason
- **D.** Return an empty string so that the loop carries on

??? success "Answer: C"
    **Why C is right:** The model can then retry, try another route, or explain the problem.

    **Why the others are wrong:**

    * **A:** Crashing loses the task and the context.
    * **B:** Fabricated results cause wrong answers.
    * **D:** Hiding the failure misleads the model.

---

<p class="qb-meta"><span class="qb-id">AW-005</span><span>Stop conditions</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent loop has a limit of 20 iterations. How should that limit be regarded?

- **A.** As a target the agent should try to reach each time
- **B.** As the normal way for the agent to finish its tasks
- **C.** As a safety net that triggers escalation if reached
- **D.** As unnecessary, since models always stop by themselves

??? success "Answer: C"
    **Why C is right:** Normal completion is signalled by stop_reason. A cap guards against runaway loops.

    **Why the others are wrong:**

    * **A:** More turns are not better.
    * **B:** Finishing by exhaustion means the task did not complete properly.
    * **D:** Loops can and do run away.

---

<p class="qb-meta"><span class="qb-id">AW-006</span><span>Runaway loops</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent calls the same search tool with the same query fifteen times in a row. The tool returns "Error" each time. Which change addresses the root cause?

- **A.** Raise the iteration limit so that the agent has more attempts
- **B.** Remove the iteration limit to avoid cutting the agent off
- **C.** Raise the temperature so that the queries vary a little
- **D.** Return a specific error and whether a retry can help

??? success "Answer: D"
    **Why D is right:** With an informative error the model can change approach instead of repeating itself.

    **Why the others are wrong:**

    * **A:** More attempts at the same failing call.
    * **B:** That removes the only protection.
    * **C:** Random variation does not fix a failing tool.

---

<p class="qb-meta"><span class="qb-id">AW-007</span><span>Human approval</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent can issue refunds. Policy says refunds above a set amount must be approved by a manager, without exception. How should this be implemented?

- **A.** A sentence in the system prompt stating the policy firmly
- **B.** A lower temperature so that the agent follows the policy
- **C.** A few-shot example showing the agent asking a manager
- **D.** A code check that blocks the tool until approved

??? success "Answer: D"
    **Why D is right:** A rule that must always hold needs deterministic enforcement outside the model.

    **Why the others are wrong:**

    * **A:** Prompts guide behaviour but cannot guarantee it.
    * **B:** Sampling settings are not enforcement.
    * **C:** Examples make it likelier, not certain.

---

<p class="qb-meta"><span class="qb-id">AW-008</span><span>Human approval</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team adds a human approval step before every tool call, including read-only lookups. Reviewers soon approve everything without reading. What is the better design?

- **A.** Require two approvers for every single tool call
- **B.** Remove approval entirely, since it isn't being read
- **C.** Show reviewers less information so that they go faster
- **D.** Require approval only for risky or irreversible actions

??? success "Answer: D"
    **Why D is right:** Gating by risk keeps reviews meaningful and avoids approval fatigue.

    **Why the others are wrong:**

    * **A:** That doubles the fatigue.
    * **B:** Risky actions would then be unguarded.
    * **C:** Reviewers need the exact action to judge it.

---

<p class="qb-meta"><span class="qb-id">AW-009</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A lead agent delegates research to a sub-agent with the instruction "research the product we discussed". The sub-agent returns generic material. Why?

- **A.** Sub-agents start fresh and never saw that discussion
- **B.** Sub-agents always ignore the first instruction given
- **C.** Sub-agents cannot use search tools of any kind
- **D.** Sub-agents are limited to the smallest model tier

??? success "Answer: A"
    **Why A is right:** Everything a sub-agent needs must be passed explicitly in its task.

    **Why the others are wrong:**

    * **B:** There is no such behaviour.
    * **C:** They can be given tools.
    * **D:** They can use any configured model.

---

<p class="qb-meta"><span class="qb-id">AW-010</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is a main benefit of delegating a noisy exploration task to a sub-agent?

- **A.** The noise stays out of the main context window
- **B.** The sub-agent shares and extends the parent's context
- **C.** The sub-agent's tokens are not billed to the account
- **D.** The sub-agent's output is guaranteed to be correct

??? success "Answer: A"
    **Why A is right:** Context isolation keeps the lead agent's window focused.

    **Why the others are wrong:**

    * **B:** It has a separate context.
    * **C:** All tokens are billed.
    * **D:** No such guarantee exists.

---

<p class="qb-meta"><span class="qb-id">AW-011</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A simple, strictly sequential task is split across five sub-agents. It becomes slower and more expensive, with no quality gain. What does this illustrate?

- **A.** Multi-agent overhead only pays off for separable work
- **B.** Five is too few; at least ten sub-agents are needed
- **C.** Sub-agents should always be run on the largest tier
- **D.** Sequential tasks cannot be done by language models

??? success "Answer: A"
    **Why A is right:** Sub-agents pay off with parallel or specialised sub-tasks, not simple linear ones.

    **Why the others are wrong:**

    * **B:** More agents add more overhead.
    * **C:** That would raise cost further.
    * **D:** A single agent or chain handles them well.

---

<p class="qb-meta"><span class="qb-id">AW-012</span><span>Agent SDK</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Using the Claude Agent SDK, a code-review agent must be able to read and search files but never modify them. Which configuration achieves this?

- **A.** Set the temperature to 0 so that it stays cautious
- **B.** Set allowed_tools to read and search tools only
- **C.** Set max_turns to 1 so that there is no time to edit
- **D.** Ask in the system prompt that files are not modified

??? success "Answer: B"
    **Why B is right:** Restricting the tool set is least privilege, enforced by the SDK.

    **Why the others are wrong:**

    * **A:** Temperature does not control tool access.
    * **C:** A turn limit does not remove the ability to edit.
    * **D:** A request, not a restriction.

---

<p class="qb-meta"><span class="qb-id">AW-013</span><span>Agent SDK</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

When is the Claude Agent SDK a better choice than a hand-written loop on the Messages API?

- **A.** When the application makes one call with no tools
- **B.** When built-in tools, hooks and sessions are wanted
- **C.** When token usage must go unrecorded
- **D.** When no tool should ever run in the application

??? success "Answer: B"
    **Why B is right:** The SDK packages the loop and the surrounding machinery.

    **Why the others are wrong:**

    * **A:** A direct API call is simpler.
    * **C:** Neither approach hides usage.
    * **D:** The SDK's value is largely in tools.

---

<p class="qb-meta"><span class="qb-id">AW-014</span><span>Patterns</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A task requires a draft to be improved against clear quality criteria over several rounds. Which pattern fits?

- **A.** A single call with a very high max_tokens value
- **B.** Evaluator-optimiser: generate, critique, then revise
- **C.** Parallelisation: produce ten drafts and return them all
- **D.** Routing: classify the draft and send it to one handler

??? success "Answer: B"
    **Why B is right:** Iterative refinement against criteria is exactly what this pattern provides.

    **Why the others are wrong:**

    * **A:** More room does not add a review step.
    * **C:** That produces alternatives, not a refined result.
    * **D:** Routing selects a path; it does not iterate.

---

<p class="qb-meta"><span class="qb-id">AW-015</span><span>Stop conditions</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO are appropriate safety limits for an autonomous agent loop? (Select TWO.)

- **A.** A maximum number of iterations
- **B.** A total token or cost budget for the task
- **C.** A minimum number of tool calls per turn
- **D.** A temperature of exactly 1.0 on every call
- **E.** A rule that the agent may never return end_turn

??? success "Answer: A and B"
    **Why A is right:** Bounds how long a loop can run.

    **Why B is right:** Bounds spending across all calls.

    **Why the others are wrong:**

    * **C:** Forcing tool calls encourages needless work.
    * **D:** Temperature is not a safety limit.
    * **E:** That would stop it from finishing.

---

<p class="qb-meta"><span class="qb-id">AW-016</span><span>Agent loop</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about returning tool results are correct? (Select TWO.)

- **A.** tool_result blocks are placed in an assistant message
- **B.** Each tool_result must reference the tool_use_id it answers
- **C.** Results may be omitted for tools that returned nothing
- **D.** A failed tool call should be returned with is_error set to true
- **E.** Results must be summarised by a second model first

??? success "Answer: B and D"
    **Why B is right:** The ID links a result to its request.

    **Why D is right:** The model needs to know that it failed.

    **Why the others are wrong:**

    * **A:** They are sent in a user message.
    * **C:** Every tool_use needs a result, even an empty one.
    * **E:** No such requirement exists.

---

<p class="qb-meta"><span class="qb-id">AW-017</span><span>Hosting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants long-running agents but does not want to build sandboxing, session storage and scaling. Data requirements permit a hosted service. Which option fits?

- **A.** A nightly batch of unrelated summary requests
- **B.** A hand-written loop on a developer's laptop
- **C.** An Anthropic-hosted managed agent service
- **D.** A single Messages API call with a long prompt

??? success "Answer: C"
    **Why C is right:** A managed service runs the harness and infrastructure, which suits long-running and asynchronous work.

    **Why the others are wrong:**

    * **A:** Batches are not interactive agents.
    * **B:** Not durable or scalable for long-running work.
    * **D:** One call is not a long-running agent.

---

<p class="qb-meta"><span class="qb-id">AW-018</span><span>Hosting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent must read files on an internal network that cannot be exposed outside the company. Which deployment is most appropriate?

- **A.** A hosted agent given the network's admin password
- **B.** A public MCP server that publishes the files
- **C.** A self-hosted agent running inside the company network
- **D.** A chat app where staff paste the files by hand

??? success "Answer: C"
    **Why C is right:** Self-hosting keeps the loop, files and credentials in the organisation's own environment.

    **Why the others are wrong:**

    * **A:** Sharing credentials outward defeats the restriction.
    * **B:** Exposes what must stay private.
    * **D:** Manual, error-prone and not an agent.

---

<p class="qb-meta"><span class="qb-id">AW-019</span><span>Frameworks</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team needs an agent workflow with explicit steps, saved state between steps, and pauses for human approval. Which kind of framework is designed for this?

- **A.** An object-relational mapper for the database
- **B.** A unit-testing framework with assertion helpers
- **C.** A graph-based framework such as LangGraph
- **D.** A CSS framework for styling the approval screen

??? success "Answer: C"
    **Why C is right:** Graph frameworks model nodes, edges and state explicitly, with checkpoints and human-in-the-loop pauses.

    **Why the others are wrong:**

    * **A:** Persistence libraries do not define agent control flow.
    * **B:** Testing tools do not orchestrate agents.
    * **D:** Unrelated to agent orchestration.

---

<p class="qb-meta"><span class="qb-id">AW-020</span><span>Frameworks</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What is the main risk of adopting an agent framework before understanding the underlying API calls?

- **A.** Frameworks only work with the smallest model tier
- **B.** Frameworks prevent the use of any tool definitions
- **C.** Frameworks make each API call cost twice as much
- **D.** The abstraction hides the prompts and requests

??? success "Answer: D"
    **Why D is right:** When something goes wrong you need to see what was actually sent. Heavy abstraction can obscure it.

    **Why the others are wrong:**

    * **A:** They work with any tier.
    * **B:** Frameworks generally support tools.
    * **C:** Pricing is unaffected by the framework itself.

---

<p class="qb-meta"><span class="qb-id">AW-021</span><span>Supervisor hierarchies</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

When is a supervisor agent with several workers a good design?

- **A.** When the task is a single short classification
- **B.** When the token budget for the task is very limited
- **C.** When every step depends closely on the previous one
- **D.** When the work splits into independent, parallel parts

??? success "Answer: D"
    **Why D is right:** Hierarchies pay off for broad, separable work. For sequential tasks they add cost and hand-off errors.

    **Why the others are wrong:**

    * **A:** Far too much machinery for one call.
    * **B:** Hierarchies multiply token use.
    * **C:** Tightly coupled steps suit a single agent or a chain.

---

<p class="qb-meta"><span class="qb-id">AW-022</span><span>Memory</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent keeps a single shared memory file for all users. One user's reply mentions another user's project. What design rule was broken?

- **A.** Memory must be stored inside the system prompt
- **B.** Memory must be written in upper-case letters only
- **C.** Memory must be reloaded twice in each new session
- **D.** Memory must be scoped per user or project

??? success "Answer: D"
    **Why D is right:** Unscoped memory leaks information between users. Scope and load only what is relevant.

    **Why the others are wrong:**

    * **A:** Location in the prompt does not isolate users.
    * **B:** Formatting does not isolate users.
    * **C:** Reloading does not scope it.

---

<p class="qb-meta"><span class="qb-id">AW-023</span><span>Agent construction</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In an Agent SDK application, a rule must run every time before any shell command executes, whatever the model decides. Which feature provides this?

- **A.** A hook registered for the pre-tool-use event
- **B.** A lower limit on the number of turns
- **C.** A sentence in the system prompt option
- **D.** A description added to the sub-agent

??? success "Answer: A"
    **Why A is right:** Hooks run deterministically at lifecycle points and can block the action.

    **Why the others are wrong:**

    * **B:** A turn cap does not inspect commands.
    * **C:** Advisory, not deterministic.
    * **D:** Descriptions guide delegation, not enforcement.

---

<p class="qb-meta"><span class="qb-id">AW-024</span><span>Agent construction</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What does a custom agent harness need to do that a single Messages API call does not?

- **A.** Run tools, feed results back, and decide when to stop
- **B.** Translate each prompt into a different language
- **C.** Train the model on the user's documents first
- **D.** Replace the system prompt after every single token

??? success "Answer: A"
    **Why A is right:** A harness is the loop around the model: dispatching tools, managing context and enforcing limits.

    **Why the others are wrong:**

    * **B:** Unrelated to what a harness does.
    * **C:** No training happens in a harness.
    * **D:** Not something a harness does.

---
