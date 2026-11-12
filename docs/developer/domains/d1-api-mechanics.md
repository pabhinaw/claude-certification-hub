# Applications & Integration · Part 1: Claude API Mechanics <span class="level-badge">33.1%</span>

A third of the exam is *Applications & Integration*. This page covers the mechanical half: exactly what goes into a request, what comes back, and what your code must do when things go wrong. [Part 2](d1-application-design.md) covers design decisions.

!!! tip "How to study this page"
    Don't just read it. Open a terminal, make each call once, and print the raw response. Twenty minutes of typing fixes these facts in memory better than two hours of reading.

## What this page covers

* The request and response shape of the Messages API
* Statelessness and conversation history
* `stop_reason`: every value and what your code does next
* Streaming events
* Errors, retries, timeouts and rate limits
* Token counting, batches, and files

---

## 1. The request

```python
import anthropic

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
MODEL = "..."                    # a current model ID from the Models overview

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    system="You are a concise assistant for a fictional bookshop.",
    messages=[{"role": "user", "content": "Suggest one classic novel."}],
)
print(response.content[0].text)
```

| Part | Rule to remember |
|---|---|
| Endpoint | `POST /v1/messages` |
| Headers (raw HTTP) | `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json`. The SDKs add these for you. |
| **Required** fields | `model`, `max_tokens`, `messages` |
| `system` | A **top-level** parameter. There is no `"system"` role inside `messages`. |
| `messages` | Alternating `user` / `assistant` turns. The first message is from `user`. |
| `content` | A plain string, or a list of **content blocks** (`text`, `image`, `document`, `tool_use`, `tool_result`, `thinking`) |
| `max_tokens` | A hard cap on **output** tokens. It is a limit, not a target. |
| Optional | `temperature`, `stop_sequences`, `stream`, `tools`, `tool_choice`, `thinking`, `output_config`, `metadata` |

## 2. The response

```json
{
  "id": "msg_01ExampleOnly",
  "type": "message",
  "role": "assistant",
  "model": "...",
  "content": [{"type": "text", "text": "Try 'Middlemarch'."}],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 31,
    "output_tokens": 9,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

!!! danger "The #1 beginner bug"
    `content` is a **list of blocks**, not a string. `response.content[0].text` works only when the first block is text. With tools or thinking enabled, the first block may be something else. Loop over the blocks and check each `type`.

## 3. The API is stateless

The API remembers nothing between calls. To continue a conversation, **your application sends the whole history every time**.

```python
history = [{"role": "user", "content": "My name is Sam."}]
r1 = client.messages.create(model=MODEL, max_tokens=200, messages=history)

history.append({"role": "assistant", "content": r1.content})   # keep ALL blocks
history.append({"role": "user", "content": "What is my name?"})
r2 = client.messages.create(model=MODEL, max_tokens=200, messages=history)
```

Consequences the exam likes:

* Input tokens **grow every turn**, so cost and latency grow too. That is why caching and context management exist.
* "Session handling" is **your** job: store the history (database, cache) keyed by your own session ID.
* When appending an assistant turn, append `response.content` as it is. Dropping `tool_use` or `thinking` blocks breaks the next request.

## 4. `stop_reason`: always check it

A `200` response only means the request was processed. `stop_reason` tells you **why generation stopped**, and your code should branch on it.

| `stop_reason` | Meaning | What your code does |
|---|---|---|
| `end_turn` | Claude finished naturally | Use the response |
| `max_tokens` | Output hit your `max_tokens` cap | Treat as **truncated**: raise the cap or continue the response |
| `stop_sequence` | Claude produced one of your `stop_sequences` | Read `stop_sequence` to see which one |
| `tool_use` | Claude wants a tool called | Run the tool, return a `tool_result`, call again |
| `pause_turn` | A server-side tool loop paused | Send the assistant content back unchanged to continue |
| `refusal` | Claude declined | Handle gracefully; don't blindly retry the same request |
| `model_context_window_exceeded` | The response filled the context window | Treat as truncated |

!!! warning "Truncated JSON"
    The classic production bug: a JSON response cut off by `max_tokens`. The parser crashes and people blame the model. Check `stop_reason == "max_tokens"` **before** parsing.

## 5. Streaming

Set `stream=True` (or use the SDK helper) to receive **server-sent events (SSE)** as tokens are generated. Streaming improves *perceived* latency. It does not make the full response finish sooner.

```text
message_start
  content_block_start      (index 0)
    content_block_delta    (text_delta / input_json_delta / thinking_delta) ... repeated
  content_block_stop
  ... more blocks ...
message_delta              (stop_reason and final usage arrive here)
message_stop
```

`ping` events can appear anywhere. Ignore them.

```python
with client.messages.stream(
    model=MODEL, max_tokens=1024,
    messages=[{"role": "user", "content": "Explain SSE in two sentences."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()      # full Message, including usage
```

Facts worth memorising:

* **Text** arrives as `text_delta`. **Tool input** arrives as `input_json_delta` pieces of *partial JSON*: accumulate the strings and parse once at `content_block_stop`. Never parse each fragment.
* `stop_reason` arrives in **`message_delta`**, near the end, not in `message_start`.
* An error can arrive **mid-stream, after the HTTP 200**, as an `error` event. Your code must handle a stream that ends badly.
* Use streaming for long outputs. Long non-streaming requests risk network timeouts, and the SDKs refuse non-streaming requests they expect to exceed about 10 minutes.

## 6. Errors

Error bodies have one shape:

```json
{"type": "error", "error": {"type": "rate_limit_error", "message": "..."}, "request_id": "req_..."}
```

| Status | `error.type` | Cause | Retry? |
|---|---|---|---|
| 400 | `invalid_request_error` | Malformed request, bad parameter | **No.** Fix the request |
| 401 | `authentication_error` | Missing or wrong API key | **No.** Fix the key |
| 403 | `permission_error` | Key lacks permission for the resource | **No** |
| 404 | `not_found_error` | Wrong model ID or resource | **No** |
| 413 | `request_too_large` | Request body over the size limit | **No.** Shrink it |
| 429 | `rate_limit_error` | Rate limit hit | **Yes**, after the `retry-after` time |
| 500 | `api_error` | Unexpected server error | **Yes**, with backoff |
| 504 | `timeout_error` | Request took too long | Yes; consider streaming |
| 529 | `overloaded_error` | API temporarily overloaded | **Yes**, with backoff |

**The one rule:** *4xx = your request is wrong, so repeating it cannot help (429 is the exception). 5xx = try again later.*

```python
import anthropic

try:
    r = client.messages.create(model=MODEL, max_tokens=512, messages=msgs)
except anthropic.RateLimitError as e:            # 429
    wait = e.response.headers.get("retry-after")
except anthropic.APIConnectionError:             # network problem, no response
    ...
except anthropic.APIStatusError as e:            # any other non-2xx
    log.error("status=%s request_id=%s", e.status_code, e.response.headers.get("request-id"))
```

**What the SDKs already do for you**

* Retry connection errors, 408, 409, 429 and 5xx **twice by default**, with exponential backoff. Change with `max_retries`.
* Time out after **10 minutes by default**. Change with `timeout`.
* Per-call override: `client.with_options(max_retries=5, timeout=30.0).messages.create(...)`.

So before writing your own retry loop, remember the SDK has one. Stacking a second loop on top multiplies the attempts.

!!! note "Log the request ID"
    Every response carries a `request-id` header (`response._request_id` in the Python SDK). Log it. It is what support needs to trace a problem.

## 7. Rate limits

* Measured per organisation, per model class, in **RPM** (requests/min), **ITPM** (input tokens/min) and **OTPM** (output tokens/min).
* A **token bucket**: capacity refills continuously, not on the minute boundary. A short burst can trip a limit even when the per-minute average looks fine.
* Exceeding any limit returns **429** with a **`retry-after`** header. Honour it.
* Response headers (`anthropic-ratelimit-*`) show the limit, what remains and when it resets.
* On most current models, **cache reads do not count toward ITPM**. Prompt caching therefore raises effective throughput as well as cutting cost.
* OTPM counts tokens **actually generated**. A large `max_tokens` does not consume rate limit by itself.
* Limits rise with your **usage tier**. A sudden sharp ramp-up can also trigger 429s; ramp gradually.

**What to do about 429s, in order:** honour `retry-after` → exponential backoff with jitter → smooth bursts with a queue → cache the stable prefix → move non-urgent work to the Batches API → request higher limits.

## 8. Token counting

```python
count = client.messages.count_tokens(
    model=MODEL, system=SYSTEM, messages=msgs, tools=TOOLS,
)
print(count.input_tokens)
```

* Takes the **same inputs** as a message request (system, tools, images, PDFs) and returns `input_tokens`.
* **Free**, with its own RPM limit, separate from message creation.
* It is an **estimate**; the real figure can differ slightly.
* Use it *before* sending: to check the prompt fits, to route to a model, or to enforce a budget. After a call, read the real numbers from `usage`.

## 9. Message Batches API

For work nobody is waiting on.

| | |
|---|---|
| Cost | **50% cheaper** than standard calls |
| Timing | Asynchronous. Most batches finish within an hour; a batch **expires after 24 hours** |
| Size | Up to 100,000 requests or 256 MB per batch |
| Matching | Each request has your own **`custom_id`**. Results are **not** guaranteed to be in order |
| Results | Each entry is `succeeded`, `errored`, `canceled` or `expired`. Results stay available for 29 days |
| Limits | Separate rate limits from the standard Messages API |

```python
batch = client.messages.batches.create(requests=[
    {"custom_id": "doc-0001",
     "params": {"model": MODEL, "max_tokens": 300,
                "messages": [{"role": "user", "content": "Summarise: ..."}]}},
])
# later: poll until batch.processing_status == "ended", then read results by custom_id
```

**Decision rule:** *Is a person or a blocking process waiting?* Yes → synchronous (stream if long). No, and hours are acceptable → batch. Batch and prompt caching can be combined.

## 10. Images, PDFs and files

* Images go in an `image` content block (base64, URL, or a file reference). PDFs go in a `document` block.
* Put the image or document **before** the question about it.
* Images and PDFs cost input tokens like everything else. Large ones are expensive.
* The **Files API** lets you upload once and reference by `file_id` across requests, instead of resending the bytes each time. It is a beta feature; check the docs for the current header.

## 11. Extended thinking in the API

When thinking is enabled, the response contains `thinking` blocks before the answer.

* Thinking counts as **output tokens**, so leave room in `max_tokens`.
* In a tool loop, **return thinking blocks unchanged** with the rest of the assistant content. Editing or dropping them breaks the next request.
* Forced `tool_choice` (`any` or a named tool) is not compatible with manually enabled thinking.
* Thinking is a *mode*, separate from the *model*. Choosing a tier and switching thinking on are two different decisions ([Model Selection](d2-model-selection.md)).

## 12. Cloud platforms and data

Claude is also available through cloud vendors. Authentication, model identifiers and feature availability differ there, so confirm a feature exists on your platform before depending on it. Know how long each feature keeps data: stored files, batches and other stateful features retain content for a period by design. [Part 3](d1-engineering-foundations.md) has the detail.

---

## Traps

| Trap | Reality |
|---|---|
| "Add a message with role `system`" | `system` is a top-level parameter |
| "The API keeps my conversation" | Stateless. You resend history |
| "Status 200 means the answer is complete" | Check `stop_reason` |
| "Streaming makes the response finish faster" | Faster *first token*, same total |
| "Retry every error" | Retry 429 / 5xx / connection. Fix 4xx |
| "`max_tokens` sets how long the answer should be" | It caps output; control length in the prompt |
| "Batch results come back in order" | Match by `custom_id` |
| "Token counting costs tokens" | Free, separately rate-limited |

## Decision rules

1. **Branch on `stop_reason` before using content.**
2. **4xx: fix. 429/5xx: back off and retry. Log `request-id`.**
3. **Long output or a waiting user → stream.**
4. **Nobody waiting → batch, matched by `custom_id`.**
5. **State lives in your app, not the API.**

## Check yourself

??? question "A chat app works for short replies but long JSON reports sometimes fail to parse. What do you check first?"
    `stop_reason`. If it is `max_tokens`, the JSON was truncated. Raise `max_tokens` (and stream), and only parse when the response completed.

??? question "Your service gets a 400 `invalid_request_error`. A colleague wraps the call in a retry loop. Why is that wrong?"
    A 400 means the request itself is invalid. Sending it again gives the same error. Fix the request. Retries are for 429, 5xx and connection errors.

??? question "While streaming a tool call you receive several `input_json_delta` events. How do you get the tool input?"
    Concatenate the `partial_json` strings for that content block and parse the result once, when `content_block_stop` arrives.

??? question "A nightly job classifies 40,000 support emails. Results are needed by 8 am. Which API?"
    The Message Batches API: half the cost, nobody is waiting, each request tagged with a `custom_id`.

??? question "Where does the conversation history live between two API calls?"
    In your application. The API is stateless, so you store the messages and resend them.

---

!!! abstract "Verify in official docs"
    Limits, headers and beta flags change. Check before relying on a number:

    * [Messages API reference](https://platform.claude.com/docs/en/api/messages)
    * [Stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
    * [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
    * [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
