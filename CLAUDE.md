# CLAUDE.md - Entry Point for AI Work in the Demo Repo

This file is intentionally brief.

While this repository is still in beta, the canonical development guidance
lives in the neighboring core repository when it is available:

* `../spreadsheet-handling/CLAUDE.md`
* `../spreadsheet-handling/AGENT.md`
* `../spreadsheet-handling/docs/internal_guide/ai_policy/`
* `../spreadsheet-handling/docs/internal_guide/dev_man/`

If that neighboring repository is not present, use the fallback rules below.

Practical summary:

* Treat this repository as a demo and integration surface, not the primary
  location for deep core-library development.
* Prefer adapting demo pipelines, sample data, walkthroughs, and focused demo
  tests to the current use case.
* If a task clearly belongs in the core library or its architecture docs,
  switch to `../spreadsheet-handling` instead of rebuilding that logic here.
* Stay inside the workspace repositories and avoid destructive or irreversible
  actions without explicit approval.
* Treat `.venv/`, `target/`, `tmp/`, generated workbooks, and similar local
  state as non-source unless the task explicitly includes them.
* Use Conventional Commits with informative subjects; if the change maps to a
  concrete feature ticket, include that scope.

For repo-committing agent behavior, see `AGENT.md`.
