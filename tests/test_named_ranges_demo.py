from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook


def test_product_business_slice_workbook_contains_named_ranges() -> None:
    workbook_path = Path("tmp/product_business_slice.xlsx")
    assert workbook_path.exists(), "Run the product business slice before this test"

    wb = load_workbook(workbook_path)
    try:
        names = set(wb.defined_names.keys())
    finally:
        wb.close()

    assert "product_product_table" in names
    assert "product_product_header" in names
    assert "product_product_body" in names
    assert "product_manager_product_manager_table" in names
    assert "branch_branch_table" in names
