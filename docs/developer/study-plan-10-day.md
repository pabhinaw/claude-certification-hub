# 10-Day Study Plan

A day-by-day plan for someone with a full-time job: about **2 hours on weekdays** and **3–4 hours on two heavier days**. Roughly 28 hours in total. The order follows exam weight, so if you lose a day, you lose the least valuable one.

!!! abstract "The method, every day"
    1. **Read** the page actively (20–40 min). Cover the "Check yourself" answers and say them aloud first.
    2. **Build** the small exercise (20–30 min). Typing the code is what makes API details stick.
    3. **Practise** the day's questions (30–40 min). For every question, right or wrong, explain why **each wrong option** is wrong.
    4. **Log misses** (5 min): one line each, "what I believed → what is true".

## The plan at a glance

| Day | Focus | Weight covered | Time |
|---|---|---|---|
| 1 | Orientation + API mechanics I | 33.1% (start) | 2 h |
| 2 | API mechanics II: streaming, errors, limits, batches | 33.1% | 2 h |
| 3 | Application design + engineering foundations | 33.1% (done) | 3 h |
| 4 | Model selection, tokens, caching, cost | 16.8% | 2.5 h |
| 5 | Agents & workflows | 14.7% | 2 h |
| 6 | Prompt & context + Tools & MCP | 21.6% | 3.5 h |
| 7 | Security + Claude Code + evals, then **Mock A** | 13.8% | 4 h |
| 8 | Repair, then **Mock B** | — | 3.5 h |
| 9 | **Mock C** + cheat sheet | — | 3 h |
| 10 | Light review, logistics, rest | — | 1 h |

---

## Day 1 · Orientation and API mechanics I

* **Read:** [Exam Overview](exam-overview.md) (10 min) · [API Mechanics](domains/d1-api-mechanics.md) sections 1–4
* **Build:** make one call and print the *whole* response object. Then build a two-turn conversation by resending history. Then set `max_tokens=20` and look at `stop_reason`.
* **Practise:** [Applications & Integration bank](question-bank/ai.md), questions AI-001 to AI-012
* **You're done when** you can write, from memory: the three required fields, where `system` goes, and what each `stop_reason` means.

??? example "Starter code (use synthetic text only)"
    ```python
    import anthropic
    client = anthropic.Anthropic()          # key from ANTHROPIC_API_KEY
    MODEL = "..."                           # a current model ID

    r = client.messages.create(model=MODEL, max_tokens=20,
        messages=[{"role": "user", "content": "Describe a rainy day in a fictional town."}])
    print(r.stop_reason, r.usage)
    print(r.model_dump_json(indent=2))
    ```

## Day 2 · API mechanics II

* **Read:** [API Mechanics](domains/d1-api-mechanics.md) sections 5–10
* **Build:** stream a response and print each event type. Trigger a 401 (wrong key) and a 400 (leave out `max_tokens`) on purpose and read the error bodies. Call `count_tokens` on a prompt.
* **Practise:** AI-013 to AI-031
* **You're done when** you can recite the error table (status → type → retry or fix) and the streaming event order.

## Day 3 · Application design and engineering foundations

This day covers the two heaviest skills in the blueprint, so give it the extra hour.

* **Read:** [Application Design](domains/d1-application-design.md) · [Engineering Foundations](domains/d1-engineering-foundations.md)
* **Build:** define a small Pydantic schema, ask for structured output, validate it, and add one semantic check. Move the model ID and `max_tokens` into a config file. Then run five calls concurrently with `AsyncAnthropic` behind a semaphore.
* **Write:** take one vague request ("make support faster") and list three functional and three infrastructure requirements for it.
* **Practise:** AI-032 to AI-050 today. Leave AI-051 onwards unread until after Mock A, or use them on Day 8.
* **You're done when**, for any scenario, you can say: which pattern, where state lives, what is validated, what happens on failure, and where each instruction should live on each Claude surface.

## Day 4 · Model selection and optimisation

* **Read:** [Model Selection & Optimisation](domains/d2-model-selection.md). Read the caching section twice.
* **Build:** send the same long system prompt twice with `cache_control` and compare `usage`. Add a timestamp at the top and watch the cache miss. Redo the worked cost example on paper with different numbers.
* **Practise:** the whole [Model Selection bank](question-bank/ms.md)
* **You're done when** you can list five reasons a cache misses and compute a daily cost from token counts.

## Day 5 · Agents and workflows

* **Read:** [Agents & Workflows](domains/d3-agents-workflows.md). If you haven't done the Architect track, add [Architect D1](../architect/domains/d1-agentic-architecture.md).
* **Build:** write the agent loop from memory with one tool, a turn cap and `is_error` handling. Or run [Lab 1](../labs/lab-01-agentic-loop.md) in dry-run mode and read every line.
* **Practise:** the whole [Agents bank](question-bank/aw.md)
* **You're done when** you can write the loop without looking, and explain guidance versus guarantee.

## Day 6 · Prompt & context, tools & MCP (heavier day)

* **Read:** [Prompt & Context](domains/d4-prompt-context.md) · [Tools & MCPs](domains/d5-tools-mcp.md)
* **Build:** the FastMCP bookshop server from the page; open it in the MCP Inspector; then add a `print()` and see what breaks.
* **Practise:** [Prompt & Context bank](question-bank/pc.md) · [Tools & MCP bank](question-bank/tm.md)
* **You're done when** you can name the three structured-output methods with their guarantees, the three MCP primitives with who controls each, and when *not* to build an MCP server.

## Day 7 · Security, the two small domains, and Mock A (heavier day)

* **Read:** [Security & Safety](domains/d6-security-safety.md) · [Claude Code · Evals](domains/d7-claude-code-evals.md)
* **Practise:** [Security bank](question-bank/ss.md) · [Claude Code & Eval bank](question-bank/cc-ev.md)
* **Then:** take **[Mock A](mock-exams.md)**, timed, in one sitting, no notes.
* **Afterwards:** review every miss and every question you guessed correctly. Add them to your miss log.

## Day 8 · Repair, then Mock B

* Sort the miss log by domain. Re-read the matching sections for your **two weakest** domains.
* Rewrite the tables you got wrong, from memory.
* Then take **[Mock B](mock-exams.md)**, timed. Review every miss and every lucky guess.

## Day 9 · Mock C and consolidation

* Take **[Mock C](mock-exams.md)**, timed. This is your final rehearsal: same time of day as your exam if you can.
* Review as before.
* Work through any bank-only questions you haven't seen.
* Read the [Cheat Sheet](cheat-sheet.md) once, slowly, and stop at anything that surprises you.
* If Mock C is below your target, spend the remaining time on that domain's page rather than retaking a mock you now remember.

## Day 10 · Light review and exam

* Cheat sheet once more (30 min). Miss log once more (15 min).
* Read the [Exam Day Guide](exam-day.md) and check your logistics.
* Stop early. Rest does more for your score now than another hour of reading.

---

## Reading your mock results

| First-attempt mock result | What to do |
|---|---|
| 90% or above, and you can explain the wrong options | You are prepared. Keep the miss log fresh |
| 80–89% | Solid. Fix the two weakest domains; expect to pass comfortably |
| 70–79% | Borderline. Give Applications & Integration and Model Selection another full pass |
| Below 70% | Consider moving the exam date. Re-read the deep-dives and redo the builds |

Practice percentages are a guide only. The real exam uses a scaled score and its own questions, so no practice result can promise an exam result.

## Alongside the official courses

The [official prep path](exam-overview.md#official-resources) has five courses, about 13 hours. If you have access, the most valuable use of limited time is to take the courses for the domains you find hardest, and use this hub for revision and practice. A workable split: watch one course on each of Days 1–5 in place of some of the reading here, and keep the builds, questions and mocks as planned.

## If you have less time

| Days left | Keep | Drop |
|---|---|---|
| 7 | Days 1–4, 6, 7, 9 | Merge Day 5 into Day 6 reading; skip Day 8 |
| 5 | API mechanics, application design, model selection, security, one mock | Builds beyond Day 1–2; small domains (cheat sheet only) |
| 3 | Cheat sheet, both parts of Applications & Integration, model selection, one mock | Everything else |

## If you passed the Architect exam first

You can move faster through Days 5 and 6, and Mock A can move earlier: skim the agent, prompt and tool-design sections, and concentrate on what is new (the loop in code, validation and retries, **building** an MCP server, MCP server versus API client). Put the saved time into Days 1–4. The [bridge page](bridge-from-architect.md) has the full map.
