#!/usr/bin/env bash
# Use local spreadsheet-handling source (sibling checkout) for Make targets.
# Usage examples:
#   scripts/dev-local-lib.sh pack
#   scripts/dev-local-lib.sh unpack
#   scripts/dev-local-lib.sh which-lib
#   scripts/dev-local-lib.sh make pack  # full control if you prefer

set -euo pipefail

# Repo root = this script's parent dir
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv"

# Where the local lib lives (adjust if needed)
LIB_SRC="${LIB_SRC:-$ROOT/../spreadsheet-handling}"
LIB_INIT="$LIB_SRC/src/spreadsheet_handling/__init__.py"

if [[ ! -f "$LIB_INIT" ]]; then
  echo "❌ Local lib not found at: $LIB_INIT"
  echo "   Set LIB_SRC=/path/to/spreadsheet-handling and retry."
  exit 2
fi

# ensure venv exists
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "➡️  creating venv at $VENV"
  python3 -m venv "$VENV"
fi

# Build PYTHONPATH that points to local lib first
export PYTHONPATH="$LIB_SRC/src:${PYTHONPATH:-}"

# Point our CLI commands to the module entrypoints (bypass console scripts)
export PACK_CMD="$VENV/bin/python -m spreadsheet_handling.cli.sheets_pack"
export UNPACK_CMD="$VENV/bin/python -m spreadsheet_handling.cli.sheets_unpack"
export RUN_CMD="$VENV/bin/python -m spreadsheet_handling.cli.run"

# Helper: show which lib is used
if [[ "${1:-}" == "which-lib" ]]; then
  "$VENV/bin/python" - <<'PY'
import spreadsheet_handling, inspect, sys
print("Using:", inspect.getfile(spreadsheet_handling))
print("sys.path[0..3]:", sys.path[:4])
PY
  exit 0
fi

# Run a make target or pass through to make
if [[ "${1:-}" == "make" ]]; then
  shift
  exec make "$@"
elif [[ -n "${1:-}" ]]; then
  exec make "$1"
else
  echo "Usage: scripts/dev-local-lib.sh <target|which-lib|make ...>"
  exit 1
fi

