from qlib import Q

# ======================= D4 · Prompt Engineering & Structured Output =======================

# --- Explicit criteria ---
Q("D4", "S5", "Explicit criteria", """
A code-review prompt says "only flag important issues". Results vary widely between runs. Best improvement?""",
  "Define categories explicitly: flag security, data loss, crashes and incorrect results; don't flag style or naming",
  "Categorical criteria are testable and consistent.",
  [("Add 'be very careful' to the prompt", "Still vague."),
   ("Ask for a confidence score and keep only issues above 0.8", "Self-reported confidence is poorly calibrated."),
   ("Lower the temperature to 0", "Reduces randomness but leaves the criteria ambiguous.")])

Q("D4", "S1", "Explicit criteria", """
A fraud triage prompt says "be conservative". Which rewrite is best?""",
  "'Flag if ANY of: amount over 10,000; new country for this customer; 3+ transactions within 10 minutes.'",
  "Concrete, checkable conditions remove ambiguity.",
  [("'Be extremely conservative.'", "More emphatic, equally vague."),
   ("'Use your best judgement about risk.'", "Delegates the ambiguity."),
   ("'Flag anything that feels unusual.'", "Subjective and inconsistent.")])

Q("D4", "G", "Explicit criteria", """
Why is filtering outputs by the model's self-reported confidence often unreliable?""",
  "Self-reported confidence is not well calibrated unless validated against labelled data",
  "Calibration must be measured; categorical criteria are usually more reliable.",
  [("Claude can't output numbers", "It can."),
   ("Confidence scores cost extra tokens", "Cost isn't the main problem."),
   ("The API removes confidence fields from responses", "No such behaviour.")])

Q("D4", "S6", "Explicit criteria", """
An extraction prompt says "extract the important dates". Different runs pick different dates. Best fix?""",
  "Name exactly which dates to extract (invoice date, due date, service period start/end) and the format",
  "Explicit field definitions remove interpretation.",
  [("Ask for 'all dates' and filter later", "Moves the ambiguity downstream."),
   ("Use a larger model", "Still has to guess what 'important' means."),
   ("Retry until two runs agree", "Agreement isn't correctness.")])

# --- Few-shot ---
Q("D4", "S6", "Few-shot", """
Extraction works on clean digital invoices but fails on scanned receipts and European-format invoices. Most efficient improvement?""",
  "Add a few varied examples covering scanned receipts and European number/date formats, including how missing fields look",
  "Varied few-shot examples teach format handling and edge cases.",
  [("Add five more examples of clean digital invoices", "Doesn't cover the failing formats."),
   ("Increase max_tokens", "Unrelated to format handling."),
   ("Switch to the Batch API", "Changes cost and latency, not accuracy.")])

Q("D4", "G", "Few-shot", """
What makes a few-shot example set most effective for ambiguous cases?""",
  "Including ambiguous examples together with the reasoning for the chosen output",
  "Showing the judgement, not just the answer, transfers to new cases.",
  [("Using many near-identical examples", "Adds little information."),
   ("Placing examples after the user's question", "Placement isn't the key factor."),
   ("Using examples with real customer data for realism", "Unnecessary, and a privacy risk.")])

Q("D4", "S6", "Few-shot", """
An extraction model sometimes invents PO numbers when none exist. Which few-shot example helps most?""",
  "One where the document has no PO number and the output shows po_number: null",
  "Demonstrating the correct handling of missing data reduces fabrication.",
  [("One with a long, complex PO number", "Doesn't teach the missing case."),
   ("One with two PO numbers", "Different problem."),
   ("One with the PO number in bold", "Formatting isn't the issue.")])

Q("D4", "S5", "Few-shot", """
Review comments from Claude vary wildly in format, which breaks a dashboard. Fastest reliable improvement short of schemas?""",
  "Provide one or two examples of the exact comment format expected",
  "Few-shot examples are highly effective for format consistency.",
  [("Ask for 'consistent formatting'", "Too vague."),
   ("Increase temperature", "Increases variation."),
   ("Run the review twice and merge", "Doesn't fix the format.")])

# --- Structured output methods ---
Q("D4", "S6", "Structured output", """
A downstream system requires schema-valid JSON on every call. Which approach is most reliable?""",
  "A tool with the schema as input_schema and a forced tool_choice, or native structured outputs where supported",
  "These constrain output to the schema rather than asking politely.",
  [("Ask for 'JSON only' in the prompt", "May add prose or drift."),
   ("Prefill the reply with '{' only", "Helps format but doesn't validate."),
   ("Regex-strip text before the first brace", "A fragile workaround.")])

Q("D4", "S6", "Structured output", """
Which statement about schema-constrained output is true?""",
  "It guarantees the output's shape, not the correctness of its values",
  "Valid JSON can still contain wrong or invented values.",
  [("It guarantees values are accurate", "Format is not truth."),
   ("It removes the need for validation", "Business rules still need checking."),
   ("It prevents hallucination entirely", "It constrains structure, not facts.")], level=1)

Q("D4", "S4", "Structured output", """
In the Claude API's native structured outputs, what is the difference between JSON outputs and strict tool use?""",
  "JSON outputs constrain Claude's final response format; strict tool use constrains tool names and inputs",
  "They solve different problems and can be combined.",
  [("They are two names for the same feature", "They control different things."),
   ("JSON outputs only work with tools", "They shape the response itself."),
   ("Strict tool use disables tool_choice", "It validates inputs; tool_choice still works.")])

Q("D4", "S6", "Structured output", """
Which feature is NOT compatible with JSON outputs mode, according to the structured outputs documentation?""",
  "Prefilling the assistant response",
  "Prefill conflicts with constrained JSON output.",
  [("Streaming", "Documented as compatible."),
   ("Batch processing", "Documented as compatible."),
   ("Token counting", "Documented as compatible.")], level=3)

Q("D4", "S6", "Structured output", """
You must extract structured data while also using extended thinking for difficult documents. What should you keep in mind?""",
  "Forced tool_choice isn't supported with manual extended thinking; use auto with clear instructions or native structured outputs, and validate",
  "Combining features requires checking compatibility.",
  [("Thinking automatically forces the extraction tool", "It doesn't."),
   ("Thinking and tools can never be used together", "They can, with auto or none."),
   ("Thinking guarantees schema compliance", "Thinking improves reasoning, not format guarantees.")], level=3)

# --- Schema design ---
Q("D4", "S6", "Schema design", """
Many supplier invoices have no VAT number, but vat_number is a required string in the schema. What is the risk, and the fix?""",
  "The model is pushed to invent plausible VAT numbers; make the field nullable or optional and say 'null if absent'",
  "Required fields with no source value invite fabrication.",
  [("Nothing; the model will output an empty string", "Not guaranteed, and empty strings are ambiguous."),
   ("Retry until a PO number is found", "Retrying can't create missing information."),
   ("Increase the temperature", "Increases variation, not accuracy.")])

Q("D4", "S6", "Schema design", """
A payment_terms field must be one of a known set, but some documents use unusual terms. Best schema design?""",
  "An enum of known values plus 'other' with a free-text detail field, and 'not_stated'",
  "Escape hatches prevent forced bad fits and fabrication.",
  [("A strict enum of known values only", "Forces unusual terms into wrong categories."),
   ("A free-text string with no enum", "Loses consistency for common cases."),
   ("A required boolean is_standard_terms", "Loses the actual terms.")])

Q("D4", "S6", "Schema design", """
Which field definition best supports human review routing?""",
  "Per-field confidence (or ambiguity notes) returned alongside the extracted values",
  "Field-level signals let reviews target specific risky fields.",
  [("One overall confidence score per document", "Hides which fields are uncertain."),
   ("A boolean 'needs_review' chosen by the model with no reason", "Opaque and uncalibrated."),
   ("No confidence information, to keep the schema small", "Removes useful routing signals.")])

Q("D4", "S6", "Schema design", """
Which fields should be marked required in an extraction schema?""",
  "Only fields that every valid input document is guaranteed to contain",
  "Everything else should be optional or nullable.",
  [("All fields, for completeness", "Forces guesses when data is missing."),
   ("None, to give the model full freedom", "Loses guarantees for fields that always exist."),
   ("The fields with the longest descriptions", "Irrelevant criterion.")], level=1)

Q("D4", "S6", "Schema design", """
A currency field sometimes receives '$', 'USD' or 'US dollars'. Best fix?""",
  "Constrain it to ISO 4217 codes (enum or pattern) and state the normalisation rule in the description",
  "Normalised, constrained values make downstream processing reliable.",
  [("Accept any string and clean it later", "Pushes inconsistency downstream."),
   ("Remove the currency field", "Loses needed data."),
   ("Ask the model to 'be consistent'", "Too vague.")])

Q("D4", "S6", "Schema design", """
A contract may list zero, one or many signatories. How should the schema represent this?""",
  "An array of signatory objects that may be empty",
  "Arrays model variable counts without forcing placeholder values.",
  [("Fields signatory_1 to signatory_5, all required", "Forces invented values and caps the count."),
   ("A single comma-separated string", "Hard to validate and parse."),
   ("A required object with one signatory", "Can't represent zero or many.")])

# --- Validation, retry & feedback ---
Q("D4", "S6", "Retry loops", """
A business-rule check finds the extracted total (1,280.00) doesn't equal the sum of line items (1,180.00). What should the retry message include?""",
  "The original document plus the specific mismatch, asking Claude to re-read the total and line items and report any discrepancy it finds",
  "Specific error feedback gives the model what it needs to correct.",
  [("'Try again.'", "No information to act on."),
   ("A request to re-check all fields", "Unfocused."),
   ("Nothing; just call the same request again", "Will likely reproduce the error.")])

Q("D4", "S6", "Retry loops", """
A document genuinely lacks a due date. The validator flags due_date as missing. What should happen?""",
  "Accept null (or route to review); don't retry to 'find' a value that isn't there",
  "Retrying missing information encourages fabrication.",
  [("Retry up to five times", "The value won't appear."),
   ("Fill in invoice_date + 30 days", "An invented business value."),
   ("Reject the document permanently", "Too harsh for an optional field.")])

Q("D4", "S6", "Retry loops", """
What is a sensible retry policy for format-validation failures in an extraction pipeline?""",
  "A small bounded number of retries with the specific error appended, then route to human review",
  "Bounded retries avoid loops; escalation handles persistent failures.",
  [("Unlimited retries until success", "Can loop forever and waste cost."),
   ("No retries; always route to a human", "Wastes reviewer time on easily fixed errors."),
   ("Retry with a random different model each time", "Unsystematic.")])

Q("D4", "S6", "Feedback loops", """
Validation errors are logged as free text and nobody analyses them. Improvement?""",
  "Log structured metadata (field, error type, document type, detected pattern) and periodically fix root causes in prompts, schemas or examples",
  "Structured error data turns failures into systematic improvements.",
  [("Delete logs older than a day", "Throws away the learning signal."),
   ("Log the full prompt and response only", "Hard to aggregate."),
   ("Email each error to the team", "Noisy and unstructured.")])

Q("D4", "S6", "Feedback loops", """
Analysis shows 40% of errors come from European decimal commas (1.240,50). Best response?""",
  "Add an explicit normalisation rule and a few-shot example for that format",
  "Fix the root cause at the prompt or example level.",
  [("Add a retry for those documents", "Treats the symptom repeatedly."),
   ("Exclude European invoices", "Drops valid business data."),
   ("Use a larger model and hope", "Not a targeted fix.")])

# --- Batch ---
Q("D4", "S6", "Batch", """
A weekly evaluation job runs 30,000 test prompts against a new prompt version. Results are reviewed the next day. Best API mode?""",
  "Message Batches API, with each test case's ID as the custom_id",
  "Evaluations are a classic batch workload: non-urgent and high volume, at about 50% lower cost.",
  [("Synchronous Messages API with many parallel workers", "Works, but costs more for no benefit."),
   ("Streaming", "Streaming is about latency for one response."),
   ("Claude Code in plan mode", "Wrong tool for bulk API work.")], level=1)

Q("D4", "S5", "Batch", """
A pre-merge check blocks developers until it completes. Should it use the Message Batches API?""",
  "No; a blocking step needs synchronous calls, because batches can take up to 24 hours",
  "Batches trade latency for cost.",
  [("Yes; batches are always faster", "Most finish within an hour, but there's no latency guarantee."),
   ("Yes; batches are cheaper, so always preferred", "Cost isn't the only constraint."),
   ("Only if the PR has more than 100 files", "Size doesn't change the blocking requirement.")], level=1)

Q("D4", "S6", "Batch", """
Batch results come back in a different order from the requests. How do you match them to source records?""",
  "Use the custom_id you set on each request",
  "Results aren't guaranteed in order; custom_id is the join key.",
  [("Assume results follow request order", "Order isn't guaranteed."),
   ("Match by response length", "Unreliable."),
   ("Re-run the batch until the order matches", "Pointless and costly.")], level=1)

Q("D4", "S6", "Batch", """
Which limit applies to a single Message Batch?""",
  "Up to 100,000 requests or 256 MB, whichever is reached first",
  "Larger workloads must be split across batches.",
  [("Up to 1,000 requests", "Far below the actual limit."),
   ("No size limit", "Limits exist."),
   ("Up to 10 GB with unlimited requests", "Not the documented limit.")], level=2)

Q("D4", "S6", "Batch", """
An agent workflow needs your code to execute tools and reply over several turns for each item. Is the Message Batches API a good fit?""",
  "Not for the interactive loop: each batch request is processed independently, with no way for your code to respond mid-task",
  "Batches suit single-shot requests; interactive tool loops need synchronous calls.",
  [("Yes; batches support interactive callbacks", "There are no per-request callbacks."),
   ("Yes, if you set a long TTL", "TTL relates to caching, not interactivity."),
   ("Yes; batches automatically run client tools", "Client tools are run by your code.")])

Q("D4", "S6", "Batch", """
Some requests in a batch errored and some expired. What is the best recovery?""",
  "Resubmit only the errored or expired items, identified by custom_id",
  "Each request succeeds or fails independently.",
  [("Resubmit the entire batch", "Pays again for completed work."),
   ("Ignore them", "Leaves gaps in the data."),
   ("Switch the whole job to synchronous calls", "Unnecessary for a few failures.")])

# --- Prompt caching ---
Q("D4", "S1", "Prompt caching", """
A support bot sends the same 25-page policy manual as the system prompt on every request. Cost is high. What helps most?""",
  "Prompt caching on the stable system prompt (cache_control), with variable content after the cache point",
  "Repeated identical prefixes are exactly what caching is for.",
  [("Batch API", "The bot is interactive."),
   ("Shorten every user message", "Doesn't address the repeated large prefix."),
   ("Lower max_tokens", "Affects output, not repeated input.")], level=1)

Q("D4", "S1", "Prompt caching", """
Caching is enabled, but cache_read_input_tokens is always 0. The system prompt begins with the current timestamp. Why?""",
  "The prefix changes on every request, so the cached prefix never matches",
  "Caching requires a byte-identical prefix up to the breakpoint.",
  [("The TTL is too long", "TTL doesn't cause zero hits."),
   ("Caching only works with batches", "It works with synchronous requests."),
   ("The model doesn't support system prompts", "Unrelated.")])

Q("D4", "S6", "Prompt caching", """
A nightly batch shares one long instruction block across all requests. Which cache lifetime fits better?""",
  "The 1-hour TTL, since batch processing can take longer than 5 minutes",
  "The default 5-minute cache may expire between requests in a long batch.",
  [("The default 5-minute TTL is always best", "May expire during the batch."),
   ("Caching doesn't work with batches", "It can be combined with batches."),
   ("A 24-hour TTL", "Not an available lifetime.")], level=3)

Q("D4", "G", "Prompt caching", """
Compared with the base input price, what does reading from the prompt cache cost?""",
  "About 0.1× the base input price",
  "Cache reads are heavily discounted; writes cost more (1.25× for 5 minutes, 2× for 1 hour).",
  [("2× the base input price", "That's the 1-hour cache write price."),
   ("1.25× the base input price", "That's the 5-minute cache write price."),
   ("The same as base input", "Reads are discounted.")], level=2)

Q("D4", "G", "Prompt caching", """
In what order does prompt caching consider the parts of a request when building the cached prefix?""",
  "Tools, then system, then messages",
  "The cache covers the prefix in that order up to the breakpoint.",
  [("Messages, then system, then tools", "Reversed."),
   ("System only", "Tools and messages can be part of the prefix."),
   ("Only the last user message", "That's usually the variable part.")], level=2)

# --- Independent review ---
Q("D4", "S5", "Independent review", """
Claude writes a migration script and is then asked, in the same conversation, to review it. The review finds nothing. Why is this weak?""",
  "Self-review in the same context tends to confirm its own reasoning; an independent instance with explicit criteria is more effective",
  "Fresh context and explicit criteria reduce confirmation bias.",
  [("Reviews must always use a smaller model", "Model size isn't the issue."),
   ("Reviews only work with temperature 1", "Unrelated."),
   ("Claude can't review code", "It can; the setup is the problem.")])

Q("D4", "S3", "Independent review", """
A long research report must be checked for unsupported claims. Best design?""",
  "A separate reviewer instance that checks each claim against its cited source",
  "Independent, criteria-based verification catches unsupported claims.",
  [("Ask the writer to add 'I am confident' to each claim", "Adds no verification."),
   ("Have the writer reread the report", "Same-context bias."),
   ("Count the number of citations", "Quantity isn't support.")])

Q("D4", "S5", "Structured output", """
A CI step converts Claude's review into GitHub annotations and needs file, line, severity and message for each finding. Which approach is most robust?""",
  "Define the findings structure as a JSON schema (structured outputs or a forced tool) and validate before posting",
  "Schema-constrained output plus validation gives parseable, checked findings.",
  [("Ask for a Markdown table and parse it with regex", "Fragile."),
   ("Ask Claude to post the annotations directly with no structure", "No validation step."),
   ("Use a higher temperature for more detailed findings", "Unrelated to structure.")])
