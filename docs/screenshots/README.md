# demo/docs/screenshots

Supplementary visual aids for the demo's maintained walkthroughs.

## Scope

Screenshots are a *supplementary* aid to the demo's curated journeys.
The primary live visual artifact is the Reveal.js deck published under
`/latest/demo/slides/` on the Pages site (rendered from the
corresponding source in `docs/walkthroughs/`). This directory adds small
static images for things that read better as a frame of a workbook than
as prose &mdash; helper columns next to FKs, list-validation dropdowns,
distinct per-sheet styling, the visible delta of a single edit.

Coverage is intentionally narrow: only the maintained **product business
slice** journey is covered. Other slices (`acme_*`, Storyforge,
multi-header, named-ranges) are not in scope.

## Layout

```
docs/screenshots/
  README.md                                   <- this file
  product_business_slice/
    workbook-overview.png                     <- captured
    helper-columns.png                        <- captured
    list-validations-status.png               <- captured
    list-validations-category.png             <- captured
    edit-status-after.png                     <- captured
```

Naming convention: kebab-case, descriptive, no version suffix in the
filename. The capture metadata (release tag, date) lives in the *Capture
log* section below.

## Current capture state

| Image | Status |
|---|---|
| `product_business_slice/workbook-overview.png` | captured (198 KiB, 1274&times;924, RGBA) |
| `product_business_slice/helper-columns.png` | captured (25 KiB, 502&times;148, RGBA) |
| `product_business_slice/list-validations-status.png` | captured (17 KiB, 251&times;178, RGBA) |
| `product_business_slice/list-validations-category.png` | captured (17 KiB, 310&times;171, RGBA) |
| `product_business_slice/edit-status-after.png` | captured (33 KiB, 536&times;197, RGBA) |

The captured set covers the four content categories the controlling FTR
calls out (overview, helper columns, list validations, edit). The
list-validations bucket is covered by two images (status and category)
instead of one because each cell only opens its own dropdown, and both
rules are part of the journey the demo `README.md` step 5 asks the
reader to inspect.

The original capture plan also listed `edit-status-before.png`. That
image was not captured: the workbook-overview and helper-columns frames
already show the unedited state of the `status` column, so a dedicated
"before" frame would duplicate signal. The single `edit-status-after.png`
is sufficient to support the README's step-6 (edit) / step-8 (verify)
narrative; removing the paired frame keeps image density honest.

Image references in the walkthrough source
`docs/walkthroughs/product_business_slice.adoc` are wrapped in
`ifndef::backend-revealjs[]` blocks so they appear in the AsciiDoc
HTML render (and on GitHub's web view of the .adoc file) but not in
the published Reveal.js deck. The demo publish-docs workflow rsyncs
only `build/slides/` into `versions/<tag>/demo/slides/` and
`latest/demo/slides/`; it does not copy `docs/screenshots/` into the
Pages layout. Embedding raw `image::` directives in the slide source
would therefore produce broken-image icons in the published deck.
Bundling images into the deck publish is the deferred follow-up named
in *Reference / publishing policy* below; the demo `README.md` itself
stays text-only and points readers at the walkthrough document for
the image-rich version.

## Per-image content specification

Each image should be cropped tight to the spreadsheet region of
interest, not a full-window capture with surrounding desktop / app
chrome. Annotations (arrows, red boxes) are welcome if they help the
reader, but the underlying screenshot must reflect the actual workbook
the maintainer ran &mdash; do not stage cells the pipeline did not
produce.

### `workbook-overview.png`

Goal: show the three sheets and their distinct per-sheet styling at a
glance.

* Open `tmp/product_business_slice.xlsx` after a clean run of
  `make run PIPELINE=./pipelines/demo_product_business_slice.yaml`.
* Capture frame: enough of the bottom sheet tab bar to show
  `product`, `product_manager`, and `branch` tabs side by side, plus
  the top three or four header rows of whichever sheet is active.
* Visible: the distinct header fills (`product` green,
  `product_manager` blue, `branch` orange) on the tab bar or via a
  quick click-through composite.

### `helper-columns.png`

Goal: show that the helper column sits next to its FK column on the
`product` sheet.

* Sheet: `product`.
* Visible columns (left to right): at minimum `id`, `name`,
  `id_(product_manager)`, `_product_manager_name`, `status`.
* Capture frame: a handful of body rows; enough for the reader to see
  that the helper value (`Marta Vogel`, etc.) tracks the FK value
  (`PM-10`, etc.). Do not crop out the helper column header.

### `list-validations-status.png` and `list-validations-category.png`

Goal: show the Excel/Calc list-validation dropdowns on the two
validated `product` columns.

* Sheet: `product`.
* Click a `status` cell to open its in-cell dropdown; capture the
  dropdown showing `active` / `pilot` / `retired`. Then repeat on a
  `category` cell to capture `entry` / `standard` / `premium`.
* Capture frame: the dropdown plus enough surrounding cells that the
  reader can see which column is opening.
* Alternative if the dropdown UI is awkward to capture: a screenshot
  of the data-validation dialog (Data &rarr; Validation) for the
  same column showing the allowed list.

### `edit-status-after.png`

Goal: support the README's step-6 (edit) / step-8 (verify) narrative
with a single after-edit frame.

* Sheet: `product`. Pick a row whose original `status` is visible in
  `workbook-overview.png` or `helper-columns.png`.
* Capture the row after the edit and save; the `status` cell shows
  the new value (for example `pilot` where the source data had
  `active`).
* A paired "before" frame is intentionally not captured because the
  pre-edit state is already visible in the overview / helper-column
  captures. Adding it would duplicate signal.

## Size and format

* PNG (matches the FTR; lossless for a screenshot of a UI).
* Target size: <= 200 KB per image. If a particular image exceeds
  that, add a one-line justification in the *Capture log* row for that
  image rather than silently shipping a large file.
* Crop tight: a full-screen capture of a 4K display is rarely useful
  and tends to push past the size budget. Crop to the spreadsheet
  region; re-export at a sensible width (1200&ndash;1600 px).
* No personally identifying info; the demo dataset is synthetic but
  if you capture window chrome, make sure it does not leak (for
  example) other open documents in the recent-files menu.

## Refresh procedure

Run this when the demo journey, the workbook layout, or the pinned
core version changes meaningfully:

1. Confirm the demo is bound to the version you are capturing against
   (typically the currently-pinned core release per
   `LIB_PYPI_VERSION` in the demo `Makefile`, or your local sibling
   checkout via `make setup-lib-local`).
2. Clean the previous run output:
   `rm -rf ./tmp/product_business_slice.xlsx`.
3. Re-run the forward pipeline:
   `make run PIPELINE=./pipelines/demo_product_business_slice.yaml`.
4. Open `./tmp/product_business_slice.xlsx` in Excel or LibreOffice
   Calc.
5. Capture the images per the spec above. Replace existing PNGs
   in-place; keep the filenames stable so any future README image
   references do not break.
6. Update the *Capture log* table at the bottom of this README with
   the release tag and capture date.
7. If a particular shot has drifted so far that no honest capture
   reproduces what an earlier image promised, **delete the stale
   image rather than ship a misleading one** (per the controlling
   FTR's drift mitigation), and remove or update any references to
   it in the per-image spec.

## Reference / publishing policy

* These screenshots are local to the demo repository. They are not
  currently copied into the Pages publish output; a later FTR will
  decide the publishing model.
* The walkthrough source at
  `docs/walkthroughs/product_business_slice.adoc` embeds them via
  `ifndef::backend-revealjs[]` so they render in the AsciiDoc HTML
  output and on the demo repository's GitHub web view of the .adoc
  file but do not appear in the published Reveal.js deck.
* Any future publishing of these images must honour the same
  frozen-context-versioned policy that
  `FTR-RELEASE-README-VERSION-BAKING-P5` (DRAFT, in core backlog) is
  expected to formalise: images linked from a release-frozen document
  must either live under `versions/<tag>/...` or carry a clear
  "latest / current release" label, so users on an older release do
  not see freshly-captured imagery without a version cue.
* The demo `README.md` itself stays text-only and points readers at
  the walkthrough document for the image-rich version; deliberately
  keeping it text-only avoids turning the entry README into an
  image-heavy page.

## Capture log

| Date       | Release tag captured against | Notes                                                                                                              |
|------------|------------------------------|--------------------------------------------------------------------------------------------------------------------|
| 2026-05-24 | `v0.1.0b6`                   | Initial capture. Manual screenshots from LibreOffice Calc on Linux against the currently-pinned core release.       |
