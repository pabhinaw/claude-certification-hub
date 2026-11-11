# Hands-on Labs <span class="level-badge">L2–L3</span>

Reading makes ideas familiar; building makes them stick. Each lab takes about 1–2 hours.

| Lab | You build | Domains |
|---|---|---|
| [Lab 1 · Build an Agentic Loop](lab-01-agentic-loop.md) | a support agent with tool gating, structured errors and guaranteed escalation | D1, D2, D5 |
| [Lab 2 · Reliable Structured Extraction](lab-02-structured-extraction.md) | an invoice extractor with forced tool output, nullable schema, retry-with-error and review routing | D4, D5 |
| [Lab 3 · Configure Claude Code for a Team](lab-03-claude-code-config.md) | CLAUDE.md, a path rule, a command, a formatting hook, permissions and a project MCP config | D3, D2 |

## Setup (once)

1. Install Python 3.10 or newer.
2. Get an API key from the Claude Console and set it as an environment variable. **Don't paste it into code.**
    === "Windows (PowerShell)"
        ```powershell
        setx ANTHROPIC_API_KEY "your-key-here"
        # close and reopen the terminal afterwards
        ```
    === "macOS / Linux"
        ```bash
        export ANTHROPIC_API_KEY="your-key-here"
        ```
3. Install the SDK: `pip install anthropic`
4. For Lab 3, install Claude Code following the official instructions.

!!! note "Data used in the labs"
    All customers, orders and invoices in these labs are **fictional test data** (IDs like `CUST-TEST-01`). Never use real personal data in demos.
