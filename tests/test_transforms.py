from __future__ import annotations

from typing import Dict

import pandas as pd

from plugins.extractions.branch_manager_summary import extract_branch_manager_summary

Frames = Dict[str, pd.DataFrame]


def test_extract_branch_manager_summary_basic_join() -> None:
    frames: Frames = {
        "branch": pd.DataFrame(
            {
                "id": ["B-001", "B-002"],
                "name": ["South", "Central"],
                "region": ["S", "C"],
            }
        ),
        "managers": pd.DataFrame(
            {
                "id_(branch)": ["B-001", "B-002"],
                "manager": ["Alice", "Bob"],
            }
        ),
    }

    out = extract_branch_manager_summary(frames)

    assert list(out) == ["BranchSummary"]
    summary = out["BranchSummary"]
    assert list(summary.columns) == ["id", "name", "region", "manager"]
    assert list(summary["manager"]) == ["Alice", "Bob"]


def test_extract_branch_manager_summary_keeps_first_manager_per_branch() -> None:
    frames: Frames = {
        "branch": pd.DataFrame(
            {
                "id": ["B-002"],
                "name": ["Central"],
                "region": ["C"],
            }
        ),
        "managers": pd.DataFrame(
            {
                "id_(branch)": ["B-002", "B-002"],
                "manager": ["Bob", "Peter"],
            }
        ),
    }

    out = extract_branch_manager_summary(frames)

    summary = out["BranchSummary"]
    assert list(summary["manager"]) == ["Bob"]
