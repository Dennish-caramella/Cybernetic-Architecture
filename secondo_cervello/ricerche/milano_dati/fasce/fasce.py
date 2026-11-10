"""Fasce di reddito e strumenti abitativi a Milano: figura e quote.

Estende ../pancia/pancia.py. Asse x: reddito complessivo IRPEF lordo del
contribuente (MEF a.i. 2024, riga MILANO, file ../pancia/mef_irpef_milano_2024.csv).
Le soglie ISEE sono tradotte in reddito lordo con l'ipotesi [I] "persona sola,
lavoratore dipendente, in affitto con canone >= 7.000 EUR/anno, patrimonio nullo"
(DPCM 159/2013 art. 4, testo 2013). Per altri nuclei le soglie si spostano a destra.

Uso: python fasce.py  -> fig_fasce_strumenti.png (200 dpi) e .svg; stampa le quote.
"""
from pathlib import Path
import csv
import numpy as np
from scipy import optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
MEF = OUT.parent / "pancia" / "mef_irpef_milano_2024.csv"

# ------------------------------------------------------------ dati MEF [V]
v = {r["variabile"]: r["valore"] for r in csv.DictReader(open(MEF, encoding="utf-8"))}
EDGES = np.array([0, 10e3, 15e3, 26e3, 55e3, 75e3, 120e3, np.inf])
LAB = ["da 0 a 10000", "da 10000 a 15000", "da 15000 a 26000", "da 26000 a 55000",
       "da 55000 a 75000", "da 75000 a 120000", "oltre 120000"]
N = np.array([int(v[f"Reddito complessivo {l} euro - Frequenza"]) for l in LAB])

def nll(F):
    return -(N * np.log(np.clip(np.diff(F(EDGES)), 1e-300, None))).sum()

def dagum():
    def cdf(x, a, b, p):
        x = np.asarray(x, float)
        with np.errstate(divide="ignore", over="ignore"):
            return np.where(x <= 0, 0.0, (1 + (np.maximum(x, 1e-9) / b) ** (-a)) ** (-p))
    f = lambda th: nll(lambda x: cdf(x, *np.exp(th)))
    r = optimize.minimize(f, [np.log(3), np.log(30e3), np.log(0.7)], method="Nelder-Mead",
                          options=dict(maxiter=4000, xatol=1e-8, fatol=1e-8))
    a, b, p = np.exp(r.x)
    return (lambda x: cdf(x, a, b, p)), (lambda x: a * p / x * (x / b) ** (a * p) / (1 + (x / b) ** a) ** (p + 1))

CDF, PDF = dagum()

def share_below(t):
    """Quota di contribuenti (reddito > 0) sotto t: classi MEF esatte, Dagum dentro la classe."""
    cum = np.concatenate([[0], np.cumsum(N)]) / N.sum()
    k = np.searchsorted(EDGES, t, side="right") - 1
    a, b = EDGES[k], EDGES[k + 1]
    return cum[k] + (CDF(t) - CDF(a)) / (CDF(b) - CDF(a)) * N[k] / N.sum()

# ------------------------------------------------------- conversioni [I]
def isee_to_gross(isee):
    """ISR = Y - min(20% Y, 3000) - min(canone, 7000); scala 1; patrimonio 0."""
    y_low = (isee + 7_000) / 0.8
    return y_low if y_low <= 15_000 else isee + 10_000

def net_employee_2024(y):
    """Netto approssimato dipendente 2024 (come pancia.py): solo ordine di grandezza."""
    inps = 0.0919 * y; b = y - inps
    irpef = 0.23 * min(b, 28e3) + 0.35 * max(0, min(b, 50e3) - 28e3) + 0.43 * max(0, b - 50e3)
    det = 1955 if b <= 15e3 else (1910 + 1190 * (28e3 - b) / 13e3 if b <= 28e3 else
                                  (1910 * (50e3 - b) / 22e3 if b <= 50e3 else 0))
    return y - inps - max(0, irpef - det) - 0.023 * b

def gross_from_net(n):
    return optimize.brentq(lambda y: net_employee_2024(y) - n, 1e3, 400e3)

RENT_ORD_L = 110e6 / 7_701                      # OMI IV 2025, nuovi contratti 4+4 [V]
T = dict(
    indigenza=isee_to_gross(3_000),             # ISEE <= 3.000 (riserva 20% SAP) [V/S]
    poverta=gross_from_net(1_256.37 * 12),      # ISTAT 2025, adulto 30-59 solo, centro AM Lombardia [V]
    adi=isee_to_gross(10_140),                  # Assegno di inclusione [L]
    affitto=isee_to_gross(15_000),              # sostegno affitto DGR 5855/2026 (avviso Lodi) [V]
    erp=isee_to_gross(16_000),                  # RR 4/2017 art. 7 [V]
    hs_lo=isee_to_gross(14_000), hs_hi=isee_to_gross(40_000),   # DGR 6209/2026 [V]
    val_lo=isee_to_gross(12_000),               # valorizzazioni ALER 12-40k [V]
    erp_perm=isee_to_gross(35_000),             # permanenza ERP [V]
    dsu=isee_to_gross(26_887.93),               # DSU 2026/27 (nucleo d'origine) [V]
    pc_lo=gross_from_net(1_500 * 12), pc_hi=gross_from_net(2_500 * 12),  # Piano Casa DG 365/2026 [V]
    conc=650 * 12 / 0.30,                       # concordato 60 m2 a 650 EUR/mese, 30% del lordo [V/I]
    mkt_lordo=RENT_ORD_L / 0.30,
    mkt_netto=optimize.brentq(lambda y: 0.30 * net_employee_2024(y) - RENT_ORD_L, 20e3, 300e3),
)

if __name__ == "__main__":
    tot = N.sum()
    print(f"contribuenti con reddito > 0: {tot}")
    for k, t in T.items():
        s = share_below(t)
        print(f"{k:10s} lordo {t:9.0f}  quota sotto {s:6.1%}  ~{s*tot/1e3:6.0f} mila contribuenti")

    # ------------------------------------------------------------- figura
    INK, MUTED = "#222222", "#6b6b6b"
    C_POV, C_SAP, C_GRIGIA, C_MKT = "#7A3B3B", "#4C6A85", "#C9A227", "#8C8C8C"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK,
                         "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                         "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(11.5, 8.6), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.0, 1.55], hspace=0.06))
    xs = np.logspace(np.log10(3e3), np.log10(250e3), 600)
    dens = PDF(xs) * xs * np.log(10)            # densita' su log10(x)
    zones = [(3e3, T["poverta"], C_POV, "sotto ~18k lordi\n(redditi individuali,\nnon famiglie povere)"),
             (T["poverta"], T["erp"], C_SAP, "18-26k\nSAP"),
             (T["erp"], T["mkt_lordo"], C_GRIGIA, "fascia grigia\n/ pancia"),
             (T["mkt_lordo"], 250e3, C_MKT, "mercato")]
    ypos = [0.86, 0.98, 0.98, 0.86]
    for lo, hi, c, lab in zones:
        m = (xs >= lo) & (xs <= hi)
        ax.fill_between(xs[m], 0, dens[m], color=c, alpha=0.45, lw=0)
    ax.plot(xs, dens, color=INK, lw=1.4)
    ymax = dens.max() * 1.32
    cuts = [3e3, T["poverta"], T["erp"], T["mkt_lordo"], 250e3]
    for (lo, hi, c, lab), yy in zip(zones, ypos):
        s = share_below(min(hi, 1e9)) - share_below(max(lo, 1)) if hi < 250e3 else 1 - share_below(lo)
        if lo == 3e3: s = share_below(hi)
        xc = np.sqrt(lo * hi) if lo != T["erp"] else 36e3
        ax.text(xc, ymax * yy, f"{lab}\n{s:.0%}", ha="center", va="top",
                fontsize=8.5, weight="bold", color=INK)
    ax.axvline(T["mkt_netto"], color=INK, lw=0.9, ls=(0, (2, 2)))
    ax.text(T["mkt_netto"] * 1.03, ymax * 0.30, "mercato al 30%\ndel netto (~81k)", fontsize=7.5, color=MUTED)
    ax.set_ylim(0, ymax * 1.08); ax.set_yticks([])
    ax.set_ylabel("densità (scala log del reddito)")
    ax.set_title("Milano: distribuzione dei redditi IRPEF (a.i. 2024) e strumenti abitativi per fascia",
                 loc="left", weight="bold", fontsize=11, pad=16)
    ax.text(0, 1.0, "quote = contribuenti con reddito > 0 (1,01 mln); soglie ISEE tradotte per persona sola, "
            "dipendente, in affitto, patrimonio nullo", transform=ax.transAxes, fontsize=7.5,
            color=MUTED, va="bottom")

    rows = [  # (etichetta, da, a, colore, tratteggio, nota)
        ("Povertà assoluta ISTAT 2025 (spesa 1.256 €/mese, adulto solo)", 3e3, T["poverta"], C_POV, "", ""),
        ("Assegno di inclusione (ISEE ≤ 10.140) [L]", 3e3, T["adi"], C_POV, "//", ""),
        ("SAP: riserva 20% indigenti (ISEE ≤ 3.000)", 3e3, T["indigenza"], C_SAP, "", "priorità assoluta"),
        ("SAP / ERP accesso (ISEE ≤ 16.000)", 3e3, T["erp"], C_SAP, "", "ALER Milano + MM Casa"),
        ("SAP: permanenza fino a ISEE 35.000", T["erp"], T["erp_perm"], C_SAP, "..", "solo chi è già dentro"),
        ("Sostegno affitto / morosità (ISEE ≤ 15.000)", 3e3, T["affitto"], C_SAP, "//", "Regione + Ambito"),
        ("Housing sociale (SAS) DGR 6209/2026: ISEE 14-40k", T["hs_lo"], T["hs_hi"], C_GRIGIA, "", "ALER, cooperative, privati"),
        ("Valorizzazioni ALER/Comune: ISEE 12-40k", T["val_lo"], T["hs_hi"], C_GRIGIA, "//", ""),
        ("Piano Casa Milano (ERSC): netto nucleo 1.500-2.500 €/mese", T["pc_lo"], T["pc_hi"], C_GRIGIA, "", "≤ 90 €/m²/anno medio"),
        ("DSU studenti 2026/27: ISEE ≤ 26.888 (nucleo d'origine)", 3e3, T["dsu"], C_GRIGIA, "xx", "borse e posti letto"),
        ("Canone concordato (nessun requisito di reddito)", T["conc"], T["mkt_lordo"], C_GRIGIA, "..", "60 m² ≈ 650 €/mese"),
        ("Mercato libero (canone ≤ 30% del lordo)", T["mkt_lordo"], 250e3, C_MKT, "", ""),
    ]
    for i, (lab, lo, hi, c, h, note) in enumerate(rows):
        y = len(rows) - 1 - i
        bx.add_patch(Rectangle((lo, y - 0.32), hi - lo, 0.64, facecolor=c, alpha=0.75 if not h else 0.35,
                               hatch=h, edgecolor=INK, lw=0.6))
        bx.text(2.9e3, y, lab, ha="right", va="center", fontsize=8.2, color=INK)
        if note:
            bx.text(hi * 1.04 if hi < 150e3 else lo * 1.04, y + (0.42 if hi < 150e3 else 0), note, ha="left", va="center", fontsize=7.0, color=MUTED, style="italic",
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.85))
    # banda di sovrapposizione (ipotesi della tesi)
    bx.axvspan(T["hs_lo"], T["erp"], color="#B5651D", alpha=0.18, lw=0)
    bx.text(np.sqrt(T["hs_lo"] * T["erp"]), len(rows) - 0.35, "sovrapposizione\nSAP ∩ housing sociale\n(ISEE 14-16k)",
            ha="center", va="bottom", fontsize=7.3, color="#7a3e0c", weight="bold")
    for k in ["poverta", "erp", "mkt_lordo"]:
        for a in (ax, bx):
            a.axvline(T[k], color=INK, lw=0.9, ls=(0, (4, 3)))
    bx.set_xscale("log"); bx.set_xlim(3e3, 250e3); bx.set_ylim(-0.7, len(rows) + 0.5)
    ticks = [5e3, 10e3, 15e3, 20e3, 26e3, 35e3, 50e3, 80e3, 120e3, 200e3]
    bx.set_xticks(ticks); bx.set_xticklabels([f"{t/1e3:.0f}k" for t in ticks])
    bx.minorticks_off()
    bx.set_yticks([]); bx.spines["left"].set_visible(False)
    bx.set_xlabel("reddito complessivo lordo annuo del contribuente (€, scala logaritmica)")
    fig.text(0.01, 0.005,
             "Fonti: MEF-DF IRPEF comunale 2024; RR Lombardia 4/2017 (testo 2025); DGR XII/6209/2026 (presentazione Regione 25/6/2026); "
             "DG Comune di Milano 365/2026 all. 1; DGR XII/6298/2026 (DSU);\nISTAT, La povertà in Italia 2025; OMI IV trim. 2025; "
             "avviso DGR 5855/2026. Barre piene = requisito di reddito verificato; tratteggio = verificato altrove o [L]. "
             "Le soglie per nuclei più grandi si spostano a destra.",
             fontsize=6.8, color=MUTED, ha="left")
    fig.subplots_adjust(left=0.33, right=0.97, top=0.94, bottom=0.08)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"fig_fasce_strumenti.{ext}", dpi=200, facecolor="white")
    print("figura scritta")
