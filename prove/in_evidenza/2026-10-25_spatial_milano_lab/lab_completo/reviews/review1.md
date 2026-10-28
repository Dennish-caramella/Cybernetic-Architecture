# Peer review 1: proposals A, B and C, plus the integration spec

Reviewer: methodological referee. Date: 2026-10-27.
Evidence: every reviewer number below comes from `lab/reviews/review1_checks.py`, run with `PYTHONPATH=C:/Temp/pl python lab/reviews/review1_checks.py` (about 7 s, read-only), from re-runs named in each section, or from the proposals' own result files.

## 0. Verdict in one paragraph

All three proposals are honest, and most of their headline numbers reproduce. None of them, as written, answers the owner's question: does overlaying people's needs on PGT-designated areas create segregation, or do those areas have real potential?

- **A** has a rigorous supply and portfolio optimiser. Its demand indicator, however, is ~99 % a rent map: Spearman ρ = 0.987 between the NIL target rate and the NIL OMI rent. That is an artefact of income resolved at only 38 CAP while rent is resolved at 88 NIL.
- **B** has a sound preference and SMAA engine. Its candidate pool lets park land through: 31 of its top-100 parcels lie inside the PCU parks, including one of the four "consensus" parcels (Parco Forlanini, 55 % farmland).
- **C** has the most careful validation. It also holds the strongest segregation evidence, but reports it without a sign. Re-signed, it shows designated sites sit in NIL with **more** foreign residents (27.8 % vs 21.7 %) and **more** poor taxpayers (31.9 % vs 29.3 %). One headline number in C's docs does not match its own result file.

The three "need" indicators also disagree. A's need is **anti-correlated** with B's and C's (ρ = −0.25 and −0.20 across 82 NIL), while B and C are near-identical (ρ = 0.94). The integration must therefore keep need as an explicit, plural layer and must not average the three.

---

## 1. Proposal A: econ / OR

### Strengths
- Grouped-data MLE with a class-exact hybrid sampler and a Pareto top. Tax calibration per CAP is stable (0.83–0.93).
- It separates normative parameters (τ, ERP rule, social rent) from epistemic ones (bootstrap). This is the right design.
- The MILP is clean: robust mean + CVaR₂₀, an exactly linear demand-weighted Gini ε-constraint, and NIL concentration caps κ that are tighter where srv_erp > 5 %. The κ cap is the only anti-segregation constraint in any proposal.
- It removes the PCU parks and does not use rig/dism as a site signal (adopted from C).
- It reports solver gaps and admits that differences under 2 % are noise.

### Methodological flaws (most severe first)
1. **Demand ≈ rent map (severe).** ρ(D_i/H_i, rent_i) = 0.987 over the NIL; ρ with % poor is −0.385. The income distribution comes from the household's CAP mix. Milan has 38 CAP and 88 NIL, and central NIL share the same few CAP. The NIL-level variation in P(TARGET) is therefore driven almost only by r_i. Two consequences:
   - "Demand is concentrated in central NIL" is close to a tautology of the design, not a finding.
   - The test applies today's market rent to incumbent households, most of whom hold older contracts or own their home. It measures *entry* affordability for a household with the CAP income profile. It does not measure the displacement of residents. The "displacement pressure" label is unsupported.

   **Fix:** report the decomposition. Re-run D_i with r_i replaced by the city median rent. The share of between-NIL variance that remains is the part due to income. Also run a city-wide search variant, where each household fails only if it fails in the cheapest NIL within 30 min. A's own limitation 4 admits this would give "much less".
2. **ERP share of 46 % (severe for interpretation).** The ISEE proxy with the full rent deduction and ISP = 0 makes almost half of Milan "ERP-eligible if renting". TARGET is the residual above this very low boundary, so it is fragile: it multiplies by ×2.6 without the deduction. **Fix:** present the τ × ERP-boundary grid as the main result, not as sensitivity, and add the purchasing-power layer (§4.3).
3. **GREY is empty, and the residual-income test never binds.** With b = 750 €/month for one adult, the residual test is dominated by τ = 0.30 everywhere. This means the basket is too low for Milan, not that the test is irrelevant. The ISTAT absolute-poverty basket for a single adult (18–59) in a north-Italian metropolitan centre is about 1,100–1,250 €/month in 2024 (to be verified in A's `purchasing_power.py`). Raising it will likely populate GREY and move demand toward low-income, lower-rent NIL. **This is the main change the purchasing-power addendum must test.**
4. **θ = 0.30 is flat across NIL.** Tenure is strongly income-graded. A flat θ inflates central demand, where ownership is higher, relative to poor NIL. Use Census 2021 tenure (owner / renter dwellings by section) if `istat_samples` holds it; otherwise state the bias direction in every output.
5. **Distance to the NIL polygon** is used as the service distance. A site 10 m outside a large NIL gets w = 1 for its whole population. Use the population-weighted hex distance from C's hex grid.
6. **No adjacency aggregation.** The 1,500 m² parcel threshold and the per-parcel 400-dwelling cap ignore that adjacent parcels form one site.
7. **Time-limit solves** (P2, P3, P4 and P6 stopped at 1.3–3.6 % gap). This is acceptable, but the Pareto "front" is not certified. Give solve time and gap per point in every published chart.

### Unsupported or overstated claims
- "The indicator therefore measures displacement pressure": see flaw 1.
- "Budget is the binding constraint, not land": shown only for FAR 0.7–1.5 on the same pre-screened 12-per-NIL pool. The pre-screen itself caps land.
- "The Piano Casa target of 10k dwellings is close to the estimated demand": demand is defined with the same τ that drives it ×6 (τ 0.25–0.40). The match is coincidental.

### Reproduced (from result files, A not re-run: 9 min)
| claim | file value | status |
|---|---|---|
| D mean / p5 / p95 = 10.5k / 4.35k / 19.26k | `validation.json` 10,503 / 4,346 / 19,259 | ✔ |
| τ: 25.3k / 9.8k / 4.1k | `sensitivity_demand.csv` 25,335 / 9,794 / 4,120 | ✔ |
| P2 served 3,845, CVaR 3,643, Gini 0.29, NIL 26 | `portfolios.csv` 3,845.4 / 3,643.2 / 0.294 / 26 | ✔ |
| P6 Gini 0.08, NIL 41, −3.5 % service | 0.080 / 41 / (3,845−3,712)/3,845 = 3.5 % | ✔ |
| OOS CVaR P2 3,646 vs EV 3,529 | 3,646.5 / 3,529.4 | ✔ |
| PU10 cuts service by 10 % | 3,475 / 3,845 = −9.6 % | ✔ |
| Dagum 36 / LN 2 | `demand_city.json` | ✔ |

Reviewer finding (new): P2's dwelling-weighted NIL % poor is 28.99, against 29.02 household-weighted for the city. Its % foreign is 18.3, against 21.0. A's portfolios therefore **do not** concentrate in deprived NIL. 43 % of P2 dwellings fall in the 10 NIL with the highest demand, and those NIL hold 56 % of demand. Only 12 % of dwellings are on srv_erp land.

### Required fixes
F-A1: rent/income variance decomposition and the city-wide-search variant. F-A2: residual-income band using the ISTAT basket (§4.3). F-A3: tenure gradient or a stated bias. F-A4: hex-based service distance. F-A5: consume the integrated site table (adjacency aggregated) instead of single parcels.

---

## 2. Proposal B: decision / participation engine

### Strengths
- It treats preferences as distributions and publishes acceptability rather than a single winner. This matches the owner's request for "a set, not the best".
- The dominance-depth reduction is exact for top-k statistics (it holds with any tie-break that respects dominance). The self-check passes.
- Bayesian pairwise learning uses correct MH on the simplex. EIG-top is a good decision-focused idea, and the negative result on misspecified β is reported.
- The E3 minority audit and the E4 JR audit are exactly the guards against majority amplification the project needs.
- The teach-back LP is correct, including the infeasible-when-dominated case.

### Methodological flaws (most severe first)
1. **Park land in the pool (severe).** `candidate_pool` admits `max(pgt_rig, pgt_dism, pgt_tras) > 0.3`. This does not exclude the PCU parks, and it uses the rig/dism zone layer that C showed is not a site signal. Reviewer check:
   - 31 of the top-100 parcels by holistic acceptability are inside PCU ambiti.
   - 22 of the top-100 are ≥ 50 % DUSAF green or agricultural.
   - 1 of the 4 E5 "consensus" parcels (039600.314 Parco Forlanini, 55 % DUSAF agricultural) is PCU, and so are 039700.144 (Forlanini) and 016400.116 (Bosco in Città) in the top-10.
   - Parcel 024100.57 (rank 7) is 100 % DUSAF "parchi e sport".

   **Fix:** use the integrated candidate filter (§4.2).
2. **The green criterion rewards being inside a park.** `green = ½ nil_green + ½ (1 − green_srv_km)` gives the maximum to parcels at 0 km, that is, inside PGT green. Combined with flaw 1, this pushes parks to the top. **Fix:** use C's A_green E2SFCA (rank) and, separately, a hard exclusion of green land.
3. **NIL-level criteria (4 of 7) create ties and clusters.** 23 of the top-100 are in Cimiano and 20 in Bosco in Città. Aggregation into sites and portfolio diversity constraints are required (B says so itself).
4. **"Need" = rent·60 / net income per taxpayer** is a NIL ratio of a mean rent to a mean per-taxpayer income. It is not a household measure. It is anti-correlated with A's TARGET rate (ρ = −0.25), so "need" means opposite things in A and B. Rename it **rent-burden index** and add A's demand as a separate criterion (§4.4).
5. **"mix" = −nil_poor is a deconcentration criterion that citizens can weight to zero.** Segregation risk must be an **audit and a constraint**, not a tradeable criterion. Keep the criterion if citizens want it, but enforce κ caps outside the weights.
6. Minor:
   - The confidence factor uses criteria noise, which breaks the exactness of the dominance filter for that statistic. This is harmless but undocumented.
   - Particle count was not checked.
   - The teach-back example differs between `summary.md` (5.1 → 12.8 %) and `model.md` (11.5 → 12.2 %). Give the source run for each.

### Unsupported claims
- "Two parcels are robust across all archetypes": true in the file (0.839 and 0.763), but both sit in one NIL and one is next to a PCU park. Robustness here partly reflects the green artefact.
- E2–E5 results are on synthetic respondents. B labels this correctly. Nothing about real citizens follows from them.

### Reproduced
| claim | value | status |
|---|---|---|
| `python engine.py` self-checks | "self-checks ok [0.55 0.24 0.06 0.15]", 13 s | ✔ (re-run) |
| pool 11,429 → 3,723 (76 NIL); 123 ever-first | `e1_summary.json`; CSV: 3,723 rows, 76 NIL, 123 with b1 > 0 | ✔ |
| best holistic 0.383, P(top-10) 0.50, conf 0.28 | 0.3833 / 0.502 / 0.283 | ✔ |
| robust-for-all 0.84 / 0.76 | 0.839 / 0.763 | ✔ |
| Cimiano 23, Bosco 20 in top-100 | 23 / 20 | ✔ |
| E2 low-noise TV@25: 0.181 / 0.091 / 0.118 | 0.1808 / 0.0909 / 0.1179 | ✔ |
| flip-20 % regret10: 0.051 vs 0.155 | 0.0508 / 0.155 | ✔ |

### Required fixes
F-B1: consume the integrated candidate set (no PCU, no green ≥ 0.5, sites not parcels). F-B2: replace the green and need criteria (§4.4). F-B3: move mix out of the weights into constraints and audit. F-B4: run SMAA on **portfolios** as well as sites (§4.6).

---

## 3. Proposal C: ML / spatial

### Strengths
- The label audit is an important finding for the whole lab:
  - dism ≡ rig (r = 0.998, 1,657 of 1,716 "ex AR_RIG");
  - rig is zone-wide (36.8 km²);
  - PCU parks dominate tras.
- Spatial-block CV, object-level recall, residual Moran and a calibration warning are exemplary. The random-CV optimism (0.93 → 0.33) is shown honestly.
- The fairness ablation is the **first quantitative segregation signal** in the lab.
- E2SFCA is used only where it adds information (schools, services, green), with the redundancy shown.
- Rejecting the neural surrogate is a correct and well-argued negative result.

### Methodological flaws (most severe first)
1. **Univariate AUC is unsigned (severe for the research question).** `pu.py` l.179 reports |AUC − 0.5| + 0.5, so the direction is lost. Reviewer re-signed values on C's own labels:
   - AUC(nil_for_) = **0.711**: designated parcels lie in NIL with more foreign residents (mean 27.8 % vs 21.7 %).
   - AUC(nil_poor) = **0.697**: more poor taxpayers (31.9 % vs 29.3 %).
   - AUC(nil_net_m) = 0.344: lower income.
   - AUC(metro_km) = 0.654: farther from metro.
   - AUC(hex_pop) = 0.217: sparsely populated cells.

   So the past designations (non-PCU AT + AMB_DEG) sit disproportionately in poorer, more foreign, less metro-served NIL. That is a real segregation-risk *signal*. It is still parcel-weighted and NIL-ecological, and it is not yet tested against a size-matched null (§4.7).
2. **Doc / result mismatch.** `summary.md` and `model.md` report global Moran's I = 0.406. `results/regions_summary.json` (re-generated identically by the reviewer) says **0.57**. Correct the docs, or explain whether 0.406 came from a different weight matrix.
3. **The hex income model varies only through % tertiary education** (b = 2.763, R² 0.75 across 81 NIL). Sub-NIL "need" is therefore an education map scaled to the NIL mean. C admits this. The HH clusters (Cimiano, Barona, Corvetto) are plausible, but the 195-region partition explains a modelled quantity. It must be labelled "modelled" in the UI.
4. **Need index definition.** rent·50 / net per taxpayer is the same construction as B (ρ = 0.94 at NIL level) and opposite to A. See §4.4.
5. **The jobs proxy** (non-residential GFA) mixes warehouses and offices. It is useful as a rank only, as C says.
6. PU labels: about 83 objects, and SCAR is violated. C states both. For integration, the PU score is an **analyst lead list only**. It must never be a criterion, because it would import the socio-economic bias C just found.

### Reproduced
| claim | value | status |
|---|---|---|
| `regions.py` re-run | 11 s; `hex_need.csv` and `regions_summary.json` byte-identical to the committed files | ✔ deterministic |
| LISA 377 raw / 193 FDR (74 HH, 111 LL); HH pop 63,026 | identical | ✔ |
| max-p 195 regions, R² 0.868 vs 0.495, ARI 0.709 / 0.631 | identical | ✔ |
| global Moran's I 0.406 | file says 0.57 | ✘ **mismatch** |
| main PU PR-AUC 0.099, ROC 0.737, recall@10 % 0.501 | `pu_metrics.json` | ✔ |
| soft_site PR-AUC 0.015 | ✔ | ✔ |
| AUC % foreign 0.711, % poor 0.697 | re-signed 0.711 / 0.697 (same magnitude, direction = higher in designated) | ✔ + sign added |

### Required fixes
F-C1: report signed AUCs and the positive/unlabelled means. F-C2: fix the Moran's I in the docs. F-C3: deliver per-parcel A_school / A_services / A_green / cum_jobs_5km as a clean table for the integrator (the `access_parcels.csv.gz` columns are fine). F-C4: export the max-p regions with geometry (hex ids → region) for the UI.

---

## 4. Cross-proposal inconsistencies

| topic | A | B | C | resolution |
|---|---|---|---|---|
| candidate pool | land ≥ 1,500 m², no PCU, no occupied housing, soft_site or (non-PCU tras or srv_erp) ∧ far_ratio < 1; pre-screen 12/NIL → 845 | land ≥ 1,000 m², soft_site or rig/dism/tras > 0.3, **PCU not excluded** → 11,429 | soft_site (15,718) for access; PU top-200 ≥ 2,000 m², no PCU | one filter, §4.2 |
| unit | parcel | parcel | parcel / hex | **site** = adjacency cluster |
| "need" | TARGET households (entry affordability, ≈ rent map) | rent·60 / net (NIL) | rent·50 / modelled hex net | keep **three named layers**: `demand_target` (A), `rent_burden` (B/C, one of them), `res_income_gap` (purchasing power, new) |
| rig/dism | not a signal | used as a pool gate | not a signal (finding) | drop as a signal; keep only as an audit category |
| green | exclusion ≥ 0.5 | criterion (rewards parks) | E2SFCA | E2SFCA + exclusion |
| heat vs green | — | both criteria | ρ = −0.87, weight only one | heat stays as a criterion, green access as E2SFCA; NIL green index dropped |
| PCU test | point-in-poly, `"PCU" in NOME_AMB` | none | `"(PCU" in NOME_AMB` | use A's `pcu_mask` (6 polygons) |
| distance | to NIL polygon | Euclidean to metro | Euclidean, Gaussian | hex-population-weighted Euclidean; network later |

---

## 5. Integration design: `lab/model/`

Goal: produce **sets of candidate sites and several alternative portfolios** for citizens to compare. Then audit the PGT-designated areas against people's needs and against matched counterfactual sites. Never output a single best parcel. Never score households.

### 5.0 Files

```
lab/model/
  config.py          all parameters, each tagged [D]/[A]/[S]; one dict per layer
  sites.py           parcels -> candidate parcels -> adjacency sites (step 1-2)
  criteria.py        site criteria matrix (step 3)
  demand.py          thin wrapper: imports A's demand.py + purchasing_power.py, returns NIL x scenario tables (step 4)
  smaa.py            imports B's engine (smaa, dominance_depth, PrefLearner, flip_l1) (step 5)
  portfolios.py      diverse portfolio generation (step 6), reuses A's LP builder / HiGHS
  audit.py           PGT-vs-people segregation + potential audit with nulls (step 7)
  export.py          compact JSON for the browser prototype (step 8)
  run.py             end-to-end, writes lab/model/out/
  tests/test_model.py   synthetic recovery, invariants, sensitivity (section 5.9)
```
Imports from `lab/proposals/*` only; nothing written to `mi/`.

### 5.1 Data (step 0)
`lab/data/parcels.csv.gz` (land only), `nil.csv`, `mi/out/core.json` (hex, metro, NIL rings), PGT raw geojson (AT with names, AMB_DEG), C's `access_parcels.csv.gz` and `hex_need.csv`, A's `demand_scenarios.csv` and `purchasing_power*`.

### 5.2 Candidate parcels and sites (`sites.py`)
**Parcel filter** `candidate_parcels(P)`:
- kind == land, not outside_city, area ≥ 300 m², the aggregation fills size;
- max(pgt_srv_verde, pgt_agr, pgt_pae, pgt_srv_ist, dusaf_wat, dusaf_infra, dusaf_green, dusaf_agr, dusaf_wood) < 0.5;
- not `pcu_mask`;
- not (n_vol > 0 ∧ use_res_share ≥ 0.5) (no displacement of residents);
- and (soft_site **or** non-PCU tras ≥ 0.5 **or** srv_erp ≥ 0.5 **or** AMB_DEG point-in-polygon);
- rig/dism are **not** an entry condition.

**Adjacency aggregation** `build_sites(cand, buffer_m=2, max_area_m2=60000)`:
1. Decode the candidate parcel polygons (tile decoder in C's `common.poly`).
2. Buffer each by 2 m.
3. Build an STRtree graph with an edge where the buffered polygons intersect **and** both parcels share the same `origin` class: designated-AT / AMB_DEG / srv_erp / soft-only. Sites never mix designated and non-designated land, so the audit can compare them.
4. Take connected components. Split any component above `max_area_m2` with k-means on centroids into ⌈area/max⌉ parts.
5. Keep sites ≥ 1,500 m².

Site attributes:
- area, geometry (union, simplified 5 m);
- `origin`, plus `at_name` where applicable;
- area-weighted parcel attributes;
- `cap = min(floor(0.70·FAR·area/80), 400)` with FAR from config ([A] 1.0);
- `cost` as in A §4;
- `nil_id` of the largest part;
- `hex_ids` within 500 m.

**Test:** the total site area equals the sum of the member parcel areas (±0.1 %), and no parcel is in two sites.

### 5.3 Demand and purchasing power (`demand.py`)
Per NIL i and scenario ω, three demand layers. All are NIL × Ω arrays from A's bootstrap.

1. `D_tau[i,ω]`: A's TARGET with τ-ratio (existing).
2. `D_res[i,ω]`: **residual-income band** (new, from A's `purchasing_power.py`):
   - Y_real = Y_nom · (CPI_NIC_Milano_2019 / CPI_NIC_Milano_2025) when incomes are 2019-based. IRPEF 2024 is already nominal 2024: deflate to a common year.
   - residual = Y/12 − R_market(i, s) − B_ISTAT(s, age mix, "Nord, centro area metropolitana") − C_commute(i).
   - fail_res ⇔ residual < 0.
   - TARGET_res = ¬ERP ∧ fail_res(market) ∧ ¬fail_res(social rent).
3. `D_entry_city[ω]`: the city-wide search variant (fail only if fail in all NIL within 30 min). It is used as a scalar and for the audit.

**Interface A must deliver** (`lab/proposals/A_econ_or/results/purchasing_power_nil.csv`, one row per nil_id × scen), with columns:
- `nil_id, scen, hh`;
- `p_erp`;
- `p_target_tau`, `p_target_res`, `p_grey_res`;
- `D_tau`, `D_res`;
- `resid_p10`, `resid_p50` (€/month, real 2025, among non-ERP renters);
- `basket_eur_m` (ISTAT absolute-poverty basket used, by household size, mean);
- `price_level_idx` (Milan vs Italy, scalar or by NIL);
- `cpi_factor_2019_2025`;
- `commute_eur_m` (assumption: ATM 39 €/month pass, or 0 inside the metro-served area).

A scalar JSON `purchasing_power_city.json` holds the sources: ISTAT basket year and value, NIC index values, the Milan/Italy price-level source.

Until it exists, `demand.py` falls back to `D_tau` only and flags `pp_layer: missing` in the export.

**Site-level demand served** (used by criteria and audit):
- w_{s,h} = exp(−d_{s,h}/λ) · 1[d ≤ 3 km], with h ranging over hex cells.
- Hex demand is NIL demand distributed by hex population: D_h = D_i · pop_h / pop_i.
- `dem_reach[s] = Σ_h w_{s,h} D_h` (expected over Ω, plus p05).
- This replaces A's distance to the NIL polygon.

### 5.4 Criteria (`criteria.py`)
Site-level and benefit-oriented. Robust min-max on p2–p98 of the **site** pool, with the raw value kept for teach-back.

| key | definition | source |
|---|---|---|
| `access_metro` | −metro_km (site centroid) | data |
| `access_jobs` | cum_jobs_5km (rank) | C |
| `services` | rank mean of A_school, A_services (E2SFCA) | C |
| `green_access` | A_green (E2SFCA, rank; winsorised) | C |
| `heat` | −nil_heatrisk | data |
| `demand_reach` | `dem_reach` using D_res if available, else D_tau | A + PP |
| `rent_burden` | NIL rent·60/net_m (B's need, renamed) | B |
| `capacity` | log cap | A |
| `cost` | −cost per dwelling | A |

`mix` is **not** a criterion. It goes to constraints (κ) and to the audit. The PU score is **not** a criterion: it is analyst-only and biased (C F-1).

### 5.5 SMAA and learning (`smaa.py`)
- Reuse B's `dominance_depth`, `smaa`, `PrefLearner`, `flip_l1`, `flip_single` unchanged on the site matrix.
- Weight distributions: uniform Dir(1), plus B's 4 archetypes re-expressed on the new criteria. Mapping:
  - access → access_metro + access_jobs (½ each);
  - need → demand_reach + rent_burden (½ each);
  - green → green_access;
  - mix → dropped, its mass renormalised.
- Outputs per site: `b1`, `top10`, `holistic`, `top10_min_arch`, `gic_arch`.
- Archetypes stay labelled SYNTHETIC.

### 5.6 Portfolio set generation (`portfolios.py`)
This is the citizens' choice set: K diverse alternatives, not one optimum.
- Base model: A's MILP. Sites replace parcels. The objective is (1−β)·mean + β·CVaR₂₀ of served `D_res` (or `D_tau`), with the κ caps.
- **Diversity by integer cuts:** after portfolio p_k with open set S_k, add Σ_{s∈S_k} y_s ≤ (1 − δ)|S_k| (δ = 0.3), so each new portfolio shares ≤ 70 % of the sites. Generate K = 6. Stop early if service drops below 85 % of p_1.
- **Policy lenses:** one portfolio each with
  - (a) `origin ∈ designated` only ("PGT as is");
  - (b) non-designated only ("people's alternative");
  - (c) unconstrained;
  - (d) Gini ≤ 0.10;
  - (e) the archetype-SMAA-weighted objective, max Σ_s y_s·cap_s·holistic_s subject to the same budget, as the participatory lens;
  - (f) D_tau vs D_res demand definition.
- Each portfolio is evaluated on all criteria, all demand layers and the audit (§5.7).
- Portfolio-level SMAA: rank the K + lens portfolios with B's `smaa` on the portfolio criteria matrix: served mean, CVaR, Gini, mean criteria of the sites, audit indices.
- Solver: HiGHS, 60 s, gap 2 %. Report the gap per portfolio.

### 5.7 PGT-vs-people audit (`audit.py`)
**Units.** Designated sets G_d:
- `AT` (non-PCU AT sites);
- `AMB_DEG`;
- `ERP` (srv_erp sites);
- `RIG` (the rig zone, reported as context only).

Alternative sets G_a:
- the people's lens portfolio (b);
- the top-N by holistic acceptability among non-designated sites, with N matched in capacity.

For each set G with total capacity K_G, assume it is built with social / ERP dwellings at its capacity. Compute:

**(a) Segregation risk**
1. *Deprivation placement*: capacity-weighted mean of NIL `poor`, `for_`, `net_m`, `resid_p10` (PP), and the C hex pressure. Report the difference from the city household-weighted mean.
2. *Post-build dissimilarity* across NIL (Duncan):
   - DI = ½ Σ_i | L_i/L − O_i/O |;
   - L_i = existing low-income households (H_i·p_erp_i) plus new dwellings in i allocated to low-income (share σ = 0.5 [A]);
   - O_i = other households.
   - Report ΔDI = DI_post − DI_now. Positive = more segregation.
3. *Isolation* of low-income households: xPx* = Σ_i (L_i/L)(L_i/H_i). Report Δ.
4. *Concentration*: the share of new capacity in NIL already in the top quintile of p_erp or of existing srv_erp share. Also the number of NIL where new + existing ERP exceeds κ.
5. *Opportunity exposure*: capacity-weighted mean of access_jobs, services, metro_km, green_access, heat. Also commute-cost erosion = residual-income loss from commute_eur_m (PP).
6. *Real-income placement* (PP addendum): Do sites go where households' real residual income is lowest, as an anti-displacement score? Or do they push residents to where commute and living costs erode it? Two measures:
   - `served_low_resid` = Σ_s Σ_h w_{s,h}·D_res_h·1[resid_p10_h in the bottom tercile] / Σ (served share to the lowest-resid areas);
   - `resid_erosion_s` = commute_eur_m(s) + (rent at s − rent at origin NIL), summed over the served demand.

**(b) Real potential**
- served `D_res` and `D_tau` (mean, CVaR) with the λ decay;
- fraction of city demand within 3 km;
- mean holistic acceptability and min archetype top-10 of the sites;
- the C need-region coverage: share of FDR-HH hex population within 1 km.

**Null / counterfactual.** For each designated set G_d, draw R = 999 random **size- and capacity-matched** site sets from the non-designated candidate sites:
- stratified by area decile;
- same number of sites;
- total capacity within ±5 %;
- optionally constrained to the same distance-to-centre ring distribution (second null).

For each index I compute:
- the z-score z = (I(G_d) − mean_null)/sd_null;
- the empirical p = (1 + #{I_null ≥ I(G_d)})/(R + 1), two-sided;
- the percentile.

The ring-matched null separates "designated land is peripheral" from "designated land is placed in poor areas *given* its periphery".

Also report the policy-lens portfolios (a) vs (b) on the same indices. This is the headline "PGT vs people" table.

**Verdict rule** (stated before running, to prevent p-hacking): a designated set is "segregation-risk" if ΔDI or ΔIsolation exceeds the null 95th percentile in **both** nulls. It is "real potential" if served D_res per € is ≥ the null median and opportunity exposure is ≥ the null median. A 2 × 2 table yields one of four labels. Apply Benjamini–Hochberg across the 4 sets × 6 indices.

### 5.8 Export for the browser (`export.py` → `lab/model/out/model.json`, target < 3 MB gzip)
```json
{"meta":{"version":"1","unit_km":0.001,"crs":"local km (README)","params":{...},"data_status":{...},"pp_layer":"ok|missing"},
 "criteria":[{"k":"access_metro","label":"...","dir":1,"raw_unit":"km","q02":..,"q98":..}],
 "sites":[{"id":"S0001","o":"AT|AMB_DEG|ERP|SOFT","at":"Scalo Farini|null","nil":71,"a":4814,"cap":42,
           "g":[dx0,dy0,...],            // delta-encoded ring, 1 m units
           "x":[...criteria 0-1...],"raw":[...],"dem":[mean,p05],
           "acc":{"b1":..,"top10":..,"hol":..,"min_arch":..}}],
 "portfolios":[{"id":"P_c1","lens":"unconstrained|pgt|people|gini|smaa|res","sites":["S0001",...],
                "served":[mean,cvar],"gini":..,"cost":..,"gap":..,"audit":{...},"smaa":{"b1":..,"top3":..}}],
 "audit":{"sets":{"AT":{"I":{"dDI":..,"dIso":..,"poor":..,...},"null_size":{"mean":..,"sd":..,"p":..},
                        "null_ring":{...},"label":"risk|potential|both|neither"}}},
 "archetypes":[{"k":"young_worker","synthetic":true,"mu":[...]}],
 "regions":{"hex":[[x,y,region,pressure,lisa]]}}
```
The browser does exact WLC and Monte-Carlo SMAA in a Web Worker (C showed 0.18 ms per full scoring). The learner (PrefLearner) is ported later.

### 5.9 Tests the integrator must pass (`tests/test_model.py`, all < 2 min)
1. **Synthetic ground-truth recovery (audit).** Build a synthetic city with 40 NIL. Plant a designated set inside the 20 % poorest NIL.
   - `audit` must flag ΔDI > null p95, with p < 0.01.
   - Plant a random designated set: the false-positive rate over 50 replications must be ≤ 0.10.
2. **Synthetic recovery (portfolio).** On a toy instance with a known optimum (5 sites, 3 NIL, brute force), the MILP must equal the brute force. Each diversity cut must reduce overlap to ≤ 70 %.
3. **Synthetic recovery (learning).** B's self-check, plus: on site criteria, a known w is recovered with TV < 0.15 after 25 EIG questions (low noise).
4. **Invariants.**
   - No PCU and no ≥ 0.5 green/agricultural parcel in any site.
   - No parcel is in two sites.
   - The Σ site area equals the parcel sum.
   - Served ≤ demand per NIL and scenario.
   - κ is respected.
   - Budget is respected.
   - Acceptabilities b[:, r] sum to 1.
   - Dominance-filtered sites have zero top-k acceptability.
   - Export geometry decodes to the site areas within 2 %.
   - No household-level record appears in the export (AI Act rule 4).
5. **Null calibration.** Under the null (the designated set drawn from the null generator itself), p-values are ~U(0, 1): KS p > 0.05 over 200 draws.
6. **Sensitivity (reported, not pass/fail; one table in `out/sensitivity.csv`).** Vary:
   - τ ∈ {0.25, 0.30, 0.35};
   - the basket ±15 %;
   - λ ∈ {1, 1.5, 3} km;
   - κ ∈ {2, 3, 5} %;
   - FAR ∈ {0.7, 1, 1.5};
   - σ (low-income share of new dwellings) ∈ {0.3, 0.5, 1};
   - adjacency buffer ∈ {0, 2, 5} m.

   Report for each:
   - the audit label of each designated set, and whether it flips;
   - Kendall τ of the site holistic ranking;
   - the overlap of portfolio p_1.
   - Pass condition for publication: the audit labels are stable on ≥ 2/3 of the grid, or the UI shows them as "parameter-dependent".

### 5.10 What to drop
- B: the `max(rig, dism, tras) > 0.3` pool gate; the green-km criterion; `mix` as a weight; mean-weights rankings in any public output (B already says so).
- A: distance to the NIL polygon; the parcel-level 12-per-NIL pre-screen (replaced by sites plus dominance filtering); the "displacement pressure" wording until F-A1 is done.
- C: the neural surrogate; the PU score as a public layer or a criterion (it stays an analyst lead list, shown with the fairness ablation); the NIL green index as a criterion (it is redundant with heat).
- Everywhere: rig/dism as a site signal (keep `RIG` only as an audit context set).

---

## 6. Reviewer evidence on the owner's question (preliminary, not the audit)
Area-weighted NIL context of land (from `review1_checks.py`; parcels inside PCU excluded from tras and soft):

| set | km² | % poor | % foreign | net €/month | metro km |
|---|---|---|---|---|---|
| all land | 144.4 | 29.7 | 24.5 | 2,086 | 1.20 |
| AT non-PCU (tras ≥ 0.5) | 4.36 | 31.0 | 26.9 | 1,930 | 1.00 |
| srv_erp | 4.01 | 30.1 | 21.9 | 1,921 | 1.01 |
| rig zone | 33.3 | 30.3 | 25.5 | 1,888 | 0.94 |
| soft_site (non-PCU) | 42.7 | 29.6 | 22.4 | 2,104 | 0.88 |

Designated AT land sits in slightly poorer, more foreign NIL than the soft-site alternatives. It is also *not* worse on metro access. This is consistent with C's re-signed AUCs. The effect is modest at NIL resolution. Whether it is significant beyond what periphery explains is exactly what the ring-matched null of §5.7 must decide. **No segregation conclusion should be published before that test.**

---

## 7. Reproducibility summary
- Re-run OK: B `engine.py` self-checks; C `regions.py` (byte-identical outputs).
- Checked against files OK: 7 headline numbers for A, 7 for B, 7 for C.
- **Failure:** C's global Moran's I is reported as 0.406 in the docs, but the file and the re-run give 0.57.
- Not re-run: A `run_all.py` (9 min), C `pu.py` / `access.py`, B `run.py` (8 min). Their numbers were checked against the committed result files only.
