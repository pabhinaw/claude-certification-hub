# Lab 3 · Configure Claude Code for a Team <span class="level-badge">L2</span>

**Goal:** take a small repo and give it a team-ready Claude Code setup, putting each piece of guidance in the **right mechanism at the right scope**.

!!! tip "Starter files"
    A ready-made copy of every file below is in [`labs-code/lab03-team-config/`](https://github.com/pabhinaw/claude-certification-hub/tree/main/labs-code/lab03-team-config). Copy it into a **test** repository and rename its `dot-claude` folder to `.claude`.

## Target structure

```text
my-team-repo/
├── CLAUDE.md                          ← team conventions (advice)
├── .mcp.json                          ← shared MCP servers (secrets via ${VAR})
└── .claude/
    ├── settings.json                  ← permissions + hooks (enforcement), committed
    ├── settings.local.json            ← your personal overrides, git-ignored
    ├── rules/
    │   └── api.md                     ← only for src/api/**
    ├── commands/
    │   └── review-pr.md               ← /review-pr for everyone
    └── hooks/
        └── format.sh                  ← run after every edit
```

## Step 1: CLAUDE.md (advice)

Run `/init` in the repo to generate a starter file, then trim it to something like:

```markdown
# Project: Example Notes API
- Stack: Node 20, TypeScript, Express, Vitest. Package manager: pnpm.
- Run tests: `pnpm test` · Lint: `pnpm lint`
- Prefer small pure functions; avoid classes unless state is needed.
- Architecture overview: @docs/architecture.md
```

Keep it short: it loads every session.

## Step 2: A path-specific rule

`.claude/rules/api.md`:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
- Validate every request body with zod before using it.
- Return errors as { code, message }; never leak stack traces.
```

## Step 3: A team command

`.claude/commands/review-pr.md`:

```markdown
---
description: Review current branch against team checklist
argument-hint: [focus]
---
Review `git diff main...HEAD`. Focus: $ARGUMENTS.
Checklist: tests added/updated · no secrets · input validation · error handling · naming.
Return a table: file | issue | severity | suggested fix.
```

Try it: `/review-pr security`.

## Step 4: Enforcement: permissions + a formatting hook

`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(pnpm test:*)", "Bash(pnpm lint:*)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)", "Edit(./migrations/**)", "Bash(git push --force:*)"]
  },
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh" } ] }
    ]
  }
}
```

`.claude/hooks/format.sh` (make it executable with `chmod +x`):

```bash
#!/usr/bin/env bash
file=$(jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0
npx prettier --write "$file" >/dev/null 2>&1 || { echo "Prettier failed on $file" >&2; exit 2; }
```

!!! info "Windows users"
    Hooks run through a shell. On Windows, use Git Bash/WSL, or write the hook in a cross-platform language (for example a small Node or Python script).

## Step 5: A shared MCP server

```bash
claude mcp add --scope project --transport http docs https://example.invalid/mcp
```

Then edit `.mcp.json` so any secret uses `${DOCS_TOKEN}`, and check discovery with `/mcp`.

## Step 6: Verify each mechanism

- [ ] Ask Claude to read `.env` → **denied**
- [ ] Ask it to edit a file → the hook formats it automatically
- [ ] Edit something in `src/api/` → the API rule is applied
- [ ] `/review-pr` is available after a teammate clones the repo
- [ ] Ask for a 20-file refactor → toggle **plan mode** (++shift+tab++) and review the plan first

## Reflection

For each line you were tempted to put in CLAUDE.md, ask: *"Is this a should, or a must?"* Every **must** you found should now live in `settings.json`.
