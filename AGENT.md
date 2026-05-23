# AGENT.md - Entry Point for Repo-Committing Agents in the Demo Repo

This file is intentionally brief.

## Canonical guidance lives in the core repository

The authoritative repo-committing rules live in the `spreadsheet-handling`
core repository -- typically a sibling on disk at:

* `../spreadsheet-handling/` (upstream default clone name), or
* `../core/` (some workspaces use a shorter local clone name)

Treat the core repository's `CLAUDE.md`, `AGENT.md`, and `docs/ai_info/`
set as the source of truth. If the core repository is absent, operate with
the fallback rules in this file for demo-local edits only.

## Central-governance reminder

The FTR backlog, AI agent instructions, developer guide, architecture
documentation, and release runbook are centralized in the core repository.

* New tickets and review notes for follow-up work belong in core's
  `docs/backlog/` (active) or `docs/cold_storage/backlog/ftrs_done/`
  (closed), not in a parallel backlog here.
* Do not grow a parallel architecture, AI policy, or release policy in
  this repository.

If a task appears to require core architecture work, stop here and continue
in the core repository, leaving only the demo-facing integration slice in
this one.

Review discipline: if a task is a review or produces findings / validation
work, create or update the matching `*_review.adoc` artifact in the repo's
review location, commit that review artifact separately from any follow-up
fix, summarize the validation commands you ran, and record the disposition
plus any residual risks.

## Minimal operating rules for this demo repository

* Optimize for demo usefulness: pipelines, walkthroughs, reference
  commands, sample data, and demo-focused tests are the normal center of
  gravity here.
* Prefer changing local configuration and documentation over adding
  framework layers or deep abstractions.
* Avoid destructive history edits, release publication, CI/CD changes, or
  deleting potentially in-progress user work without explicit approval.
* Treat `tmp/`, `target/`, `.venv/`, generated outputs, and local scratch
  files as non-source unless the task explicitly includes them.
* Use Conventional Commits with informative English subjects and a short
  body for non-trivial changes.
* When applying an architectural / code review for an FTR implementation,
  record the review under
  `docs/backlog/reviews/FTR-<ID>_review.adoc` while the work is in
  progress, then move the review next to the FTR in core
  `docs/cold_storage/backlog/ftrs_done/` once the FTR closes. Trivial edits
  do not need a review note. See core
  `docs/ai_info/git_and_workflow.adoc` for the canonical format.

## Shared helpers (`tools/`) vs core-local automation (`scripts/`)

The core repository distinguishes:

* `core/tools/` -- shared helpers intended to be copied into sibling repos
  (e.g. `repo_snapshot.sh`). This repo's `Makefile` `snapshot` target is
  the canonical example: it expects `tools/repo_snapshot.sh` and instructs
  the user to copy it from the core repo if absent.
* `core/scripts/` -- repo-local automation tied to core's own build / dev
  loop. Do not copy from there.

See `docs/ai_info/conventions.adoc` ("Helper script placement") in the core
repository for the full rule.
