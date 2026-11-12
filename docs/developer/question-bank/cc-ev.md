# Question Bank · Claude Code · Eval, Testing & Debugging

**19 original questions** (0 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Configuration · Custom commands · Debugging · Error types · Evals · Graders · Headless mode · Parallel work · Permission modes · Permissions · Repository setup · Rules · Sessions

---

<p class="qb-meta"><span class="qb-id">CC-001</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team wants every developer's Claude Code sessions in a repository to know the build command and coding conventions automatically. Where should this go?

- **A.** In a message pasted at the start of every session
- **B.** In each developer's personal user-level settings
- **C.** In the project's CLAUDE.md, committed to the repository
- **D.** In the name of the main git branch

??? success "Answer: C"
    **Why C is right:** Project memory is loaded each session and shared through version control.

    **Why the others are wrong:**

    * **A:** Manual and easily forgotten.
    * **B:** Not shared; it would drift between people.
    * **D:** Not a configuration mechanism.

---

<p class="qb-meta"><span class="qb-id">CC-002</span><span>Rules</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Test files under tests/ need different conventions from the rest of the codebase. Which Claude Code mechanism applies instructions only when those files are involved?

- **A.** A higher permission level for the tests folder
- **B.** A hook that deletes files outside the tests folder
- **C.** A rule file scoped to the tests/ path
- **D.** A larger CLAUDE.md with the test rules at the top

??? success "Answer: C"
    **Why C is right:** Path-scoped rules load only for matching files, keeping other work uncluttered.

    **Why the others are wrong:**

    * **A:** Permissions control actions, not conventions.
    * **B:** Destructive and unrelated.
    * **D:** Loaded every time, relevant or not.

---

<p class="qb-meta"><span class="qb-id">CC-003</span><span>Sessions</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

How is Claude Code run non-interactively, for example inside a CI job?

- **A.** By setting the temperature to zero in CLAUDE.md
- **B.** By renaming the project folder to "ci"
- **C.** By starting it and piping keystrokes into the window
- **D.** With the -p flag and a prompt, optionally with JSON output

??? success "Answer: D"
    **Why D is right:** Print mode runs a single prompt without an interactive session.

    **Why the others are wrong:**

    * **A:** Not how non-interactive mode is selected.
    * **B:** Folder names do not change the mode.
    * **C:** Fragile and unnecessary.

---

<p class="qb-meta"><span class="qb-id">CC-004</span><span>Permissions</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In Claude Code settings, a command matches both an allow rule and a deny rule. What happens?

- **A.** Both rules are ignored and the defaults are used
- **B.** The command is allowed, because allow is checked first
- **C.** The command is denied, because deny takes precedence
- **D.** The user is asked to choose which rule applies

??? success "Answer: C"
    **Why C is right:** Deny rules win, which makes them suitable for hard limits.

    **Why the others are wrong:**

    * **A:** Rules are not discarded on conflict.
    * **B:** Deny takes precedence over allow.
    * **D:** The conflict is resolved by precedence.

---

<p class="qb-meta"><span class="qb-id">CC-005</span><span>Repository setup</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer opens Claude Code in an existing repository for the first time. Which command creates a starter CLAUDE.md from the codebase?

- **A.** /compact
- **B.** /clear
- **C.** /mcp
- **D.** /init

??? success "Answer: D"
    **Why D is right:** /init analyses the project and drafts a CLAUDE.md, which should then be reviewed and trimmed.

    **Why the others are wrong:**

    * **A:** Summarises the conversation to save context.
    * **B:** Clears the conversation.
    * **C:** Manages MCP server connections.

---

<p class="qb-meta"><span class="qb-id">CC-006</span><span>Permission modes</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer wants Claude Code to investigate a bug and propose an approach without changing any files yet. Which mode fits?

- **A.** Fast mode
- **B.** Accept edits mode
- **C.** Bypass permissions mode
- **D.** Plan mode

??? success "Answer: D"
    **Why D is right:** Plan mode allows reading and planning, with no edits until the plan is approved.

    **Why the others are wrong:**

    * **A:** A speed setting, not a permission mode.
    * **B:** Applies file edits without asking.
    * **C:** Removes prompts and allows changes.

---

<p class="qb-meta"><span class="qb-id">CC-007</span><span>Headless mode</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A CI job runs Claude Code non-interactively and another program needs to process events as they happen. Which output setting fits?

- **A.** Plain text printed after the run has ended
- **B.** A screenshot of the final terminal window
- **C.** The default interactive terminal display
- **D.** The stream-json output format

??? success "Answer: D"
    **Why D is right:** Streaming JSON emits events as they occur for another process to consume.

    **Why the others are wrong:**

    * **A:** Arrives only at the end and is unstructured.
    * **B:** Not structured output.
    * **C:** Not machine-readable and needs a terminal.

---

<p class="qb-meta"><span class="qb-id">CC-008</span><span>Custom commands</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team repeatedly types the same long review prompt in Claude Code. What is the lightest way to make it reusable by name?

- **A.** A custom slash command in .claude/commands/
- **B.** A deny rule in the project's settings
- **C.** A PreToolUse hook that blocks commits
- **D.** A new MCP server with one review tool

??? success "Answer: A"
    **Why A is right:** A Markdown file there becomes a /command shared through the repository.

    **Why the others are wrong:**

    * **B:** Permissions do not store prompts.
    * **C:** Hooks enforce; they do not store prompts.
    * **D:** Far heavier than needed for a prompt.

---

<p class="qb-meta"><span class="qb-id">CC-009</span><span>Parallel work</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In Claude Code, what distinguishes a sub-agent from a parallel session?

- **A.** A sub-agent is a scoped helper inside one session
- **B.** A sub-agent shares the parent's whole context
- **C.** A sub-agent always runs on a different machine
- **D.** A sub-agent can only be used for writing tests

??? success "Answer: A"
    **Why A is right:** Sub-agents have their own context and tool limits and report to the parent; parallel sessions are separate instances.

    **Why the others are wrong:**

    * **B:** It has its own context window.
    * **C:** Location is not the distinction.
    * **D:** Sub-agents can be defined for many jobs.

---

<p class="qb-meta"><span class="qb-id">EV-001</span><span>Evals</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team changes the wording of a production prompt. What should happen before the change is released?

- **A.** Test only the one example that motivated the change
- **B.** Run the eval set and compare with the old version
- **C.** Release it and wait for customer complaints to arrive
- **D.** Ask two colleagues whether the wording reads better

??? success "Answer: B"
    **Why B is right:** Regression testing catches behaviour that the change broke.

    **Why the others are wrong:**

    * **A:** Misses regressions elsewhere.
    * **C:** Users become the test suite.
    * **D:** Opinion about wording is not a behaviour test.

---

<p class="qb-meta"><span class="qb-id">EV-002</span><span>Graders</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An eval must judge whether support replies are empathetic and accurate, across thousands of cases. Which grading approach is most practical?

- **A.** Exact string comparison with a reference reply
- **B.** A check that each reply exceeds fifty words
- **C.** A rubric-driven LLM grader, spot-checked
- **D.** Manual review of every case by one engineer

??? success "Answer: C"
    **Why C is right:** Nuanced quality at scale suits a model grader, calibrated against human judgement.

    **Why the others are wrong:**

    * **A:** Good replies vary in wording.
    * **B:** Length does not measure empathy or accuracy.
    * **D:** Does not scale to thousands of cases.

---

<p class="qb-meta"><span class="qb-id">EV-003</span><span>Debugging</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent gives a wrong answer. The logs show that a tool returned an HTML error page where JSON was expected, and the page was passed straight to the model. What is the right fix?

- **A.** Increase max_tokens so that the page fits better
- **B.** Rewrite the system prompt to be more persuasive
- **C.** Switch to a larger model that can interpret HTML
- **D.** Validate tool output; return a structured error if bad

??? success "Answer: D"
    **Why D is right:** Malformed tool responses should be caught before they reach the model.

    **Why the others are wrong:**

    * **A:** More room for bad data does not help.
    * **B:** The fault is in the data, not the prompt.
    * **C:** The page contains no answer to interpret.

---

<p class="qb-meta"><span class="qb-id">EV-004</span><span>Debugging</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A multi-step agent fails intermittently in production and nobody can explain why. What should be added first?

- **A.** Tracing of each call, tool input, result and usage
- **B.** A higher temperature to see more varied failures
- **C.** A second agent that guesses what the first one did
- **D.** A longer system prompt asking it to avoid failing

??? success "Answer: A"
    **Why A is right:** You cannot debug what you cannot see. Traces make the sequence reproducible.

    **Why the others are wrong:**

    * **B:** Adds noise.
    * **C:** Speculation is not observability.
    * **D:** Does not reveal the cause.

---

<p class="qb-meta"><span class="qb-id">EV-005</span><span>Debugging</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent gives a wrong answer. The trace shows the correct tool was called and returned the right data, and the full history was sent. Where is the problem most likely?

- **A.** In the HTTP layer, so add more retry attempts
- **B.** In the model's output, so improve the prompt
- **C.** In the API key, so rotate it and then try again
- **D.** In the tool code, so rewrite the tool's schema

??? success "Answer: B"
    **Why B is right:** With correct inputs and working tools, the remaining variable is the model's response.

    **Why the others are wrong:**

    * **A:** The calls succeeded; there is nothing to retry.
    * **C:** Authentication succeeded.
    * **D:** The tool returned the right data.

---

<p class="qb-meta"><span class="qb-id">EV-006</span><span>Debugging</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A failure happens identically on every run with the same input. Another varies from run to run. Which is more likely an integration bug rather than model variability?

- **A.** The one that varies from one run to the next
- **B.** Both equally, since all failures are random
- **C.** The one that happens identically every time
- **D.** Neither, since integration bugs cannot be found

??? success "Answer: C"
    **Why C is right:** Deterministic failures usually come from code or configuration; varying ones often from model non-determinism.

    **Why the others are wrong:**

    * **A:** Variation points to model behaviour.
    * **B:** Not all failures are random.
    * **D:** They can be found from traces.

---

<p class="qb-meta"><span class="qb-id">EV-007</span><span>Graders</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team builds an LLM-based grader. What should be done before relying on its scores?

- **A.** Let it grade its own grading for consistency
- **B.** Raise its temperature for more varied scores
- **C.** Use it only on cases that are known to pass
- **D.** Calibrate it against cases that people have labelled

??? success "Answer: D"
    **Why D is right:** Agreement with human labels shows whether the grader measures what you intend.

    **Why the others are wrong:**

    * **A:** Self-assessment is not calibration.
    * **B:** Variation makes a grader less reliable.
    * **C:** That would hide failures.

---

<p class="qb-meta"><span class="qb-id">EV-008</span><span>Error types</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A request fails with a 400 because a tool_result was sent without its matching tool_use. How should this be classified and handled?

- **A.** A terminal client error: fix the message construction
- **B.** A rate-limit error: wait for the retry-after time
- **C.** A model refusal: rephrase the user's question
- **D.** A transient server error: retry it with backoff

??? success "Answer: A"
    **Why A is right:** The request is invalid and will fail every time. Code must be corrected; retrying is pointless.

    **Why the others are wrong:**

    * **B:** That would be a 429.
    * **C:** A refusal is a successful response, not a 400.
    * **D:** A 400 is not transient.

---

<p class="qb-meta"><span class="qb-id">EV-009</span><span>Evals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team edits a skill that steers its coding agent. What is the most reliable way to check that the agent still performs as before?

- **A.** Run the eval suite in CI whenever that configuration changes
- **B.** Compare the length of the old and new skill
- **C.** Try one prompt by hand and see if it looks fine
- **D.** Wait for developers to report worse results

??? success "Answer: A"
    **Why A is right:** Configuration that steers the agent deserves the same regression testing as code.

    **Why the others are wrong:**

    * **B:** Length says nothing about behaviour.
    * **C:** One manual check misses regressions elsewhere.
    * **D:** Users become the test suite.

---

<p class="qb-meta"><span class="qb-id">EV-010</span><span>Evals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What is the difference between giving an agent a feedback loop and adding a verifier sub-agent?

- **A.** The loop replaces tests; the verifier replaces review
- **B.** The loop runs during the task; the verifier checks at the end in a fresh context
- **C.** They are two names for exactly the same mechanism
- **D.** The loop is run by people; the verifier by the model

??? success "Answer: B"
    **Why B is right:** A feedback loop lets the agent correct itself repeatedly; a fresh-context verifier gives an independent final check.

    **Why the others are wrong:**

    * **A:** Neither replaces tests or human review.
    * **C:** They serve different purposes at different times.
    * **D:** Both are automated.

---
