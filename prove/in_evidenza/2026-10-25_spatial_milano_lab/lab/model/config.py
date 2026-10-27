"""All parameters of the integrated model (lab/model). Tags: [D] real data / cited source, [A] assumption,
[S] synthetic. One dict per layer. The audit decision rule (AUDIT['rule']) is PRE-REGISTERED: it was written
here before the first audit run and must not be edited after looking at results (see results.md)."""
import os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
ROOT = os.path.dirname(LAB)
MI = os.path.join(ROOT, "mi")                       # read-only
PROP = os.path.join(LAB, "proposals")               # read-only
OUT = os.path.join(HERE, "out")                     # intermediate cache (pickles)
RES = os.path.join(LAB, "results")                  # published outputs
for d in (OUT, RES): os.makedirs(d, exist_ok=True)
for p in ("A_econ_or", "B_decision", "C_ml_spatial"):
    q = os.path.join(PROP, p)
    if q not in sys.path: sys.path.append(q)   # append: our demand.py must win over A's

T0 = time.time()
log = lambda *a: print(f"[{time.time() - T0:6.1f}s]", *a, file=sys.stderr, flush=True)
LON0, LAT0 = 9.19, 45.465

# ---------------------------------------------------------------- sites (review1 §5.2)
SITE = dict(
    a_min_parcel=300.0,   # [A] m2, aggregation fills size
    excl_share=0.5,       # [A] max share of green / agri / water / infra / school land
    excl_cols=["pgt_srv_verde", "pgt_agr", "pgt_pae", "pgt_srv_ist", "dusaf_wat", "dusaf_infra", "dusaf_green", "dusaf_agr", "dusaf_wood"],
    occ_res_share=0.5,    # [A] parcels with volumes and >= 50 % residential volume excluded (no displacement)
    plan_share=0.5,       # [A] tras / srv_erp share that makes a parcel "designated"
    buffer_m=2.0,         # [A] adjacency buffer
    max_area_m2=60000.0,  # [A] split larger components with k-means
    site_min_m2=1500.0,   # [A]
    simplify_m=1.0,       # [A] export geometry (5 m distorted small sites by >2 %)
)
ORIGINS = ["AT", "AMB_DEG", "ERP", "SOFT"]   # priority order; SOFT = non-designated

# ---------------------------------------------------------------- supply / cost (copied from A's SUP; A = assumption)
SUP = dict(far=1.0, yield_=0.70, gfa_dw=80.0, m_min=20, m_max=400, land_inc=0.20, c_build=2000.0, c_demo=25.0)

# ---------------------------------------------------------------- demand (review1 §5.3, coordinator note 2026-10-27)
DEM = dict(
    n_scen=20,            # [A] bootstrap scenarios (A uses 40; 20 for runtime)
    nh=2000,              # households simulated per NIL and scenario
    seed=1,
    tau=0.30,             # [A] normative rent/income ratio (A)
    nh_basket1=1256.37 * 0.60,   # [D/A] ISTAT abs.-poverty single adult, Lombardy metro centre, minus 40 % rent share (A)
    decent_mult=1.5,      # [A] 'decent living' basket = 1.5 x ISTAT non-housing (A, coordinator: D_res_decent)
    lam_km=1.5,           # [A] distance decay of service
    d_max=3.0,            # [A] no service beyond 3 km
    basket_mult=1.0,      # sensitivity multiplier on every basket
    pp_file=os.path.join(PROP, "A_econ_or", "results", "purchasing_power_nil.csv"),
)
# layers: D_tau (A base) | D_res_decent (residual test, 1.5 x ISTAT basket; portfolio layer) |
#         D_res_istat (pure ISTAT residual; reported only, near-empty)

# ---------------------------------------------------------------- SMAA (review1 §5.5; archetypes SYNTHETIC, from B)
CRIT = ["access_metro", "access_jobs", "services", "green_access", "heat", "demand_reach", "rent_burden", "capacity", "cost"]
SMAA = dict(S=20000, K=10, kappa=40.0, seed=1)
# B's archetype means over [access, need, green, heat, capacity, mix, cost]; mix dropped and renormalised,
# access -> access_metro + access_jobs (1/2 each), need -> demand_reach + rent_burden (1/2 each)       [S]
B_ARCH = {"young_worker": [0.30, 0.20, 0.08, 0.07, 0.10, 0.10, 0.15],
          "family_children": [0.12, 0.12, 0.25, 0.15, 0.08, 0.18, 0.10],
          "elderly": [0.25, 0.08, 0.17, 0.30, 0.05, 0.10, 0.05],
          "commuter": [0.40, 0.10, 0.05, 0.05, 0.10, 0.05, 0.25]}


def arch_means():
    out = {}
    for k, (ac, nd, gr, ht, cp, mx, co) in B_ARCH.items():
        v = dict(access_metro=ac / 2, access_jobs=ac / 2, services=0.0, green_access=gr, heat=ht,
                 demand_reach=nd / 2, rent_burden=nd / 2, capacity=cp, cost=co)
        s = sum(v.values()); out[k] = [max(v[c] / s, 1e-3) for c in CRIT]   # services gets a 0.001 floor
    return out

# ---------------------------------------------------------------- portfolios (review1 §5.6)
PORT = dict(
    K=6, delta=0.3, stop_frac=0.85,   # diverse set: each new portfolio shares <= 70 % of sites
    beta=0.5, alpha=0.2,              # (1-beta) mean + beta CVaR_20
    budget=1.0e9,                     # [A] EUR (A)
    kappa=0.03, kappa_erp=0.015,      # [A] NIL caps (A); tighter where srv_erp > 5 % of NIL area
    gini=0.10,                        # lens (d)
    k_per_nil=8,                      # cheapest-per-dwelling sites kept per NIL and per designated/non class (+ all ERP)
    time_limit=30, gap=0.02,
    time_limit_choice=300, gap_choice=0.01,   # review2: P1-P6 and lenses solved to <= 1 % gap (<= 300 s each)
    matched_draws=6, matched_time_limit=60,   # review2: size- / ring-matched non-designated pools vs L_pgt
)

# ---------------------------------------------------------------- audit (review1 §5.7) -- PRE-REGISTERED
AUDIT = dict(
    R=999, seed=7,
    sigma=0.5,            # [A] share of new dwellings allocated to low-income households
    cap_tol=0.05,         # capacity match +-5 %
    n_area_strata=10,     # area deciles
    n_rings=5,            # distance-to-centre quintiles (ring null)
    q_fdr=0.05,
    hh_floor=500,         # [A] review2 (post hoc): NIL with < 500 households get city-mean placement values (CAP-imputed income)
    sets=["AT", "AMB_DEG", "ERP", "RIG"],   # RIG = context only (not in the verdict)
    # 6 indices entering BH, with the HARM direction ('+' = larger is worse for segregation / worse for people)
    bh_indices={"dDI": "+", "dIso": "+", "dep_poor": "+", "dep_resid": "-", "conc_q5": "+", "opp": "-"},
    rule=("PRE-REGISTERED 2026-10-27, before any audit run. For each designated set G in {AT, AMB_DEG, ERP} and each null "
          "N in {size (area-decile + capacity +-5 %), ring (area-decile x centre-distance quintile + capacity +-5 %)}: "
          "one-sided empirical p in the harm direction, p = (1 + #{null at least as harmful as G}) / (R + 1), R = 999. "
          "Benjamini-Hochberg at q = 0.05 over the 4 sets x 6 indices (dDI, dIso, dep_poor, dep_resid, conc_q5, opp) "
          "separately within each null. SEGREGATION-RISK if (dDI or dIso is BH-significant) in BOTH nulls. "
          "REAL-POTENTIAL if served demand per EUR (D_res_decent, else D_tau) >= null median AND opportunity index >= null "
          "median, in BOTH nulls. Label = risk / potential / both / neither. RIG is reported as context, not labelled."),
)

# ---------------------------------------------------------------- sensitivity grid (review1 §5.9.6)
SENS = dict(tau=[0.25, 0.35], basket=[0.85, 1.15], lam_km=[1.0, 3.0], kappa=[0.02, 0.05], far=[0.7, 1.5],
            sigma=[0.3, 1.0], buffer_m=[0.0, 5.0])
SENS_R = 299      # null draws in the sensitivity grid (runtime)

# Disclosed post-hoc changes to the pre-registered specification (after review 2). The rule text above is unchanged;
# these change what the indices measure or how the family is formed. Reported in results.md section 2.
POSTHOC = [
    "conc_q5 now uses the top quintile of p_erp only (the srv_erp arm made it partly tautological for ERP); the old OR definition is reported as conc_q5_or.",
    "Placement indices (poor, for_, net_m, resid, q5 membership) use a household floor: NIL with < 500 households take the city mean (their income is CAP-imputed).",
    "The null pool is all candidate land including G (permutation null), not non-designated land only (review 2 calibration fix).",
    "The BH family is now the stated 4 sets (AT, AMB_DEG, ERP, RIG) x 6 indices; the first runs used 3 sets.",
    "All p-values are one-sided in the harm direction (review1 said two-sided; config said one-sided). Two-sided p are in audit_indices.csv.",
    "NIL-block permutation null added as a co-primary robustness check (reported next to the label, not part of the rule).",
]


def load_prop(proposal, module):
    """Import lab/proposals/<proposal>/<module>.py under a unique name (A's demand.py would shadow ours)."""
    import importlib.util
    name = f"prop_{proposal}_{module}"
    if name in sys.modules: return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, os.path.join(PROP, proposal, module + ".py"))
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m)
    return m
