# Prompt Engineering Basics <span class="level-badge">L1</span>

A **prompt** is everything you send Claude: the system prompt, the conversation, any documents and tool definitions. Prompt engineering means writing that input so the output is **correct, consistent and usable**.

## 1. Be clear and specific

Claude can't read your mind. Imagine briefing a smart new colleague who knows nothing about your project.

| ❌ Vague | ✅ Specific |
|---|---|
| "Summarise this." | "Summarise this incident report in 3 bullet points for an on-call engineer: what broke, the customer impact, and the current status." |
| "Make it better." | "Shorten to under 120 words, keep the two figures, and use plain English with no jargon." |

Say **who it's for**, **what good looks like**, the **format**, and any **constraints**.

## 2. Use a system prompt for role and rules

The `system` parameter holds stable instructions: role, tone, policies, output format. The user turn holds the specific task.

```python
system = "You are a support assistant for a fictional online bookstore. Answer in under 80 words. If you don't know, say so."
```

## 3. Structure long prompts with XML tags

Tags make it clear which part is instructions, data or examples:

```xml
<instructions>Extract the order ID and the customer's request.</instructions>
<email>
Hi, my order ORD-10001 arrived damaged, can I get a replacement?
</email>
<output_format>JSON with keys order_id and request</output_format>
```

## 4. Show examples (few-shot)

One to three **worked examples** are often the fastest way to get a consistent format, especially for edge cases. Use **varied** examples, not three near-identical ones.

## 5. Let Claude think when the task is hard

For multi-step reasoning, ask Claude to work through the problem before answering, or turn on extended or adaptive thinking. Keep the final answer in a separate, clearly marked part if your code parses it.

## 6. Give explicit criteria, not vague adjectives

"Flag risky transactions" is vague. "Flag a transaction if it is over 10,000, in a new country, or the third in 10 minutes" is testable and consistent.

## 7. Put long documents first, the question last

For long inputs, place the documents at the top and the instructions and question at the end. This also helps prompt caching, because the stable part becomes the prefix.

## 8. Prompts guide; code guarantees

A prompt makes good behaviour **likely**. If something must **always** or **never** happen, enforce it in code: schemas, `tool_choice`, hooks or permission rules. This idea runs through the whole Architect exam.

## Check yourself

??? question "Your extraction prompt works on clean PDFs but fails on scanned receipts. What's the cheapest first improvement?"
    Add one or two **few-shot examples** of scanned receipts (including a missing field shown as `null`), and give explicit normalisation rules.

??? question "A prompt says 'NEVER refund over 500'. Is that enough?"
    No. That's a hard business rule, so enforce it in code (for example a PreToolUse hook on the refund tool). The prompt can still explain the rule.

**Verify in official docs:** [Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
