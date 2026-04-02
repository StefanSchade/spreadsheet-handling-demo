from __future__ import annotations

from typing import Dict

import pandas as pd

from plugins.extractions.branch_manager_summary import extract_branch_manager_summary
from plugins.extractions.product_overview import extract_product_overview

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


def test_extract_product_overview_builds_report_table() -> None:
    frames: Frames = {
        "product": pd.DataFrame(
            {
                "id": ["P-100"],
                "name": ["Starter Kit"],
                "id_(product_manager)": ["PM-10"],
                "status": ["active"],
                "category": ["entry"],
            }
        ),
        "product_manager": pd.DataFrame(
            {
                "id": ["PM-10"],
                "name": ["Marta Vogel"],
                "id_(branch)": ["B-001"],
                "email": ["marta@example.test"],
            }
        ),
        "branch": pd.DataFrame(
            {
                "id": ["B-001"],
                "name": ["Berlin Hub"],
                "country": ["DE"],
                "region": ["Central Europe"],
            }
        ),
    }

    out = extract_product_overview(frames)

    assert list(out) == ["ProductOverview"]
    overview = out["ProductOverview"]
    assert list(overview.columns) == [
        "product_id",
        "product_name",
        "status",
        "category",
        "product_manager_name",
        "branch_name",
        "branch_country",
        "branch_region",
    ]
    assert overview.iloc[0]["product_manager_name"] == "Marta Vogel"
    assert overview.iloc[0]["branch_name"] == "Berlin Hub"
