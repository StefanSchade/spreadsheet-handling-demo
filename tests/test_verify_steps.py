from __future__ import annotations

from typing import Dict

import pandas as pd
import pytest

from plugins.verify_steps import make_verify_step


Frames = Dict[str, pd.DataFrame]


def test_verify_warn_mode_all_good() -> None:
    frames: Frames = {
        "products": pd.DataFrame({"id": [1, 2], "name": ["A", "B"]}),
        "fees": pd.DataFrame({"product_id": [1, 2], "amount": [1.0, 2.0]}),
    }
    step = make_verify_step(mode="warn")
    out = step(frames)
    assert out is frames  # same object or equal content is fine


def test_verify_fail_on_empty_columns() -> None:
    frames: Frames = {"empty": pd.DataFrame()}
    step = make_verify_step(mode="fail")
    with pytest.raises(ValueError):
        step(frames)
