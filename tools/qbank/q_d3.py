from qlib import Q

# ======================= D3 · Claude Code Configuration & Workflows =======================

# --- Choosing the mechanism ---
Q("D3", "S2", "Mechanism choice", """
The team convention "use pnpm, not npm, for all commands" should apply across the whole repo for everyone. Where does it belong?""",
  "The project CLAUDE.md, committed to the repo",
  "Team-wide conventions are guidance and belong in project memory.",
  [("~/.claude/CLAUDE.md on each laptop", "Personal scope, not shared."),
   ("A PreToolUse hook that rewrites npm to pnpm", "Possible, but heavy-handed for a convention; CLAUDE.md is the right first home."),
   ("A custom slash command", "Commands are invoked on demand, not applied automatically.")], level=1)

Q("D3", "S2", "Mechanism choice", """
Guidance about React component patterns should apply only when Claude works in src/components/. What is the best mechanism?""",
  "A rule file in .claude/rules/ with a paths glob such as src/components/**",
  "Path-scoped rules load only when relevant.",
  [("The root CLAUDE.md", "Loads in every session, wasting context elsewhere."),
   ("A Stop hook", "Hooks enforce actions; they don't provide coding guidance."),
   ("settings.local.json", "That holds settings, not guidance.")])

Q("D3", "S2", "Mechanism choice", """
Claude must never read .env files in the repo, under any circumstances. What is the right mechanism?""",
  "A permissions deny rule for reading .env files in project settings (optionally backed by a PreToolUse hook)",
  "Must-never rules about tools and paths belong in enforced permissions.",
  [("A line in CLAUDE.md saying not to read .env", "Advisory only."),
   ("A rule file scoped to .env", "Rules are guidance."),
   ("A slash command that reminds Claude about secrets", "Relies on someone invoking it.")])

Q("D3", "S4", "Mechanism choice", """
A packaged capability (instructions plus helper scripts) should load automatically whenever a task involves generating release notes. Which mechanism fits?""",
  "A Skill whose description says when it applies",
  "Skills are loaded on demand when the task matches their description, and can bundle resources.",
  [("A custom slash command", "Requires a person to invoke it."),
   ("CLAUDE.md", "Always loaded, even when irrelevant."),
   ("A PostToolUse hook", "Hooks run code; they don't provide task expertise.")])

Q("D3", "S2", "Mechanism choice", """
Every Python file Claude edits must pass the ruff linter, with no exceptions. Where does this belong?""",
  "A PostToolUse hook matching Edit and Write that runs ruff and exits 2 with the errors if it fails",
  "No exceptions means deterministic enforcement.",
  [("CLAUDE.md", "Claude may forget."),
   ("A /format command", "Requires a person to remember."),
   ("A Skill about formatting", "Guidance, not enforcement.")], level=1)

Q("D3", "S4", "Mechanism choice", """
A developer prefers very terse answers in every project, but teammates don't. Where should this preference live?""",
  "~/.claude/CLAUDE.md (user-level memory)",
  "Personal preferences belong at user scope.",
  [("The project CLAUDE.md", "Imposes it on the whole team."),
   (".claude/settings.json", "Shared settings file, and not for style guidance."),
   ("A PreToolUse hook", "Hooks aren't for response style.")])

# --- Advice vs enforcement ---
Q("D3", "S2", "Advice vs enforcement", """
Which CLAUDE.md line should be moved to settings or hooks?""",
  "'Never run git push --force.'",
  "A must-never rule about a command needs enforcement (permission deny or hook).",
  [("'Prefer small, pure functions.'", "Style guidance belongs in CLAUDE.md."),
   ("'Architecture overview: see docs/architecture.md.'", "Context, fine in CLAUDE.md."),
   ("'Tests use Vitest.'", "Factual context, fine in CLAUDE.md.")])

Q("D3", "S2", "Advice vs enforcement", """
A team writes "ALWAYS run tests before finishing" in CLAUDE.md, but Claude sometimes doesn't. Most reliable fix?""",
  "A Stop hook (or PostToolUse hook) that runs the tests and blocks finishing until they pass",
  "Hooks enforce what memory can only suggest.",
  [("Repeat the instruction three times", "Emphasis isn't enforcement."),
   ("Move the instruction to the top of CLAUDE.md", "Placement doesn't guarantee behaviour."),
   ("Create a /test command", "Still relies on someone remembering.")])

Q("D3", "S2", "Advice vs enforcement", """
Which item is appropriate to keep in CLAUDE.md rather than enforcing?""",
  "'Prefer composition over inheritance in UI components.'",
  "Judgement-based guidance belongs in memory.",
  [("'Never modify files in /migrations.'", "Must-never: enforce with permissions."),
   ("'Block any command containing rm -rf.'", "Must-never: enforce with permissions or a hook."),
   ("'Always format with Prettier after editing.'", "Always: enforce with a hook.")])

Q("D3", "S5", "Advice vs enforcement", """
In CI, Claude must not be able to push to any branch. Which approach is most reliable?""",
  "Deny the relevant git push commands in the CI settings' permissions (and use credentials without push rights)",
  "Enforce at the tool level and the credential level.",
  [("Tell Claude in the CI prompt not to push", "Advisory only."),
   ("Use plan mode in CI", "Plan mode isn't the guard; permissions are."),
   ("Lower max turns", "Doesn't prevent a push.")])

# --- CLAUDE.md & context ---
Q("D3", "S2", "Context", """
For one task, Claude needs to see the exact contents of src/billing/rates.ts. What's the best way to provide it?""",
  "Reference it directly in the prompt with @src/billing/rates.ts",
  "@ references give precise, current, task-specific context.",
  [("Paste it into the project CLAUDE.md", "Loads every session, and goes stale."),
   ("Describe the file from memory", "Imprecise."),
   ("Create a rule file containing the code", "Rules are guidance, not file copies.")])

Q("D3", "S2", "Context", """
Build and test commands are needed in nearly every session by everyone on the team. Where should they go?""",
  "The project CLAUDE.md",
  "Cross-session, team-wide context belongs in project memory.",
  [("Inline in each prompt", "Repetitive and error-prone."),
   ("An @ reference in each prompt", "Better suited to task-specific files."),
   ("~/.claude/CLAUDE.md", "Personal scope, not shared.")], level=1)

Q("D3", "S2", "Context", """
The project CLAUDE.md has grown to thousands of lines covering every subsystem. What is the best restructuring?""",
  "Keep CLAUDE.md short; move topic details into imported files or path-scoped rules that load when relevant",
  "Modular memory saves context and stays maintainable.",
  [("Leave it, because more context is always better", "Irrelevant context dilutes attention and costs tokens."),
   ("Delete it and rely on prompts", "Loses shared conventions."),
   ("Split it into several CLAUDE.md files in the root", "Doesn't make loading conditional.")])

Q("D3", "S2", "Context", """
A monorepo has packages/api and packages/web with different conventions. How can each package get its own guidance?""",
  "Use a CLAUDE.md in each package directory (or path-scoped rules), which applies when Claude works there",
  "Sub-directory memory and path rules give targeted guidance.",
  [("One root CLAUDE.md with both sets of conventions", "Both sets load everywhere and can conflict."),
   ("Separate user-level CLAUDE.md files", "User scope isn't per package."),
   ("Settings files per package", "Settings don't carry coding guidance.")])

Q("D3", "S4", "Context", """
A one-off detail ("the client wants the export in CSV this time") applies only to the current request. Where should it go?""",
  "Inline in the prompt",
  "One-off details don't belong in persistent memory.",
  [("The project CLAUDE.md", "Would persist and mislead future sessions."),
   ("A rule file", "Rules are for recurring guidance."),
   ("User settings", "Settings don't hold task details.")], level=1)

# --- Rules ---
Q("D3", "S2", "Rules", """
What does a paths glob in a .claude/rules/ file's frontmatter do?""",
  "Loads the rule only when Claude works on files matching the pattern",
  "Path-scoped rules keep guidance precise and context lean.",
  [("Blocks Claude from editing those files", "That's a permission rule."),
   ("Runs a script whenever matching files change", "That's a hook."),
   ("Copies the rule into every CLAUDE.md", "No such behaviour.")], level=1)

Q("D3", "S2", "Rules", """
Terraform guidance should apply only to files under infra/. Which configuration is correct?""",
  "A .claude/rules/terraform.md file with paths: [\"infra/**/*.tf\"] in its frontmatter",
  "That scopes the rule exactly.",
  [("A Terraform section in ~/.claude/CLAUDE.md", "User scope, and not path-limited."),
   ("A PreToolUse hook on infra/", "Hooks enforce actions; they don't give guidance."),
   ("A permissions allow rule for infra/", "Permissions don't carry guidance.")])

# --- Commands & skills ---
Q("D3", "S4", "Commands", """
A /review-pr command should be available to everyone who clones the repository. Where should it be created?""",
  ".claude/commands/review-pr.md, committed to the repo",
  "Project commands are shared through the repo.",
  [("~/.claude/commands/review-pr.md", "Personal only."),
   (".mcp.json", "MCP configuration, not commands."),
   ("The project CLAUDE.md", "Memory, not a command.")], level=1)


Q("D3", "S4", "Commands", """
How does a custom slash command receive the text a user types after it, e.g. /review-pr security?""",
  "Through the $ARGUMENTS placeholder in the command file",
  "$ARGUMENTS is replaced with the user's input.",
  [("Through an environment variable named CLAUDE_ARGS", "Not how commands receive arguments."),
   ("It can't; commands take no input", "Commands accept arguments."),
   ("Through a hook's stdin", "Hooks receive event JSON, not command arguments.")])

Q("D3", "S4", "Skills", """
What mainly decides when Claude loads a Skill automatically?""",
  "The Skill's description in its SKILL.md frontmatter",
  "Like tool descriptions, the skill description drives selection.",
  [("The file size of the skill folder", "Irrelevant."),
   ("The alphabetical order of skills", "Irrelevant."),
   ("Whether the user types the skill's name", "Skills can load without being named.")])

Q("D3", "S4", "Skills", """
When is a Skill a better choice than a slash command?""",
  "When Claude should pick up the capability automatically when a task matches, and it bundles scripts or reference files",
  "Skills are model-invoked packages; commands are person-invoked prompts.",
  [("When the workflow must only run when a person explicitly asks", "That's a command."),
   ("When the rule must be enforced every time", "That's a hook or permission."),
   ("When the guidance is a short team convention", "That fits CLAUDE.md.")])

# --- Settings & permissions ---
Q("D3", "S4", "Settings", """
A developer needs a personal sandbox URL setting for one project that must not be committed. Which file?""",
  ".claude/settings.local.json",
  "Local project settings are personal and git-ignored.",
  [(".claude/settings.json", "Shared and committed."),
   ("~/.claude/settings.json", "Applies to all projects."),
   ("CLAUDE.md", "Memory, not settings, and usually committed.")])

Q("D3", "S4", "Settings", """
A shared project settings file allows a command, but an enterprise managed policy denies it. What happens?""",
  "The managed policy wins and the command is denied",
  "Managed policy has the highest precedence and can't be overridden.",
  [("The project setting wins because it's more specific", "Managed policy overrides it."),
   ("The user is asked to choose each time", "Precedence decides; the user doesn't choose."),
   ("Both apply, so the command runs with a warning", "Deny wins.")])

Q("D3", "S4", "Settings", """
A settings file has both an allow rule and a deny rule that match the same command. What is the outcome?""",
  "The deny rule wins",
  "Deny takes priority over allow.",
  [("The allow rule wins because it's listed first", "Order doesn't override deny."),
   ("The most recently edited file wins", "Not how evaluation works."),
   ("Claude chooses based on context", "Permissions are evaluated deterministically.")])

# --- Plan mode ---
Q("D3", "S2", "Plan mode", """
Which task most warrants plan mode before any edits?""",
  "A database schema change that affects three services owned by different teams",
  "Broad, high-risk, review-needed changes benefit from planning first.",
  [("Fixing a typo in a docstring", "Trivial and easily reverted."),
   ("Renaming a local variable", "Small and clearly scoped."),
   ("Adding a missing import", "Direct execution is fine.")], level=1)

Q("D3", "S2", "Plan mode", """
What does plan mode do?""",
  "Lets Claude investigate and propose a plan without modifying files",
  "It separates analysis from execution.",
  [("Runs all edits in a sandbox branch automatically", "It doesn't edit at all."),
   ("Disables all tools, including Read", "Read-only investigation is allowed."),
   ("Forces Claude to use a larger model", "Unrelated to model choice.")], level=1)

Q("D3", "S2", "Plan mode", """
A change touches a public API used by other teams and is hard to reverse. What workflow is best?""",
  "Use plan mode, review the plan with stakeholders, then execute",
  "Irreversible, cross-team changes need review before implementation.",
  [("Execute directly, then open a PR for review", "Review after implementation is costly for irreversible changes."),
   ("Execute directly in small commits without review", "Ignores stakeholder impact."),
   ("Ask Claude to be careful", "Not a process.")])

# --- Hooks for quality ---
Q("D3", "S2", "Quality hooks", """
A PostToolUse lint hook exits with code 2 and prints lint errors to stderr. What happens?""",
  "The edit has already happened; the errors are fed back to Claude so it can fix them",
  "For PostToolUse, exit 2 gives blocking feedback; it can't undo the completed edit.",
  [("The edit is rolled back automatically", "PostToolUse runs after the action."),
   ("The session terminates", "Exit 2 doesn't end the session."),
   ("Nothing; exit 2 is ignored for PostToolUse", "The stderr feedback is shown to Claude.")])

Q("D3", "S2", "Quality hooks", """
A team's lint hook exits with code 1 on errors, yet Claude never seems to react to lint failures. Why?""",
  "Exit code 1 is a non-blocking error; the hook must exit 2 to feed stderr back to Claude as a blocking error",
  "Only exit 2 blocks and feeds stderr to Claude.",
  [("Hooks only work with Python scripts", "Any command works."),
   ("Lint output must be written to stdout", "For exit 2, stderr is what's fed back."),
   ("PostToolUse hooks can't see file paths", "The tool input, including the file path, is provided on stdin.")])

# --- Iterative refinement ---
Q("D3", "S2", "Iterative refinement", """
Claude's date-parsing function still fails after two attempts with feedback "still wrong". What is the most effective next message?""",
  "Concrete failing input/output pairs, e.g. input '5/3/2026' expected '2026-03-05', got '2026-05-03'",
  "Specific, testable feedback converges fastest.",
  [("'Please try harder this time.'", "Not actionable."),
   ("'Rewrite it from scratch.'", "Loses progress without explaining the failure."),
   ("'Use a different library.'", "Guessing at the cause rather than describing the failure.")])

Q("D3", "S2", "Iterative refinement", """
Three reported issues interact: fixing the parser changes the validator's input, which affects the formatter. How should feedback be given?""",
  "Batch them into one message so they're evaluated and fixed together",
  "Interacting issues should be handled together to avoid fix-break cycles.",
  [("One at a time, waiting for each fix", "Each fix may break the others."),
   ("Only report the most severe and ignore the rest", "Leaves known issues."),
   ("Report them in three separate sessions", "Loses the connection between them.")])

Q("D3", "S2", "Iterative refinement", """
Five unrelated issues are found in different modules. What is a sensible approach?""",
  "Handle them sequentially, verifying each fix",
  "Independent issues can be addressed one by one with clear verification.",
  [("Always batch everything into one message", "Batching is for interacting issues; independent ones are clearer in sequence."),
   ("Ignore minor ones", "Leaves known defects."),
   ("Ask Claude to find more issues first", "Delays fixing known issues.")])

Q("D3", "S4", "Iterative refinement", """
Requirements for a feature are vague. What technique helps before Claude writes code?""",
  "The interview pattern: ask Claude to question you about requirements first",
  "Clarifying up front prevents rework.",
  [("Let Claude guess and iterate", "Wastes cycles."),
   ("Use plan mode only", "Helps structure the work but doesn't fill requirement gaps."),
   ("Set a lower temperature", "Unrelated to missing requirements.")])

# --- Exploration ---
Q("D3", "S4", "Exploration", """
A developer asks Claude to understand an unfamiliar 3,000-file codebase. Which approach is most context-efficient?""",
  "Start broad (structure, README), narrow with Grep and Glob, read only relevant files, and record findings in a notes file",
  "Incremental exploration with external notes manages context limits.",
  [("Read every file alphabetically", "Exhausts context quickly."),
   ("Ask Claude to summarise the repo from its training data", "It hasn't seen your private code."),
   ("Read only the largest files", "Size isn't relevance.")])

Q("D3", "S4", "Exploration", """
Broad exploration is filling the main session's context. What helps most?""",
  "Delegate the exploration to a subagent that returns a concise summary",
  "Subagent isolation keeps the main context focused.",
  [("Disable Grep to reduce output", "Removes a precise tool."),
   ("Start a new session every few minutes", "Loses continuity."),
   ("Increase max_tokens", "Output length isn't the issue.")])

# --- CI/CD ---
Q("D3", "S5", "CI/CD", """
Claude Code must run in a CI job without waiting for keyboard input. Which flag is essential?""",
  "-p (print / non-interactive mode)",
  "-p runs a single prompt non-interactively.",
  [("--continue", "Resumes a session; doesn't make it non-interactive."),
   ("--verbose", "Only changes logging."),
   ("Shift+Tab", "A keyboard shortcut, not a CLI flag.")], level=1)

Q("D3", "S5", "CI/CD", """
A pipeline step must parse Claude Code's review findings automatically. What should the invocation include?""",
  "--output-format json (with a defined output structure in the prompt or schema)",
  "Machine-readable output is needed for parsing.",
  [("A request to 'format nicely' in the prompt", "Not reliably parseable."),
   ("--resume", "Unrelated to output format."),
   ("Plan mode", "Doesn't change output format.")])

Q("D3", "S5", "CI/CD", """
In CI, Claude generates code and then reviews it. Which setup gives the most trustworthy review?""",
  "Run the review in a separate, fresh session (independent instance) with explicit review criteria",
  "Independent review avoids self-confirmation bias.",
  [("Ask the generating session to double-check its work", "Same-context self-review tends to agree with itself."),
   ("Skip review because the code compiles", "Compiling isn't correctness."),
   ("Use the Batch API for the review", "Batch is about cost and latency, not independence.")])

Q("D3", "S5", "CI/CD", """
A PR review job reviews 40 changed files and misses issues between files. Improvement?""",
  "Per-file review passes plus a cross-file integration pass",
  "Catches local and interface-level issues.",
  [("One pass over all files concatenated", "Long context reduces attention to detail."),
   ("Review only the five largest files", "Arbitrary coverage."),
   ("Increase temperature for creativity", "Unrelated.")])

# --- Extra CI/CD scenario coverage ---
Q("D3", "S5", "CI/CD", """
A nightly CI job asks Claude Code to triage flaky tests and open a summary. The job sometimes runs far longer than expected. Which control helps most?""",
  "Bound the run (for example a turn or time limit in the job) and restrict allowed tools to what triage needs",
  "Headless runs need explicit limits and least-privilege tools.",
  [("Run it interactively so someone can stop it", "Defeats automation."),
   ("Remove the job's timeout so it can finish", "Makes runaway runs worse."),
   ("Use plan mode so nothing runs", "Then it can't run the tests it needs.")])

Q("D3", "S5", "CI/CD", """
A CI review job needs the team's coding conventions. What is the best way to provide them?""",
  "Commit them to the project CLAUDE.md (and rules), which Claude Code loads in the CI checkout",
  "Project memory travels with the repo into CI.",
  [("Paste them into the CI YAML as a long string", "Duplicates and drifts from the source of truth."),
   ("Rely on the reviewer's ~/.claude/CLAUDE.md", "User files don't exist on CI runners."),
   ("Skip conventions in CI", "Reviews would miss team standards.")])
