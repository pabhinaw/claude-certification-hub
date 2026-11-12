# Question Bank · Applications & Integration

**76 original questions** (5 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Access control · Application design · Architecture · Batches · Choosing a pattern · Configuration · Conversation history · Errors · Life cycle · Observability · Platforms · Rate limits · Reliability · Request shape · Requirements · Response shape · SDK behaviour · SDLC integration · Schema design · Session handling · Software engineering · Statelessness · Stop reasons · Streaming · Sync or batch · Systems life cycle · Technical fundamentals · Token counting · Validation

---

<p class="qb-meta"><span class="qb-id">AI-001</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer adds {"role": "system", "content": "You are a helpful travel assistant."} as the first item in the messages list and receives a 400 error. What is the correct fix?

- **A.** Move the text to the top-level system parameter of the request
- **B.** Place the system message last so that it takes priority
- **C.** Rename the role to "developer" and send the request again
- **D.** Send the system text in a custom HTTP request header

??? success "Answer: A"
    **Why A is right:** System prompts are a top-level parameter. The messages list only accepts user and assistant roles.

    **Why the others are wrong:**

    * **B:** Position does not matter; the role itself is not accepted.
    * **C:** There is no developer role in the Messages API.
    * **D:** Headers carry authentication and versioning, not prompt content.

---

<p class="qb-meta"><span class="qb-id">AI-002</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Which set of fields is required in every Messages API request?

- **A.** model, max_tokens and messages
- **B.** model, max_tokens and stream
- **C.** model, messages and temperature
- **D.** model, system and messages

??? success "Answer: A"
    **Why A is right:** These three are mandatory. Everything else, including system and temperature, is optional.

    **Why the others are wrong:**

    * **B:** stream is optional, and messages is missing.
    * **C:** temperature is optional, and max_tokens is missing.
    * **D:** system is optional, and max_tokens is missing.

---

<p class="qb-meta"><span class="qb-id">AI-003</span><span>Statelessness</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A chatbot answers the first question well, but when the user follows up with "and what about the second one?", Claude has no idea what "the second one" refers to. The code sends only the newest user message on each call. What is the cause?

- **A.** The API is stateless, so earlier turns must be resent
- **B.** The model's context window was exceeded by the first answer
- **C.** The temperature is too low for the model to recall context
- **D.** The session expired because the two calls were too far apart

??? success "Answer: A"
    **Why A is right:** Nothing is remembered between calls. The full history must be included in messages each time.

    **Why the others are wrong:**

    * **B:** A short exchange is nowhere near the window; the history was simply not sent.
    * **C:** Temperature affects sampling, not memory.
    * **D:** There is no server-side session to expire.

---

<p class="qb-meta"><span class="qb-id">AI-004</span><span>Response shape</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

This line works in testing but raises an exception in production after tools are added to the request:

```python
answer = response.content[0].text
```

What is the most likely reason?

- **A.** The response body is returned as a string once tools are enabled
- **B.** The first block is sometimes tool_use, without text
- **C.** Tool-enabled responses place the text in response.completion
- **D.** The SDK needs an additional await when tools are present

??? success "Answer: B"
    **Why B is right:** content is a list of typed blocks. Code must check each block's type rather than assume the first is text.

    **Why the others are wrong:**

    * **A:** The response shape is unchanged; content remains a list of blocks.
    * **C:** There is no completion field in the Messages API response.
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

- **A.** Repeat the same request until stop_reason is end_turn
- **B.** Run the tool and send a tool_result in a user turn
- **C.** Show the response text to the user as the final answer
- **D.** Increase max_tokens, because the response was truncated

??? success "Answer: B"
    **Why B is right:** tool_use means Claude is waiting for your code to execute the tool and return the result.

    **Why the others are wrong:**

    * **A:** Repeating the request without a tool result just produces the same tool call.
    * **C:** The turn is not finished; Claude is waiting for a tool result.
    * **D:** Truncation is reported as max_tokens, not tool_use.

---

<p class="qb-meta"><span class="qb-id">AI-007</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application uses a server-side web search tool. A response comes back with stop_reason "pause_turn". What is the correct handling?

- **A.** Treat it as a refusal and show an apology to the user
- **B.** Discard the response and start a new conversation
- **C.** Send the assistant content back so Claude can continue
- **D.** Execute the search in your own code and return a tool_result

??? success "Answer: C"
    **Why C is right:** pause_turn means a server-side tool loop paused. Returning the content unchanged lets it resume.

    **Why the others are wrong:**

    * **A:** A pause is not a refusal; the work is simply unfinished.
    * **B:** That throws away progress; the turn can be continued.
    * **D:** Server tools run on the platform; there is no client tool call waiting.

---

<p class="qb-meta"><span class="qb-id">AI-008</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A request sets stop_sequences to ["###"]. The response has stop_reason "stop_sequence". Which statement is correct?

- **A.** The request failed validation because "###" is a reserved token
- **B.** The output was truncated by the max_tokens limit
- **C.** Claude produced "###", and so generation stopped there
- **D.** Claude declined to answer and used "###" as a marker

??? success "Answer: C"
    **Why C is right:** Custom stop sequences end generation, and the response reports the matched sequence.

    **Why the others are wrong:**

    * **A:** It is a normal, successful response.
    * **B:** That would be reported as max_tokens.
    * **D:** Declining is reported as refusal.

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
- **B.** ping
- **C.** content_block_stop
- **D.** message_start

??? success "Answer: A"
    **Why A is right:** message_delta carries top-level changes such as stop_reason and final usage, just before message_stop.

    **Why the others are wrong:**

    * **B:** ping events are keep-alives with no message data.
    * **C:** That closes a single content block, not the message.
    * **D:** message_start opens the message; stop_reason is not known yet.

---

<p class="qb-meta"><span class="qb-id">AI-011</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

During a streamed response, a tool call's arguments arrive as several input_json_delta events. How should the application obtain the tool input?

- **A.** Parse each partial_json fragment as it arrives and merge the objects
- **B.** Concatenate the partial_json strings and parse once at content_block_stop
- **C.** Ignore the deltas and read the input from message_start
- **D.** Wait for a tool_result event that contains the full input

??? success "Answer: B"
    **Why B is right:** Each delta is a fragment of JSON. Only the accumulated string is valid JSON.

    **Why the others are wrong:**

    * **A:** Individual fragments are not valid JSON on their own.
    * **C:** message_start arrives before any tool input is generated.
    * **D:** tool_result is something your application sends, not something it receives.

---

<p class="qb-meta"><span class="qb-id">AI-012</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A streaming request returns HTTP 200 and begins sending text. Thirty seconds later the stream ends with an error event. What does this show?

- **A.** The SDK has a bug, because a 200 response cannot contain an error
- **B.** The request was invalid and should have been rejected with a 400
- **C.** Errors can occur mid-stream, so the client must cope
- **D.** The content already received is corrupted and must be discarded silently

??? success "Answer: C"
    **Why C is right:** The status line is sent before generation finishes. Failures after that arrive as an error event in the stream.

    **Why the others are wrong:**

    * **A:** This is documented behaviour for streaming.
    * **B:** An invalid request is rejected before the stream starts.
    * **D:** The partial content is not corrupt; the application decides whether to retry or show it.

---

<p class="qb-meta"><span class="qb-id">AI-013</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service receives 400 invalid_request_error on some requests. A teammate proposes wrapping the call in a loop that retries up to five times. What is the best response?

- **A.** Retry once only, because the second attempt usually succeeds
- **B.** Agree, but switch to a larger model on the last attempt
- **C.** Agree, but add exponential backoff between the attempts
- **D.** Don't retry: the request is malformed, so fix it

??? success "Answer: D"
    **Why D is right:** Client errors of this type are deterministic. The same request will fail the same way.

    **Why the others are wrong:**

    * **A:** Nothing changes between attempts, so it will not succeed.
    * **B:** The error is about the request format, not model capability.
    * **C:** Backoff helps with overload, not with an invalid request.

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

- **A.** The API is temporarily overloaded; retry with exponential backoff
- **B.** The request body is too large; shrink it before trying again
- **C.** The API key is invalid; replace it before trying again
- **D.** The model ID does not exist; correct it before trying again

??? success "Answer: A"
    **Why A is right:** 529 is a transient server-side condition and is safe to retry after a delay.

    **Why the others are wrong:**

    * **B:** That is 413 request_too_large.
    * **C:** That is 401 authentication_error.
    * **D:** That is 404 not_found_error.

---

<p class="qb-meta"><span class="qb-id">AI-016</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A newly deployed service gets 401 authentication_error on every call, while the same code works on the developer's laptop. What is the most likely cause?

- **A.** The prompt contains content that the model refuses
- **B.** The model is overloaded in the deployment's region
- **C.** The deployed service is sending requests too quickly
- **D.** The API key is missing or wrong in that environment

??? success "Answer: D"
    **Why D is right:** 401 means the key was not supplied or is not valid. Environment differences are the usual reason.

    **Why the others are wrong:**

    * **A:** A refusal is a 200 response with a stop_reason, not a 401.
    * **B:** That would produce 529.
    * **C:** That would produce 429.

---

<p class="qb-meta"><span class="qb-id">AI-017</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A client uploads a very large PDF inline and the API returns 413. Which action addresses the cause?

- **A.** Switch to streaming so that the upload is sent in chunks
- **B.** Reduce the request size, for example by splitting the document
- **C.** Raise max_tokens so that the model can read the whole file
- **D.** Retry with exponential backoff until the request is accepted

??? success "Answer: B"
    **Why B is right:** 413 request_too_large means the body exceeds the size limit. Only a smaller request helps.

    **Why the others are wrong:**

    * **A:** Streaming affects the response, not the size of the request.
    * **C:** max_tokens limits output; it does not affect request size.
    * **D:** The request will be too large every time.

---

<p class="qb-meta"><span class="qb-id">AI-018</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A developer wraps every SDK call in a custom loop that retries five times on failure. During an outage, each user action produces far more API calls than expected. Why?

- **A.** Each retry is billed as a batch of one hundred requests
- **B.** The SDK opens one connection per token it generates
- **C.** The API duplicates every request during an outage
- **D.** The SDK retries by default, so layers multiply

??? success "Answer: D"
    **Why D is right:** The official SDKs retry transient errors twice by default. An outer loop multiplies that.

    **Why the others are wrong:**

    * **A:** Retries are ordinary single requests.
    * **B:** Connections are not opened per token.
    * **C:** The API does not duplicate requests.

---

<p class="qb-meta"><span class="qb-id">AI-019</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A non-streaming request that generates a very long document fails intermittently with timeouts and dropped connections. What is the recommended change?

- **A.** Use streaming, so that data flows continuously during generation
- **B.** Send the request twice in parallel and keep the faster one
- **C.** Set max_retries to zero so that the failure surfaces sooner
- **D.** Lower max_tokens to 256 so that responses return quickly

??? success "Answer: A"
    **Why A is right:** Long idle connections are fragile. Streaming keeps the connection active and is recommended for long outputs.

    **Why the others are wrong:**

    * **B:** That doubles cost and still risks both timing out.
    * **C:** That removes recovery without fixing the cause.
    * **D:** That would truncate the document the task needs.

---

<p class="qb-meta"><span class="qb-id">AI-020</span><span>Observability</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A customer reports a strange answer from yesterday. Which logged value is most useful when asking Anthropic support to investigate that specific call?

- **A.** The request ID returned in the response headers
- **B.** The local timestamp of the user's click
- **C.** The first eight characters of the API key
- **D.** The temperature value used for the request

??? success "Answer: A"
    **Why A is right:** Every response has a unique request-id that identifies the exact call.

    **Why the others are wrong:**

    * **B:** Timestamps are imprecise and not unique.
    * **C:** Key fragments identify the account, not a single request.
    * **D:** A parameter value does not identify a request.

---

<p class="qb-meta"><span class="qb-id">AI-021</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A dashboard shows average usage at 60% of the requests-per-minute limit, yet the application still receives occasional 429 errors at the top of each hour when a scheduled job starts. Why?

- **A.** A token bucket lets a sudden burst exceed capacity
- **B.** Rate limits are reset to zero at the start of each hour
- **C.** 429 is returned at random to keep usage below 50%
- **D.** Scheduled jobs are counted twice against the limit

??? success "Answer: A"
    **Why A is right:** The limit is not a simple per-minute counter. Short bursts can drain the bucket even when the average is low.

    **Why the others are wrong:**

    * **B:** There is no hourly reset that lowers capacity.
    * **C:** Limits are deterministic, not random.
    * **D:** Requests are counted once regardless of origin.

---

<p class="qb-meta"><span class="qb-id">AI-022</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application with a large, repeated system prompt keeps hitting its input-tokens-per-minute limit. Which change raises effective throughput without asking for higher limits?

- **A.** Raise the temperature, since it reduces the tokens processed
- **B.** Enable streaming, since streamed tokens are not rate limited
- **C.** Cache the prompt, since cached reads are mostly exempt
- **D.** Lower max_tokens, since it is counted against the input limit

??? success "Answer: C"
    **Why C is right:** On most current models cache_read_input_tokens are excluded from ITPM, so caching increases throughput.

    **Why the others are wrong:**

    * **A:** Temperature does not change token counts.
    * **B:** Streaming does not change rate-limit accounting.
    * **D:** max_tokens concerns output and is not counted against input limits.

---

<p class="qb-meta"><span class="qb-id">AI-023</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Before sending a request that includes a long document, a service wants to know whether it will fit and which model to route it to. What is the best approach?

- **A.** Send the request and read usage from the error response
- **B.** Divide the character count by ten to estimate the tokens
- **C.** Set max_tokens to zero to get a free dry run
- **D.** Call the token counting endpoint before sending

??? success "Answer: D"
    **Why D is right:** count_tokens accepts the same system, messages and tools as a real request and returns the input token count at no charge.

    **Why the others are wrong:**

    * **A:** That wastes a call and may fail or cost money.
    * **B:** A crude ratio is unreliable, especially with tools, images or non-English text.
    * **C:** max_tokens must be positive; this is not a dry-run mechanism.

---

<p class="qb-meta"><span class="qb-id">AI-024</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which statement about the token counting endpoint is correct?

- **A.** It is free, separately limited, and gives an estimate
- **B.** It only supports plain text and rejects tools or images
- **C.** It is billed at the input rate and shares the Messages rate limit
- **D.** It returns both the input tokens and the predicted output tokens

??? success "Answer: A"
    **Why A is right:** Counting does not generate output, is not billed, and is limited separately from message creation.

    **Why the others are wrong:**

    * **B:** It accepts the same structured inputs as a message request.
    * **C:** It is free and separately limited.
    * **D:** Output length is not known before generation.

---

<p class="qb-meta"><span class="qb-id">AI-025</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team submits 5,000 requests in one message batch and reads the results file line by line, assuming line N answers request N. Some answers end up attached to the wrong records. What is the fix?

- **A.** Submit the requests in smaller batches of exactly 100
- **B.** Match each result to its request using custom_id
- **C.** Add a sequence number to each prompt and ask Claude to repeat it
- **D.** Sort the results by their completion timestamp

??? success "Answer: B"
    **Why B is right:** Batch results are not guaranteed to be in submission order. custom_id exists for matching.

    **Why the others are wrong:**

    * **A:** Batch size does not make the order reliable.
    * **C:** Fragile and unnecessary when custom_id is provided.
    * **D:** Completion time does not reflect submission order.

---

<p class="qb-meta"><span class="qb-id">AI-026</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Every night a company summarises 60,000 product reviews. Results are needed by the next morning. Which approach is most cost-effective?

- **A.** Synchronous calls with streaming enabled for every review
- **B.** The Message Batches API, since nobody is waiting on each result
- **C.** Synchronous calls using the most capable model available
- **D.** One request containing all 60,000 reviews in a single prompt

??? success "Answer: B"
    **Why B is right:** Batches are asynchronous and half the price, which suits large offline jobs.

    **Why the others are wrong:**

    * **A:** Streaming helps a waiting user, not an overnight job.
    * **C:** That maximises cost with no stated quality need.
    * **D:** It would exceed limits and give poor per-review results.

---

<p class="qb-meta"><span class="qb-id">AI-027</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

To cut costs, a product manager suggests sending live customer chat messages through the Message Batches API. What is the main problem?

- **A.** Batches cost more per token than synchronous calls
- **B.** Batches are asynchronous and may take hours to finish
- **C.** Batches can only be submitted once per day
- **D.** Batches do not support system prompts or tools

??? success "Answer: B"
    **Why B is right:** A batch has no latency guarantee beyond finishing within its processing window.

    **Why the others are wrong:**

    * **A:** They cost less, about half.
    * **C:** There is no such restriction.
    * **D:** Batch requests accept normal Messages parameters.

---

<p class="qb-meta"><span class="qb-id">AI-028</span><span>Errors</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO errors are appropriate to retry automatically with backoff? (Select TWO.)

- **A.** 429 rate_limit_error
- **B.** 401 authentication_error
- **C.** 404 not_found_error
- **D.** 529 overloaded_error
- **E.** 400 invalid_request_error

??? success "Answer: A and D"
    **Why A is right:** Rate limiting is temporary; wait and retry.

    **Why D is right:** Overload is temporary; back off and retry.

    **Why the others are wrong:**

    * **B:** The key is wrong; retrying cannot fix it.
    * **C:** The resource or model does not exist; retrying cannot fix it.
    * **E:** The request is malformed and will fail again.

---

<p class="qb-meta"><span class="qb-id">AI-029</span><span>Request shape</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about the Messages API are correct? (Select TWO.)

- **A.** The API stores each conversation for 24 hours by default
- **B.** max_tokens sets the minimum length of the response
- **C.** The system prompt is supplied as a top-level parameter
- **D.** The application must resend prior turns to continue a conversation
- **E.** A 200 status guarantees that the answer is complete

??? success "Answer: C and D"
    **Why C is right:** system is not a role inside messages.

    **Why D is right:** The API is stateless.

    **Why the others are wrong:**

    * **A:** No conversation state is kept between calls.
    * **B:** It is an upper limit on output.
    * **E:** stop_reason may still indicate truncation.

---

<p class="qb-meta"><span class="qb-id">AI-030</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer sets max_tokens to 4,000 hoping for longer, more detailed answers, but replies remain short. Why?

- **A.** Values above 1,024 are silently reduced by the API
- **B.** The value is ignored unless streaming is enabled
- **C.** max_tokens is a cap; ask for length in the prompt
- **D.** max_tokens applies to the input rather than the output

??? success "Answer: C"
    **Why C is right:** The parameter caps output. It does not instruct the model to write more.

    **Why the others are wrong:**

    * **A:** Models support much larger outputs.
    * **B:** It applies to streamed and non-streamed responses alike.
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

- **A.** A single agent with a higher turn limit to explore options
- **B.** A multi-agent system with one agent for each of the steps
- **C.** A prompt chain run by application code, with a check between steps
- **D.** One very long prompt that asks for all three results at once

??? success "Answer: C"
    **Why C is right:** When steps are fixed and known, a workflow is cheaper, faster and more predictable than an agent.

    **Why the others are wrong:**

    * **A:** Autonomy adds unpredictability where none is needed.
    * **B:** Extra coordination cost with no benefit for a fixed sequence.
    * **D:** Harder to validate and debug than separate steps.

---

<p class="qb-meta"><span class="qb-id">AI-033</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A help desk receives billing questions, technical faults and sales enquiries. Each type needs different instructions and tools. Which pattern fits best?

- **A.** Parallelisation: send each message to all three handlers
- **B.** A single general prompt that lists every rule for all types
- **C.** Evaluator-optimiser: draft a reply, then critique and revise it
- **D.** Routing: classify each message, then send it to a specialised prompt

??? success "Answer: D"
    **Why D is right:** Routing separates concerns, so each path can be tuned without harming the others.

    **Why the others are wrong:**

    * **A:** Wasteful, and the answers then need reconciling.
    * **B:** Rules for different types interfere with one another.
    * **C:** That improves one output; it does not pick a path.

---

<p class="qb-meta"><span class="qb-id">AI-034</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An internal assistant must answer questions using the company's 4,000-page policy library, which changes monthly. Which design is most appropriate?

- **A.** Rely on the model's training data to know the policies
- **B.** Retrieve relevant passages and add them to the prompt
- **C.** Paste the full library into the system prompt on every request
- **D.** Raise the temperature so that the model recalls more detail

??? success "Answer: B"
    **Why B is right:** Retrieval supplies current, relevant content without sending everything every time.

    **Why the others are wrong:**

    * **A:** The model has never seen private, changing documents.
    * **C:** Likely too large, slow and costly.
    * **D:** Temperature does not add knowledge.

---

<p class="qb-meta"><span class="qb-id">AI-035</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A web chat application needs multi-turn conversations. Where should conversation history be kept?

- **A.** In the Claude API, retrieved with the previous message ID
- **B.** Nowhere, since the model retains recent conversations
- **C.** In the system prompt, appended to after every turn
- **D.** In a server-side store keyed by the application's own session ID

??? success "Answer: D"
    **Why D is right:** The application owns state. A backend store lets it reload and resend history securely.

    **Why the others are wrong:**

    * **A:** The API does not store conversations for retrieval.
    * **B:** The model retains nothing between calls.
    * **C:** History belongs in messages; rewriting the system prompt also defeats caching.

---

<p class="qb-meta"><span class="qb-id">AI-036</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

Two browser tabs for the same user send messages to the same conversation at almost the same moment. Afterwards the stored history has turns out of order and one reply is missing. What should be added?

- **A.** A lower temperature so that both replies are identical
- **B.** A longer max_tokens so that neither reply is dropped
- **C.** Per-session locking when the history is updated
- **D.** A second API key so that the two tabs do not collide

??? success "Answer: C"
    **Why C is right:** It is an ordinary concurrent-write problem on shared state, solved with ordinary concurrency control.

    **Why the others are wrong:**

    * **A:** Sampling settings cannot fix a race condition.
    * **B:** The reply was lost in storage, not truncated.
    * **D:** Keys are unrelated to writes to your own store.

---

<p class="qb-meta"><span class="qb-id">AI-037</span><span>Architecture</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A mobile team wants the app to call the Claude API directly to avoid an extra network hop. What is the main objection?

- **A.** The Claude API refuses requests from mobile devices
- **B.** Direct calls are billed at a higher rate per token
- **C.** Mobile networks cannot carry server-sent events
- **D.** The API key would ship in the app and be extractable

??? success "Answer: D"
    **Why D is right:** Client-side keys cannot be kept secret. Calls should go through a backend that holds the key.

    **Why the others are wrong:**

    * **A:** The API does not identify device types.
    * **B:** Pricing does not depend on where the call originates.
    * **C:** They can; this is not the issue.

---

<p class="qb-meta"><span class="qb-id">AI-038</span><span>Schema design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An extraction schema marks delivery_date as a required string. For emails that contain no date, the model returns a plausible but invented date. What is the best schema change?

- **A.** Make the field nullable, returning null when absent
- **B.** Lower the temperature so that the date is deterministic
- **C.** Mark the field required in two places for emphasis
- **D.** Add a regular expression that enforces a date format

??? success "Answer: A"
    **Why A is right:** A required field with no source value pushes the model to invent one.

    **Why the others are wrong:**

    * **B:** A deterministic invented date is still invented.
    * **C:** Emphasis does not create missing information.
    * **D:** The format was fine; the value was fabricated.

---

<p class="qb-meta"><span class="qb-id">AI-039</span><span>Schema design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A ticket classifier uses an enum of five categories. Unusual tickets are being forced into badly fitting categories. Which change helps most?

- **A.** Add an "other" value, with a short free-text field for the detail
- **B.** Remove the enum and accept any free-text category
- **C.** Add twenty more categories to cover every case
- **D.** Send each ticket three times and take the majority label

??? success "Answer: A"
    **Why A is right:** An escape value stops the model from being forced into a wrong label.

    **Why the others are wrong:**

    * **B:** That loses the consistency the enum provides.
    * **C:** Large enums are harder to choose from and never cover everything.
    * **D:** Voting between wrong labels does not produce a right one.

---

<p class="qb-meta"><span class="qb-id">AI-040</span><span>Validation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An invoice extractor uses structured outputs, so every response matches the schema. Finance finds invoices where the line items do not add up to the stated total. What is missing?

- **A.** A system prompt reminder that totals must be accurate
- **B.** A higher max_tokens value so that totals are not truncated
- **C.** A stricter schema with additionalProperties set to false
- **D.** A semantic check in code that lines sum to the total

??? success "Answer: D"
    **Why D is right:** A schema guarantees structure, not correctness. Business rules need their own validation.

    **Why the others are wrong:**

    * **A:** A reminder is not verification.
    * **B:** Nothing was truncated.
    * **C:** The structure was already valid; the values were wrong.

---

<p class="qb-meta"><span class="qb-id">AI-041</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

After a timeout, a workflow retried a step, and a customer was refunded twice. Which design principle prevents this?

- **A.** Make the side effect idempotent, using an idempotency key
- **B.** Increase the timeout to ten minutes for every call
- **C.** Disable all retries across the whole application
- **D.** Ask the model to remember which refunds it has issued

??? success "Answer: A"
    **Why A is right:** With an idempotency key, a repeated attempt is recognised and not executed again.

    **Why the others are wrong:**

    * **B:** Timeouts can still occur; duplicates remain possible.
    * **C:** That sacrifices resilience; the issue is the repeated side effect.
    * **D:** Model memory is not a reliable transaction record.

---

<p class="qb-meta"><span class="qb-id">AI-042</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

The Claude API has been returning errors for several minutes. Every user request waits through multiple retries and then fails. What should the application do instead?

- **A.** Stop calling after repeated failures and fall back
- **B.** Increase the retry count so that requests eventually pass
- **C.** Remove the timeout so that requests can wait as long as needed
- **D.** Return an empty reply so that users don't see any error

??? success "Answer: A"
    **Why A is right:** A circuit breaker with graceful degradation avoids piling up slow, doomed requests.

    **Why the others are wrong:**

    * **B:** More retries deepen the pile-up during an outage.
    * **C:** Hanging requests exhaust resources and frustrate users.
    * **D:** Silent empty answers hide the failure and confuse users.

---

<p class="qb-meta"><span class="qb-id">AI-043</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A marketing campaign sends bursts of thousands of requests within a few seconds, causing many 429 errors, although total daily volume is well within limits. Which design smooths this out?

- **A.** Open more connections so that the burst finishes sooner
- **B.** Put requests on a queue and process them at a controlled rate
- **C.** Raise max_tokens so that each request does more work
- **D.** Disable SDK retries so that failures return faster

??? success "Answer: B"
    **Why B is right:** A queue absorbs bursts and feeds the API at a steady pace.

    **Why the others are wrong:**

    * **A:** That intensifies the burst.
    * **C:** It does not reduce the request rate.
    * **D:** Requests would simply fail instead of completing.

---

<p class="qb-meta"><span class="qb-id">AI-044</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A model ID is hard-coded in forty source files. A newer model must now be adopted. Which practice would have made this a small change?

- **A.** Storing the model ID inside the system prompt text
- **B.** Keeping the model ID in configuration, read by all the call sites
- **C.** Letting each developer choose the model on their machine
- **D.** Using a different model ID in every file for flexibility

??? success "Answer: B"
    **Why B is right:** Configuration lets the model change without editing code across the codebase.

    **Why the others are wrong:**

    * **A:** The prompt does not select the model.
    * **C:** Uncontrolled variation between environments.
    * **D:** That makes the system even harder to manage.

---

<p class="qb-meta"><span class="qb-id">AI-045</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Production behaviour changed slightly overnight with no deployment. The service uses a model alias that always points to the newest version. What is the recommended practice?

- **A.** Switch aliases every day to average out the differences
- **B.** Pin a specific model version and upgrade deliberately after testing
- **C.** Keep the alias and add more few-shot examples each week
- **D.** Keep the alias and lower the temperature to stabilise output

??? success "Answer: B"
    **Why B is right:** A moving alias can change behaviour without warning. Pinning makes upgrades a tested release.

    **Why the others are wrong:**

    * **A:** That adds variation rather than removing it.
    * **C:** Examples do not prevent the underlying model from changing.
    * **D:** Sampling settings do not prevent a model change.

---

<p class="qb-meta"><span class="qb-id">AI-046</span><span>Life cycle</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A developer edits one paragraph of a production system prompt and deploys it directly. The next day, a previously working feature is broken. Which process was missing?

- **A.** A rule that only senior developers may edit prompts
- **B.** A longer system prompt with more capital letters
- **C.** Versioned prompts and evals before release
- **D.** A higher max_tokens setting in production

??? success "Answer: C"
    **Why C is right:** A prompt change is a behaviour change. Regression evals catch breakage before users do.

    **Why the others are wrong:**

    * **A:** Seniority does not replace testing.
    * **B:** Emphasis is not a release process.
    * **D:** Unrelated to the regression.

---

<p class="qb-meta"><span class="qb-id">AI-047</span><span>Life cycle</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

After launch, which set of measurements best shows the health of a Claude-powered feature?

- **A.** The average temperature across all the requests
- **B.** Error rates, latency, token cost, validation failures
- **C.** The count of developers who can access the API key
- **D.** The number of lines in the system prompt each week

??? success "Answer: B"
    **Why B is right:** Together these cover reliability, speed, spend and output quality.

    **Why the others are wrong:**

    * **A:** A configuration value, not an outcome.
    * **C:** An access-control fact, not a health metric.
    * **D:** Prompt length says nothing about behaviour in production.

---

<p class="qb-meta"><span class="qb-id">AI-048</span><span>Access control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a multi-tenant application, a user of one company receives an answer that quotes another company's document. Where is the flaw?

- **A.** The model's context window was too large
- **B.** The system prompt did not forbid sharing documents
- **C.** Retrieval was not scoped to the authenticated user's tenant
- **D.** The temperature allowed the model to be creative

??? success "Answer: C"
    **Why C is right:** Isolation must be enforced when data is fetched, before anything reaches the prompt.

    **Why the others are wrong:**

    * **A:** Window size does not select which documents are retrieved.
    * **B:** A prompt rule cannot undo data that was already supplied.
    * **D:** The other tenant's content was in the context; this is not creativity.

---

<p class="qb-meta"><span class="qb-id">AI-049</span><span>Configuration</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO practices are appropriate for managing configuration of a Claude application? (Select TWO.)

- **A.** Load the API key from a secret manager or environment variable
- **B.** Commit the API key in a private repository for convenience
- **C.** Use separate keys and settings for development and production
- **D.** Embed prompts as string literals spread across the modules
- **E.** Share one key across all teams to simplify rotation

??? success "Answer: A and C"
    **Why A is right:** Keeps the key out of code and repositories.

    **Why C is right:** Limits blast radius and separates usage.

    **Why the others are wrong:**

    * **B:** Private repositories still leak; keys do not belong in source control.
    * **D:** Scattered prompts are hard to version, review and test.
    * **E:** A shared key widens exposure and hides who used what.

---

<p class="qb-meta"><span class="qb-id">AI-050</span><span>Sync or batch</span><span>Select TWO</span><span title="Difficulty">●○○</span></p>

A team is deciding between synchronous calls and the Message Batches API for a new workload. Which TWO facts are most relevant to the decision? (Select TWO.)

- **A.** Whether a user or blocking process is waiting on each result
- **B.** Whether the system prompt uses XML tags or Markdown
- **C.** Whether a delay of up to several hours is acceptable
- **D.** Whether the prompts are written in British or American English
- **E.** Whether the developers prefer Python or TypeScript

??? success "Answer: A and C"
    **Why A is right:** Batches are asynchronous, so waiting users rule them out.

    **Why C is right:** Batch completion time is not immediate.

    **Why the others are wrong:**

    * **B:** Prompt formatting does not affect the choice.
    * **D:** Spelling variety has no bearing on the choice.
    * **E:** Both SDKs support both modes.

---

<p class="qb-meta"><span class="qb-id">AI-051</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A sponsor asks a developer to "add AI to the returns process". What should the developer do first?

- **A.** Build a multi-agent prototype to show the sponsor
- **B.** Write a long system prompt covering every case
- **C.** Clarify the goal and write measurable requirements
- **D.** Choose the most capable model that is available

??? success "Answer: C"
    **Why C is right:** An ambiguous goal cannot be designed or tested. Requirements come before model or pattern choices.

    **Why the others are wrong:**

    * **A:** Building before the goal is clear risks solving the wrong problem.
    * **B:** There is nothing agreed yet for the prompt to implement.
    * **D:** Model choice depends on requirements that don't exist yet.

---

<p class="qb-meta"><span class="qb-id">AI-052</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which of these is an infrastructure (non-functional) requirement?

- **A.** The system must draft a reply for an agent to approve
- **B.** The system must classify tickets into six categories
- **C.** Responses must begin within two seconds at peak load
- **D.** The system must extract the invoice number and total

??? success "Answer: C"
    **Why C is right:** It describes how well the system must perform, not what it does.

    **Why the others are wrong:**

    * **A:** That is a function the system performs.
    * **B:** That is a function the system performs.
    * **D:** That is a function the system performs.

---

<p class="qb-meta"><span class="qb-id">AI-053</span><span>Requirements</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A requirement states: "Customer data must not leave the company's cloud region." Which design decision does this affect most directly?

- **A.** Whether examples in the prompt use XML tags
- **B.** Whether the temperature is set near 0 or 1
- **C.** Whether responses are parsed with Pydantic
- **D.** Which platform and deployment option is used

??? success "Answer: D"
    **Why D is right:** Data-residency constraints determine where and through which provider the model is called.

    **Why the others are wrong:**

    * **A:** Prompt formatting does not control where data is processed.
    * **B:** Sampling settings are unrelated to data location.
    * **C:** Validation tooling is unrelated to data location.

---

<p class="qb-meta"><span class="qb-id">AI-054</span><span>Systems life cycle</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An application has run unchanged for a year. One morning every request fails with a 404 naming the model. Nothing was deployed. What life-cycle activity was neglected?

- **A.** Testing: the unit tests should have been stricter
- **B.** Development: the code should have used raw HTTP
- **C.** Design: the system should have used more agents
- **D.** Maintenance: tracking model deprecations

??? success "Answer: D"
    **Why D is right:** Models are retired on a schedule. Operating an LLM system includes watching for that and migrating in time.

    **Why the others are wrong:**

    * **A:** Unit tests cannot keep a retired model available.
    * **B:** The SDK is not the cause of a retired model.
    * **C:** Agent count has nothing to do with a retired model.

---

<p class="qb-meta"><span class="qb-id">AI-055</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

What is the relationship between an official Claude SDK and the REST API?

- **A.** The SDK is required; raw HTTP calls are rejected
- **B.** The SDK uses a separate, faster private protocol
- **C.** The SDK runs the model locally on your machine
- **D.** The SDK is a wrapper over the same REST API

??? success "Answer: D"
    **Why D is right:** SDKs add typing, retries, timeouts and stream handling on top of the same HTTP endpoints.

    **Why the others are wrong:**

    * **A:** Any HTTP client can call the API.
    * **B:** It calls the same public HTTP API.
    * **C:** Models run on the provider's servers.

---

<p class="qb-meta"><span class="qb-id">AI-056</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer builds a JSON request body by joining strings and inserting the user's text directly. Requests fail whenever the text contains a quotation mark. What is the correct fix?

- **A.** Serialise the object with a JSON library
- **B.** Wrap the user's text in a second pair of quotes
- **C.** Ask users not to type quotation marks in the box
- **D.** Replace every quotation mark with a blank space

??? success "Answer: A"
    **Why A is right:** A serialiser escapes special characters correctly. String concatenation does not.

    **Why the others are wrong:**

    * **B:** Adds more unescaped quotes and makes the JSON worse.
    * **C:** Unreasonable, and other characters will also break it.
    * **D:** Corrupts the user's text and misses other special characters.

---

<p class="qb-meta"><span class="qb-id">AI-057</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A script summarises 4,000 documents by launching all requests at once with asyncio.gather. Most fail with 429 errors. A user is waiting for the results. What is the best change?

- **A.** Limit concurrency with a semaphore or worker pool
- **B.** Switch every call to the synchronous client instead
- **C.** Remove the awaits so that requests return sooner
- **D.** Launch the same requests twice to improve the odds

??? success "Answer: A"
    **Why A is right:** Bounded concurrency keeps throughput high while staying inside rate limits.

    **Why the others are wrong:**

    * **B:** Sequential calls would be very slow for a waiting user.
    * **C:** Without awaiting, results are never collected.
    * **D:** Doubles the load that caused the errors.

---

<p class="qb-meta"><span class="qb-id">AI-058</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A coding agent produced a change that passes the existing tests. What should happen before it is merged?

- **A.** The change is merged and reviewed after the release
- **B.** Nothing further; passing tests are sufficient proof
- **C.** The same session reviews and approves its own change
- **D.** A person reviews the diff, edge cases included

??? success "Answer: D"
    **Why D is right:** Passing tests show only what the tests cover. Review is still needed for generated code.

    **Why the others are wrong:**

    * **A:** Review after release finds problems too late.
    * **B:** Tests rarely cover every edge case or security concern.
    * **C:** A fresh reviewer avoids the author's blind spots.

---

<p class="qb-meta"><span class="qb-id">AI-059</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants an agent to migrate 180 files from one logging library to another. Which approach is most likely to succeed?

- **A.** Plan first, then migrate in small verified steps
- **B.** Let several agents edit the same files in parallel
- **C.** Skip the tests until every file has been converted
- **D.** Ask for all 180 files to be rewritten in one prompt

??? success "Answer: A"
    **Why A is right:** Large refactors need a plan, a safety net of tests, and incremental verification.

    **Why the others are wrong:**

    * **B:** Conflicting edits on shared files cause breakage.
    * **C:** Errors compound and become hard to locate.
    * **D:** Overloads context and gives no checkpoint when something breaks.

---

<p class="qb-meta"><span class="qb-id">AI-060</span><span>Software engineering</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

During code review, a reviewer notices that generated code imports a package nobody on the team has heard of. What is the right reaction?

- **A.** Assume it is a standard library the team forgot
- **B.** Verify the package exists and is trustworthy
- **C.** Delete the import line and merge the remainder
- **D.** Install it at once, since the model recommended it

??? success "Answer: B"
    **Why B is right:** Generated code can reference non-existent or unsuitable packages. Dependencies must be checked.

    **Why the others are wrong:**

    * **A:** An assumption, not a check.
    * **C:** The code probably depends on it and would break.
    * **D:** A recommendation is not verification.

---

<p class="qb-meta"><span class="qb-id">AI-061</span><span>Technical fundamentals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Why does the Messages API use server-sent events for streaming, and not WebSockets?

- **A.** Token streaming only needs one-way delivery
- **B.** WebSockets are limited to a hundred messages
- **C.** WebSockets cannot carry text, only binary frames
- **D.** Server-sent events let the client send mid-stream

??? success "Answer: A"
    **Why A is right:** SSE provides one-way streaming over ordinary HTTP. WebSockets are for two-way communication.

    **Why the others are wrong:**

    * **B:** There is no such limit.
    * **C:** WebSockets carry text as well as binary.
    * **D:** SSE is one-way; the client does not send on it.

---

<p class="qb-meta"><span class="qb-id">AI-062</span><span>Technical fundamentals</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A browser-based voice assistant needs the client and the team's backend to exchange audio and control messages continuously in both directions. Which transport suits that link?

- **A.** A nightly batch upload
- **B.** A WebSocket connection
- **C.** A series of separate GET requests
- **D.** Server-sent events alone

??? success "Answer: B"
    **Why B is right:** WebSockets keep one connection open over which both sides can send at any time.

    **Why the others are wrong:**

    * **A:** A batch has no real-time interaction.
    * **C:** Polling is slow and one-directional per request.
    * **D:** SSE only carries data from server to client.

---

<p class="qb-meta"><span class="qb-id">AI-063</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A prompt gives excellent results in the Claude chat app. Sent unchanged through the Messages API, results are noticeably different. What is the most likely explanation?

- **A.** The API always serves an older and weaker model
- **B.** The API adds no product system prompt, tools or memory
- **C.** The API ignores the first message of each request
- **D.** The API runs every request at temperature zero

??? success "Answer: B"
    **Why B is right:** Each surface assembles context differently. Through the API, Claude sees only what the request contains.

    **Why the others are wrong:**

    * **A:** The model is whichever one the request names.
    * **C:** Every message sent is used.
    * **D:** The default is not zero unless set.

---

<p class="qb-meta"><span class="qb-id">AI-064</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In Claude Code, a team writes "Never run database migrations" in CLAUDE.md. A migration is later run during a session. Why was the instruction not a guarantee?

- **A.** CLAUDE.md is only loaded on the first day of use
- **B.** CLAUDE.md is guidance, not an enforced control
- **C.** CLAUDE.md applies to Python files and no others
- **D.** CLAUDE.md is limited to twenty lines of content

??? success "Answer: B"
    **Why B is right:** Instructions are advisory. Enforcement needs a permission rule or a hook.

    **Why the others are wrong:**

    * **A:** It is loaded in every session.
    * **C:** It is not restricted by language.
    * **D:** There is no such limit.

---

<p class="qb-meta"><span class="qb-id">AI-065</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer has spent three hours in one Claude Code session on several unrelated tasks. Answers are getting worse and earlier instructions are being forgotten. What is the best practice?

- **A.** Keep going and repeat each instruction in capitals
- **B.** Raise the max_tokens value for the next reply
- **C.** Start a fresh session per task, carrying a short summary
- **D.** Paste the whole transcript back in as a reminder

??? success "Answer: C"
    **Why C is right:** Unrelated history pollutes the context. Clean sessions with a deliberate hand-over work better.

    **Why the others are wrong:**

    * **A:** Adds more noise to an already crowded context.
    * **B:** Output size is not the issue.
    * **D:** Makes the context problem worse.

---

<p class="qb-meta"><span class="qb-id">AI-066</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team wants every developer to have the same set of Claude Code skills, commands and hooks for a project. Which approach fits best?

- **A.** Have each developer recreate them from memory
- **B.** Email the files and ask each person to copy them
- **C.** Package them as a plugin enabled in the project settings
- **D.** Describe them in the README without any files

??? success "Answer: C"
    **Why C is right:** A plugin bundles these components, and project settings share it with everyone who works in the repository.

    **Why the others are wrong:**

    * **A:** Guarantees inconsistency.
    * **B:** Manual copies drift apart and are never updated together.
    * **D:** A description does not install anything.

---

<p class="qb-meta"><span class="qb-id">AI-067</span><span>Application design</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Before installing a third-party Claude Code plugin, what is the most important consideration?

- **A.** It should be the newest plugin in the marketplace
- **B.** It should contain more commands than other plugins
- **C.** It can run code, so its source must be trusted
- **D.** Its name should be shorter than twelve characters

??? success "Answer: C"
    **Why C is right:** Plugins can execute code and extend what the agent can do. Treat them like any other dependency.

    **Why the others are wrong:**

    * **A:** Newness says nothing about safety.
    * **B:** Size is not a measure of trust or quality.
    * **D:** Name length is irrelevant.

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

- **A.** CLAUDE.md in the project root
- **B.** .claude/settings.json
- **C.** .mcp.json in the project root
- **D.** .claude/settings.local.json

??? success "Answer: D"
    **Why D is right:** The local settings file is for personal overrides and is not committed.

    **Why the others are wrong:**

    * **A:** It holds instructions, not permission settings, and is shared.
    * **B:** That file is committed and shared with the team.
    * **C:** It lists shared MCP servers.

---

<p class="qb-meta"><span class="qb-id">AI-070</span><span>Platforms</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An application is moved from the direct Claude API to a cloud vendor's platform. A beta feature it depends on stops working. What should have been checked first?

- **A.** Whether the team's laptops were recently updated
- **B.** Whether the prompts were translated to English
- **C.** Whether the cloud vendor uses a faster network
- **D.** Whether that feature is available on the chosen platform

??? success "Answer: D"
    **Why D is right:** Feature availability, model identifiers and authentication differ between platforms.

    **Why the others are wrong:**

    * **A:** Client machines are unrelated.
    * **B:** Language is unrelated to feature availability.
    * **C:** Network speed does not add a missing feature.

---

<p class="qb-meta"><span class="qb-id">AI-071</span><span>Requirements</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO are infrastructure (non-functional) requirements? (Select TWO.)

- **A.** The service must translate documents into French
- **B.** The service must handle 50 requests per second at peak
- **C.** The service must flag invoices with missing totals
- **D.** The service must produce a summary for each ticket
- **E.** Prompts and outputs must be retained for no more than 30 days

??? success "Answer: B and E"
    **Why B is right:** A throughput constraint.

    **Why E is right:** A data-retention constraint.

    **Why the others are wrong:**

    * **A:** A function.
    * **C:** A function.
    * **D:** A function.

---

<p class="qb-meta"><span class="qb-id">AI-072</span><span>SDLC integration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team adopts AI-assisted delivery and wants an audit trail showing who asked for a change, what the agent produced and who approved it. Which practice provides this most directly?

- **A.** Commit each stage's artefact to version control
- **B.** Ask the agent to remember earlier decisions
- **C.** Email a weekly summary of what was built
- **D.** Keep the artefacts in each person's chat history

??? success "Answer: A"
    **Why A is right:** Intent, specification, plan, code and review findings in git give a dated, attributable record.

    **Why the others are wrong:**

    * **B:** Model memory is not an audit record.
    * **C:** A summary is not a traceable record of each decision.
    * **D:** Private chat history is neither shared nor reviewable.

---

<p class="qb-meta"><span class="qb-id">AI-073</span><span>SDLC integration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent wrote a change and opened a pull request. Which arrangement preserves separation of duties?

- **A.** Branch protection requires a human code owner's approval
- **B.** The request merges automatically once tests pass
- **C.** The agent pushes straight to the main branch
- **D.** The same agent session approves its own request

??? success "Answer: A"
    **Why A is right:** The author of a change, human or agent, should not be the one who approves it.

    **Why the others are wrong:**

    * **B:** Tests do not replace an accountable approval.
    * **C:** That bypasses review altogether.
    * **D:** Self-approval removes the independent check.

---

<p class="qb-meta"><span class="qb-id">AI-074</span><span>SDLC integration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An engineer asks Claude Code to fix a bug. The agent makes the failing test pass by changing the test's expected value. Which workflow prevents this?

- **A.** Run the same request again in a longer session
- **B.** Raise the temperature so the fix is more creative
- **C.** Commit the failing test first, then forbid edits to it
- **D.** Delete the test so that it can no longer fail

??? success "Answer: C"
    **Why C is right:** A test that existed before the fix and could not be changed is real evidence that the bug is gone.

    **Why the others are wrong:**

    * **A:** Nothing stops the same shortcut being taken again.
    * **B:** Sampling settings do not protect the test.
    * **D:** Removes the evidence altogether.

---

<p class="qb-meta"><span class="qb-id">AI-075</span><span>SDLC integration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An engineer wants three independent tasks worked on at the same time by separate Claude Code sessions. What keeps the sessions from overwriting each other's files?

- **A.** Running all three in the same working folder
- **B.** Sharing one conversation between the sessions
- **C.** Lowering max_tokens for each of the sessions
- **D.** Giving each session its own git worktree and branch

??? success "Answer: D"
    **Why D is right:** A worktree is a separate checkout, so parallel sessions cannot collide on files.

    **Why the others are wrong:**

    * **A:** They would edit the same files and conflict.
    * **B:** Sessions do not share a conversation, and that would not isolate files.
    * **C:** Output limits do not isolate file changes.

---

<p class="qb-meta"><span class="qb-id">AI-076</span><span>SDLC integration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Work items live in an existing ticket system, and the team now also keeps specifications as files in the repository. The two start to disagree. What is the recommended rule?

- **A.** Name one system as the source of truth and link the other
- **B.** Stop using version control for specifications
- **C.** Ask the agent to guess which copy is correct
- **D.** Keep both and let each team trust its own copy

??? success "Answer: A"
    **Why A is right:** One authoritative record per artefact, with a link from the copy, prevents drift.

    **Why the others are wrong:**

    * **B:** Loses the reviewable, versioned record.
    * **C:** Guessing is not governance.
    * **D:** That guarantees the copies diverge.

---
