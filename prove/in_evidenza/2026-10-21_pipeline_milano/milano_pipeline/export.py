import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .io_utils import WGS84


def _num(v):
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return round(float(v), 4)
    return v


def _rings(geom, tol=0.00004):
    g = geom.simplify(tol, preserve_topology=True)
    parts = [g] if g.geom_type == "Polygon" else list(g.geoms) if g.geom_type == "MultiPolygon" else []
    return [[[round(x, 5), round(y, 5)] for x, y in p.exterior.coords] for p in parts if not p.is_empty]


def export_all(R):
    out = Path(R["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    cells, lots, cfg, prov = R["cells"], R["lots"], R["cfg"], R["prov"]

    cells.reset_index().to_crs(WGS84).to_file(out / "celle.geojson", driver="GeoJSON")
    if len(lots):
        lots.to_file(out / "lotti_candidati.geojson", driver="GeoJSON")
        lots.drop(columns="geometry").sort_values(f"rank_{list(cfg['idoneita']['scenari'])[0]}").to_csv(
            out / "lotti_candidati.csv", index=False)
    json.dump(R["cluster_report"], open(out / "report_cluster.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({"idoneita": R["suit_report"], "sensibilita_risoluzione": R["sens_report"]},
              open(out / "report_idoneita.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    prov.save(out / "manifest.json")

    # pacchetto per il viewer (script caricabile da file://, senza server)
    cells4 = cells.to_crs(WGS84)
    ccols = [c for c in cells4.columns if c != "geometry"]
    data = {
        "manifest": prov.data,
        "scenari": cfg["idoneita"]["scenari"],
        "criteri": list(cfg["idoneita"]["criteri"].keys()),
        "vincoli": cfg["idoneita"]["vincoli_booleani"],
        "cluster_report": R["cluster_report"],
        "cells": [{"id": i, "r": max(_rings(g, 0.00001), key=len), "p": {c: _num(row[c]) for c in ccols}}
                  for (i, row), g in zip(cells4.iterrows(), cells4.geometry)],
        "lots": [{"id": r["lot_id"], "r": _rings(r.geometry),
                  "p": {c: _num(r[c]) for c in lots.columns if c not in ("geometry", "lot_id")}}
                 for _, r in lots.iterrows()] if len(lots) else [],
        "boundary": [ring for g in R["inputs"]["boundary"].geometry for ring in _rings(g, 0.0002)],
        "roads": [[[round(x, 5), round(y, 5)] for x, y in g.coords] for g in
                  (R["roads"].geometry.simplify(0.0001).explode(index_parts=False) if len(R["roads"]) else [])
                  if g.geom_type == "LineString"],
        "pois": {c: [[round(p.x, 5), round(p.y, 5)] for p in g.geometry] for c, g in R["inputs"]["pois"].items()},
    }
    vdir = Path(R["out_dir"]).parent / "viewer"
    vdir.mkdir(exist_ok=True)
    with open(vdir / ("data_test.js" if prov.data["synthetic"] else "data.js"), "w", encoding="utf-8") as f:
        f.write("window.PIPELINE_DATA = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    return out
