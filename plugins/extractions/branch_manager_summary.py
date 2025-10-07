from __future__ import annotations
from typing import Dict, Iterable, List
import pandas as pd

Frames = Dict[str, pd.DataFrame]

def _flatten_labels(cols: Iterable[object]) -> List[str]:
    """Map ('id_(branch)', '', '') -> 'id_(branch)'; plain strings stay as-is."""
    out: List[str] = []
    for c in cols:
        if isinstance(c, tuple):
            for x in c:
                s = str(x)
                if s:
                    out.append(s)
                    break
            else:
                out.append("")  # all empty
        else:
            out.append(str(c))
    return out

def _first_present(cols: Iterable[str], options: Iterable[str]) -> str | None:
    lo = {c.lower(): c for c in cols}
    for opt in options:
        key = str(opt).lower()
        if key in lo:
            return lo[key]
    return None

def _get_frame(frames: Frames, *candidates: str) -> pd.DataFrame | None:
    for key in candidates:
        if key in frames:
            return frames[key]
    return None

def extract_branch_manager_summary(
        frames: Frames,
        *,
        branch_keys=("branch", "branches"),
        manager_keys=("managers", "manager", "branch_managers"),
) -> Frames:
    """
    Join branches with managers and emit 'BranchSummary' with: id, name, region, manager.
    Tolerates:
      - Branch PK:  'id' | 'branch_id'
      - Manager FK: 'id' | 'branch_id' | 'id_(branch)'
      - Manager name: 'manager' | 'manager_name' | 'lead'
      - Tuple-ish (MultiIndex-like) headers in either table
      - Duplicate manager rows per branch (keeps first)
    """
    branches = _get_frame(frames, *branch_keys)
    if branches is None:
        raise KeyError(f"Could not find a branches table. Tried keys: {branch_keys}")

    managers = _get_frame(frames, *manager_keys)
    if managers is None:
        managers = pd.DataFrame(columns=["id", "manager"])

    # ---- normalize headers in both tables ----
    b = branches.copy()
    m = managers.copy()

    print("[extract] branches columns:", list(b.columns))
    print("[extract] managers columns:", list(m.columns))

    b.columns = _flatten_labels(b.columns)
    m.columns = _flatten_labels(m.columns)

    print("[extract] flat branches columns:", list(b.columns))
    print("[extract] flat managers columns:", list(m.columns))

    # ---- detect branch columns ----
    b_id  = _first_present(b.columns, ["id", "branch_id"])
    b_nm  = _first_present(b.columns, ["name"])
    b_reg = _first_present(b.columns, ["region"])
    for need, label in [(b_id, "id/branch_id"), (b_nm, "name"), (b_reg, "region")]:
        if need is None:
            raise KeyError(f"Branches missing required column '{label}'")

    if b_id != "id":
        b = b.rename(columns={b_id: "id"})
        b_id = "id"

    # ---- detect manager columns ----
    m_fk  = _first_present(m.columns, ["id", "branch_id", "id_(branch)"])
    m_mgr = _first_present(m.columns, ["manager", "manager_name", "lead"])

    if m_fk is None and len(m) > 0:
        # If headers were odd and we still didn’t match, fail loudly:
        raise KeyError(f"Managers missing required FK column (expected one of: id | branch_id | id_(branch)); got {list(m.columns)}")

    if m_mgr is None:
        m_mgr = "manager"
        if m_mgr not in m.columns:
            # make sure the column exists to allow a clean left join
            m[m_mgr] = ""

    if m_fk is None:
        # empty managers table → still allow left join
        m_fk = "id"
        m = pd.DataFrame(columns=[m_fk, m_mgr])

    if m_fk != "id":
        m = m.rename(columns={m_fk: "id"})

    # if there are multiple manager rows per id, take the first non-empty
    if len(m) > 0:
        m = (m
             .sort_values([ "id" ])
             .drop_duplicates(subset=[ "id" ], keep="first"))

    merged = pd.merge(b, m[[ "id", m_mgr ]], how="left", on="id").rename(columns={m_mgr: "manager"})
    out = {
        "BranchSummary": (merged.loc[:, ["id", b_nm, b_reg, "manager"]]
                          .rename(columns={b_nm: "name", b_reg: "region"})
                          .sort_values(["id"])
                          .reset_index(drop=True))
    }
    return out
