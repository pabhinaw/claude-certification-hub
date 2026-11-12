"""Authoring helper for the Developer (CCDV-F) question bank.

Q(...)  single-answer question: one correct option + three wrong ones.
M(...)  multiple-response question: TWO correct options + three wrong ones.

Domain codes
  AI Applications & Integration      MS Model Selection & Optimisation
  AW Agents & Workflows              PC Prompt & Context Engineering
  TM Tools & MCPs                    SS Security & Safety
  CC Claude Code                     EV Eval, Testing & Debugging

All questions are ORIGINAL, written from public documentation and general
engineering practice. None are real or recalled exam items. All data is fictional.
"""
QUESTIONS = []
DOMS = {"AI", "MS", "AW", "PC", "TM", "SS", "CC", "EV"}


def Q(domain, topic, stem, correct, why, wrong, level=2):
    assert domain in DOMS, domain
    assert len(wrong) == 3 and all(len(w) == 2 for w in wrong), stem[:60]
    QUESTIONS.append(dict(domain=domain, topic=topic, stem=stem.strip(), level=level,
                          right=[(correct.strip(), why.strip())],
                          wrong=[(a.strip(), b.strip()) for a, b in wrong]))


def M(domain, topic, stem, right, wrong, level=2):
    assert domain in DOMS, domain
    assert len(right) == 2 and len(wrong) == 3, stem[:60]
    assert "TWO" in stem, "multiple-response stems must say 'Select TWO'"
    QUESTIONS.append(dict(domain=domain, topic=topic, stem=stem.strip(), level=level,
                          right=[(a.strip(), b.strip()) for a, b in right],
                          wrong=[(a.strip(), b.strip()) for a, b in wrong]))
