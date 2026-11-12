# Question Bank · Claude Code · Eval, Testing & Debugging

**8 original questions** (0 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Configuration · Debugging · Evals · Graders · Permissions · Rules · Sessions

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
- **C.** The user is asked to choose which rule applies
- **D.** The command is denied, because deny takes precedence

??? success "Answer: D"
    **Why D is right:** Deny rules win, which makes them suitable for hard limits.

    **Why the others are wrong:**

    * **A:** Rules are not discarded on conflict.
    * **B:** Deny takes precedence over allow.
    * **C:** The conflict is resolved by precedence.

---

<p class="qb-meta"><span class="qb-id">EV-001</span><span>Evals</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team changes the wording of a production prompt. What should happen before the change is released?

- **A.** Run the eval set and compare with the old version
- **B.** Test only the one example that motivated the change
- **C.** Release it and wait for customer complaints to arrive
- **D.** Ask two colleagues whether the wording reads better

??? success "Answer: A"
    **Why A is right:** Regression testing catches behaviour that the change broke.

    **Why the others are wrong:**

    * **B:** Misses regressions elsewhere.
    * **C:** Users become the test suite.
    * **D:** Opinion about wording is not a behaviour test.

---

<p class="qb-meta"><span class="qb-id">EV-002</span><span>Graders</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An eval must judge whether support replies are empathetic and accurate, across thousands of cases. Which grading approach is most practical?

- **A.** A rubric-driven LLM grader, spot-checked
- **B.** Exact string comparison with a reference reply
- **C.** A check that each reply exceeds fifty words
- **D.** Manual review of every case by one engineer

??? success "Answer: A"
    **Why A is right:** Nuanced quality at scale suits a model grader, calibrated against human judgement.

    **Why the others are wrong:**

    * **B:** Good replies vary in wording.
    * **C:** Length does not measure empathy or accuracy.
    * **D:** Does not scale to thousands of cases.

---

<p class="qb-meta"><span class="qb-id">EV-003</span><span>Debugging</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent gives a wrong answer. The logs show that a tool returned an HTML error page where JSON was expected, and the page was passed straight to the model. What is the right fix?

- **A.** Increase max_tokens so that the page fits better
- **B.** Validate tool output; return a structured error if bad
- **C.** Rewrite the system prompt to be more persuasive
- **D.** Switch to a larger model that can interpret HTML

??? success "Answer: B"
    **Why B is right:** Malformed tool responses should be caught before they reach the model.

    **Why the others are wrong:**

    * **A:** More room for bad data does not help.
    * **C:** The fault is in the data, not the prompt.
    * **D:** The page contains no answer to interpret.

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
