# Proposal C — learned and spatial components (researcher C)

Scope: four components that the integrated site-selection model can use. They are an accessibility layer, a detector for "designated-site likeness", sub-NIL need regions and an interactivity check. Every number below comes from `results/*` produced by the scripts in this folder. Data status follows lab rule 3: **real** (derived from mi/ data), **assumption** (a stated parameter) or **proxy**.

Run (PowerShell or bash, from this folder; total ≈ 4 min on the dev laptop):

```
PYTHONPATH=C:/Temp/pl python access.py     # ~42 s
PYTHONPATH=C:/Temp/pl python pu.py         # ~165 s
PYTHONPATH=C:/Temp/pl python regions.py    # ~5 s
PYTHONPATH=C:/Temp/pl python surrogate.py  # ~10 s (needs access.py output; times JS with node if present)
```

Inputs are read only: `lab/data/parcels.csv.gz` (land parcels, `kind == 'land'`, n = 112,851), `mi/out/core.json`, `mi/out/pgt.json`, and `mi/raw/pgt_aree_dismesse.geojson` plus `mi/raw/pgt_ambiti_trasformazione.geojson`. Nothing is written to `mi/`.

---

## 1. Accessibility (Gaussian E2SFCA) — `access.py`

**Method.** This is the enhanced two-step floating catchment area (Luo & Qi 2009) with the Gaussian kernel of Dai (2010):

$$G(d,d_0)=\frac{e^{-\frac12 (d/d_0)^2}-e^{-\frac12}}{1-e^{-\frac12}}\ \ (d<d_0),\quad 0\ \text{otherwise}$$

$$R_j=\frac{S_j}{\sum_k G(d_{kj},d_0)\,D_k},\qquad A_i=\sum_j G(d_{ij},d_0)\,R_j$$

Distances are Euclidean in the local km frame. Demand points $k$ are the 1,077 census-2021 hex cells. Supply points $j$ are a 100 m grid inside each PGT polygon, with the polygon area split equally among its points.

| measure | supply $S_j$ | demand $D_k$ | $d_0$ (assumption) | status |
|---|---|---|---|---|
| A_jobs | non-residential GFA on parcels whose dominant DBT use is a work use (Amministrativo, Commerciale, Industriale, Servizi pubblici, Trasporti), aggregated to a 250 m grid; 23.96 km² in total | hex `emp` (employed residents = job seekers) | 8 km (≈30-40 min by transit) | **proxy**: workplace jobs are not available |
| A_school | PGT `srv_ist` area | hex pop × NIL share aged 0-14 | 1.0 km | real geometry, area as a capacity **proxy** |
| A_services | PGT `srv_alt` area | hex pop | 1.0 km | as above |
| A_green | PGT `srv_verde` area | hex pop | 0.8 km | real |
| A_metro | 1 per station (130) | hex pop | 1.0 km | real |

The script also computes simple comparators: nearest distance to a school, a service, green space and metro, the metro stations within 800 m, and the cumulative work GFA within 5 km.

**Results** (15,718 `soft_site` candidates; `results/access_summary.json`, `access_corr.csv`)

- **Jobs.** E2SFCA vs cumulative-5 km: Spearman ρ = 0.978, and the top-10 % Jaccard overlap is 0.807. At city scale the competition term adds almost nothing, so **use the simpler cumulative measure**.
- **Metro.** E2SFCA vs nearest distance: ρ = −0.88. Against stations within 800 m: ρ = 0.887. Top-10 % Jaccard is 0.179, because the measures disagree on which sites are best. **Keep one metro measure only.**
- **Schools, services, green.** E2SFCA is only weakly related to nearest distance: ρ = −0.379, −0.16 and −0.39, with top-10 % Jaccard of 0.11 and 0.122. Capacity and competition change the picture substantially. **These are the measures where E2SFCA earns its place.**
- **Redundancy (diagnostic only, never used for weights).**
  - |ρ| ≥ 0.7 pairs: A_jobs–nil_heatexp 0.724, nil_green–nil_heatexp −0.87, metro measures among themselves, and jobs measures among themselves.
  - PCA on rank-standardised indicators: the first component explains 41 % of the variance, and 4 eigenvalues are > 1.
  - The heat/green redundancy predicted by the report is confirmed (ρ = −0.87). Ask citizens to weight only one of the two.
- **Known artefact.** 2SFCA explodes where demand is near zero, for example parks at the city edge: A_green max = 6,248 m²/resident against a median of 8.3. **Use rank or winsorised normalisation** (`surrogate.py` uses ranks).

---

## 2. PU learning of "designated-site likeness" — `pu.py`

### Label audit (a finding in its own right)

- **`pgt_rig` and `pgt_dism` are the same polygons.** Parcel-share correlation r = 0.998. In the raw layer, 1,657 of the 1,716 `aree_dismesse` features carry `NOTE = "ex AR_RIG"`, and only 59 are `"ex AMB_DEG"`.
- **Every `rig` feature is "Ambito di rigenerazione diffusa".** That is 36.8 km² of zone-level policy, with 34.5 km² of it on fully urbanised soil. It labels a *zone*, not a *site*.
- **`tras` includes the PCU park ambiti (6 of the 30 AT features).** These are Parchi della Campagna Urbana, for example Bosco in Città and Abbazie. They held 5,653 of the 6,989 `tras` parcels. A first run with them included learned "peri-urban farmland" and ranked Parco Nord parcels first. They are now excluded from the positives and from the candidates.

**Final positives $s=1$:** parcels whose point-on-surface lies in a redevelopment AT (24 non-PCU AT features, the scali, caserme, Piazza d'Armi and others) or in one of the 59 AMB_DEG polygons. That gives 1,440 parcels, a base rate of 1.28 %. All other parcels are unlabelled. A secondary run uses `pgt_rig` as the target (34,552 parcels).

### Model

Elkan & Noto (2008) under SCAR:

- Train $g(x)=P(s=1\mid x)$.
- Estimate $c=P(s=1\mid y=1)=\mathbb E[g(x)\mid s=1]$ on held-out positives.
- Compute $P(y=1\mid x)=g(x)/c$.

The comparator is PU bagging (Mordelet & Vert 2014): 10 bags, each using all training positives against an equal-size unlabelled sample. Learners are `HistGradientBoostingClassifier` (300 iterations, 31 leaves) and a logistic baseline.

**Features (no PGT layer is used, to avoid label leakage).**

| group | features |
|---|---|
| physical | log area, coverage, FAR, FAR ratio, h_max, h_mean, n_vol, residential share, dominant-use dummies |
| context | morphology of the 30 nearest parcels (coverage, FAR, % industrial, % vacant, size), metro distance and count, green distance, hex pop/emp/dwellings, distance to centre |
| nil (ablation) | rent, price, net income, density, % foreign, % poor, % 65+ |
| dusaf (ablation) | land-cover shares from 2024 |

**Main model = physical + context.** NIL socio-economics are excluded on ethical grounds: they would flag a site because of who lives nearby. DUSAF 2024 is excluded as post-designation leakage: AT sites are *now* "cantieri".

### Validation design

- **Folds.** Five-fold `GroupKFold` on spatial blocks of 2 km (the tiles, 67 blocks) and 4 km (merged tiles, 21 blocks). A random K-fold is reported only to show optimism.
- **Out-of-fold scores.** Every parcel's score comes from a model that never saw its block.
- **Metrics.** PR-AUC (vs base rate), ROC-AUC, recall@1/5/10 % of parcels, a reliability table by decile, the Brier score and fold-wise $c$.
- **Residual check.** Moran's I of $s-g$ on an 8-NN parcel graph.
- **Object-level recall.** Positives are ~83 planning objects (24 AT features + 59 AMB_DEG), not 1,440 independent parcels, so the script also reports the share of each AT's area that falls in the top score decile.

### Results (`pu_metrics.json`, `pu_ablation.csv`, `pu_object_recall.csv`)

| run (target = sites) | PR-AUC | ROC-AUC | recall@5 % | recall@10 % |
|---|---|---|---|---|
| random K-fold, all features | 0.928 | 0.990 | 0.976 | 0.980 |
| block 2 km, all features | 0.363 | 0.843 | 0.586 | 0.654 |
| block 4 km, all features | 0.326 | 0.775 | 0.531 | 0.589 |
| block 4 km, PU bagging ×10 | 0.334 | 0.825 | 0.572 | 0.652 |
| block 4 km, logistic | 0.072 | 0.846 | 0.319 | 0.522 |
| **block 4 km, physical + context (main)** | **0.099** | 0.737 | 0.394 | 0.501 |
| block 4 km, physical only | 0.020 | 0.626 | 0.099 | 0.159 |
| block 4 km, physical + context + NIL | 0.256 | 0.730 | 0.474 | 0.524 |
| block 4 km, context + NIL only | 0.244 | 0.723 | 0.453 | 0.508 |
| baseline: `soft_site` FAR rule | 0.015 | 0.530 | 0.076 | 0.142 |
| baseline: −far_ratio | 0.017 | 0.613 | 0.095 | 0.243 |

Base rate: 0.0128.

- **Spatial leakage is large.** PR-AUC falls from 0.93 (random) to 0.33 (4 km blocks). A random-CV figure would be dishonest here.
- **The FAR rule does not find designated sites** (PR-AUC 0.015 ≈ base rate). The main PU model reaches 7.7× the base rate. At object level, 14 of 21 redevelopment ATs have ≥ 50 % of their area in the top decile (median share 0.873).
- **Socio-economics inflate the score.** Adding NIL socio-economics raises PR-AUC from 0.099 to 0.256, and context + NIL alone (0.244) beats parcel physics. Past designations are therefore strongly associated with *who lives in the NIL*: univariate AUC is 0.711 for % foreign and 0.697 for % poor. A model that imitates planners would reproduce this pattern. That is why NIL socio-economics stay out of the main model.
- **SCAR fails spatially.** The Elkan–Noto $c$ varies between folds from 0.055 to 0.512 (block 4 km, all features), and is 0.06 on average for the main model.
- **Probabilities are not calibrated.** The Brier score (0.0126) equals the constant-predictor Brier $p(1-p)=0.0126$. **Use $g$ only as a rank.** Never present $g/c$ as a probability.
- **Residuals stay clustered.** Moran's I of the residuals is 0.738 (main) against 0.762 for the label itself, under block CV. The model misses or finds *whole objects*, and some of the spatial structure remains unexplained.
- **Zone target (`rig`).** PR-AUC is 0.963 under random CV and 0.747 under 4 km blocks, against a base rate of 0.306. Most of this is location; it is a zoning map, not a property of the site.

**Output.** `pu_top_sites.csv` / `.geojson` holds the top 200 unlabelled parcels, filtered to ≥ 2,000 m² with < 50 % in green, agricultural, landscape, school or service land, water, infrastructure or the PCU ambiti. Both files carry x, y, lon, lat, score and attributes. Profile of the 200:

- 146.5 ha in 36 NIL; 57.5 % lie inside `rig` and 83.5 % also pass the `soft_site` rule.
- Dominant uses: none (vacant) 82, Altro 39, Industriale 34, Commerciale 23.
- The leading clusters are Ortomercato, Lambrate-Ortica, Monlué and Porta Genova.

### Novelty claim

No study was found that applies PU learning to *planning designations* as labels for soft-site detection; the same goes for this kind of validation. The validation combines spatial-block CV, object-level recall and an explicit leakage and fairness ablation. The defensible contribution is methodological and **negative as much as positive**:

1. Planner labels are spatially non-SCAR.
2. Imitation reproduces socio-spatial patterns.
3. FAR-rule screening is uncorrelated with what planners actually designated.

### Limitations

- The effective sample is ~83 objects.
- Labels are planning decisions (not ground truth "potential"), and unlabelled ≠ negative.
- There are no ownership, heritage or contamination layers.
- The DBT dates from 2020, and parcels are point-located.
- No hyper-parameter search was run, to avoid overfitting folds.

### Ethics

- The detector ranks **parcels**, never households (AI Act Annex III 5a does not apply).
- "Looks like a designated site" is **not** "should be redeveloped". Many detected parcels are working premises: 34 industrial and 23 commercial among the top 200. Redevelopment can displace workers and small firms. The output is for analysts as a lead list to check with ownership data, not a public "target map".
- The analysis shows that imitating planners encodes neighbourhood demographics. The fairness ablation must accompany any reuse.

---

## 3. Spatial need regions — `regions.py`

**Indicator (proxy).** A rent-to-income index per hex cell:

$$\text{pressure}_h=\frac{\text{rent}_{OMI(h)}\cdot 50\,\text{m}^2}{\widehat{\text{net}}_h}$$

$$\widehat{\text{net}}_h=\text{net}_{NIL}\cdot\exp\big(b\,(\tilde s_h-s_{NIL})\big)$$

- $s$ is the tertiary-educated share. $\tilde s_h$ is shrunk toward the NIL value with a prior weight of 200 residents.
- $b = 2.763$ comes from regressing log NIL net income on NIL tertiary share across NIL: R² = 0.752, n = 81.
- This is a simple dasymetric small-area estimate. Income below NIL level is **modelled, not observed**.

**LISA.**

- Local Moran with row-standardised contiguity weights (hex centres ≤ 0.45 km; the graph is forced connected).
- 9,999 conditional permutations.
- Benjamini–Hochberg FDR at q = 0.05.

**max-p.** A simple version of Duque, Anselin & Rey (2012), floor ≥ 5,000 residents:

1. 60 randomised growth constructions, each adding the most similar neighbour.
2. Enclave assignment.
3. Boundary-move local search with exact ΔSSD, keeping the floor and contiguity. Both are asserted in the code.
4. Stability is the ARI among the 10 best solutions.

Labels are neutral (`R01…`).

**Results** (`regions_summary.json`, `hex_need.csv`, `regions_map.png`)

- Global Moran's I = 0.406.
- **LISA.** 377 cells are significant at raw p ≤ 0.05; **193 survive FDR**: 74 HH, 111 LL, 4 HL, 4 LH. About half of the raw "hotspots" would be false discoveries.
- **HH population.** FDR HH cells hold 63,026 residents in 24 NIL, for example Cimiano-Rottole, Barona, Taliedo, Lodi-Corvetto and Rogoredo. Only 2 HH cells lie in NIL at or below the median NIL pressure, so "hidden pockets" are rare *with this indicator*. That is expected, because its hex variation comes only from education.
- **max-p.** p = 195 regions (population 5,009 / 6,491 / 13,878 min/median/max), and 125 regions cross NIL borders.
  - Between-region R² = 0.868, against 0.495 for the 88-NIL partition: the sub-NIL regions explain the indicator much better than NIL do.
  - Stability is moderate: ARI 0.709 mean and 0.631 minimum among the top 10 solutions. Show a co-assignment frequency or several variants rather than one map, as the report advises.

---

## 4. Neural surrogate — `surrogate.py` (verdict: **do not use**)

- **Setup.** 15,718 soft-site candidates × 6 rank-normalised criteria. The criteria are A_jobs, A_school, A_services, A_green, metro proximity and GFA headroom.
- **Surrogate fidelity.** An MLP (64-64) maps $w$ to the scores of a 500-candidate shortlist. It trains in 3.7 s. Spearman is 0.9998 (median) and 0.9992 (p5); top-20 overlap is 0.967 (mean) and 0.90 (p5).
- **Speed comparison.**
  - Exact shortlist scoring takes 0.002 ms in numpy, against 0.169 ms for the MLP. **The surrogate is ~85× slower, and it is approximate.**
  - Exact WLC on all 15,718 candidates takes 0.08 ms in numpy and **0.18 ms in node.js**.
  - Monte-Carlo acceptability (1,000 Dirichlet draws, P(top-100)) takes 221 ms in numpy and 1.38 s in node. The node version uses a naive full sort per draw; a selection algorithm or a Web Worker fixes this.
- **Conclusion.** WLC is linear in $w$, so exact computation is cheaper than any network. A learned surrogate would only make sense for non-linear, expensive models (PROMETHEE on large sets, MILP portfolios), and even then precomputation or a worker is simpler. **Rejected.**

---

## What to adopt in the integrated model

1. Use E2SFCA for schools, services and green, with rank normalisation. Use the cumulative 5 km measure for jobs, and a single metro measure. Let citizens weight only one of heat and green.
2. Use the PU score as an **analyst-only** ranked lead list to complement the FAR rule, never as a public criterion or probability. Ship it with the fairness ablation.
3. Use the max-p and LISA-FDR layer as the sub-NIL "need" map, with neutral labels and several variants.
4. Skip the neural surrogate. Compute exactly in JS and move Monte Carlo to a Web Worker.

## References

- Luo & Qi 2009, *Health & Place* 15:1100 (E2SFCA). Dai 2010, *Landscape & Urban Planning* 97:180 (Gaussian 2SFCA).
- Elkan & Noto 2008, KDD (PU learning). Mordelet & Vert 2014, *Pattern Recognition Letters* 37:201 (PU bagging). Bekker & Davis 2020, *Machine Learning* 109:719 (PU survey, SCAR).
- Roberts et al. 2017, *Ecography* 40:913 (block cross-validation).
- Anselin 1995, *Geographical Analysis* 27:93 (LISA). Benjamini & Hochberg 1995, *JRSS-B* 57:289.
- Duque, Anselin & Rey 2012, *J. Regional Science* 52:397 (max-p).
- The report `reports/Lotti per social housing partecipativo.md`, §5 and "Cosa applicare".
