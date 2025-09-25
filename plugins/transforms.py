from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd

from spreadsheet_handling.pipeline.pipeline import BoundStep

Frames = Dict[str, pd.DataFrame]


@dataclass(frozen=True)
class ExtractProductsCfg:
    """Configuration for the extract-products step (example demo)."""
    left_key: str = "id"
    right_key: str = "product_id"
    output_sheet: str = "products_extracted"


def make_extract_products_step(
    *,
    left_key: str = "id",
    right_key: str = "product_id",
    output_sheet: str = "products_extracted",
    name: str = "extract_products",
) -> BoundStep:
    """
    Demo transform step: merge 'products' with 'fees' into 'products_extracted'.
    Pure Frames->Frames; no file I/O here.
    """
    cfg = ExtractProductsCfg(left_key=left_key, right_key=right_key, output_sheet=output_sheet)

    def _run(fr: Frames) -> Frames:
        out: Frames = dict(fr)

        products = fr.get("products") or fr.get("product")
        fees = fr.get("fees")

        if products is None or fees is None:
            # If inputs are missing, just pass through
            return out

        if cfg.left_key not in products.columns or cfg.right_key not in fees.columns:
            # Keys not present; pass through
            return out

        merged = products.merge(fees, left_on=cfg.left_key, right_on=cfg.right_key, how="left")
        out[cfg.output_sheet] = merged
        return out

    return BoundStep(
        name=name,
        config={"left_key": left_key, "right_key": right_key, "output_sheet": output_sheet},
        fn=_run,
    )
