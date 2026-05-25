"""Contract checks for demo pipelines that use FK-helper primitives.

Under the v2 FK-helper runtime contract
(``FTR-FK-HELPER-DOCS-DEMO-REALIGNMENT-P5``), every demo pipeline that
runs an FK-helper consumer must run a policy producer
(``infer_fk_relations`` or ``configure_fk_helpers``) earlier in the same
pipeline -- with the documented exception of the reimport pipeline, which
relies on derived helper provenance persisted in the workbook.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

PIPELINES_DIR = Path(__file__).resolve().parents[1] / "pipelines"

_FK_HELPER_CONSUMERS = frozenset(
    {
        "add_fk_helpers",
        "reorder_fk_helpers",
        "validate_fk_helpers",
        "remove_fk_helpers",
    }
)

_FK_POLICY_PRODUCERS = frozenset(
    {
        "infer_fk_relations",
        "configure_fk_helpers",
    }
)

# `demo_workbook_reimport.yaml` is the documented exception: it reads
# derived helper provenance written by an earlier forward run, so no
# in-pipeline producer is required.
_REIMPORT_PIPELINES = frozenset({"demo_workbook_reimport.yaml"})


def _iter_steps(doc: dict) -> list[dict]:
    if isinstance(doc, dict) and isinstance(doc.get("pipeline"), list):
        return [s for s in doc["pipeline"] if isinstance(s, dict)]
    return []


@pytest.mark.parametrize(
    "pipeline_yaml",
    sorted(p.name for p in PIPELINES_DIR.glob("*.yaml")),
)
def test_demo_pipeline_uses_v2_fk_contract(pipeline_yaml: str) -> None:
    """FK-helper consumers must follow a policy producer in the same pipeline."""
    path = PIPELINES_DIR / pipeline_yaml
    steps = _iter_steps(yaml.safe_load(path.read_text(encoding="utf-8")))

    seen_producer = False
    for raw in steps:
        step_id = raw.get("step")
        if step_id in _FK_POLICY_PRODUCERS:
            seen_producer = True
            continue
        if step_id not in _FK_HELPER_CONSUMERS:
            continue
        if pipeline_yaml in _REIMPORT_PIPELINES:
            # Reimport reads persisted provenance; no in-pipeline producer
            # is required.
            continue
        assert seen_producer, (
            f"{pipeline_yaml}: FK-helper consumer {step_id!r} appears "
            f"before any FK policy producer "
            f"({sorted(_FK_POLICY_PRODUCERS)})"
        )
