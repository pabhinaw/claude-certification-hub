# LLM & Claude Basics <span class="level-badge">L1</span>

## What a large language model does

A large language model (LLM) reads text and predicts what text should come next. Claude is an LLM made by Anthropic. Everything Claude "knows" during a request comes from two places:

1. **Its training**: general knowledge, fixed at a cutoff date.
2. **The context you send**: the system prompt, the conversation so far, tool results and documents.

Claude has **no memory between API calls**. If something is not in the request, Claude does not know it. This one fact explains a large share of exam questions.

## Tokens

Text is split into **tokens** (pieces of words). Pricing, speed and limits are all measured in tokens:

* **Input tokens**: everything you send (system prompt, messages, tool definitions, documents).
* **Output tokens**: what Claude writes back. You cap this with `max_tokens`.

A rough rule of thumb for English is that 1 token is about ¾ of a word.

## The context window

The **context window** is the maximum number of tokens Claude can consider in one request, inputs and outputs together. A bigger window is not automatically better:

* Long contexts cost more and run slower.
* Information buried in the *middle* of a very long context is used less reliably than information at the start or the end (the **"lost in the middle"** effect).
* In agent loops, tool results pile up quickly and crowd out what matters.

That is why the exams care so much about **context management** (Domain 5).

## Model tiers

Anthropic offers a family of models at different points on the capability / speed / cost curve. The classic tiers are **Haiku** (fastest, cheapest), **Sonnet** (balanced) and **Opus** (most capable). Newer, higher tiers may also exist. Model names and versions change often, so always check the official *Models overview* page.

Architect-level rule: **match the model to the task**. Use a smaller model for high-volume, simple classification or routing; use a larger model for complex reasoning, planning or coordination. In a multi-agent system the coordinator and the subagents can use different models.

## Extended / adaptive thinking

Claude can "think" before answering, which improves performance on hard reasoning tasks. Good to know for the exam: with manually enabled extended thinking, **forced tool use (`tool_choice` of `any` or a named `tool`) is not supported**. Only `auto` and `none` work. See [Tool Use Basics](tool-use-basics.md).

## Check yourself

??? question "Claude answered correctly in turn 1 but 'forgot' the user's name in turn 2. What is the most likely bug?"
    The application did not include the turn-1 messages in the turn-2 request. The API is stateless; the client must resend the history.

??? question "Why might an important instruction placed in the middle of a 150k-token prompt be ignored?"
    The "lost in the middle" effect. Put critical facts at the start or end, or keep them in a compact, repeated "case facts" block.
