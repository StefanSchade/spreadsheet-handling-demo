from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping, TypedDict

import pandas as pd

# Import the project's BoundStep type from the library
from spreadsheet_handling.pipeline.pipeline import BoundStep

Frames = Dict[str, pd.DataFrame]


@dataclass(frozen=True)
class VerifyConfig:
    """Configuration for verification behavior."""
    mode: str = "warn"  # "warn" | "fail"


def make_verify_step(*, mode: str = "warn", name: str = "verify") -> BoundStep:
    """
    Create a typed verification step (Frames -> Frames).
    - In 'warn' mode: logs issues (stdout) and returns frames unchanged.
    - In 'fail' mode: raises ValueError on the first detected issue.
    """
    cfg = VerifyConfig(mode=mode)

    def _verify(frames: Frames) -> Frames:
        issues: list[str] = []

        # Example checks (extend as needed):
        # 1) Ensure each sheet has at least a header (non-empty dataframe)
        for sheet_name, df in frames.items():
            if not isinstance(df, pd.DataFrame):
                issues.append(f"{sheet_name}: not a DataFrame")
                continue
            if df.shape[1] == 0:
                issues.append(f"{sheet_name}: no columns")
            # Example: no duplicated column names
            if df.columns.duplicated().any():
                issues.append(f"{sheet_name}: duplicated columns detected")

        if issues:
            msg = "Verification issues:\n- " + "\n- ".join(issues)
            if cfg.mode == "fail":
                raise ValueError(msg)
            # warn mode: print and proceed
            print(msg)

        return frames

    # Return BoundStep with declared name/config
    return BoundStep(name=name, config={"mode": cfg.mode}, fn=_verify)
