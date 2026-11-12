"""Tiny helper for authoring questions.

Each question is written with the CORRECT option first and the three wrong
options as (text, why_it_is_wrong) pairs. build.py shuffles options
deterministically so correct answers are spread evenly across A-D.

Scenario codes:
  S1 Customer support agent      S2 Code generation with Claude Code
  S3 Multi-agent research        S4 Developer productivity
  S5 Claude Code in CI/CD        S6 Structured data extraction
  G  General / cross-cutting
All questions are ORIGINAL, written from public documentation and design
principles. None are real or recalled exam items. All data is fictional.
"""
QUESTIONS = []

def Q(domain, scenario, topic, stem, correct, why, wrong, level=2):
    assert domain in {"D1", "D2", "D3", "D4", "D5"}, domain
    assert scenario in {"S1", "S2", "S3", "S4", "S5", "S6", "G"}, scenario
    assert len(wrong) == 3 and all(len(w) == 2 for w in wrong), stem[:60]
    QUESTIONS.append(dict(domain=domain, scenario=scenario, topic=topic, stem=stem.strip(),
                          correct=correct.strip(), why=why.strip(),
                          wrong=[(a.strip(), b.strip()) for a, b in wrong], level=level))
