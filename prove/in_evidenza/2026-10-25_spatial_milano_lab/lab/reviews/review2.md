# Review 2: independent adversarial referee report on `lab/model`

Date: 2026-10-27. Reviewer: second referee. Scope: the review1 spec, `lab/model/*.py`, `lab/results/*` (`results.md`, `tests.json`, `audit_*.csv`, `sensitivity.csv`, `portfolios.csv`).
Scratch scripts for every number below are in `C:/Temp/r2/` (`fp.py`, `robust.py`, `block.py`, `erpcost.py`, `port.py`, `seeds.py`). Pre-fix outputs are backed up in `C:/Temp/r2/before/`.
I made no writes in `mi/` or `lab/proposals/`.

## Summary

The pipeline is carefully built. The invariants hold, the MILP matches brute force, and the verdict-lookup fix is a genuine bug fix. Two of the three published labels do not survive scrutiny, however:

- **AT = RISK** is a Monte-Carlo coin flip. Under the calibrated null, 11 of 20 seeds give "risk" and 9 give "neither". The label holds at 2 of 14 sensitivity grid points. It also disappears under a NIL-block null (dDI p = 0.10), because AT sits in only 12 NIL (7.5 effective NIL). What does survive is a **placement** finding: AT capacity lands in NIL with lower residual income and more ERP concentration. Even that finding is driven largely by one 92-household NIL (Stephenson) that inherits its income statistics from a CAP.
- **ERP = POTENTIAL** comes from one assumption: srv_erp land is costed at 1 €/m². If ERP land is costed at market like the null sites, served per €1M is 1.32, against a null median of 1.58 (size) and 1.39 (ring), so the label becomes "neither". In absolute terms, ERP sites serve *fewer* target households than matched alternatives (1,729 vs a null median of 2,262 / 1,942).
- **"The people's portfolio serves 43 % more"** is mostly a pool-size effect. The non-designated MILP pool has 620 sites and 47k capacity; the designated pool has 150 sites and 16k. Against non-designated pools of the same size the advantage is +21 %. If the pools are also ring-matched, it is +5 %, and PGT sits inside the range of those pools.

**Decision: ACCEPT WITH MAJOR REVISIONS.** Publish as a prototype only with the revised claims in the final table.

---

## Issue 1: false-positive test (spec: 50 reps ≤ 0.10; integrator: 0.12 at 50, raised to 200 reps for 0.07)

**Finding.** Raising the reps after seeing a FAIL was post hoc. The integrator disclosed it, but the pass criterion was still changed after the result was known. The real problem is different, though: the harness draws the "designated" set G uniformly from **all** sites and draws the null from the **complement** only. Under the random-partition H0 that the harness simulates, that null is not exchangeable with G. Removing G's sites under-represents G's own NIL in the null, which makes G look more extreme.

**Evidence** (2,000 replications each, R = 199, exact Clopper-Pearson 95 % CI):

| null pool | FP rate | 95 % CI | first 50 | first 200 | KS p (randomised p-values) |
|---|---|---|---|---|---|
| complement of G (as shipped) | 0.061 | [0.051, 0.072] | 0.12 | 0.07 | 0.069 |
| all sites incl. G (permutation) | 0.042 | [0.034, 0.052] | 0.08 | 0.045 | 0.81 |

So the shipped audit was mildly **anti-conservative** (≈ 6 % at nominal 5 %): the 50-rep FAIL was a real signal, not only noise. The ≤ 0.10 bound in the spec is too lax to detect this. On real data the same mechanism applies under the H0 "designation is a random partition of candidate land". With the permutation pool, AT's dDI p rises from 0.003 to 0.011 (size) and from 0.007 to 0.010 (ring). AT's dIso p in the ring null rises from 0.014 to 0.044.

Test 5 (`5_null_pvalues_uniform`, KS p = 0.985) is tautological. It draws G from the null generator itself, so it cannot detect this kind of problem.

**Severity:** moderate. The size of the bias is small, but it moved AT's borderline q-values.

**Fixes applied:**
- `run.py`: the null pool is now `soft | m` (all candidate land including G), not `soft & ~m`. For RIG ⊂ SOFT this is unchanged.
- `tests.py` 1b: G is tested against the same permutation pool with 1,000 reps and R = 99. Pass requires rate ≤ 0.10 **and** a CI lower bound ≤ 0.05. Result: **0.031 [0.021, 0.044]**, PASS. The test is calibrated and slightly conservative, as expected with R = 99 ties.
- Full re-run done; runtime 14.5 min, tests 78 s.

## Issue 2: pre-registration integrity (verdict-lookup bug)

**Finding.** This is a genuine bug fix. With `Q.index == k`, an integer RangeIndex was compared with strings such as `"dDI"`. That comparison is always False, so the risk clause could never fire for any set. The fix (`Q.idx == k`) is the only sensible implementation of the rule text.

**Re-derived by hand** from the pre-fix `audit_bh.csv` and `config.AUDIT['rule']`:
- AT: dDI q = 0.0108 (size) and 0.024 (ring), both < 0.05, so risk holds.
- AT: served/€1M is 0.935, below the null median of 0.967 / 0.979, so potential fails.
- Label: "risk". This matches the shipped label.
- After the Issue 1 fix: dDI q = 0.0396 (size) and 0.036 (ring). The label is still "risk", but only just.

**Other deviations from the pre-registered text and the spec.** None of them changes a label:
1. The rule says BH over "4 sets × 6 indices", but `verdict()` passes 3 sets (18 tests per null). Including RIG gives AT dDI q = 0.007 / 0.019 instead of 0.011 / 0.024 (pre-fix numbers).
2. The spec says two-sided p; the config says one-sided in the harm direction. With two-sided p (pre-fix), AT dDI q = 0.022 / 0.048, which is borderline in the ring null.
3. The spec's verdict was "exceeds the null p95 in both nulls"; the config uses "BH-significant". These are close, but they are not the same rule.

**Severity:** low for integrity. The documentation should list deviations 1–3.

## Issue 3: is AT "risk" substantive?

**Sign and units are correct.** DI is the Duncan index (0–1); ΔDI = post − now; harm = '+'. Baseline DI₀ = 0.0872 and city p_erp = 0.463. AT gives ΔDI = −0.00052 against a null mean of −0.00085, so AT *reduces* segregation, just by 0.00033 DI points less than matched land would. That is 0.4 % of baseline DI. In other words, "risk" means "slightly less desegregating", which is substantively negligible.

**NIL clustering.** AT's 58 sites lie in only **12 NIL**, with an effective number (by capacity) of **7.5**. Four NIL hold 67 % of AT capacity: Lodi-Corvetto 2,056, Bovisa 1,808, Stephenson 1,641 and Forze Armate 1,440. ERP touches 33 NIL (effective 12.8); AMB_DEG touches 5 (3.7). The site-level null scatters capacity over many more NIL, so its variance understates the variance relevant to a 7-NIL allocation.

I added a **NIL-block permutation null**. It re-assigns each NIL-block of capacity to a distinct random NIL whose non-designated capacity can absorb it, optionally within the same centre-distance ring; 4,999 draws. Implemented as `audit.block_test`, written to `audit_robustness.csv` and reported in `results.md` §3.

| set | null | p dDI | p dIso | p dep_poor | p dep_resid | p conc_q5 |
|---|---|---|---|---|---|---|
| AT | NIL-block | **0.103** | 0.170 | 0.051 | 0.015 | 0.011 |
| AT | NIL-block, ring | **0.102** | 0.222 | 0.038 | 0.014 | 0.023 |
| ERP | NIL-block | 0.155 | 0.322 | 0.146 | 0.253 | 0.0002 |
| ERP | NIL-block, ring | 0.475 | 0.670 | 0.321 | 0.280 | 0.0002 |
| AMB_DEG | NIL-block | 0.686 | 0.210 | 0.428 | 0.544 | 0.085 |

Under the NIL-block null the AT segregation signal (dDI, dIso) is **not significant**. The placement signals (dep_resid, conc_q5, dep_poor) remain at p ≈ 0.01–0.05 before any multiplicity correction.

**Data artefact.** Stephenson has 92 households (172 inhabitants) and receives 1,641 AT dwellings, 17.9× its stock. It shares CAP 20157 statistics with Cascina Merlata and Roserio: poor = 40.57, the city maximum, and p_erp = 0.638. Its "deprivation" therefore describes the CAP, not the place where the dwellings would go, and building there creates a new neighbourhood rather than adding to a poor one. Results with Stephenson's AT sites dropped:
- Site null: dep_poor p = 0.179 (size) and 0.016 (ring); dDI p = 0.026 / 0.018.
- NIL-block null: dep_poor p = 0.30 / 0.18, dep_resid 0.089 / 0.068, conc_q5 0.027 / 0.053.

Leave-one-NIL-out (site nulls, R = 499): AT's dDI p climbs to 0.02–0.038 when Corvetto, Bovisa, Forze Armate or Stephenson is dropped. With 18 tests per null under BH, a raw p of 0.03 does not clear q = 0.05.

**Monte-Carlo stability** (calibrated null, R = 999, 20 seeds, full BH verdict): AT = risk in **11 of 20** seeds and neither in 9. AT dDI q ranges over 0.014–0.040 (size) and 0.025–0.072 (ring). In the re-run sensitivity grid (R = 299), AT keeps "risk" at only **2 of 14 points** (stability 0.14). These include τ, basket and λ, which cannot change dDI at all, so the flips are pure null noise. Before the fix the integrator reported 0.93 stability.

**Severity: high.** The headline AT = RISK is not a robust finding.

**Fix applied:** the NIL-block null and the AT stability statement are now generated in `results.md`. **Required (not applied):**
- State in the headline that AT's label is unstable.
- Lead with placement (dep_resid / conc_q5), not segregation.
- Flag or exclude NIL with fewer than about 500 households from the placement indices, or move to hex-level deprivation.

## Issue 4: circularity

1. **`conc_q5` is partly defined by PGT designation itself.** `q5` = top quintile of p_erp **or** of srv_erp share, and srv_erp is the PGT ERP layer. For ERP, 82 % of capacity is in q5 through srv_erp alone and only 26 % through p_erp. ERP's conc_q5 = 0.85 (NIL-block p = 0.0002) is therefore largely tautological. For AT the split is 57 % via p_erp and 45 % via srv_erp, against 20 % via p_erp for all SOFT capacity, so AT's concentration is real but overstated by the OR. **Required:** report conc_q5 on p_erp only, and drop the srv_erp arm for ERP.
2. **κ coupling.** NIL with srv_erp > 5 % get κ = 0.015 instead of 0.03. This covers 78 % of ERP capacity and 25 % of AT, against 26 % of SOFT. That penalises L_pgt in the MILP, but only slightly: with uniform κ = 0.03, L_pgt serves 1,200 instead of 1,166 (+3 %).
3. **Same signal, counted several times.** p_erp is simulated from CAP-level MEF income, and `poor`, `net_m` and `resid` also come from MEF/CAP income. So dDI, dIso, dep_poor, dep_resid and conc_q5 are one ecological signal measured at 38 CAP, not 5 independent pieces of evidence. BH remains valid under positive dependence, but the narrative should not count them as corroboration.
4. Demand D (target households) and the placement indices share p_erp and resid. Served-per-€ for designated sets saturates (results.md caveat 7), so it mostly tracks **cost**. That is exactly the channel through which the ERP land assumption acts (Issue 7a).

**Severity:** moderate. Partly fixed by disclosure; the conc_q5 redefinition is still required.

## Issue 5: "the people's portfolio serves 43 % more"

L_people serves 1,672 and L_pgt 1,166, so +43.4 %. The comparison is not like for like:

| | MILP pool sites | pool capacity | NIL covered |
|---|---|---|---|
| designated (L_pgt) | 150 (AT 51, ERP 95, AMB_DEG 4) | 16,226 | 36 |
| non-designated (L_people) | 620 (8 cheapest per NIL) | 47,234 | 82 |

Both pools face the same budget, κ and m_min, but L_people chooses from 2.9× the capacity in 2.3× the NIL. The designated pool also benefits from free ERP land. I ran a **size-matched comparison**: random non-designated pools with the designated pool's count per area decile, capacity 16.0k–16.9k against 16.2k, without the cheapest-8 prescreen, solved with the same MILP; 8 draws each.

| comparison | served (mean, range) | L_pgt 1,166 relative |
|---|---|---|
| full L_people (as published) | 1,672 | −30 % (people +43 %) |
| size-matched non-designated pools | 1,413 (1,336–1,530) | −17 % (people +21 %) |
| size- and ring-matched pools | 1,228 (1,130–1,341) | −5 % (people +5 %); L_pgt beats 2 of 8 |
| L_people, 300 s (certified optimal, gap 0.07 %) | 1,732 | people +48 % |

**Finding.** About half of the 43 % comes from pool size. Most of the rest comes from periphery (ring), not from designated sites being individually worse. "+43 %" is a fair answer to "what if you could choose freely from all non-designated land?" It is not evidence that "PGT sites are worse sites".

**Severity: high** for the headline wording. **Required:** quote the matched figures (+21 % size-matched, ≈ +5 % ring-matched) next to the 43 %.

## Issue 6: solver gaps (P1–P6: 2.3–7.4 %)

P1 re-solved for 300 s reaches certified Optimal (gap 0.06 %) with served = 1,794.6, against 1,741.8 at 30 s (+3.0 %). It has 117 sites instead of 102, and a designated share of 0.33 instead of 0.30.
- **What survives:** the 85 %-of-P1 stop rule still admits P2–P6 (threshold 1,525 against 1,626–1,716). The claim that many near-equivalent portfolios exist, with designated share between 0.25 and 0.33, holds.
- **What does not survive:** the *ranking* among P1–P6. They differ by ≤ 7 %, which is inside the solver gaps, and P5's gap is 7.4 %. Portfolio-SMAA P(top-3) values such as P5 0.45, P6 0.59 and P2 0.00 are therefore not interpretable.
- **Related SMAA weakness:** CVaR₂₀ is ≈ 654 for every non-PGT portfolio, because it is saturated by the low-demand scenarios. `portfolio_smaa` min-max-normalises each column, so a 651.6 vs 654.4 difference is stretched to the full [0, 1] range and enters the ranking as if it were material.

**Severity:** moderate. **Required:** raise the time limit to ≥ 300 s for P1–P6 (≈ 30 min) or report the P-ranking as indicative only, and drop or rescale saturated criteria before min-max normalisation.

## Issue 7: other bugs, weaknesses and leakage

a. **ERP "potential" rests on one assumption.** In `add_capacity_cost`, `public = origin == "ERP"` puts land at 1 €/m², against 20 % of OMI price × GFA elsewhere. Mean fixed cost per dwelling is 1,785 € for ERP and 65,518 € for SOFT. Costing ERP land like SOFT gives served/€1M = 1.32 against a null median of 1.58 / 1.39, so the label would be "neither". Ownership of srv_erp land is not verified: designation is not ownership. ERP sites also serve fewer target households in absolute terms (1,729 against a null mean of 2,262 / 1,942), even though they are placed in deprived NIL. This check is now generated in `results.md` and `audit_robustness.csv`.

b. **Sensitivity grid vs base precision.** The grid uses R = 299 while the base uses R = 999. For borderline labels the grid then measures Monte-Carlo noise, not parameter sensitivity. Recommend reporting p-value or q-value bands instead of label flips, or using R ≥ 999 for AT.

c. **Tiny NIL.** Six NIL have fewer than 130 households (Cascina Merlata 1, Giardini P.ta Venezia 21, Parco Nord 61, Stephenson 92, Assiano 108, Roserio 128). In some of them, CAP-level income is copied onto a near-empty area (40.57 % poor in three of them), and they carry large new capacity (RIG puts 1,265 dwellings in Cascina Merlata). Deprivation-weighted indices should use a household floor or hex data.

d. **Test 5 is tautological** (Issue 1), and test 1a only checks an extreme planted effect. Neither probes the clustered-allocation case that matters here. **Required:** add a planted test with G concentrated in a few random NIL under H0, to calibrate the site-level null against clustering. The NIL-block results above suggest the site-level null will be anti-conservative in that case.

e. **No data leakage** into the export was found (4j passes). No household records are present.

f. The MILP and invariant tests (2a, 2b, 4a–4i) are sound. 4d checks the scenario mean only, but per-scenario u ≤ D is enforced by a variable bound, so this is acceptable.

## Changes made to `lab/model/` (all re-run)

| file | change | reason |
|---|---|---|
| `run.py` | null pool `soft & ~m` → `soft \| m` | calibration (Issue 1) |
| `run.py` | after the verdict: NIL-block nulls for AT / AMB_DEG / ERP and the ERP-at-market-land check; stored in `out["block"]`, written to `results/audit_robustness.csv` | Issues 3 and 7a |
| `audit.py` | new `block_test()` (NIL-block permutation null; post hoc; not in the verdict) | Issue 3 |
| `tests.py` | 1b: permutation pool, 1,000 reps, R = 99, exact CI in the pass rule | Issue 1 |
| `report.py` | new §3 subsection "Robustness checks added by review 2"; disclosure sentence on the pool change | transparency |

Re-run: `run.py` 14.5 min, then `tests.py` 78 s (0 failed), then `report.py` regenerated `results.md` with the new `tests.json`.

The pre-registered rule text in `config.py` is **unchanged**. The pool change is a calibration fix, and it makes p-values larger.

## Updated headline numbers (after the fixes)

| | before | after |
|---|---|---|
| AT dDI q (size / ring) | 0.011 / 0.024 | 0.040 / 0.036 |
| AT dIso q (size / ring) | 0.060 / 0.036 | 0.063 / 0.113 |
| AT label (base / seed stability / grid stability) | risk / – / 0.93 | risk / 11 of 20 seeds / 0.14 |
| AT NIL-block p, dDI (any / ring) | – | 0.10 / 0.10 |
| ERP served/€1M vs null median (size / ring) | 1.73 vs 1.58 / 1.41 | unchanged; with market land: 1.32 vs 1.58 / 1.39 |
| FP rate of the audit (synthetic) | 0.07 (200 reps, complement pool) | 0.042 [0.034, 0.052] (2,000 reps, R = 199); 0.031 [0.021, 0.044] (1,000 reps, R = 99) |
| People vs PGT served | +43 % | +43 % raw; +21 % size-matched; +5 % size-and-ring-matched |
| P1 served (30 s / 300 s) | 1,742 | 1,795 (certified optimal) |

## Final verdict per designated set

| set | published label | defensible claim |
|---|---|---|
| **AT** | RISK | **Placement concern, not demonstrated segregation risk.** At FAR 1.0, AT capacity sits in NIL whose residual income is about 150 €/month below the city mean, against about 45 below for matched land. 82 % of it is in top-ERP NIL, against about 49 %. Under the NIL-block null this holds (dep_resid p ≈ 0.015, conc_q5 p ≈ 0.01–0.02), but it rests on 7.5 effective NIL and heavily on Stephenson (92 households, CAP-imputed income). ΔDI is 0.0003 DI points (0.4 % of baseline) less desegregating than matched land. The pre-registered "risk" label is a coin flip (11 of 20 seeds, 2 of 14 grid points) and disappears at NIL level (p = 0.10). Report it as "not robust". |
| **ERP** | POTENTIAL | **Cheap, not well located for demand.** The advantage exists only if srv_erp land is free to build on (unverified). At market land cost: "neither". In absolute terms it serves fewer target households than matched land. Its concentration in high-ERP NIL is largely tautological (srv_erp defines q5). Opportunity index 0.590 against a null median of 0.569–0.578 (not significant). |
| **AMB_DEG** | NEITHER | **Uninformative.** 5 sites in 5 NIL (348 dwellings). The study has no power for this set; say nothing beyond that. |
| RIG (context) | – | RIG land sits in poorer NIL (+1.25 pp poor against 0.59 for the null; −78 €/month residual against −30). Under the permutation null, site-level p ≈ 0.001 for dDI, dIso, dep_poor and dep_resid; conc_q5 is not significant (p = 0.05). RIG is 41 % of the SOFT pool, so the permutation null is conservative here. It touches 53 NIL (26.6 effective), so this is the most robust placement signal in the study, but it is context, not a verdict. |
| people vs PGT | +43 % | +43 % is the gain from free choice over all non-designated land. Holding pool size fixed, the gain is about +21 %; holding ring as well, it is about +5 %. PGT's shortfall is mostly *scarce and peripheral land*, not bad sites. |

## Decision

**ACCEPT WITH MAJOR REVISIONS** for publishing the prototype. Before publishing:
1. The headline labels must carry the robustness statements above. The code now generates the evidence, but `report.py`'s §1 prose still leads with the label.
2. Redefine conc_q5 on p_erp only.
3. Add a household floor for placement indices, or flag Stephenson.
4. Make the ERP land-cost assumption a headline caveat.
5. Quote matched figures next to "+43 %".
6. Either run P1–P6 to optimality or mark their ranking as indicative.

The model, the invariants and the openness of the pre-registration are good enough for a prototype. The substantive answer to the research question should be stated as: "designated land, especially AT and the regeneration zone, sits in poorer NIL; there is no robust evidence that building it would increase segregation; ERP's apparent advantage is an accounting assumption."
