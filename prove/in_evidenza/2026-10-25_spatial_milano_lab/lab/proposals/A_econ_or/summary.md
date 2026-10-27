# A_econ_or — summary: the belly of the distribution, measured and served

To reproduce, run `prep.py` once (about 1.5 min), then `run_all.py` (about 9 min). Use `PYTHONPATH=C:/Temp/pl python` for both.

## Model

The model works at NIL level only. It never scores individual households.

1. Income.
   - A Dagum MLE is fitted on grouped IRPEF data per CAP (36 of 38 CAP).
   - It is calibrated to tax.
   - Synthetic households are built from Census 2021 sizes, with 1.40 earners per household.
   - Gross income is converted to net household income.
2. Income bands.
   - **ERP**: ISEE proxy at or below 16k.
   - **TARGET**: not ERP, fails the market rent test (τ=30% or residual income), but passes the 90 €/m²/yr social rent.
   - **GREY**: not ERP and fails both rents.
   - Uncertainty comes from a 40-scenario bootstrap.
3. Robust MILP (HiGHS).
   - Objective: maximise the mean plus CVaR₂₀ of households served, with distance decay λ=1.5 km.
   - Constraints: budget; project size of 20–400 dwellings; NIL social-mix caps of 3% (1.5% where ERP is already concentrated).
   - A Gini ε-constraint gives the Pareto set.
   - Supply excludes the PCU parks, and `rig`/`dism` are not used as site signals.

## Demand

- About 10,500 target renter households (p5–p95: 4,350–19,260). Their annual gap to market rent is 20 M€.
- Demand is concentrated in central and semi-central NIL: Buenos Aires–Venezia 1,330, Duomo 730, Brera 695, Isola 545.
- Peripheral NIL are near 0. The indicator therefore measures displacement pressure.
- Target households' median net income is 2,418 €/month.
- The GREY band is empty: every non-ERP household can afford social rent.

## Validation

- The tax ratio is stable across CAP.
- 54% of employees fail the market test.
- The ANSA figure of 37–38% "excluded but not ERP" is reproduced only with looser thresholds. Under our definitions the share is 3.7–16.5%.
- The Piano Casa target of 10k dwellings is close to the estimated demand.

## Sensitivity (D = city-wide demand, households)

- **Rent threshold τ**: D = 25.3k at τ 0.25, 9.8k at τ 0.30 (base), 4.1k at τ 0.35.
- **ERP boundary**: without the rent deduction, D = 25.2k.
- **Earners per household**: D stays in the range 8.9–10.5k.

## Portfolios (845 candidates, 41k dwellings at FAR 1)

| ID | Constraint | Dwellings | Served | CVaR₂₀ | Gini |
|---|---|---|---|---|---|
| P1 | 0.5 bn€ | 2,197 | 2,064 | 2,018 | 0.45 |
| P2 | 1.0 bn€ | 4,147 | 3,845 | 3,643 | 0.29 |
| P3 | 1.5 bn€ | 6,045 | 5,365 | 4,673 | 0.23 |
| P4 | 2.5 bn€ | 10,109 | 7,655 | 5,336 | 0.13 |
| P5 | 1 bn€, Gini ≤ 0.15 | 4,225 | 3,865 | 3,479 | 0.15 |
| P6 | 1 bn€, Gini ≤ 0.08 | 4,167 | 3,712 | 3,213 | 0.08 |

- Equity is cheap. Moving from Gini 0.29 to 0.08 costs 3.5% of mean service, and the number of NIL served rises from 26 to 41.
- The robust model holds up out of sample. On fresh scenarios, P2 keeps a CVaR of 3,646, against 3,529 for the expected-value model.
- Budget is the binding constraint, not land. Changing FAR from 0.7 to 1.5 moves service only from 3,742 to 3,924.
- Filtering candidates to C's PU top-10% halves the pool and cuts service by 10%.
- Some MILP runs reached the time limit with a 0–3.6% gap. Treat differences under 2% as noise.

## Open questions

1. The exact SAP/ISEE rule, and the ANSA definition behind the 37–38% figure.
2. Choosing τ is a normative decision.
3. Tenure share by NIL.
4. Whether demand should be served locally (anti-displacement) or city-wide.
5. Real PGT indices, ownership and construction costs.
6. Merging adjacent parcels.

## Potere d'acquisto reale (`purchasing_power.py`, `results/purchasing_power*`)

- **Fonti**
  - Soglia ISTAT di povertà assoluta, Lombardia, comune centro di area metropolitana, adulto solo: 1.256,37 €/mese. Anno di riferimento da verificare.
  - Paniere non abitativo = 60% della soglia, quindi 754 €/mese. La quota del 60% è un'assunzione da verificare.
  - Livello dei prezzi Milano/Italia: 1,047 (Istat-Unioncamere-Tagliacarne, 2009).
  - Inflazione NIC: serie nazionale, da verificare.
  - Canoni OMI 2019 e 2024: dato reale.
  - Crescita dei redditi 2019-2024: non osservata, trattata come scenario (+10%, +15%, +20%).
- **Reddito reale**
  - Il reddito netto familiare mediano per NIL è 2.303 €/mese nominali, cioè 2.199 € a prezzi medi italiani.
  - Il 31% delle famiglie, se affittasse a prezzi di mercato, avrebbe un residuo negativo dopo canone e paniere.
- **Erosione 2019-2024**
  - Canoni OMI: +41% in mediana. Periferia (fascia D) +48%, centro (fascia B) +26%.
  - Inflazione: +17,4%.
  - Reddito reale: tra −6% e +2%.
  - Reddito rispetto al canone: tra −15% e −22%.
- **La definizione decide se la "pancia" esiste.** Domanda insoddisfatta per regola:
  - rapporto τ = 30%: 9.794 famiglie;
  - reddito residuo ISTAT (canone + paniere): 103 famiglie (bootstrap 13-412);
  - paniere "dignitoso", 1,5 volte quello ISTAT: 2.067 famiglie.

  La fascia esclusa ma non ERP soffre di sovraccarico da canone, non di povertà materiale. Chi non arriva al minimo dopo il canone è quasi sempre già idoneo all'ERP. La soglia del 30% va dichiarata come scelta normativa.
- **Localizzazione**
  - La domanda è all'85% nei 20 NIL più cari.
  - Ai rapporti affitto/reddito del 2019 sarebbe di 2,8 mila famiglie, al 99,7% negli stessi NIL.
  - La pancia resta centrale ma si allarga verso l'esterno.
- **Portafogli con la domanda a reddito residuo**
  - P2r: 21 siti, 577 alloggi, 0,18 mld €, 153 famiglie servite, 11,5% di siti in comune con P2.
  - P6r: risultato simile.
  - I portafogli P1-P6 hanno senso solo se l'obiettivo pubblico è il sovraccarico da canone.
- **Da verificare**
  - La soglia ISTAT esatta per il 2024.
  - L'inflazione NIC di Milano.
  - I redditi MEF di Milano del 2019.
  - La mappatura NIL → fascia OMI.
