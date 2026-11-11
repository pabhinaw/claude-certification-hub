# Agent SDK Basics <span class="level-badge">L1–L2</span>

The **Claude Agent SDK** (Python and TypeScript) gives you the same agent loop, built-in tools and context management that power Claude Code, as a library you can program.

## Client SDK vs Agent SDK

| | Anthropic **Client** SDK (Messages API) | Claude **Agent** SDK |
|---|---|---|
| Who runs the tool loop? | **you** write the loop (`stop_reason == "tool_use"` → run tool → send result) | the **SDK** runs it for you |
| Built-in tools | none: you define every tool | Read, Write, Edit, Bash, Grep, Glob, WebSearch and more |
| Extras | — | subagents, hooks, sessions, permissions, MCP, Claude Code settings |
| Best for | precise control, simple integrations | autonomous agents that work with files, code and tools |

Understanding the manual loop ([Lab 1](../labs/lab-01-agentic-loop.md)) makes the Agent SDK much easier to reason about.

## A first agent (Python)

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="List the TODO comments in this project and group them by file.",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"]),  # read-only
    ):
        print(message)

anyio.run(main)
```

* `query()`: one task, streams messages back.
* `ClaudeSDKClient`: a longer, multi-turn conversation that keeps its session.

## Key options (`ClaudeAgentOptions`)

| Option | What it does | Architect relevance |
|---|---|---|
| `allowed_tools` / `disallowed_tools` | which tools the agent may use (disallow wins) | **least privilege**; fewer tools = better selection |
| `system_prompt` | role and instructions | keep stable for caching |
| `permission_mode` | e.g. default, `acceptEdits`, `plan` | plan mode = investigate without editing |
| `agents` | named **subagents** (`AgentDefinition`: description, prompt, tools, model) | specialised, isolated contexts |
| `hooks` | Python callbacks on events such as `PreToolUse` / `PostToolUse` | **deterministic** policy enforcement |
| `mcp_servers` | connect MCP servers | external tools and data |
| `setting_sources` | load filesystem settings such as `["project"]` (CLAUDE.md, skills, commands) | without it, project settings aren't loaded |
| `resume` / `fork_session` | continue or branch a previous session | session-state questions |

## Subagents

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Agent"],   # the subagent tool (named "Task" in older versions)
    agents={
        "security-reviewer": AgentDefinition(
            description="Reviews code for security issues. Use for any auth or input-handling change.",
            prompt="You are a security reviewer. Report findings as a table with severity.",
            tools=["Read", "Grep"],                       # least privilege
            model="sonnet",
        )
    },
)
```

Remember:

* The subagent's **description** decides when the main agent delegates to it, just like a tool description.
* A subagent has its **own context**. It doesn't see the parent's conversation, so the delegation message must carry what it needs.
* The parent must be allowed to use the **subagent tool**, or it can't delegate.

## Hooks in the SDK

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def block_env_reads(input_data, tool_use_id, context):
    path = input_data.get("tool_input", {}).get("file_path", "")
    if ".env" in path:
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Secrets files are off-limits."}}
    return {}

options = ClaudeAgentOptions(hooks={"PreToolUse": [HookMatcher(matcher="Read", hooks=[block_env_reads])]})
```

## Check yourself

??? question "You added a skill to `.claude/skills/` but your SDK agent never uses it. Likely cause?"
    Filesystem settings aren't loaded. Set `setting_sources=["project"]` (or include `"user"`), and make sure the Skill tool is allowed.

??? question "The main agent never delegates to your `security-reviewer` subagent. First two things to check?"
    1) The parent's `allowed_tools` includes the subagent tool; 2) the subagent's **description** clearly says when to use it.

**Verify in official docs:** [Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)
