from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook


def test_product_multiheader_workbook_has_grouped_headers() -> None:
    workbook_path = Path("tmp/product_multiheader.xlsx")
    assert workbook_path.exists(), "Run the product multiheader slice before this test"

    wb = load_workbook(workbook_path)
    try:
        ws = wb["product_overview"]
        merged = {str(rng) for rng in ws.merged_cells.ranges}
        assert ws["A1"].value == "product"
        assert ws["A2"].value == "id"
        assert ws["B2"].value == "name"
        assert ws["C1"].value == "manager"
        assert ws["D1"].value == "branch"
        assert "A1:B1" in merged
        assert "D1:E1" in merged
    finally:
        wb.close()
