# Claude Code Basics <span class="level-badge">L1</span>

**Claude Code** is Anthropic's agentic coding tool. It runs in your terminal (and in IDEs, desktop and web), reads and edits files, runs commands and uses tools such as Read, Write, Edit, Grep, Glob and Bash.

What the exams test is **configuration**: *where* each kind of guidance lives, and *who* it applies to.

## The configuration map

| Mechanism | Where it lives | What it is for | Enforced? |
|---|---|---|---|
| **CLAUDE.md** (memory) | `~/.claude/CLAUDE.md` (you, all projects) · `./CLAUDE.md` or `./.claude/CLAUDE.md` (team, this repo) · sub-folder `CLAUDE.md` (loaded when Claude works there) | conventions, architecture notes, commands to run | No: guidance the model *should* follow |
| **Rules** | `.claude/rules/*.md`, optionally with `paths:` globs | topic- or path-specific guidance that loads only when relevant | No: guidance |
| **Custom slash commands** | `.claude/commands/` (project) · `~/.claude/commands/` (personal) | reusable prompts you invoke on demand, e.g. `/review-pr` | No: invoked by a person |
| **Skills** | `.claude/skills/<name>/SKILL.md` (project) · `~/.claude/skills/` (personal) | packaged expertise Claude can load when the task matches its description | No: loaded on demand |
| **Subagents** | `.claude/agents/*.md` | specialised helpers with their own context, tools and prompt | Tool limits are enforced |
| **Settings & permissions** | `~/.claude/settings.json` · `.claude/settings.json` · `.claude/settings.local.json` · managed policy | allow / ask / deny rules for tools, env vars, hooks | **Yes** |
| **Hooks** | inside any settings file, under `"hooks"` | scripts that run at lifecycle events (PreToolUse, PostToolUse, Stop…) | **Yes**: deterministic |
| **MCP servers** | `.mcp.json` (project) · `~/.claude.json` (local / user) | connect external tools and data | n/a |

!!! tip "The golden rule"
    **CLAUDE.md is advice. Hooks and permissions are law.** If something must *never* or *always* happen, it does not belong only in CLAUDE.md.

## Settings precedence (highest wins)

1. Enterprise **managed** policy (cannot be overridden)
2. Command-line arguments
3. `.claude/settings.local.json`: personal, this project, git-ignored
4. `.claude/settings.json`: shared with the team, committed
5. `~/.claude/settings.json`: personal, all projects

A permission **deny** rule wins over an allow rule.

## Everyday commands

| Command / key | What it does |
|---|---|
| `claude` | start an interactive session |
| `claude -p "…"` | non-interactive "print" mode, for scripts and CI |
| `--output-format json` | machine-readable output (useful in CI) |
| `claude --continue` / `--resume` | continue the latest session / pick one to resume |
| `/init` | generate a starter CLAUDE.md for the repo |
| `/memory` | open and edit memory files |
| `/compact` | summarise the conversation to free context |
| `/clear` | start fresh in the same session |
| ++shift+tab++ | cycle permission modes, including **plan mode** |

## Plan mode in one sentence

Plan mode lets Claude **investigate and propose a plan without editing anything**. Use it for large, multi-file, architectural or hard-to-reverse changes, or whenever stakeholders should review first. Skip it for small, well-scoped edits.

Next: [MCP Basics](mcp-basics.md) · Deep dive: [D3 · Claude Code Configuration & Workflows](../architect/domains/d3-claude-code.md)
