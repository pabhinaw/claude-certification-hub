# Agents & Workflows <span class="level-badge">14.7%</span>

If you studied the Architect track, most of this is familiar: read [Architect D1](../../architect/domains/d1-agentic-architecture.md) for the design reasoning. This page adds the **implementation** view the Developer exam prefers: the loop in code, stop conditions, and the Agent SDK.

## What this domain covers

* Workflows versus agents, and the standard patterns
* The tool-use loop in code
* Stop conditions and runaway-loop protection
* Human approval gates
* Sub-agents
* The Claude Agent SDK
* Supervisor hierarchies, memory, self-hosted versus managed agents, third-party frameworks

---

## 1. Workflow or agent?

| | Workflow | Agent |
|---|---|---|
| Who decides the next step | **Your code** | **The model** |
| Predictability | High | Lower |
| Cost / latency | Lower | Higher |
| Best when | Steps are known | Steps can't be known in advance |

**Five workflow patterns**

| Pattern | Shape | Use for |
|---|---|---|
| Prompt chaining | A → B → C, with checks between | Fixed multi-step transformations |
| Routing | Classify, then send to a specialist prompt | Mixed input types |
| Parallelisation | Fan out, then combine | Independent sub-tasks, or voting |
| Orchestrator–workers | A lead model splits the task and delegates | Sub-tasks unknown until run time |
| Evaluator–optimiser | Generate → critique → revise | Clear quality criteria, iterative gains |

## 2. The agent loop

An agent is a loop around the Messages API. Learn this code until you can write it from memory.

```python
MAX_TURNS = 15
messages = [{"role": "user", "content": task}]

for turn in range(MAX_TURNS):
    resp = client.messages.create(
        model=MODEL, max_tokens=2048, system=SYSTEM, tools=TOOLS, messages=messages,
    )
    messages.append({"role": "assistant", "content": resp.content})   # all blocks

    if resp.stop_reason != "tool_use":
        break                                   # end_turn, max_tokens, refusal ...

    results = []
    for block in resp.content:
        if block.type == "tool_use":
            try:
                out = run_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
            except ToolError as e:
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": str(e), "is_error": True})
    messages.append({"role": "user", "content": results})   # ALL results, one message
else:
    escalate("turn limit reached")              # loop ended without finishing
```

The rules inside it:

1. **Loop on `stop_reason == "tool_use"`**, not on parsing the text for phrases like "done".
2. Append the **whole** assistant content, then one `user` message carrying a `tool_result` for **every** `tool_use` block.
3. Match each result by **`tool_use_id`**.
4. Tool failures go back as `is_error: true` so the model can adapt. Don't crash the loop and don't hide the error.
5. A **turn cap** is a safety net, not the normal exit.

## 3. Stop conditions

| Condition | Type |
|---|---|
| `stop_reason == "end_turn"` | Normal completion |
| Turn / iteration cap | Safety net |
| Token or cost budget for the task | Safety net |
| Wall-clock timeout | Safety net |
| No-progress detection (same tool, same input, repeatedly) | Safety net |
| Human says stop, or approval denied | Control |

**Runaway loops.** Typical causes: a tool keeps failing with an unhelpful error; the goal has no clear finish; two steps undo each other. Defences: informative tool errors (say whether to retry), explicit completion criteria in the prompt, caps, repeated-call detection, and escalation to a person when a cap is hit. Hitting a cap should produce a **clear hand-off**, not silence.

## 4. Human approval gates

Put a person in front of actions that are **irreversible, expensive or sensitive**: payments, deletions, sending external messages, production changes.

```python
if block.name in REQUIRES_APPROVAL:
    if not ask_human(block.name, block.input):
        results.append({"type": "tool_result", "tool_use_id": block.id,
                        "content": "Denied by reviewer. Do not retry; suggest alternatives.",
                        "is_error": True})
        continue
```

* The gate lives in **code** (or a hook), never only in the prompt. A prompt asks; code enforces.
* Gate by **risk**, not on everything. Approving every read teaches people to click "yes" without looking.
* Show the reviewer the exact action and arguments.

## 5. Sub-agents

A sub-agent runs in its **own context window** with its own instructions and tools, and returns a result to the caller.

Why use them:

* **Context isolation**: noisy exploration stays out of the main context; only a summary comes back
* **Specialisation**: narrow instructions and a small tool set per role
* **Parallelism**: independent sub-tasks run at the same time

What to remember:

* A sub-agent **does not inherit** the parent's conversation. Pass everything it needs in the task description.
* Ask for a **structured, concise result** (findings, sources, confidence), not a transcript.
* Sub-agents multiply token use. For a simple sequential task a single agent is better.
* Sub-agents usually cannot spawn their own sub-agents; coordination stays with the lead.
* Cheaper tiers often suit sub-agents doing simple work.

## 6. The Claude Agent SDK

The Agent SDK packages the loop, built-in tools (file read/edit, shell, search), context management, permissions, hooks, sub-agents and sessions, so you don't rewrite them.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a careful code reviewer.",
        allowed_tools=["Read", "Grep", "Glob"],     # least privilege: read-only
        permission_mode="default",
        max_turns=20,
    )
    async for message in query(prompt="Review src/ for unhandled errors.", options=options):
        print(message)

asyncio.run(main())
```

| Option | Purpose |
|---|---|
| `allowed_tools` / `disallowed_tools` | Which tools the agent may use |
| `permission_mode` | How tool permissions are handled (ask, auto-accept edits, and so on) |
| `max_turns` | Turn cap |
| `hooks` | Code that runs at lifecycle points (for example `PreToolUse`) and can block an action |
| `agents` | Sub-agent definitions (description, prompt, tools, model) |
| `mcp_servers` | MCP servers to connect |
| `setting_sources` | Whether to load project/user settings such as `CLAUDE.md` |
| `resume` | Continue a previous session by ID |

`query()` suits one-off tasks; `ClaudeSDKClient` suits multi-turn, interactive sessions.

**Raw API loop or Agent SDK?**

| Choose the **raw Messages API loop** | Choose the **Agent SDK** |
|---|---|
| A few custom tools, simple control flow | You need file, shell or search tools out of the box |
| You want full control of every request | You want built-in context management, hooks, permissions, sessions |
| Minimal dependencies | Sub-agents and MCP with little code |

## 7. Hierarchies, memory, hosting and frameworks

### Supervisor hierarchies

A **supervisor** (manager, orchestrator, lead) agent plans, delegates to workers and combines their results.

| Benefit | Cost |
|---|---|
| Each worker has a clean, focused context | Many times the tokens of a single agent |
| Parallel work on separable sub-tasks | Coordination errors; information lost in hand-offs |
| Specialised prompts and tool sets | Harder to trace and debug |

Use a hierarchy when the work is broad and separable. Keep a single agent when the task is sequential or the steps depend closely on each other. Keep hierarchies shallow, and make hand-offs explicit (goal, inputs, expected output format).

### Agent memory

| Kind | Lives in | Lasts |
|---|---|---|
| Working memory | The context window | This session |
| Persistent memory | Files or a store outside the window (notes, a memory tool, a database) | Across sessions |

* Store **decisions, facts and progress**, not transcripts.
* Scope memory deliberately (per user, per project, per agent). A shared memory can leak one user's data to another.
* Load only what is relevant; loading everything defeats the purpose.
* Treat stored memory as **data**: it may be stale or contain injected text.

### Self-hosted or Anthropic-hosted

| | Self-hosted (your loop or the Agent SDK) | Anthropic-hosted managed agents |
|---|---|---|
| Who runs the loop | Your process, on your infrastructure | The platform |
| You manage | Compute, sandboxing, session state, scaling | The agent definition and the environment configuration |
| Good for | Full control, access to local files and private networks, custom harness logic, strict data requirements | Long-running or asynchronous tasks without building runtime infrastructure |
| Watch for | Operational effort | Sessions are stateful and stored by the service; beta features and data-retention eligibility |

The managed service is organised around an **agent** (model, system prompt, tools, MCP servers, skills), an **environment** (where sessions run: a cloud sandbox, or a sandbox you host) and **sessions** (running instances whose state is kept server-side). Check the docs for current status and limits.

### Third-party agent frameworks

| Framework | Idea | Fits when |
|---|---|---|
| **LangGraph** | The agent as a **graph**: nodes, edges, explicit shared state, checkpoints | You want explicit control flow, durable state and human-in-the-loop pauses |
| **PydanticAI** | **Type-safe** agents with validated inputs and outputs | Typed Python code and structured, validated results matter most |
| **Strands Agents** | **Model-driven**: give a model, tools and a prompt, and the model plans | You want a light, open-source SDK with little orchestration code |

When to use any framework: it can save time on plumbing, but it adds an abstraction that can hide the actual prompts and requests, which makes debugging harder. A sound default is to **start with direct API calls or the Agent SDK, and adopt a framework when it removes real work**. Whatever you choose, make sure you can see the underlying prompts and responses.

## 8. Guidance versus guarantee

The idea that carries across both exams:

| Need | Mechanism |
|---|---|
| Should usually happen | Prompt instruction |
| Must **always** / **never** happen | Code: a hook, a gate, `tool_choice`, permissions, validation |

If a question says "must", "always", "never" or "guarantee", the answer is rarely "strengthen the prompt".

---

## Traps

| Tempting answer | Why it's wrong |
|---|---|
| Stop when the reply contains "task complete" | Fragile; use `stop_reason` |
| Use the turn cap as the normal way to finish | It is a safety net; hitting it is a failure to handle |
| Return an empty result when a tool fails | Hides the failure; return `is_error` with detail |
| Assume the sub-agent knows the earlier conversation | Isolated context; pass it explicitly |
| Add "ask before refunds" to the system prompt for a hard rule | Enforce with a code gate or hook |
| One agent with 40 tools | Selection degrades; split by role or trim |

## Check yourself

??? question "An agent keeps calling `get_weather` with the same city 30 times. Two fixes?"
    Make the tool error informative (say why it failed and whether a retry can help), and add loop protection: repeated-call detection plus a turn cap that escalates.

??? question "What decides whether your loop continues after a response?"
    `stop_reason`. Continue only on `tool_use`; anything else ends the loop or needs handling.

??? question "Claude returned three `tool_use` blocks. How do you reply?"
    One `user` message containing three `tool_result` blocks, each with the matching `tool_use_id`.

??? question "A research sub-agent returns generic results because it 'didn't know the product name'. Cause?"
    The parent never passed it. Sub-agents start with a fresh context; include all needed details in the task.

??? question "Refunds above a limit must never be issued without a manager. Where is that enforced?"
    In code: an approval gate or a pre-tool hook that blocks the call. Not by prompt wording alone.

---

!!! abstract "Verify in official docs"
    * [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
    * [Tool use: implementation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
    * [Stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
    * Agent SDK basics on this site: [Fundamentals → Agent SDK](../../fundamentals/agent-sdk-basics.md)
