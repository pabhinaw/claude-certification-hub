"""Lab 1 - A support agent loop with a prerequisite gate, structured tool
errors and a guaranteed resolution-or-escalation outcome.

Run without an API key (scripted demo):
    python lab01_agent_loop.py --dry-run

Run against the Claude API (set ANTHROPIC_API_KEY first):
    pip install anthropic
    python lab01_agent_loop.py "Hi, I'm CUST-TEST-01, please refund ORD-10001. OTP 123456"

All customers, orders and codes below are FICTIONAL test data.
"""
import argparse
import json
import os
import sys
from types import SimpleNamespace as NS

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")  # check the Models page for current names

# ----------------------------------------------------------------- fictional data
CUSTOMERS = {"CUST-TEST-01": {"otp": "123456"}}
ORDERS = {
    "ORD-10001": {"customer": "CUST-TEST-01", "amount": 1499, "status": "delivered"},
    "ORD-10002": {"customer": "CUST-TEST-01", "amount": 3500, "status": "delivered"},
}
REFUND_LIMIT = 2000

TOOLS = [
    {"name": "verify_customer",
     "description": "Verify a customer's identity with their one-time passcode. MUST succeed before any refund. "
                    "Input: customer_id like CUST-TEST-01 and the 6-digit otp.",
     "input_schema": {"type": "object",
                      "properties": {"customer_id": {"type": "string"}, "otp": {"type": "string"}},
                      "required": ["customer_id", "otp"]}},
    {"name": "lookup_order",
     "description": "Get the status and amount of ONE order. Input: order_id like ORD-10001. Read-only.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
    {"name": "process_refund",
     "description": "Refund an order for a VERIFIED customer. Requires verify_customer to have succeeded first. "
                    "Amounts above the agent limit are rejected; escalate those.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
    {"name": "escalate_to_human",
     "description": "Hand the case to a human. Use immediately if the customer asks for a person, "
                    "or when policy or limits prevent resolution.",
     "input_schema": {"type": "object",
                      "properties": {"reason": {"type": "string"}, "summary": {"type": "string"}},
                      "required": ["reason", "summary"]}},
]


def new_session():
    return {"verified_customer": None, "resolved": False, "escalated": False, "actions": []}


def err(category, message, retryable, action):
    return {"error_category": category, "is_retryable": retryable, "message": message, "suggested_action": action}


def run_tool(session, name, args):
    """Execute one tool. Returns (is_error, payload). Business rules are enforced HERE, in code."""
    session["actions"].append({"tool": name, "input": args})
    if name == "verify_customer":
        c = CUSTOMERS.get(args.get("customer_id"))
        if not c:
            return True, err("not_found", "No such customer", False, "Ask the customer to re-check their ID")
        if c["otp"] != args.get("otp"):
            return True, err("validation", "OTP incorrect", True, "Ask the customer for the OTP again")
        session["verified_customer"] = args["customer_id"]
        return False, {"verified": True}

    if name == "lookup_order":
        o = ORDERS.get(args.get("order_id"))
        return (False, o) if o else (True, err("not_found", "Order not found", False, "Confirm the order ID"))

    if name == "process_refund":
        if not session["verified_customer"]:                      # prerequisite gate
            return True, err("precondition", "Customer not verified", True, "Call verify_customer first")
        o = ORDERS.get(args.get("order_id"))
        if not o or o["customer"] != session["verified_customer"]:
            return True, err("permission", "Order does not belong to the verified customer", False, "Escalate")
        if o["amount"] > REFUND_LIMIT:                            # policy limit
            return True, err("business", "Above the agent refund limit", False, "Escalate for approval")
        session["resolved"] = True
        return False, {"refunded": o["amount"]}

    if name == "escalate_to_human":
        session["escalated"] = True
        return False, {"ticket": "HUMAN-QUEUE-001"}

    return True, err("validation", f"Unknown tool {name}", False, "Use one of the listed tools")


def handoff_package(session, reason):
    return {"reason": reason, "verified_customer": session["verified_customer"],
            "actions_taken": session["actions"], "resolved": session["resolved"]}


def agent(client, user_text, max_iterations=10, log=print):
    session = new_session()
    messages = [{"role": "user", "content": user_text}]
    for _ in range(max_iterations):
        resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS,
                                      system="You are a support agent for a fictional store. Be brief.",
                                      messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            break
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                is_error, payload = run_tool(session, block.name, block.input)
                log(f"  tool {block.name}({block.input}) -> {'ERROR ' if is_error else ''}{payload}")
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(payload), "is_error": is_error})
        messages.append({"role": "user", "content": results})

    # ---- orchestration-layer guarantee: every session ends resolved or escalated ----
    if not (session["resolved"] or session["escalated"]):
        session["escalated"] = True
        log("  [auto-escalation] no resolution recorded -> handoff:",
            json.dumps(handoff_package(session, "no resolution recorded")))
    return session


# ----------------------------------------------------------------- dry-run client
class ScriptedClient:
    """Replays scripted model turns so the loop logic can be tested without an API key."""

    def __init__(self, turns):
        self.turns = list(turns)
        self.messages = self

    def create(self, **_):
        if not self.turns:
            return NS(stop_reason="end_turn", content=[NS(type="text", text="(done)")])
        calls = self.turns.pop(0)
        if not calls:
            return NS(stop_reason="end_turn", content=[NS(type="text", text="All set!")])
        blocks = [NS(type="tool_use", id=f"toolu_{i}", name=n, input=a) for i, (n, a) in enumerate(calls)]
        return NS(stop_reason="tool_use", content=blocks)


def dry_run():
    scenarios = {
        "1. Refund attempted BEFORE verification (gate blocks it, model recovers)": [
            [("process_refund", {"order_id": "ORD-10001"})],
            [("verify_customer", {"customer_id": "CUST-TEST-01", "otp": "123456"})],
            [("process_refund", {"order_id": "ORD-10001"})],
            []],
        "2. Refund above the limit (business error, agent escalates)": [
            [("verify_customer", {"customer_id": "CUST-TEST-01", "otp": "123456"})],
            [("process_refund", {"order_id": "ORD-10002"})],
            [("escalate_to_human", {"reason": "over limit", "summary": "Refund 3500 needs approval"})],
            []],
        "3. Model stops without resolving (orchestration layer auto-escalates)": [
            [("lookup_order", {"order_id": "ORD-10001"})],
            []],
    }
    ok = True
    for title, turns in scenarios.items():
        print(f"\n{title}")
        s = agent(ScriptedClient(turns), "(scripted)")
        outcome = "RESOLVED" if s["resolved"] else "ESCALATED" if s["escalated"] else "NEITHER"
        print(f"  outcome: {outcome}")
        ok = ok and outcome != "NEITHER"
    print("\nAll sessions ended resolved or escalated:", ok)
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("message", nargs="?", default="Hi, I'm CUST-TEST-01, please refund ORD-10001.")
    p.add_argument("--dry-run", action="store_true", help="run scripted scenarios without an API key")
    a = p.parse_args()
    if a.dry_run:
        return dry_run()
    import anthropic  # imported here so --dry-run needs no dependencies
    session = agent(anthropic.Anthropic(), a.message)
    print(json.dumps({k: v for k, v in session.items() if k != "actions"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
