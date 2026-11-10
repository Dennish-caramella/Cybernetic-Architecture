"""Analisi mercato abitativo e accessibilita' Milano (sessione 2026-11-10).

Input (scaricati in scratchpad, NON versionati; URL nel report 02_mercato_e_accessibilita.md):
  MEF  Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.csv / _2014.csv / subcomunale_CSV_2024.csv
  Comune di Milano open data: OMI riepilogo ds1996, OMI 2025/2 compravendita e locazione, ds1442 famiglie
  eurostat_*.csv (prodotti da fetch_eurostat.py, in questa cartella)
Uso: python3 -I analisi_accessibilita.py <cartella_input>
Output (in questa cartella): CSV derivati elencati in fondo.
Tutte le ipotesi sono marcate [H] e riportate nel report.
"""
import sys, os, json, urllib.request
import numpy as np, pandas as pd

IN = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- 1. Redditi MEF
CL = [("<=0", -np.inf, 0), ("0-10k", 0, 10000), ("10-15k", 10000, 15000), ("15-26k", 15000, 26000),
      ("26-55k", 26000, 55000), ("55-75k", 55000, 75000), ("75-120k", 75000, 120000), (">120k", 120000, np.inf)]
LAB = {"<=0": "minore o uguale a zero euro", "0-10k": "da 0 a 10000 euro", "10-15k": "da 10000 a 15000 euro",
       "15-26k": "da 15000 a 26000 euro", "26-55k": "da 26000 a 55000 euro", "55-75k": "da 55000 a 75000 euro",
       "75-120k": "da 75000 a 120000 euro", ">120k": "oltre 120000 euro"}

def mef(path, comune_col="Denominazione Comune"):
    d = pd.read_csv(path, sep=";", dtype=str, encoding="latin1")
    d.columns = [c.strip().replace("minore di zero", "minore o uguale a zero").replace(" - Ammontare in euro", " - Ammontare")
                 .replace(" - Ammontare", " - Ammontare in euro") for c in d.columns]
    return d

def classi(row):
    out = []
    for k, lo, hi in CL:
        f = float(row[f"Reddito complessivo {LAB[k]} - Frequenza"] or 0)
        a = float(row[f"Reddito complessivo {LAB[k]} - Ammontare in euro"] or 0)
        out.append(dict(classe=k, lo=lo, hi=hi, contribuenti=f, ammontare_eur=a, media_eur=a / f if f else np.nan))
    return pd.DataFrame(out)

c24 = mef(f"{IN}/comunale_CSV_2024/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.csv")
c14 = mef(f"{IN}/comunale_CSV_2014/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2014.csv")
mi24 = c24[(c24["Denominazione Comune"] == "MILANO") & (c24["Sigla Provincia"] == "MI")].iloc[0]
mi14 = c14[(c14["Denominazione Comune"] == "MILANO") & (c14["Sigla Provincia"] == "MI")].iloc[0]
k24, k14 = classi(mi24), classi(mi14)
k24["anno"], k14["anno"] = 2024, 2014
k24["quota_contribuenti"] = k24.contribuenti / k24.contribuenti.sum()
k24["quota_reddito"] = k24.ammontare_eur / k24.ammontare_eur.sum()
pd.concat([k24, k14]).to_csv(f"{OUT}/mef_milano_classi_reddito_2014_2024.csv", index=False)

def sintesi(r):
    g = lambda c: float(r[c] or 0) if c in r.index else np.nan
    if "Reddito complessivo - Ammontare in euro" not in r.index:  # 2014: totale dalle classi
        kk = classi(r); r = r.copy()
        r["Reddito complessivo - Ammontare in euro"] = kk.ammontare_eur.sum()
        r["Reddito complessivo - Frequenza"] = kk.contribuenti.sum()
    return dict(contribuenti=g("Numero contribuenti"),
                reddito_complessivo_tot=g("Reddito complessivo - Ammontare in euro"),
                reddito_complessivo_freq=g("Reddito complessivo - Frequenza"),
                media_complessivo=g("Reddito complessivo - Ammontare in euro") / g("Reddito complessivo - Frequenza"),
                lav_dip_freq=g("Reddito da lavoro dipendente e assimilati - Frequenza"),
                lav_dip_media=g("Reddito da lavoro dipendente e assimilati - Ammontare in euro") / g("Reddito da lavoro dipendente e assimilati - Frequenza"),
                pensione_freq=g("Reddito da pensione - Frequenza"),
                pensione_media=g("Reddito da pensione - Ammontare in euro") / g("Reddito da pensione - Frequenza"),
                imposta_netta_tot=g("Imposta netta - Ammontare in euro"))
S24, S14 = sintesi(mi24), sintesi(mi14)

# Percentili per interpolazione lineare della CDF entro le classi [I]: si assume distribuzione uniforme
# entro classe; per la classe aperta >120k non serve (P80 cade sotto).
def percentile(k, p):
    k = k[k.classe != "<=0"].copy()  # esclusi redditi <=0 (206 contribuenti) [H]
    cum = k.contribuenti.cumsum() / k.contribuenti.sum()
    prev = 0.0
    for (_, r), c in zip(k.iterrows(), cum):
        if p <= c:
            lo, hi = r.lo, r.hi
            return lo + (p - prev) / (c - prev) * (hi - lo)
        prev = c
PCT = [0.2, 0.4, 0.5, 0.6, 0.8]
perc = pd.DataFrame([dict(percentile=f"P{int(p*100)}", lordo_2024=percentile(k24, p), lordo_2014=percentile(k14, p)) for p in PCT])

# CAP (subcomunale) 2024
sc = mef(f"{IN}/subcomunale_CSV_2024/Redditi_e_principali_variabili_IRPEF_su_base_subcomunale_CSV_2024.csv")
sc = sc[(sc["Denominazione Comune"] == "MILANO") & (sc["Sigla Provincia"] == "MI")]
cap = pd.DataFrame(dict(CAP=sc.CAP, contribuenti=sc["Numero contribuenti"].astype(float),
                        reddito_tot=sc["Reddito complessivo - Ammontare in euro"].astype(float),
                        freq=sc["Reddito complessivo - Frequenza"].astype(float),
                        sotto26k=sum(sc[f"Reddito complessivo {LAB[c]} - Frequenza"].astype(float) for c in ["<=0", "0-10k", "10-15k", "15-26k"]),
                        oltre120k=sc["Reddito complessivo oltre 120000 euro - Frequenza"].astype(float)))
cap["media"] = cap.reddito_tot / cap.freq
cap["quota_sotto26k"] = cap.sotto26k / cap.freq
cap["quota_oltre120k"] = cap.oltre120k / cap.freq
cap["mediana_interp"] = [percentile(classi(r), 0.5) for _, r in sc.iterrows()]
cap.loc[cap.sotto26k.isna(), "mediana_interp"] = np.nan  # classi non pubblicate per il CAP
cap.sort_values("media").to_csv(f"{OUT}/mef_milano_cap_2024.csv", index=False)

# ---------------------------------------------------------------- 2. Netto [H]
def irpef_netto(R, pensionato=False):
    """Netto annuo da reddito complessivo R, regole 2024 semplificate [H]:
    IRPEF 23/35/43 (soglie 28k/50k); detrazione lavoro dipendente (o pensione) art.13 TUIR 2024;
    trattamento integrativo 1.200 se R<=15k (solo dipendenti); addizionale regionale Lombardia
    1,23/1,58/1,72/1,73%; addizionale comunale Milano 0,8% con esenzione fino a 23.000 [S].
    Ignora: altre detrazioni (figli >21, spese), cedolare, contributi gia' esclusi dal complessivo."""
    t = 0.23 * min(R, 28000) + 0.35 * max(0, min(R, 50000) - 28000) + 0.43 * max(0, R - 50000)
    if not pensionato:
        if R <= 15000: d = 1955
        elif R <= 28000: d = 1910 + 1190 * (28000 - R) / 13000
        elif R <= 50000: d = 1910 * (50000 - R) / 22000
        else: d = 0
        if 25000 < R <= 35000: d += 65
    else:
        if R <= 8500: d = 1955
        elif R <= 28000: d = 700 + 1255 * (28000 - R) / 19500
        elif R <= 50000: d = 700 * (50000 - R) / 22000
        else: d = 0
        if 25000 < R <= 29000: d += 50
    irpef = max(0, t - d)
    ti = 1200 if (not pensionato and 8500 < R <= 15000) else 0
    reg = 0.0123 * min(R, 15000) + 0.0158 * max(0, min(R, 28000) - 15000) + 0.0172 * max(0, min(R, 50000) - 28000) + 0.0173 * max(0, R - 50000)
    com = 0.008 * R if R > 23000 else 0
    if R <= 8500: reg = com = 0  # no tax area [H]
    return R - irpef - reg - com + ti

perc["netto_2024"] = perc.lordo_2024.map(irpef_netto)
perc["netto_2024_pensionato"] = perc.lordo_2024.map(lambda r: irpef_netto(r, True))
perc.to_csv(f"{OUT}/mef_milano_percentili_contribuenti.csv", index=False)

# ---------------------------------------------------------------- 3. OMI
omi_r = pd.read_csv(f"{IN}/omi/quotazioni_omi_locazione_2025_2.csv", sep=";", decimal=",", encoding="utf-8-sig")
omi_s = pd.read_csv(f"{IN}/omi/quotazioni_omi_compravendita_2025_2.csv", sep=";", decimal=",", encoding="utf-8-sig")
sel = lambda d: d[(d.Descr_Tipologia == "Abitazioni civili") & (d.Stato == "NORMALE")]
r, s = sel(omi_r).copy(), sel(omi_s).copy()
r["loc_mid"] = (r.Loc_min + r.Loc_max) / 2
s["compr_mid"] = (s.Compr_min + s.Compr_max) / 2
z = r[["Fascia", "Zona", "Loc_min", "Loc_max", "loc_mid"]].merge(s[["Zona", "Compr_min", "Compr_max", "compr_mid"]], on="Zona")
z["rendimento_lordo"] = z.loc_mid * 12 / z.compr_mid
z.sort_values("compr_mid").to_csv(f"{OUT}/omi_milano_2025S2_civili_normale_per_zona.csv", index=False)
fas = z.groupby("Fascia").agg(zone=("Zona", "count"), loc_mid_mediana=("loc_mid", "median"), loc_min_min=("Loc_min", "min"),
                              loc_max_max=("Loc_max", "max"), compr_mid_mediana=("compr_mid", "median"),
                              compr_min_min=("Compr_min", "min"), compr_max_max=("Compr_max", "max")).reset_index()
tot = dict(Fascia="TUTTE", zone=len(z), loc_mid_mediana=z.loc_mid.median(), loc_min_min=z.Loc_min.min(), loc_max_max=z.Loc_max.max(),
           compr_mid_mediana=z.compr_mid.median(), compr_min_min=z.Compr_min.min(), compr_max_max=z.Compr_max.max())
fas = pd.concat([fas, pd.DataFrame([tot])])
fas.to_csv(f"{OUT}/omi_milano_2025S2_sintesi_fasce.csv", index=False)

# Serie storica: mediana tra zone dei punti medi (civili, normale), per semestre
h = pd.read_csv(f"{IN}/omi/ds1996_quotazioni_omi_compravendita_e_locazione_riepilogo.csv", sep=";", decimal=",", encoding="utf-8-sig")
h = sel(h).copy()
for c in ["Compr_min", "Compr_max", "Loc_min", "Loc_max"]:
    h[c] = pd.to_numeric(h[c].astype(str).str.replace(",", "."), errors="coerce")
h["compr_mid"] = (h.Compr_min + h.Compr_max) / 2
h["loc_mid"] = (h.Loc_min + h.Loc_max) / 2
ts = h.groupby(["Anno", "Periodo"]).agg(zone=("Zona", "nunique"), compr_mid_mediana=("compr_mid", "median"),
                                         loc_mid_mediana=("loc_mid", "median")).reset_index()
ts.to_csv(f"{OUT}/omi_milano_serie_semestrale_civili_normale.csv", index=False)

# ---------------------------------------------------------------- 4. Accessibilita' [H]
OMI_LOC = {"periferia (mediana fascia D/E)": float(z[z.Fascia.isin(["D", "E"])].loc_mid.median()),
           "citta' (mediana tutte le zone)": float(z.loc_mid.median()),
           "semicentro (mediana fascia C)": float(z[z.Fascia == "C"].loc_mid.median())}
OMI_VEN = {"periferia (mediana fascia D/E)": float(z[z.Fascia.isin(["D", "E"])].compr_mid.median()),
           "citta' (mediana tutte le zone)": float(z.compr_mid.median()),
           "semicentro (mediana fascia C)": float(z[z.Fascia == "C"].compr_mid.median())}
ANNUNCI_S = 23.3  # [S] canone medio richiesto Milano, Idealista 2025 (non verificato in questa sessione)
PIANO_CASA = 80 / 12  # €/m2/mese, tetto Piano Casa 2024; 90/12 con DG 365/2026

# Eurostat: soglia di rischio poverta' 60% mediana, Italia, indagine 2025 (redditi 2024)
li = pd.read_csv(f"{OUT}/eurostat_ilc_li01.csv")
li = li[(li.time == 2025) & (li.unit == "EUR") & (li.statinfo == "MED_EI") & (li.rskpovth == "B_60")].set_index("hhcomp").value
AROP1 = float(li["A1"])  # 13.237 euro/anno, persona sola

# Famiglie tipo [H]: superficie lorda commerciale (OMI e' su superficie lorda), scala OCSE modificata,
# percettori, figli per Assegno Unico.
TIPI = [
    dict(tipo="persona sola (<65)", mq=45, percettori=1, pens=False, figli=0, scala=1.0, isee_scala=1.0),
    dict(tipo="anziano solo (pensionato)", mq=50, percettori=1, pens=True, figli=0, scala=1.0, isee_scala=1.0),
    dict(tipo="coppia senza figli (2 percettori)", mq=60, percettori=2, pens=False, figli=0, scala=1.5, isee_scala=1.57),
    dict(tipo="monogenitore + 1 figlio <14", mq=65, percettori=1, pens=False, figli=1, scala=1.3, isee_scala=1.57),
    dict(tipo="coppia + 2 figli <14 (2 percettori)", mq=85, percettori=2, pens=False, figli=2, scala=2.1, isee_scala=2.46),
]

def auu_mese_per_figlio(isee):
    """Assegno Unico 2024 (importi base per figlio minore) [S: INPS 2024 max 199,4 / min 57,0;
    soglie ISEE 17.090,61 / 45.574,96]; interpolazione lineare, maggiorazioni ignorate [H]."""
    if isee <= 17090.61: return 199.4
    if isee >= 45574.96: return 57.0
    return 199.4 - (199.4 - 57.0) * (isee - 17090.61) / (45574.96 - 17090.61)

MUTUO = dict(ltv=0.8, anni=25, tasso=0.033)  # [H]
def rata_annua(capitale, i=MUTUO["tasso"], n=MUTUO["anni"]):
    return capitale * i / (1 - (1 + i) ** -n)

rows = []
for _, pr in perc.iterrows():
    for t in TIPI:
        lordo1 = pr.lordo_2024
        netto1 = irpef_netto(lordo1, t["pens"])
        lordo_fam = lordo1 * t["percettori"]
        # ISEE proxy (solo redditi, patrimonio 0, detrazione affitto max 7.000) [H]
        isee = max(0, lordo_fam - 7000) / t["isee_scala"]
        auu = 12 * t["figli"] * auu_mese_per_figlio(isee) if t["figli"] else 0
        netto = netto1 * t["percettori"] + auu
        for zona, cm in list(OMI_LOC.items()) + [("Piano Casa (80 €/m2/anno)", PIANO_CASA), ("annunci [S] 23,3 €/m2", ANNUNCI_S)]:
            canone = cm * t["mq"] * 12
            res = netto - canone
            basket = AROP1 * t["scala"]  # [H] paniere non abitativo = soglia AROP 60% (tutta)
            row = dict(percentile=pr.percentile, tipo=t["tipo"], mq=t["mq"], lordo_individuale=round(lordo1),
                       netto_famiglia=round(netto), auu_annuo=round(auu), isee_proxy=round(isee), zona=zona,
                       canone_eur_mq_mese=round(cm, 2), canone_annuo=round(canone), canone_mese=round(canone / 12),
                       RTI=round(canone / netto, 3), oltre30=canone / netto > 0.30, oltre40=canone / netto > 0.40,
                       residuo_annuo=round(res), paniere_non_abitativo=round(basket),
                       shelter_poor=res < basket, shelter_poor_75=res < 0.75 * basket,
                       ERP_eleggibile_proxy=isee <= 16000)
            if zona in OMI_VEN:
                prezzo = OMI_VEN[zona] * t["mq"]
                row.update(prezzo_alloggio=round(prezzo), PTI=round(prezzo / netto, 1),
                           rata_mutuo_su_netto=round(rata_annua(prezzo * MUTUO["ltv"]) / netto, 3),
                           anni_risparmio_anticipo_20pct_al_10pct=round(0.2 * prezzo / (0.10 * netto), 1))
            rows.append(row)
acc = pd.DataFrame(rows)
acc.to_csv(f"{OUT}/accessibilita_famiglie_tipo.csv", index=False)

# Soglie di reddito lordo individuale per RTI 30% con canone OMI mediano citta' (persona sola 45 m2)
def soglia_lordo(target_netto, pens=False):
    lo, hi = 0, 300000
    for _ in range(60):
        m = (lo + hi) / 2
        if irpef_netto(m, pens) < target_netto: lo = m
        else: hi = m
    return hi
soglie = []
for t in TIPI:
    for zona, cm in list(OMI_LOC.items()) + [("Piano Casa (80 €/m2/anno)", PIANO_CASA), ("Piano Casa (90 €/m2/anno)", 90 / 12), ("annunci [S] 23,3 €/m2", ANNUNCI_S)]:
        canone = cm * t["mq"] * 12
        # netto familiare necessario; ripartito sui percettori (AUU ignorato qui, conservativo) [H]
        need = canone / 0.30 / t["percettori"]
        g = soglia_lordo(need, t["pens"])
        cdf = (k24[k24.classe != "<=0"])
        # quota contribuenti sotto g
        cum = 0; tot = cdf.contribuenti.sum(); q = None; acc_c = 0
        for _, r_ in cdf.iterrows():
            if g >= r_.hi: acc_c += r_.contribuenti
            else:
                acc_c += r_.contribuenti * max(0, (g - r_.lo)) / (r_.hi - r_.lo); break
        soglie.append(dict(tipo=t["tipo"], zona=zona, canone_annuo=round(canone), netto_necessario_per_percettore=round(need),
                           lordo_necessario_per_percettore=round(g), percentile_contribuenti_milano=round(acc_c / tot, 3)))
pd.DataFrame(soglie).to_csv(f"{OUT}/soglie_reddito_rti30.csv", index=False)

# "Pancia": tra soglia ERP (ISEE <= 16.000, Lombardia) e soglia di mercato (RTI 30%) [H]
# ISEE proxy = (redditi lordi familiari - detrazione affitto 7.000) / scala; patrimonio = 0.
def quota_sotto(g):
    cdf = k24[k24.classe != "<=0"]; tot = cdf.contribuenti.sum(); acc_c = 0
    for _, r_ in cdf.iterrows():
        if g >= r_.hi: acc_c += r_.contribuenti
        else:
            acc_c += r_.contribuenti * max(0, g - r_.lo) / (r_.hi - r_.lo); break
    return acc_c / tot
sd = pd.DataFrame(soglie); pancia = []
for t in TIPI:
    erp_g = (16000 * t["isee_scala"] + 7000) / t["percettori"]
    for zona in ["citta' (mediana tutte le zone)", "periferia (mediana fascia D/E)", "annunci [S] 23,3 €/m2"]:
        m = sd[(sd.tipo == t["tipo"]) & (sd.zona == zona)].iloc[0]
        pancia.append(dict(tipo=t["tipo"], zona=zona, lordo_soglia_ERP_per_percettore=round(erp_g),
                           pct_ERP=round(quota_sotto(erp_g), 3), lordo_soglia_mercato_per_percettore=m.lordo_necessario_per_percettore,
                           pct_mercato=m.percentile_contribuenti_milano,
                           ampiezza_pancia_pp=round(100 * max(0, m.percentile_contribuenti_milano - quota_sotto(erp_g)), 1)))
pd.DataFrame(pancia).to_csv(f"{OUT}/pancia_erp_mercato.csv", index=False)
print(pd.DataFrame(pancia).to_string())

print(json.dumps(dict(S24=S24, S14=S14), indent=1))
print(k24.to_string()); print(perc.round(0).to_string()); print(fas.round(2).to_string())
print(ts.tail(22).round(1).to_string()); print(OMI_LOC, OMI_VEN)
print(cap.describe().round(0).to_string())
print(pd.DataFrame(soglie).to_string())
