"""Build the question bank.

Run from the repo root:   python tools/qbank/build.py

Outputs
  docs/assets/data/qbank.json                      data for the mock-exam engine
  docs/architect/question-bank/d1.md ... d5.md     static, readable bank pages

All questions are original. See docs/resources/content-policy.md.
"""
import json, os, random, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import qlib  # noqa: E402
import q_core, q_d1, q_d2, q_d3, q_d4, q_d5, q_multi  # noqa: E402,F401
from overrides import OV, OV2  # noqa: E402

DOMAINS = {
    "D1": "Agentic Architecture & Orchestration",
    "D2": "Tool Design & MCP Integration",
    "D3": "Claude Code Configuration & Workflows",
    "D4": "Prompt Engineering & Structured Output",
    "D5": "Context Management & Reliability",
}
SCENARIOS = {
    "S1": "Customer support agent", "S2": "Code generation with Claude Code",
    "S3": "Multi-agent research", "S4": "Developer productivity",
    "S5": "Claude Code in CI/CD", "S6": "Structured data extraction", "G": "General",
}
# 60-question mock: weights 27/18/20/20/15 %
MOCK_COUNTS = {"D1": 16, "D2": 11, "D3": 12, "D4": 12, "D5": 9}
MOCKS = ["A", "B", "C"]
# Editorial difficulty: questions that combine several concepts or hinge on a subtle detail
HARD = {"D1-031", "D1-033", "D1-042", "D1-046", "D2-015", "D2-016", "D2-020", "D2-021", "D2-022",
        "D3-029", "D3-030", "D3-034", "D3-035", "D4-033", "D4-040", "D5-018", "D5-022", "D5-024"}
LETTERS = "ABCDE"
# Short scenario framing shown above each question (our own wording).
SCENARIO_INTRO = {
    "S1": "You are building an agent that resolves customer issues such as orders, refunds and account changes with backend tools, and escalates to people when needed.",
    "S2": "Your team uses Claude Code to write, refactor and document code, and wants consistent, shared configuration across the repository.",
    "S3": "A coordinator agent delegates searching, analysis and synthesis to specialised sub-agents and produces a cited report.",
    "S4": "You are building tools that help engineers explore unfamiliar codebases and automate routine work, using built-in tools and MCP servers.",
    "S5": "Claude Code runs in a CI/CD pipeline to review changes, generate tests and report findings without human interaction.",
    "S6": "A pipeline extracts structured fields from unstructured documents, validates them and routes uncertain results to people.",
}
# Exam simulation: 4 of the 6 scenarios, 15 questions each, like the published exam structure.
SIM = {"type": "scenarios", "pick": 4, "per": 15, "filler": "G"}


def build():
    by_domain = defaultdict(list)
    for q in qlib.QUESTIONS:
        by_domain[q["domain"]].append(q)

    out = []
    for d in sorted(by_domain):
        qs = by_domain[d]
        rng = random.Random(f"hub-{d}")
        mock_fill = {m: 0 for m in MOCKS}
        for i, q in enumerate(qs, start=1):
            qid = f"{d}-{i:03d}"
            if qid in OV:
                new_c, new_w = OV.pop(qid)
                q = dict(q)
                if new_c:
                    q["correct"] = new_c
                if new_w:
                    q["wrong"] = [(nw if nw else ow, note) for nw, (ow, note) in zip(new_w, q["wrong"])]
            if qid in OV2:
                q = dict(q)
                repl = OV2.pop(qid)
                new = []
                for ow, note in q["wrong"]:
                    if ow in repl:
                        new.append((repl.pop(ow), note))
                    else:
                        new.append((ow, note))
                assert not repl, f"{qid}: unmatched OV2 texts {list(repl)}"
                q["wrong"] = new
            pos = (i - 1) % 4  # spread correct answers evenly across A-D
            wrong = list(q["wrong"])
            rng.shuffle(wrong)
            options, notes = [], []
            wi = 0
            multi = q.get("multi")
            if multi:
                slots = sorted(random.Random(f"hub-multi-{qid}").sample(range(5), 2)); ri = 0
                for slot in range(5):
                    if slot in slots:
                        options.append(multi[ri][0]); notes.append(multi[ri][1]); ri += 1
                    else:
                        options.append(wrong[wi][0]); notes.append(wrong[wi][1]); wi += 1
            for slot in range(0 if multi else 4):
                if slot == pos:
                    options.append(q["correct"]); notes.append(q["why"])
                else:
                    options.append(wrong[wi][0]); notes.append(wrong[wi][1]); wi += 1
            # round-robin assignment into mocks until each is full
            mock = None
            m = MOCKS[(i - 1) % 3]
            if mock_fill[m] < MOCK_COUNTS[d]:
                mock = m; mock_fill[m] += 1
            else:
                for alt in MOCKS:
                    if mock_fill[alt] < MOCK_COUNTS[d]:
                        mock = alt; mock_fill[alt] += 1; break
            item = dict(id=qid, domain=d, scenario=q["scenario"], topic=q["topic"],
                        level=3 if qid in HARD else q["level"], stem=q["stem"], options=options,
                        notes=notes, mock=mock)
            if multi:
                item["answers"] = slots; item["select"] = 2
            else:
                item["answer"] = pos
            out.append(item)
        short = {m: MOCK_COUNTS[d] - mock_fill[m] for m in MOCKS if mock_fill[m] < MOCK_COUNTS[d]}
        assert not short, f"{d} lacks questions for mocks: {short}"
    # Put the multiple-response questions into the mocks: each replaces the last
    # single-answer question of the same domain in its mock, so domain counts stay exact.
    multis = [q for q in out if "answers" in q and q["mock"] is None]
    for k, mq in enumerate(multis):
        m = MOCKS[k % len(MOCKS)]
        victim = [q for q in out if q["mock"] == m and q["domain"] == mq["domain"] and "answer" in q][-1]
        victim["mock"] = None; mq["mock"] = m
    for d in DOMAINS:
        for m in MOCKS:
            assert sum(1 for q in out if q["domain"] == d and q["mock"] == m) == MOCK_COUNTS[d], (d, m)
    return out


def check_overrides_used():
    assert not OV, f"Unknown override IDs: {sorted(OV)}"
    assert not OV2, f"Unknown OV2 IDs: {sorted(OV2)}"


def md_escape(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")


def write_pages(data):
    base = os.path.join(ROOT, "docs", "architect", "question-bank")
    os.makedirs(base, exist_ok=True)
    for d, name in DOMAINS.items():
        qs = [q for q in data if q["domain"] == d]
        lines = [f"# Question Bank · {d} {name}", "",
                 f"**{len(qs)} original questions.** Try each one before opening the answer. Every answer explains "
                 "why the correct option is right **and why each other option is wrong**.", "",
                 "!!! note \"Original practice material\"",
                 "    Written from public documentation and design principles. These are not real or recalled exam questions "
                 "([content policy](../../resources/content-policy.md)). For a timed experience, take a "
                 "[mock exam](../mock-exams.md).", ""]
        topics = sorted({q["topic"] for q in qs})
        lines += ["**Topics covered:** " + " · ".join(topics), "", "---", ""]
        for q in qs:
            dots = "●" * q["level"] + "○" * (3 - q["level"])
            lines.append(f'<p class="qb-meta"><span class="qb-id">{q["id"]}</span>'
                         f'<span>{md_escape(q["topic"])}</span><span>{SCENARIOS[q["scenario"]]}</span>'
                         f'<span title="Difficulty">{dots}</span></p>')
            lines.append("")
            lines.append(md_escape(q["stem"]))
            lines.append("")
            for i, o in enumerate(q["options"]):
                lines.append(f"- **{LETTERS[i]}.** {md_escape(o)}")
            lines.append("")
            right = q["answers"] if "answers" in q else [q["answer"]]
            lines.append(f'??? success "Answer: {" and ".join(LETTERS[i] for i in right)}"')
            for i in right:
                lines.append(f'    **Why {LETTERS[i]} is right:** {md_escape(q["notes"][i])}')
                lines.append("")
            lines.append("    **Why the others are wrong:**")
            lines.append("")
            for i in range(len(q["options"])):
                if i not in right:
                    lines.append(f"    * **{LETTERS[i]}:** {md_escape(q['notes'][i])}")
            lines.append("")
            lines.append("---")
            lines.append("")
        with open(os.path.join(base, f"{d.lower()}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main():
    data = build()
    check_overrides_used()
    path = os.path.join(ROOT, "docs", "assets", "data")
    os.makedirs(path, exist_ok=True)
    payload = {"version": 2, "exam": "CCAR-F", "domains": DOMAINS, "scenarios": SCENARIOS,
               "scenarioIntro": SCENARIO_INTRO, "sim": SIM, "minutes": 120,
               "mockCounts": MOCK_COUNTS, "questions": data}
    with open(os.path.join(path, "qbank.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    write_pages(data)
    counts = defaultdict(int)
    for q in data:
        counts[(q["domain"], q["mock"])] += 1
    print(f"{len(data)} questions written")
    for d in DOMAINS:
        print(d, {m: counts[(d, m)] for m in MOCKS + [None]})


if __name__ == "__main__":
    main()
