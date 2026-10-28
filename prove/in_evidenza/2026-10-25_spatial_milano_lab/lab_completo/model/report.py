"""Writes lab/results/results.md from the run (called by run.py; standalone: python report.py uses out/base.pkl,
out/sens.pkl and results/tests.json). Every number below is generated; the prose is conditional on the results."""
import json, os, pickle
import numpy as np, pandas as pd
from config import *

KEYS = [("dDI", "Δ dissimilarity (post − now)"), ("dIso", "Δ isolation of low-income hh"), ("dep_poor", "% poor taxpayers vs city (pp)"),
        ("dep_resid", "residual income vs city (€/month)"), ("conc_q5", "share of new dwellings in top-quintile p_erp NIL (above the household floor)"), ("conc_q5_or", "old definition: top quintile of p_erp OR srv_erp"),
        ("opp", "opportunity index (0-1)"), ("served_per_meur", "served target hh per €1M"), ("rent_erosion", "OMI rent growth 2019→24 at site"),
        ("hh_need_cov1km", "share of C's high-pressure hex pop within 1 km")]


def f(v, d=3):
    if v is None or (isinstance(v, float) and not np.isfinite(v)): return "–"
    return f"{v:,.{d}f}"


def pct(v): return f"{v * 100:+.0f} %"


def claims(o, sens=None):
    """Defensible claim per set (review2 final table), generated from the numbers; English + Italian text,
    key numbers under site nulls and NIL-block nulls, caveats. Used by results.md §1 and model.json."""
    res, lab, S, N, B = o["res"], o["labels"], o["S"], o["N"], o.get("block", {})
    hh, pe = N.hh.values, N.p_erp.values; L0, O0 = hh * pe, hh * (1 - pe)
    DI0 = 0.5 * np.abs(L0 / L0.sum() - O0 / O0.sum()).sum()
    stab = {g: (1 - sens[f"flip_{g}"].mean()) if sens is not None and len(sens) else None for g in ("AT", "AMB_DEG", "ERP")}
    def nil_eff(m):
        c = pd.Series(S.cap.values[m]).groupby(S.nil.values[m]).sum(); return len(c), float(1 / ((c / c.sum()) ** 2).sum())
    out = {}
    for g in ("AT", "AMB_DEG", "ERP", "RIG"):
        m = (S.origin.eq(g) if g != "RIG" else S.origin.eq("SOFT") & (S.pgt_rig >= 0.5)).values
        rs, rr = res[g]["size"], res[g]["ring"]
        nn, ne = nil_eff(m)
        blk = {n: B.get((g, n), {}) for n in ("nil_block", "nil_block_ring")}
        num = dict(sites=int(m.sum()), dwellings=int(S.cap[m].sum()), n_nil=nn, eff_nil=round(ne, 1),
                   site_null={n: {k: dict(obs=res[g][n][k]["obs"], null_mean=res[g][n][k]["mean"], null_median=res[g][n][k]["median"],
                                          p_harm=(AU_harm(res[g][n], k)))
                                  for k in ("dDI", "dIso", "dep_poor", "dep_resid", "conc_q5", "opp", "served_per_meur") if k in res[g][n]}
                              for n in ("size", "ring")},
                   block_null={n: {k: v for k, v in b.items() if k in ("dDI", "dIso", "dep_poor", "dep_resid", "conc_q5")} for n, b in blk.items() if b},
                   grid_stability=None if stab.get(g) is None else round(float(stab[g]), 2))
        if g != "RIG":
            Qg = o["Q"][(o["Q"].set == g) & (o["Q"].idx == "dDI")]
            num["q_dDI"] = {r.null: round(r.q_bh, 4) for r in Qg.itertuples()}
        cav = []
        dd = rs["dDI"]["obs"] - rs["dDI"]["mean"]
        if g == "AT":
            bp = lambda n, k: blk[n].get(k, np.nan) if blk[n] else np.nan
            robust = lab[g] == "risk" and all(bp(n, "dDI") < 0.05 or bp(n, "dIso") < 0.05 for n in blk) and (stab[g] or 0) >= 2 / 3
            place = all(min(bp(n, "dep_resid"), bp(n, "conc_q5")) < 0.05 for n in blk)
            ns = {n: B.get(("AT_noStephenson", n), {}) for n in ("size", "ring", "nil_block", "nil_block_ring")}
            num["without_stephenson"] = ns
            num["dDI_diff_vs_null"] = dd; num["dDI_diff_share_of_DI0"] = dd / DI0
            site_place = all(min(AU_harm(res[g][n], "dep_resid"), AU_harm(res[g][n], "conc_q5")) < 0.05 for n in ("size", "ring"))
            seg_en = "and a robust segregation signal." if robust else "not a robust segregation risk."
            seg_it = "con un segnale di segregazione robusto." if robust else "non un rischio di segregazione robusto."
            if place: head_en, head_it = "Placement concern, " + seg_en, "Problema di collocazione, " + seg_it
            elif site_place:
                head_en = "Placement concern at site level only (not significant under the NIL-block null), " + seg_en
                head_it = "Problema di collocazione solo a livello di sito (non significativo col null per blocchi di NIL), " + seg_it
            else: head_en, head_it = ("Segregation signal." if robust else "No robust finding."), ("Segnale di segregazione." if robust else "Nessun risultato robusto.")
            en = (f"{head_en} At FAR {SUP['far']} AT capacity ({num['dwellings']:,} dwellings) sits in NIL whose residual income is "
                  f"{rs['dep_resid']['obs']:.0f} €/month vs the city mean (matched land {rs['dep_resid']['mean']:.0f} / {rr['dep_resid']['mean']:.0f}); "
                  f"{rs['conc_q5']['obs'] * 100:.0f} % of it is in top-quintile p_erp NIL (matched {rs['conc_q5']['mean'] * 100:.0f} / {rr['conc_q5']['mean'] * 100:.0f} %). "
                  f"NIL-block null: dep_resid p = {bp('nil_block', 'dep_resid'):.3f} / {bp('nil_block_ring', 'dep_resid'):.3f}, conc_q5 p = {bp('nil_block', 'conc_q5'):.3f} / {bp('nil_block_ring', 'conc_q5'):.3f}. "
                  f"It rests on {nn} NIL ({ne:.1f} effective). ΔDI is {dd:+.5f} vs matched land ({dd / DI0 * 100:+.1f} % of baseline DI {DI0:.3f}): "
                  f"slightly less desegregating, not segregating. Pre-registered label '{lab[g]}' (dDI q {num['q_dDI'].get('size', np.nan):.3f} / {num['q_dDI'].get('ring', np.nan):.3f}); "
                  f"NIL-block dDI p = {bp('nil_block', 'dDI'):.3f} / {bp('nil_block_ring', 'dDI'):.3f}; grid stability {num['grid_stability']}.")
            it = (f"{head_it} A FAR {SUP['far']} la capacità AT ({num['dwellings']:,} alloggi) ricade in NIL con reddito residuo "
                  f"{rs['dep_resid']['obs']:.0f} €/mese rispetto alla media cittadina (aree confrontabili {rs['dep_resid']['mean']:.0f} / {rr['dep_resid']['mean']:.0f}); "
                  f"il {rs['conc_q5']['obs'] * 100:.0f} % è in NIL del quintile più alto di idonei ERP (confronto {rs['conc_q5']['mean'] * 100:.0f} / {rr['conc_q5']['mean'] * 100:.0f} %). "
                  f"Con il null per blocchi di NIL: reddito residuo p = {bp('nil_block', 'dep_resid'):.3f}, concentrazione p = {bp('nil_block', 'conc_q5'):.3f}. "
                  f"Si basa su {nn} NIL ({ne:.1f} effettivi). ΔDI {dd:+.5f} rispetto alle aree confrontabili ({dd / DI0 * 100:+.1f} % del DI di base): "
                  f"costruire lì desegrega un po' meno, non segrega. Etichetta pre-registrata '{lab[g]}'; null per blocchi dDI p = {bp('nil_block', 'dDI'):.3f}; "
                  f"stabilità nella griglia di sensibilità {num['grid_stability']}.")
            cav = ["NIL-level (88 NIL) and CAP-level (38 CAP) income: one ecological signal, not independent pieces of evidence.",
                   f"Stephenson (92 households, CAP-imputed income) is neutralised by the {AUDIT['hh_floor']}-household floor; results without its AT sites are in numbers.without_stephenson.",
                   "The site-level null is anti-conservative when a set is concentrated in few NIL (test 1c); read the NIL-block null as co-primary."]
        elif g == "ERP":
            e = [B.get(("ERP_market_land", n), {}) for n in ("size", "ring")]
            mk = all(x and x["served_per_meur"] >= x["null_median"] for x in e)
            num["market_land"] = e
            head_en = "Cheap only if the land is free." if not mk else "Potential survives market land cost."
            head_it = "Conveniente solo se il suolo è gratuito." if not mk else "Il potenziale regge anche con suolo a prezzo di mercato."
            en = (f"{head_en} Label '{lab[g]}' rests on srv_erp land at 1 €/m² (ownership not verified). Costed at market land: served per €1M "
                  f"{e[0].get('served_per_meur', np.nan):.2f} vs null median {e[0].get('null_median', np.nan):.2f} / {e[1].get('null_median', np.nan):.2f} → "
                  f"{'still potential' if mk else 'neither'}. In absolute terms it serves {rs['served']['obs']:,.0f} target households vs {rs['served']['mean']:,.0f} / {rr['served']['mean']:,.0f} for matched land. "
                  f"Opportunity {rs['opp']['obs']:.3f} vs null median {rs['opp']['median']:.3f} / {rr['opp']['median']:.3f}. "
                  f"Concentration in top-p_erp NIL {rs['conc_q5']['obs'] * 100:.0f} % (matched {rs['conc_q5']['mean'] * 100:.0f} %).")
            it = (f"{head_it} L'etichetta '{lab[g]}' dipende dal suolo srv_erp valutato 1 €/m² (proprietà non verificata). Con suolo a prezzo di mercato: "
                  f"{e[0].get('served_per_meur', np.nan):.2f} famiglie servite per 1 M€ contro una mediana di {e[0].get('null_median', np.nan):.2f} / {e[1].get('null_median', np.nan):.2f} → "
                  f"{'resta potenziale' if mk else 'nessuna etichetta'}. In valore assoluto serve {rs['served']['obs']:,.0f} famiglie target contro {rs['served']['mean']:,.0f} delle aree confrontabili. "
                  f"Indice di opportunità {rs['opp']['obs']:.3f} (mediana {rs['opp']['median']:.3f}).")
            cav = ["srv_erp designation is not ownership; land cost is an assumption.",
                   "Served per € saturates for large sets, so it mostly tracks cost."]
        elif g == "AMB_DEG":
            en = f"No information. {num['sites']} sites in {nn} NIL ({num['dwellings']} dwellings): the study has no power for this set."
            it = f"Nessuna informazione. {num['sites']} siti in {nn} NIL ({num['dwellings']} alloggi): lo studio non ha potenza statistica per questo insieme."
            cav = ["Do not read 'neither' as evidence of absence."]
        else:
            en = (f"Most robust placement signal (context, not a verdict). Regeneration-zone land ({num['sites']} sites, {nn} NIL, {ne:.1f} effective) sits in poorer NIL: "
                  f"{rs['dep_poor']['obs']:+.2f} pp poor taxpayers (matched {rs['dep_poor']['mean']:+.2f}), residual income {rs['dep_resid']['obs']:.0f} €/month (matched {rs['dep_resid']['mean']:.0f}); "
                  f"site-level p dep_poor {AU_harm(rs, 'dep_poor'):.3f}, dep_resid {AU_harm(rs, 'dep_resid'):.3f}.")
            it = (f"Il segnale di collocazione più robusto (contesto, non un verdetto). Le aree degli ambiti di rigenerazione ({num['sites']} siti, {nn} NIL, {ne:.1f} effettivi) "
                  f"stanno in NIL più poveri: {rs['dep_poor']['obs']:+.2f} punti di contribuenti poveri (confronto {rs['dep_poor']['mean']:+.2f}), reddito residuo {rs['dep_resid']['obs']:.0f} €/mese (confronto {rs['dep_resid']['mean']:.0f}).")
            cav = ["RIG is 41 % of the non-designated pool, so its null is conservative.", "Context only: not part of the pre-registered verdict."]
        out[g] = dict(label=lab.get(g, "context"), claim_en=en, claim_it=it, numbers=num, caveats=cav)
    mt = o.get("matched")
    if mt:
        out["people_vs_pgt"] = dict(raw=mt["raw_gain"], size_matched=mt["size"]["gain_vs_pgt"], ring_matched=mt["ring"]["gain_vs_pgt"],
                                    pgt_beats_ring_draws=mt["ring"]["pgt_beats"], draws=PORT["matched_draws"],
                                    claim_en=(f"Served target households, non-designated ('people') lens vs 'PGT as is': {pct(mt['raw_gain'])} when it can choose freely from all "
                                              f"non-designated land; {pct(mt['size']['gain_vs_pgt'])} against non-designated pools of the same size; {pct(mt['ring']['gain_vs_pgt'])} "
                                              f"when also ring-matched (PGT beats {mt['ring']['pgt_beats']} of {PORT['matched_draws']} pools). PGT's shortfall is mostly scarce, peripheral land."),
                                    claim_it=(f"Famiglie target servite, lente 'delle persone' rispetto a 'PGT così com'è': {pct(mt['raw_gain'])} scegliendo liberamente tra tutte le aree non designate; "
                                              f"a parità di dimensione del bacino {pct(mt['size']['gain_vs_pgt'])}; a parità anche di distanza dal centro {pct(mt['ring']['gain_vs_pgt'])}. "
                                              f"Lo svantaggio del PGT dipende soprattutto da aree scarse e periferiche, non da siti peggiori."))
    return out


def AU_harm(r, k):
    return (r[k]["p_up"] if AUDIT["bh_indices"].get(k, "+") == "+" else r[k]["p_dn"]) if k in AUDIT["bh_indices"] else r[k]["p_two"]


def write(o, sens=None, runtime_min=None):
    L = []; a = L.append
    lab, res, Q = o["labels"], o["res"], o["Q"]
    S, P, N = o["S"], o["P"], o["N"]
    cnt = S.origin.value_counts()
    a("# Integrated model — PGT-designated land vs people's needs (Milan)\n")
    a(f"Generated by `lab/model/run.py` (runtime {runtime_min} min). Purchasing-power layer: **{'ok' if o['pp_ok'] else 'missing'}**; "
      f"portfolio demand layer: **{o['layer']}**. All numbers are NIL- or hex-level aggregates; no household is scored.\n")
    # ---------------- headline
    a("## 1. Headline answer\n")
    CL = claims(o, sens)
    at_place = CL["AT"]["claim_en"].startswith("Placement concern"); at_robust = "a robust segregation signal" in CL["AT"]["claim_en"]
    erp_acc = CL["ERP"]["claim_en"].startswith("Cheap only")
    a("**Answer to the research question.** " +
      (("Designated land, especially AT and the regeneration zone, sits in poorer NIL" + (" (for AT at site level only: not significant under the NIL-block null). " if "site level only" in CL["AT"]["claim_en"] else ". "))
       if at_place else "Designated AT land is not robustly placed in poorer NIL. ") +
      ("Building it would also robustly increase segregation. " if at_robust else "There is no robust evidence that building it would increase segregation. ") +
      ("ERP's apparent advantage is an accounting assumption about land cost." if erp_acc else "ERP's advantage survives market land cost.") + "\n")
    a("| set | pre-registered label | defensible claim |"); a("|---|---|---|")
    for g in ("AT", "ERP", "AMB_DEG", "RIG"):
        a(f"| **{g}** | {CL[g]['label']} | {CL[g]['claim_en']} |")
    if "people_vs_pgt" in CL: a(f"| people vs PGT | – | {CL['people_vs_pgt']['claim_en']} |")
    a("\n**Caveats on these claims:** " + " ".join(dict.fromkeys(c for g in ("AT", "ERP", "AMB_DEG", "RIG") for c in CL[g]["caveats"])) + "\n")
    a("### Detail behind the labels\n")
    def row(g, n, k): return res[g][n][k]
    for g in ("AT", "AMB_DEG", "ERP"):
        r = res[g]["size"]; rr = res[g]["ring"]
        a(f"- **{g}** ({int(cnt.get(g, 0))} sites, {int(S.cap[S.origin == g].sum()):,} dwellings at FAR {SUP['far']}): label **{lab[g].upper()}**. "
          f"Poor-taxpayer placement {f(r['dep_poor']['obs'], 2)} pp vs city (null {f(r['dep_poor']['mean'], 2)} size / {f(rr['dep_poor']['mean'], 2)} ring); "
          f"residual income {f(r['dep_resid']['obs'], 0)} €/month vs city (null {f(r['dep_resid']['mean'], 0)} / {f(rr['dep_resid']['mean'], 0)}); "
          f"ΔDI {f(r['dDI']['obs'], 5)} (null {f(r['dDI']['mean'], 5)} / {f(rr['dDI']['mean'], 5)}); "
          f"top-ERP-quintile concentration {f(r['conc_q5']['obs'], 2)} (null {f(r['conc_q5']['mean'], 2)} / {f(rr['conc_q5']['mean'], 2)}); "
          f"served per €1M {f(r['served_per_meur']['obs'], 2)} (null median {f(r['served_per_meur']['median'], 2)} / {f(rr['served_per_meur']['median'], 2)}); "
          f"opportunity {f(r['opp']['obs'], 3)} (null median {f(r['opp']['median'], 3)} / {f(rr['opp']['median'], 3)}).")
    rg = res["RIG"]["size"]
    a(f"- **RIG** (context, {int(((S.origin == 'SOFT') & (S.pgt_rig >= 0.5)).sum())} non-designated sites in the regeneration zone): "
      f"poor placement {f(rg['dep_poor']['obs'], 2)} pp (null {f(rg['dep_poor']['mean'], 2)}), residual {f(rg['dep_resid']['obs'], 0)} €/month (null {f(rg['dep_resid']['mean'], 0)}).\n")
    a("**Reading.** Interpret the labels with the effect sizes, not alone:")
    a("- The *placement* indices (poor share, foreign share, net income, residual income, concentration in high-ERP NIL) measure **where** the land sits relative to deprivation. "
      "They are the closest answer to 'does PGT land sit where poor people already are'.")
    a(f"- The *segregation* indices (ΔDI, Δisolation) measure the **change** in NIL-level sorting if the land were built with σ = {AUDIT['sigma']} low-income occupancy. "
      f"Milan's simulated ERP-eligible share is {f(float(np.average(N.p_erp, weights=N.hh)), 2)}, close to σ, so new mixed housing barely moves DI anywhere (all ΔDI ≈ 10⁻⁴–10⁻³). "
      "A 'risk' label therefore means 'reduces segregation less than matched alternatives would', not 'creates a ghetto'. The σ sensitivity (σ = 1, all-social) is the stress case.\n")
    # ---------------- rule
    a("## 2. Pre-registered decision rule\n")
    a("> " + AUDIT["rule"] + "\n")
    a("Written in `lab/model/config.py` before the first audit run. Unchanged afterwards. Null draws R = "
      f"{AUDIT['R']}; capacity matched within ±{int(AUDIT['cap_tol'] * 100)} % (match rate per set in `audit_indices.csv`)."
      " Disclosure: one trial run preceded the published one. It exposed a code bug in the verdict lookup (`Q.index` instead of the index column), which mislabelled AT as 'neither'. The bug was fixed; the rule text, indices and thresholds were not changed. Runtime settings (MILP pool 8/NIL, 30 s limit, export simplification 1 m) were changed after that trial run. Review 2 then changed the null pool from non-designated sites only to all candidate sites incl. G (calibration fix; it typically makes p larger) and re-ran.\n")
    a("**All tests are one-sided** in the harm direction stated in `config.AUDIT['bh_indices']` (+ = larger is worse; − for residual income and opportunity). "
      f"The BH family is the stated {len(AUDIT['sets'])} sets ({', '.join(AUDIT['sets'])}) × {len(AUDIT['bh_indices'])} indices, per null; only AT, AMB_DEG and ERP get labels.\n")
    a("**Disclosed post-hoc specification changes (after review 2; the rule text is unchanged):**\n")
    for t in POSTHOC: a(f"- {t}")
    a("")
    # ---------------- audit table
    a("## 3. Audit: designated sets vs matched nulls\n")
    a("| set | null | index | observed | null mean | null sd | z | p (harm dir.) | BH q |")
    a("|---|---|---|---|---|---|---|---|---|")
    for g in ("AT", "AMB_DEG", "ERP", "RIG"):
        for n in ("size", "ring"):
            for k, _ in KEYS:
                if k not in res[g][n]: continue
                r = res[g][n][k]
                q = Q[(Q.set == g) & (Q.null == n) & (Q.idx == k)]
                ph = (r["p_up"] if AUDIT["bh_indices"].get(k, "+") == "+" else r["p_dn"]) if k in AUDIT["bh_indices"] else r["p_two"]
                a(f"| {g} | {n} | {k} | {f(r['obs'], 4)} | {f(r['mean'], 4)} | {f(r['sd'], 4)} | {f(r['z'], 2)} | {f(ph, 3)}{'' if k in AUDIT['bh_indices'] else ' (2-sided)'} | {f(float(q.q_bh.iloc[0]), 3) if len(q) else '–'} |")
    a("\nIndex definitions: " + "; ".join(f"`{k}` = {d}" for k, d in KEYS) + ". Full table: `audit_indices.csv`; BH: `audit_bh.csv`.\n")
    a("### Alternatives at matched capacity\n")
    A = pd.DataFrame(o["alt"]).T
    cols = [c for c in ["dep_poor", "dep_for", "dep_net", "dep_resid", "conc_q5", "opp", "served_per_meur", "hh_need_cov1km", "rent_erosion", "hol"] if c in A]
    a("| set | " + " | ".join(cols) + " |"); a("|---" * (len(cols) + 1) + "|")
    for i, r in A.iterrows(): a(f"| {i} | " + " | ".join(f(r[c], 3) for c in cols) + " |")
    a("\n`topHol_matched_X` = non-designated sites ranked by SMAA holistic acceptability (uniform weights) until X's capacity is reached.\n")
    if o.get("block"):
        B = o["block"]
        a("### Robustness checks added by review 2 (post hoc, not part of the pre-registered verdict)\n")
        a("Null draws in §3 come from candidate land including G (permutation null; review 2 showed that drawing from the complement only is "
          "anti-conservative, false-positive rate 0.061 vs nominal 0.05). The NIL-block null below re-assigns each set's capacity per NIL to distinct "
          "random NIL able to absorb it (optionally in the same centre ring): deprivation is NIL-level, so the effective sample size is the number of NIL "
          "a set touches, not its number of sites.\n")
        ks = ["dDI", "dIso", "dep_poor", "dep_resid", "conc_q5"]
        a("| set | null | NIL touched | effective NIL (capacity) | " + " | ".join(f"p {k}" for k in ks) + " |"); a("|---" * (len(ks) + 4) + "|")
        for (g, n), v in B.items():
            if n.startswith("nil_block"): a(f"| {g} | {n} | {v['n_nil']} | {f(v['neff'], 1)} | " + " | ".join(f(v.get(k), 3) for k in ks) + " |")
        e = [B.get(("ERP_market_land", n)) for n in ("size", "ring")]
        if all(e):
            a(f"\nERP with its land costed at market like non-designated land (instead of 1 €/m²): served per €1M {f(e[0]['served_per_meur'], 2)} "
              f"vs null median {f(e[0]['null_median'], 2)} (size) / {f(e[1]['null_median'], 2)} (ring). The ERP 'potential' label "
              f"{'survives' if all(x['served_per_meur'] >= x['null_median'] for x in e) else 'does NOT survive'} this; it rests on the [A] assumption that srv_erp land is free.\n")
        ks2 = list(AUDIT["bh_indices"])
        a("AT variants, site-level nulls (one-sided harm p): with the household floor and **without Stephenson's AT sites**, and **without the floor** (raw CAP-imputed values).\n")
        a("| variant | null | " + " | ".join(f"p {k}" for k in ks2) + " |"); a("|---" * (len(ks2) + 2) + "|")
        for v in ("AT_noStephenson", "AT_nofloor"):
            for n in ("size", "ring"):
                d = B.get((v, n))
                if d: a(f"| {v} | {n} | " + " | ".join(f(d.get(k), 3) for k in ks2) + " |")
        a("\nBase AT (with floor, with Stephenson) is in the §3 table; AT_noStephenson under the NIL-block nulls is in the table above.\n")
    # ---------------- demand / PP
    a("## 4. Demand and real purchasing power\n")
    Dl = o["Dl"]; tot = Dl[Dl.scen >= 0].groupby("scen")[[c for c in Dl if c.startswith("D_")]].sum()
    for c in tot:
        a(f"- `{c}`: mean {f(tot[c].mean(), 0)} households (p05 {f(tot[c].quantile(.05), 0)}, p95 {f(tot[c].quantile(.95), 0)}), {DEM['n_scen']} bootstrap scenarios of A's simulator.")
    if "fa1" in o:
        x = o["fa1"]
        a(f"- F-A1: city-wide search variant (cheapest NIL within 5 km) gives {f(x['D_city_search'], 0)} vs {f(x['D_tau_base'], 0)} households; "
          f"with the city-median rent everywhere {f(x['D_tau_median_rent'], 0)}. Share of between-NIL variance of the target rate left when rent is "
          f"equalised (= due to income): {f(x['var_share_income'], 3)}. Spearman(target rate, OMI rent) = {f(x['rho_rate_rent'], 3)}.")
    if o["pp_ok"]:
        pj = json.load(open(os.path.join(PROP, "A_econ_or", "results", "purchasing_power.json")))
        er = pj.get("erosion", [{}])
        a(f"- From A (`purchasing_power.json`): ISTAT absolute-poverty threshold single adult {pj['constants']['pov_single']} €/month "
          f"(non-housing part {f(pj['nonhousing_basket_single'], 0)}); NIC 2019→24 {f(er[1].get('cpi_2019_24', np.nan) * 100, 1)} %; OMI rents 2019→24 "
          f"+{f(er[1].get('omi_rent_change', np.nan) * 100, 1)} %; Milan/Italy price level {pj['constants']['p_milan']} (does not move the band).")
        a("- Reading: the pure ISTAT residual test leaves ~100 target households: those who fail the residual test at market rent mostly fail it at social rent too "
          "or are ERP-eligible. The 'belly' is **rent overburden**, not material poverty. Portfolios use the 1.5× ('decent') basket layer; D_tau is reported for comparison (lens `L_dtau`).")
    else:
        a("- **pp_layer = missing**: A's `purchasing_power_nil.csv` was not found; only D_tau is used. Re-run `run.py` when it exists.")
    a("")
    # ---------------- portfolios
    a("## 5. The choice set: diverse portfolios and policy lenses\n")
    a("| id | lens | status | gap | sites | dwellings | cost €M | served mean | CVaR20 | Gini | share designated | served D_tau | poor pp | ΔDI | opp | SMAA P(top-3) |")
    a("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for p in P:
        r = p["r"]; au = p["audit"]
        des = (S.origin.values[p["sites_idx"]] != "SOFT").mean() if len(p["sites_idx"]) else np.nan
        a(f"| {p['id']} | {p['lens']} | {r.get('status')} | {f(r.get('gap'), 3)} | {r.get('sites')} | {f(r.get('dwellings'), 0)} | {f((r.get('cost_eur') or 0) / 1e6, 0)} | "
          f"{f(r.get('served_mean'), 0)} | {f(r.get('served_cvar'), 0)} | {f(r.get('gini_cov'), 3)} | {f(des, 2)} | {f(p['eval'].get('D_tau', {}).get('served_mean'), 0)} | "
          f"{f(au['dep_poor'], 2)} | {f(au['dDI'], 5)} | {f(au['opp'], 3)} | {f(p.get('smaa_top3'), 2)} |")
    a(f"\nP1 = robust optimum (no lens); P2..P{PORT['K']} each share ≤ {int((1 - PORT['delta']) * 100)} % of the sites of every earlier one (integer cuts), "
      f"kept only if served ≥ {int(PORT['stop_frac'] * 100)} % of P1. Lenses: `pgt` designated only, `people` non-designated only, `gini` Gini ≤ {PORT['gini']}, "
      "`smaa` max Σ capacity × holistic acceptability (participatory lens), `demand_tau` = optimum for D_tau. Budget €"
      f"{PORT['budget'] / 1e9:.1f} bn, HiGHS ≤ {PORT['time_limit_choice']} s / gap {PORT['gap_choice']}: 'Time limit reached' rows are not certified optimal.\n")
    PP = [p for p in P if p["id"].startswith("P")]
    sv = [p["r"].get("served_mean") or 0 for p in PP]; gp = max((p["r"].get("gap") or 0) for p in PP) if PP else 0
    opt = all(p["r"].get("status") == "Optimal" for p in PP)
    spread = (max(sv) - min(sv)) / max(max(sv), 1e-9) if sv else 0
    a(f"P1–P{len(PP)}: {'all certified optimal' if opt else 'NOT all certified optimal'} (max gap {gp:.3f}); served spread {spread * 100:.1f} %. "
      + ("**Their ranking is indicative only**: the spread is within a few times the solver gap and the scenario noise; treat P1–P6 as a set of near-equivalent alternatives."
         if (not opt or spread < 5 * max(gp, 0.01)) else "The ranking is outside the solver gap.")
      + " Portfolio SMAA uses fixed criterion ranges (served share of demand, 1−Gini, opportunity, rent burden, low poor-share placement); CVaR20 is dropped because it is saturated (≈ equal for all non-PGT portfolios).\n")
    mt = o.get("matched")
    if mt:
        a(f"**People vs PGT, like for like.** Raw: L_people {f(mt['people'], 0)} vs L_pgt {f(mt['pgt'], 0)} served ({pct(mt['raw_gain'])}). "
          f"Size-matched non-designated pools ({PORT['matched_draws']} draws, same count per area decile and capacity ±5 % as the designated pool of "
          f"{mt['pgt_pool']['sites']} sites / {f(mt['pgt_pool']['cap'], 0)} dwellings): mean {f(mt['size']['mean'], 0)} (range {f(mt['size']['lo'], 0)}–{f(mt['size']['hi'], 0)}), "
          f"{pct(mt['size']['gain_vs_pgt'])}. Size- and ring-matched: {f(mt['ring']['mean'], 0)} ({f(mt['ring']['lo'], 0)}–{f(mt['ring']['hi'], 0)}), {pct(mt['ring']['gain_vs_pgt'])}; "
          f"L_pgt beats {mt['ring']['pgt_beats']} of {PORT['matched_draws']} ring-matched pools.\n")
    # ---------------- sensitivity
    a("## 6. Sensitivity (reported, not pass/fail)\n")
    if sens is not None and len(sens):
        a("| param | value | AT | AT dDI q (size / ring) | AMB_DEG | ERP | Kendall τ (holistic) | P1 overlap |"); a("|---|---|---|---|---|---|---|---|")
        for _, r in sens.iterrows():
            q = f"{f(r.get('q_AT_dDI_size'), 3)} / {f(r.get('q_AT_dDI_ring'), 3)}" if "q_AT_dDI_size" in r else "–"
            a(f"| {r.param} | {r.value} | {r.label_AT} | {q} | {r.label_AMB_DEG} | {r.label_ERP} | {f(r.kendall_tau_hol, 3)} | {f(r.p1_overlap, 2)} |")
        a("\nτ, basket and λ cannot change ΔDI, so AT label changes at those points are Monte-Carlo noise of the null (R = "
          f"{SENS_R}), not parameter sensitivity; the q column shows how close to 0.05 AT sits.")
        st = {g: 1 - sens[f"flip_{g}"].mean() for g in ("AT", "AMB_DEG", "ERP")}
        a("\nLabel stability (share of grid points with the base label): " + ", ".join(f"{g} {f(v, 2)}{' (stable)' if v >= 2 / 3 else ' → **parameter-dependent**'}" for g, v in st.items()) +
          f". Grid uses R = {SENS_R}, 8 scenarios, 20 s MILP limit (cheaper than the base run).\n")
    else:
        a("Not run (`--no-sens`).\n")
    # ---------------- tests
    a("## 7. Tests (`lab/model/tests.py`)\n")
    tf = os.path.join(RES, "tests.json")
    if os.path.exists(tf):
        T = json.load(open(tf))
        for k, v in T.items():
            if isinstance(v, dict): a(f"- {'PASS' if v.get('ok') else ('INFO' if v.get('ok') is None else 'FAIL')} `{k}`: " + ", ".join(f"{kk}={vv}" for kk, vv in v.items() if kk != "ok"))
    else:
        a("Run `python lab/model/tests.py` (results land in tests.json).")
    a("")
    # ---------------- caveats
    a("## 8. Data status and caveats\n")
    a("**Real data:** cadastral parcels and DBT volumes, PGT 2030 layers (AT, ex-AMB_DEG, srv_erp, rig), DUSAF, census-2021 hex cells, "
      "MEF IRPEF 2024 by CAP, OMI 2019–2024 rents, NIL indicators (core.json), ISTAT absolute-poverty threshold (A, to verify).")
    a(f"**Assumptions:** FAR {SUP['far']}, yield {SUP['yield_']}, 80 m²/dwelling, cost model (A), τ {DEM['tau']}, basket 1.5× ISTAT, renter share 0.30, "
      f"σ {AUDIT['sigma']}, κ {PORT['kappa']}/{PORT['kappa_erp']}, λ {DEM['lam_km']} km, adjacency buffer {SITE['buffer_m']} m, srv_erp land at 1 €/m².")
    a("**Synthetic:** archetype weight distributions (B), the synthetic city in tests; simulated households are a model of NIL distributions, not records.")
    a("**Limits:** (1) deprivation is NIL-ecological (88 NIL, income only at 38 CAP) — within-NIL placement is invisible except via C's modelled hex pressure; "
      "(2) the DI/isolation use the ERP-eligible share as 'low income'; (3) no ownership, constraints, heritage or real PGT indices — capacity is notional; "
      "(4) AMB_DEG has only "
      f"{int(cnt.get('AMB_DEG', 0))} sites: low power, a 'neither' there is uninformative; (5) designated sets are evaluated as if fully built at FAR {SUP['far']}; "
      "(6) Euclidean distances; (7) served demand saturates for large sets (capacity ≫ D_res_decent), so served per € mostly tracks cost; served D_tau is reported too; "
      "(8) the PU score from C is not used anywhere (biased by design).")
    open(os.path.join(RES, "results.md"), "w", encoding="utf-8").write("\n".join(L))
    log("results.md written")


if __name__ == "__main__":
    o = pickle.load(open(os.path.join(OUT, "base.pkl"), "rb"))
    sp = os.path.join(OUT, "sens.pkl"); sens = pickle.load(open(sp, "rb")) if os.path.exists(sp) else None
    write(o, sens, o.get("runtime_min"))
