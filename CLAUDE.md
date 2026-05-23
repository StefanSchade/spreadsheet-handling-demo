# CLAUDE.md - Entry Point for AI Work in the Demo Repo

This file is intentionally brief.

## Canonical guidance lives in the core repository

The authoritative AI agent instructions, FTR backlog, developer guide,
architecture documentation, and release runbook live in the
`spreadsheet-handling` core repository -- typically a sibling on disk:

* `../spreadsheet-handling/` (upstream default clone name), or
* `../core/` (some workspaces use a shorter local clone name)

Load and follow:

* the core `CLAUDE.md` and `AGENT.md` entry files
* `docs/ai_info/_ai_info.adoc` (canonical AI / repo-committing guidance)
* `docs/ai_info/repository_boundaries.adoc`
  (responsibilities of core / demo / pages; central-governance policy)
* the active FTR or review note for the current task
* relevant chapters of `docs/developer_guide/`

If the core repository is not present on disk, work from the fallback rules
below for demo-local edits only; do not invent parallel architecture or
policy here.

## What this repo owns

* demo pipelines, sample data, walkthrough source (AsciiDoc), launchers,
  and the Reveal.js render scaffold
* demo-focused tests and CI workflow
* the demo README -- the primary user entry point linking to the published
  Pages site

## What this repo does NOT own

* the FTR backlog -- centralized in core under `docs/backlog/`. New tickets
  belong there even if the implementation work lands here.
* review notes for FTRs -- authored during the work, but once the FTR closes
  they live next to the closed FTR in core
  `docs/cold_storage/backlog/ftrs_done/`.
* AI agent instructions, developer guide, architecture documentation --
  centralized in core. Do not grow a parallel policy here.
* release orchestration and version semantics -- core owns this; sibling
  workflows mirror the patterns documented in core's ch09 release
  management.

## Fallback operating rules (use when core is unavailable)

* Treat this repository as a demo and integration surface, not the primary
  location for deep core-library development.
* Prefer adapting demo pipelines, sample data, walkthroughs, and focused
  demo tests to the current use case.
* If a task clearly belongs in the core library or its architecture docs,
  stop and switch to the core repository instead of rebuilding logic here.
* Stay inside the workspace repositories and avoid destructive or
  irreversible actions without explicit approval.
* Treat `.venv/`, `target/`, `tmp/`, generated workbooks, and similar local
  state as non-source unless the task explicitly includes them.
* Use Conventional Commits with informative subjects; if the change maps to
  a concrete FTR, include the FTR ID as the Conventional Commit scope.

For repo-committing agent behavior, see `AGENT.md`.
