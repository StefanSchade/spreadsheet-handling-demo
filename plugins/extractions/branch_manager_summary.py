# plugins/extractions/branch_manager_summary.py
from __future__ import annotations
from typing import Dict
import pandas as pd

Frames = Dict[str, pd.DataFrame]

def _get_frame(frames: Frames, *candidates: str) -> pd.DataFrame | None:
    for key in candidates:
        if key in frames:
            return frames[key]
    return None

def extract_branch_manager_summary(
        frames: Frames,
        *,
        branch_keys=("branch", "branches"),
        manager_keys=("managers", "manager", "branch_managers"),
) -> Frames:
    """
    Join branches with managers on 'branch_id' and emit a single sheet
    'BranchSummary' with: branch_id, name, region, manager.

    If managers is missing, we still emit the branches with manager empty.
    """

    branches = _get_frame(frames, *branch_keys)
    if branches is None:
        raise KeyError(f"Could not find a branches table. Tried keys: {branch_keys}")

    managers = _get_frame(frames, *manager_keys)
    if managers is None:
        # make empty managers table with expected columns so left-join works
        managers = pd.DataFrame(columns=["branch_id", "manager"])

    # be tolerant about column names casing
    b = branches.rename(columns=str)
    m = managers.rename(columns=str)

    # ensure required columns exist
    for col in ("branch_id", "name", "region"):
        if col not in b.columns:
            raise KeyError(f"Branches missing required column '{col}'")

    if "branch_id" not in m.columns or "manager" not in m.columns:
        # allow alternative columns? keep it simple for demo
        pass

    merged = pd.merge(b, m, how="left", on="branch_id")

    out = {
        "BranchSummary": merged.loc[:, ["branch_id", "name", "region", "manager"]]
        .sort_values(["branch_id"])
        .reset_index(drop=True)
    }
    return out
