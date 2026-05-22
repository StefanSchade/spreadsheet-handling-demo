#!/usr/bin/env bash
# run_demo.sh -- ACME demo launcher for Linux/macOS
#
# Usage:  ./run_demo.sh <pipeline.yaml> [extra flags]
# Flag:   --refresh-venv  force venv recreate (e.g. after Python upgrade)
#
# Examples:
#   ./run_demo.sh pipelines/acme_01_plain_forward.yaml
#   ./run_demo.sh pipelines/acme_01_plain_reverse.yaml

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
VENV="$SCRIPT_DIR/.venv"

REFRESH=0
if [[ "${1:-}" == "--refresh-venv" ]]; then
  REFRESH=1
  shift
fi

if [[ -z "${1:-}" ]]; then
  echo "Usage: $0 [--refresh-venv] <pipeline.yaml>"
  echo
  echo "  $0 pipelines/acme_01_plain_forward.yaml"
  echo "  $0 pipelines/acme_01_plain_reverse.yaml"
  exit 1
fi

# Create venv and install once; skip on subsequent runs to avoid uncontrolled upgrades
if [[ "$REFRESH" -eq 1 ]] || [[ ! -x "$VENV/bin/python" ]]; then
  echo "Setting up .venv (run with --refresh-venv to force update) ..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -e "$SCRIPT_DIR"
  echo "Done."
fi

"$VENV/bin/python" -m spreadsheet_handling.cli.apps.run --config "$@"
