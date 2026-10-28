import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import yaml

WGS84 = "EPSG:4326"
METRIC = "EPSG:32632"  # UTM 32N, adatto a Milano


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def sha256_file(path, block=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()


def read_vector(path, layer=None):
    gdf = gpd.read_file(path, layer=layer)
    if gdf.crs is None:
        raise ValueError(f"{path}: CRS assente. Impostalo prima di usare il file (non lo assumo).")
    return gdf.to_crs(WGS84)


class Provenance:
    """Registra per ogni passo cosa è stato letto, cosa è mancato, cosa è stato saltato."""

    def __init__(self, synthetic=False):
        self.data = {
            "creato_il": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "synthetic": bool(synthetic),
            "fonti": {},
            "avvisi": [],
            "feature_assenti": [],
            "vincoli_non_applicati": [],
        }

    def fonte(self, nome, **info):
        self.data["fonti"][nome] = info

    def avviso(self, msg):
        self.data["avvisi"].append(msg)
        print("AVVISO:", msg)

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
