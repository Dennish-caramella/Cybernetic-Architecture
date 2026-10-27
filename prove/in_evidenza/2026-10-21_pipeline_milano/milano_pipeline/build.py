"""Orchestrazione della pipeline."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from . import accessibility as acc
from . import clustering, features, grid as grid_mod, interpolate, lots as lots_mod, osm_fetch
from . import suitability as su
from .io_utils import METRIC, WGS84, Provenance, load_yaml, read_vector, sha256_file


def load_sources(grid, sources_cfg, root, prov):
    """Legge le fonti ufficiali presenti su disco e le trasferisce sulle celle. Le fonti assenti sono segnalate."""
    parts = []
    for nome, spec in sources_cfg["fonti"].items():
        f = Path(root) / spec["file"]
        if nome == "lotti_pgt":
            continue
        if not f.exists():
            prov.fonte(nome, presente=False, file=str(spec["file"]), ente=spec.get("ente"), stato_verifica=spec.get("stato_verifica"))
            prov.avviso(f"fonte '{nome}' non trovata ({spec['file']}): indicatori corrispondenti assenti")
            continue
        src = read_vector(f)
        prov.fonte(nome, presente=True, file=str(spec["file"]), righe=len(src), sha256=sha256_file(f),
                   ente=spec.get("ente"), stato_verifica=spec.get("stato_verifica"))
        parts.append(interpolate.transfer(grid, src, spec["attributi"], prov, nome))
    return parts


def analyze(inputs, cfg, sources_cfg, root, res, prov, with_access=True):
    grid = grid_mod.build_grid(inputs["boundary"], res)
    df = grid.set_index("h3")[["area_m2"]].copy()
    for p in load_sources(grid, sources_cfg, root, prov):
        df = df.join(p)

    b = features.sum_area_share(grid, inputs["buildings"], "built_density")
    if b is not None:
        df = df.join(b)
    t = features.share_of_cell(grid, inputs["transform"], "transformable_share_osm")
    if t is not None:
        df = df.join(t)
        prov.avviso("quota trasformabile da OSM (landuse dismessi/ferroviari/industriali): CANDIDATI da verificare con il PGT")
    if "c_protetta" not in df:
        pr = features.share_of_cell(grid, inputs["protected"], "prot_share")
        if pr is not None:
            df = df.join(pr)
            df["c_protetta"] = (df.pop("prot_share") >= 0.2).astype(int)
            prov.avviso("vincolo 'c_protetta' derivato da OSM (boundary=protected_area): fonte non ufficiale, da sostituire")

    if with_access:
        origins = grid_mod.cell_centroids(grid)
        times = acc.access_times(inputs["graph"], origins, inputs["pois"],
                                 cfg["accessibilita"]["velocita_kmh"], cfg["accessibilita"]["tempo_max_min"])
        pai, nok = acc.compute_pai(times, cfg["accessibilita"]["categorie"])
        tmax = cfg["accessibilita"]["tempo_max_min"]
        n_unreach = int(times.isna().sum().sum())
        if n_unreach:
            prov.avviso(f"accessibilità: {n_unreach} valori cella-servizio oltre {tmax} min (o servizio assente) "
                        f"fissati a {tmax} min per gli indicatori continui t_* (valore censurato, non reale)")
        df = df.join(times.fillna(tmax)).assign(pai=pai, servizi_raggiunti=nok)
    df = features.finalize(df, cfg)
    return grid, df


def run_all(root, cfg_path, sources_path, data_dir, synthetic=False, sensibilita=False, out_dir="data_output"):
    root = Path(root)
    cfg = load_yaml(root / cfg_path)
    sources_cfg = load_yaml(root / sources_path)
    prov = Provenance(synthetic=synthetic)
    cache = root / data_dir / "osm_cache"

    boundary = osm_fetch.fetch_boundary(cfg["area"]["osm_query"], cache)
    osm = osm_fetch.fetch_all(boundary, cache)
    roads = osm_fetch.fetch_major_roads(boundary, cache)
    inputs = {"boundary": boundary, "graph": osm["graph"], "pois": osm["pois"], "buildings": osm["buildings"],
              "transform": osm["transform"], "protected": osm["protected"]}
    prov.fonte("osm", presente=True, **{k: len(v) for k, v in osm["pois"].items()},
               edifici=len(osm["buildings"]), stato_verifica=sources_cfg["osm"]["stato_verifica"])

    res = cfg["griglia"]["h3_res"]
    grid, df = analyze(inputs, cfg, sources_cfg, root, res, prov)

    scores, cl_report = clustering.run(df, cfg["clustering"], prov)
    df = df.join(scores)
    suit, su_report = su.run(df, cfg["idoneita"], prov, seed=cfg["clustering"]["seed"])
    df = df.join(suit)

    cells = grid.set_index("h3")[["geometry"]].join(df)

    # lotti candidati
    lots_src = None
    lp = root / sources_cfg["fonti"]["lotti_pgt"]["file"]
    if lp.exists():
        lots_src = read_vector(lp)
        prov.fonte("lotti_pgt", presente=True, righe=len(lots_src), sha256=sha256_file(lp))
        origine = "PGT"
    else:
        lots_src = inputs["transform"]
        origine = "OSM (landuse dismessi/ferroviari/industriali), da verificare con PGT e catasto"
    lots = lots_mod.build_lots(lots_src, cfg["lotti"]["area_minima_m2"], inputs["boundary"])
    lots = lots_mod.evaluate(lots, cells, None, inputs["graph"], inputs["pois"], cfg, prov)
    prov.data["origine_lotti"] = origine

    sens_report = None
    if sensibilita:
        sens_report = maup_test(inputs, cfg, sources_cfg, root, res, df, prov)

    return {"roads": roads, "cfg": cfg, "prov": prov, "grid": grid, "cells": cells, "lots": lots, "inputs": inputs,
            "cluster_report": cl_report, "suit_report": su_report, "sens_report": sens_report,
            "out_dir": root / out_dir}


def maup_test(inputs, cfg, sources_cfg, root, res_base, df_base, prov):
    """Confronta l'idoneità a risoluzioni diverse aggregando al genitore H3 di livello più basso."""
    import h3
    from scipy.stats import spearmanr

    sc = list(cfg["idoneita"]["scenari"])[0]
    base_cols = f"s_{sc}"
    out = {}
    low = min([res_base] + cfg["griglia"]["h3_res_sensibilita"])

    def parent_mean(frame, r):
        s = frame[base_cols]
        par = [h3.cell_to_parent(c, low) if r > low else c for c in s.index]
        return s.groupby(par).mean()

    ref = parent_mean(df_base, res_base)
    for r in cfg["griglia"]["h3_res_sensibilita"]:
        p2 = Provenance()
        grid_r, d_r = analyze(inputs, cfg, sources_cfg, root, r, p2)
        s_r, _ = su.run(d_r, cfg["idoneita"], None, seed=cfg["clustering"]["seed"])
        m = parent_mean(s_r, r)
        j = pd.concat([ref.rename("a"), m.rename("b")], axis=1).dropna()
        rho = spearmanr(j["a"], j["b"])[0] if len(j) > 3 else float("nan")
        out[f"res{res_base}_vs_res{r}"] = {"celle_confronto": int(len(j)), "spearman": float(rho),
                                          "livello_confronto": int(low)}
    return out
