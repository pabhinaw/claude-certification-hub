"""Build the Developer (CCDV-F) question bank.

Run from the repo root:   python tools/qbank/build_dev.py

Outputs
  docs/assets/data/qbank-dev.json              data for the mock-exam engine
  docs/developer/question-bank/*.md            static, readable bank pages

All questions are original. See docs/resources/content-policy.md.
"""
import json, os, random, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "dev"))

import devlib  # noqa: E402
import q_ai, q_ms, q_rest  # noqa: E402,F401

DOMAINS = {
    "AI": "Applications & Integration",
    "MS": "Model Selection & Optimisation",
    "AW": "Agents & Workflows",
    "PC": "Prompt & Context Engineering",
    "TM": "Tools & MCPs",
    "SS": "Security & Safety",
    "CC": "Claude Code",
    "EV": "Eval, Testing & Debugging",
}
# 53-question mock, following the published weights 33.1/16.8/14.7/11.0/10.6/8.1/3.1/2.6 %
MOCK_COUNTS = {"AI": 18, "MS": 9, "AW": 8, "PC": 6, "TM": 5, "SS": 4, "CC": 2, "EV": 1}
MOCKS = ["A", "B"]
PAGES = [("ai", ["AI"]), ("ms", ["MS"]), ("aw", ["AW"]), ("pc", ["PC"]),
         ("tm", ["TM"]), ("ss", ["SS"]), ("cc-ev", ["CC", "EV"])]
LETTERS = "ABCDE"
SEED = "hub-dev-3"


def build():
    assert sum(MOCK_COUNTS.values()) == 53
    by_domain = defaultdict(list)
    for q in devlib.QUESTIONS:
        by_domain[q["domain"]].append(q)
    out = []
    spread = defaultdict(int)
    for d in DOMAINS:
        qs = by_domain[d]
        need = MOCK_COUNTS[d] * len(MOCKS)
        assert len(qs) >= need, f"{d}: {len(qs)} questions, mocks need {need}"
        rng = random.Random(f"{SEED}-{d}")
        picked = sorted(rng.sample(range(len(qs)), need))
        # alternate multiple-response and single-answer items separately, so mocks are comparable
        multi = [x for x in picked if len(qs[x]["right"]) == 2]
        single = [x for x in picked if len(qs[x]["right"]) == 1]
        mock_of, fill = {}, {m: 0 for m in MOCKS}
        for idx in multi:                                   # global alternation across domains
            m = MOCKS[spread["multi"] % len(MOCKS)]; spread["multi"] += 1
            mock_of[idx] = m; fill[m] += 1
        for k, idx in enumerate(single):
            m = MOCKS[k % len(MOCKS)]
            if fill[m] >= MOCK_COUNTS[d]:
                m = next(x for x in MOCKS if fill[x] < MOCK_COUNTS[d])
            mock_of[idx] = m; fill[m] += 1
        assert all(fill[m] == MOCK_COUNTS[d] for m in MOCKS), (d, fill)
        for i, q in enumerate(qs, start=1):
            qid = f"{d}-{i:03d}"
            wrong = list(q["wrong"]); rng.shuffle(wrong)
            n = len(q["right"]) + len(wrong)
            if len(q["right"]) == 1:
                key = mock_of.get(i - 1)
                slots = [spread[key] % 4]; spread[key] += 1  # spread evenly across A-D within each mock
            else:
                slots = sorted(rng.sample(range(n), 2))
            options, notes, ri, wi = [], [], 0, 0
            for s in range(n):
                if s in slots:
                    options.append(q["right"][ri][0]); notes.append(q["right"][ri][1]); ri += 1
                else:
                    options.append(wrong[wi][0]); notes.append(wrong[wi][1]); wi += 1
            item = dict(id=qid, domain=d, topic=q["topic"], level=q["level"], stem=q["stem"],
                        options=options, notes=notes, mock=mock_of.get(i - 1))
            if len(slots) == 1:
                item["answer"] = slots[0]
            else:
                item["answers"] = slots; item["select"] = 2
            out.append(item)
    # exam order: deterministic shuffle so domains are mixed, as in a real sitting
    for m in MOCKS:
        ids = [q["id"] for q in out if q["mock"] == m]
        random.Random(f"{SEED}-order-{m}").shuffle(ids)
        pos = {qid: k for k, qid in enumerate(ids)}
        for q in out:
            if q["mock"] == m:
                q["order"] = pos[q["id"]]
    return out


def esc(s):
    return s.replace("<", "&lt;").replace(">", "&gt;")


def stem_md(stem):
    """Keep indented code lines as a code block; escape the rest."""
    out, code = [], []
    for line in stem.split("\n"):
        if line.startswith("    "):
            code.append(line)
        else:
            if code:
                out += ["```python"] + [c[4:] for c in code] + ["```"]; code = []
            out.append(esc(line))
    if code:
        out += ["```python"] + [c[4:] for c in code] + ["```"]
    return "\n".join(out)


def write_pages(data):
    base = os.path.join(ROOT, "docs", "developer", "question-bank")
    os.makedirs(base, exist_ok=True)
    for slug, doms in PAGES:
        qs = [q for q in data if q["domain"] in doms]
        title = " · ".join(DOMAINS[d] for d in doms)
        multi = sum(1 for q in qs if "answers" in q)
        lines = [f"# Question Bank · {title}", "",
                 f"**{len(qs)} original questions** ({multi} multiple-response). Try each one before opening the "
                 "answer. Every answer explains why the correct option is right **and why each other option is wrong**.", "",
                 "!!! note \"Original practice material\"",
                 "    Written from public documentation and general engineering practice. These are not real or recalled "
                 "exam questions ([content policy](../../resources/content-policy.md)). For a timed experience, take a "
                 "[mock exam](../mock-exams.md).", ""]
        topics = sorted({q["topic"] for q in qs})
        lines += ["**Topics covered:** " + " · ".join(topics), "", "---", ""]
        for q in qs:
            dots = "●" * q["level"] + "○" * (3 - q["level"])
            kind = "Select TWO" if "answers" in q else "Single answer"
            lines.append(f'<p class="qb-meta"><span class="qb-id">{q["id"]}</span>'
                         f'<span>{esc(q["topic"])}</span><span>{kind}</span>'
                         f'<span title="Difficulty">{dots}</span></p>')
            lines += ["", stem_md(q["stem"]), ""]
            for i, o in enumerate(q["options"]):
                lines.append(f"- **{LETTERS[i]}.** {esc(o)}")
            lines.append("")
            right = q["answers"] if "answers" in q else [q["answer"]]
            label = " and ".join(LETTERS[i] for i in right)
            lines.append(f'??? success "Answer: {label}"')
            for i in right:
                lines.append(f"    **Why {LETTERS[i]} is right:** {esc(q['notes'][i])}")
                lines.append("")
            lines.append("    **Why the others are wrong:**")
            lines.append("")
            for i in range(len(q["options"])):
                if i not in right:
                    lines.append(f"    * **{LETTERS[i]}:** {esc(q['notes'][i])}")
            lines += ["", "---", ""]
        with open(os.path.join(base, f"{slug}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main():
    data = build()
    path = os.path.join(ROOT, "docs", "assets", "data")
    os.makedirs(path, exist_ok=True)
    payload = {"version": 1, "exam": "CCDV-F", "domains": DOMAINS, "mocks": MOCKS, "minutes": 120,
               "blurb": "weighted by domain · single and multiple-response · mixed order",
               "mockCounts": MOCK_COUNTS, "questions": data}
    with open(os.path.join(path, "qbank-dev.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    write_pages(data)
    print(f"{len(data)} questions written")
    for m in MOCKS:
        qs = [q for q in data if q["mock"] == m]
        print("mock", m, len(qs), "multi:", sum("answers" in q for q in qs),
              "answer spread:", [sum(q.get("answer") == k for q in qs) for k in range(4)])
    print("bank only:", sum(q["mock"] is None for q in data))


if __name__ == "__main__":
    main()
