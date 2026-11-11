# Lab 1 · Build an Agentic Loop <span class="level-badge">L2</span>

**Goal:** a small support agent that

* loops correctly on `stop_reason`,
* can't refund before verification (code gate),
* returns structured tool errors,
* and **always** ends resolved or escalated.

## Step 1: Fake backend (fictional data)

Create `lab1_agent.py`:

```python
import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"   # check the Models page for current names

# --- Fictional test data -------------------------------------------------
CUSTOMERS = {"CUST-TEST-01": {"otp": "123456", "name": "Test User"}}
ORDERS = {"ORD-10001": {"customer": "CUST-TEST-01", "amount": 1499, "status": "delivered"}}
REFUND_LIMIT = 2000

session = {"verified_customer": None, "resolved": False, "escalated": False}
```

## Step 2: Tools with strong descriptions

```python
TOOLS = [
  {"name": "verify_customer",
   "description": "Verify a customer's identity with their one-time passcode. MUST succeed before any refund. Input: customer_id like CUST-TEST-01 and the 6-digit otp.",
   "input_schema": {"type": "object",
                    "properties": {"customer_id": {"type": "string"}, "otp": {"type": "string"}},
                    "required": ["customer_id", "otp"]}},
  {"name": "lookup_order",
   "description": "Get status and amount of ONE order. Input: order_id like ORD-10001. Does not change anything.",
   "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
  {"name": "process_refund",
   "description": "Refund an order for a VERIFIED customer. Requires verify_customer to have succeeded first. Amounts above the agent limit are rejected; escalate those.",
   "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
  {"name": "escalate_to_human",
   "description": "Hand the case to a human. Use immediately if the customer asks for a person, or when policy or limits prevent resolution.",
   "input_schema": {"type": "object",
                    "properties": {"reason": {"type": "string"}, "summary": {"type": "string"}},
                    "required": ["reason", "summary"]}},
]
```

## Step 3: Tool execution with a gate and structured errors

```python
def err(category, message, retryable, action):
    return {"error_category": category, "is_retryable": retryable,
            "message": message, "suggested_action": action}

def run_tool(name, args):
    if name == "verify_customer":
        c = CUSTOMERS.get(args["customer_id"])
        if not c:
            return True, err("not_found", "No such customer", False, "Ask the customer to re-check their ID")
        if c["otp"] != args["otp"]:
            return True, err("validation", "OTP incorrect", True, "Ask for the OTP again")
        session["verified_customer"] = args["customer_id"]
        return False, {"verified": True}

    if name == "lookup_order":
        o = ORDERS.get(args["order_id"])
        return (False, o) if o else (True, err("not_found", "Order not found", False, "Confirm the order ID"))

    if name == "process_refund":
        # ---- PREREQUISITE GATE: deterministic, not a prompt ----
        if not session["verified_customer"]:
            return True, err("precondition", "Customer not verified", True, "Call verify_customer first")
        o = ORDERS.get(args["order_id"])
        if not o or o["customer"] != session["verified_customer"]:
            return True, err("permission", "Order does not belong to verified customer", False, "Escalate")
        if o["amount"] > REFUND_LIMIT:
            return True, err("business", "Above agent refund limit", False, "Escalate for approval")
        session["resolved"] = True
        return False, {"refunded": o["amount"]}

    if name == "escalate_to_human":
        session["escalated"] = True
        return False, {"ticket": "HUMAN-QUEUE-001"}

    return True, err("validation", f"Unknown tool {name}", False, "Use a listed tool")
```

## Step 4: The loop and the termination guarantee

```python
def agent(user_text, max_iterations=10):
    messages = [{"role": "user", "content": user_text}]
    for _ in range(max_iterations):
        resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS,
            system="You are a support agent for a fictional store. Be brief.",
            messages=messages)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            break                                   # end_turn, max_tokens, refusal…

        results = []
        for block in resp.content:
            if block.type == "tool_use":
                is_error, payload = run_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(payload), "is_error": is_error})
        messages.append({"role": "user", "content": results})

    # ---- ORCHESTRATION-LAYER GUARANTEE ----
    if not (session["resolved"] or session["escalated"]):
        session["escalated"] = True
        print("[auto-escalation] no resolution recorded; created handoff for human queue")
    return messages

if __name__ == "__main__":
    agent("Hi, I'm CUST-TEST-01, please refund ORD-10001.")
    print(session)
```

## Step 5: Experiments (this is where the learning is)

1. Run it as is. Does Claude ask for the OTP? (It should; the refund is gated.)
2. Change the message to include `otp 123456`. Watch verify → refund.
3. Set the order amount to `3500`. Observe the *business* error and the escalation.
4. Comment out the gate in `process_refund` and ask for a refund without an OTP. What happens? **This is why prompts aren't guarantees.**
5. Say "I want a human". Does it escalate immediately?
6. Set `max_iterations=1` and confirm the auto-escalation fires.

## What you practised

`stop_reason` loop · `tool_result` with `is_error` · prerequisite gate · structured error categories · guaranteed resolution-or-escalation.
