from __future__ import annotations

import json
from pathlib import Path

from spreadsheet_handling.cli.apps.run import main as run_main


def _run_demo(*argv: str) -> None:
    exit_code = run_main(list(argv))
    assert exit_code == 0, f"demo run failed: {' '.join(argv)}"


def _sort_pairs(rows):
    return sorted(
        ((r["product_id"], r["market_id"], r["available"]) for r in rows),
        key=lambda t: (t[0], t[1]),
    )


def test_acme_03_xref_roundtrip_recovers_canonical_pairs(tmp_path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    workbook_path = tmp_path / "acme_03_xref.xlsx"
    reimport_dir = tmp_path / "acme_03_xref_roundtrip"

    _run_demo(
        "--config",
        "pipelines/acme_03_xref_forward.yaml",
        "--out-path",
        str(workbook_path),
    )

    _run_demo(
        "--config",
        "pipelines/acme_03_xref_reverse.yaml",
        "--in-path",
        str(workbook_path),
        "--out-path",
        str(reimport_dir),
    )

    source = json.loads(
        (repo_root / "data/acme_03_xref/product_market.json").read_text(encoding="utf-8")
    )
    returned = json.loads((reimport_dir / "product_market.json").read_text(encoding="utf-8"))

    assert _sort_pairs(returned) == _sort_pairs(source)
