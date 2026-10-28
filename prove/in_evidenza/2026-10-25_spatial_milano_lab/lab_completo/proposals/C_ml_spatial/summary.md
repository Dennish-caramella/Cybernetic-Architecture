# Researcher C: ML and spatial — summary

To reproduce, run the scripts from this folder in this order with `PYTHONPATH=C:/Temp/pl python <script>`. The total runtime is about 4 minutes.

1. `access.py`
2. `pu.py`
3. `regions.py`
4. `surrogate.py`

## Key finding: two PGT label layers are broken

- `pgt_dism` is almost the same as `pgt_rig` (r = 0.998). Of the 1,716 dismissed-area features, 1,657 are marked "ex AR_RIG".
- `rig` is a zone-wide policy covering 36.8 km². It does not mark individual sites.
- `pgt_tras` is dominated by the 6 PCU park areas, which hold 5,653 of its 6,989 parcels. Those 6 areas are excluded.

## 1. Accessibility

E2SFCA was computed for 112,851 land parcels.

| Measure | Decision | Evidence |
|---|---|---|
| Schools, services, green | Keep E2SFCA | ρ against simple distance is −0.16 to −0.39 |
| Jobs | Use the count of jobs within 5 km | ρ = 0.978 against E2SFCA |
| Metro | Keep only one measure | — |

- The jobs measure is a proxy: non-residential floor area.
- Heat and green are redundant (ρ = −0.87).
- 2SFCA blows up where population is low. Normalise it by rank.

## 2. PU site detector (planner labels: 1,440 parcels)

- Random cross-validation is badly over-optimistic. PR-AUC is 0.928 with random folds and 0.326 with 4 km blocks.
- The main model uses physical and context features only, with no socio-economic data. Under block validation:
  - PR-AUC is 0.099 (7.7× the base rate).
  - ROC is 0.737.
  - Recall@10 % is 0.50.
- The FAR rule behind `soft_site` performs at the base rate (PR-AUC 0.015).
- Socio-economic features raise PR-AUC to 0.256, but they copy who lives there. They are excluded.
- The scores are not calibrated:
  - Elkan–Noto c varies from 0.055 to 0.51 across blocks.
  - Residual Moran's I is 0.738.
  - Use the score as a rank only.
- The top 200 parcels of at least 2,000 m² are in `results/pu_top_sites.*`. This list is for analysts only, never public.

## 3. Need regions (250 m hex cells, rent / modelled income)

- Global Moran's I is 0.406.
- 193 cells remain significant after FDR correction. 74 are high-high, holding 63k residents in 24 NIL.
- max-p gives 195 regions. They explain more variance than the NIL (R² 0.868 vs 0.495).
- Region stability is moderate (ARI 0.71), so show several variants.

## 4. Neural surrogate: rejected

- Fidelity is good: ρ = 0.9998.
- It is about 85× slower than the exact calculation.
- Exact computation in JS is already fast enough. Scoring takes 0.18 ms for 15,718 candidates.

## Open checks

- No hyperparameter search was run.
- The jobs proxy and hex income are not validated.
- Distances are Euclidean.
- Only about 83 planning objects back the labels.
