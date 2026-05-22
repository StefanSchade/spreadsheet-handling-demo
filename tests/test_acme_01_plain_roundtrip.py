from __future__ import annotations

import json
from pathlib import Path

from spreadsheet_handling.cli.apps.run import main as run_main


def _run_demo(*argv: str) -> None:
    exit_code = run_main(list(argv))
    assert exit_code == 0, f"demo run failed: {' '.join(argv)}"


def test_acme_01_plain_roundtrip_preserves_source(tmp_path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(repo_root)

    workbook_path = tmp_path / "acme_01_plain.xlsx"
    reimport_dir = tmp_path / "acme_01_roundtrip"

    _run_demo(
        "--config",
        "pipelines/acme_01_plain_forward.yaml",
        "--out-path",
        str(workbook_path),
    )

    _run_demo(
        "--config",
        "pipelines/acme_01_plain_reverse.yaml",
        "--in-path",
        str(workbook_path),
        "--out-path",
        str(reimport_dir),
    )

    source = json.loads((repo_root / "data/acme_plain/employees.json").read_text(encoding="utf-8"))
    returned = json.loads((reimport_dir / "employees.json").read_text(encoding="utf-8"))

    assert returned == source
