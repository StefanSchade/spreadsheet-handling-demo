# spreadsheet-handling-demo

Consumer demo repo for `spreadsheet-handling`.

## Current stance

The maintained demo path goes through `sheets-run` plus checked-in YAML
config/pipeline files.

For the upcoming beta cycle this demo stays intentionally `xlsx`-first. ODS is
covered in the core repository, but is not yet externalized through the demo's
maintained run path.

## Local setup

```bash
make setup
make setup-lib-local
```

## Curated journey: Product Business Slice

This is the primary maintained journey. It shows the core idea in one small
flow: a normalized JSON model becomes a business-readable workbook and survives
an edit-and-reimport roundtrip without losing identity.

**1. Generate the workbook**

```bash
make run PIPELINE=./pipelines/demo_product_business_slice.yaml
```

* Output: `./tmp/product_business_slice.xlsx`
* Observe: FK helper columns (e.g. `_product_manager_name`) next to their FK
  column, list validations on `status` / `category` / `country`, and per-sheet
  header styling.
* Idea: normalized FK relations + helper enrichment produce a readable
  workbook without denormalizing the source data.

**2. Edit, then reimport**

Change a cell in the workbook (e.g. a `status`), then read it back:

```bash
make run PIPELINE=./pipelines/demo_workbook_reimport.yaml \
  IN_PATH=./tmp/product_business_slice.xlsx \
  OUT_PATH=./tmp/product_business_slice_reimported
```

* Output: `./tmp/product_business_slice_reimported/*.json`
* Observe: your edited value is preserved; derived helper columns do not
  corrupt the canonical JSON.
* Idea: the JSON ↔ XLSX roundtrip is deterministic and edit-safe.

Full narrative: `docs/walkthroughs/product_business_slice.adoc`. More curated
journeys are indexed in `docs/index.adoc`.

## Verify

```bash
.venv/bin/pytest -q
```

Smoke/integration checks run the curated journeys against the bound core
checkout (use `make setup-lib-local` to bind the local library).

## Published documentation

Released versions of `spreadsheet-handling` publish their documentation to
GitHub Pages:

* Site root: <https://stefanschade.github.io/spreadsheet-handling-pages/>
* Core user guide: `latest/core/user-guide/` under that site
* Release notes: `latest/core/release-notes/`
* Demo walkthroughs as Reveal.js slides: `latest/demo/slides/`
  (or the per-version path `versions/<tag>/demo/slides/`)

The PyPI project page links back to the same site, so installation from PyPI
and reading the matching walkthroughs use the same documentation set.
