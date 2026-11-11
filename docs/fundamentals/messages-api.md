# The Messages API <span class="level-badge">L1</span>

The **Messages API** is the main way applications talk to Claude.

## Anatomy of a request

```python
import anthropic

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY from your environment

response = client.messages.create(
    model="claude-sonnet-5-5",          # check the Models page for current names
    max_tokens=1024,                    # upper limit on the reply length
    system="You are a concise support assistant for a fictional bookstore.",
    messages=[
        {"role": "user", "content": "Do you ship to Pune?"},
    ],
)
print(response.content[0].text)
print(response.stop_reason)             # e.g. "end_turn"
```

| Field | Meaning |
|---|---|
| `model` | which Claude model to use |
| `max_tokens` | hard cap on output length |
| `system` | instructions and persona; not part of the `messages` list |
| `messages` | the conversation so far, alternating `user` / `assistant` |
| `tools` | optional tool definitions (see [Tool Use Basics](tool-use-basics.md)) |

!!! danger "Never hard-code API keys"
    Keep keys in environment variables or a secrets manager. Never commit them to Git.

## The API is stateless: you own the conversation

Every request must contain **the whole conversation you want Claude to consider**. To continue a chat, append Claude's reply and the user's next message, then send the full list again:

```python
history = [{"role": "user", "content": "Do you ship to Pune?"}]
r1 = client.messages.create(model=MODEL, max_tokens=512, messages=history)

history.append({"role": "assistant", "content": r1.content})   # keep Claude's turn
history.append({"role": "user", "content": "How long does it take?"})
r2 = client.messages.create(model=MODEL, max_tokens=512, messages=history)
```

This is an exam favourite: **"How do you maintain state across turns?"** → by including the prior messages in every request. The server does not remember anything for you.

## Reading the response: `stop_reason`

`stop_reason` tells your code **why Claude stopped**. Your program should branch on it, never on the wording of Claude's text.

| `stop_reason` | Meaning | What your code does |
|---|---|---|
| `end_turn` | Claude finished its answer | show the answer / finish |
| `tool_use` | Claude wants you to run a tool | run it, send back a `tool_result`, call again |
| `max_tokens` | hit your `max_tokens` cap | answer is truncated: raise the limit or continue |
| `stop_sequence` | hit one of your custom stop sequences | handle as designed |
| `pause_turn` | a long server-side tool turn was paused | send the response back to let it continue |
| `refusal` | Claude declined for safety reasons | handle gracefully; do not blindly retry |

## Synchronous vs batch

| | Messages API | Message Batches API |
|---|---|---|
| Latency | seconds | asynchronous, up to 24 h (often much faster) |
| Cost | standard | about **50% cheaper** |
| Use when | a user or workflow is **waiting** for the answer | nothing is blocked: overnight reports, bulk back-fills, evaluations |
| Correlating results | n/a | each request carries your own `custom_id` |

Rule: **if a person or a blocking pipeline step is waiting, use synchronous**. If the work can wait and volume is high, use batches.

## Prompt caching (preview)

If many requests share a long, identical prefix (a big system prompt, tool definitions or a reference document), you can mark it with `cache_control` so later requests reuse it. This cuts cost and latency. Caching works on *prefixes*, so put stable content first and changing content last.

## Check yourself

??? question "A nightly job summarises 40,000 support tickets for a morning report. Synchronous or batch?"
    **Batch.** Nothing is waiting in real time, the volume is high, and it costs about half as much. Use `custom_id` to match results back to tickets.

??? question "A pre-merge CI check must pass before a developer can merge. Synchronous or batch?"
    **Synchronous.** The workflow is blocked waiting for the result, and a batch could take hours.
