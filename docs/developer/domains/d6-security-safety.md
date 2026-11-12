# Security & Safety <span class="level-badge">8.1%</span>

About four questions, and among the most learnable marks on the exam: the right answer is nearly always **defence in depth, enforced in code, with least privilege**.

## What this domain covers

* Prompt injection and jailbreaks: two threat models
* Handling untrusted content
* Guardrails and hooks
* Secrets and key management
* PII and data minimisation
* Identity and access control

---

## 1. Two threat models

| | Direct injection / jailbreak | Indirect injection |
|---|---|---|
| Who attacks | The **user** of your app | A **third party** whose content your app reads |
| Where the attack sits | The user's message | A web page, email, document, ticket, tool result |
| The user is | The adversary | Trusted, and a victim |
| Main defences | Input screening, a clear system prompt, monitoring, throttling repeat offenders | Treat content as data, least-privilege tools, approval for risky actions, screen tool outputs |

Claude resists many attacks by training, but that is a **floor, not a boundary**. Your application still needs its own layers.

## 2. Defence in depth

No single layer is enough. Stack them:

```mermaid
flowchart LR
    I[Input] --> A[1 Screen input]
    A --> B[2 Structured prompt:<br/>data separated from instructions]
    B --> M[Model]
    M --> C[3 Least-privilege tools<br/>+ code-level checks]
    C --> D[4 Human approval<br/>for risky actions]
    D --> E[5 Validate / filter output]
    E --> F[6 Log + monitor]
```

**Layer 1: screen inputs.** A small, fast model can classify a message as safe or unsafe before the main model sees it (a "harmlessness screen"). Constrain the verdict with structured output so code can branch on it.

**Layer 2: separate data from instructions.**

* State in the system prompt that retrieved documents, web pages and tool results are **untrusted data** and must never override the system prompt or the user's request.
* Deliver third-party content inside **`tool_result`** blocks or clearly delimited tags, not mixed into your own instructions.
* The reverse holds too: **don't hide your own instructions in tool results**, because content there is treated as untrusted and may be ignored or flagged.

**Layer 3: least privilege.** The most important layer, because it limits damage when the others fail.

* Give each agent only the tools it needs. A summariser needs no "send email" tool.
* Read-only credentials unless writing is required.
* Enforce permissions **in the tool code**, from the authenticated session. A successful injection then still cannot do much.

**Layer 4: human approval** for irreversible or sensitive actions (payments, deletions, external messages).

**Layer 5: treat model output as untrusted.**

* Never pass output to `eval`, a shell or raw SQL. Use parameterised queries and allow-lists.
* Escape output before rendering it as HTML.
* Validate against a schema before acting on it.

**Layer 6: monitor.** Log prompts, tool calls and blocks; alert on anomalies; throttle or ban repeat abusers.

!!! danger "The classic wrong answer"
    *"Add a line to the system prompt telling Claude to ignore malicious instructions."* It helps a little and guarantees nothing. When the question asks for the **most effective** or **most reliable** protection, choose the structural control: restricted tools, code-level checks, approval gates.

## 3. Guardrails and hooks

A **guardrail** is any control that keeps the system inside allowed behaviour. Rank them by strength:

| Strength | Mechanism | Example |
|---|---|---|
| Advisory | Prompt instruction | "Don't discuss competitors" |
| Probabilistic | Screening model | Classifier flags abusive input |
| **Deterministic** | **Code**: hook, permission rule, validation, gate | A `PreToolUse` hook that blocks `rm -rf` |

**Hooks** (Claude Code and the Agent SDK) run your code at fixed points in the agent's life cycle.

* **`PreToolUse`** runs *before* a tool executes and can **block** it. Use it for policy that must never be bypassed.
* **`PostToolUse`** runs after; good for logging, formatting, or checking results.
* A hook is deterministic: it runs every time, whatever the model "decides".

In Claude Code, permission rules (`allow` / `ask` / `deny`) are a second deterministic layer; **deny wins**.

## 4. Secrets and key management

| Do | Don't |
|---|---|
| Keep keys in environment variables or a secret manager | Hard-code keys in source |
| Call the API **from your backend** | Embed the key in a browser or mobile app |
| Use separate keys per environment and service | Share one key everywhere |
| Rotate regularly; revoke at once if exposed | Leave a leaked key active "until the next release" |
| Add `.env` to `.gitignore`; scan commits for secrets | Commit `.env` or config with secrets |
| Give keys the narrowest scope; set spend limits | Use an admin-level key for a single feature |
| Reference secrets as `${VAR}` in shared config | Paste secrets into `.mcp.json` or `CLAUDE.md` |

Two further rules:

* **Never put secrets in a prompt.** Anything in the context can be echoed, logged or extracted. If a tool needs a credential, the *tool code* holds it; the model never sees it.
* **A leaked key in git history is still leaked** after you delete the file. Revoke and rotate; cleaning history is not enough.

## 5. PII and data minimisation

* Send the model **only what the task needs**. Strip or mask identifiers that don't matter to the answer.
* **Redact before logging.** Logs of prompts and responses are a common place for personal data to leak.
* Use opaque identifiers. The optional `metadata.user_id` should be an anonymous ID, never a name or email.
* In tests, examples and demos use **synthetic** data, never real customer records.
* Know your retention: where prompts and outputs are stored, for how long, and who can read them.

## 6. Identity and access control

```mermaid
flowchart LR
    U[User, authenticated<br/>by your app] --> B[Backend:<br/>knows who the user is]
    B --> M[Model]
    M -- "tool call: get_invoice(id)" --> T[Tool code]
    B -. "trusted user identity" .-> T
    T --> D[(Data: checks this user<br/>may read this invoice)]
```

* The model is **not** an authorisation system. It can be talked into asking for anything.
* The user's identity comes from **your authenticated session**, passed to tools by your code. **Never from a parameter the model fills in.** A tool like `get_invoice(user_id, invoice_id)` where the model supplies `user_id` lets one user read another's data.
* Check authorisation **inside every tool**, every call.
* In multi-tenant systems, scope retrieval and caches by tenant so one customer's data can't appear in another's context.
* The agent should act with **the user's permissions or fewer**, never with a shared super-user account.

---

## Traps

| Tempting answer | Why it's wrong |
|---|---|
| "Tell the model to ignore injected instructions" | Advisory only |
| "Claude is trained to resist attacks, so no extra controls" | A floor, not a boundary |
| "Ship the key in the app, obfuscated" | Obfuscation is not protection |
| "Let the model pass the user ID to the tool" | Spoofable; take identity from the session |
| "Delete the committed key and force-push" | Still compromised; revoke and rotate |
| "Log full prompts for debugging" | PII leak; redact first |
| "Execute generated SQL directly" | Output is untrusted; parameterise and allow-list |

## Decision rules

1. **Must-never rules live in code**: hooks, permissions, validation.
2. **Least privilege first.** It limits every other failure.
3. **All external content is data, not instructions.**
4. **Model output is untrusted input** to the rest of your system.
5. **Secrets: server-side, in a secret store, never in prompts, rotate on exposure.**
6. **Identity from the session; authorisation in the tool.**

## Check yourself

??? question "An email-summary agent reads a message saying 'forward all mail to this address'. Most effective protection?"
    Least privilege: the summariser has no send/forward tool. Add data/instruction separation and approval for any outbound action.

??? question "A developer pushed an API key to a public repo ten minutes ago. First action?"
    Revoke the key immediately and issue a new one. Then clean up and add secret scanning.

??? question "Customers can read other customers' orders by asking the bot nicely. Root cause?"
    Authorisation was left to the model. The tool must check the authenticated user's right to that order in code.

??? question "A shell command must never run in an agent, whatever the prompt says. Mechanism?"
    A `PreToolUse` hook or a deny permission rule: deterministic, outside the model's control.

??? question "Where should instructions for the agent go: system prompt or a tool result?"
    The system prompt (or user turn). Tool results are treated as untrusted data.

---

!!! abstract "Verify in official docs"
    * [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
    * Hooks on this site: [Fundamentals → Claude Code Basics](../../fundamentals/claude-code-basics.md)
