"""Step 8: compact JSON for the browser (lab/results/model.json). Site geometry: local km frame (README), polygons
as lists of rings [exterior, holes...], each ring delta-encoded integers in unit 0.0005 km (as mi tiles).
Only sites, portfolios, NIL/hex aggregates: no household-level record."""
import json, os
import numpy as np, shapely
from config import *

U = 0.0005


def enc_ring(coords):
    q = np.round(np.asarray(coords)[:-1] / U).astype(np.int64)
    d = np.diff(q, axis=0, prepend=np.zeros((1, 2), np.int64))
    return d.ravel().tolist()


def dec_ring(a):
    return np.cumsum(np.asarray(a, np.int64).reshape(-1, 2), axis=0) * U


def enc_geom(g):
    g = g.simplify(SITE["simplify_m"] / 1000.0, preserve_topology=True)
    parts = getattr(g, "geoms", [g])
    return [[enc_ring(p.exterior.coords)] + [enc_ring(h.coords) for h in p.interiors] for p in parts if p.geom_type == "Polygon" and not p.is_empty]


def dec_geom(G):
    from shapely.geometry import Polygon
    return shapely.union_all([Polygon(dec_ring(p[0]), [dec_ring(h) for h in p[1:]]).buffer(0) for p in G])


def r4(v):
    return None if v is None or (isinstance(v, float) and not np.isfinite(v)) else round(float(v), 4)


def write(o, pcrit, sens=None, runtime_min=None):
    S, X, raw = o["S"], o["X"], o["raw"]
    sid = [f"S{i:04d}" for i in range(len(S))]
    sites = [dict(id=sid[i], o=S.origin[i], at=S.at_name[i], nil=int(S.nil_id[i]), a=int(round(S.area_m2[i])), cap=int(S.cap[i]),
                  g=enc_geom(S.geom[i]), x=[r4(v) for v in X.values[i]], raw=[r4(v) for v in raw.values[i]],
                  dem=[r4(S.dem_mean[i]), r4(S.dem_p05[i])],
                  acc=dict(b1=r4(S.b1[i]), top10=r4(S.top10_uniform[i]), hol=r4(S.hol[i]), min_arch=r4(S.min_arch[i]),
                           gic=r4(S.gic_arch[i]), arch={a: r4(S[f"top10_{a}"][i]) for a in arch_means()}),
                  rent_g=r4(S.rent_g[i]))
             for i in range(len(S))]
    ports = [dict(id=p["id"], lens=p["lens"], sites=[sid[j] for j in p["sites_idx"]],
                  dw=[int(round(v)) for v in p["built"][p["y"]]],
                  served=[r4(p["r"].get("served_mean")), r4(p["r"].get("served_cvar"))], gini=r4(p["r"].get("gini_cov")),
                  cost=r4(p["r"].get("cost_eur")), gap=r4(p["r"].get("gap")), status=p["r"].get("status"),
                  eval={l: [r4(v["served_mean"]), r4(v["served_cvar"])] for l, v in p["eval"].items()},
                  audit={k: r4(v) for k, v in p["audit"].items()}, smaa=dict(b1=r4(p.get("smaa_b1")), top3=r4(p.get("smaa_top3"))),
                  designated_share=r4((S.origin.values[p["sites_idx"]] != "SOFT").mean() if len(p["sites_idx"]) else None),
                  optimal=p["r"].get("status") == "Optimal")
             for p in o["P"]]
    import report as RP
    CL = RP.claims(o, sens)
    clean = lambda v: {kk: clean(vv) for kk, vv in v.items()} if isinstance(v, dict) else [clean(x) for x in v] if isinstance(v, list) else (r4(v) if isinstance(v, (float, np.floating)) else v)
    aud = {g: dict(label=o["labels"].get(g, "context"), claim_it=CL[g]["claim_it"], claim_en=CL[g]["claim_en"],
                   key_numbers=clean(CL[g]["numbers"]), caveats=CL[g]["caveats"],
                   **{n: {k: {kk: r4(vv) for kk, vv in v.items()} for k, v in r.items()} for n, r in d.items()},
                   match={n: r4(o["match"][(g, n)]) for n in d})
           for g, d in o["res"].items()}
    hn = __import__("pandas").read_csv(os.path.join(PROP, "C_ml_spatial", "results", "hex_need.csv"))
    regions = [[r4(a), r4(b), c, r4(d), e] for a, b, c, d, e in zip(hn.x, hn.y, hn.region, hn.pressure, np.where(hn.sig_fdr05, hn.lisa_quad, ""))]
    J = dict(meta=dict(version="1", unit_km=U, crs="local km: x=(lon-9.19)*KX, y=-(lat-45.465)*KY (README), y south",
                       geom="sites[].g = polygons; each polygon = [exterior, holes...]; ring = delta ints x unit_km",
                       pp_layer="ok" if o["pp_ok"] else "missing", demand_layer=o["layer"], runtime_min=runtime_min,
                       params=dict(SITE={k: v for k, v in SITE.items() if k != "excl_cols"}, SUP=SUP,
                                   DEM={k: v for k, v in DEM.items() if k != "pp_file"}, PORT=PORT,
                                   AUDIT={k: v for k, v in AUDIT.items()}),
                       data_status=dict(real="parcels, PGT, DUSAF, census hex, IRPEF 2024 by CAP, OMI 2019-2024, ISTAT basket",
                                        assumption="FAR, yield, cost, tau, basket share, renter share, sigma, kappa, lambda",
                                        synthetic="archetype weight distributions (B); simulated households are a model, not records"),
                       counts=o["counts"]),
             criteria=o["cspec"], sites=sites, portfolios=ports, portfolio_criteria=pcrit, audit=aud,
             people_vs_pgt=clean({k: v for k, v in CL.get("people_vs_pgt", {}).items()}),
             posthoc_changes=POSTHOC, rule=AUDIT["rule"],
             archetypes=[dict(k=k, synthetic=True, mu=[round(v, 4) for v in mu]) for k, mu in arch_means().items()],
             regions=dict(keys=["x", "y", "region", "pressure", "lisa_fdr"], hex=regions),
             sensitivity=None if sens is None else sens.to_dict("records"))
    s = json.dumps(J, separators=(",", ":"), default=lambda v: v.item() if hasattr(v, "item") else str(v))
    open(os.path.join(RES, "model.json"), "w", encoding="utf-8").write(s)
    log("model.json", round(len(s) / 1e6, 2), "MB")
    return J
