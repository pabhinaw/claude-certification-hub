# Question Bank · Prompt & Context Engineering

**12 original questions** (1 multiple-response). Try each one before opening the answer. Every answer explains why the correct option is right **and why each other option is wrong**.

!!! note "Original practice material"
    Written from public documentation and general engineering practice. These are not real or recalled exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a [mock exam](../mock-exams.md).

**Topics covered:** Context drift · Context management · Examples · Hallucination · Long context · Prompt clarity · Structured output · Validation · XML structure

---

<p class="qb-meta"><span class="qb-id">PC-001</span><span>Prompt clarity</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A prompt says "Summarise this." The summaries vary widely in length and focus. What is the most effective first improvement?

- **A.** State the audience, purpose, length and what to include
- **B.** Switch to the largest model tier that is available
- **C.** Add "IMPORTANT" in capitals before the instruction
- **D.** Set the max_tokens parameter to a very low value

??? success "Answer: A"
    **Why A is right:** Specific instructions and context are the first thing to fix.

    **Why the others are wrong:**

    * **B:** The problem is an underspecified prompt.
    * **C:** Emphasis without detail adds little.
    * **D:** That truncates rather than guides.

---

<p class="qb-meta"><span class="qb-id">PC-002</span><span>Examples</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A prompt includes three examples that are nearly identical. Outputs now copy their wording and structure too closely. What should change?

- **A.** Use varied examples that cover different cases
- **B.** Remove every example and rely on the instructions
- **C.** Add ten more examples that are similar to those three
- **D.** Move the three examples into the user's message

??? success "Answer: A"
    **Why A is right:** Diverse examples show the pattern without anchoring on one instance.

    **Why the others are wrong:**

    * **B:** Usually loses the format guidance examples provide.
    * **C:** Reinforces the over-fitting.
    * **D:** Location does not address their similarity.

---

<p class="qb-meta"><span class="qb-id">PC-003</span><span>XML structure</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A prompt places instructions and a pasted customer email in one block of text. Claude sometimes follows sentences from the email as if they were instructions. What structural change helps most?

- **A.** Write all of the instructions in capital letters
- **B.** Wrap the email in XML tags and refer to it by tag name
- **C.** Put the email before the instructions without any markers
- **D.** Shorten the email to its first two sentences

??? success "Answer: B"
    **Why B is right:** Tags separate data from instructions clearly.

    **Why the others are wrong:**

    * **A:** Emphasis does not create a boundary.
    * **C:** Order alone does not separate them.
    * **D:** Loses information and leaves the ambiguity.

---

<p class="qb-meta"><span class="qb-id">PC-004</span><span>Long context</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A prompt contains a 60-page document and one question about it. Where should the question go for best results?

- **A.** Before the document, at the very beginning only
- **B.** After the document, at the end of the prompt
- **C.** In a separate request sent five minutes later
- **D.** In the middle of the document, at a random page

??? success "Answer: B"
    **Why B is right:** With long inputs, placing the query last tends to improve answers.

    **Why the others are wrong:**

    * **A:** Generally weaker than placing it after long content.
    * **C:** A separate request would not include the document.
    * **D:** The middle of long inputs gets the least attention.

---

<p class="qb-meta"><span class="qb-id">PC-005</span><span>Structured output</span><span>Single answer</span><span title="Difficulty">●○○</span></p>

A service needs every response to be valid JSON matching a fixed schema. Which approach gives the strongest guarantee?

- **A.** One example of the JSON in the system prompt
- **B.** A regular expression that removes surrounding text
- **C.** Structured outputs with a JSON schema
- **D.** An instruction: "Return only JSON, nothing else"

??? success "Answer: C"
    **Why C is right:** Schema-constrained output guarantees the shape of the response.

    **Why the others are wrong:**

    * **A:** Examples guide but do not guarantee.
    * **B:** Cleans up after the fact; invalid JSON can still occur.
    * **D:** Usually works but guarantees nothing.

---

<p class="qb-meta"><span class="qb-id">PC-006</span><span>Structured output</span><span>Single answer</span><span title="Difficulty">●●●</span></p>

A team uses structured outputs and removes all response checks, reasoning that the schema is guaranteed. Which case can still deliver an unusable response?

- **A.** The model uses double quotes around the strings
- **B.** The model inserts spaces between the JSON tokens
- **C.** The output is cut off because max_tokens was reached
- **D.** The model returns the properties in a different order

??? success "Answer: C"
    **Why C is right:** Truncation and refusals fall outside the guarantee, so stop_reason must still be checked.

    **Why the others are wrong:**

    * **A:** Double quotes are required by JSON.
    * **B:** Whitespace is valid JSON.
    * **D:** Property order does not make JSON unusable.

---

<p class="qb-meta"><span class="qb-id">PC-007</span><span>Validation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A response fails schema validation. Which retry strategy is most effective?

- **A.** Raise the temperature and send the identical request
- **B.** Send the identical request again until it validates
- **C.** Accept the response and correct it by hand later
- **D.** Send the error back and ask for a fix, with a limit

??? success "Answer: D"
    **Why D is right:** Specific feedback lets the model fix the problem; a limit prevents endless loops.

    **Why the others are wrong:**

    * **A:** More randomness reduces consistency.
    * **B:** A blind retry tends to repeat the error and may never end.
    * **C:** Passes invalid data downstream.

---

<p class="qb-meta"><span class="qb-id">PC-008</span><span>Validation</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An extractor retries three times because the field "warranty_period" fails validation; the source document never mentions a warranty. What is the right fix?

- **A.** Switch to a larger model to find the hidden value
- **B.** Increase the number of retries from three to ten
- **C.** Add an example with a typical warranty period
- **D.** Allow null; retries cannot supply missing data

??? success "Answer: D"
    **Why D is right:** When information is absent from the source, the schema must allow absence.

    **Why the others are wrong:**

    * **A:** There is no value to find.
    * **B:** No number of retries creates missing data.
    * **C:** Encourages the model to invent one.

---

<p class="qb-meta"><span class="qb-id">PC-009</span><span>Context drift</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

In a long support conversation the assistant starts quoting the wrong order number. Earlier turns were replaced by a summary to save tokens. What would prevent this?

- **A.** Keep exact values in a facts block sent every turn
- **B.** Summarise more aggressively to free additional space
- **C.** Ask the customer to repeat the number in each message
- **D.** Raise the temperature so that the model re-reads context

??? success "Answer: A"
    **Why A is right:** Summaries blur precise details. Pinned facts keep them exact.

    **Why the others are wrong:**

    * **B:** Loses even more detail.
    * **C:** Poor experience and unnecessary.
    * **D:** Temperature does not change what is in context.

---

<p class="qb-meta"><span class="qb-id">PC-010</span><span>Context management</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

An agent's context fills up with large results from file reads made many turns ago, which could be fetched again if needed. Which technique fits best?

- **A.** Clear old tool results but keep the recent ones
- **B.** Duplicate the results so that they are not forgotten
- **C.** Switch off tools so that no further results are added
- **D.** Delete the system prompt to recover the most tokens

??? success "Answer: A"
    **Why A is right:** Stale, re-fetchable tool output is the cheapest thing to drop.

    **Why the others are wrong:**

    * **B:** Uses even more context.
    * **C:** Stops the agent from working.
    * **D:** Removes the agent's instructions.

---

<p class="qb-meta"><span class="qb-id">PC-011</span><span>Hallucination</span><span>Single answer</span><span title="Difficulty">●●○</span></p>

A question-answering feature over supplied documents sometimes states facts that are not in them. Which prompt technique reduces this most directly?

- **A.** Tell the model that it is a world-class expert
- **B.** Ask for quotes first and allow "not found"
- **C.** Remove the documents and ask from memory instead
- **D.** Raise the temperature to encourage a fuller answer

??? success "Answer: B"
    **Why B is right:** Grounding in quotes plus permission to say the answer is absent reduces invention.

    **Why the others are wrong:**

    * **A:** A role does not ground answers in the documents.
    * **C:** Removes the grounding entirely.
    * **D:** More randomness tends to increase invention.

---

<p class="qb-meta"><span class="qb-id">PC-012</span><span>Structured output</span><span>Select TWO</span><span title="Difficulty">●●○</span></p>

A response from a structured-output request must be checked before use. Which TWO checks remain necessary? (Select TWO.)

- **A.** That stop_reason does not indicate truncation or refusal
- **B.** That the response contains at least one XML tag
- **C.** That the response was generated at temperature 1
- **D.** That the values satisfy business rules, such as totals adding up
- **E.** That the response is longer than the prompt

??? success "Answer: A and D"
    **Why A is right:** Those cases fall outside the schema guarantee.

    **Why D is right:** A schema checks shape, not correctness.

    **Why the others are wrong:**

    * **B:** XML tags are irrelevant to JSON output.
    * **C:** Temperature is not a validity criterion.
    * **E:** Relative length is meaningless.

---
