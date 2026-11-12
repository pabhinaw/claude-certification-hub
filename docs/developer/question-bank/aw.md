# Question Bank · Agents & Workflows

**16 original questions** (2 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Agent SDK · Agent loop · Human approval · Patterns · Runaway loops · Stop conditions · Sub-agents · Workflow vs agent

---

<p class="qb-meta"><span class="qb-id">AW-001</span><span>Workflow vs agent</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is the defining difference between a workflow and an agent?

- **A.** A workflow uses one model; an agent always uses several
- **B.** Code fixes a workflow's steps; an agent's model chooses
- **C.** A workflow cannot call tools; an agent always calls tools
- **D.** A workflow runs in batch; an agent always runs in real time

??? success "Answer: B"
    **Why B is right:** The distinction is who controls the sequence of actions.

    **Why the others are wrong:**

    * **A:** Either can use one or many models.
    * **C:** Workflows can use tools too.
    * **D:** Timing mode is unrelated.

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
- **B.** One assistant message containing both of the results
- **C.** One user message with two ID-matched tool_result blocks
- **D.** Only the first result; Claude will ask again for the second

??? success "Answer: C"
    **Why C is right:** All results for a turn go back together, each linked to its request by ID.

    **Why the others are wrong:**

    * **A:** Results for one assistant turn belong in a single user message.
    * **B:** Tool results are sent in a user message.
    * **D:** Every tool_use needs a result or the request is invalid.

---

<p class="qb-meta"><span class="qb-id">AW-004</span><span>Agent loop</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool raises an exception inside an agent loop. What is the best way to handle it?

- **A.** Return an empty string so that the loop carries on
- **B.** Return a made-up success value to keep the flow simple
- **C.** Return a tool_result with is_error true and a reason
- **D.** Let the exception end the process so that it is noticed

??? success "Answer: C"
    **Why C is right:** The model can then retry, try another route, or explain the problem.

    **Why the others are wrong:**

    * **A:** Hiding the failure misleads the model.
    * **B:** Fabricated results cause wrong answers.
    * **D:** Crashing loses the task and the context.

---

<p class="qb-meta"><span class="qb-id">AW-005</span><span>Stop conditions</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent loop has a limit of 20 iterations. How should that limit be regarded?

- **A.** As the normal way for the agent to finish its tasks
- **B.** As a target the agent should try to reach each time
- **C.** As unnecessary, since models always stop by themselves
- **D.** As a safety net that triggers escalation if reached

??? success "Answer: D"
    **Why D is right:** Normal completion is signalled by stop_reason. A cap guards against runaway loops.

    **Why the others are wrong:**

    * **A:** Finishing by exhaustion means the task did not complete properly.
    * **B:** More turns are not better.
    * **C:** Loops can and do run away.

---

<p class="qb-meta"><span class="qb-id">AW-006</span><span>Runaway loops</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent calls the same search tool with the same query fifteen times in a row. The tool returns "Error" each time. Which change addresses the root cause?

- **A.** Raise the temperature so that the queries vary a little
- **B.** Raise the iteration limit so that the agent has more attempts
- **C.** Remove the iteration limit to avoid cutting the agent off
- **D.** Return a specific error and whether a retry can help

??? success "Answer: D"
    **Why D is right:** With an informative error the model can change approach instead of repeating itself.

    **Why the others are wrong:**

    * **A:** Random variation does not fix a failing tool.
    * **B:** More attempts at the same failing call.
    * **C:** That removes the only protection.

---

<p class="qb-meta"><span class="qb-id">AW-007</span><span>Human approval</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent can issue refunds. Policy says refunds above a set amount must be approved by a manager, without exception. How should this be implemented?

- **A.** A code check that blocks the tool until approved
- **B.** A sentence in the system prompt stating the policy firmly
- **C.** A lower temperature so that the agent follows the policy
- **D.** A few-shot example showing the agent asking a manager

??? success "Answer: A"
    **Why A is right:** A rule that must always hold needs deterministic enforcement outside the model.

    **Why the others are wrong:**

    * **B:** Prompts guide behaviour but cannot guarantee it.
    * **C:** Sampling settings are not enforcement.
    * **D:** Examples make it likelier, not certain.

---

<p class="qb-meta"><span class="qb-id">AW-008</span><span>Human approval</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team adds a human approval step before every tool call, including read-only lookups. Reviewers soon approve everything without reading. What is the better design?

- **A.** Require approval only for risky or irreversible actions
- **B.** Show reviewers less information so that they go faster
- **C.** Remove approval entirely, since it isn't being read
- **D.** Require two approvers for every single tool call

??? success "Answer: A"
    **Why A is right:** Gating by risk keeps reviews meaningful and avoids approval fatigue.

    **Why the others are wrong:**

    * **B:** Reviewers need the exact action to judge it.
    * **C:** Risky actions would then be unguarded.
    * **D:** That doubles the fatigue.

---

<p class="qb-meta"><span class="qb-id">AW-009</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A lead agent delegates research to a sub-agent with the instruction "research the product we discussed". The sub-agent returns generic material. Why?

- **A.** Sub-agents are limited to the smallest model tier
- **B.** Sub-agents start fresh and never saw that discussion
- **C.** Sub-agents always ignore the first instruction given
- **D.** Sub-agents cannot use search tools of any kind

??? success "Answer: B"
    **Why B is right:** Everything a sub-agent needs must be passed explicitly in its task.

    **Why the others are wrong:**

    * **A:** They can use any configured model.
    * **C:** There is no such behaviour.
    * **D:** They can be given tools.

---

<p class="qb-meta"><span class="qb-id">AW-010</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is a main benefit of delegating a noisy exploration task to a sub-agent?

- **A.** The sub-agent's tokens are not billed to the account
- **B.** The noise stays out of the main context window
- **C.** The sub-agent's output is guaranteed to be correct
- **D.** The sub-agent shares and extends the parent's context

??? success "Answer: B"
    **Why B is right:** Context isolation keeps the lead agent's window focused.

    **Why the others are wrong:**

    * **A:** All tokens are billed.
    * **C:** No such guarantee exists.
    * **D:** It has a separate context.

---

<p class="qb-meta"><span class="qb-id">AW-011</span><span>Sub-agents</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A simple, strictly sequential task is split across five sub-agents. It becomes slower and more expensive, with no quality gain. What does this illustrate?

- **A.** Five is too few; at least ten sub-agents are needed
- **B.** Sub-agents should always be run on the largest tier
- **C.** Multi-agent overhead only pays off for separable work
- **D.** Sequential tasks cannot be done by language models

??? success "Answer: C"
    **Why C is right:** Sub-agents pay off with parallel or specialised sub-tasks, not simple linear ones.

    **Why the others are wrong:**

    * **A:** More agents add more overhead.
    * **B:** That would raise cost further.
    * **D:** A single agent or chain handles them well.

---

<p class="qb-meta"><span class="qb-id">AW-012</span><span>Agent SDK</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Using the Claude Agent SDK, a code-review agent must be able to read and search files but never modify them. Which configuration achieves this?

- **A.** Ask in the system prompt that files are not modified
- **B.** Set the temperature to 0 so that it stays cautious
- **C.** Set allowed_tools to read and search tools only
- **D.** Set max_turns to 1 so that there is no time to edit

??? success "Answer: C"
    **Why C is right:** Restricting the tool set is least privilege, enforced by the SDK.

    **Why the others are wrong:**

    * **A:** A request, not a restriction.
    * **B:** Temperature does not control tool access.
    * **D:** A turn limit does not remove the ability to edit.

---

<p class="qb-meta"><span class="qb-id">AW-013</span><span>Agent SDK</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

When is the Claude Agent SDK a better choice than a hand-written loop on the Messages API?

- **A.** When the application makes one call with no tools
- **B.** When token usage must go unrecorded
- **C.** When no tool should ever run in the application
- **D.** When built-in tools, hooks and sessions are wanted

??? success "Answer: D"
    **Why D is right:** The SDK packages the loop and the surrounding machinery.

    **Why the others are wrong:**

    * **A:** A direct API call is simpler.
    * **B:** Neither approach hides usage.
    * **C:** The SDK's value is largely in tools.

---

<p class="qb-meta"><span class="qb-id">AW-014</span><span>Patterns</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A task requires a draft to be improved against clear quality criteria over several rounds. Which pattern fits?

- **A.** Routing: classify the draft and send it to one handler
- **B.** Parallelisation: produce ten drafts and return them all
- **C.** A single call with a very high max_tokens value
- **D.** Evaluator-optimiser: generate, critique, then revise

??? success "Answer: D"
    **Why D is right:** Iterative refinement against criteria is exactly what this pattern provides.

    **Why the others are wrong:**

    * **A:** Routing selects a path; it does not iterate.
    * **B:** That produces alternatives, not a refined result.
    * **C:** More room does not add a review step.

---

<p class="qb-meta"><span class="qb-id">AW-015</span><span>Stop conditions</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO are appropriate safety limits for an autonomous agent loop? (Select TWO.)

- **A.** A maximum number of iterations
- **B.** A temperature of exactly 1.0 on every call
- **C.** A rule that the agent may never return end_turn
- **D.** A minimum number of tool calls per turn
- **E.** A total token or cost budget for the task

??? success "Answer: A and E"
    **Why A is right:** Bounds how long a loop can run.

    **Why E is right:** Bounds spending across all calls.

    **Why the others are wrong:**

    * **B:** Temperature is not a safety limit.
    * **C:** That would stop it from finishing.
    * **D:** Forcing tool calls encourages needless work.

---

<p class="qb-meta"><span class="qb-id">AW-016</span><span>Agent loop</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about returning tool results are correct? (Select TWO.)

- **A.** Results may be omitted for tools that returned nothing
- **B.** Each tool_result must reference the tool_use_id it answers
- **C.** tool_result blocks are placed in an assistant message
- **D.** A failed tool call should be returned with is_error set to true
- **E.** Results must be summarised by a second model first

??? success "Answer: B and D"
    **Why B is right:** The ID links a result to its request.

    **Why D is right:** The model needs to know that it failed.

    **Why the others are wrong:**

    * **A:** Every tool_use needs a result, even an empty one.
    * **C:** They are sent in a user message.
    * **E:** No such requirement exists.

---
