# Question Bank · Applications & Integration

**71 original questions** (5 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Access control · Application design · Architecture · Batches · Choosing a pattern · Configuration · Conversation history · Errors · Life cycle · Observability · Platforms · Rate limits · Reliability · Request shape · Requirements · Response shape · SDK behaviour · Schema design · Session handling · Software engineering · Statelessness · Stop reasons · Streaming · Sync or batch · Systems life cycle · Technical fundamentals · Token counting · Validation

---

<p class="qb-meta"><span class="qb-id">AI-001</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer adds {"role": "system", "content": "You are a helpful travel assistant."} as the first item in the messages list and receives a 400 error. What is the correct fix?

- **A.** Move the text to the top-level system parameter of the request
- **B.** Place the system message last so that it takes priority
- **C.** Send the system text in a custom HTTP request header
- **D.** Rename the role to "developer" and send the request again

??? success "Answer: A"
    **Why A is right:** System prompts are a top-level parameter. The messages list only accepts user and assistant roles.

    **Why the others are wrong:**

    * **B:** Position does not matter; the role itself is not accepted.
    * **C:** Headers carry authentication and versioning, not prompt content.
    * **D:** There is no developer role in the Messages API.

---

<p class="qb-meta"><span class="qb-id">AI-002</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which set of fields is required in every Messages API request?

- **A.** model, max_tokens and messages
- **B.** model, system and messages
- **C.** model, messages and temperature
- **D.** model, max_tokens and stream

??? success "Answer: A"
    **Why A is right:** These three are mandatory. Everything else, including system and temperature, is optional.

    **Why the others are wrong:**

    * **B:** system is optional, and max_tokens is missing.
    * **C:** temperature is optional, and max_tokens is missing.
    * **D:** stream is optional, and messages is missing.

---

<p class="qb-meta"><span class="qb-id">AI-003</span><span>Statelessness</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A chatbot answers the first question well, but when the user follows up with "and what about the second one?", Claude has no idea what "the second one" refers to. The code sends only the newest user message on each call. What is the cause?

- **A.** The API is stateless, so earlier turns must be resent
- **B.** The session expired because the two calls were too far apart
- **C.** The temperature is too low for the model to recall context
- **D.** The model's context window was exceeded by the first answer

??? success "Answer: A"
    **Why A is right:** Nothing is remembered between calls. The full history must be included in messages each time.

    **Why the others are wrong:**

    * **B:** There is no server-side session to expire.
    * **C:** Temperature affects sampling, not memory.
    * **D:** A short exchange is nowhere near the window; the history was simply not sent.

---

<p class="qb-meta"><span class="qb-id">AI-004</span><span>Response shape</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

This line works in testing but raises an exception in production after tools are added to the request:

```python
answer = response.content[0].text
```

What is the most likely reason?

- **A.** Tool-enabled responses place the text in response.completion
- **B.** The first block is sometimes tool_use, without text
- **C.** The response body is returned as a string once tools are enabled
- **D.** The SDK needs an additional await when tools are present

??? success "Answer: B"
    **Why B is right:** content is a list of typed blocks. Code must check each block's type rather than assume the first is text.

    **Why the others are wrong:**

    * **A:** There is no completion field in the Messages API response.
    * **C:** The response shape is unchanged; content remains a list of blocks.
    * **D:** Whether a call is awaited depends on the client type, not on tools.

---

<p class="qb-meta"><span class="qb-id">AI-005</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A report generator asks for a long JSON document. About one request in twenty fails with a JSON parse error near the end of the text. The HTTP status is always 200. What should the developer check first?

- **A.** Whether the temperature is too high for producing JSON
- **B.** Whether stop_reason is max_tokens, meaning the output was cut off
- **C.** Whether the system prompt is longer than the user prompt
- **D.** Whether the API key is being rate limited on some requests

??? success "Answer: B"
    **Why B is right:** A 200 only means the request was processed. Truncation is reported through stop_reason, and truncated JSON cannot parse.

    **Why the others are wrong:**

    * **A:** Temperature may vary wording but would not cut the document off at the end.
    * **C:** Relative prompt lengths have no bearing on truncated output.
    * **D:** Rate limiting returns 429, not a 200 with partial content.

---

<p class="qb-meta"><span class="qb-id">AI-006</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A response arrives with stop_reason "tool_use". What must the application do next?

- **A.** Show the response text to the user as the final answer
- **B.** Run the tool and send a tool_result in a user turn
- **C.** Repeat the same request until stop_reason is end_turn
- **D.** Increase max_tokens, because the response was truncated

??? success "Answer: B"
    **Why B is right:** tool_use means Claude is waiting for your code to execute the tool and return the result.

    **Why the others are wrong:**

    * **A:** The turn is not finished; Claude is waiting for a tool result.
    * **C:** Repeating the request without a tool result just produces the same tool call.
    * **D:** Truncation is reported as max_tokens, not tool_use.

---

<p class="qb-meta"><span class="qb-id">AI-007</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application uses a server-side web search tool. A response comes back with stop_reason "pause_turn". What is the correct handling?

- **A.** Treat it as a refusal and show an apology to the user
- **B.** Execute the search in your own code and return a tool_result
- **C.** Send the assistant content back so Claude can continue
- **D.** Discard the response and start a new conversation

??? success "Answer: C"
    **Why C is right:** pause_turn means a server-side tool loop paused. Returning the content unchanged lets it resume.

    **Why the others are wrong:**

    * **A:** A pause is not a refusal; the work is simply unfinished.
    * **B:** Server tools run on the platform; there is no client tool call waiting.
    * **D:** That throws away progress; the turn can be continued.

---

<p class="qb-meta"><span class="qb-id">AI-008</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A request sets stop_sequences to ["###"]. The response has stop_reason "stop_sequence". Which statement is correct?

- **A.** Claude declined to answer and used "###" as a marker
- **B.** The output was truncated by the max_tokens limit
- **C.** Claude produced "###", and so generation stopped there
- **D.** The request failed validation because "###" is a reserved token

??? success "Answer: C"
    **Why C is right:** Custom stop sequences end generation, and the response reports the matched sequence.

    **Why the others are wrong:**

    * **A:** Declining is reported as refusal.
    * **B:** That would be reported as max_tokens.
    * **D:** It is a normal, successful response.

---

<p class="qb-meta"><span class="qb-id">AI-009</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team streams responses so users see text immediately. A new developer claims this also halves the total generation time. What is accurate?

- **A.** Streaming halves total time because tokens are sent in parallel
- **B.** Streaming is slower overall and should be avoided for chat
- **C.** Streaming speeds the first token, not the total time
- **D.** Streaming reduces cost because fewer tokens are billed

??? success "Answer: C"
    **Why C is right:** Streaming changes when the user sees output, not how long generation takes.

    **Why the others are wrong:**

    * **A:** Tokens are generated in sequence either way.
    * **B:** The overhead is negligible and perceived latency is far better.
    * **D:** Billing is identical for streamed and non-streamed responses.

---

<p class="qb-meta"><span class="qb-id">AI-010</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

While streaming, in which event does the final stop_reason arrive?

- **A.** message_delta
- **B.** message_start
- **C.** content_block_stop
- **D.** ping

??? success "Answer: A"
    **Why A is right:** message_delta carries top-level changes such as stop_reason and final usage, just before message_stop.

    **Why the others are wrong:**

    * **B:** message_start opens the message; stop_reason is not known yet.
    * **C:** That closes a single content block, not the message.
    * **D:** ping events are keep-alives with no message data.

---

<p class="qb-meta"><span class="qb-id">AI-011</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

During a streamed response, a tool call's arguments arrive as several input_json_delta events. How should the application obtain the tool input?

- **A.** Wait for a tool_result event that contains the full input
- **B.** Concatenate the partial_json strings and parse once at content_block_stop
- **C.** Ignore the deltas and read the input from message_start
- **D.** Parse each partial_json fragment as it arrives and merge the objects

??? success "Answer: B"
    **Why B is right:** Each delta is a fragment of JSON. Only the accumulated string is valid JSON.

    **Why the others are wrong:**

    * **A:** tool_result is something your application sends, not something it receives.
    * **C:** message_start arrives before any tool input is generated.
    * **D:** Individual fragments are not valid JSON on their own.

---

<p class="qb-meta"><span class="qb-id">AI-012</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A streaming request returns HTTP 200 and begins sending text. Thirty seconds later the stream ends with an error event. What does this show?

- **A.** The content already received is corrupted and must be discarded silently
- **B.** The request was invalid and should have been rejected with a 400
- **C.** Errors can occur mid-stream, so the client must cope
- **D.** The SDK has a bug, because a 200 response cannot contain an error

??? success "Answer: C"
    **Why C is right:** The status line is sent before generation finishes. Failures after that arrive as an error event in the stream.

    **Why the others are wrong:**

    * **A:** The partial content is not corrupt; the application decides whether to retry or show it.
    * **B:** An invalid request is rejected before the stream starts.
    * **D:** This is documented behaviour for streaming.

---

<p class="qb-meta"><span class="qb-id">AI-013</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service receives 400 invalid_request_error on some requests. A teammate proposes wrapping the call in a loop that retries up to five times. What is the best response?

- **A.** Agree, but add exponential backoff between the attempts
- **B.** Agree, but switch to a larger model on the last attempt
- **C.** Retry once only, because the second attempt usually succeeds
- **D.** Don't retry: the request is malformed, so fix it

??? success "Answer: D"
    **Why D is right:** Client errors of this type are deterministic. The same request will fail the same way.

    **Why the others are wrong:**

    * **A:** Backoff helps with overload, not with an invalid request.
    * **B:** The error is about the request format, not model capability.
    * **C:** Nothing changes between attempts, so it will not succeed.

---

<p class="qb-meta"><span class="qb-id">AI-014</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

During a traffic spike an application receives 429 rate_limit_error. What should it do first?

- **A.** Report an error to users, because 429 cannot be retried
- **B.** Create a new API key so that the limit is reset
- **C.** Retry immediately in a tight loop until a request succeeds
- **D.** Wait for the time given in the retry-after header, then retry

??? success "Answer: D"
    **Why D is right:** A 429 includes a retry-after header that says how long to wait.

    **Why the others are wrong:**

    * **A:** 429 is one of the retryable errors.
    * **B:** Limits apply to the organisation, not to a single key.
    * **C:** That makes the overload worse and prolongs the limit.

---

<p class="qb-meta"><span class="qb-id">AI-015</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What does a 529 overloaded_error indicate, and how should code respond?

- **A.** The model ID does not exist; correct it before trying again
- **B.** The API key is invalid; replace it before trying again
- **C.** The request body is too large; shrink it before trying again
- **D.** The API is temporarily overloaded; retry with exponential backoff

??? success "Answer: D"
    **Why D is right:** 529 is a transient server-side condition and is safe to retry after a delay.

    **Why the others are wrong:**

    * **A:** That is 404 not_found_error.
    * **B:** That is 401 authentication_error.
    * **C:** That is 413 request_too_large.

---

<p class="qb-meta"><span class="qb-id">AI-016</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A newly deployed service gets 401 authentication_error on every call, while the same code works on the developer's laptop. What is the most likely cause?

- **A.** The model is overloaded in the deployment's region
- **B.** The deployed service is sending requests too quickly
- **C.** The prompt contains content that the model refuses
- **D.** The API key is missing or wrong in that environment

??? success "Answer: D"
    **Why D is right:** 401 means the key was not supplied or is not valid. Environment differences are the usual reason.

    **Why the others are wrong:**

    * **A:** That would produce 529.
    * **B:** That would produce 429.
    * **C:** A refusal is a 200 response with a stop_reason, not a 401.

---

<p class="qb-meta"><span class="qb-id">AI-017</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A client uploads a very large PDF inline and the API returns 413. Which action addresses the cause?

- **A.** Reduce the request size, for example by splitting the document
- **B.** Switch to streaming so that the upload is sent in chunks
- **C.** Raise max_tokens so that the model can read the whole file
- **D.** Retry with exponential backoff until the request is accepted

??? success "Answer: A"
    **Why A is right:** 413 request_too_large means the body exceeds the size limit. Only a smaller request helps.

    **Why the others are wrong:**

    * **B:** Streaming affects the response, not the size of the request.
    * **C:** max_tokens limits output; it does not affect request size.
    * **D:** The request will be too large every time.

---

<p class="qb-meta"><span class="qb-id">AI-018</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A developer wraps every SDK call in a custom loop that retries five times on failure. During an outage, each user action produces far more API calls than expected. Why?

- **A.** The SDK retries by default, so layers multiply
- **B.** The API duplicates every request during an outage
- **C.** The SDK opens one connection per token it generates
- **D.** Each retry is billed as a batch of one hundred requests

??? success "Answer: A"
    **Why A is right:** The official SDKs retry transient errors twice by default. An outer loop multiplies that.

    **Why the others are wrong:**

    * **B:** The API does not duplicate requests.
    * **C:** Connections are not opened per token.
    * **D:** Retries are ordinary single requests.

---

<p class="qb-meta"><span class="qb-id">AI-019</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A non-streaming request that generates a very long document fails intermittently with timeouts and dropped connections. What is the recommended change?

- **A.** Use streaming, so that data flows continuously during generation
- **B.** Lower max_tokens to 256 so that responses return quickly
- **C.** Send the request twice in parallel and keep the faster one
- **D.** Set max_retries to zero so that the failure surfaces sooner

??? success "Answer: A"
    **Why A is right:** Long idle connections are fragile. Streaming keeps the connection active and is recommended for long outputs.

    **Why the others are wrong:**

    * **B:** That would truncate the document the task needs.
    * **C:** That doubles cost and still risks both timing out.
    * **D:** That removes recovery without fixing the cause.

---

<p class="qb-meta"><span class="qb-id">AI-020</span><span>Observability</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A customer reports a strange answer from yesterday. Which logged value is most useful when asking Anthropic support to investigate that specific call?

- **A.** The request ID returned in the response headers
- **B.** The local timestamp of the user's click
- **C.** The temperature value used for the request
- **D.** The first eight characters of the API key

??? success "Answer: A"
    **Why A is right:** Every response has a unique request-id that identifies the exact call.

    **Why the others are wrong:**

    * **B:** Timestamps are imprecise and not unique.
    * **C:** A parameter value does not identify a request.
    * **D:** Key fragments identify the account, not a single request.

---

<p class="qb-meta"><span class="qb-id">AI-021</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A dashboard shows average usage at 60% of the requests-per-minute limit, yet the application still receives occasional 429 errors at the top of each hour when a scheduled job starts. Why?

- **A.** Scheduled jobs are counted twice against the limit
- **B.** A token bucket lets a sudden burst exceed capacity
- **C.** Rate limits are reset to zero at the start of each hour
- **D.** 429 is returned at random to keep usage below 50%

??? success "Answer: B"
    **Why B is right:** The limit is not a simple per-minute counter. Short bursts can drain the bucket even when the average is low.

    **Why the others are wrong:**

    * **A:** Requests are counted once regardless of origin.
    * **C:** There is no hourly reset that lowers capacity.
    * **D:** Limits are deterministic, not random.

---

<p class="qb-meta"><span class="qb-id">AI-022</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application with a large, repeated system prompt keeps hitting its input-tokens-per-minute limit. Which change raises effective throughput without asking for higher limits?

- **A.** Raise the temperature, since it reduces the tokens processed
- **B.** Cache the prompt, since cached reads are mostly exempt
- **C.** Lower max_tokens, since it is counted against the input limit
- **D.** Enable streaming, since streamed tokens are not rate limited

??? success "Answer: B"
    **Why B is right:** On most current models cache_read_input_tokens are excluded from ITPM, so caching increases throughput.

    **Why the others are wrong:**

    * **A:** Temperature does not change token counts.
    * **C:** max_tokens concerns output and is not counted against input limits.
    * **D:** Streaming does not change rate-limit accounting.

---

<p class="qb-meta"><span class="qb-id">AI-023</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Before sending a request that includes a long document, a service wants to know whether it will fit and which model to route it to. What is the best approach?

- **A.** Divide the character count by ten to estimate the tokens
- **B.** Set max_tokens to zero to get a free dry run
- **C.** Call the token counting endpoint before sending
- **D.** Send the request and read usage from the error response

??? success "Answer: C"
    **Why C is right:** count_tokens accepts the same system, messages and tools as a real request and returns the input token count at no charge.

    **Why the others are wrong:**

    * **A:** A crude ratio is unreliable, especially with tools, images or non-English text.
    * **B:** max_tokens must be positive; this is not a dry-run mechanism.
    * **D:** That wastes a call and may fail or cost money.

---

<p class="qb-meta"><span class="qb-id">AI-024</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which statement about the token counting endpoint is correct?

- **A.** It is billed at the input rate and shares the Messages rate limit
- **B.** It returns both the input tokens and the predicted output tokens
- **C.** It only supports plain text and rejects tools or images
- **D.** It is free, separately limited, and gives an estimate

??? success "Answer: D"
    **Why D is right:** Counting does not generate output, is not billed, and is limited separately from message creation.

    **Why the others are wrong:**

    * **A:** It is free and separately limited.
    * **B:** Output length is not known before generation.
    * **C:** It accepts the same structured inputs as a message request.

---

<p class="qb-meta"><span class="qb-id">AI-025</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team submits 5,000 requests in one message batch and reads the results file line by line, assuming line N answers request N. Some answers end up attached to the wrong records. What is the fix?

- **A.** Sort the results by their completion timestamp
- **B.** Match each result to its request using custom_id
- **C.** Add a sequence number to each prompt and ask Claude to repeat it
- **D.** Submit the requests in smaller batches of exactly 100

??? success "Answer: B"
    **Why B is right:** Batch results are not guaranteed to be in submission order. custom_id exists for matching.

    **Why the others are wrong:**

    * **A:** Completion time does not reflect submission order.
    * **C:** Fragile and unnecessary when custom_id is provided.
    * **D:** Batch size does not make the order reliable.

---

<p class="qb-meta"><span class="qb-id">AI-026</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Every night a company summarises 60,000 product reviews. Results are needed by the next morning. Which approach is most cost-effective?

- **A.** Synchronous calls using the most capable model available
- **B.** The Message Batches API, since nobody is waiting on each result
- **C.** One request containing all 60,000 reviews in a single prompt
- **D.** Synchronous calls with streaming enabled for every review

??? success "Answer: B"
    **Why B is right:** Batches are asynchronous and half the price, which suits large offline jobs.

    **Why the others are wrong:**

    * **A:** That maximises cost with no stated quality need.
    * **C:** It would exceed limits and give poor per-review results.
    * **D:** Streaming helps a waiting user, not an overnight job.

---

<p class="qb-meta"><span class="qb-id">AI-027</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

To cut costs, a product manager suggests sending live customer chat messages through the Message Batches API. What is the main problem?

- **A.** Batches can only be submitted once per day
- **B.** Batches do not support system prompts or tools
- **C.** Batches are asynchronous and may take hours to finish
- **D.** Batches cost more per token than synchronous calls

??? success "Answer: C"
    **Why C is right:** A batch has no latency guarantee beyond finishing within its processing window.

    **Why the others are wrong:**

    * **A:** There is no such restriction.
    * **B:** Batch requests accept normal Messages parameters.
    * **D:** They cost less, about half.

---

<p class="qb-meta"><span class="qb-id">AI-028</span><span>Errors</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO errors are appropriate to retry automatically with backoff? (Select TWO.)

- **A.** 400 invalid_request_error
- **B.** 401 authentication_error
- **C.** 429 rate_limit_error
- **D.** 529 overloaded_error
- **E.** 404 not_found_error

??? success "Answer: C and D"
    **Why C is right:** Rate limiting is temporary; wait and retry.

    **Why D is right:** Overload is temporary; back off and retry.

    **Why the others are wrong:**

    * **A:** The request is malformed and will fail again.
    * **B:** The key is wrong; retrying cannot fix it.
    * **E:** The resource or model does not exist; retrying cannot fix it.

---

<p class="qb-meta"><span class="qb-id">AI-029</span><span>Request shape</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about the Messages API are correct? (Select TWO.)

- **A.** The system prompt is supplied as a top-level parameter
- **B.** The application must resend prior turns to continue a conversation
- **C.** A 200 status guarantees that the answer is complete
- **D.** max_tokens sets the minimum length of the response
- **E.** The API stores each conversation for 24 hours by default

??? success "Answer: A and B"
    **Why A is right:** system is not a role inside messages.

    **Why B is right:** The API is stateless.

    **Why the others are wrong:**

    * **C:** stop_reason may still indicate truncation.
    * **D:** It is an upper limit on output.
    * **E:** No conversation state is kept between calls.

---

<p class="qb-meta"><span class="qb-id">AI-030</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer sets max_tokens to 4,000 hoping for longer, more detailed answers, but replies remain short. Why?

- **A.** The value is ignored unless streaming is enabled
- **B.** Values above 1,024 are silently reduced by the API
- **C.** max_tokens is a cap; ask for length in the prompt
- **D.** max_tokens applies to the input rather than the output

??? success "Answer: C"
    **Why C is right:** The parameter caps output. It does not instruct the model to write more.

    **Why the others are wrong:**

    * **A:** It applies to streamed and non-streamed responses alike.
    * **B:** Models support much larger outputs.
    * **D:** It limits output tokens.

---

<p class="qb-meta"><span class="qb-id">AI-031</span><span>Conversation history</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In an agent loop, a developer appends only the text of each assistant response to the history and discards the other blocks. The next request fails with an error about a tool_result. Why?

- **A.** The history exceeded the limit of ten messages per request
- **B.** Text blocks must be removed from history before tool results
- **C.** The matching tool_use block is missing from the history
- **D.** tool_result blocks are only valid in the system parameter

??? success "Answer: C"
    **Why C is right:** A tool_result must follow an assistant message that contains the matching tool_use block.

    **Why the others are wrong:**

    * **A:** There is no such ten-message limit.
    * **B:** Text blocks are allowed alongside tool_use blocks.
    * **D:** They belong in a user message.

---

<p class="qb-meta"><span class="qb-id">AI-032</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A pipeline always performs the same three steps: translate a document, summarise it, then format the summary as HTML. A teammate proposes an autonomous agent with tools for each step. What is the better design?

- **A.** A multi-agent system with one agent for each of the steps
- **B.** One very long prompt that asks for all three results at once
- **C.** A single agent with a higher turn limit to explore options
- **D.** A prompt chain run by application code, with a check between steps

??? success "Answer: D"
    **Why D is right:** When steps are fixed and known, a workflow is cheaper, faster and more predictable than an agent.

    **Why the others are wrong:**

    * **A:** Extra coordination cost with no benefit for a fixed sequence.
    * **B:** Harder to validate and debug than separate steps.
    * **C:** Autonomy adds unpredictability where none is needed.

---

<p class="qb-meta"><span class="qb-id">AI-033</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A help desk receives billing questions, technical faults and sales enquiries. Each type needs different instructions and tools. Which pattern fits best?

- **A.** Evaluator-optimiser: draft a reply, then critique and revise it
- **B.** A single general prompt that lists every rule for all types
- **C.** Parallelisation: send each message to all three handlers
- **D.** Routing: classify each message, then send it to a specialised prompt

??? success "Answer: D"
    **Why D is right:** Routing separates concerns, so each path can be tuned without harming the others.

    **Why the others are wrong:**

    * **A:** That improves one output; it does not pick a path.
    * **B:** Rules for different types interfere with one another.
    * **C:** Wasteful, and the answers then need reconciling.

---

<p class="qb-meta"><span class="qb-id">AI-034</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An internal assistant must answer questions using the company's 4,000-page policy library, which changes monthly. Which design is most appropriate?

- **A.** Rely on the model's training data to know the policies
- **B.** Raise the temperature so that the model recalls more detail
- **C.** Paste the full library into the system prompt on every request
- **D.** Retrieve relevant passages and add them to the prompt

??? success "Answer: D"
    **Why D is right:** Retrieval supplies current, relevant content without sending everything every time.

    **Why the others are wrong:**

    * **A:** The model has never seen private, changing documents.
    * **B:** Temperature does not add knowledge.
    * **C:** Likely too large, slow and costly.

---

<p class="qb-meta"><span class="qb-id">AI-035</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A web chat application needs multi-turn conversations. Where should conversation history be kept?

- **A.** In a server-side store keyed by the application's own session ID
- **B.** Nowhere, since the model retains recent conversations
- **C.** In the system prompt, appended to after every turn
- **D.** In the Claude API, retrieved with the previous message ID

??? success "Answer: A"
    **Why A is right:** The application owns state. A backend store lets it reload and resend history securely.

    **Why the others are wrong:**

    * **B:** The model retains nothing between calls.
    * **C:** History belongs in messages; rewriting the system prompt also defeats caching.
    * **D:** The API does not store conversations for retrieval.

---

<p class="qb-meta"><span class="qb-id">AI-036</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

Two browser tabs for the same user send messages to the same conversation at almost the same moment. Afterwards the stored history has turns out of order and one reply is missing. What should be added?

- **A.** Per-session locking when the history is updated
- **B.** A lower temperature so that both replies are identical
- **C.** A second API key so that the two tabs do not collide
- **D.** A longer max_tokens so that neither reply is dropped

??? success "Answer: A"
    **Why A is right:** It is an ordinary concurrent-write problem on shared state, solved with ordinary concurrency control.

    **Why the others are wrong:**

    * **B:** Sampling settings cannot fix a race condition.
    * **C:** Keys are unrelated to writes to your own store.
    * **D:** The reply was lost in storage, not truncated.

---

<p class="qb-meta"><span class="qb-id">AI-037</span><span>Architecture</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A mobile team wants the app to call the Claude API directly to avoid an extra network hop. What is the main objection?

- **A.** The API key would ship in the app and be extractable
- **B.** Direct calls are billed at a higher rate per token
- **C.** The Claude API refuses requests from mobile devices
- **D.** Mobile networks cannot carry server-sent events

??? success "Answer: A"
    **Why A is right:** Client-side keys cannot be kept secret. Calls should go through a backend that holds the key.

    **Why the others are wrong:**

    * **B:** Pricing does not depend on where the call originates.
    * **C:** The API does not identify device types.
    * **D:** They can; this is not the issue.

---

<p class="qb-meta"><span class="qb-id">AI-038</span><span>Schema design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An extraction schema marks delivery_date as a required string. For emails that contain no date, the model returns a plausible but invented date. What is the best schema change?

- **A.** Make the field nullable, returning null when absent
- **B.** Mark the field required in two places for emphasis
- **C.** Add a regular expression that enforces a date format
- **D.** Lower the temperature so that the date is deterministic

??? success "Answer: A"
    **Why A is right:** A required field with no source value pushes the model to invent one.

    **Why the others are wrong:**

    * **B:** Emphasis does not create missing information.
    * **C:** The format was fine; the value was fabricated.
    * **D:** A deterministic invented date is still invented.

---

<p class="qb-meta"><span class="qb-id">AI-039</span><span>Schema design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A ticket classifier uses an enum of five categories. Unusual tickets are being forced into badly fitting categories. Which change helps most?

- **A.** Remove the enum and accept any free-text category
- **B.** Add an "other" value, with a short free-text field for the detail
- **C.** Add twenty more categories to cover every case
- **D.** Send each ticket three times and take the majority label

??? success "Answer: B"
    **Why B is right:** An escape value stops the model from being forced into a wrong label.

    **Why the others are wrong:**

    * **A:** That loses the consistency the enum provides.
    * **C:** Large enums are harder to choose from and never cover everything.
    * **D:** Voting between wrong labels does not produce a right one.

---

<p class="qb-meta"><span class="qb-id">AI-040</span><span>Validation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An invoice extractor uses structured outputs, so every response matches the schema. Finance finds invoices where the line items do not add up to the stated total. What is missing?

- **A.** A stricter schema with additionalProperties set to false
- **B.** A semantic check in code that lines sum to the total
- **C.** A higher max_tokens value so that totals are not truncated
- **D.** A system prompt reminder that totals must be accurate

??? success "Answer: B"
    **Why B is right:** A schema guarantees structure, not correctness. Business rules need their own validation.

    **Why the others are wrong:**

    * **A:** The structure was already valid; the values were wrong.
    * **C:** Nothing was truncated.
    * **D:** A reminder is not verification.

---

<p class="qb-meta"><span class="qb-id">AI-041</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

After a timeout, a workflow retried a step, and a customer was refunded twice. Which design principle prevents this?

- **A.** Increase the timeout to ten minutes for every call
- **B.** Make the side effect idempotent, using an idempotency key
- **C.** Ask the model to remember which refunds it has issued
- **D.** Disable all retries across the whole application

??? success "Answer: B"
    **Why B is right:** With an idempotency key, a repeated attempt is recognised and not executed again.

    **Why the others are wrong:**

    * **A:** Timeouts can still occur; duplicates remain possible.
    * **C:** Model memory is not a reliable transaction record.
    * **D:** That sacrifices resilience; the issue is the repeated side effect.

---

<p class="qb-meta"><span class="qb-id">AI-042</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

The Claude API has been returning errors for several minutes. Every user request waits through multiple retries and then fails. What should the application do instead?

- **A.** Return an empty reply so that users don't see any error
- **B.** Stop calling after repeated failures and fall back
- **C.** Remove the timeout so that requests can wait as long as needed
- **D.** Increase the retry count so that requests eventually pass

??? success "Answer: B"
    **Why B is right:** A circuit breaker with graceful degradation avoids piling up slow, doomed requests.

    **Why the others are wrong:**

    * **A:** Silent empty answers hide the failure and confuse users.
    * **C:** Hanging requests exhaust resources and frustrate users.
    * **D:** More retries deepen the pile-up during an outage.

---

<p class="qb-meta"><span class="qb-id">AI-043</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A marketing campaign sends bursts of thousands of requests within a few seconds, causing many 429 errors, although total daily volume is well within limits. Which design smooths this out?

- **A.** Raise max_tokens so that each request does more work
- **B.** Open more connections so that the burst finishes sooner
- **C.** Put requests on a queue and process them at a controlled rate
- **D.** Disable SDK retries so that failures return faster

??? success "Answer: C"
    **Why C is right:** A queue absorbs bursts and feeds the API at a steady pace.

    **Why the others are wrong:**

    * **A:** It does not reduce the request rate.
    * **B:** That intensifies the burst.
    * **D:** Requests would simply fail instead of completing.

---

<p class="qb-meta"><span class="qb-id">AI-044</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A model ID is hard-coded in forty source files. A newer model must now be adopted. Which practice would have made this a small change?

- **A.** Letting each developer choose the model on their machine
- **B.** Storing the model ID inside the system prompt text
- **C.** Keeping the model ID in configuration, read by all the call sites
- **D.** Using a different model ID in every file for flexibility

??? success "Answer: C"
    **Why C is right:** Configuration lets the model change without editing code across the codebase.

    **Why the others are wrong:**

    * **A:** Uncontrolled variation between environments.
    * **B:** The prompt does not select the model.
    * **D:** That makes the system even harder to manage.

---

<p class="qb-meta"><span class="qb-id">AI-045</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Production behaviour changed slightly overnight with no deployment. The service uses a model alias that always points to the newest version. What is the recommended practice?

- **A.** Keep the alias and add more few-shot examples each week
- **B.** Keep the alias and lower the temperature to stabilise output
- **C.** Pin a specific model version and upgrade deliberately after testing
- **D.** Switch aliases every day to average out the differences

??? success "Answer: C"
    **Why C is right:** A moving alias can change behaviour without warning. Pinning makes upgrades a tested release.

    **Why the others are wrong:**

    * **A:** Examples do not prevent the underlying model from changing.
    * **B:** Sampling settings do not prevent a model change.
    * **D:** That adds variation rather than removing it.

---

<p class="qb-meta"><span class="qb-id">AI-046</span><span>Life cycle</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A developer edits one paragraph of a production system prompt and deploys it directly. The next day, a previously working feature is broken. Which process was missing?

- **A.** A longer system prompt with more capital letters
- **B.** A rule that only senior developers may edit prompts
- **C.** A higher max_tokens setting in production
- **D.** Versioned prompts and evals before release

??? success "Answer: D"
    **Why D is right:** A prompt change is a behaviour change. Regression evals catch breakage before users do.

    **Why the others are wrong:**

    * **A:** Emphasis is not a release process.
    * **B:** Seniority does not replace testing.
    * **C:** Unrelated to the regression.

---

<p class="qb-meta"><span class="qb-id">AI-047</span><span>Life cycle</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

After launch, which set of measurements best shows the health of a Claude-powered feature?

- **A.** Error rates, latency, token cost, validation failures
- **B.** The average temperature across all the requests
- **C.** The count of developers who can access the API key
- **D.** The number of lines in the system prompt each week

??? success "Answer: A"
    **Why A is right:** Together these cover reliability, speed, spend and output quality.

    **Why the others are wrong:**

    * **B:** A configuration value, not an outcome.
    * **C:** An access-control fact, not a health metric.
    * **D:** Prompt length says nothing about behaviour in production.

---

<p class="qb-meta"><span class="qb-id">AI-048</span><span>Access control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a multi-tenant application, a user of one company receives an answer that quotes another company's document. Where is the flaw?

- **A.** The temperature allowed the model to be creative
- **B.** The system prompt did not forbid sharing documents
- **C.** Retrieval was not scoped to the authenticated user's tenant
- **D.** The model's context window was too large

??? success "Answer: C"
    **Why C is right:** Isolation must be enforced when data is fetched, before anything reaches the prompt.

    **Why the others are wrong:**

    * **A:** The other tenant's content was in the context; this is not creativity.
    * **B:** A prompt rule cannot undo data that was already supplied.
    * **D:** Window size does not select which documents are retrieved.

---

<p class="qb-meta"><span class="qb-id">AI-049</span><span>Configuration</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO practices are appropriate for managing configuration of a Claude application? (Select TWO.)

- **A.** Embed prompts as string literals spread across the modules
- **B.** Load the API key from a secret manager or environment variable
- **C.** Use separate keys and settings for development and production
- **D.** Commit the API key in a private repository for convenience
- **E.** Share one key across all teams to simplify rotation

??? success "Answer: B and C"
    **Why B is right:** Keeps the key out of code and repositories.

    **Why C is right:** Limits blast radius and separates usage.

    **Why the others are wrong:**

    * **A:** Scattered prompts are hard to version, review and test.
    * **D:** Private repositories still leak; keys do not belong in source control.
    * **E:** A shared key widens exposure and hides who used what.

---

<p class="qb-meta"><span class="qb-id">AI-050</span><span>Sync or batch</span><span>Select TWO</span><span title="Difficulty">●○○</span></p>

A team is deciding between synchronous calls and the Message Batches API for a new workload. Which TWO facts are most relevant to the decision? (Select TWO.)

- **A.** Whether the developers prefer Python or TypeScript
- **B.** Whether the system prompt uses XML tags or Markdown
- **C.** Whether the prompts are written in British or American English
- **D.** Whether a user or blocking process is waiting on each result
- **E.** Whether a delay of up to several hours is acceptable

??? success "Answer: D and E"
    **Why D is right:** Batches are asynchronous, so waiting users rule them out.

    **Why E is right:** Batch completion time is not immediate.

    **Why the others are wrong:**

    * **A:** Both SDKs support both modes.
    * **B:** Prompt formatting does not affect the choice.
    * **C:** Spelling variety has no bearing on the choice.

---

<p class="qb-meta"><span class="qb-id">AI-051</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A sponsor asks a developer to "add AI to the returns process". What should the developer do first?

- **A.** Write a long system prompt covering every case
- **B.** Build a multi-agent prototype to show the sponsor
- **C.** Choose the most capable model that is available
- **D.** Clarify the goal and write measurable requirements

??? success "Answer: D"
    **Why D is right:** An ambiguous goal cannot be designed or tested. Requirements come before model or pattern choices.

    **Why the others are wrong:**

    * **A:** There is nothing agreed yet for the prompt to implement.
    * **B:** Building before the goal is clear risks solving the wrong problem.
    * **C:** Model choice depends on requirements that don't exist yet.

---

<p class="qb-meta"><span class="qb-id">AI-052</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which of these is an infrastructure (non-functional) requirement?

- **A.** The system must draft a reply for an agent to approve
- **B.** The system must extract the invoice number and total
- **C.** The system must classify tickets into six categories
- **D.** Responses must begin within two seconds at peak load

??? success "Answer: D"
    **Why D is right:** It describes how well the system must perform, not what it does.

    **Why the others are wrong:**

    * **A:** That is a function the system performs.
    * **B:** That is a function the system performs.
    * **C:** That is a function the system performs.

---

<p class="qb-meta"><span class="qb-id">AI-053</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A requirement states: "Customer data must not leave the company's cloud region." Which design decision does this affect most directly?

- **A.** Whether responses are parsed with Pydantic
- **B.** Whether examples in the prompt use XML tags
- **C.** Whether the temperature is set near 0 or 1
- **D.** Which platform and deployment option is used

??? success "Answer: D"
    **Why D is right:** Data-residency constraints determine where and through which provider the model is called.

    **Why the others are wrong:**

    * **A:** Validation tooling is unrelated to data location.
    * **B:** Prompt formatting does not control where data is processed.
    * **C:** Sampling settings are unrelated to data location.

---

<p class="qb-meta"><span class="qb-id">AI-054</span><span>Systems life cycle</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An application has run unchanged for a year. One morning every request fails with a 404 naming the model. Nothing was deployed. What life-cycle activity was neglected?

- **A.** Maintenance: tracking model deprecations
- **B.** Testing: the unit tests should have been stricter
- **C.** Development: the code should have used raw HTTP
- **D.** Design: the system should have used more agents

??? success "Answer: A"
    **Why A is right:** Models are retired on a schedule. Operating an LLM system includes watching for that and migrating in time.

    **Why the others are wrong:**

    * **B:** Unit tests cannot keep a retired model available.
    * **C:** The SDK is not the cause of a retired model.
    * **D:** Agent count has nothing to do with a retired model.

---

<p class="qb-meta"><span class="qb-id">AI-055</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is the relationship between an official Claude SDK and the REST API?

- **A.** The SDK is a wrapper over the same REST API
- **B.** The SDK is required; raw HTTP calls are rejected
- **C.** The SDK uses a separate, faster private protocol
- **D.** The SDK runs the model locally on your machine

??? success "Answer: A"
    **Why A is right:** SDKs add typing, retries, timeouts and stream handling on top of the same HTTP endpoints.

    **Why the others are wrong:**

    * **B:** Any HTTP client can call the API.
    * **C:** It calls the same public HTTP API.
    * **D:** Models run on the provider's servers.

---

<p class="qb-meta"><span class="qb-id">AI-056</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer builds a JSON request body by joining strings and inserting the user's text directly. Requests fail whenever the text contains a quotation mark. What is the correct fix?

- **A.** Wrap the user's text in a second pair of quotes
- **B.** Serialise the object with a JSON library
- **C.** Replace every quotation mark with a blank space
- **D.** Ask users not to type quotation marks in the box

??? success "Answer: B"
    **Why B is right:** A serialiser escapes special characters correctly. String concatenation does not.

    **Why the others are wrong:**

    * **A:** Adds more unescaped quotes and makes the JSON worse.
    * **C:** Corrupts the user's text and misses other special characters.
    * **D:** Unreasonable, and other characters will also break it.

---

<p class="qb-meta"><span class="qb-id">AI-057</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A script summarises 4,000 documents by launching all requests at once with asyncio.gather. Most fail with 429 errors. A user is waiting for the results. What is the best change?

- **A.** Remove the awaits so that requests return sooner
- **B.** Switch every call to the synchronous client instead
- **C.** Limit concurrency with a semaphore or worker pool
- **D.** Launch the same requests twice to improve the odds

??? success "Answer: C"
    **Why C is right:** Bounded concurrency keeps throughput high while staying inside rate limits.

    **Why the others are wrong:**

    * **A:** Without awaiting, results are never collected.
    * **B:** Sequential calls would be very slow for a waiting user.
    * **D:** Doubles the load that caused the errors.

---

<p class="qb-meta"><span class="qb-id">AI-058</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A coding agent produced a change that passes the existing tests. What should happen before it is merged?

- **A.** A person reviews the diff, edge cases included
- **B.** The change is merged and reviewed after the release
- **C.** Nothing further; passing tests are sufficient proof
- **D.** The same session reviews and approves its own change

??? success "Answer: A"
    **Why A is right:** Passing tests show only what the tests cover. Review is still needed for generated code.

    **Why the others are wrong:**

    * **B:** Review after release finds problems too late.
    * **C:** Tests rarely cover every edge case or security concern.
    * **D:** A fresh reviewer avoids the author's blind spots.

---

<p class="qb-meta"><span class="qb-id">AI-059</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants an agent to migrate 180 files from one logging library to another. Which approach is most likely to succeed?

- **A.** Let several agents edit the same files in parallel
- **B.** Plan first, then migrate in small verified steps
- **C.** Ask for all 180 files to be rewritten in one prompt
- **D.** Skip the tests until every file has been converted

??? success "Answer: B"
    **Why B is right:** Large refactors need a plan, a safety net of tests, and incremental verification.

    **Why the others are wrong:**

    * **A:** Conflicting edits on shared files cause breakage.
    * **C:** Overloads context and gives no checkpoint when something breaks.
    * **D:** Errors compound and become hard to locate.

---

<p class="qb-meta"><span class="qb-id">AI-060</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

During code review, a reviewer notices that generated code imports a package nobody on the team has heard of. What is the right reaction?

- **A.** Install it at once, since the model recommended it
- **B.** Verify the package exists and is trustworthy
- **C.** Assume it is a standard library the team forgot
- **D.** Delete the import line and merge the remainder

??? success "Answer: B"
    **Why B is right:** Generated code can reference non-existent or unsuitable packages. Dependencies must be checked.

    **Why the others are wrong:**

    * **A:** A recommendation is not verification.
    * **C:** An assumption, not a check.
    * **D:** The code probably depends on it and would break.

---

<p class="qb-meta"><span class="qb-id">AI-061</span><span>Technical fundamentals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Why does the Messages API use server-sent events for streaming, and not WebSockets?

- **A.** WebSockets cannot carry text, only binary frames
- **B.** Token streaming only needs one-way delivery
- **C.** WebSockets are limited to a hundred messages
- **D.** Server-sent events let the client send mid-stream

??? success "Answer: B"
    **Why B is right:** SSE provides one-way streaming over ordinary HTTP. WebSockets are for two-way communication.

    **Why the others are wrong:**

    * **A:** WebSockets carry text as well as binary.
    * **C:** There is no such limit.
    * **D:** SSE is one-way; the client does not send on it.

---

<p class="qb-meta"><span class="qb-id">AI-062</span><span>Technical fundamentals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A browser-based voice assistant needs the client and the team's backend to exchange audio and control messages continuously in both directions. Which transport suits that link?

- **A.** A series of separate GET requests
- **B.** A nightly batch upload
- **C.** Server-sent events alone
- **D.** A WebSocket connection

??? success "Answer: D"
    **Why D is right:** WebSockets keep one connection open over which both sides can send at any time.

    **Why the others are wrong:**

    * **A:** Polling is slow and one-directional per request.
    * **B:** A batch has no real-time interaction.
    * **C:** SSE only carries data from server to client.

---

<p class="qb-meta"><span class="qb-id">AI-063</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A prompt gives excellent results in the Claude chat app. Sent unchanged through the Messages API, results are noticeably different. What is the most likely explanation?

- **A.** The API ignores the first message of each request
- **B.** The API always serves an older and weaker model
- **C.** The API adds no product system prompt, tools or memory
- **D.** The API runs every request at temperature zero

??? success "Answer: C"
    **Why C is right:** Each surface assembles context differently. Through the API, Claude sees only what the request contains.

    **Why the others are wrong:**

    * **A:** Every message sent is used.
    * **B:** The model is whichever one the request names.
    * **D:** The default is not zero unless set.

---

<p class="qb-meta"><span class="qb-id">AI-064</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In Claude Code, a team writes "Never run database migrations" in CLAUDE.md. A migration is later run during a session. Why was the instruction not a guarantee?

- **A.** CLAUDE.md is limited to twenty lines of content
- **B.** CLAUDE.md applies to Python files and no others
- **C.** CLAUDE.md is guidance, not an enforced control
- **D.** CLAUDE.md is only loaded on the first day of use

??? success "Answer: C"
    **Why C is right:** Instructions are advisory. Enforcement needs a permission rule or a hook.

    **Why the others are wrong:**

    * **A:** There is no such limit.
    * **B:** It is not restricted by language.
    * **D:** It is loaded in every session.

---

<p class="qb-meta"><span class="qb-id">AI-065</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer has spent three hours in one Claude Code session on several unrelated tasks. Answers are getting worse and earlier instructions are being forgotten. What is the best practice?

- **A.** Keep going and repeat each instruction in capitals
- **B.** Paste the whole transcript back in as a reminder
- **C.** Start a fresh session per task, carrying a short summary
- **D.** Raise the max_tokens value for the next reply

??? success "Answer: C"
    **Why C is right:** Unrelated history pollutes the context. Clean sessions with a deliberate hand-over work better.

    **Why the others are wrong:**

    * **A:** Adds more noise to an already crowded context.
    * **B:** Makes the context problem worse.
    * **D:** Output size is not the issue.

---

<p class="qb-meta"><span class="qb-id">AI-066</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants every developer to have the same set of Claude Code skills, commands and hooks for a project. Which approach fits best?

- **A.** Have each developer recreate them from memory
- **B.** Email the files and ask each person to copy them
- **C.** Describe them in the README without any files
- **D.** Package them as a plugin enabled in the project settings

??? success "Answer: D"
    **Why D is right:** A plugin bundles these components, and project settings share it with everyone who works in the repository.

    **Why the others are wrong:**

    * **A:** Guarantees inconsistency.
    * **B:** Manual copies drift apart and are never updated together.
    * **C:** A description does not install anything.

---

<p class="qb-meta"><span class="qb-id">AI-067</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Before installing a third-party Claude Code plugin, what is the most important consideration?

- **A.** It should contain more commands than other plugins
- **B.** It should be the newest plugin in the marketplace
- **C.** Its name should be shorter than twelve characters
- **D.** It can run code, so its source must be trusted

??? success "Answer: D"
    **Why D is right:** Plugins can execute code and extend what the agent can do. Treat them like any other dependency.

    **Why the others are wrong:**

    * **A:** Size is not a measure of trust or quality.
    * **B:** Newness says nothing about safety.
    * **C:** Name length is irrelevant.

---

<p class="qb-meta"><span class="qb-id">AI-068</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Output quality dropped last Tuesday. The team cannot tell which prompt text was in use that day, because prompts are edited directly in a dashboard. What practice is missing?

- **A.** A larger context window for the affected model
- **B.** A second dashboard with a different colour scheme
- **C.** A rule that prompts may be edited only on Fridays
- **D.** Prompt versioning, logged on each request

??? success "Answer: D"
    **Why D is right:** Versioned prompts plus logging make it possible to connect a behaviour change to a specific prompt.

    **Why the others are wrong:**

    * **A:** Window size does not record prompt history.
    * **B:** Cosmetic and unrelated.
    * **C:** Scheduling edits does not record what changed.

---

<p class="qb-meta"><span class="qb-id">AI-069</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In Claude Code, which file should hold a personal permission override that must not be shared with the team?

- **A.** .claude/settings.local.json
- **B.** CLAUDE.md in the project root
- **C.** .mcp.json in the project root
- **D.** .claude/settings.json

??? success "Answer: A"
    **Why A is right:** The local settings file is for personal overrides and is not committed.

    **Why the others are wrong:**

    * **B:** It holds instructions, not permission settings, and is shared.
    * **C:** It lists shared MCP servers.
    * **D:** That file is committed and shared with the team.

---

<p class="qb-meta"><span class="qb-id">AI-070</span><span>Platforms</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An application is moved from the direct Claude API to a cloud vendor's platform. A beta feature it depends on stops working. What should have been checked first?

- **A.** Whether that feature is available on the chosen platform
- **B.** Whether the cloud vendor uses a faster network
- **C.** Whether the team's laptops were recently updated
- **D.** Whether the prompts were translated to English

??? success "Answer: A"
    **Why A is right:** Feature availability, model identifiers and authentication differ between platforms.

    **Why the others are wrong:**

    * **B:** Network speed does not add a missing feature.
    * **C:** Client machines are unrelated.
    * **D:** Language is unrelated to feature availability.

---

<p class="qb-meta"><span class="qb-id">AI-071</span><span>Requirements</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO are infrastructure (non-functional) requirements? (Select TWO.)

- **A.** The service must flag invoices with missing totals
- **B.** The service must handle 50 requests per second at peak
- **C.** The service must produce a summary for each ticket
- **D.** Prompts and outputs must be retained for no more than 30 days
- **E.** The service must translate documents into French

??? success "Answer: B and D"
    **Why B is right:** A throughput constraint.

    **Why D is right:** A data-retention constraint.

    **Why the others are wrong:**

    * **A:** A function.
    * **C:** A function.
    * **E:** A function.

---
