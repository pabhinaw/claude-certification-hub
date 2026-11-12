# Hands-on Labs <span class="level-badge">L2–L3</span>

Reading makes ideas familiar; building makes them stick. Each lab takes about 1–2 hours.

| Lab | You build | Domains |
|---|---|---|
| [Lab 1 · Build an Agentic Loop](lab-01-agentic-loop.md) | a support agent with tool gating, structured errors and guaranteed escalation | D1, D2, D5 |
| [Lab 2 · Reliable Structured Extraction](lab-02-structured-extraction.md) | an invoice extractor with forced tool output, nullable schema, retry-with-error and review routing | D4, D5 |
| [Lab 3 · Configure Claude Code for a Team](lab-03-claude-code-config.md) | CLAUDE.md, a path rule, a command, a formatting hook, permissions and a project MCP config | D3, D2 |
| [Lab 4 · Multi-Agent Research Pipeline](lab-04-multi-agent-research.md) | a coordinator with sub-agents, parallel delegation, provenance, and recovery from failures and conflicting sources | D1, D2, D5 |

The official Architect exam guide recommends four kinds of hands-on practice: a multi-tool agent with escalation, a team Claude Code configuration, a structured extraction pipeline, and a multi-agent research pipeline. Labs 1, 3, 2 and 4 follow those themes in that order.

!!! tip "Runnable code"
    Labs 1–3 have ready-to-run code in the [lab code download](../assets/downloads/labs-code.zip) (a small zip file; unzip it anywhere). Labs 1 and 2 include a **`--dry-run`** mode that works **without an API key**, so you can see the patterns in action first.

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
