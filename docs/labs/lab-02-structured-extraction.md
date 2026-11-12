# Lab 2 · Reliable Structured Extraction <span class="level-badge">L3</span>

!!! tip "Prefer to run it first?"
    The complete script is in [`labs-code/`](https://github.com/pabhinaw/claude-certification-hub/tree/main/labs-code). Try `python lab02_extraction.py --dry-run`, which needs no API key, then read on to understand each part.

**Goal:** extract invoice fields that are **always schema-valid**, **never fabricated**, retried with **specific errors**, and **routed to review by risk**.

## Step 1: Fictional documents

```python
DOCS = {
  "doc-1": "INVOICE #A-1001\nDate: 2026-02-14\nBill to: Example Traders Pvt Ltd\nPO: PO-7788\nTotal: INR 12,500.00\nTerms: Net 30",
  "doc-2": "Rechnung Nr. 55-B · Datum: 5. März 2026 · Gesamt: 1.240,50 EUR · Zahlbar sofort",
  "doc-3": "Receipt 9912 -- total 89.99 USD -- thank you!",   # no date, no PO, no terms
}
```

## Step 2: A schema that allows "missing"

```python
SCHEMA = {
  "type": "object",
  "properties": {
    "invoice_number": {"type": "string"},
    "invoice_date": {"type": ["string", "null"], "description": "ISO 8601 YYYY-MM-DD. null if not present. Never guess."},
    "po_number": {"type": ["string", "null"], "description": "null if no PO number appears."},
    "total": {"type": ["number", "null"], "description": "Plain number, '.' as decimal separator."},
    "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. INR, EUR, USD."},
    "payment_terms": {"type": "string", "enum": ["net_30", "net_60", "due_on_receipt", "other", "not_stated"]},
    "low_confidence_fields": {"type": "array", "items": {"type": "string"},
                              "description": "Names of fields that were ambiguous or hard to read."}
  },
  "required": ["invoice_number", "payment_terms", "low_confidence_fields"]
}

TOOL = {"name": "record_invoice", "description": "Record fields extracted from ONE invoice.",
        "input_schema": SCHEMA}
```

## Step 3: Forced tool call + few-shot + normalisation rules

```python
import anthropic, json, datetime
client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"

SYSTEM = """Extract invoice fields. Rules:
- Dates → YYYY-MM-DD. Amounts → plain numbers with '.' decimals (1.240,50 → 1240.50).
- If a field is not in the document, use null (or 'not_stated'). NEVER infer or invent.
- 'Zahlbar sofort' / 'due immediately' → due_on_receipt.
Example: "Receipt 77 total 10 USD" → invoice_date null, po_number null, payment_terms not_stated."""

def extract(text, feedback=None):
    content = text if not feedback else f"{text}\n\nYour previous output failed validation: {feedback}. Fix only that."
    resp = client.messages.create(model=MODEL, max_tokens=1024, system=SYSTEM,
        tools=[TOOL], tool_choice={"type": "tool", "name": "record_invoice"},   # guaranteed call
        messages=[{"role": "user", "content": content}])
    return next(b.input for b in resp.content if b.type == "tool_use")
```

## Step 4: Validate, then retry with the SPECIFIC error (bounded)

```python
def validate(d):
    if d.get("invoice_date"):
        try: datetime.date.fromisoformat(d["invoice_date"])
        except ValueError: return f"invoice_date '{d['invoice_date']}' is not YYYY-MM-DD"
    if d.get("total") is not None and d["total"] < 0:
        return "total must be non-negative"
    return None

def extract_with_retry(text, max_retries=2):
    data, error_log = extract(text), []
    for _ in range(max_retries):
        problem = validate(data)
        if not problem:
            break
        error_log.append({"error": problem})          # feed the pattern log (Step 6)
        data = extract(text, feedback=problem)
    return data, error_log
```

Note: there is **no retry for null fields**. Missing information can't be retried into existence.

## Step 5: Risk-based review routing

```python
CRITICAL = {"total", "currency", "invoice_number"}

def route(doc_id, data):
    reasons = []
    if CRITICAL & set(data.get("low_confidence_fields", [])):
        reasons.append("critical field low confidence")
    if data.get("total") is None:
        reasons.append("critical field missing")
    if data.get("currency") not in {"INR", "USD", "EUR", None}:
        reasons.append("unusual currency")
    return ("HUMAN_REVIEW", reasons) if reasons else ("AUTO_ACCEPT", [])

for doc_id, text in DOCS.items():
    data, errs = extract_with_retry(text)
    print(doc_id, json.dumps(data), route(doc_id, data), errs)
```

## Step 6: Close the feedback loop (design exercise)

Write down how you would:

1. Store each validation error with `doc_id`, field, error type and a `detected_pattern` (e.g. "European decimal comma").
2. Review the patterns weekly, and add a new rule or few-shot example when a pattern recurs.
3. Calibrate: label 100 documents by hand and compare with `low_confidence_fields`. Are the flags actually predictive per field?
4. Add **stratified sampling** of AUTO_ACCEPT items per document type for ongoing QA.

## What you practised

Forced `tool_choice` · nullable schema · enums with `not_stated` · normalisation + few-shot · retry with the specific error · no retry for missing data · field-level review routing.

??? tip "Bonus: run doc-1..doc-3 through the Batch API"
    Wrap each request with a `custom_id` equal to the `doc_id` and submit via the Message Batches API. Compare cost and latency with the synchronous run.
