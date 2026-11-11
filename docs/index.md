---
hide:
  - navigation
---

# Claude Certification Hub

**One place to go from "what is Claude?" to passing Anthropic's Claude certifications, and to building real production systems along the way.**

This site is organised the way a good course is: understand the exam, build the fundamentals, master each domain, practise, then review. Every page is tagged with a level so you always know where you are.

<div class="grid cards" markdown>

-   :material-compass-outline:{ .lg .middle } **Start Here**

    ---

    Which certification fits you, what each one costs and covers, and a basic-to-advanced roadmap.

    [:octicons-arrow-right-24: Orientation](start-here/index.md)

-   :material-book-open-variant:{ .lg .middle } **Fundamentals**

    ---

    The Messages API, tool use, Claude Code and MCP explained from zero. No prior AI experience assumed.

    [:octicons-arrow-right-24: Learn the basics](fundamentals/index.md)

-   :material-sitemap:{ .lg .middle } **Architect (CCAR-F)**

    ---

    Full track: exam overview, blueprint, the six scenarios, five domain deep-dives, practice questions and a cheat sheet.

    [:octicons-arrow-right-24: Architect track](architect/index.md)

-   :material-code-braces:{ .lg .middle } **Developer (CCDV-F)**

    ---

    Exam overview and a bridge from the Architect track. Domain deep-dives are coming next.

    [:octicons-arrow-right-24: Developer track](developer/index.md)

-   :material-flask-outline:{ .lg .middle } **Hands-on Labs**

    ---

    Build an agentic loop, a reliable extraction pipeline and a team-ready Claude Code setup.

    [:octicons-arrow-right-24: Start building](labs/index.md)

-   :material-lightning-bolt:{ .lg .middle } **Cheat Sheet**

    ---

    The decision rules that answer most scenario questions, on one page.

    [:octicons-arrow-right-24: Quick review](architect/cheat-sheet.md)

</div>

## How the levels work

| Badge | Level | You can… |
|---|---|---|
| <span class="level-badge">L1</span> | **Basic** | explain what Claude, the Messages API, tools, Claude Code and MCP are |
| <span class="level-badge">L2</span> | **Intermediate** | build a working tool-using app and configure Claude Code for yourself |
| <span class="level-badge">L3</span> | **Advanced** | design multi-agent systems, team-wide configurations and reliable extraction pipelines |
| <span class="level-badge">L4</span> | **Exam-ready** | pick the *best* option among several plausible ones, under time pressure |

!!! tip "The single most important idea in these exams"
    The exams reward **deterministic guarantees over hopeful instructions**. When a question asks how to make something *always* happen (a tool is always called, a policy is never broken, a session always ends with a resolution), the answer is almost always something enforced in code, configuration, hooks or schemas, not "add a sentence to the prompt".

## Who built this

This hub was started by a CCAR-F certified engineer, who passed with **893/1000** on the first attempt, to give back to fellow learners. Read [My Exam Journey](about/my-journey.md) for honest notes on what was hard.

!!! note "Disclaimer"
    This is an independent community resource. It is not affiliated with or endorsed by Anthropic, and it contains **no real exam questions**. All practice questions are original. Exam details change, so always confirm on the [official pages](resources/official-links.md).
