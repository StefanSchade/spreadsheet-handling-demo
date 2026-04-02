from __future__ import annotations

from typing import Dict

import pandas as pd

Frames = Dict[str, pd.DataFrame]


def extract_product_overview(frames: Frames) -> Frames:
    products = frames.get("product")
    managers = frames.get("product_manager")
    branches = frames.get("branch")

    if products is None:
        raise KeyError("Could not find required table 'product'")
    if managers is None:
        raise KeyError("Could not find required table 'product_manager'")
    if branches is None:
        raise KeyError("Could not find required table 'branch'")

    product_cols = {"id", "name", "id_(product_manager)", "status", "category"}
    manager_cols = {"id", "name", "id_(branch)", "email"}
    branch_cols = {"id", "name", "country", "region"}

    missing_product = product_cols.difference(products.columns)
    missing_manager = manager_cols.difference(managers.columns)
    missing_branch = branch_cols.difference(branches.columns)
    if missing_product:
        raise KeyError(f"product missing columns: {sorted(missing_product)}")
    if missing_manager:
        raise KeyError(f"product_manager missing columns: {sorted(missing_manager)}")
    if missing_branch:
        raise KeyError(f"branch missing columns: {sorted(missing_branch)}")

    merged = products.merge(
        managers.rename(
            columns={
                "id": "product_manager_id",
                "name": "product_manager_name",
                "id_(branch)": "branch_id",
            }
        ),
        how="left",
        left_on="id_(product_manager)",
        right_on="product_manager_id",
    ).merge(
        branches.rename(
            columns={
                "id": "branch_id",
                "name": "branch_name",
                "country": "branch_country",
                "region": "branch_region",
            }
        ),
        how="left",
        on="branch_id",
    )

    overview = merged.loc[
        :,
        [
            "id",
            "name",
            "status",
            "category",
            "product_manager_name",
            "branch_name",
            "branch_country",
            "branch_region",
        ],
    ].rename(
        columns={
            "id": "product_id",
            "name": "product_name",
        }
    )

    overview = overview.sort_values(["product_id"]).reset_index(drop=True)
    return {"ProductOverview": overview}
