from __future__ import annotations

from typing import Dict

import pandas as pd

from plugins.transforms import make_extract_products_step

Frames = Dict[str, pd.DataFrame]


def test_extract_products_basic_merge() -> None:
    frames: Frames = {
        "products": pd.DataFrame({"id": [1, 2], "name": ["A", "B"]}),
        "fees": pd.DataFrame({"product_id": [1, 2], "amount": [1.0, 2.0]}),
    }
    step = make_extract_products_step()
    out = step(frames)
    assert "products_extracted" in out
    merged = out["products_extracted"]
    assert list(merged.columns)[:3] == ["id", "name", "product_id"]  # merge structure predictable
    assert merged.shape[0] == 2
    assert float(merged["amount"].sum()) == 3.0


def test_extract_products_missing_inputs_pass_through() -> None:
    frames: Frames = {"products": pd.DataFrame({"id": [1]})}
    step = make_extract_products_step()
    out = step(frames)
    assert out is not None
    assert "products_extracted" not in out
