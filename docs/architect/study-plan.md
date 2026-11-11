# Study Plans

Pick the plan that matches your experience. Both assume about **1–1.5 hours on weekdays and 3 hours on weekends**.

## Plan A: 6 weeks (newer to Claude)

| Week | Focus | Do |
|---|---|---|
| 1 | Fundamentals (L1) | All [Fundamentals](../fundamentals/index.md) pages; get an API key; run a "hello Claude" script |
| 2 | D1 Agentic (27%) | [D1 page](domains/d1-agentic-architecture.md) + [Lab 1](../labs/lab-01-agentic-loop.md) |
| 3 | D3 Claude Code (20%) | [D3 page](domains/d3-claude-code.md) + [Lab 3](../labs/lab-03-claude-code-config.md) |
| 4 | D4 Prompt & Output (20%) | [D4 page](domains/d4-prompt-structured-output.md) + [Lab 2](../labs/lab-02-structured-extraction.md) |
| 5 | D2 Tools/MCP (18%) + D5 Context (15%) | Both domain pages; connect one MCP server in Claude Code |
| 6 | Exam-ready (L4) | [Scenarios](scenarios.md), [Commonly Missed](commonly-missed.md), [Practice](practice-questions.md) twice, [Cheat Sheet](cheat-sheet.md) |

## Plan B: 3 weeks (already building with Claude)

| Week | Focus |
|---|---|
| 1 | D1 + D2 pages; skim the labs and do only the parts you have never built |
| 2 | D3 + D4 + D5 pages; [Scenarios](scenarios.md) |
| 3 | [Commonly Missed](commonly-missed.md), [Practice](practice-questions.md), review wrong answers, [Cheat Sheet](cheat-sheet.md) |

## Daily routine (about 75 minutes)

1. **10 min**: recall yesterday's decision rules from memory.
2. **40 min**: one domain section, taking notes as *principle → fact*.
3. **15 min**: the *Check yourself* questions for that section.
4. **10 min**: write one scenario-style question of your own about it. Teaching is the strongest test.

## Readiness checklist

- [ ] I score 85% or more on the practice questions, and can explain every wrong option
- [ ] I can draw the agentic loop and name every `stop_reason` branch
- [ ] I can place each Claude Code mechanism (CLAUDE.md, rules, commands, skills, hooks, permissions, MCP) at the right scope
- [ ] I know when to force `tool_choice` and how to enforce tool order
- [ ] I can design an extraction schema that never forces a guess
- [ ] I can design human-review routing that is better than random sampling
