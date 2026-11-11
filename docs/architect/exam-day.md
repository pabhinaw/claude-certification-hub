# Exam Day Guide

## The week before

- [ ] Confirm your booking, time zone and ID requirements in the confirmation email
- [ ] Run the proctoring system check on the **same computer and network** you'll use
- [ ] Plan a quiet room with a clear desk; tell family or housemates you'll be unavailable for about 2.5 hours
- [ ] Final pass: [Cheat Sheet](cheat-sheet.md) + your wrong answers from [Practice](practice-questions.md)

## Time strategy (60 questions · 120 minutes)

* Budget about **1 min 45 s per question**, keeping about 15 minutes for review.
* Questions come grouped by **scenario**. Read the scenario setup carefully once; most answers depend on a detail in it (team-wide vs personal, blocking vs not, strict vs flexible).
* **Flag and move on** if you're stuck past 3 minutes.

## Reading a question

1. **Find the keyword that sets the requirement**: *always / never / guarantee / most reliable / least effort / team-wide / personal / waiting / overnight / strict*.
2. **Name the domain principle** it maps to (guarantee → hooks/schema/tool_choice; team → project scope; waiting → sync…).
3. **Eliminate** the "prompt harder", "bigger model", "more retries", "parse the text" options.
4. Between the last two, pick the one that is **deterministic, targeted, and at the correct scope**.

## Common distractor patterns

| Distractor | Why it's tempting | Why it loses |
|---|---|---|
| Strengthen the system prompt | It often helps in practice | Not a guarantee |
| Use a larger model / bigger context | Feels like "more power" | Doesn't fix a design flaw |
| Add retries | Works for transient errors | Useless for missing info or logic errors |
| Self-review in the same context | Cheap | Biased; use an independent instance |
| Random sampling | Statistically familiar | Misses rare high-risk cases |
| Configure at user scope | Quick for you | Teammates don't get it |

## After the exam

You'll get a result and a **score report with a per-area breakdown**. Even if you pass, note your weakest areas; they're the best map for real-world improvement (and for the Developer exam). Remember that exam questions stay confidential: discuss topics, never questions.
