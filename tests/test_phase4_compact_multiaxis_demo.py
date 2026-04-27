from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from spreadsheet_handling.cli.apps.run import main as run_main
from spreadsheet_handling.io_backends.ods.ods_backend import OdsBackend
from spreadsheet_handling.io_backends.xlsx.xlsx_backend import ExcelBackend


def _run_demo(repo_root: Path, *argv: str) -> None:
    exit_code = run_main(list(argv))
    assert exit_code == 0, f"demo run failed from {repo_root}"


def _read_json(path: Path) -> list[dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase4_expand_demo_shows_sparse_compact_multiaxis_relation(tmp_path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    out_dir = tmp_path / "expanded"

    _run_demo(
        repo_root,
        "--config",
        "pipelines/demo_phase4_compact_multiaxis_expand.yaml",
        "--out-path",
        str(out_dir),
    )

    rows = _read_json(out_dir / "feature_product_codes.json")
    assert rows == [
        {
            "feature_id": "F-010",
            "feature_label": "Price can be edited",
            "column_key": "P-100",
            "code": "E",
            "code_group": "input",
        },
        {
            "feature_id": "F-010",
            "feature_label": "Price can be edited",
            "column_key": "P-200",
            "code": "E-R-K",
            "code_group": "input",
        },
        {
            "feature_id": "F-020",
            "feature_label": "Calculated tax field",
            "column_key": "P-100",
            "code": "S",
            "code_group": "system",
        },
        {
            "feature_id": "F-020",
            "feature_label": "Calculated tax field",
            "column_key": "P-200",
            "code": "S",
            "code_group": "system",
        },
        {
            "feature_id": "F-020",
            "feature_label": "Calculated tax field",
            "column_key": "P-300",
            "code": "R",
            "code_group": "review",
        },
    ]
    assert "F-030" not in {row["feature_id"] for row in rows}

    meta = yaml.safe_load((out_dir / "_meta.yaml").read_text(encoding="utf-8"))
    assert meta["compact_multiaxis"]["feature_product_codes"]["drop_empty"] is True
    assert "legend_blocks" in meta


def test_phase4_roundtrip_demo_compares_sparse_and_lossless_modes(tmp_path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    out_dir = tmp_path / "roundtrip"

    _run_demo(
        repo_root,
        "--config",
        "pipelines/demo_phase4_compact_multiaxis_roundtrip.yaml",
        "--out-path",
        str(out_dir),
    )

    sparse_rows = _read_json(out_dir / "feature_matrix_sparse_roundtrip.json")
    lossless_rows = _read_json(out_dir / "feature_matrix_lossless_roundtrip.json")
    token_rows = _read_json(out_dir / "feature_token_matrix_canonical_roundtrip.json")

    assert [row["feature_id"] for row in sparse_rows] == ["F-010", "F-020"]
    assert [row["feature_id"] for row in lossless_rows] == ["F-010", "F-020", "F-030"]
    assert lossless_rows[2] == {
        "feature_id": "F-030",
        "feature_label": "Reserved future toggle",
        "P-100": "",
        "P-200": "",
        "P-300": "",
    }
    assert token_rows[0]["P-100"] == "E-K"


@pytest.mark.parametrize(
    ("out_kind", "suffix", "backend"),
    [
        ("xlsx", ".xlsx", ExcelBackend),
        ("ods", ".ods", OdsBackend),
    ],
)
def test_phase4_workbook_demo_writes_xlsx_and_ods(
    tmp_path,
    monkeypatch,
    out_kind: str,
    suffix: str,
    backend,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)
    workbook_path = tmp_path / f"phase4_compact_multiaxis{suffix}"

    _run_demo(
        repo_root,
        "--config",
        "pipelines/demo_phase4_compact_multiaxis_workbook.yaml",
        "--out-kind",
        out_kind,
        "--out-path",
        str(workbook_path),
    )

    assert workbook_path.exists()
    frames = backend().read_multi(str(workbook_path), header_levels=1)
    assert "feature_product_codes" in frames
    assert "feature_product_tokens" in frames
    assert frames["feature_product_codes"].iloc[0]["code_group"] == "input"
    assert frames["feature_product_tokens"].iloc[0]["token_group"] == "key"
    assert "legend_blocks" in frames["_meta"]
