from pathlib import Path
import yaml

def extract_all(dataset, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Beispielhafte YAMLs:
    emit_yaml(out_dir/"rules.yml", {"rules": derive_rules(dataset)})
    emit_yaml(out_dir/"products.yml", {"products": derive_products(dataset)})
    # ... bis ~10 Dateien

def emit_yaml(path: Path, obj):
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)

def derive_rules(dataset):
    # TODO: echte Logik aus dataset ableiten
    return [{"id": "R1", "expr": "fee > 0"}]

def derive_products(dataset):
    return [{"product_id": "P-001", "name": "Dummy", "fees": [1.0, 2.0]}]
