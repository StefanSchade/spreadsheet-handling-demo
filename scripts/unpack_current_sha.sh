#!/usr/bin/env bash
set -euo pipefail

TMP_DIR="${1:?tmp dir missing}"
DATA_DIR="${2:?data dir missing}"
SHA="${3:?sha missing}"

# UNPACK_CMD is passed via env (defaults for safety)
UNPACK_CMD="${UNPACK_CMD:-sheets-unpack}"

shopt -s nullglob

found=0
for x in "$TMP_DIR"/*-"$SHA".xlsx; do
  base="$(basename "$x")"

  # Skip Excel lock/temp files like "~$foo.xlsx"
  if [[ "$base" == "~$"* ]]; then
    echo "Skipping Excel lock file: $x"
    continue
  fi

  found=1
  name_noext="${base%.xlsx}"
  setname="${name_noext%-${SHA}}"

  echo "Unpacking $x -> $DATA_DIR/$setname"
  # call the CLI
  $UNPACK_CMD "$x" -o "$DATA_DIR/$setname"
done

if [[ $found -eq 0 ]]; then
  echo "No workbooks for current SHA ($SHA) in $TMP_DIR. Run make pack first."
  exit 2
fi

echo "OK: JSON updated under $DATA_DIR"
