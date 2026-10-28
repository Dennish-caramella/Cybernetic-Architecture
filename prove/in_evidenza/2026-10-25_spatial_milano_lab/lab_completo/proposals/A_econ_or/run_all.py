"""End-to-end experiment: demand (with bootstrap), demand sensitivity, Pareto portfolios, robustness, FAR sensitivity.
Run from project root:  PYTHONPATH=C:/Temp/pl python lab/proposals/A_econ_or/run_all.py   (~12-15 min)
Requires results/cache/ from prep.py (run once, ~1.5 min)."""
import json, os, sys, time
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import demand, portfolio as PF

RES = os.path.join(HERE, "results"); T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
TL = float(os.environ.get("A_TL", 60))       # MILP time limit per solve (s)

# ---------------------------------------------------------------- 1. demand + bootstrap
R = demand.main(); log("demand done")
S = R["S"]

# ---------------------------------------------------------------- 2. demand sensitivity (deterministic base draw, same seed)
VAR = [("base", {}), ("tau=0.25", dict(tau=0.25)), ("tau=0.35", dict(tau=0.35)), ("tau=0.40", dict(tau=0.40)),
       ("earn_k=0.5", dict(earn_k=0.5)), ("earn_k=1.5", dict(earn_k=1.5)), ("rho=0", dict(rho=0.0)), ("rho=0.6", dict(rho=0.6)),
       ("basket=600", dict(basket1=600.0)), ("basket=900", dict(basket1=900.0)),
       ("ERP boundary w/o rent deduction", dict(isee_rent_ded=0.0)), ("ISEE assets term 3k", dict(isp=3000.0)),
       ("social rent 120 EUR/m2/yr", dict(social_rent=120.0)), ("renter=0.25", dict(renter=0.25)), ("renter=0.35", dict(renter=0.35))]
rows = []
for name, p in VAR:
    r = demand.run(p, n_scen=0, nh=3000, seed=1, quiet=True)
    c = demand.city_stats(r); ic = c.pop("individual_employee_check")
    rows.append(dict(variant=name, **{k: v for k, v in c.items() if not isinstance(v, list)},
                     target_net_p50=(c["target_net_month_p10_p50_p90"] or [np.nan] * 3)[1],
                     emp_share_mkt_fail=ic["share_mkt_fail"], emp_share_erp=ic["share_erp"], emp_share_excluded_not_erp=ic["share_excluded_not_erp"],
                     emp_share_net_1500_2500=ic["share_net_1500_2500"]))
    log("sens", name, round(rows[-1]["D_total_base"]))
pd.DataFrame(rows).to_csv(os.path.join(RES, "sensitivity_demand.csv"), index=False)

# ---------------------------------------------------------------- 3. portfolios (Pareto via epsilon-constraint)
sp = dict(PF.SUP); M = PF.prepare(sp, S)
log("candidates", len(M["L"]), "service pairs", len(M["ps"]), "capacity", int(M["L"].cap.sum()))
M["L"].to_csv(os.path.join(RES, "candidates_far1.0.csv"), index=False)
RUNS = [("P1_budget0.5bn", 0.5e9, None, 0.5), ("P2_budget1.0bn", 1.0e9, None, 0.5), ("P3_budget1.5bn", 1.5e9, None, 0.5),
        ("P4_budget2.5bn", 2.5e9, None, 0.5), ("P5_1.0bn_gini0.15", 1.0e9, 0.15, 0.5), ("P6_1.0bn_gini0.08", 1.0e9, 0.08, 0.5),
        ("R0_1.0bn_expected_only", 1.0e9, None, 0.0)]
summ, NILS, ACC = [], [], {}
for name, B, g, beta in RUNS:
    r, site, nr = PF.solve_portfolio(M, sp, B, beta=beta, gini_max=g, time_limit=TL)
    r.update(portfolio=name, far=sp["far"], n_candidates=len(M["L"]), capacity=float(M["L"].cap.sum())); summ.append(r)
    site.to_csv(os.path.join(RES, f"sites_{name.split('_')[0]}.csv"), index=False)   # short names: Windows MAX_PATH
    NILS.append(nr.assign(portfolio=name)); ACC[name] = nr.set_index("nil_id").access
    log(name, r["status"], r["sec"], "s  dw", round(r["dwellings"]), "served", round(r["served_mean"]), "gini", round(r["gini_cov"], 3))

# supply sensitivity at 1.0 bn: FAR, and Researcher C's PU-learning rank (top 10 % of land parcels) as extra filter
for tag, extra in (("F07", dict(far=0.7)), ("F15", dict(far=1.5)), ("PU10", dict(pu_top=0.10))):
    sp2 = dict(PF.SUP, **extra); M2 = PF.prepare(sp2, S)
    r, site, nr = PF.solve_portfolio(M2, sp2, 1.0e9, time_limit=TL)
    r.update(portfolio=f"{tag}_1.0bn", far=sp2["far"], n_candidates=len(M2["L"]), capacity=float(M2["L"].cap.sum())); summ.append(r)
    site.to_csv(os.path.join(RES, f"sites_{tag}.csv"), index=False)
    log(tag, r["status"], "dw", round(r["dwellings"]), "served", round(r["served_mean"]))

# out-of-sample robustness: re-evaluate fixed allocations on 40 fresh demand scenarios (new seed)
R2 = demand.run(n_scen=40, nh=3000, seed=99, quiet=True)
D2 = R2["S"].pivot(index="nil_id", columns="scen", values="D").reindex(M["ids"]).fillna(0).values
for r in summ:
    if r["portfolio"] in ACC:
        a = ACC[r["portfolio"]].reindex(M["ids"]).fillna(0).values[:, None]
        sv = np.minimum(a, D2).sum(0)
        r.update(oos_served_mean=float(sv.mean()), oos_served_cvar20=float(np.sort(sv)[:8].mean()))
P = pd.DataFrame(summ)
P.to_csv(os.path.join(RES, "portfolios.csv"), index=False)
pd.concat(NILS).to_csv(os.path.join(RES, "portfolio_nil_coverage.csv"), index=False)

# ---------------------------------------------------------------- 4. validation vs external figures
city = json.load(open(os.path.join(RES, "demand_city.json")))
val = dict(
    excluded_share_employees_model=city["individual_employee_check"]["share_excluded_not_erp"],
    excluded_share_employees_model_no_rent_deduction=float(pd.read_csv(os.path.join(RES, "sensitivity_demand.csv")).set_index("variant")
                                                             .loc["ERP boundary w/o rent deduction", "emp_share_excluded_not_erp"]),
    employees_market_fail_model=city["individual_employee_check"]["share_mkt_fail"],
    ansa_ceto_medio_escluso=0.375,
    target_net_income_p10_p50_p90=city["target_net_month_p10_p50_p90"], piano_casa_band=[1500, 2500],
    unmet_demand_households=[city["D_total_p05"], city["D_total_mean"], city["D_total_p95"]], piano_casa_target_dwellings=10000,
    runtime_min=round((time.time() - T0) / 60, 1))
json.dump(val, open(os.path.join(RES, "validation.json"), "w"), indent=1)

# ---------------------------------------------------------------- 5. charts (matplotlib optional)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    q = P[P.portfolio.str.match(r"P\d")]
    fig, ax = plt.subplots(figsize=(6, 4))
    sc = ax.scatter(q.cost_eur / 1e9, q.served_mean, c=q.gini_cov, cmap="viridis_r", s=60)
    for _, r in q.iterrows(): ax.annotate(r.portfolio.split("_")[0], (r.cost_eur / 1e9, r.served_mean), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("cost (bn EUR)"); ax.set_ylabel("expected served target households"); fig.colorbar(sc, label="Gini of NIL coverage")
    ax.set_title("Pareto portfolios (epsilon-constraint)"); fig.tight_layout(); fig.savefig(os.path.join(RES, "pareto.png"), dpi=110)
    d = pd.read_csv(os.path.join(RES, "demand_nil.csv")).sort_values("D_mean", ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(d.name.str[:28], d.D_mean, xerr=[d.D_mean - d.D_p05, d.D_p95 - d.D_mean], color="#4c78a8")
    ax.invert_yaxis(); ax.set_xlabel("unmet target-band renter households (mean, p5-p95)"); fig.tight_layout()
    fig.savefig(os.path.join(RES, "demand_top20.png"), dpi=110)
except ImportError:
    log("matplotlib not available: CSV only")
log("DONE", round((time.time() - T0) / 60, 1), "min")
