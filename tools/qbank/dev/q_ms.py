from devlib import Q, M

# ================= Model Selection & Optimisation =================

Q("MS", "Tokens", """
Which statement about tokens and pricing is correct?""",
  "Output tokens are priced higher than input tokens",
  "Output costs several times more per token, so trimming output is an effective saving.",
  [("Input and output tokens are always priced the same", "They are priced differently."),
   ("Only output tokens are billed; input is free", "Input tokens are billed too."),
   ("Tokens are billed per request, whatever the length", "Billing is per token.")], level=1)

Q("MS", "Context window", """
What does a model's context window limit?""",
  "The total input and output tokens in one request",
  "System prompt, tools, history and the generated output all share the window.",
  [("The number of requests that can be sent per minute", "That is a rate limit."),
   ("How many days a conversation is stored by the API", "The API does not store conversations."),
   ("The number of tools that may be defined in a request", "Tools consume tokens but the window is measured in tokens.")], level=1)

Q("MS", "Context window", """
A team moves to a model with a much larger context window and expects the assistant to remember users between sessions. It does not. Why?""",
  "A context window is per request and is not persistent memory",
  "Whatever the size, the window holds only what is sent in that request.",
  [("Large windows are only active when streaming is enabled", "Window size is unrelated to streaming."),
   ("Memory only works at temperature zero", "Temperature has nothing to do with persistence."),
   ("The window must first be enabled in the Console", "It is a property of the model, not a setting.")], level=1)

Q("MS", "Sampling", """
A data-extraction task needs the most consistent output possible. Which setting is most appropriate?""",
  "A low temperature, close to 0",
  "Low temperature favours the most likely tokens and reduces variation.",
  [("A high temperature, close to 1", "That increases variety, the opposite of the goal."),
   ("A very small max_tokens value", "That truncates output; it does not make it consistent."),
   ("A long list of stop sequences", "Stop sequences end output; they do not reduce variation.")], level=1)

Q("MS", "Non-determinism", """
A unit test sends a fixed prompt at temperature 0 and asserts that the reply equals a stored string. It passes most days and occasionally fails. What is the best fix?""",
  "Assert on structure and key facts instead of exact text",
  "Output is not guaranteed identical even at temperature 0. Tests should check properties.",
  [("Run the test five times and pass if any run matches", "That hides flakiness instead of removing the fragile assertion."),
   ("Set top_p to 0 as well as temperature to force identity", "No sampling setting guarantees identical output."),
   ("Cache the first response and compare against it forever", "That tests the cache, not the model's behaviour.")])

Q("MS", "Model choice", """
A service must label two million short messages per day as spam or not spam, with low latency. Which starting point is most sensible?""",
  "The smallest, fastest tier, verified against an eval set",
  "Simple, high-volume classification suits the cheapest tier. Evals confirm whether it is good enough.",
  [("The most capable tier, to be safe on every message", "Far more cost and latency than a simple task needs."),
   ("The most capable tier, with extended thinking enabled", "Thinking adds cost and delay to a task that needs neither."),
   ("Whichever tier leads a public coding leaderboard", "A coding benchmark does not predict spam classification.")], level=1)

Q("MS", "Model choice", """
A legal-analysis feature produces subtle reasoning errors on a mid-tier model. Volume is low and mistakes are costly. What should be tried?""",
  "A more capable tier, comparing results on the eval set",
  "With low volume and high error cost, capability outweighs price. Evals confirm the gain.",
  [("A smaller tier, because it will respond more quickly", "Speed is not the problem; reasoning quality is."),
   ("The same tier with a higher temperature setting", "More randomness will not improve reasoning."),
   ("The same tier with max_tokens reduced by half", "Shorter output does not fix reasoning errors.")])

Q("MS", "Model choice", """
What is the most reliable basis for choosing between two model tiers for a specific product feature?""",
  "Comparing both on your own eval set for the feature",
  "Only task-specific evaluation shows how each model performs on your workload.",
  [("Selecting whichever model was released most recently", "Newer does not mean better value for every task."),
   ("Selecting whichever model has the larger context window", "Window size is one factor and says little about quality on your task."),
   ("Asking each model which of them is better at the task", "Self-assessment is not evidence.")])

Q("MS", "Model choice", """
A support system handles simple FAQs and a small number of complex disputes. Which design best balances cost and quality?""",
  "Route simple requests to a small model, hard ones up",
  "Mixing tiers applies capability where it is needed and saves money elsewhere.",
  [("Send everything to the largest model for consistency", "Overpays for the simple majority."),
   ("Send everything to the smallest model to control cost", "Under-serves the complex disputes."),
   ("Alternate between models on every request for fairness", "Random assignment ignores what each task needs.")])

Q("MS", "Thinking", """
Extended thinking is switched on for a feature that looks up a store's opening hours from a provided table. Cost and latency rise with no quality gain. Why?""",
  "Thinking adds billed output and time a lookup doesn't need",
  "Thinking helps complex multi-step reasoning. On simple tasks it only adds cost and delay.",
  [("Thinking disables prompt caching for the whole account", "It does not disable caching account-wide."),
   ("Thinking forces the model to use the largest tier", "It does not change the model."),
   ("Thinking doubles the size of the input prompt", "It adds output tokens, not input.")])

Q("MS", "Prompt caching", """
A request includes a 9,000-token policy document marked with cache_control. The first response shows cache_creation_input_tokens of about 9,000 and cache_read_input_tokens of 0. What does this mean?""",
  "The prefix was cached now; later calls can read it",
  "The first call pays the write. Subsequent matching calls within the lifetime show cache reads.",
  [("Caching failed because no tokens were read from the cache", "A first call always writes rather than reads."),
   ("The document was too short to be eligible for caching", "Tokens were written, so it was eligible."),
   ("The cache is disabled for requests with a system prompt", "System prompts are a typical thing to cache.")])

Q("MS", "Prompt caching", """
Caching is enabled on a long system prompt, but cache_read_input_tokens is always 0. The prompt begins with "Current date and time: " followed by a timestamp. What is the cause?""",
  "The timestamp changes, so the prefix never matches",
  "A cache hit needs an identical prefix. Dynamic content must come after the cached section.",
  [("System prompts cannot be cached, only user messages", "System prompts can be cached."),
   ("Caching only takes effect after 100 identical requests", "There is no such threshold."),
   ("The cache lifetime is one second by default", "The default lifetime is five minutes.")])

Q("MS", "Prompt caching", """
How should a prompt be arranged to get the most from prompt caching?""",
  "Stable content first, then whatever changes",
  "Caching works on prefixes, so everything before the breakpoint must stay identical.",
  [("Changing content first, so that the model reads it sooner", "A changing start invalidates the whole prefix."),
   ("Stable and changing content interleaved in small pieces", "The first change ends the reusable prefix."),
   ("Order is irrelevant, since caching matches by content hash", "Matching is prefix-based; order matters.")], level=1)

Q("MS", "Prompt caching", """
With default settings, how long does a cached prefix remain available?""",
  "Five minutes, refreshed each time it is read",
  "The default lifetime is five minutes and each hit renews it. A one-hour option costs more to write.",
  [("Twenty-four hours from when it is first written", "That is not the default lifetime."),
   ("Until the API key that wrote it is rotated", "Lifetime is time-based."),
   ("For exactly one further request, then it is deleted", "It can be read many times within its lifetime.")])

Q("MS", "Prompt caching", """
How are cache writes and cache reads priced relative to normal input tokens (default five-minute cache)?""",
  "Writes cost about 1.25 times; reads about 0.1 times",
  "There is a small premium to write and a large discount to read.",
  [("Writes are free; reads cost the same as normal input", "Writes carry a premium and reads are discounted."),
   ("Writes and reads both cost half of normal input", "That confuses caching with batch pricing."),
   ("Writes cost ten times more; reads are free", "Neither figure is right.")])

Q("MS", "Prompt caching", """
A tool that answers one-off questions, each with a completely different 300-token prompt, enables prompt caching. Costs do not fall. Why?""",
  "Nothing is repeated, and the prompts are too short",
  "Caching pays only when a sufficiently long prefix is reused.",
  [("Caching only works with the Message Batches API", "It works with ordinary requests."),
   ("Caching needs temperature 0 to produce cache hits", "Sampling settings are not part of the match."),
   ("Caching applies only to output tokens, not input", "It applies to input prefixes.")])

Q("MS", "Prompt caching", """
A team reorders its tool definitions between requests, depending on which features are enabled. The cache hit rate collapses. Why?""",
  "Tools start the prefix, so changes invalidate the rest",
  "The prefix order is tools, then system, then messages. A change early on breaks the rest.",
  [("Tool definitions are never included in cached content", "They are part of the prefix."),
   ("Reordering tools raises the cache's minimum token size", "The minimum size does not depend on ordering."),
   ("Each tool definition needs its own cache breakpoint", "One breakpoint after the tools is enough; only four exist.")], level=3)

Q("MS", "Cost", """
A chatbot sends a 10,000-token system prompt, a short question and gets a short answer, thousands of times a day. Which single change is likely to cut cost the most?""",
  "Caching the system prompt",
  "The repeated prefix dominates input cost, and cache reads are charged at a fraction of the normal price.",
  [("Enabling streaming on every response", "Streaming does not change cost."),
   ("Lowering the temperature to zero", "Temperature does not change token counts."),
   ("Raising max_tokens on each request", "A higher cap cannot reduce cost.")])

Q("MS", "Cost", """
Which combination gives the lowest cost for a large overnight job where every request shares a long instruction block?""",
  "Message Batches API together with prompt caching",
  "The batch discount and cache reads can be combined for work that is not time-sensitive.",
  [("Synchronous calls together with extended thinking", "Thinking adds output cost and sync has no discount."),
   ("Streaming together with a higher temperature", "Neither reduces cost."),
   ("The largest model together with a higher max_tokens", "Both tend to raise cost.")])

Q("MS", "Latency", """
Responses are about 800 words and users complain about waiting. The content cannot be shortened. Which change most improves the experience at no extra cost?""",
  "Stream the response so that text appears as it is generated",
  "Streaming cuts perceived latency without changing the content or the price.",
  [("Use the Message Batches API for these requests", "Batches are asynchronous and far slower."),
   ("Add extended thinking so that the answer is planned", "Thinking adds time before the answer starts."),
   ("Increase max_tokens to give the model more room", "A higher cap does not speed anything up.")], level=1)

Q("MS", "Latency", """
Which factor usually has the largest effect on the total time of a single response?""",
  "The number of output tokens generated",
  "Output is generated token by token, so longer answers take longer.",
  [("The number of characters in the model ID", "Irrelevant."),
   ("Whether the system prompt uses XML tags", "Formatting has negligible effect."),
   ("The alphabetical order of the tool names", "Irrelevant.")])

Q("MS", "Token budgeting", """
An agent occasionally runs for hundreds of turns and produces a large bill. Which control addresses this most directly?""",
  "A total token or cost budget for the task",
  "Per-call limits do not bound a loop. A task-level budget does.",
  [("A lower max_tokens value on each individual call", "Each call is smaller but the number of calls is unbounded."),
   ("A higher temperature to encourage shorter runs", "Temperature does not bound the loop."),
   ("A longer system prompt asking the agent to be frugal", "A request, not a limit.")])

M("MS", "Prompt caching", """
Which TWO conditions would prevent a prompt-cache hit? (Select TWO.)""",
  [("A per-user greeting placed at the start of the cached block", "Any difference in the prefix breaks the match."),
   ("More than the cache lifetime passing between requests", "An expired entry cannot be read.")],
  [("A different user question placed after the cache breakpoint", "Content after the breakpoint may vary freely."),
   ("Using streaming for the second request but not the first", "Streaming does not affect the match."),
   ("Sending the second request from a different server", "The origin machine is not part of the match.")])

M("MS", "Latency", """
Which TWO changes reduce the actual end-to-end time of a response? (Select TWO.)""",
  [("Using a smaller, faster model tier", "Smaller tiers generate faster."),
   ("Asking for a shorter answer", "Fewer output tokens take less time.")],
  [("Raising the max_tokens limit", "A higher cap does not speed generation."),
   ("Raising the temperature", "Sampling randomness does not change speed."),
   ("Logging the request ID", "Logging has no effect on generation time.")], level=1)
