"""Lab 2 - Reliable structured extraction: forced tool output, a nullable
schema, validation with specific-error retries, and risk-based review routing.

Run without an API key (scripted demo):
    python lab02_extraction.py --dry-run

Run against the Claude API (set ANTHROPIC_API_KEY first):
    pip install anthropic
    python lab02_extraction.py

All documents below are FICTIONAL.
"""
import argparse
import datetime
import json
import os
import sys
from types import SimpleNamespace as NS

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")

DOCS = {
    "doc-1": "INVOICE #A-1001\nDate: 2026-02-14\nBill to: Example Traders Pvt Ltd\nPO: PO-7788\nTotal: INR 12,500.00\nTerms: Net 30",
    "doc-2": "Rechnung Nr. 55-B · Datum: 5. März 2026 · Gesamt: 1.240,50 EUR · Zahlbar sofort",
    "doc-3": "Receipt 9912 -- total 89.99 USD -- thank you!",
}

SCHEMA = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string"},
        "invoice_date": {"type": ["string", "null"], "description": "ISO 8601 YYYY-MM-DD. null if not present. Never guess."},
        "po_number": {"type": ["string", "null"], "description": "null if no PO number appears."},
        "total": {"type": ["number", "null"], "description": "Plain number with '.' as the decimal separator."},
        "currency": {"type": ["string", "null"], "description": "ISO 4217 code, e.g. INR, EUR, USD."},
        "payment_terms": {"type": "string", "enum": ["net_30", "net_60", "due_on_receipt", "other", "not_stated"]},
        "low_confidence_fields": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["invoice_number", "payment_terms", "low_confidence_fields"],
}
TOOL = {"name": "record_invoice", "description": "Record fields extracted from ONE invoice.", "input_schema": SCHEMA}

SYSTEM = """Extract invoice fields. Rules:
- Dates -> YYYY-MM-DD. Amounts -> plain numbers with '.' decimals (1.240,50 -> 1240.50).
- If a field is not in the document, use null (or 'not_stated'). NEVER infer or invent.
- 'Zahlbar sofort' / 'due immediately' -> due_on_receipt.
Example: "Receipt 77 total 10 USD" -> invoice_date null, po_number null, payment_terms not_stated."""

CRITICAL = {"total", "currency", "invoice_number"}


def extract(client, text, feedback=None):
    content = text if not feedback else f"{text}\n\nYour previous output failed validation: {feedback}. Fix only that."
    resp = client.messages.create(model=MODEL, max_tokens=1024, system=SYSTEM, tools=[TOOL],
                                  tool_choice={"type": "tool", "name": "record_invoice"},   # guaranteed call
                                  messages=[{"role": "user", "content": content}])
    return next(b.input for b in resp.content if b.type == "tool_use")


def validate(d):
    if d.get("invoice_date"):
        try:
            datetime.date.fromisoformat(d["invoice_date"])
        except ValueError:
            return f"invoice_date '{d['invoice_date']}' is not a valid YYYY-MM-DD date"
    if d.get("total") is not None and d["total"] < 0:
        return "total must be non-negative"
    return None


def extract_with_retry(client, text, max_retries=2):
    data, log = extract(client, text), []
    for _ in range(max_retries):
        problem = validate(data)
        if not problem:
            break
        log.append(problem)                      # feeds the error-pattern log
        data = extract(client, text, feedback=problem)
    return data, log


def route(data):
    reasons = []
    if CRITICAL & set(data.get("low_confidence_fields", [])):
        reasons.append("critical field low confidence")
    if data.get("total") is None:
        reasons.append("critical field missing")
    return ("HUMAN_REVIEW", reasons) if reasons else ("AUTO_ACCEPT", [])


class ScriptedClient:
    """Returns scripted tool inputs so the pipeline can be tested without an API key."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.messages = self

    def create(self, **_):
        return NS(stop_reason="tool_use", content=[NS(type="tool_use", id="t", name="record_invoice",
                                                      input=self.outputs.pop(0))])


def dry_run():
    scripted = {
        "doc-1": [{"invoice_number": "A-1001", "invoice_date": "2026-02-14", "po_number": "PO-7788", "total": 12500.0,
                   "currency": "INR", "payment_terms": "net_30", "low_confidence_fields": []}],
        "doc-2": [  # first attempt has a bad date -> retry with the specific error
            {"invoice_number": "55-B", "invoice_date": "5. März 2026", "po_number": None, "total": 1240.5,
             "currency": "EUR", "payment_terms": "due_on_receipt", "low_confidence_fields": []},
            {"invoice_number": "55-B", "invoice_date": "2026-03-05", "po_number": None, "total": 1240.5,
             "currency": "EUR", "payment_terms": "due_on_receipt", "low_confidence_fields": []}],
        "doc-3": [{"invoice_number": "9912", "invoice_date": None, "po_number": None, "total": 89.99,
                   "currency": "USD", "payment_terms": "not_stated", "low_confidence_fields": ["total"]}],
    }
    expected = {"doc-1": "AUTO_ACCEPT", "doc-2": "AUTO_ACCEPT", "doc-3": "HUMAN_REVIEW"}
    ok = True
    for doc_id, text in DOCS.items():
        data, errors = extract_with_retry(ScriptedClient(scripted[doc_id]), text)
        decision, reasons = route(data)
        print(f"{doc_id}: {decision} {reasons} | retries: {errors}")
        print("   ", json.dumps(data, ensure_ascii=False))
        ok = ok and decision == expected[doc_id] and validate(data) is None
    print("\nDry run checks passed:", ok)
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if a.dry_run:
        return dry_run()
    import anthropic
    client = anthropic.Anthropic()
    for doc_id, text in DOCS.items():
        data, errors = extract_with_retry(client, text)
        print(doc_id, route(data), errors, json.dumps(data, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
