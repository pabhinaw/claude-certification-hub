# Question Bank · Model Selection & Optimisation

**24 original questions** (2 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Context window · Cost · Latency · Model choice · Non-determinism · Prompt caching · Sampling · Thinking · Token budgeting · Tokens

---

<p class="qb-meta"><span class="qb-id">MS-001</span><span>Tokens</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which statement about tokens and pricing is correct?

- **A.** Output tokens are priced higher than input tokens
- **B.** Tokens are billed per request, whatever the length
- **C.** Input and output tokens are always priced the same
- **D.** Only output tokens are billed; input is free

??? success "Answer: A"
    **Why A is right:** Output costs several times more per token, so trimming output is an effective saving.

    **Why the others are wrong:**

    * **B:** Billing is per token.
    * **C:** They are priced differently.
    * **D:** Input tokens are billed too.

---

<p class="qb-meta"><span class="qb-id">MS-002</span><span>Context window</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What does a model's context window limit?

- **A.** The number of tools that may be defined in a request
- **B.** The total input and output tokens in one request
- **C.** The number of requests that can be sent per minute
- **D.** How many days a conversation is stored by the API

??? success "Answer: B"
    **Why B is right:** System prompt, tools, history and the generated output all share the window.

    **Why the others are wrong:**

    * **A:** Tools consume tokens but the window is measured in tokens.
    * **C:** That is a rate limit.
    * **D:** The API does not store conversations.

---

<p class="qb-meta"><span class="qb-id">MS-003</span><span>Context window</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team moves to a model with a much larger context window and expects the assistant to remember users between sessions. It does not. Why?

- **A.** The window must first be enabled in the Console
- **B.** A context window is per request and is not persistent memory
- **C.** Memory only works at temperature zero
- **D.** Large windows are only active when streaming is enabled

??? success "Answer: B"
    **Why B is right:** Whatever the size, the window holds only what is sent in that request.

    **Why the others are wrong:**

    * **A:** It is a property of the model, not a setting.
    * **C:** Temperature has nothing to do with persistence.
    * **D:** Window size is unrelated to streaming.

---

<p class="qb-meta"><span class="qb-id">MS-004</span><span>Sampling</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A data-extraction task needs the most consistent output possible. Which setting is most appropriate?

- **A.** A very small max_tokens value
- **B.** A low temperature, close to 0
- **C.** A high temperature, close to 1
- **D.** A long list of stop sequences

??? success "Answer: B"
    **Why B is right:** Low temperature favours the most likely tokens and reduces variation.

    **Why the others are wrong:**

    * **A:** That truncates output; it does not make it consistent.
    * **C:** That increases variety, the opposite of the goal.
    * **D:** Stop sequences end output; they do not reduce variation.

---

<p class="qb-meta"><span class="qb-id">MS-005</span><span>Non-determinism</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A unit test sends a fixed prompt at temperature 0 and asserts that the reply equals a stored string. It passes most days and occasionally fails. What is the best fix?

- **A.** Set top_p to 0 as well as temperature to force identity
- **B.** Run the test five times and pass if any run matches
- **C.** Assert on structure and key facts instead of exact text
- **D.** Cache the first response and compare against it forever

??? success "Answer: C"
    **Why C is right:** Output is not guaranteed identical even at temperature 0. Tests should check properties.

    **Why the others are wrong:**

    * **A:** No sampling setting guarantees identical output.
    * **B:** That hides flakiness instead of removing the fragile assertion.
    * **D:** That tests the cache, not the model's behaviour.

---

<p class="qb-meta"><span class="qb-id">MS-006</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service must label two million short messages per day as spam or not spam, with low latency. Which starting point is most sensible?

- **A.** The most capable tier, with extended thinking enabled
- **B.** The most capable tier, to be safe on every message
- **C.** The smallest, fastest tier, verified against an eval set
- **D.** Whichever tier leads a public coding leaderboard

??? success "Answer: C"
    **Why C is right:** Simple, high-volume classification suits the cheapest tier. Evals confirm whether it is good enough.

    **Why the others are wrong:**

    * **A:** Thinking adds cost and delay to a task that needs neither.
    * **B:** Far more cost and latency than a simple task needs.
    * **D:** A coding benchmark does not predict spam classification.

---

<p class="qb-meta"><span class="qb-id">MS-007</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A legal-analysis feature produces subtle reasoning errors on a mid-tier model. Volume is low and mistakes are costly. What should be tried?

- **A.** The same tier with max_tokens reduced by half
- **B.** A smaller tier, because it will respond more quickly
- **C.** A more capable tier, comparing results on the eval set
- **D.** The same tier with a higher temperature setting

??? success "Answer: C"
    **Why C is right:** With low volume and high error cost, capability outweighs price. Evals confirm the gain.

    **Why the others are wrong:**

    * **A:** Shorter output does not fix reasoning errors.
    * **B:** Speed is not the problem; reasoning quality is.
    * **D:** More randomness will not improve reasoning.

---

<p class="qb-meta"><span class="qb-id">MS-008</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What is the most reliable basis for choosing between two model tiers for a specific product feature?

- **A.** Selecting whichever model was released most recently
- **B.** Selecting whichever model has the larger context window
- **C.** Asking each model which of them is better at the task
- **D.** Comparing both on your own eval set for the feature

??? success "Answer: D"
    **Why D is right:** Only task-specific evaluation shows how each model performs on your workload.

    **Why the others are wrong:**

    * **A:** Newer does not mean better value for every task.
    * **B:** Window size is one factor and says little about quality on your task.
    * **C:** Self-assessment is not evidence.

---

<p class="qb-meta"><span class="qb-id">MS-009</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A support system handles simple FAQs and a small number of complex disputes. Which design best balances cost and quality?

- **A.** Alternate between models on every request for fairness
- **B.** Send everything to the largest model for consistency
- **C.** Send everything to the smallest model to control cost
- **D.** Route simple requests to a small model, hard ones up

??? success "Answer: D"
    **Why D is right:** Mixing tiers applies capability where it is needed and saves money elsewhere.

    **Why the others are wrong:**

    * **A:** Random assignment ignores what each task needs.
    * **B:** Overpays for the simple majority.
    * **C:** Under-serves the complex disputes.

---

<p class="qb-meta"><span class="qb-id">MS-010</span><span>Thinking</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Extended thinking is switched on for a feature that looks up a store's opening hours from a provided table. Cost and latency rise with no quality gain. Why?

- **A.** Thinking adds billed output and time a lookup doesn't need
- **B.** Thinking doubles the size of the input prompt
- **C.** Thinking forces the model to use the largest tier
- **D.** Thinking disables prompt caching for the whole account

??? success "Answer: A"
    **Why A is right:** Thinking helps complex multi-step reasoning. On simple tasks it only adds cost and delay.

    **Why the others are wrong:**

    * **B:** It adds output tokens, not input.
    * **C:** It does not change the model.
    * **D:** It does not disable caching account-wide.

---

<p class="qb-meta"><span class="qb-id">MS-011</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A request includes a 9,000-token policy document marked with cache_control. The first response shows cache_creation_input_tokens of about 9,000 and cache_read_input_tokens of 0. What does this mean?

- **A.** The prefix was cached now; later calls can read it
- **B.** Caching failed because no tokens were read from the cache
- **C.** The document was too short to be eligible for caching
- **D.** The cache is disabled for requests with a system prompt

??? success "Answer: A"
    **Why A is right:** The first call pays the write. Subsequent matching calls within the lifetime show cache reads.

    **Why the others are wrong:**

    * **B:** A first call always writes rather than reads.
    * **C:** Tokens were written, so it was eligible.
    * **D:** System prompts are a typical thing to cache.

---

<p class="qb-meta"><span class="qb-id">MS-012</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Caching is enabled on a long system prompt, but cache_read_input_tokens is always 0. The prompt begins with "Current date and time: " followed by a timestamp. What is the cause?

- **A.** System prompts cannot be cached, only user messages
- **B.** The timestamp changes, so the prefix never matches
- **C.** Caching only takes effect after 100 identical requests
- **D.** The cache lifetime is one second by default

??? success "Answer: B"
    **Why B is right:** A cache hit needs an identical prefix. Dynamic content must come after the cached section.

    **Why the others are wrong:**

    * **A:** System prompts can be cached.
    * **C:** There is no such threshold.
    * **D:** The default lifetime is five minutes.

---

<p class="qb-meta"><span class="qb-id">MS-013</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

How should a prompt be arranged to get the most from prompt caching?

- **A.** Stable and changing content interleaved in small pieces
- **B.** Stable content first, then whatever changes
- **C.** Order is irrelevant, since caching matches by content hash
- **D.** Changing content first, so that the model reads it sooner

??? success "Answer: B"
    **Why B is right:** Caching works on prefixes, so everything before the breakpoint must stay identical.

    **Why the others are wrong:**

    * **A:** The first change ends the reusable prefix.
    * **C:** Matching is prefix-based; order matters.
    * **D:** A changing start invalidates the whole prefix.

---

<p class="qb-meta"><span class="qb-id">MS-014</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

With default settings, how long does a cached prefix remain available?

- **A.** For exactly one further request, then it is deleted
- **B.** Twenty-four hours from when it is first written
- **C.** Five minutes, refreshed each time it is read
- **D.** Until the API key that wrote it is rotated

??? success "Answer: C"
    **Why C is right:** The default lifetime is five minutes and each hit renews it. A one-hour option costs more to write.

    **Why the others are wrong:**

    * **A:** It can be read many times within its lifetime.
    * **B:** That is not the default lifetime.
    * **D:** Lifetime is time-based.

---

<p class="qb-meta"><span class="qb-id">MS-015</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

How are cache writes and cache reads priced relative to normal input tokens (default five-minute cache)?

- **A.** Writes are free; reads cost the same as normal input
- **B.** Writes cost ten times more; reads are free
- **C.** Writes and reads both cost half of normal input
- **D.** Writes cost about 1.25 times; reads about 0.1 times

??? success "Answer: D"
    **Why D is right:** There is a small premium to write and a large discount to read.

    **Why the others are wrong:**

    * **A:** Writes carry a premium and reads are discounted.
    * **B:** Neither figure is right.
    * **C:** That confuses caching with batch pricing.

---

<p class="qb-meta"><span class="qb-id">MS-016</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool that answers one-off questions, each with a completely different 300-token prompt, enables prompt caching. Costs do not fall. Why?

- **A.** Caching applies only to output tokens, not input
- **B.** Caching only works with the Message Batches API
- **C.** Nothing is repeated, and the prompts are too short
- **D.** Caching needs temperature 0 to produce cache hits

??? success "Answer: C"
    **Why C is right:** Caching pays only when a sufficiently long prefix is reused.

    **Why the others are wrong:**

    * **A:** It applies to input prefixes.
    * **B:** It works with ordinary requests.
    * **D:** Sampling settings are not part of the match.

---

<p class="qb-meta"><span class="qb-id">MS-017</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A team reorders its tool definitions between requests, depending on which features are enabled. The cache hit rate collapses. Why?

- **A.** Reordering tools raises the cache's minimum token size
- **B.** Each tool definition needs its own cache breakpoint
- **C.** Tool definitions are never included in cached content
- **D.** Tools start the prefix, so changes invalidate the rest

??? success "Answer: D"
    **Why D is right:** The prefix order is tools, then system, then messages. A change early on breaks the rest.

    **Why the others are wrong:**

    * **A:** The minimum size does not depend on ordering.
    * **B:** One breakpoint after the tools is enough; only four exist.
    * **C:** They are part of the prefix.

---

<p class="qb-meta"><span class="qb-id">MS-018</span><span>Cost</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A chatbot sends a 10,000-token system prompt, a short question and gets a short answer, thousands of times a day. Which single change is likely to cut cost the most?

- **A.** Enabling streaming on every response
- **B.** Lowering the temperature to zero
- **C.** Raising max_tokens on each request
- **D.** Caching the system prompt

??? success "Answer: D"
    **Why D is right:** The repeated prefix dominates input cost, and cache reads are charged at a fraction of the normal price.

    **Why the others are wrong:**

    * **A:** Streaming does not change cost.
    * **B:** Temperature does not change token counts.
    * **C:** A higher cap cannot reduce cost.

---

<p class="qb-meta"><span class="qb-id">MS-019</span><span>Cost</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which combination gives the lowest cost for a large overnight job where every request shares a long instruction block?

- **A.** Message Batches API together with prompt caching
- **B.** Synchronous calls together with extended thinking
- **C.** Streaming together with a higher temperature
- **D.** The largest model together with a higher max_tokens

??? success "Answer: A"
    **Why A is right:** The batch discount and cache reads can be combined for work that is not time-sensitive.

    **Why the others are wrong:**

    * **B:** Thinking adds output cost and sync has no discount.
    * **C:** Neither reduces cost.
    * **D:** Both tend to raise cost.

---

<p class="qb-meta"><span class="qb-id">MS-020</span><span>Latency</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Responses are about 800 words and users complain about waiting. The content cannot be shortened. Which change most improves the experience at no extra cost?

- **A.** Stream the response so that text appears as it is generated
- **B.** Add extended thinking so that the answer is planned
- **C.** Use the Message Batches API for these requests
- **D.** Increase max_tokens to give the model more room

??? success "Answer: A"
    **Why A is right:** Streaming cuts perceived latency without changing the content or the price.

    **Why the others are wrong:**

    * **B:** Thinking adds time before the answer starts.
    * **C:** Batches are asynchronous and far slower.
    * **D:** A higher cap does not speed anything up.

---

<p class="qb-meta"><span class="qb-id">MS-021</span><span>Latency</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which factor usually has the largest effect on the total time of a single response?

- **A.** The alphabetical order of the tool names
- **B.** The number of output tokens generated
- **C.** Whether the system prompt uses XML tags
- **D.** The number of characters in the model ID

??? success "Answer: B"
    **Why B is right:** Output is generated token by token, so longer answers take longer.

    **Why the others are wrong:**

    * **A:** Irrelevant.
    * **C:** Formatting has negligible effect.
    * **D:** Irrelevant.

---

<p class="qb-meta"><span class="qb-id">MS-022</span><span>Token budgeting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent occasionally runs for hundreds of turns and produces a large bill. Which control addresses this most directly?

- **A.** A total token or cost budget for the task
- **B.** A lower max_tokens value on each individual call
- **C.** A higher temperature to encourage shorter runs
- **D.** A longer system prompt asking the agent to be frugal

??? success "Answer: A"
    **Why A is right:** Per-call limits do not bound a loop. A task-level budget does.

    **Why the others are wrong:**

    * **B:** Each call is smaller but the number of calls is unbounded.
    * **C:** Temperature does not bound the loop.
    * **D:** A request, not a limit.

---

<p class="qb-meta"><span class="qb-id">MS-023</span><span>Prompt caching</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO conditions would prevent a prompt-cache hit? (Select TWO.)

- **A.** A per-user greeting placed at the start of the cached block
- **B.** Sending the second request from a different server
- **C.** A different user question placed after the cache breakpoint
- **D.** Using streaming for the second request but not the first
- **E.** More than the cache lifetime passing between requests

??? success "Answer: A and E"
    **Why A is right:** Any difference in the prefix breaks the match.

    **Why E is right:** An expired entry cannot be read.

    **Why the others are wrong:**

    * **B:** The origin machine is not part of the match.
    * **C:** Content after the breakpoint may vary freely.
    * **D:** Streaming does not affect the match.

---

<p class="qb-meta"><span class="qb-id">MS-024</span><span>Latency</span><span>Select TWO</span><span title="Difficulty">●○○</span></p>

Which TWO changes reduce the actual end-to-end time of a response? (Select TWO.)

- **A.** Raising the max_tokens limit
- **B.** Logging the request ID
- **C.** Using a smaller, faster model tier
- **D.** Raising the temperature
- **E.** Asking for a shorter answer

??? success "Answer: C and E"
    **Why C is right:** Smaller tiers generate faster.

    **Why E is right:** Fewer output tokens take less time.

    **Why the others are wrong:**

    * **A:** A higher cap does not speed generation.
    * **B:** Logging has no effect on generation time.
    * **D:** Sampling randomness does not change speed.

---
