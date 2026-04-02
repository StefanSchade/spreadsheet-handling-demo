from __future__ import annotations

import pandas as pd
import pytest

from plugins.extractions.branch_manager_summary import extract_branch_manager_summary


def test_branch_manager_summary_accepts_branch_alias() -> None:
    frames = {
        "branches": pd.DataFrame(
            {
                "branch_id": ["B-001"],
                "name": ["South"],
                "region": ["S"],
            }
        ),
        "manager": pd.DataFrame(
            {
                "branch_id": ["B-001"],
                "manager_name": ["Alice"],
            }
        ),
    }

    out = extract_branch_manager_summary(frames)

    assert list(out["BranchSummary"]["manager"]) == ["Alice"]


def test_branch_manager_summary_requires_branches_table() -> None:
    with pytest.raises(KeyError, match="branches table"):
        extract_branch_manager_summary({})
