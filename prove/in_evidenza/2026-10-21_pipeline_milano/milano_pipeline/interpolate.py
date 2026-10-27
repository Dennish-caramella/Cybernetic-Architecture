"""Trasferimento di attributi da poligoni sorgente alle celle H3 per sovrapposizione areale.

Nota metodologica: l'interpolazione areale assume distribuzione uniforme dentro ogni poligono sorgente.
È una semplificazione che introduce errore (MAUP). Il test di sensibilità sulla risoluzione H3 serve a misurarlo.
"""
import numpy as np
import pandas as pd

from .io_utils import METRIC


def _overlay(grid, src):
    g = grid[["h3", "geometry"]].to_crs(METRIC)
    s = src.to_crs(METRIC)
    s = s[s.geometry.notna() & ~s.geometry.is_empty].copy()
    s["geometry"] = s.geometry.make_valid()
    s["src_area"] = s.geometry.area
    s["src_idx"] = np.arange(len(s))
    inter = g.overlay(s, how="intersection", keep_geom_type=False)
    inter = inter[inter.geometry.area > 0].copy()
    inter["ov_area"] = inter.geometry.area
    return inter


def transfer(grid, src, attributes, prov=None, fonte=""):
    """attributes: dict nome_canonico -> {col, kind, peso?}. Ritorna DataFrame indicizzato per h3."""
    out = pd.DataFrame(index=grid["h3"])
    usable = {}
    for name, spec in attributes.items():
        if spec.get("kind") == "coverage":
            usable[name] = spec
        elif spec.get("col") and spec["col"] in src.columns:
            usable[name] = spec
        elif prov is not None:
            prov.avviso(f"{fonte}: attributo '{name}' saltato (colonna non indicata o assente nel file)")
    if not usable:
        return out
    cols = [s["col"] for s in usable.values() if s.get("col")]
    src2 = src[cols + ["geometry"]].copy() if cols else src[["geometry"]].copy()
    inter = _overlay(grid, src2.reset_index(drop=True))
    cell_area = grid.set_index("h3")["area_m2"]
    for name, spec in usable.items():
        kind = spec["kind"]
        if kind == "coverage":
            cov = inter.groupby("h3")["ov_area"].sum() / cell_area
            out[name] = cov.reindex(out.index).fillna(0).clip(0, 1)
            thr = spec.get("soglia_overlap")
            if thr is not None and name.startswith("c_"):
                out[name] = (out[name] >= thr).astype(int)
            continue
        vals = pd.to_numeric(inter[spec["col"]], errors="coerce")
        frac = inter["ov_area"] / inter["src_area"]
        if kind == "extensive":
            out[name] = (vals * frac).groupby(inter["h3"]).sum().reindex(out.index)
        elif kind == "intensive":
            w = inter["ov_area"]
            peso = spec.get("peso")
            if peso:
                pc = [s["col"] for n, s in attributes.items() if n == peso and s.get("col")]
                if pc and pc[0] in inter.columns:
                    # popolazione stimata nella sovrapposizione = pop del poligono * quota di area
                    w = pd.to_numeric(inter[pc[0]], errors="coerce").fillna(0) * frac
            ok = vals.notna() & (w > 0)
            num = (vals[ok] * w[ok]).groupby(inter.loc[ok, "h3"]).sum()
            den = w[ok].groupby(inter.loc[ok, "h3"]).sum()
            out[name] = (num / den).reindex(out.index)
        else:
            raise ValueError(f"kind sconosciuto: {kind}")
    return out
