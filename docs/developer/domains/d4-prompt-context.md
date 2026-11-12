# Prompt & Context Engineering <span class="level-badge">11.0%</span>

Architect [D4](../../architect/domains/d4-prompt-structured-output.md) and [D5](../../architect/domains/d5-context-reliability.md) cover the design side. The Developer exam adds the code side: **getting output your program can trust**, and keeping long conversations healthy.

## What this domain covers

* System prompts, examples and XML structure
* Structured output: three methods and their guarantees
* Output validation, defensive parsing, retries on malformed responses
* Context management and context drift

---

## 1. Prompt engineering essentials

**Be clear and specific.** Treat Claude like a capable new colleague with no background: say what the task is for, who the audience is, and what a good result looks like. Vague prompt → generic output.

**System prompt.** Use it for the role, standing rules, tone and stable reference material. Put the per-request task in the user turn.

**Examples (few-shot).** The most reliable way to fix format and edge-case behaviour.

* 3–5 examples, **varied**, covering the tricky cases
* Wrap them in `<example>` tags so they are not mistaken for instructions
* If output copies an example too closely, the examples are too alike

**XML tags.** Separate the parts of a prompt so instructions, data and examples cannot blur together.

```text
<instructions>Summarise the complaint in one sentence.</instructions>
<complaint>
{{customer_text}}
</complaint>
```

Tags also make the *output* easy to extract: ask for the answer inside `<answer>` tags.

**Long documents.** Documents at the top, the question at the end. For multiple documents wrap each one with its source metadata.

**Let Claude think** on multi-step problems (extended thinking, or "reason in `<thinking>` tags, then answer"). Skip it for simple tasks.

**Positive instructions with reasons** work better than a list of "NEVER". Say what to do and why.

**Reducing hallucination.** Allow "I don't know"; ask for supporting quotes first and answers based only on them; restrict the answer to the supplied documents.

## 2. Structured output: three methods

| Method | How | Guarantee |
|---|---|---|
| **Prompt + parse** | Ask for JSON, show an example, parse | None. Can produce prose around the JSON or invalid JSON |
| **Tool use as a schema** | Define a tool whose `input_schema` is your structure, force it with `tool_choice`; add `strict: true` for guaranteed schema conformance | The tool is called; with `strict`, input matches the schema |
| **Structured outputs** | `output_config={"format": {"type": "json_schema", "schema": {...}}}` | The response text is valid JSON matching the schema |

```python
response = client.messages.create(
    model=MODEL, max_tokens=1024,
    messages=[{"role": "user", "content": f"Extract the order details:\n<email>{email}</email>"}],
    output_config={"format": {"type": "json_schema", "schema": {
        "type": "object",
        "properties": {
            "order_ref": {"type": ["string", "null"]},
            "items": {"type": "array", "items": {"type": "string"}},
            "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["order_ref", "items", "urgency"],
        "additionalProperties": False,
    }}},
)
```

!!! danger "What the guarantee does *not* cover"
    * **Truncation**: if `stop_reason` is `max_tokens`, the JSON is incomplete.
    * **Refusal**: a refusal does not follow your schema.
    * **Truth**: the schema fixes shape, not correctness. Values can still be wrong or invented.

    So you still check `stop_reason` and still validate meaning.

Older code sometimes "prefills" the assistant turn with `{` to steer JSON. Treat that as a legacy trick: it conflicts with thinking and with structured outputs, and current models may reject it. Prefer the schema-based methods.

## 3. Validation and defensive parsing

Model output is **untrusted input** to your program. Handle it in layers:

```python
import json
from pydantic import ValidationError

def parse_reply(resp):
    if resp.stop_reason == "max_tokens":
        raise Truncated()                       # 1. complete?
    if resp.stop_reason == "refusal":
        raise Refused()
    text = next(b.text for b in resp.content if b.type == "text")   # 2. right block
    try:
        data = Invoice.model_validate_json(text)                    # 3. shape
    except ValidationError as e:
        raise Malformed(str(e))
    if abs(sum(i.amount for i in data.lines) - data.total) > 0.01:  # 4. meaning
        raise Inconsistent("line items do not sum to total")
    return data
```

**Retry with feedback, bounded.**

```python
for attempt in range(3):
    resp = call(messages)
    try:
        return parse_reply(resp)
    except (Malformed, Inconsistent) as e:
        messages += [{"role": "assistant", "content": resp.content},
                     {"role": "user", "content": f"That failed validation: {e}. Return corrected JSON only."}]
raise NeedsHumanReview()
```

* Send the **specific error** back. A blind identical retry tends to repeat the mistake.
* **Cap** the attempts, then fall back (human queue, default, clear error).
* A retry cannot create information that isn't in the source. If a field is absent from the document, the fix is a nullable field, not more attempts.
* `Truncated` needs a bigger `max_tokens`, not a retry of the same call.

### Scepticism toward confident output

Fluent, confident wording is **not evidence of correctness**. A model can state a wrong figure, an invented citation or a non-existent function with complete assurance.

* Don't use the model's own "I'm confident" as a quality signal. Self-reported confidence is poorly calibrated.
* Verify what matters against a source: recompute totals, check that cited passages exist, run the code, look the ID up.
* Ask for evidence (quotes, references to the supplied documents) so claims can be checked.
* Route high-stakes or unverifiable outputs to a person.

### Input sanitisation

Clean and constrain what goes *into* a prompt.

* Validate type, length and format of user input before it reaches the model; reject or truncate oversize input.
* Put variable content inside delimiters (XML tags) and tell Claude it is data.
* Escape or strip content that could break your delimiters, such as a user typing your closing tag.
* Remove what the task doesn't need: secrets, personal data, irrelevant boilerplate.
* Sanitisation reduces risk; it does not replace least-privilege tools and output validation ([Security](d6-security-safety.md)).

### Where instructions belong

| Put it in… | When it is… |
|---|---|
| System prompt | Role, standing rules, tone, stable reference material |
| User turn | The specific task and its data |
| Tool descriptions | When and how to use each tool |
| `CLAUDE.md` / project instructions | Project facts that apply every session |
| Code / configuration | Anything that must be guaranteed |

Prompting is **iterative**: change one thing, run the eval set, compare, keep or revert. Guessing at several changes together tells you nothing about which one helped.

## 4. Context management

Every turn resends the history, so long sessions get slower, dearer and less accurate.

**Context drift** is what happens as a conversation grows: early instructions lose influence, stale or contradictory details accumulate, and exact facts (IDs, amounts, dates) get blurred by summaries.

| Technique | What it does | Watch out for |
|---|---|---|
| **Pinned facts block** | Keep exact values (IDs, amounts, decisions) in a structured block resent each turn | Keep it small and current |
| **Summarisation / compaction** | Replace old turns with a summary | Summaries lose precise details; keep those in the facts block |
| **Trim tool results** | Return only the fields needed; clear old, re-fetchable tool output | Don't clear what is still needed |
| **Retrieval** | Fetch only relevant chunks per request | Retrieval quality limits answer quality |
| **External memory / notes** | Store progress outside the window (file, database) and reload | Treat stored content as data, not instructions |
| **Sub-agents** | Do noisy work in a separate context, return a summary | Costs more tokens overall |
| **Fresh session** | Start again with a hand-over summary | Better than pushing a degraded context further |

The platform offers server-side helpers for some of these (context editing that clears old tool results, compaction, a memory tool). Know that they exist and what problem each solves; check the docs for current names and flags.

**Position matters.** In very long inputs, material in the middle gets the least attention. Put key instructions at the start or end, and restate critical constraints near the question.

**Prompt templates.** Keep fixed text separate from variables, and substitute variables into clearly delimited places (XML tags). It makes prompts testable, version-controllable and cache-friendly, and keeps user data from being read as instructions.

---

## Traps

| Tempting answer | Why it's wrong |
|---|---|
| "Add 'respond ONLY in JSON' in capitals" | Still no guarantee; use a schema-based method |
| "Structured outputs mean no validation needed" | Shape only; truncation, refusal and wrong values remain |
| "Retry until it parses" | Unbounded; and a blind retry repeats the error |
| "Raise temperature to fix format errors" | Makes output less consistent |
| "A bigger context window solves drift" | More room, same dilution; manage the context |
| "Summarise everything to save tokens" | Loses exact figures; pin them |

## Check yourself

??? question "You need machine-readable output that always matches a schema. Best method?"
    Structured outputs with a JSON schema (or a strict tool). Then still check `stop_reason` and validate meaning.

??? question "Extraction retries three times for a 'delivery_date' that isn't in the email, then invents one. Fix?"
    Make the field nullable and tell the model to return null when absent. Retrying cannot produce missing information.

??? question "After 40 turns the assistant quotes the wrong order number. What prevents this?"
    A pinned case-facts block with exact values resent each turn, instead of relying on summaries of old turns.

??? question "User text sometimes gets treated as instructions. Structural fix?"
    Wrap the user content in XML tags and state that content inside is data to analyse, not instructions.

??? question "A validation failure occurs. What does the retry message contain?"
    The specific validation error and a request for corrected output, with a cap on attempts and a fallback.

---

!!! abstract "Verify in official docs"
    * [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
    * [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) · [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
    * Prompting basics on this site: [Fundamentals → Prompt Engineering](../../fundamentals/prompt-engineering-basics.md)
