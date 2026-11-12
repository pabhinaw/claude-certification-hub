# Lab code

Runnable companions to the hub's [Hands-on Labs](https://pabhinaw.github.io/claude-certification-hub/labs/).
All data is **fictional**. Never put real customer data or API keys in these files.

| File | What it shows | Try it without an API key |
|---|---|---|
| `lab01_agent_loop.py` | `stop_reason` loop · prerequisite gate · structured tool errors · guaranteed resolution-or-escalation | `python lab01_agent_loop.py --dry-run` |
| `lab02_extraction.py` | forced `tool_choice` · nullable schema · retry with the specific error · risk-based review routing | `python lab02_extraction.py --dry-run` |
| `lab03-team-config/` | CLAUDE.md · path-scoped rule · team slash command · permissions · PostToolUse formatting hook | copy into a **test** repo, rename `dot-claude` to `.claude`, then open it with Claude Code |

## Running against the real API

```bash
pip install anthropic
export ANTHROPIC_API_KEY="..."        # Windows PowerShell: setx ANTHROPIC_API_KEY "..."
python lab01_agent_loop.py "Hi, I'm CUST-TEST-01, please refund ORD-10001. OTP 123456"
```

Set `CLAUDE_MODEL` to choose a model (check the Models page for current names).

## What the dry runs prove

* **Lab 1:** a refund attempted before verification is blocked by the code gate and the agent recovers; an over-limit refund escalates; a session that stops without resolving is auto-escalated with a handoff package.
* **Lab 2:** a malformed date triggers one retry with the exact validation error; a receipt with an uncertain total is routed to human review.

> **Why `dot-claude`?** The Lab 3 config folder is stored as `dot-claude` so it can never accidentally configure Claude Code inside *this* repository. Rename it to `.claude` only in your own test project.
