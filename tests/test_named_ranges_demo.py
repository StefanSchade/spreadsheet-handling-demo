from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook
from spreadsheet_handling.cli.apps.run import main as run_main


def test_product_business_slice_workbook_contains_named_ranges(tmp_path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    workbook_path = tmp_path / "product_business_slice.xlsx"
    exit_code = run_main([
        "--config",
        "pipelines/demo_product_business_slice.yaml",
        "--out-path",
        str(workbook_path),
    ])
    assert exit_code == 0

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
