# Question Bank · Applications & Integration

**50 original questions** (4 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Access control · Architecture · Batches · Choosing a pattern · Configuration · Conversation history · Errors · Life cycle · Observability · Rate limits · Reliability · Request shape · Response shape · SDK behaviour · Schema design · Session handling · Statelessness · Stop reasons · Streaming · Sync or batch · Token counting · Validation

---

<p class="qb-meta"><span class="qb-id">AI-001</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer adds {"role": "system", "content": "You are a helpful travel assistant."} as the first item in the messages list and receives a 400 error. What is the correct fix?

- **A.** Move the text to the top-level system parameter of the request
- **B.** Send the system text in a custom HTTP request header
- **C.** Place the system message last so that it takes priority
- **D.** Rename the role to "developer" and send the request again

??? success "Answer: A"
    **Why A is right:** System prompts are a top-level parameter. The messages list only accepts user and assistant roles.

    **Why the others are wrong:**

    * **B:** Headers carry authentication and versioning, not prompt content.
    * **C:** Position does not matter; the role itself is not accepted.
    * **D:** There is no developer role in the Messages API.

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

- **A.** The model's context window was exceeded by the first answer
- **B.** The API is stateless, so earlier turns must be resent
- **C.** The session expired because the two calls were too far apart
- **D.** The temperature is too low for the model to recall context

??? success "Answer: B"
    **Why B is right:** Nothing is remembered between calls. The full history must be included in messages each time.

    **Why the others are wrong:**

    * **A:** A short exchange is nowhere near the window; the history was simply not sent.
    * **C:** There is no server-side session to expire.
    * **D:** Temperature affects sampling, not memory.

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

- **A.** Whether the API key is being rate limited on some requests
- **B.** Whether the system prompt is longer than the user prompt
- **C.** Whether stop_reason is max_tokens, meaning the output was cut off
- **D.** Whether the temperature is too high for producing JSON

??? success "Answer: C"
    **Why C is right:** A 200 only means the request was processed. Truncation is reported through stop_reason, and truncated JSON cannot parse.

    **Why the others are wrong:**

    * **A:** Rate limiting returns 429, not a 200 with partial content.
    * **B:** Relative prompt lengths have no bearing on truncated output.
    * **D:** Temperature may vary wording but would not cut the document off at the end.

---

<p class="qb-meta"><span class="qb-id">AI-006</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A response arrives with stop_reason "tool_use". What must the application do next?

- **A.** Repeat the same request until stop_reason is end_turn
- **B.** Increase max_tokens, because the response was truncated
- **C.** Run the tool and send a tool_result in a user turn
- **D.** Show the response text to the user as the final answer

??? success "Answer: C"
    **Why C is right:** tool_use means Claude is waiting for your code to execute the tool and return the result.

    **Why the others are wrong:**

    * **A:** Repeating the request without a tool result just produces the same tool call.
    * **B:** Truncation is reported as max_tokens, not tool_use.
    * **D:** The turn is not finished; Claude is waiting for a tool result.

---

<p class="qb-meta"><span class="qb-id">AI-007</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application uses a server-side web search tool. A response comes back with stop_reason "pause_turn". What is the correct handling?

- **A.** Execute the search in your own code and return a tool_result
- **B.** Treat it as a refusal and show an apology to the user
- **C.** Discard the response and start a new conversation
- **D.** Send the assistant content back so Claude can continue

??? success "Answer: D"
    **Why D is right:** pause_turn means a server-side tool loop paused. Returning the content unchanged lets it resume.

    **Why the others are wrong:**

    * **A:** Server tools run on the platform; there is no client tool call waiting.
    * **B:** A pause is not a refusal; the work is simply unfinished.
    * **C:** That throws away progress; the turn can be continued.

---

<p class="qb-meta"><span class="qb-id">AI-008</span><span>Stop reasons</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A request sets stop_sequences to ["###"]. The response has stop_reason "stop_sequence". Which statement is correct?

- **A.** Claude produced "###", and so generation stopped there
- **B.** The output was truncated by the max_tokens limit
- **C.** Claude declined to answer and used "###" as a marker
- **D.** The request failed validation because "###" is a reserved token

??? success "Answer: A"
    **Why A is right:** Custom stop sequences end generation, and the response reports the matched sequence.

    **Why the others are wrong:**

    * **B:** That would be reported as max_tokens.
    * **C:** Declining is reported as refusal.
    * **D:** It is a normal, successful response.

---

<p class="qb-meta"><span class="qb-id">AI-009</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A team streams responses so users see text immediately. A new developer claims this also halves the total generation time. What is accurate?

- **A.** Streaming is slower overall and should be avoided for chat
- **B.** Streaming speeds the first token, not the total time
- **C.** Streaming reduces cost because fewer tokens are billed
- **D.** Streaming halves total time because tokens are sent in parallel

??? success "Answer: B"
    **Why B is right:** Streaming changes when the user sees output, not how long generation takes.

    **Why the others are wrong:**

    * **A:** The overhead is negligible and perceived latency is far better.
    * **C:** Billing is identical for streamed and non-streamed responses.
    * **D:** Tokens are generated in sequence either way.

---

<p class="qb-meta"><span class="qb-id">AI-010</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

While streaming, in which event does the final stop_reason arrive?

- **A.** ping
- **B.** content_block_stop
- **C.** message_delta
- **D.** message_start

??? success "Answer: C"
    **Why C is right:** message_delta carries top-level changes such as stop_reason and final usage, just before message_stop.

    **Why the others are wrong:**

    * **A:** ping events are keep-alives with no message data.
    * **B:** That closes a single content block, not the message.
    * **D:** message_start opens the message; stop_reason is not known yet.

---

<p class="qb-meta"><span class="qb-id">AI-011</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

During a streamed response, a tool call's arguments arrive as several input_json_delta events. How should the application obtain the tool input?

- **A.** Ignore the deltas and read the input from message_start
- **B.** Wait for a tool_result event that contains the full input
- **C.** Parse each partial_json fragment as it arrives and merge the objects
- **D.** Concatenate the partial_json strings and parse once at content_block_stop

??? success "Answer: D"
    **Why D is right:** Each delta is a fragment of JSON. Only the accumulated string is valid JSON.

    **Why the others are wrong:**

    * **A:** message_start arrives before any tool input is generated.
    * **B:** tool_result is something your application sends, not something it receives.
    * **C:** Individual fragments are not valid JSON on their own.

---

<p class="qb-meta"><span class="qb-id">AI-012</span><span>Streaming</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A streaming request returns HTTP 200 and begins sending text. Thirty seconds later the stream ends with an error event. What does this show?

- **A.** The SDK has a bug, because a 200 response cannot contain an error
- **B.** The request was invalid and should have been rejected with a 400
- **C.** The content already received is corrupted and must be discarded silently
- **D.** Errors can occur mid-stream, so the client must cope

??? success "Answer: D"
    **Why D is right:** The status line is sent before generation finishes. Failures after that arrive as an error event in the stream.

    **Why the others are wrong:**

    * **A:** This is documented behaviour for streaming.
    * **B:** An invalid request is rejected before the stream starts.
    * **C:** The partial content is not corrupt; the application decides whether to retry or show it.

---

<p class="qb-meta"><span class="qb-id">AI-013</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service receives 400 invalid_request_error on some requests. A teammate proposes wrapping the call in a loop that retries up to five times. What is the best response?

- **A.** Don't retry: the request is malformed, so fix it
- **B.** Agree, but add exponential backoff between the attempts
- **C.** Retry once only, because the second attempt usually succeeds
- **D.** Agree, but switch to a larger model on the last attempt

??? success "Answer: A"
    **Why A is right:** Client errors of this type are deterministic. The same request will fail the same way.

    **Why the others are wrong:**

    * **B:** Backoff helps with overload, not with an invalid request.
    * **C:** Nothing changes between attempts, so it will not succeed.
    * **D:** The error is about the request format, not model capability.

---

<p class="qb-meta"><span class="qb-id">AI-014</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

During a traffic spike an application receives 429 rate_limit_error. What should it do first?

- **A.** Wait for the time given in the retry-after header, then retry
- **B.** Create a new API key so that the limit is reset
- **C.** Retry immediately in a tight loop until a request succeeds
- **D.** Report an error to users, because 429 cannot be retried

??? success "Answer: A"
    **Why A is right:** A 429 includes a retry-after header that says how long to wait.

    **Why the others are wrong:**

    * **B:** Limits apply to the organisation, not to a single key.
    * **C:** That makes the overload worse and prolongs the limit.
    * **D:** 429 is one of the retryable errors.

---

<p class="qb-meta"><span class="qb-id">AI-015</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

What does a 529 overloaded_error indicate, and how should code respond?

- **A.** The API is temporarily overloaded; retry with exponential backoff
- **B.** The request body is too large; shrink it before trying again
- **C.** The model ID does not exist; correct it before trying again
- **D.** The API key is invalid; replace it before trying again

??? success "Answer: A"
    **Why A is right:** 529 is a transient server-side condition and is safe to retry after a delay.

    **Why the others are wrong:**

    * **B:** That is 413 request_too_large.
    * **C:** That is 404 not_found_error.
    * **D:** That is 401 authentication_error.

---

<p class="qb-meta"><span class="qb-id">AI-016</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A newly deployed service gets 401 authentication_error on every call, while the same code works on the developer's laptop. What is the most likely cause?

- **A.** The deployed service is sending requests too quickly
- **B.** The API key is missing or wrong in that environment
- **C.** The model is overloaded in the deployment's region
- **D.** The prompt contains content that the model refuses

??? success "Answer: B"
    **Why B is right:** 401 means the key was not supplied or is not valid. Environment differences are the usual reason.

    **Why the others are wrong:**

    * **A:** That would produce 429.
    * **C:** That would produce 529.
    * **D:** A refusal is a 200 response with a stop_reason, not a 401.

---

<p class="qb-meta"><span class="qb-id">AI-017</span><span>Errors</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A client uploads a very large PDF inline and the API returns 413. Which action addresses the cause?

- **A.** Retry with exponential backoff until the request is accepted
- **B.** Reduce the request size, for example by splitting the document
- **C.** Raise max_tokens so that the model can read the whole file
- **D.** Switch to streaming so that the upload is sent in chunks

??? success "Answer: B"
    **Why B is right:** 413 request_too_large means the body exceeds the size limit. Only a smaller request helps.

    **Why the others are wrong:**

    * **A:** The request will be too large every time.
    * **C:** max_tokens limits output; it does not affect request size.
    * **D:** Streaming affects the response, not the size of the request.

---

<p class="qb-meta"><span class="qb-id">AI-018</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A developer wraps every SDK call in a custom loop that retries five times on failure. During an outage, each user action produces far more API calls than expected. Why?

- **A.** The API duplicates every request during an outage
- **B.** The SDK retries by default, so layers multiply
- **C.** Each retry is billed as a batch of one hundred requests
- **D.** The SDK opens one connection per token it generates

??? success "Answer: B"
    **Why B is right:** The official SDKs retry transient errors twice by default. An outer loop multiplies that.

    **Why the others are wrong:**

    * **A:** The API does not duplicate requests.
    * **C:** Retries are ordinary single requests.
    * **D:** Connections are not opened per token.

---

<p class="qb-meta"><span class="qb-id">AI-019</span><span>SDK behaviour</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A non-streaming request that generates a very long document fails intermittently with timeouts and dropped connections. What is the recommended change?

- **A.** Lower max_tokens to 256 so that responses return quickly
- **B.** Set max_retries to zero so that the failure surfaces sooner
- **C.** Use streaming, so that data flows continuously during generation
- **D.** Send the request twice in parallel and keep the faster one

??? success "Answer: C"
    **Why C is right:** Long idle connections are fragile. Streaming keeps the connection active and is recommended for long outputs.

    **Why the others are wrong:**

    * **A:** That would truncate the document the task needs.
    * **B:** That removes recovery without fixing the cause.
    * **D:** That doubles cost and still risks both timing out.

---

<p class="qb-meta"><span class="qb-id">AI-020</span><span>Observability</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A customer reports a strange answer from yesterday. Which logged value is most useful when asking Anthropic support to investigate that specific call?

- **A.** The first eight characters of the API key
- **B.** The temperature value used for the request
- **C.** The request ID returned in the response headers
- **D.** The local timestamp of the user's click

??? success "Answer: C"
    **Why C is right:** Every response has a unique request-id that identifies the exact call.

    **Why the others are wrong:**

    * **A:** Key fragments identify the account, not a single request.
    * **B:** A parameter value does not identify a request.
    * **D:** Timestamps are imprecise and not unique.

---

<p class="qb-meta"><span class="qb-id">AI-021</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A dashboard shows average usage at 60% of the requests-per-minute limit, yet the application still receives occasional 429 errors at the top of each hour when a scheduled job starts. Why?

- **A.** 429 is returned at random to keep usage below 50%
- **B.** Scheduled jobs are counted twice against the limit
- **C.** Rate limits are reset to zero at the start of each hour
- **D.** A token bucket lets a sudden burst exceed capacity

??? success "Answer: D"
    **Why D is right:** The limit is not a simple per-minute counter. Short bursts can drain the bucket even when the average is low.

    **Why the others are wrong:**

    * **A:** Limits are deterministic, not random.
    * **B:** Requests are counted once regardless of origin.
    * **C:** There is no hourly reset that lowers capacity.

---

<p class="qb-meta"><span class="qb-id">AI-022</span><span>Rate limits</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

An application with a large, repeated system prompt keeps hitting its input-tokens-per-minute limit. Which change raises effective throughput without asking for higher limits?

- **A.** Raise the temperature, since it reduces the tokens processed
- **B.** Enable streaming, since streamed tokens are not rate limited
- **C.** Lower max_tokens, since it is counted against the input limit
- **D.** Cache the prompt, since cached reads are mostly exempt

??? success "Answer: D"
    **Why D is right:** On most current models cache_read_input_tokens are excluded from ITPM, so caching increases throughput.

    **Why the others are wrong:**

    * **A:** Temperature does not change token counts.
    * **B:** Streaming does not change rate-limit accounting.
    * **C:** max_tokens concerns output and is not counted against input limits.

---

<p class="qb-meta"><span class="qb-id">AI-023</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Before sending a request that includes a long document, a service wants to know whether it will fit and which model to route it to. What is the best approach?

- **A.** Divide the character count by ten to estimate the tokens
- **B.** Send the request and read usage from the error response
- **C.** Call the token counting endpoint before sending
- **D.** Set max_tokens to zero to get a free dry run

??? success "Answer: C"
    **Why C is right:** count_tokens accepts the same system, messages and tools as a real request and returns the input token count at no charge.

    **Why the others are wrong:**

    * **A:** A crude ratio is unreliable, especially with tools, images or non-English text.
    * **B:** That wastes a call and may fail or cost money.
    * **D:** max_tokens must be positive; this is not a dry-run mechanism.

---

<p class="qb-meta"><span class="qb-id">AI-024</span><span>Token counting</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Which statement about the token counting endpoint is correct?

- **A.** It is free, separately limited, and gives an estimate
- **B.** It only supports plain text and rejects tools or images
- **C.** It returns both the input tokens and the predicted output tokens
- **D.** It is billed at the input rate and shares the Messages rate limit

??? success "Answer: A"
    **Why A is right:** Counting does not generate output, is not billed, and is limited separately from message creation.

    **Why the others are wrong:**

    * **B:** It accepts the same structured inputs as a message request.
    * **C:** Output length is not known before generation.
    * **D:** It is free and separately limited.

---

<p class="qb-meta"><span class="qb-id">AI-025</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A team submits 5,000 requests in one message batch and reads the results file line by line, assuming line N answers request N. Some answers end up attached to the wrong records. What is the fix?

- **A.** Add a sequence number to each prompt and ask Claude to repeat it
- **B.** Sort the results by their completion timestamp
- **C.** Submit the requests in smaller batches of exactly 100
- **D.** Match each result to its request using custom_id

??? success "Answer: D"
    **Why D is right:** Batch results are not guaranteed to be in submission order. custom_id exists for matching.

    **Why the others are wrong:**

    * **A:** Fragile and unnecessary when custom_id is provided.
    * **B:** Completion time does not reflect submission order.
    * **C:** Batch size does not make the order reliable.

---

<p class="qb-meta"><span class="qb-id">AI-026</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

Every night a company summarises 60,000 product reviews. Results are needed by the next morning. Which approach is most cost-effective?

- **A.** The Message Batches API, since nobody is waiting on each result
- **B.** Synchronous calls using the most capable model available
- **C.** Synchronous calls with streaming enabled for every review
- **D.** One request containing all 60,000 reviews in a single prompt

??? success "Answer: A"
    **Why A is right:** Batches are asynchronous and half the price, which suits large offline jobs.

    **Why the others are wrong:**

    * **B:** That maximises cost with no stated quality need.
    * **C:** Streaming helps a waiting user, not an overnight job.
    * **D:** It would exceed limits and give poor per-review results.

---

<p class="qb-meta"><span class="qb-id">AI-027</span><span>Batches</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

To cut costs, a product manager suggests sending live customer chat messages through the Message Batches API. What is the main problem?

- **A.** Batches can only be submitted once per day
- **B.** Batches are asynchronous and may take hours to finish
- **C.** Batches cost more per token than synchronous calls
- **D.** Batches do not support system prompts or tools

??? success "Answer: B"
    **Why B is right:** A batch has no latency guarantee beyond finishing within its processing window.

    **Why the others are wrong:**

    * **A:** There is no such restriction.
    * **C:** They cost less, about half.
    * **D:** Batch requests accept normal Messages parameters.

---

<p class="qb-meta"><span class="qb-id">AI-028</span><span>Errors</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO errors are appropriate to retry automatically with backoff? (Select TWO.)

- **A.** 404 not_found_error
- **B.** 400 invalid_request_error
- **C.** 429 rate_limit_error
- **D.** 529 overloaded_error
- **E.** 401 authentication_error

??? success "Answer: C and D"
    **Why C is right:** Rate limiting is temporary; wait and retry.

    **Why D is right:** Overload is temporary; back off and retry.

    **Why the others are wrong:**

    * **A:** The resource or model does not exist; retrying cannot fix it.
    * **B:** The request is malformed and will fail again.
    * **E:** The key is wrong; retrying cannot fix it.

---

<p class="qb-meta"><span class="qb-id">AI-029</span><span>Request shape</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

Which TWO statements about the Messages API are correct? (Select TWO.)

- **A.** A 200 status guarantees that the answer is complete
- **B.** The system prompt is supplied as a top-level parameter
- **C.** The application must resend prior turns to continue a conversation
- **D.** max_tokens sets the minimum length of the response
- **E.** The API stores each conversation for 24 hours by default

??? success "Answer: B and C"
    **Why B is right:** system is not a role inside messages.

    **Why C is right:** The API is stateless.

    **Why the others are wrong:**

    * **A:** stop_reason may still indicate truncation.
    * **D:** It is an upper limit on output.
    * **E:** No conversation state is kept between calls.

---

<p class="qb-meta"><span class="qb-id">AI-030</span><span>Request shape</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A developer sets max_tokens to 4,000 hoping for longer, more detailed answers, but replies remain short. Why?

- **A.** Values above 1,024 are silently reduced by the API
- **B.** max_tokens is a cap; ask for length in the prompt
- **C.** The value is ignored unless streaming is enabled
- **D.** max_tokens applies to the input rather than the output

??? success "Answer: B"
    **Why B is right:** The parameter caps output. It does not instruct the model to write more.

    **Why the others are wrong:**

    * **A:** Models support much larger outputs.
    * **C:** It applies to streamed and non-streamed responses alike.
    * **D:** It limits output tokens.

---

<p class="qb-meta"><span class="qb-id">AI-031</span><span>Conversation history</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In an agent loop, a developer appends only the text of each assistant response to the history and discards the other blocks. The next request fails with an error about a tool_result. Why?

- **A.** Text blocks must be removed from history before tool results
- **B.** tool_result blocks are only valid in the system parameter
- **C.** The matching tool_use block is missing from the history
- **D.** The history exceeded the limit of ten messages per request

??? success "Answer: C"
    **Why C is right:** A tool_result must follow an assistant message that contains the matching tool_use block.

    **Why the others are wrong:**

    * **A:** Text blocks are allowed alongside tool_use blocks.
    * **B:** They belong in a user message.
    * **D:** There is no such ten-message limit.

---

<p class="qb-meta"><span class="qb-id">AI-032</span><span>Choosing a pattern</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A pipeline always performs the same three steps: translate a document, summarise it, then format the summary as HTML. A teammate proposes an autonomous agent with tools for each step. What is the better design?

- **A.** A single agent with a higher turn limit to explore options
- **B.** One very long prompt that asks for all three results at once
- **C.** A prompt chain run by application code, with a check between steps
- **D.** A multi-agent system with one agent for each of the steps

??? success "Answer: C"
    **Why C is right:** When steps are fixed and known, a workflow is cheaper, faster and more predictable than an agent.

    **Why the others are wrong:**

    * **A:** Autonomy adds unpredictability where none is needed.
    * **B:** Harder to validate and debug than separate steps.
    * **D:** Extra coordination cost with no benefit for a fixed sequence.

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

- **A.** Raise the temperature so that the model recalls more detail
- **B.** Paste the full library into the system prompt on every request
- **C.** Rely on the model's training data to know the policies
- **D.** Retrieve relevant passages and add them to the prompt

??? success "Answer: D"
    **Why D is right:** Retrieval supplies current, relevant content without sending everything every time.

    **Why the others are wrong:**

    * **A:** Temperature does not add knowledge.
    * **B:** Likely too large, slow and costly.
    * **C:** The model has never seen private, changing documents.

---

<p class="qb-meta"><span class="qb-id">AI-035</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A web chat application needs multi-turn conversations. Where should conversation history be kept?

- **A.** In a server-side store keyed by the application's own session ID
- **B.** In the Claude API, retrieved with the previous message ID
- **C.** In the system prompt, appended to after every turn
- **D.** Nowhere, since the model retains recent conversations

??? success "Answer: A"
    **Why A is right:** The application owns state. A backend store lets it reload and resend history securely.

    **Why the others are wrong:**

    * **B:** The API does not store conversations for retrieval.
    * **C:** History belongs in messages; rewriting the system prompt also defeats caching.
    * **D:** The model retains nothing between calls.

---

<p class="qb-meta"><span class="qb-id">AI-036</span><span>Session handling</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

Two browser tabs for the same user send messages to the same conversation at almost the same moment. Afterwards the stored history has turns out of order and one reply is missing. What should be added?

- **A.** A lower temperature so that both replies are identical
- **B.** Per-session locking when the history is updated
- **C.** A longer max_tokens so that neither reply is dropped
- **D.** A second API key so that the two tabs do not collide

??? success "Answer: B"
    **Why B is right:** It is an ordinary concurrent-write problem on shared state, solved with ordinary concurrency control.

    **Why the others are wrong:**

    * **A:** Sampling settings cannot fix a race condition.
    * **C:** The reply was lost in storage, not truncated.
    * **D:** Keys are unrelated to writes to your own store.

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

- **A.** Add twenty more categories to cover every case
- **B.** Remove the enum and accept any free-text category
- **C.** Add an "other" value, with a short free-text field for the detail
- **D.** Send each ticket three times and take the majority label

??? success "Answer: C"
    **Why C is right:** An escape value stops the model from being forced into a wrong label.

    **Why the others are wrong:**

    * **A:** Large enums are harder to choose from and never cover everything.
    * **B:** That loses the consistency the enum provides.
    * **D:** Voting between wrong labels does not produce a right one.

---

<p class="qb-meta"><span class="qb-id">AI-040</span><span>Validation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An invoice extractor uses structured outputs, so every response matches the schema. Finance finds invoices where the line items do not add up to the stated total. What is missing?

- **A.** A higher max_tokens value so that totals are not truncated
- **B.** A semantic check in code that lines sum to the total
- **C.** A system prompt reminder that totals must be accurate
- **D.** A stricter schema with additionalProperties set to false

??? success "Answer: B"
    **Why B is right:** A schema guarantees structure, not correctness. Business rules need their own validation.

    **Why the others are wrong:**

    * **A:** Nothing was truncated.
    * **C:** A reminder is not verification.
    * **D:** The structure was already valid; the values were wrong.

---

<p class="qb-meta"><span class="qb-id">AI-041</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

After a timeout, a workflow retried a step, and a customer was refunded twice. Which design principle prevents this?

- **A.** Increase the timeout to ten minutes for every call
- **B.** Make the side effect idempotent, using an idempotency key
- **C.** Disable all retries across the whole application
- **D.** Ask the model to remember which refunds it has issued

??? success "Answer: B"
    **Why B is right:** With an idempotency key, a repeated attempt is recognised and not executed again.

    **Why the others are wrong:**

    * **A:** Timeouts can still occur; duplicates remain possible.
    * **C:** That sacrifices resilience; the issue is the repeated side effect.
    * **D:** Model memory is not a reliable transaction record.

---

<p class="qb-meta"><span class="qb-id">AI-042</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

The Claude API has been returning errors for several minutes. Every user request waits through multiple retries and then fails. What should the application do instead?

- **A.** Increase the retry count so that requests eventually pass
- **B.** Return an empty reply so that users don't see any error
- **C.** Remove the timeout so that requests can wait as long as needed
- **D.** Stop calling after repeated failures and fall back

??? success "Answer: D"
    **Why D is right:** A circuit breaker with graceful degradation avoids piling up slow, doomed requests.

    **Why the others are wrong:**

    * **A:** More retries deepen the pile-up during an outage.
    * **B:** Silent empty answers hide the failure and confuse users.
    * **C:** Hanging requests exhaust resources and frustrate users.

---

<p class="qb-meta"><span class="qb-id">AI-043</span><span>Reliability</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A marketing campaign sends bursts of thousands of requests within a few seconds, causing many 429 errors, although total daily volume is well within limits. Which design smooths this out?

- **A.** Open more connections so that the burst finishes sooner
- **B.** Disable SDK retries so that failures return faster
- **C.** Put requests on a queue and process them at a controlled rate
- **D.** Raise max_tokens so that each request does more work

??? success "Answer: C"
    **Why C is right:** A queue absorbs bursts and feeds the API at a steady pace.

    **Why the others are wrong:**

    * **A:** That intensifies the burst.
    * **B:** Requests would simply fail instead of completing.
    * **D:** It does not reduce the request rate.

---

<p class="qb-meta"><span class="qb-id">AI-044</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A model ID is hard-coded in forty source files. A newer model must now be adopted. Which practice would have made this a small change?

- **A.** Storing the model ID inside the system prompt text
- **B.** Letting each developer choose the model on their machine
- **C.** Keeping the model ID in configuration, read by all the call sites
- **D.** Using a different model ID in every file for flexibility

??? success "Answer: C"
    **Why C is right:** Configuration lets the model change without editing code across the codebase.

    **Why the others are wrong:**

    * **A:** The prompt does not select the model.
    * **B:** Uncontrolled variation between environments.
    * **D:** That makes the system even harder to manage.

---

<p class="qb-meta"><span class="qb-id">AI-045</span><span>Configuration</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

Production behaviour changed slightly overnight with no deployment. The service uses a model alias that always points to the newest version. What is the recommended practice?

- **A.** Pin a specific model version and upgrade deliberately after testing
- **B.** Switch aliases every day to average out the differences
- **C.** Keep the alias and add more few-shot examples each week
- **D.** Keep the alias and lower the temperature to stabilise output

??? success "Answer: A"
    **Why A is right:** A moving alias can change behaviour without warning. Pinning makes upgrades a tested release.

    **Why the others are wrong:**

    * **B:** That adds variation rather than removing it.
    * **C:** Examples do not prevent the underlying model from changing.
    * **D:** Sampling settings do not prevent a model change.

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

- **A.** The average temperature across all the requests
- **B.** The count of developers who can access the API key
- **C.** The number of lines in the system prompt each week
- **D.** Error rates, latency, token cost, validation failures

??? success "Answer: D"
    **Why D is right:** Together these cover reliability, speed, spend and output quality.

    **Why the others are wrong:**

    * **A:** A configuration value, not an outcome.
    * **B:** An access-control fact, not a health metric.
    * **C:** Prompt length says nothing about behaviour in production.

---

<p class="qb-meta"><span class="qb-id">AI-048</span><span>Access control</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a multi-tenant application, a user of one company receives an answer that quotes another company's document. Where is the flaw?

- **A.** Retrieval was not scoped to the authenticated user's tenant
- **B.** The model's context window was too large
- **C.** The system prompt did not forbid sharing documents
- **D.** The temperature allowed the model to be creative

??? success "Answer: A"
    **Why A is right:** Isolation must be enforced when data is fetched, before anything reaches the prompt.

    **Why the others are wrong:**

    * **B:** Window size does not select which documents are retrieved.
    * **C:** A prompt rule cannot undo data that was already supplied.
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
- **B.** Whether the developers prefer Python or TypeScript
- **C.** Whether a delay of up to several hours is acceptable
- **D.** Whether the system prompt uses XML tags or Markdown
- **E.** Whether the prompts are written in British or American English

??? success "Answer: A and C"
    **Why A is right:** Batches are asynchronous, so waiting users rule them out.

    **Why C is right:** Batch completion time is not immediate.

    **Why the others are wrong:**

    * **B:** Both SDKs support both modes.
    * **D:** Prompt formatting does not affect the choice.
    * **E:** Spelling variety has no bearing on the choice.

---
