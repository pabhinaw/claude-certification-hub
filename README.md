# Claude Certification Hub

A free, community-built, **basic → advanced** learning platform for Anthropic's Claude certifications:

1. **Claude Certified Architect – Foundations (CCAR-F)** — complete track
2. **Claude Certified Developer – Foundations (CCDV-F)** — in progress

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published with GitHub Pages.

> Unofficial and independent: not affiliated with, sponsored or endorsed by Anthropic. Contains no real or recalled exam questions. Claude and Anthropic are trademarks of Anthropic, PBC.

---

## Project layout

```
claude-certification-hub/
├── mkdocs.yml                 ← site settings + navigation menu
├── requirements.txt           ← the one Python package the site needs
├── .github/workflows/deploy.yml  ← auto-publishes the site on every push
└── docs/                      ← ALL the content (plain Markdown files)
    ├── index.md               ← home page
    ├── start-here/            ← orientation, roadmap, study method
    ├── fundamentals/          ← basic level (API, tools, Claude Code, MCP)
    ├── architect/             ← CCAR-F track (overview, blueprint, 5 domains, practice)
    ├── developer/             ← CCDV-F track
    ├── labs/                  ← hands-on exercises
    ├── resources/             ← official links, contributing
    └── about/                 ← author's exam journey
```

To add a page: create a `.md` file under `docs/`, then add one line for it under `nav:` in `mkdocs.yml`.

---

## Publish to GitHub Pages — step by step (first time)

**Step 1 — Create a GitHub account** (skip if you have one) at https://github.com.

**Step 2 — Create an empty repository**
- Click **+** (top right) → **New repository**
- Name: `claude-certification-hub` · Visibility: **Public**
- Do **not** tick "Add a README" (we already have one) → **Create repository**

**Step 3 — Upload this folder.** Easiest beginner route is **GitHub Desktop** (https://desktop.github.com):
- File → **Add local repository** → choose this folder → it will offer to "create a repository" → click it
- Write a summary like `first version` → **Commit to main** → **Publish repository**
  (untick "Keep this code private")

**Step 4 — Put your username in `mkdocs.yml`.** Replace every `YOUR-GITHUB-USERNAME` with your GitHub username, commit and push again.

**Step 5 — Turn on Pages**
- In the repo on github.com: **Settings → Pages**
- Under **Build and deployment → Source**, choose **GitHub Actions**

**Step 6 — Watch it build.** Open the **Actions** tab. When the green tick appears (1–2 minutes), your site is live at
`https://YOUR-GITHUB-USERNAME.github.io/claude-certification-hub/`

From now on, every time you commit and push, the site rebuilds itself.

---

## Preview locally (optional)

```bash
pip install -r requirements.txt
mkdocs serve
```
Then open http://127.0.0.1:8000 — the page refreshes as you edit.

## Privacy rule for this repo

Never commit score reports, candidate IDs, registration numbers, API keys or real customer data.
The `.gitignore` already blocks `*scorereport*.pdf`, `.env` and a `private/` folder.

## License

Content: CC BY 4.0. Code samples: MIT.
