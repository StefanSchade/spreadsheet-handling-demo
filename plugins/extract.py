from pathlib import Path
from spreadsheet_handling.api import load_dataset
from plugins.extractors import extract_all
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

ds = load_dataset(args.data)
extract_all(ds, Path(args.out))
print(f"Extracted YAMLs to {args.out}")
