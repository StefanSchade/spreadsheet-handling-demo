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
    workbook-overview.png                     <- planned
    helper-columns.png                        <- planned
    list-validations-status.png               <- planned
    edit-status-before.png                    <- planned
    edit-status-after.png                     <- planned
```

Naming convention: kebab-case, descriptive, no version suffix in the
filename. The capture metadata (release tag, date) lives in the *Capture
log* section below.

## Current capture state

| Image | Status |
|---|---|
| `product_business_slice/workbook-overview.png` | pending capture |
| `product_business_slice/helper-columns.png` | pending capture |
| `product_business_slice/list-validations-status.png` | pending capture |
| `product_business_slice/edit-status-before.png` | pending capture |
| `product_business_slice/edit-status-after.png` | pending capture |

This first slice landed the directory layout, the per-image content
specification below, and the maintainer refresh procedure. The actual
PNG capture is a maintainer step (the controlling FTR rejects automated
/ headless capture for the beta line). Until the images exist, the demo
`README.md` deliberately does not reference them; it stays text-only and
points users to the Reveal.js deck for live visual material. Adding
inline image references is a one-line follow-up once a captured set
lands.

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

### `list-validations-status.png`

Goal: show the Excel/Calc list-validation dropdown on a `status`
cell.

* Sheet: `product`.
* Click a `status` cell to open the in-cell dropdown.
* Capture frame: the dropdown showing `active` / `pilot` / `retired`
  with the cell address visible.
* Alternative if the dropdown UI is awkward to capture: a screenshot
  of the data-validation dialog (Data &rarr; Validation) for the
  `status` column showing the allowed list.

### `edit-status-before.png` and `edit-status-after.png`

Goal: a paired before/after of a single business edit, to support the
README's step-6 (edit) / step-8 (verify) narrative.

* Pick one row on `product` (the same row in both frames).
* `edit-status-before.png` &mdash; row before the edit; `status` shows
  its original value (e.g. `active`).
* `edit-status-after.png` &mdash; same row after the edit and save;
  `status` shows the new value (e.g. `pilot`).
* The two frames should be identical except for the edited cell;
  do not also rearrange columns, change zoom, or change the active
  sheet between frames.

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
* Any future publishing of these images must honour the same
  frozen-context-versioned policy that
  `FTR-RELEASE-README-VERSION-BAKING-P5` (DRAFT, in core backlog) is
  expected to formalise: images linked from a release-frozen document
  must either live under `versions/<tag>/...` or carry a clear
  "latest / current release" label, so users on an older release do
  not see freshly-captured imagery without a version cue.
* References from the demo `README.md` are an explicit follow-up
  step once a captured set lands; the FTR allows both
  "reference inline now" and "hold references for the publishing
  slice" as acceptable models.

## Capture log

| Date       | Release tag captured against | Notes                          |
|------------|------------------------------|--------------------------------|
| (pending)  | (pending)                    | Initial capture not yet landed |
