from qlib import Q

# ======================= D5 · Context Management & Reliability =======================

# --- Context preservation ---
Q("D5", "S1", "Context preservation", """
After several rounds of summarising a long support conversation, the agent quotes the wrong refund amount. What is the likely cause?""",
  "Progressive summarisation lost the exact figure; key facts should live in a verbatim case-facts block",
  "Repeated summaries drop details such as amounts, IDs and dates.",
  [("The model can't handle numbers", "It can; the number was lost from context."),
   ("The context window was too large", "Size wasn't the cause."),
   ("Caching returned an old response", "Caching reuses prompt prefixes, not answers.")])

Q("D5", "G", "Context preservation", """
A critical instruction placed in the middle of a 120k-token prompt is often ignored. What is the best mitigation?""",
  "Put critical instructions and facts at the start or end, or in a compact block near the question",
  "Information in the middle of long contexts is used less reliably ('lost in the middle').",
  [("Repeat the instruction in capital letters in the same position", "Position is the issue."),
   ("Add more documents so the instruction stands out", "Makes it worse."),
   ("Lower the temperature", "Doesn't change how position affects attention.")], level=1)

Q("D5", "S3", "Context preservation", """
An agent's context fills with raw tool outputs (logs, full JSON, whole pages) after a few steps. Best practice?""",
  "Trim or summarise tool results to what's needed before appending, and delegate bulky reads to subagents",
  "Tool-result accumulation is a major source of context degradation.",
  [("Keep everything, since more context is better", "Irrelevant content dilutes attention."),
   ("Restart the agent after every tool call", "Loses all continuity."),
   ("Disable tools that return large outputs", "Loses capability.")])

Q("D5", "S1", "Context preservation", """
What belongs in a case-facts block for a support agent?""",
  "Stable, verified facts the agent must not lose: customer and order IDs, amounts, dates, verification status and decisions so far",
  "A compact, verbatim block protects critical facts from summarisation loss.",
  [("The full transcript", "That's what the block is meant to replace."),
   ("The model's tone instructions", "Those belong in the system prompt."),
   ("Every tool result received so far", "Too bulky; include only the key facts.")])

Q("D5", "S2", "Context preservation", """
During a long coding session, Claude uses /compact. Which practice prevents important details from being lost?""",
  "Keep key findings and decisions in a scratchpad or notes file that survives compaction",
  "External notes preserve details that a summary may drop.",
  [("Never use /compact", "Context will eventually overflow."),
   ("Compact after every message", "Over-compacting loses detail faster."),
   ("Increase max_tokens before compacting", "Unrelated.")])

# --- Escalation ---

Q("D5", "S1", "Escalation", """
A customer asks for a refund type that no policy covers. What should the agent do?""",
  "Escalate to a human; don't invent a policy",
  "Policy gaps are an escalation trigger.",
  [("Approve it, since the customer is probably right", "Improvising policy is risky."),
   ("Deny it, since it isn't listed", "Equally improvised."),
   ("Apply the closest existing policy without saying so", "Hidden assumptions create liability.")])

Q("D5", "S1", "Escalation", """
Which signal is the LEAST reliable trigger for escalation?""",
  "Detected negative sentiment in the customer's tone",
  "Tone doesn't reliably indicate whether the agent can resolve the issue.",
  [("An explicit request to speak to a person", "A strong, explicit trigger."),
   ("An action exceeding the agent's authorisation", "A clear policy trigger."),
   ("No progress after several attempts", "A reliable trigger.")])

Q("D5", "S1", "Escalation", """
A routine password reset request comes in, and the agent has the tools to complete it. The customer sounds frustrated. What should the agent do?""",
  "Resolve it autonomously, efficiently and empathetically",
  "Routine, resolvable requests should be resolved; frustration alone isn't a reason to escalate.",
  [("Escalate because the customer is frustrated", "Sentiment alone is a poor trigger."),
   ("Escalate all account-related requests", "Defeats the purpose of the agent."),
   ("Ask the customer to try again later", "Unhelpful.")])

Q("D5", "S1", "Escalation", """
An agent has tried three different approaches to fix a sync issue, and each failed. What now?""",
  "Escalate with a summary of what was tried and the results",
  "Lack of progress is an escalation trigger; the summary prevents repeated work.",
  [("Keep trying new approaches until the iteration cap", "Wastes time."),
   ("Tell the customer it's fixed", "Dishonest."),
   ("Close the ticket", "Abandons the customer.")])

Q("D5", "S1", "Escalation", """
A requested action exceeds the agent's refund authority. What is the correct behaviour?""",
  "Route it for approval or escalate, with the case details and the reason",
  "Authorisation limits are hard boundaries.",
  [("Split the refund into smaller amounts under the limit", "Circumvents the control."),
   ("Proceed and note it for later review", "Violates the limit."),
   ("Refuse without explanation", "Unhelpful; escalation is available.")])

# --- Error propagation ---
Q("D5", "S3", "Error propagation", """
A subagent's call to an internal analytics API returns a permission error. What should it report to the coordinator?""",
  "A structured, non-retryable permission error naming the source, so the coordinator can report the gap or request access",
  "Coordinators need to tell access failures apart from empty results, and know whether retrying makes sense.",
  [("'No relevant sources found.'", "Misrepresents a failure as an empty result."),
   ("Results invented from general knowledge", "Fabrication."),
   ("Nothing, to keep the report clean", "Silent gaps mislead the final output.")], level=1)

Q("D5", "S3", "Error propagation", """
Two of five data sources failed during a research run. How should the final report handle this?""",
  "Clearly mark the report as partial, naming which sources failed and how that limits the conclusions",
  "Transparent partial results are better than silently incomplete ones.",
  [("Omit any mention of the failures", "Readers will over-trust the report."),
   ("Delay the report indefinitely", "May be unnecessary; partial results can still be useful."),
   ("Fill the gaps with estimates", "Fabrication.")])

Q("D5", "S4", "Error propagation", """
Which practice is an anti-pattern in agent error handling?""",
  "Catching all tool exceptions and returning empty results so the agent keeps going",
  "Suppressing errors creates confident wrong answers.",
  [("Returning structured errors with retryability", "Good practice."),
   ("Escalating after repeated failures", "Good practice."),
   ("Logging errors with context", "Good practice.")])

Q("D5", "S6", "Error propagation", """
An extraction service can't read page 3 of a PDF. What should the output indicate?""",
  "That fields from page 3 couldn't be read (with a reason), so they're routed for review rather than left blank as if absent",
  "'Couldn't access' must stay distinct from 'not present'.",
  [("Leave those fields null with no explanation", "Indistinguishable from genuinely missing data."),
   ("Guess the values from the other pages", "Fabrication."),
   ("Fail the whole document silently", "Loses the readable data and the reason.")])

# --- Long-running work ---
Q("D5", "S2", "Long-running work", """
Which combination best sustains coherent exploration of a very large codebase across sessions?""",
  "Subagents for broad searches, a scratchpad of findings, targeted reads, and periodic state exports",
  "Each technique protects context or durability.",
  [("Reading all files at the start of each session", "Exhausts context."),
   ("Relying solely on the conversation history", "Lost on reset or compaction."),
   ("Maximising max_tokens", "Output size isn't the constraint.")])

Q("D5", "S2", "Long-running work", """
An agent crashes halfway through a 200-file migration. What design would have made recovery easy?""",
  "Writing progress (done, pending, decisions) to a state file after each batch of files",
  "Externalised state enables resumption without redoing work.",
  [("Keeping progress only in the model's context", "Lost on crash."),
   ("Running all 200 files in one step", "Bigger blast radius."),
   ("Using plan mode", "Planning helps up front but doesn't record progress.")])

Q("D5", "S4", "Long-running work", """
Why is targeted reading (search first, then read specific sections) important in long sessions?""",
  "It keeps context for relevant content and delays degradation",
  "Context is a scarce resource.",
  [("Because Read can only open one file per session", "No such limit."),
   ("Because Grep is cheaper than Read in API pricing", "Tool calls aren't priced like that."),
   ("Because large files can't be read at all", "They can, but it's often wasteful.")], level=1)

# --- Human review routing ---
Q("D5", "S6", "Review routing", """
An extraction pipeline currently sends a random 5% sample of documents to human review. Errors in critical fields still reach finance. Best redesign?""",
  "Route by risk: field-level calibrated confidence, critical-field rules and document characteristics, plus stratified sampling for QA",
  "Random sampling misses rare, high-risk cases.",
  [("Increase the random sample to 20%", "Costs more and still misses targeted risks."),
   ("Review everything", "Defeats automation."),
   ("Use the model's overall document confidence only", "Hides field-level problems.")])

Q("D5", "S6", "Review routing", """
Overall extraction accuracy is 98%, but bank account numbers on handwritten forms are wrong 15% of the time. What does this show?""",
  "Aggregate metrics can hide field- and segment-level failures; measure per field and per document type",
  "Breakdowns reveal where review is actually needed.",
  [("98% is good enough to skip review", "Critical-field errors matter more than the average."),
   ("Handwritten forms should be dropped", "Excludes valid input."),
   ("The model needs a higher temperature", "Unrelated.")])

Q("D5", "S6", "Review routing", """
Before trusting field-level confidence scores to auto-accept extractions, what should you do?""",
  "Calibrate them against a labelled set, checking that 'high confidence' is actually correct at the expected rate, per field",
  "Uncalibrated confidence can't safely gate automation.",
  [("Nothing; scores are calibrated by default", "Calibration must be verified."),
   ("Multiply all scores by 0.9 for safety", "Arbitrary."),
   ("Use only scores above 0.99", "Still uncalibrated.")])

Q("D5", "S6", "Review routing", """
What is stratified sampling in the context of extraction QA?""",
  "Sampling within subgroups (e.g. document type × confidence band) so rare categories are reviewed too",
  "Ensures coverage of rare but risky segments.",
  [("Sampling the first N documents each day", "Biased toward arrival order."),
   ("Sampling only low-confidence items", "That's routing, not QA of accepted items."),
   ("Sampling a fixed percentage at random", "That's simple random sampling.")])

Q("D5", "S6", "Review routing", """
How should reviewers be shown items routed for review?""",
  "With the specific fields and reasons flagged, so they verify those rather than the whole document",
  "Targeted review is faster and more accurate.",
  [("The whole document with no hints, to avoid bias", "Wastes reviewer effort."),
   ("Only the model's final JSON", "Reviewers need the source to verify."),
   ("A random subset of fields", "Misses the flagged risks.")])

# --- Provenance ---
Q("D5", "S3", "Provenance", """
A research report states market sizes from several sources. What practice best supports trust?""",
  "Keep a claim-to-source mapping with dates for each figure through to the final report",
  "Traceable, dated claims can be verified.",
  [("List all sources at the end without mapping them", "Readers can't tell which claim comes from where."),
   ("Round all figures to remove inconsistencies", "Hides real differences."),
   ("Use only the most recent source", "May discard valid, relevant data.")])


Q("D5", "S3", "Provenance", """
Why should time-sensitive facts in a report carry dates?""",
  "Values change over time, and the date tells readers how current the claim is",
  "Temporal context prevents outdated figures being read as current.",
  [("Dates increase the word count", "Not a goal."),
   ("Search engines require dates", "Irrelevant to accuracy."),
   ("Dates replace the need for sources", "Both are needed.")], level=1)

# --- Evaluation ---
Q("D5", "S6", "Evaluation", """
A new prompt raises overall accuracy from 92% to 94%, but the 'total amount' field got worse. What should you do?""",
  "Analyse per field and decide by business impact; a regression in a critical field may outweigh the average gain",
  "Per-field evaluation reveals trade-offs that averages hide.",
  [("Ship it, since the average improved", "Ignores the critical regression."),
   ("Revert immediately without analysis", "May discard real improvements."),
   ("Test on fewer documents", "Less evidence, not more.")])
