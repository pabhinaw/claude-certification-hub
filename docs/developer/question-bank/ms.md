# Question Bank · Model Selection & Optimisation

**30 original questions** (2 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Cache checkpoints · Context window · Cost · Latency · Model choice · Model options · Model releases · Non-determinism · Prompt caching · Prompting styles · Sampling · Thinking · Token budgeting · Tokens · Usage tracking

---

<p class="qb-meta"><span class="qb-id">MS-001</span><span>Tokens</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which statement about tokens and pricing is correct?

- **A.** Output tokens are priced higher than input tokens
- **B.** Only output tokens are billed; input is free
- **C.** Input and output tokens are always priced the same
- **D.** Tokens are billed per request, whatever the length

??? success "Answer: A"
    **Why A is right:** Output costs several times more per token, so trimming output is an effective saving.

    **Why the others are wrong:**

    * **B:** Input tokens are billed too.
    * **C:** They are priced differently.
    * **D:** Billing is per token.

---

<p class="qb-meta"><span class="qb-id">MS-002</span><span>Context window</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What does a model's context window limit?

- **A.** The total input and output tokens in one request
- **B.** How many days a conversation is stored by the API
- **C.** The number of requests that can be sent per minute
- **D.** The number of tools that may be defined in a request

??? success "Answer: A"
    **Why A is right:** System prompt, tools, history and the generated output all share the window.

    **Why the others are wrong:**

    * **B:** The API does not store conversations.
    * **C:** That is a rate limit.
    * **D:** Tools consume tokens but the window is measured in tokens.

---

<p class="qb-meta"><span class="qb-id">MS-003</span><span>Context window</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team moves to a model with a much larger context window and expects the assistant to remember users between sessions. It does not. Why?

- **A.** Memory only works at temperature zero
- **B.** A context window is per request and is not persistent memory
- **C.** Large windows are only active when streaming is enabled
- **D.** The window must first be enabled in the Console

??? success "Answer: B"
    **Why B is right:** Whatever the size, the window holds only what is sent in that request.

    **Why the others are wrong:**

    * **A:** Temperature has nothing to do with persistence.
    * **C:** Window size is unrelated to streaming.
    * **D:** It is a property of the model, not a setting.

---

<p class="qb-meta"><span class="qb-id">MS-004</span><span>Sampling</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A data-extraction task needs the most consistent output possible. Which setting is most appropriate?

- **A.** A long list of stop sequences
- **B.** A low temperature, close to 0
- **C.** A high temperature, close to 1
- **D.** A very small max_tokens value

??? success "Answer: B"
    **Why B is right:** Low temperature favours the most likely tokens and reduces variation.

    **Why the others are wrong:**

    * **A:** Stop sequences end output; they do not reduce variation.
    * **C:** That increases variety, the opposite of the goal.
    * **D:** That truncates output; it does not make it consistent.

---

<p class="qb-meta"><span class="qb-id">MS-005</span><span>Non-determinism</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A unit test sends a fixed prompt at temperature 0 and asserts that the reply equals a stored string. It passes most days and occasionally fails. What is the best fix?

- **A.** Run the test five times and pass if any run matches
- **B.** Assert on structure and key facts instead of exact text
- **C.** Set top_p to 0 as well as temperature to force identity
- **D.** Cache the first response and compare against it forever

??? success "Answer: B"
    **Why B is right:** Output is not guaranteed identical even at temperature 0. Tests should check properties.

    **Why the others are wrong:**

    * **A:** That hides flakiness instead of removing the fragile assertion.
    * **C:** No sampling setting guarantees identical output.
    * **D:** That tests the cache, not the model's behaviour.

---

<p class="qb-meta"><span class="qb-id">MS-006</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service must label two million short messages per day as spam or not spam, with low latency. Which starting point is most sensible?

- **A.** Whichever tier leads a public coding leaderboard
- **B.** The most capable tier, to be safe on every message
- **C.** The smallest, fastest tier, verified against an eval set
- **D.** The most capable tier, with extended thinking enabled

??? success "Answer: C"
    **Why C is right:** Simple, high-volume classification suits the cheapest tier. Evals confirm whether it is good enough.

    **Why the others are wrong:**

    * **A:** A coding benchmark does not predict spam classification.
    * **B:** Far more cost and latency than a simple task needs.
    * **D:** Thinking adds cost and delay to a task that needs neither.

---

<p class="qb-meta"><span class="qb-id">MS-007</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A legal-analysis feature produces subtle reasoning errors on a mid-tier model. Volume is low and mistakes are costly. What should be tried?

- **A.** The same tier with max_tokens reduced by half
- **B.** A more capable tier, comparing results on the eval set
- **C.** The same tier with a higher temperature setting
- **D.** A smaller tier, because it will respond more quickly

??? success "Answer: B"
    **Why B is right:** With low volume and high error cost, capability outweighs price. Evals confirm the gain.

    **Why the others are wrong:**

    * **A:** Shorter output does not fix reasoning errors.
    * **C:** More randomness will not improve reasoning.
    * **D:** Speed is not the problem; reasoning quality is.

---

<p class="qb-meta"><span class="qb-id">MS-008</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What is the most reliable basis for choosing between two model tiers for a specific product feature?

- **A.** Selecting whichever model was released most recently
- **B.** Selecting whichever model has the larger context window
- **C.** Comparing both on your own eval set for the feature
- **D.** Asking each model which of them is better at the task

??? success "Answer: C"
    **Why C is right:** Only task-specific evaluation shows how each model performs on your workload.

    **Why the others are wrong:**

    * **A:** Newer does not mean better value for every task.
    * **B:** Window size is one factor and says little about quality on your task.
    * **D:** Self-assessment is not evidence.

---

<p class="qb-meta"><span class="qb-id">MS-009</span><span>Model choice</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A support system handles simple FAQs and a small number of complex disputes. Which design best balances cost and quality?

- **A.** Send everything to the largest model for consistency
- **B.** Send everything to the smallest model to control cost
- **C.** Route simple requests to a small model, hard ones up
- **D.** Alternate between models on every request for fairness

??? success "Answer: C"
    **Why C is right:** Mixing tiers applies capability where it is needed and saves money elsewhere.

    **Why the others are wrong:**

    * **A:** Overpays for the simple majority.
    * **B:** Under-serves the complex disputes.
    * **D:** Random assignment ignores what each task needs.

---

<p class="qb-meta"><span class="qb-id">MS-010</span><span>Thinking</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Extended thinking is switched on for a feature that looks up a store's opening hours from a provided table. Cost and latency rise with no quality gain. Why?

- **A.** Thinking forces the model to use the largest tier
- **B.** Thinking doubles the size of the input prompt
- **C.** Thinking disables prompt caching for the whole account
- **D.** Thinking adds billed output and time a lookup doesn't need

??? success "Answer: D"
    **Why D is right:** Thinking helps complex multi-step reasoning. On simple tasks it only adds cost and delay.

    **Why the others are wrong:**

    * **A:** It does not change the model.
    * **B:** It adds output tokens, not input.
    * **C:** It does not disable caching account-wide.

---

<p class="qb-meta"><span class="qb-id">MS-011</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A request includes a 9,000-token policy document marked with cache_control. The first response shows cache_creation_input_tokens of about 9,000 and cache_read_input_tokens of 0. What does this mean?

- **A.** The cache is disabled for requests with a system prompt
- **B.** Caching failed because no tokens were read from the cache
- **C.** The document was too short to be eligible for caching
- **D.** The prefix was cached now; later calls can read it

??? success "Answer: D"
    **Why D is right:** The first call pays the write. Subsequent matching calls within the lifetime show cache reads.

    **Why the others are wrong:**

    * **A:** System prompts are a typical thing to cache.
    * **B:** A first call always writes rather than reads.
    * **C:** Tokens were written, so it was eligible.

---

<p class="qb-meta"><span class="qb-id">MS-012</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Caching is enabled on a long system prompt, but cache_read_input_tokens is always 0. The prompt begins with "Current date and time: " followed by a timestamp. What is the cause?

- **A.** System prompts cannot be cached, only user messages
- **B.** The cache lifetime is one second by default
- **C.** The timestamp changes, so the prefix never matches
- **D.** Caching only takes effect after 100 identical requests

??? success "Answer: C"
    **Why C is right:** A cache hit needs an identical prefix. Dynamic content must come after the cached section.

    **Why the others are wrong:**

    * **A:** System prompts can be cached.
    * **B:** The default lifetime is five minutes.
    * **D:** There is no such threshold.

---

<p class="qb-meta"><span class="qb-id">MS-013</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

How should a prompt be arranged to get the most from prompt caching?

- **A.** Order is irrelevant, since caching matches by content hash
- **B.** Changing content first, so that the model reads it sooner
- **C.** Stable and changing content interleaved in small pieces
- **D.** Stable content first, then whatever changes

??? success "Answer: D"
    **Why D is right:** Caching works on prefixes, so everything before the breakpoint must stay identical.

    **Why the others are wrong:**

    * **A:** Matching is prefix-based; order matters.
    * **B:** A changing start invalidates the whole prefix.
    * **C:** The first change ends the reusable prefix.

---

<p class="qb-meta"><span class="qb-id">MS-014</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

With default settings, how long does a cached prefix remain available?

- **A.** Five minutes, refreshed each time it is read
- **B.** Until the API key that wrote it is rotated
- **C.** For exactly one further request, then it is deleted
- **D.** Twenty-four hours from when it is first written

??? success "Answer: A"
    **Why A is right:** The default lifetime is five minutes and each hit renews it. A one-hour option costs more to write.

    **Why the others are wrong:**

    * **B:** Lifetime is time-based.
    * **C:** It can be read many times within its lifetime.
    * **D:** That is not the default lifetime.

---

<p class="qb-meta"><span class="qb-id">MS-015</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

How are cache writes and cache reads priced relative to normal input tokens (default five-minute cache)?

- **A.** Writes cost about 1.25 times; reads about 0.1 times
- **B.** Writes are free; reads cost the same as normal input
- **C.** Writes and reads both cost half of normal input
- **D.** Writes cost ten times more; reads are free

??? success "Answer: A"
    **Why A is right:** There is a small premium to write and a large discount to read.

    **Why the others are wrong:**

    * **B:** Writes carry a premium and reads are discounted.
    * **C:** That confuses caching with batch pricing.
    * **D:** Neither figure is right.

---

<p class="qb-meta"><span class="qb-id">MS-016</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A tool that answers one-off questions, each with a completely different 300-token prompt, enables prompt caching. Costs do not fall. Why?

- **A.** Nothing is repeated, and the prompts are too short
- **B.** Caching only works with the Message Batches API
- **C.** Caching needs temperature 0 to produce cache hits
- **D.** Caching applies only to output tokens, not input

??? success "Answer: A"
    **Why A is right:** Caching pays only when a sufficiently long prefix is reused.

    **Why the others are wrong:**

    * **B:** It works with ordinary requests.
    * **C:** Sampling settings are not part of the match.
    * **D:** It applies to input prefixes.

---

<p class="qb-meta"><span class="qb-id">MS-017</span><span>Prompt caching</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A team reorders its tool definitions between requests, depending on which features are enabled. The cache hit rate collapses. Why?

- **A.** Reordering tools raises the cache's minimum token size
- **B.** Tools start the prefix, so changes invalidate the rest
- **C.** Tool definitions are never included in cached content
- **D.** Each tool definition needs its own cache breakpoint

??? success "Answer: B"
    **Why B is right:** The prefix order is tools, then system, then messages. A change early on breaks the rest.

    **Why the others are wrong:**

    * **A:** The minimum size does not depend on ordering.
    * **C:** They are part of the prefix.
    * **D:** One breakpoint after the tools is enough; only four exist.

---

<p class="qb-meta"><span class="qb-id">MS-018</span><span>Cost</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A chatbot sends a 10,000-token system prompt, a short question and gets a short answer, thousands of times a day. Which single change is likely to cut cost the most?

- **A.** Raising max_tokens on each request
- **B.** Caching the system prompt
- **C.** Lowering the temperature to zero
- **D.** Enabling streaming on every response

??? success "Answer: B"
    **Why B is right:** The repeated prefix dominates input cost, and cache reads are charged at a fraction of the normal price.

    **Why the others are wrong:**

    * **A:** A higher cap cannot reduce cost.
    * **C:** Temperature does not change token counts.
    * **D:** Streaming does not change cost.

---

<p class="qb-meta"><span class="qb-id">MS-019</span><span>Cost</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which combination gives the lowest cost for a large overnight job where every request shares a long instruction block?

- **A.** Synchronous calls together with extended thinking
- **B.** Message Batches API together with prompt caching
- **C.** Streaming together with a higher temperature
- **D.** The largest model together with a higher max_tokens

??? success "Answer: B"
    **Why B is right:** The batch discount and cache reads can be combined for work that is not time-sensitive.

    **Why the others are wrong:**

    * **A:** Thinking adds output cost and sync has no discount.
    * **C:** Neither reduces cost.
    * **D:** Both tend to raise cost.

---

<p class="qb-meta"><span class="qb-id">MS-020</span><span>Latency</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Responses are about 800 words and users complain about waiting. The content cannot be shortened. Which change most improves the experience at no extra cost?

- **A.** Increase max_tokens to give the model more room
- **B.** Use the Message Batches API for these requests
- **C.** Stream the response so that text appears as it is generated
- **D.** Add extended thinking so that the answer is planned

??? success "Answer: C"
    **Why C is right:** Streaming cuts perceived latency without changing the content or the price.

    **Why the others are wrong:**

    * **A:** A higher cap does not speed anything up.
    * **B:** Batches are asynchronous and far slower.
    * **D:** Thinking adds time before the answer starts.

---

<p class="qb-meta"><span class="qb-id">MS-021</span><span>Latency</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which factor usually has the largest effect on the total time of a single response?

- **A.** Whether the system prompt uses XML tags
- **B.** The alphabetical order of the tool names
- **C.** The number of output tokens generated
- **D.** The number of characters in the model ID

??? success "Answer: C"
    **Why C is right:** Output is generated token by token, so longer answers take longer.

    **Why the others are wrong:**

    * **A:** Formatting has negligible effect.
    * **B:** Irrelevant.
    * **D:** Irrelevant.

---

<p class="qb-meta"><span class="qb-id">MS-022</span><span>Token budgeting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent occasionally runs for hundreds of turns and produces a large bill. Which control addresses this most directly?

- **A.** A lower max_tokens value on each individual call
- **B.** A longer system prompt asking the agent to be frugal
- **C.** A total token or cost budget for the task
- **D.** A higher temperature to encourage shorter runs

??? success "Answer: C"
    **Why C is right:** Per-call limits do not bound a loop. A task-level budget does.

    **Why the others are wrong:**

    * **A:** Each call is smaller but the number of calls is unbounded.
    * **B:** A request, not a limit.
    * **D:** Temperature does not bound the loop.

---

<p class="qb-meta"><span class="qb-id">MS-023</span><span>Prompt caching</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO conditions would prevent a prompt-cache hit? (Select TWO.)

- **A.** A different user question placed after the cache breakpoint
- **B.** Sending the second request from a different server
- **C.** A per-user greeting placed at the start of the cached block
- **D.** More than the cache lifetime passing between requests
- **E.** Using streaming for the second request but not the first

??? success "Answer: C and D"
    **Why C is right:** Any difference in the prefix breaks the match.

    **Why D is right:** An expired entry cannot be read.

    **Why the others are wrong:**

    * **A:** Content after the breakpoint may vary freely.
    * **B:** The origin machine is not part of the match.
    * **E:** Streaming does not affect the match.

---

<p class="qb-meta"><span class="qb-id">MS-024</span><span>Latency</span><span>Select TWO</span><span title="Difficulty">●○○</span></p>

Which TWO changes reduce the actual end-to-end time of a response? (Select TWO.)

- **A.** Raising the temperature
- **B.** Using a smaller, faster model tier
- **C.** Asking for a shorter answer
- **D.** Logging the request ID
- **E.** Raising the max_tokens limit

??? success "Answer: B and C"
    **Why B is right:** Smaller tiers generate faster.

    **Why C is right:** Fewer output tokens take less time.

    **Why the others are wrong:**

    * **A:** Sampling randomness does not change speed.
    * **D:** Logging has no effect on generation time.
    * **E:** A higher cap does not speed generation.

---

<p class="qb-meta"><span class="qb-id">MS-025</span><span>Model options</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An interactive coding tool uses a top-tier model and needs faster output without changing the model's quality. Cost is a secondary concern. Which option addresses this directly?

- **A.** The Batches API, which returns results in seconds
- **B.** A higher max_tokens, which makes generation faster
- **C.** A smaller tier, which keeps the quality identical
- **D.** Fast mode, which speeds up the same model at a premium

??? success "Answer: D"
    **Why D is right:** Fast mode raises output speed for the same model at a higher price.

    **Why the others are wrong:**

    * **A:** Batches are asynchronous and slower.
    * **B:** The cap does not change speed.
    * **C:** A smaller model is faster but not the same quality.

---

<p class="qb-meta"><span class="qb-id">MS-026</span><span>Model options</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which statement correctly separates model choice from reasoning mode?

- **A.** Choosing a larger tier turns thinking on by default always
- **B.** Enabling thinking switches the request to a larger tier
- **C.** Thinking is only available on the smallest model tier
- **D.** Picking a tier and enabling thinking are separate decisions

??? success "Answer: D"
    **Why D is right:** A tier sets capability and price; thinking or effort settings control how much reasoning is done on a request.

    **Why the others are wrong:**

    * **A:** Tier and thinking are configured separately.
    * **B:** The model stays the same.
    * **C:** It is not limited to the smallest tier.

---

<p class="qb-meta"><span class="qb-id">MS-027</span><span>Prompting styles</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A classification prompt works well zero-shot. A developer adds twelve long examples "to be safe". What is the main cost?

- **A.** The context window is permanently reduced in size
- **B.** The model is no longer able to return any labels
- **C.** The API rejects prompts that contain examples
- **D.** More input tokens on every request, with little benefit

??? success "Answer: D"
    **Why D is right:** Examples are sent each time. When zero-shot already works, they add cost and latency for no gain.

    **Why the others are wrong:**

    * **A:** The window is per request, not permanently changed.
    * **B:** Examples do not prevent output.
    * **C:** Examples are allowed.

---

<p class="qb-meta"><span class="qb-id">MS-028</span><span>Model releases</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team upgrades to a newer model version. Token counts for the same prompts change, and some replies are formatted differently. What does this show?

- **A.** The API key was rotated during the upgrade process
- **B.** The prompts were corrupted while being transferred
- **C.** The temperature setting is reset by every upgrade
- **D.** Releases change behaviour; upgrades need evals

??? success "Answer: D"
    **Why D is right:** New versions are not drop-in replacements. Pin versions, re-run evals and re-count tokens.

    **Why the others are wrong:**

    * **A:** Key rotation does not change model behaviour.
    * **B:** Nothing indicates corruption.
    * **C:** Request parameters are whatever the code sends.

---

<p class="qb-meta"><span class="qb-id">MS-029</span><span>Cache checkpoints</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A prompt has tool definitions, a system prompt, a large reference document, and a growing conversation. Why might a developer set several cache breakpoints?

- **A.** So parts that change at different rates cache apart
- **B.** So that each breakpoint doubles the context window
- **C.** So that output tokens are billed at the cache rate
- **D.** So that the model reads the document several times

??? success "Answer: A"
    **Why A is right:** A change only invalidates what follows it. Layered breakpoints keep stable sections cached.

    **Why the others are wrong:**

    * **B:** They do not change the window.
    * **C:** Caching applies to input.
    * **D:** Breakpoints do not repeat content.

---

<p class="qb-meta"><span class="qb-id">MS-030</span><span>Usage tracking</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A company wants to know which product feature drives its Claude spend. What is the most direct approach?

- **A.** Record the usage from each response, tagged by feature
- **B.** Ask each team for an informal monthly impression
- **C.** Estimate from the number of lines in each prompt
- **D.** Compare the temperature used by each feature

??? success "Answer: A"
    **Why A is right:** Each response reports input, output and cache tokens. Tagging them shows where cost goes.

    **Why the others are wrong:**

    * **B:** Impressions are not measurements.
    * **C:** Line counts are a poor proxy for tokens.
    * **D:** Temperature does not indicate cost.

---
