# Researcher B: cybernetic participation engine — summary

All preferences are synthetic: the 4 archetypes, the simulated respondents and the stress-test minority. No number here describes real citizens.

To reproduce, run `PYTHONPATH=C:/Temp/pl python run.py`. The full run takes 486 s. `python engine.py` runs the self-checks.

## E1: criteria and SMAA (real data)

- Hard filters leave 11,429 land parcels. The exact dominance-depth filter (k=10) keeps 3,723 parcels in 76 NIL. The SMAA short-list has 654 parcels in 45 NIL.
- Under uniform weights only 123 parcels are ever ranked first. The best parcel is first for only 8–15 % of weight vectors.
  - Best holistic acceptability is 0.38, for parcel 015400.27 (Cimiano, 60 m from M2 Cascina Gobba).
  - That parcel has P(top-10) = 0.50 and a confidence factor of 0.28.
  - So there is no single best parcel. Robustness has to be shown as a probability.
- Two parcels are robust across all archetypes (lowest P(top-10) across archetypes):
  - 015200.232: 0.84
  - 015400.27: 0.76
- The criteria trade off against each other:
  - Heat and cost: ρ = 0.56 (cheaper areas are hotter).
  - Need and social mix: ρ = −0.45 (high-need areas are poorer).
- Spatial clustering problem:
  - The top-100 holds 23 parcels in Cimiano and 20 in Parco Bosco in Città.
  - Four of the seven criteria are NIL-level, so neighbouring parcels tie on them.
  - Parcels must be grouped into sites, with a portfolio constraint.

## E2: active question choice (32 simulated respondents per cell, 25 questions)

- At low noise, weight error (TV) after 25 questions:
  - Random questions: 0.181.
  - EIG on weights: 0.091.
  - EIG on the top parcel: 0.118.
- Active choice reaches random's question-25 accuracy in about 8–10 questions.
- EIG on the top parcel is the most robust to careless answers. With 20 % random flips, top-10 regret is 0.051 against 0.155 for random questions.
- Negative result: at high noise with the wrong assumed β, regret does not fall. β must be estimated per person.

## E3: learning across participants

- The population prior helps majority newcomers. Their top-10 regret after 8 questions falls from 0.057 to 0.031.
- It worsens the minority's weight error, from 0.212 to 0.232. This measures the majority-amplification bias.
- Recommendations:
  - Use the population prior only for choosing questions, or per group.
  - Make a minority-error check a release gate.

## E4: aggregation and fairness

- With realistic archetypes, every rule gives 0.89–0.94 satisfaction, and JR always holds.
- With a polarised minority:
  - Mean weights, Borda and Kemeny violate JR. JR held in 0 of 6 runs.
  - seq-PAV is the most proportional. 71–80 % of the minority get one of their own top-10. It costs 0.05–0.08 in total satisfaction.
  - Elicitation error erodes proportionality. With learned weights, seq-PAV kept JR in 3 of 6 runs, against 6 of 6 with true weights.
- Recommendation: publish the group-consensus bridge parcels and a seq-PAV set side by side. Never publish a mean-weight ranking alone.

## E5: Milan demo and teach-back

- Each archetype answered 12 questions.
  - Weight error was 0.10–0.24.
  - 3 of 4 recovered their exact top parcel.
  - Top-10 regret was ≤ 0.075 for all.
- Cross-archetype consensus, one parcel per NIL:
  - 015200.232 Cimiano
  - 039600.314 Parco Forlanini
  - 011700.231 Gallaratese
  - 061900.177 Triulzo Superiore
- Teach-back gives the minimal weight change that flips a pair. Example: "015200.232 would overtake 015400.27 if green rose from 5.1 % to 12.8 % of your weight." When one parcel is at least as good on every criterion, the LP reports that no reweighting can flip them.

## Limits

- All preferences are synthetic.
- The linear model cannot represent vetoes or lexicographic rankings.
- Kemeny is exact only on the Borda top-20.
- Posterior size (2,000 particles) was not checked for sensitivity.
- E3 and E4 have few runs per cell. Treat differences below about 0.03 as noise.
