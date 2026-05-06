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

## Primary demo flows

Generate the curated product workbook:

```bash
make run PIPELINE=./pipelines/demo_product_business_slice.yaml
```

Read a workbook back to JSON through the same generic runner:

```bash
make run PIPELINE=./pipelines/demo_workbook_reimport.yaml \
  IN_PATH=./tmp/product_business_slice.xlsx \
  OUT_PATH=./tmp/product_business_slice_reimported
```

Run the demo smoke tests:

```bash
.venv/bin/pytest -q
```

## Documentation

Start with `docs/index.adoc` for the user-facing walkthroughs and capability
overview.

Maintainer coordination lives under `docs/internal/`. New users can ignore that
directory; it exists only to keep demo integration work aligned with the main
library.

## Phase 4 local demo flows

These flows intentionally use the local sibling checkout after
`make setup-lib-local`:

```bash
make run PIPELINE=./pipelines/demo_phase4_compact_multiaxis_expand.yaml
make run PIPELINE=./pipelines/demo_phase4_compact_multiaxis_roundtrip.yaml
make run PIPELINE=./pipelines/demo_phase4_compact_multiaxis_workbook.yaml
make run PIPELINE=./pipelines/demo_phase4_compact_multiaxis_workbook.yaml \
  OUT_KIND=ods OUT_PATH=./tmp/phase4_compact_multiaxis.ods
```
