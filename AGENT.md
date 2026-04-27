# AGENT.md - Entry Point for Repo-Committing Agents in the Demo Repo

This file is intentionally brief.

Primary guidance:

* If `../spreadsheet-handling` exists, treat its `CLAUDE.md`, `AGENT.md`, and
  internal guide as the canonical source of truth.
* If that neighboring repository is absent, operate with the fallback rules in
  this file.

Minimal operating rules for this demo repository:

* Optimize for demo usefulness: pipelines, walkthroughs, reference commands,
  sample data, and demo-focused tests are the normal center of gravity here.
* Do not grow a parallel architecture policy in this repo when the same issue
  belongs to the core project.
* Prefer changing local configuration and documentation over adding framework
  layers or deep abstractions.
* Avoid destructive history edits, release publication, CI/CD changes, or
  deleting potentially in-progress user work without explicit approval.
* Treat `tmp/`, `build/`, `.venv/`, generated outputs, and local scratch files
  as non-source unless the task explicitly includes them.
* Use Conventional Commits with informative English subjects and a short body
  for non-trivial changes.

If the task appears to require core architecture work, continue in
`../spreadsheet-handling` and leave only the demo-facing integration slice
here.
