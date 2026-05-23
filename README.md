# spreadsheet-handling-demo

Consumer demo repository for `spreadsheet-handling`. The maintained demo
path is the **product business slice**: it shows the core idea in one
small flow &mdash; a normalized JSON model becomes a business-readable
workbook, you edit a cell, and the workbook reimports without losing
identity.

For the current beta cycle this demo stays intentionally `xlsx`-first.
ODS is covered in the core repository but is not yet externalized
through the demo's maintained run path.

## First-hour tutorial: the product business slice

Eight concrete steps. You should finish them in well under an hour;
budget the time for *reading* the generated workbook, not for setup.

### 1. Clone the demo

```bash
git clone https://github.com/StefanSchade/spreadsheet-handling-demo.git
cd spreadsheet-handling-demo
```

### 2. Set up the local environment

```bash
make setup
make setup-lib-local      # bind the local core checkout (sibling on disk)
```

If you do not have a local core checkout, replace the second command with
`make setup-lib-pypi` to install the pinned PyPI release instead.

### 3. Run the product business slice forward pipeline

```bash
make run PIPELINE=./pipelines/demo_product_business_slice.yaml
```

Output: `./tmp/product_business_slice.xlsx`.

### 4. Open the generated workbook

Open `./tmp/product_business_slice.xlsx` in Excel or LibreOffice Calc.
The workbook has three sheets: `product`, `product_manager`, and `branch`.

### 5. Inspect helper columns, validations, and styling

Look at the `product` sheet and notice:

- a derived helper column (e.g. `_product_manager_name`) sitting next to
  the foreign-key column &mdash; this is added by the
  `add_fk_helpers` pipeline step from the related `product_manager` table;
- list validations on `status` (`active` / `pilot` / `retired`),
  `category` (`entry` / `standard` / `premium`), and `country`
  (`DE` / `CH` / `AT`) &mdash; try entering an out-of-list value, the cell
  rejects it;
- per-sheet header fills (`product` green, `product_manager` blue,
  `branch` orange) and the `branch` sheet keeping its header unfrozen
  while the other two freeze theirs &mdash; per-sheet overrides come from
  `data/product_business_slice/overrides.yaml`.

The idea here: normalized FK relations plus helper enrichment produce a
readable workbook without denormalizing the source data.

### 6. Edit a single business value

In the workbook, change one cell &mdash; for example switch a product's
`status` from `active` to `pilot`, or rename a `product_manager` &mdash;
and save the file. Leave the helper column alone; it is derived.

### 7. Re-import the workbook

```bash
make run PIPELINE=./pipelines/demo_workbook_reimport.yaml \
  IN_PATH=./tmp/product_business_slice.xlsx \
  OUT_PATH=./tmp/product_business_slice_reimported
```

Output: `./tmp/product_business_slice_reimported/*.json`.

### 8. Verify the canonical JSON remains clean

Compare the reimported JSON against the original source data:

```bash
diff -ru --exclude=overrides.yaml --exclude=_meta.yaml \
  ./data/product_business_slice ./tmp/product_business_slice_reimported \
  | head -40
```

You should see exactly the field you edited in step 6. The excluded files
are workbook rendering/configuration sidecars, not business payload. The
helper column does not leak into the canonical JSON, sheet ordering is
preserved, and the FK identifiers are untouched. That edit-safe
round-trip is the property the slice is built to demonstrate.

## Where to go next

- **View this slice as a short visual walkthrough** &mdash;
  <https://stefanschade.github.io/spreadsheet-handling-pages/latest/demo/slides/product_business_slice.html>
  is the Reveal.js deck for the same flow you just ran.
- **Read the user guide (latest release)** &mdash;
  <https://stefanschade.github.io/spreadsheet-handling-pages/latest/core/user-guide/>.
- **Browse documentation by version** &mdash;
  <https://stefanschade.github.io/spreadsheet-handling-pages/>
  is the per-release archive portal; it carries the latest-release
  banner and a list of every published version.

The full narrative for this slice is at
`docs/walkthroughs/product_business_slice.adoc`. More curated journeys
are indexed in `docs/index.adoc`; they are not part of the maintained
first-hour tutorial path.

## Verify

```bash
.venv/bin/pytest -q
```

Smoke/integration checks run the curated journeys against the bound core
checkout (use `make setup-lib-local` to bind the local library).
