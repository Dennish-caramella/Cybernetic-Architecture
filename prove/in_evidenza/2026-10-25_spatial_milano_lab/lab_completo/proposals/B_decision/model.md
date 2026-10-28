# B — Cybernetic participation engine: formal model

Researcher B (decision science, preference learning, social choice). Code: `engine.py` (library and self-checks), `run.py` (experiments E1–E5). Results: `results/`. Findings: `summary.md`.

Data status, following lab rule 3:
- **Real (derived):** parcel and NIL columns of `lab/data/parcels.csv.gz`.
- **Assumption-based proxies:** `gfa_headroom_m2`, `soft_site`.
- **SYNTHETIC:** the archetype weight distributions, the simulated respondents and the "polarised" stress-test minority.

No result here measures real citizens' preferences. Literature references marked *[canonical, from memory]* were not re-checked online in this session.

---

## 0. The loop

```
 citizens ──pairwise answers──► per-person posterior p(w | answers)  ◄── prior (uniform ⊕ population)
     ▲                                   │                                       ▲
     │ teach-back (flip explanation)     ▼                                       │ empirical Bayes
     │                       active question selection (EIG)                     │ (feeds the next person)
     │                                   │                                       │
     └──── ranking shown ◄── SMAA over posterior / group mixture ──► group clustering ──► GIC consensus, JR audit
```

Ashby's requisite variety asks the regulator to keep the variety of needs [canonical, from memory]. Each person is therefore a **distribution** over weights, not a point. Groups are mixtures of these distributions. The public output is acceptability (a probability of ranking well), never a single "citizens' vector".

## 1. Criteria matrix

**Support (hard constraints, not negotiable; Habraken's support/infill split).** The candidate pool is set in `engine.candidate_pool`:
- `kind == land` and `area_m2 ≥ 1000`;
- `soft_site` or max(`pgt_rig`, `pgt_dism`, `pgt_tras`) > 0.3;
- max(`pgt_srv_verde`, `pgt_agr`, `pgt_pae`, `dusaf_wat`) < 0.5 (no parks, farmland, protected landscape or water);
- `gfa_headroom_m2 > 0`, NIL rent and income known, inside the city.

The pool holds **11,429 parcels**.

**Infill (negotiable, weighted).** There are m = 7 criteria. Each is oriented as a benefit and scored in [0, 1].

| j | criterion | raw indicator (column) | direction | rationale |
|---|---|---|---|---|
| 1 | access | `metro_km` | lower better | transit access (report §"Dai 120.000 lotti") |
| 2 | need | `nil_rent`·60 / `nil_net_m` | higher better | affordability pressure: OMI rent for 60 m² as a share of net monthly income per taxpayer; build where the market excludes people |
| 3 | green | ½·`nil_green` (↑) + ½·`green_srv_km` (↓) | higher better | liveability for future residents |
| 4 | heat | `nil_heatrisk` | lower better | climate risk |
| 5 | capacity | log10 `gfa_headroom_m2` | higher better | homes deliverable (log: diminishing returns; proxy) |
| 6 | mix | `nil_poor` (% taxpayers ≤ 15k) | lower better | poverty deconcentration, a policy assumption (mixed-income literature) |
| 7 | cost | `nil_price` (OMI €/m²) | lower better | land-cost proxy |

**Normalisation** (robust min-max on the pool):

  s_ij = clip((r_ij − q02_j) / (q98_j − q02_j), 0, 1), and 1 − s_ij for cost-type criteria.

A weight therefore means "importance of the swing from the 2nd to the 98th percentile of *this* pool" (SWING logic; Lienert et al. 2016 in the report). Weights are not abstract importance and must be re-elicited if the pool changes.

**Redundancy diagnostic.** Spearman correlations on the pool are in `results/criteria_spec.json`.
- heat–cost ρ = 0.56: cheap areas are hot.
- green–cost ρ = 0.52.
- need–mix ρ = −0.45: high-need NILs are poorer, so need and deconcentration conflict.
- access–heat ρ = −0.44.

No pair exceeds |ρ| = 0.6, so all seven criteria are kept. The report's "rent is a double-edged criterion" appears here as the need/cost/mix triangle.

**Exact top-k reduction (dominance depth).** Let d_i = #{l : s_l ≥ s_i componentwise, s_l ≠ s_i}.

For any w ≥ 0, every l counted in d_i scores at least as high as i. If d_i ≥ k, alternative i has rank > k under every weight vector (strictly, when ties are broken by dominance).

Filtering to d_i < k is therefore **exact** for all top-k SMAA statistics. It is not a heuristic. With k = 10 it keeps 3,723 of 11,429 parcels (76 NIL). NIL-level criteria create many ties, which is why the reduction is modest.

The parcels with P(top-10) > 0 under at least one of the five weight distributions of §2 form the **SMAA short-list** used for questions and rankings: 654 parcels in 45 NIL.

## 2. Preferences as distributions: SMAA-2

The utility is linear (WLC), u(i, w) = w·s_i, with w ∈ Δ^{m−1}. For a weight density f(w), with Monte Carlo S = 20,000 (Lahdelma, Hokkanen & Salminen 1998; Lahdelma & Salminen 2001) [canonical, from memory]:

- rank acceptability: b_i^r = ∫ f(w) 1[rank(i, w) = r] dw
- central weight vector: w_i^c = E_f[w | rank(i, w) = 1]
- confidence factor: p_i^c = P_ξ(i is first under w_i^c), where ξ is criteria noise s + N(0, 0.05²). The noise is an assumption standing for proxy and ecological error.
- holistic acceptability: a_i^h = Σ_{r≤k} α_r b_i^r, with meta-weights α_r = (k − r + 1)/k
- top-k acceptability: T_i(f) = Σ_{r≤k} b_i^r

The distributions f are:
- (a) uniform Dirichlet(1), meaning no preference information;
- (b) four **SYNTHETIC** archetypes, each Dir(κ·μ) with κ = 40.

| archetype (SYNTHETIC) | μ = (access, need, green, heat, capacity, mix, cost) | literature motivation |
|---|---|---|
| young single worker | .30 .20 .08 .07 .10 .10 .15 | transit and price sensitivity of young renters (EHS private-renter segmentation, report §3) |
| family with children | .12 .12 .25 .15 .08 .18 .10 | green, schools and mix (report §3 "una famiglia con figli pesa scuole e verde") |
| elderly | .25 .08 .17 .30 .05 .10 .05 | heat vulnerability of over-65s (Kovats & Hajat 2008) [canonical, from memory]; proximity |
| commuter | .40 .10 .05 .05 .10 .05 .25 | access and cost |

Two group-robust statistics are computed:
- **Robust-for-all** = min_g T_i(f_g).
- **Archetype GIC** = Π_g (T_i(f_g)·S + 1)/(S + 2): the Polis group-informed consensus with Laplace smoothing, applied to SMAA acceptabilities.

The archetypes are used **only** to weight parcels. They are never used to score households (AI Act Annex III 5(a)).

## 3. Learning loop: Bayesian pairwise preference learning

**Question.** "Which of these two real parcels is better for you, a or b?" The answer is y ∈ {0, 1}.

**Likelihood.** Bradley–Terry / logit with a lapse rate (Bradley & Terry 1952; Luce 1959; Wichmann & Hill 2001 for lapse) [canonical, from memory]:

  P(y = 1 | w) = ε + (1 − 2ε)·σ(β·w·(s_a − s_b)),  β = 15, ε = 0.05.

The lapse ε bounds the influence of any single answer, so one careless click cannot zero out a hypothesis. β is fixed at the "medium noise" value, and E2 tests mis-specification against it.

**Prior.** Dirichlet(1), or the population prior of §4.

**Posterior.** The posterior is p(w | D) ∝ p(w) Π_t P(y_t | w). It is represented by P = 2,000 weighted particles (sequential importance sampling).

When the effective sample size 1/Σπ² falls below P/3, the engine runs a **resample-move** step (Gilks & Berzuini 2001; Chopin 2002) [canonical, from memory]:
- multinomial resampling;
- four Metropolis–Hastings moves with Dirichlet random-walk proposals w′ ~ Dir(c·w), c = 150.

The acceptance ratio is

  [p(w′) L(D | w′) Dir(w | c w′)] / [p(w) L(D | w) Dir(w′ | c w)].

This is exact Bayesian inference in the limit P → ∞, with no Laplace or Gaussian approximation on the simplex. That matters because posteriors pile up on the faces of the simplex.

**Active question selection.** At each step 200 non-dominated pairs of short-listed parcels are drawn. Pairs where one parcel Pareto-dominates the other are excluded, because their answer carries no trade-off. The pair maximising one of two scores is asked:

- **EIG-w (BALD; Houlsby et al. 2011; Lindley 1956)** [canonical, from memory]:
  I(y; w) = H(Σ_p π_p P_p) − Σ_p π_p H(P_p).
- **EIG-top (decision-focused):** I(y; τ), where τ(w) = argmax_i w·s_i is the identity of the respondent's best parcel. With T the particles × top-parcel one-hot matrix, q_y = (π ⊙ P_y)ᵀ T:
  I = H(πᵀT) − Σ_y p̄_y H(q_y / p̄_y).
  This targets only the uncertainty that changes the decision, in the spirit of Chajewska, Koller & Parr 2000 and the regret-based elicitation of Viappiani & Boutilier 2010 [canonical, from memory].

Both scores are evaluated exactly over the particles: one (P × 200) matrix product per question, a few milliseconds.

**Stopping rule (proposed, not tested).** Stop when max_i P(τ = i) ≥ 0.8, or when max EIG < 0.02 nats, or after 12 questions.

**Teach-back after each answer.** Show the current top parcels and the flip explanation of §6.

## 4. Cybernetic loop across participants (empirical Bayes)

Participant n + 1 starts from

  p_{n+1}(w) = ρ·Dir(w | 1) + (1 − ρ)·(1/n) Σ_{j≤n} Dir(w | κ_p·ŵ_j),  ρ = 0.3, κ_p = 50,

where ŵ_j is the posterior mean of participant j. The system therefore asks fewer questions as the population grows (Robbins 1956 empirical Bayes [canonical, from memory]; Guo & Sanner 2010 used population priors for pairwise elicitation [canonical, from memory]).

**Risk (Sanchez's critique, report §1).** A population prior pulls newcomers toward the majority. This is exactly the "amplification of existing tendencies" the platform must avoid.

Two guards are in place:
1. The uniform component ρ = 0.3 keeps every region of the simplex reachable.
2. E3 audits the error **separately for the minority**. The prior is kept only if the minority error does not increase.

Both enter the mixture density in the MH ratio exactly.

## 5. Aggregation that preserves heterogeneity

Inputs are each participant's learned utilities U_ni = ŵ_n·s_i on the short-list. Each rule outputs a set S of K = 10 parcels (a committee).

| rule | definition | known properties [canonical, from memory] |
|---|---|---|
| mean weights | top-K of (mean_n ŵ_n)·s | Pareto on weights; erases variety (report "Non applicare") |
| Borda | top-K of Σ_n rank_n(i) | positional, monotone; not Condorcet-consistent |
| Kemeny | exact ILP (HiGHS via `scipy.milp`) on the top-20 by Borda: min Σ disagreements subject to transitivity, x_ab + x_bc + x_ca ∈ [1, 2] | Condorcet-consistent, the maximum-likelihood ranking (Young 1988); NP-hard in general |
| seq-PAV | approval = own top-K; greedy PAV | proportional; satisfies EJR in its exact form, seq-PAV only approximately (Aziz et al. 2017) |
| **GIC (group-informed consensus)** | cluster ŵ_n by k-means (k ∈ 2..5 by silhouette); P_g(i) = (#members of g with i in their top-K + 1)/(\|g\| + 2); GIC_i = Π_g P_g(i) | Polis (Small et al. 2021): rewards parcels liked *across* groups; a multiplicative veto for a group that rejects a parcel |

**Fairness metrics.** All use true SYNTHETIC weights.
- Normalised satisfaction: sat_n(S) = (ū_n(S) − ū_n(all)) / (ū_n(own top-K) − ū_n(all)). Averaged per group, then the worst group is taken.
- Justified representation (JR, Aziz et al. 2017): no set of ≥ N/K voters who share an approved parcel may be left with no approved parcel in S.
- The share of minority members with ≥ 1 of their own top-K in S.

## 6. Explanation layer (teach-back)

For a pair where a currently beats b under w (g = w·(s_a − s_b) > 0, d = s_a − s_b), the engine computes two things.

**Minimal L1 flip (LP).** Solve

  min ‖w′ − w‖₁  s.t.  w′ ∈ Δ, w′·d ≤ 0.

The problem is written with w′ = w + p − q, p, q ≥ 0, and solved with HiGHS. The answer is reported as "points out of 100 to move" plus w′. The problem is infeasible exactly when a Pareto-dominates b. Then the message is "no weighting can put b above a; a is at least as good on every criterion."

**Single-criterion flip (closed form).** Raise criterion j and shrink the others proportionally: w(t) = (1 − t)w + t e_j. The flip happens at

  t* = g / (g − d_j)  for d_j < 0,

and the new weight of j is (1 − t*) w_j + t*. The easiest j becomes one sentence for the chat, for example: "'015200.232' would overtake '015400.27' if green rose from 11.5% to 12.2% of your weight." The chat **explains**. It never proposes weights or rankings (report "Non applicare").

## 7. Novelty claim (relative to the literature cited)

Every ingredient exists separately: SMAA-2, Bradley–Terry, Bayesian elicitation with EIG, Polis GIC, PAV/JR. The proposal combines them as follows:

1. **Distribution-valued participation.** Each person is a posterior over w. SMAA is run on posterior and group mixtures, not on an analyst's uniform prior. SMAA studies normally use uniform or analyst-specified intervals. Here the weight density is *learned from citizens' choices between real parcels*.
2. **Decision-focused question selection on a real spatial choice set (EIG-top).** It is compared with BALD on w and with random questions on real Milan parcels.
3. **Exact dominance-depth reduction** for top-k SMAA on ~10⁴ alternatives.
4. **GIC on SMAA acceptabilities.** Polis's product-of-group-agreement is applied to "P(parcel in my top-k)" instead of to agree/disagree votes. It is audited with JR and per-group satisfaction against Borda, Kemeny and PAV.
5. **An audited empirical-Bayes cybernetic loop.** The population prior speeds up learning, and an explicit minority-error test guards against majority amplification.
6. **LP teach-back** giving the minimal weight change that flips a pair, plus a one-criterion sentence for non-experts.

To my knowledge (not systematically searched in this session), no published GIS-MCDA site-selection study for social housing learns citizen weight *distributions* from pairwise choices between real sites. The report likewise found expert AHP to be dominant.

## 8. Limitations

- **Synthetic preferences.** All E2–E5 respondents and the archetypes are synthetic. Real citizens may be non-compensatory (veto, lexicographic), which WLC with a logit cannot represent. A remedy is to add OWA or veto thresholds as hard constraints chosen by the person.
- **Criteria are proxies.** Four of the seven criteria are NIL-level (ecological), so parcels of one NIL tie on them. The top of every ranking is crowded by clusters of adjacent parcels from one NIL (23 of the top-100 by holistic acceptability are in Cimiano–Rottole–Feltre). Two fixes are needed upstream: parcel aggregation into sites, and portfolio or concentration constraints (the MILP of the report). `e5` already shows a one-parcel-per-NIL list.
- **Normalisation dependence.** Robust min-max ties the weights to this pool. Learned weights must be re-elicited, or carried over in raw units, if the pool changes.
- **Logit noise is fixed (β = 15).** In E2, high noise and flip noise test the misspecification. A hierarchical β per person is a natural extension.
- **Inference cost.** The particle filter is exact only asymptotically. P = 2,000 was chosen for speed, and the posterior mean error at P = 2,000 vs larger P was not quantified.
- **Learned population prior.** It can still shift minorities. The guard ρ = 0.3 is a design choice, not an optimum.
- **Self-selection is not modelled.** The canal aperto vs panel sorteggiato design and reweighting on census margins are not modelled here (report §3).
- **Approximate rules.** Kemeny is exact only on the top-20 by Borda. seq-PAV is the greedy approximation of PAV.
- **GIC behaviour.** GIC with many small groups is very peaked: products of small probabilities. Its ranking is shown, not its absolute values.
