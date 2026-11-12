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
    ├── notes/                 ← Study Notes articles
    ├── resources/             ← official links, contributing
    └── about/                 ← about the author, how I prepared
```

Also at the top level:

```
├── overrides/            ← custom page templates (home, learner stories, reviewed-by line)
├── labs-code/            ← runnable lab code (dry-run mode needs no API key)
└── tools/qbank/          ← question-bank source files + build script
```

To add a page: create a `.md` file under `docs/`, then add one line for it under `nav:` in `mkdocs.yml`.

## Updating the question bank

Questions live in `tools/qbank/q_*.py` (one file per domain). After editing, regenerate the bank pages and the mock-exam data:

```bash
python tools/qbank/build.py
```

The script assigns IDs, spreads correct answers evenly across A–D, builds three non-overlapping 60-question mocks weighted by domain, and writes `docs/assets/data/qbank.json` and `docs/architect/question-bank/d1.md`–`d5.md`. Commit the generated files too.

The Developer bank works the same way. Questions live in `tools/qbank/dev/q_*.py` (`Q(...)` for single-answer, `M(...)` for "Select TWO"):

```bash
python tools/qbank/build_dev.py
```

It writes `docs/assets/data/qbank-dev.json` and `docs/developer/question-bank/*.md`, and builds three non-overlapping 53-question mocks.

---

## Publish to GitHub Pages — step by step (first time)

**Step 1 — Create a GitHub account** (skip if you have one) at https://github.com.

**Step 2 — Create an empty repository**
- Click **+** (top right) → **New repository**
- Name: `claude-certification-hub` · Visibility: **Public** on the free plan (see "Keeping the source private" below for alternatives)
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

## Keeping the source private

The site itself is public (that is its purpose), but the source repository does not have to be. Nothing on the site links to this repository: there is no "edit this page" link, lab code is offered as a zip download, and corrections go through the About page.

Things to know:

* **Hosting.** GitHub Pages serves a site from a *private* repository only on a paid plan (GitHub Pro or higher). On the free plan the repository must be public, or the site goes offline. Options:
    1. **GitHub Pro**: make this repository private and change nothing else. Same address, same workflow.
    2. **Free, different host**: connect the private repository to a static host that supports private repositories on its free tier (for example Cloudflare Pages or Netlify). Build command `pip install -r requirements.txt && mkdocs build`, output folder `site`. The address changes, so update `site_url` in `mkdocs.yml`.
    3. **Free, two repositories**: keep the source here (private) and push only the built `site/` folder to a second, public repository that Pages serves.
* **What stays visible.** Whatever the site serves is public by nature: every page, and the question data file with its answers. A private repository hides the *source* (the authoring scripts, drafts and history), not the published content.
* **Lab code zip.** After changing anything in `labs-code/`, rebuild the download:
  `zip -r docs/assets/downloads/labs-code.zip labs-code -x "*/__pycache__/*"`
* **History.** If this repository was public before, earlier commits may already have been copied or indexed. Check that no secret was ever committed (none should have been).

## Learner comments

The **About → Learner Stories** page has an on-page comment box powered by [giscus](https://giscus.app). giscus needs a **public** repository to store comments, so use a small separate one that contains nothing but discussions.

**One-time setup**

1. Create a new **public** repository named `claude-certification-hub-comments` (tick "Add a README").
2. In that repository: **Settings → General → Features**: tick **Discussions**.
3. Open its **Discussions** tab → pencil icon next to *Categories* → **New category**: name `Learner Stories`, format **Announcement** (only you and giscus can start threads; anyone can comment).
4. Install the giscus app on that repository only: https://github.com/apps/giscus
5. On https://giscus.app enter `pabhinaw/claude-certification-hub-comments`, choose the `Learner Stories` category, and copy `data-repo-id` and `data-category-id` from the generated snippet.
6. Paste both into `mkdocs.yml` under `extra: comments:` (`repo_id` and `category_id`), then commit and push.
7. Optional: add a file `giscus.json` to the comments repository containing `{"origins": ["https://pabhinaw.github.io"]}` so that only your site can embed the comments.

**Moderating**

* Every comment appears in the Discussions tab. Use the `…` menu on a comment to **hide** or **delete** it.
* Remove anything containing exam questions, exam content, score details or personal contact data.
* Watch the repo's Discussions (Watch → Custom → Discussions) to get an email for each new comment.

**Featuring a comment on the home page (optional)**

Copy the comment **word for word** into the `testimonials:` list in `mkdocs.yml`, after the commenter agrees. Never write or "improve" a testimonial yourself.

## Privacy rule for this repo

Never commit score reports, candidate IDs, registration numbers, API keys or real customer data.
The `.gitignore` already blocks `*scorereport*.pdf`, `.env` and a `private/` folder.

## License

Content: CC BY 4.0. Code samples: MIT.
