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
