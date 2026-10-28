# A_econ_or — From the belly of the income distribution to Pareto portfolios of parcels

Researcher A (urban economics + OR). Code: `prep.py` (derived inputs, ~1.5 min, run once), `demand.py` (steps 1-2), `portfolio.py` (steps 3-4), `run_all.py` (whole experiment, ~9 min). Results are in `results/`. Every number below comes from those files.
Labels used: **[S]** cited source; **[S, from memory]** canonical source, not re-checked online; **[A]** assumption made for this model; **[D]** real data.

## 1. Question and unit

For each of Milan's 88 NIL, how many households fall in the "belly"? These are households that are **not eligible for public housing (ERP/SAP)** but **cannot afford an adequate market-rate rental in their own NIL**, while they **can afford the Piano Casa social rent**. Which alternative sets of parcels serve them best, under budget, social-mix and equity limits, and with uncertain demand?
No household is ever scored. Households are synthetic draws used only to estimate NIL-level counts (lab rule 4).

## 2. Income model (per CAP)

**Data [D].** MEF IRPEF 2024 gives, for each of 38 CAP, counts and amounts of *reddito complessivo* in 7 classes with edges e = {0, 10k, 15k, 26k, 55k, 75k, 120k, ∞}, plus the ≤0 class. In 17 CAP the ">120k" cell is blank (statistical confidentiality). We impute it as the reddito-complessivo total minus the published classes, for both frequency and amount (`prep.py`). The imputed top-class means are 175-295k, which is plausible.

**Grouped MLE.** For F ∈ {lognormal, Singh-Maddala, Dagum} we maximise
ℓ(θ) = Σ_k n_k log[F(e_{k+1};θ) − F(e_k;θ)]
and pick F per CAP by AIC. Dagum wins in 36 CAP and lognormal in 2 (`income_fits.csv`).

**Class-exact hybrid sampler (novelty 1).** We draw the class from the *observed* shares, so class shares are reproduced exactly. Inside each bounded class the value comes from the fitted F truncated to that class. Inside the open top class it comes from a Pareto law whose index α = m/(m − 120k) matches the observed class mean m (α between 1.37 and 3.16). Check against the observed within-class means: 26-55k is off by +2.3 % on average (max +3.5 %), 15-26k by −1.6 %. Without the Pareto top, the parametric tail understated the mean by 3-27 %.

**Gross → net.** We apply the IRPEF 2024 schedule (23/35/43 %), the employee credit (art. 13 TUIR), the Lombardy regional surtax and the Milan municipal 0.8 % surtax above 23k [S, from memory]. Surtaxes apply only when IRPEF is due. **Validation and calibration:** the modelled total tax per CAP overstates the MEF total (Imposta netta + surtaxes) by a stable factor. The ratio observed/modelled is 0.87 ± 0.02 (range 0.83-0.93), which is consistent with credits we leave out (dependants, 19 % expense credits). We multiply the tax by this per-CAP factor, so net incomes reproduce observed taxes exactly.

**CAP → NIL [D].** We count OSM `addr:postcode` addresses inside each NIL (39,292 addresses, 287 CAP-NIL pairs). The household CAP is drawn from these shares (π_iC).

## 3. Households, affordability and the target band

**Households [D + A].** Census 2021 sections give households by size (PF3-PF8) and are assigned to NIL by centroid. The NIL count is anagrafe pop 2025 / census mean size, for 744,871 households in total.
**Earners.** k = 1 + Binomial(s − 1, p_i), where p_i matches the mean number of taxpayers per household. That mean is (city taxpayers / adults) × adults_i / H_i [A]. The city result is 1.40 earners per household.
**Pooling.** Earner incomes are pooled through an exchangeable Gaussian copula with ρ = 0.3 (assortative mating) [A]. Net household income Y = Σ_k net(y_k), because Italy taxes individuals.

For a household h of size s in NIL i:
- **Market rent** R = r_i · A(s). r_i is the OMI 2024/2 rent in €/m²/month [D]. A(s) = 45/55/70/85/95/110 m² for s = 1..6+ [A; DM 22/4/2008 "~1 room per member"; Piano Casa examples of 50/70 m²].
- **Social rent** R^soc = 90/12 · A(s) [S: Piano Casa bandi, ANSA 26/3/2026].
- **Fail test** fail(r) ⇔ r > τ·Y/12 (ratio test, τ = 0.30) **or** Y/12 − r < b·m(s) (residual-income test, b = 750 €/month for one adult [A], m = modified OECD scale).
- **ERP proxy** ISEE ≈ [Σ_k y_k − Σ_k min(0.2 y_k, 3000) − min(12R, 7000) + ISP] / scale_ISEE(s). Eligible if ISEE ≤ 16,000 € [S, from memory: R.R. 4/2017]. ISP (assets) = 0 in the base case, because asset data are missing. This makes ERP eligibility an upper bound.
- **Three-way band (novelty 2):**
  - ERP = {ISEE ≤ 16k}
  - **TARGET** = ¬ERP ∧ fail(R) ∧ ¬fail(R^soc)
  - GREY = ¬ERP ∧ fail(R) ∧ fail(R^soc), i.e. too rich for ERP and too poor for the social rent.
- **Unmet demand** D_i = θ · H_i · P_i(TARGET), with θ = 0.30 the share of households renting or entering the rental market [A; tenure is not in the data]. **€ gap** = θ H_i E[max(R − τY/12, 0) · 12 · 1_TARGET].

**Uncertainty: structural bootstrap with 40 scenarios.** Each scenario redraws:
- the class shares (Dirichlet(n + 1));
- the CAP mix (Dirichlet(addr + 0.5));
- a city rent factor (lognormal, sd 0.07) and a NIL rent factor (sd 0.05) [A: OMI min-max band];
- earn_k ~ U(0.8, 1.2), ρ ± 0.2, b ± 15 % and θ ± 15 %.

Normative parameters (τ, the ERP rule, the social rent) are **not** bootstrapped. They are explored as policy sensitivity, which keeps epistemic and normative uncertainty separate (novelty 3).

## 4. Supply

**Candidates [D + A].** A parcel is a candidate if all of the following hold:
- land, area ≥ 1,500 m², inside the city;
- less than 50 % in green, agricultural, landscape, school, water, infrastructure or wood layers;
- not occupied housing (n_vol > 0 and residential share ≥ 0.5, to avoid displacement);
- **not inside the 6 PCU parks** (*Parchi della Campagna Urbana*), which are AT polygons named "PCU" = farmland/parks. They cover 6,478 of the 7,990 parcels with pgt_tras ≥ 0.5;
- soft_site, **or** (non-PCU tras or srv_erp ≥ 0.5, with far_ratio < 1).

Per Researcher C's warning, **rig/dism are not used as a site signal**. They are a zone-wide policy layer: dism ≈ rig (r = 0.998), and rig is "rigenerazione diffusa".

**Capacity** cap_s = min(⌊0.70 · FAR · area / 80⌋, 400), keeping only cap_s ≥ 20. Inputs: yield 70 % [S: Mill Valley]; FAR 1.0 [A; PGT base 0.35 rising to about 1 with transfers/ERS, unverified]; 80 m² gross per dwelling [A].

**Cost** = fixed_s + v · dwellings:
- fixed_s = 0.20 · OMI price · buildable GFA (land incidence) [A], or 1 €/m² on srv_erp land (assumed municipal) [S: Piano Casa cession], plus 25 €/m³ demolition of existing volume [A];
- v = 2,000 €/m² × 80 m² [S, unverified: 1,800-2,500].

Median cost is about 215 k€ per dwelling.

**Pre-screen.** We keep the 12 cheapest-per-dwelling sites per NIL plus all srv_erp sites. That gives 845 sites with 41,227 dwellings of capacity.

## 5. Robust multi-objective MILP (HiGHS)

**Sets.** s ∈ sites, i ∈ NIL, ω ∈ Ω (40 demand scenarios).

**Accessibility.** w_si = exp(−d_si/λ), where d_si is the distance from the parcel to the NIL polygon (0 inside), λ = 1.5 km, and w = 0 for d > 3 km [A]. Units therefore serve their own and nearby NIL. Demand is defined at the NIL level, which is an anti-displacement reading.

**Variables.** y_s ∈ {0,1}; x_si ≥ 0 (dwellings on s allocated to the demand of i); u_iω ≥ 0; η, ξ_ω ≥ 0.

max (1−β) · (1/|Ω|) Σ_ω Σ_i u_iω + β [η − 1/(α|Ω|) Σ_ω ξ_ω]  (mean + CVaR_α of served households, β = 0.5, α = 0.2)

s.t.
- 20 y_s ≤ Σ_i x_si ≤ cap_s y_s  (minimum and maximum project size)
- Σ_s (fixed_s y_s + v Σ_i x_si) ≤ B  (budget, the ε for cost)
- u_iω ≤ Σ_s w_si x_si,  u_iω ≤ D_iω  (served ≤ accessible supply, served ≤ demand)
- Σ_s x_si ≤ max_ω D_iω
- Σ_{s ∈ NIL h} Σ_i x_si ≤ κ_h H_h, with κ = 3 % of households, or 1.5 % where PGT srv_erp > 5 % of the NIL area (no further concentration of public housing) [A]
- ξ_ω ≥ η − Σ_i u_iω
- **Equity ε-constraint (linearised Gini).** With coverage c_i = ū_i/D̄_i and weights D̄_i, Gini = Σ_{i<j} D̄_i D̄_j |c_i − c_j| / (D_tot · U). This gives Σ_{i<j} d_ij ≤ g · D_tot · Σ_i ū_i, with d_ij ≥ ±(D̄_j ū_i − D̄_i ū_j). The constraint is exactly linear because the mean term is itself a variable (novelty 4).

**Pareto set.** ε on budget B ∈ {0.5, 1.0, 1.5, 2.5} bn€, and on Gini g ∈ {0.15, 0.08} at B = 1 bn€. Each solve has a 60 s limit and a 2 % gap target. Robustness is checked out of sample: the fixed allocations are re-evaluated on 40 fresh scenarios (seed 99).

## 6. Novelty claim (relative to the report and the literature it cites)

The report states (sec. 4) that no published MILP exists for social mix in social housing. Its formulation is site × profile allocation with MCDA suitability. Ours adds:
1. a **demand side derived from grouped fiscal microdata**, with class-exact hybrid sampling, a Pareto top, and tax-calibrated gross→net conversion;
2. a **formal three-way band** (ERP / target / grey) that combines the residual-income and ratio tests with an ISEE proxy;
3. **two-stage-like robust service** using CVaR over a structural bootstrap, with normative and epistemic parameters kept separate;
4. an **exactly linear demand-weighted Gini ε-constraint**.

The pieces are known individually: grouped-data MLE of income distributions (Dagum, Singh-Maddala), Stone's shelter poverty, Bramley needs assessment, Rockafellar-Uryasev CVaR [S, from memory]. We have not seen them combined for a site-portfolio problem. This is an author claim, not checked by a systematic literature search.

## 7. Limitations (most important first)

1. **The ERP boundary drives everything.** The ISEE proxy ignores assets (ISP) and uses the legal rent deduction. As a result, about 46 % of households look ERP-eligible if they rented. Without the rent deduction, demand is 2.6× larger. With a 3k assets term, it is 1.6× larger. The SAP threshold value (16k) is from memory.
2. τ is the most influential parameter: τ = 0.25 gives 25.3k households and τ = 0.40 gives 1.5k. The residual-income basket and the social rent level have **no** effect in this band, because the ratio test always binds first and the grey zone is empty.
3. Tenure θ is a flat placeholder, with no tenure-income gradient. This likely understates demand in poorer NIL.
4. Demand is NIL-anchored ("stay in your neighbourhood"). A city-wide search model would give much less, because peripheral rents of about 8-11 €/m² pass the test.
5. Supply proxies: there is no PGT index, ownership, constraint or real cost data. soft_site scores at base rate against planner labels (Researcher C: PR-AUC 0.015). Parcels are not aggregated by adjacency. srv_erp land is assumed public.
6. MILP solves stop at the time limit with a 0-3.6 % gap. Portfolio differences under about 2 % in served demand are within solver tolerance. Example: P5 serves 1 % more than P2 because P2 stopped at a 1.3 % gap.
7. The decay λ, the κ caps and the 20-400 project bounds are untested normative choices.
