from devlib import Q, M

# ================= Applications & Integration: API mechanics =================

Q("AI", "Request shape", """
A developer adds {"role": "system", "content": "You are a helpful travel assistant."} as the first item in the messages list and receives a 400 error. What is the correct fix?""",
  "Move the text to the top-level system parameter of the request",
  "System prompts are a top-level parameter. The messages list only accepts user and assistant roles.",
  [("Rename the role to \"developer\" and send the request again", "There is no developer role in the Messages API."),
   ("Place the system message last so that it takes priority", "Position does not matter; the role itself is not accepted."),
   ("Send the system text in a custom HTTP request header", "Headers carry authentication and versioning, not prompt content.")], level=1)

Q("AI", "Request shape", """
Which set of fields is required in every Messages API request?""",
  "model, max_tokens and messages",
  "These three are mandatory. Everything else, including system and temperature, is optional.",
  [("model, system and messages", "system is optional, and max_tokens is missing."),
   ("model, messages and temperature", "temperature is optional, and max_tokens is missing."),
   ("model, max_tokens and stream", "stream is optional, and messages is missing.")], level=1)

Q("AI", "Statelessness", """
A chatbot answers the first question well, but when the user follows up with "and what about the second one?", Claude has no idea what "the second one" refers to. The code sends only the newest user message on each call. What is the cause?""",
  "The API is stateless, so earlier turns must be resent",
  "Nothing is remembered between calls. The full history must be included in messages each time.",
  [("The session expired because the two calls were too far apart", "There is no server-side session to expire."),
   ("The model's context window was exceeded by the first answer", "A short exchange is nowhere near the window; the history was simply not sent."),
   ("The temperature is too low for the model to recall context", "Temperature affects sampling, not memory.")], level=1)

Q("AI", "Response shape", """
This line works in testing but raises an exception in production after tools are added to the request:

    answer = response.content[0].text

What is the most likely reason?""",
  "The first block is sometimes tool_use, without text",
  "content is a list of typed blocks. Code must check each block's type rather than assume the first is text.",
  [("The response body is returned as a string once tools are enabled", "The response shape is unchanged; content remains a list of blocks."),
   ("Tool-enabled responses place the text in response.completion", "There is no completion field in the Messages API response."),
   ("The SDK needs an additional await when tools are present", "Whether a call is awaited depends on the client type, not on tools.")])

Q("AI", "Stop reasons", """
A report generator asks for a long JSON document. About one request in twenty fails with a JSON parse error near the end of the text. The HTTP status is always 200. What should the developer check first?""",
  "Whether stop_reason is max_tokens, meaning the output was cut off",
  "A 200 only means the request was processed. Truncation is reported through stop_reason, and truncated JSON cannot parse.",
  [("Whether the temperature is too high for producing JSON", "Temperature may vary wording but would not cut the document off at the end."),
   ("Whether the API key is being rate limited on some requests", "Rate limiting returns 429, not a 200 with partial content."),
   ("Whether the system prompt is longer than the user prompt", "Relative prompt lengths have no bearing on truncated output.")])

Q("AI", "Stop reasons", """
A response arrives with stop_reason "tool_use". What must the application do next?""",
  "Run the tool and send a tool_result in a user turn",
  "tool_use means Claude is waiting for your code to execute the tool and return the result.",
  [("Show the response text to the user as the final answer", "The turn is not finished; Claude is waiting for a tool result."),
   ("Repeat the same request until stop_reason is end_turn", "Repeating the request without a tool result just produces the same tool call."),
   ("Increase max_tokens, because the response was truncated", "Truncation is reported as max_tokens, not tool_use.")], level=1)

Q("AI", "Stop reasons", """
An application uses a server-side web search tool. A response comes back with stop_reason "pause_turn". What is the correct handling?""",
  "Send the assistant content back so Claude can continue",
  "pause_turn means a server-side tool loop paused. Returning the content unchanged lets it resume.",
  [("Treat it as a refusal and show an apology to the user", "A pause is not a refusal; the work is simply unfinished."),
   ("Execute the search in your own code and return a tool_result", "Server tools run on the platform; there is no client tool call waiting."),
   ("Discard the response and start a new conversation", "That throws away progress; the turn can be continued.")], level=3)

Q("AI", "Stop reasons", """
A request sets stop_sequences to ["###"]. The response has stop_reason "stop_sequence". Which statement is correct?""",
  "Claude produced \"###\", and so generation stopped there",
  "Custom stop sequences end generation, and the response reports the matched sequence.",
  [("The request failed validation because \"###\" is a reserved token", "It is a normal, successful response."),
   ("The output was truncated by the max_tokens limit", "That would be reported as max_tokens."),
   ("Claude declined to answer and used \"###\" as a marker", "Declining is reported as refusal.")], level=1)

Q("AI", "Streaming", """
A team streams responses so users see text immediately. A new developer claims this also halves the total generation time. What is accurate?""",
  "Streaming speeds the first token, not the total time",
  "Streaming changes when the user sees output, not how long generation takes.",
  [("Streaming halves total time because tokens are sent in parallel", "Tokens are generated in sequence either way."),
   ("Streaming is slower overall and should be avoided for chat", "The overhead is negligible and perceived latency is far better."),
   ("Streaming reduces cost because fewer tokens are billed", "Billing is identical for streamed and non-streamed responses.")], level=1)

Q("AI", "Streaming", """
While streaming, in which event does the final stop_reason arrive?""",
  "message_delta",
  "message_delta carries top-level changes such as stop_reason and final usage, just before message_stop.",
  [("message_start", "message_start opens the message; stop_reason is not known yet."),
   ("content_block_stop", "That closes a single content block, not the message."),
   ("ping", "ping events are keep-alives with no message data.")])

Q("AI", "Streaming", """
During a streamed response, a tool call's arguments arrive as several input_json_delta events. How should the application obtain the tool input?""",
  "Concatenate the partial_json strings and parse once at content_block_stop",
  "Each delta is a fragment of JSON. Only the accumulated string is valid JSON.",
  [("Parse each partial_json fragment as it arrives and merge the objects", "Individual fragments are not valid JSON on their own."),
   ("Ignore the deltas and read the input from message_start", "message_start arrives before any tool input is generated."),
   ("Wait for a tool_result event that contains the full input", "tool_result is something your application sends, not something it receives.")])

Q("AI", "Streaming", """
A streaming request returns HTTP 200 and begins sending text. Thirty seconds later the stream ends with an error event. What does this show?""",
  "Errors can occur mid-stream, so the client must cope",
  "The status line is sent before generation finishes. Failures after that arrive as an error event in the stream.",
  [("The SDK has a bug, because a 200 response cannot contain an error", "This is documented behaviour for streaming."),
   ("The request was invalid and should have been rejected with a 400", "An invalid request is rejected before the stream starts."),
   ("The content already received is corrupted and must be discarded silently", "The partial content is not corrupt; the application decides whether to retry or show it.")], level=3)

Q("AI", "Errors", """
A service receives 400 invalid_request_error on some requests. A teammate proposes wrapping the call in a loop that retries up to five times. What is the best response?""",
  "Don't retry: the request is malformed, so fix it",
  "Client errors of this type are deterministic. The same request will fail the same way.",
  [("Agree, but add exponential backoff between the attempts", "Backoff helps with overload, not with an invalid request."),
   ("Agree, but switch to a larger model on the last attempt", "The error is about the request format, not model capability."),
   ("Retry once only, because the second attempt usually succeeds", "Nothing changes between attempts, so it will not succeed.")], level=1)

Q("AI", "Errors", """
During a traffic spike an application receives 429 rate_limit_error. What should it do first?""",
  "Wait for the time given in the retry-after header, then retry",
  "A 429 includes a retry-after header that says how long to wait.",
  [("Retry immediately in a tight loop until a request succeeds", "That makes the overload worse and prolongs the limit."),
   ("Create a new API key so that the limit is reset", "Limits apply to the organisation, not to a single key."),
   ("Report an error to users, because 429 cannot be retried", "429 is one of the retryable errors.")], level=1)

Q("AI", "Errors", """
What does a 529 overloaded_error indicate, and how should code respond?""",
  "The API is temporarily overloaded; retry with exponential backoff",
  "529 is a transient server-side condition and is safe to retry after a delay.",
  [("The request body is too large; shrink it before trying again", "That is 413 request_too_large."),
   ("The API key is invalid; replace it before trying again", "That is 401 authentication_error."),
   ("The model ID does not exist; correct it before trying again", "That is 404 not_found_error.")])

Q("AI", "Errors", """
A newly deployed service gets 401 authentication_error on every call, while the same code works on the developer's laptop. What is the most likely cause?""",
  "The API key is missing or wrong in that environment",
  "401 means the key was not supplied or is not valid. Environment differences are the usual reason.",
  [("The deployed service is sending requests too quickly", "That would produce 429."),
   ("The model is overloaded in the deployment's region", "That would produce 529."),
   ("The prompt contains content that the model refuses", "A refusal is a 200 response with a stop_reason, not a 401.")], level=1)

Q("AI", "Errors", """
A client uploads a very large PDF inline and the API returns 413. Which action addresses the cause?""",
  "Reduce the request size, for example by splitting the document",
  "413 request_too_large means the body exceeds the size limit. Only a smaller request helps.",
  [("Retry with exponential backoff until the request is accepted", "The request will be too large every time."),
   ("Raise max_tokens so that the model can read the whole file", "max_tokens limits output; it does not affect request size."),
   ("Switch to streaming so that the upload is sent in chunks", "Streaming affects the response, not the size of the request.")])

Q("AI", "SDK behaviour", """
A developer wraps every SDK call in a custom loop that retries five times on failure. During an outage, each user action produces far more API calls than expected. Why?""",
  "The SDK retries by default, so layers multiply",
  "The official SDKs retry transient errors twice by default. An outer loop multiplies that.",
  [("The SDK opens one connection per token it generates", "Connections are not opened per token."),
   ("Each retry is billed as a batch of one hundred requests", "Retries are ordinary single requests."),
   ("The API duplicates every request during an outage", "The API does not duplicate requests.")])

Q("AI", "SDK behaviour", """
A non-streaming request that generates a very long document fails intermittently with timeouts and dropped connections. What is the recommended change?""",
  "Use streaming, so that data flows continuously during generation",
  "Long idle connections are fragile. Streaming keeps the connection active and is recommended for long outputs.",
  [("Lower max_tokens to 256 so that responses return quickly", "That would truncate the document the task needs."),
   ("Set max_retries to zero so that the failure surfaces sooner", "That removes recovery without fixing the cause."),
   ("Send the request twice in parallel and keep the faster one", "That doubles cost and still risks both timing out.")])

Q("AI", "Observability", """
A customer reports a strange answer from yesterday. Which logged value is most useful when asking Anthropic support to investigate that specific call?""",
  "The request ID returned in the response headers",
  "Every response has a unique request-id that identifies the exact call.",
  [("The first eight characters of the API key", "Key fragments identify the account, not a single request."),
   ("The temperature value used for the request", "A parameter value does not identify a request."),
   ("The local timestamp of the user's click", "Timestamps are imprecise and not unique.")], level=1)

Q("AI", "Rate limits", """
A dashboard shows average usage at 60% of the requests-per-minute limit, yet the application still receives occasional 429 errors at the top of each hour when a scheduled job starts. Why?""",
  "A token bucket lets a sudden burst exceed capacity",
  "The limit is not a simple per-minute counter. Short bursts can drain the bucket even when the average is low.",
  [("Rate limits are reset to zero at the start of each hour", "There is no hourly reset that lowers capacity."),
   ("Scheduled jobs are counted twice against the limit", "Requests are counted once regardless of origin."),
   ("429 is returned at random to keep usage below 50%", "Limits are deterministic, not random.")], level=3)

Q("AI", "Rate limits", """
An application with a large, repeated system prompt keeps hitting its input-tokens-per-minute limit. Which change raises effective throughput without asking for higher limits?""",
  "Cache the prompt, since cached reads are mostly exempt",
  "On most current models cache_read_input_tokens are excluded from ITPM, so caching increases throughput.",
  [("Lower max_tokens, since it is counted against the input limit", "max_tokens concerns output and is not counted against input limits."),
   ("Enable streaming, since streamed tokens are not rate limited", "Streaming does not change rate-limit accounting."),
   ("Raise the temperature, since it reduces the tokens processed", "Temperature does not change token counts.")], level=3)

Q("AI", "Token counting", """
Before sending a request that includes a long document, a service wants to know whether it will fit and which model to route it to. What is the best approach?""",
  "Call the token counting endpoint before sending",
  "count_tokens accepts the same system, messages and tools as a real request and returns the input token count at no charge.",
  [("Divide the character count by ten to estimate the tokens", "A crude ratio is unreliable, especially with tools, images or non-English text."),
   ("Send the request and read usage from the error response", "That wastes a call and may fail or cost money."),
   ("Set max_tokens to zero to get a free dry run", "max_tokens must be positive; this is not a dry-run mechanism.")], level=1)

Q("AI", "Token counting", """
Which statement about the token counting endpoint is correct?""",
  "It is free, separately limited, and gives an estimate",
  "Counting does not generate output, is not billed, and is limited separately from message creation.",
  [("It is billed at the input rate and shares the Messages rate limit", "It is free and separately limited."),
   ("It returns both the input tokens and the predicted output tokens", "Output length is not known before generation."),
   ("It only supports plain text and rejects tools or images", "It accepts the same structured inputs as a message request.")])

Q("AI", "Batches", """
A team submits 5,000 requests in one message batch and reads the results file line by line, assuming line N answers request N. Some answers end up attached to the wrong records. What is the fix?""",
  "Match each result to its request using custom_id",
  "Batch results are not guaranteed to be in submission order. custom_id exists for matching.",
  [("Submit the requests in smaller batches of exactly 100", "Batch size does not make the order reliable."),
   ("Sort the results by their completion timestamp", "Completion time does not reflect submission order."),
   ("Add a sequence number to each prompt and ask Claude to repeat it", "Fragile and unnecessary when custom_id is provided.")])

Q("AI", "Batches", """
Every night a company summarises 60,000 product reviews. Results are needed by the next morning. Which approach is most cost-effective?""",
  "The Message Batches API, since nobody is waiting on each result",
  "Batches are asynchronous and half the price, which suits large offline jobs.",
  [("Synchronous calls with streaming enabled for every review", "Streaming helps a waiting user, not an overnight job."),
   ("Synchronous calls using the most capable model available", "That maximises cost with no stated quality need."),
   ("One request containing all 60,000 reviews in a single prompt", "It would exceed limits and give poor per-review results.")], level=1)

Q("AI", "Batches", """
To cut costs, a product manager suggests sending live customer chat messages through the Message Batches API. What is the main problem?""",
  "Batches are asynchronous and may take hours to finish",
  "A batch has no latency guarantee beyond finishing within its processing window.",
  [("Batches do not support system prompts or tools", "Batch requests accept normal Messages parameters."),
   ("Batches cost more per token than synchronous calls", "They cost less, about half."),
   ("Batches can only be submitted once per day", "There is no such restriction.")])

M("AI", "Errors", """
Which TWO errors are appropriate to retry automatically with backoff? (Select TWO.)""",
  [("429 rate_limit_error", "Rate limiting is temporary; wait and retry."),
   ("529 overloaded_error", "Overload is temporary; back off and retry.")],
  [("400 invalid_request_error", "The request is malformed and will fail again."),
   ("401 authentication_error", "The key is wrong; retrying cannot fix it."),
   ("404 not_found_error", "The resource or model does not exist; retrying cannot fix it.")])

M("AI", "Request shape", """
Which TWO statements about the Messages API are correct? (Select TWO.)""",
  [("The system prompt is supplied as a top-level parameter", "system is not a role inside messages."),
   ("The application must resend prior turns to continue a conversation", "The API is stateless.")],
  [("The API stores each conversation for 24 hours by default", "No conversation state is kept between calls."),
   ("max_tokens sets the minimum length of the response", "It is an upper limit on output."),
   ("A 200 status guarantees that the answer is complete", "stop_reason may still indicate truncation.")])

Q("AI", "Request shape", """
A developer sets max_tokens to 4,000 hoping for longer, more detailed answers, but replies remain short. Why?""",
  "max_tokens is a cap; ask for length in the prompt",
  "The parameter caps output. It does not instruct the model to write more.",
  [("max_tokens applies to the input rather than the output", "It limits output tokens."),
   ("The value is ignored unless streaming is enabled", "It applies to streamed and non-streamed responses alike."),
   ("Values above 1,024 are silently reduced by the API", "Models support much larger outputs.")], level=1)

Q("AI", "Conversation history", """
In an agent loop, a developer appends only the text of each assistant response to the history and discards the other blocks. The next request fails with an error about a tool_result. Why?""",
  "The matching tool_use block is missing from the history",
  "A tool_result must follow an assistant message that contains the matching tool_use block.",
  [("Text blocks must be removed from history before tool results", "Text blocks are allowed alongside tool_use blocks."),
   ("The history exceeded the limit of ten messages per request", "There is no such ten-message limit."),
   ("tool_result blocks are only valid in the system parameter", "They belong in a user message.")])

# ================= Applications & Integration: application design =================

Q("AI", "Choosing a pattern", """
A pipeline always performs the same three steps: translate a document, summarise it, then format the summary as HTML. A teammate proposes an autonomous agent with tools for each step. What is the better design?""",
  "A prompt chain run by application code, with a check between steps",
  "When steps are fixed and known, a workflow is cheaper, faster and more predictable than an agent.",
  [("A multi-agent system with one agent for each of the steps", "Extra coordination cost with no benefit for a fixed sequence."),
   ("A single agent with a higher turn limit to explore options", "Autonomy adds unpredictability where none is needed."),
   ("One very long prompt that asks for all three results at once", "Harder to validate and debug than separate steps.")])

Q("AI", "Choosing a pattern", """
A help desk receives billing questions, technical faults and sales enquiries. Each type needs different instructions and tools. Which pattern fits best?""",
  "Routing: classify each message, then send it to a specialised prompt",
  "Routing separates concerns, so each path can be tuned without harming the others.",
  [("Evaluator-optimiser: draft a reply, then critique and revise it", "That improves one output; it does not pick a path."),
   ("Parallelisation: send each message to all three handlers", "Wasteful, and the answers then need reconciling."),
   ("A single general prompt that lists every rule for all types", "Rules for different types interfere with one another.")])

Q("AI", "Choosing a pattern", """
An internal assistant must answer questions using the company's 4,000-page policy library, which changes monthly. Which design is most appropriate?""",
  "Retrieve relevant passages and add them to the prompt",
  "Retrieval supplies current, relevant content without sending everything every time.",
  [("Paste the full library into the system prompt on every request", "Likely too large, slow and costly."),
   ("Rely on the model's training data to know the policies", "The model has never seen private, changing documents."),
   ("Raise the temperature so that the model recalls more detail", "Temperature does not add knowledge.")])

Q("AI", "Session handling", """
A web chat application needs multi-turn conversations. Where should conversation history be kept?""",
  "In a server-side store keyed by the application's own session ID",
  "The application owns state. A backend store lets it reload and resend history securely.",
  [("In the Claude API, retrieved with the previous message ID", "The API does not store conversations for retrieval."),
   ("In the system prompt, appended to after every turn", "History belongs in messages; rewriting the system prompt also defeats caching."),
   ("Nowhere, since the model retains recent conversations", "The model retains nothing between calls.")], level=1)

Q("AI", "Session handling", """
Two browser tabs for the same user send messages to the same conversation at almost the same moment. Afterwards the stored history has turns out of order and one reply is missing. What should be added?""",
  "Per-session locking when the history is updated",
  "It is an ordinary concurrent-write problem on shared state, solved with ordinary concurrency control.",
  [("A lower temperature so that both replies are identical", "Sampling settings cannot fix a race condition."),
   ("A second API key so that the two tabs do not collide", "Keys are unrelated to writes to your own store."),
   ("A longer max_tokens so that neither reply is dropped", "The reply was lost in storage, not truncated.")], level=3)

Q("AI", "Architecture", """
A mobile team wants the app to call the Claude API directly to avoid an extra network hop. What is the main objection?""",
  "The API key would ship in the app and be extractable",
  "Client-side keys cannot be kept secret. Calls should go through a backend that holds the key.",
  [("Mobile networks cannot carry server-sent events", "They can; this is not the issue."),
   ("The Claude API refuses requests from mobile devices", "The API does not identify device types."),
   ("Direct calls are billed at a higher rate per token", "Pricing does not depend on where the call originates.")], level=1)

Q("AI", "Schema design", """
An extraction schema marks delivery_date as a required string. For emails that contain no date, the model returns a plausible but invented date. What is the best schema change?""",
  "Make the field nullable, returning null when absent",
  "A required field with no source value pushes the model to invent one.",
  [("Add a regular expression that enforces a date format", "The format was fine; the value was fabricated."),
   ("Mark the field required in two places for emphasis", "Emphasis does not create missing information."),
   ("Lower the temperature so that the date is deterministic", "A deterministic invented date is still invented.")])

Q("AI", "Schema design", """
A ticket classifier uses an enum of five categories. Unusual tickets are being forced into badly fitting categories. Which change helps most?""",
  "Add an \"other\" value, with a short free-text field for the detail",
  "An escape value stops the model from being forced into a wrong label.",
  [("Remove the enum and accept any free-text category", "That loses the consistency the enum provides."),
   ("Add twenty more categories to cover every case", "Large enums are harder to choose from and never cover everything."),
   ("Send each ticket three times and take the majority label", "Voting between wrong labels does not produce a right one.")])

Q("AI", "Validation", """
An invoice extractor uses structured outputs, so every response matches the schema. Finance finds invoices where the line items do not add up to the stated total. What is missing?""",
  "A semantic check in code that lines sum to the total",
  "A schema guarantees structure, not correctness. Business rules need their own validation.",
  [("A stricter schema with additionalProperties set to false", "The structure was already valid; the values were wrong."),
   ("A higher max_tokens value so that totals are not truncated", "Nothing was truncated."),
   ("A system prompt reminder that totals must be accurate", "A reminder is not verification.")])

Q("AI", "Reliability", """
After a timeout, a workflow retried a step, and a customer was refunded twice. Which design principle prevents this?""",
  "Make the side effect idempotent, using an idempotency key",
  "With an idempotency key, a repeated attempt is recognised and not executed again.",
  [("Disable all retries across the whole application", "That sacrifices resilience; the issue is the repeated side effect."),
   ("Increase the timeout to ten minutes for every call", "Timeouts can still occur; duplicates remain possible."),
   ("Ask the model to remember which refunds it has issued", "Model memory is not a reliable transaction record.")])

Q("AI", "Reliability", """
The Claude API has been returning errors for several minutes. Every user request waits through multiple retries and then fails. What should the application do instead?""",
  "Stop calling after repeated failures and fall back",
  "A circuit breaker with graceful degradation avoids piling up slow, doomed requests.",
  [("Increase the retry count so that requests eventually pass", "More retries deepen the pile-up during an outage."),
   ("Remove the timeout so that requests can wait as long as needed", "Hanging requests exhaust resources and frustrate users."),
   ("Return an empty reply so that users don't see any error", "Silent empty answers hide the failure and confuse users.")])

Q("AI", "Reliability", """
A marketing campaign sends bursts of thousands of requests within a few seconds, causing many 429 errors, although total daily volume is well within limits. Which design smooths this out?""",
  "Put requests on a queue and process them at a controlled rate",
  "A queue absorbs bursts and feeds the API at a steady pace.",
  [("Open more connections so that the burst finishes sooner", "That intensifies the burst."),
   ("Raise max_tokens so that each request does more work", "It does not reduce the request rate."),
   ("Disable SDK retries so that failures return faster", "Requests would simply fail instead of completing.")])

Q("AI", "Configuration", """
A model ID is hard-coded in forty source files. A newer model must now be adopted. Which practice would have made this a small change?""",
  "Keeping the model ID in configuration, read by all the call sites",
  "Configuration lets the model change without editing code across the codebase.",
  [("Using a different model ID in every file for flexibility", "That makes the system even harder to manage."),
   ("Storing the model ID inside the system prompt text", "The prompt does not select the model."),
   ("Letting each developer choose the model on their machine", "Uncontrolled variation between environments.")], level=1)

Q("AI", "Configuration", """
Production behaviour changed slightly overnight with no deployment. The service uses a model alias that always points to the newest version. What is the recommended practice?""",
  "Pin a specific model version and upgrade deliberately after testing",
  "A moving alias can change behaviour without warning. Pinning makes upgrades a tested release.",
  [("Keep the alias and lower the temperature to stabilise output", "Sampling settings do not prevent a model change."),
   ("Keep the alias and add more few-shot examples each week", "Examples do not prevent the underlying model from changing."),
   ("Switch aliases every day to average out the differences", "That adds variation rather than removing it.")])

Q("AI", "Life cycle", """
A developer edits one paragraph of a production system prompt and deploys it directly. The next day, a previously working feature is broken. Which process was missing?""",
  "Versioned prompts and evals before release",
  "A prompt change is a behaviour change. Regression evals catch breakage before users do.",
  [("A longer system prompt with more capital letters", "Emphasis is not a release process."),
   ("A rule that only senior developers may edit prompts", "Seniority does not replace testing."),
   ("A higher max_tokens setting in production", "Unrelated to the regression.")])

Q("AI", "Life cycle", """
After launch, which set of measurements best shows the health of a Claude-powered feature?""",
  "Error rates, latency, token cost, validation failures",
  "Together these cover reliability, speed, spend and output quality.",
  [("The number of lines in the system prompt each week", "Prompt length says nothing about behaviour in production."),
   ("The count of developers who can access the API key", "An access-control fact, not a health metric."),
   ("The average temperature across all the requests", "A configuration value, not an outcome.")], level=1)

Q("AI", "Access control", """
In a multi-tenant application, a user of one company receives an answer that quotes another company's document. Where is the flaw?""",
  "Retrieval was not scoped to the authenticated user's tenant",
  "Isolation must be enforced when data is fetched, before anything reaches the prompt.",
  [("The system prompt did not forbid sharing documents", "A prompt rule cannot undo data that was already supplied."),
   ("The model's context window was too large", "Window size does not select which documents are retrieved."),
   ("The temperature allowed the model to be creative", "The other tenant's content was in the context; this is not creativity.")])

M("AI", "Configuration", """
Which TWO practices are appropriate for managing configuration of a Claude application? (Select TWO.)""",
  [("Load the API key from a secret manager or environment variable", "Keeps the key out of code and repositories."),
   ("Use separate keys and settings for development and production", "Limits blast radius and separates usage.")],
  [("Commit the API key in a private repository for convenience", "Private repositories still leak; keys do not belong in source control."),
   ("Embed prompts as string literals spread across the modules", "Scattered prompts are hard to version, review and test."),
   ("Share one key across all teams to simplify rotation", "A shared key widens exposure and hides who used what.")])

M("AI", "Sync or batch", """
A team is deciding between synchronous calls and the Message Batches API for a new workload. Which TWO facts are most relevant to the decision? (Select TWO.)""",
  [("Whether a user or blocking process is waiting on each result", "Batches are asynchronous, so waiting users rule them out."),
   ("Whether a delay of up to several hours is acceptable", "Batch completion time is not immediate.")],
  [("Whether the prompts are written in British or American English", "Spelling variety has no bearing on the choice."),
   ("Whether the developers prefer Python or TypeScript", "Both SDKs support both modes."),
   ("Whether the system prompt uses XML tags or Markdown", "Prompt formatting does not affect the choice.")], level=1)
