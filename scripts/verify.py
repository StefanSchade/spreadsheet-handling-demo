from __future__ import annotations

from pathlib import Path

from spreadsheet_handling.io_backends.json_backend import JSONBackend

from plugins.extractions.branch_manager_summary import extract_branch_manager_summary


def main() -> None:
    data_dir = Path("./data/branches_minimal")
    frames = JSONBackend().read_multi(str(data_dir), header_levels=1)
    out = extract_branch_manager_summary(frames)
    summary = out["BranchSummary"]

    assert list(summary.columns) == ["id", "name", "region", "manager"]
    print("Verification OK.")


if __name__ == "__main__":
    main()
