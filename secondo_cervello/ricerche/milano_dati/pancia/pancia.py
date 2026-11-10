"""Pancia della gaussiana: figure concettuale ed empirica (Milano).

Dati: MEF - Dipartimento Finanze, "Redditi e principali variabili IRPEF su base
comunale", anno d'imposta 2024 (dichiarazioni 2025), file
Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip, riga MILANO
(estratto in mef_irpef_milano_2024.csv, accanto a questo script).

Uso:  python pancia.py      (scrive PNG 200 dpi e SVG nella cartella dello script,
                             stampa le quote per zona)
"""
from pathlib import Path
import csv
import numpy as np
from scipy import optimize, stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- dati MEF [V]
def load_mef(path=OUT / "mef_irpef_milano_2024.csv"):
    v = {r["variabile"]: r["valore"] for r in csv.DictReader(open(path, encoding="utf-8"))}
    edges = [0, 10_000, 15_000, 26_000, 55_000, 75_000, 120_000, np.inf]
    lab = ["da 0 a 10000", "da 10000 a 15000", "da 15000 a 26000", "da 26000 a 55000",
           "da 55000 a 75000", "da 75000 a 120000", "oltre 120000"]
    n = np.array([int(v[f"Reddito complessivo {l} euro - Frequenza"]) for l in lab])
    amt = np.array([int(v[f"Reddito complessivo {l} euro - Ammontare in euro"]) for l in lab])
    n_le0 = int(v["Reddito complessivo minore o uguale a zero euro - Frequenza"])
    tot_n = int(v["Reddito complessivo - Frequenza"])
    tot_amt = int(v["Reddito complessivo - Ammontare in euro"])
    return np.array(edges, float), n, amt, n_le0, tot_n, tot_amt

EDGES, N, AMT, N_LE0, TOT_N, TOT_AMT = load_mef()
assert N.sum() + N_LE0 == TOT_N

# ------------------------------------------------------------- soglie
# ISEE -> reddito complessivo lordo del contribuente. Ipotesi [I]: nucleo di
# 1 persona, lavoratore dipendente, in affitto con canone >= 7.000 EUR/anno,
# patrimonio nullo. ISR = Y - min(20% Y, 3000) - min(canone, 7000)
# (DPCM 159/2013 art. 4 c. 3 lett. e; c. 4 lett. b) [V]; ISEE = ISR / 1 (scala=1).
def isee_to_gross_single(isee, rent_ded=7_000, work_ded_max=3_000):
    return isee + rent_ded + work_ded_max  # valido per Y > 15.000

T_ERP = isee_to_gross_single(16_000)       # RR 4/2017 art. 7 c.1 lett. c [V] -> 26.000
T_GRIGIA = isee_to_gross_single(40_000)    # tetto ISEE housing sociale ALER [S] -> 50.000

# Mercato: canone medio dei nuovi contratti ordinari di lungo periodo (ORD_L),
# Milano, IV trim. 2025: 110 mln EUR / 7.701 abitazioni (OMI, statistiche
# trimestrali residenziale IV 2025, tab. 8) [V]; canoni in milioni arrotondati.
RENT_ORD_L = 110e6 / 7_701
T_MKT_GROSS = RENT_ORD_L / 0.30           # canone <= 30% del reddito LORDO

def net_employee_2024(y):
    """Netto annuo approssimato di un dipendente, 2024 [I]: INPS 9,19%,
    IRPEF 23/35/43% (28k/50k), detrazione lavoro dipendente art. 13 TUIR,
    addizionali reg.+com. forfettarie 2,3%. Ignora esonero contributivo e
    trattamento integrativo: solo ordine di grandezza."""
    inps = 0.0919 * y
    b = y - inps
    irpef = 0.23 * min(b, 28e3) + 0.35 * max(0, min(b, 50e3) - 28e3) + 0.43 * max(0, b - 50e3)
    if b <= 15e3:
        det = 1955
    elif b <= 28e3:
        det = 1910 + 1190 * (28e3 - b) / 13e3
    elif b <= 50e3:
        det = 1910 * (50e3 - b) / 22e3
    else:
        det = 0
    return y - inps - max(0, irpef - det) - 0.023 * b

T_MKT_NET = optimize.brentq(lambda y: 0.30 * net_employee_2024(y) - RENT_ORD_L, 20e3, 300e3)

# ------------------------------------------------- fit su dati raggruppati
def nll(F):
    p = np.diff(F(EDGES))
    return -(N * np.log(np.clip(p, 1e-300, None))).sum()

def fit_lognorm():
    f = lambda th: nll(lambda x: stats.lognorm.cdf(x, th[1], scale=np.exp(th[0])))
    r = optimize.minimize(f, [np.log(26e3), 0.8], method="Nelder-Mead")
    return lambda x: stats.lognorm.cdf(x, r.x[1], scale=np.exp(r.x[0])), \
           lambda x: stats.lognorm.pdf(x, r.x[1], scale=np.exp(r.x[0])), r.x

def fit_dagum():  # Dagum = Burr III: F(x) = (1 + (x/b)^-a)^-p
    def cdf(x, a, b, p):
        x = np.asarray(x, float)
        with np.errstate(divide="ignore", over="ignore"):
            return np.where(x <= 0, 0.0, (1 + (np.maximum(x, 1e-9) / b) ** (-a)) ** (-p))
    f = lambda th: nll(lambda x: cdf(x, np.exp(th[0]), np.exp(th[1]), np.exp(th[2])))
    r = optimize.minimize(f, [np.log(3), np.log(30e3), np.log(0.7)], method="Nelder-Mead",
                          options=dict(maxiter=4000, xatol=1e-8, fatol=1e-8))
    a, b, p = np.exp(r.x)
    pdf = lambda x: a * p / x * (x / b) ** (a * p) / (1 + (x / b) ** a) ** (p + 1)
    return (lambda x: cdf(x, a, b, p)), pdf, (a, b, p)

LN_CDF, LN_PDF, LN_PAR = fit_lognorm()
DG_CDF, DG_PDF, DG_PAR = fit_dagum()

def share_below(t, mode="dagum"):
    """Quota di contribuenti (con reddito > 0) sotto t. Le classi MEF sono
    rispettate esattamente; dentro la classe si interpola con la forma del fit
    Dagum ('dagum') o in modo uniforme ('unif')."""
    cum = np.concatenate([[0], np.cumsum(N)]) / N.sum()
    k = np.searchsorted(EDGES, t, side="right") - 1
    a, b = EDGES[k], EDGES[k + 1]
    if mode == "unif":
        frac = (t - a) / (b - a) if np.isfinite(b) else np.nan
    else:
        frac = (DG_CDF(t) - DG_CDF(a)) / (DG_CDF(b) - DG_CDF(a))
    return cum[k] + frac * N[k] / N.sum()

# --------------------------------------------------------- palette e stile
C_SX, C_PANCIA, C_DX, INK, MUTED = "#4C6A85", "#C9A227", "#8C8C8C", "#222222", "#6b6b6b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})

def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)

# --------------------------------------------------- (a) schema concettuale
def fig_concettuale():
    x = np.linspace(-3.4, 3.4, 600)
    y = stats.norm.pdf(x)
    a, b = -1.0, 1.0
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for lo, hi, c, h in [(-3.4, a, C_SX, "///"), (a, b, C_PANCIA, ""), (b, 3.4, C_DX, "\\\\\\")]:
        m = (x >= lo) & (x <= hi)
        ax.fill_between(x[m], 0, y[m], color=c, alpha=0.55, lw=0, hatch=h, edgecolor="white")
    ax.plot(x, y, color=INK, lw=1.6)
    for t in (a, b):
        ax.axvline(t, color=INK, lw=0.9, ls=(0, (4, 3)))
    ax.text(-2.55, 0.33, "TUTELA PUBBLICA\nERP / SAP", ha="center", color=C_SX, weight="bold")
    ax.text(-2.55, 0.29, "lo Stato deve proteggere", ha="center", color=MUTED, fontsize=8.5)
    ax.text(0, 0.43, "PANCIA: COMMONS", ha="center", color="#7a5f0c", weight="bold", fontsize=11)
    ax.text(0, 0.18, "ceto medio senza risposta\n(\"fascia grigia\"):\ntroppo ricco per l'ERP,\ntroppo povero per il mercato",
            ha="center", color=INK, fontsize=8.5)
    ax.text(2.55, 0.33, "MERCATO\nE COMMITTENZA PRIVATA", ha="center", color="#555555", weight="bold")
    ax.text(2.55, 0.29, "servita da developer e architetti", ha="center", color=MUTED, fontsize=8.5)
    ax.text(a - 0.06, 0.012, "soglia di accesso ERP (ISEE)", rotation=90, ha="right", va="bottom", fontsize=8, color=INK)
    ax.text(b + 0.06, 0.012, "soglia di sostenibilità del canone", rotation=90, ha="left", va="bottom", fontsize=8, color=INK)
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(0, 0.47)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("capacità di spesa per l'abitazione (reddito)  →", labelpad=8)
    ax.set_ylabel("quota di famiglie")
    ax.set_title("La \"pancia\" della distribuzione: schema concettuale", loc="left", weight="bold")
    fig.text(0.01, -0.03, "Schema non in scala. La distribuzione reale dei redditi è asimmetrica a destra "
             "(vedi figura empirica); le soglie sono istituzionali, non statistiche.",
             fontsize=7.5, color=MUTED)
    save(fig, "fig_a_pancia_concettuale")

# --------------------------------------------------- (b) versione empirica
def fig_empirica(t_left, t_right, t_right_alt, shares):
    widths = np.diff(EDGES)[:-1]
    dens = N[:-1] / N.sum() / (widths / 1000)          # quota per 1.000 EUR
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    # pannello 1: scala lineare
    ax = axes[0]
    xmax = 160e3
    for lo, hi, c in [(0, t_left, C_SX), (t_left, t_right, C_PANCIA), (t_right, xmax, C_DX)]:
        ax.axvspan(lo / 1e3, hi / 1e3, color=c, alpha=0.16, lw=0)
    ax.bar(EDGES[:-2] / 1e3, dens, width=widths / 1e3, align="edge", color="white",
           edgecolor=INK, lw=0.9, label="classi MEF (dati osservati)")
    xs = np.linspace(500, xmax, 800)
    ax.plot(xs / 1e3, DG_PDF(xs) * 1000, color=INK, lw=1.4, ls="-", label="fit Dagum (dati raggruppati)")
    ax.plot(xs / 1e3, LN_PDF(xs) * 1000, color=MUTED, lw=1.0, ls=(0, (3, 2)), label="fit lognormale")
    ax.text(121, dens[-1] * 0.9 + 0.0006, f"> 120.000 €:\n{N[-1] / N.sum():.1%}\n(classe aperta)",
            fontsize=7.5, color=INK)
    for t, ls, lab in [(t_left, "-", f"ERP: ISEE 16.000 ≈ {t_left/1e3:.0f}k lordi"),
                       (t_right, "-", f"mercato: canone = 30% lordo ≈ {t_right/1e3:.1f}k"),
                       (t_right_alt, ":", f"variante: 30% del netto ≈ {t_right_alt/1e3:.0f}k")]:
        ax.axvline(t / 1e3, color=INK, lw=1.0, ls=ls)
    ymax = dens.max() * 1.7
    ax.text(t_left / 2e3, ymax * 0.93, f"tutela ERP\n{shares[0]:.0%}", ha="center", color=C_SX, weight="bold")
    ax.text((t_left + t_right) / 2e3, ymax * 0.93, f"pancia\n{shares[1]:.0%}", ha="center", color="#7a5f0c", weight="bold")
    ax.text((t_right + xmax) / 2e3 + 12, ymax * 0.93, f"mercato\n{shares[2]:.0%}", ha="center", color="#555555", weight="bold")
    ax.text(t_left / 1e3 + 1, ymax * 0.62, f"{t_left/1e3:.0f}k", fontsize=7.5)
    ax.text(t_right / 1e3 + 1, ymax * 0.62, f"{t_right/1e3:.1f}k", fontsize=7.5)
    ax.text(t_right_alt / 1e3 + 1, ymax * 0.62, f"{t_right_alt/1e3:.0f}k\n(netto)", fontsize=7.5)
    ax.set_xlim(0, xmax / 1e3); ax.set_ylim(0, ymax)
    ax.set_xlabel("reddito complessivo IRPEF per contribuente (migliaia di €, lordo)")
    ax.set_ylabel("quota di contribuenti per 1.000 €")
    ax.legend(frameon=False, fontsize=7.5, loc="center right")
    ax.set_title("Milano, contribuenti IRPEF per reddito complessivo, a.i. 2024", loc="left", weight="bold", fontsize=10)
    # pannello 2: scala logaritmica (dove la lognormale diventa una campana)
    ax = axes[1]
    xs = np.logspace(np.log10(2e3), np.log10(1e6), 600)
    for lo, hi, c in [(2e3, t_left, C_SX), (t_left, t_right, C_PANCIA), (t_right, 1e6, C_DX)]:
        ax.axvspan(lo, hi, color=c, alpha=0.16, lw=0)
    ax.plot(xs, DG_PDF(xs) * xs * np.log(10), color=INK, lw=1.4)
    ax.plot(xs, LN_PDF(xs) * xs * np.log(10), color=MUTED, lw=1.0, ls=(0, (3, 2)))
    for t, ls in [(t_left, "-"), (t_right, "-"), (t_right_alt, ":")]:
        ax.axvline(t, color=INK, lw=1.0, ls=ls)
    ax.set_xscale("log")
    ax.set_xticks([5e3, 1e4, 2.6e4, 5e4, 1e5, 2.5e5, 1e6])
    ax.set_xticklabels(["5k", "10k", "26k", "50k", "100k", "250k", "1M"])
    ax.set_xlabel("reddito (scala logaritmica)")
    ax.set_ylabel("densità per decade di reddito (fit)")
    ax.set_title("Sull'asse logaritmico la \"campana\" ricompare", loc="left", weight="bold", fontsize=10)
    fig.text(0.01, -0.07,
             "Fonte: MEF-Dip. Finanze, IRPEF su base comunale, a.i. 2024 (contribuenti con reddito > 0: "
             f"{N.sum():,}".replace(",", ".") + "). Soglie: RR Lombardia 4/2017 art. 7 (ISEE 16.000); OMI-AdE, "
             "canone medio nuovi contratti ORD_L Milano IV trim. 2025.\n"
             "Unità = contribuente, non famiglia; reddito lordo, non disponibile. Conversione ISEE→reddito: "
             "persona sola, dipendente, in affitto, senza patrimonio (approssimazione). "
             "Quote calcolate rispettando le classi MEF, con interpolazione Dagum dentro la classe 26-55k.",
             fontsize=7, color=MUTED)
    fig.tight_layout()
    save(fig, "fig_b_pancia_empirica_milano")

if __name__ == "__main__":
    print(f"contribuenti con reddito>0: {N.sum()}  (<=0: {N_LE0}; totale {TOT_N})")
    print(f"reddito medio: {TOT_AMT / TOT_N:,.0f}; medie di classe:", (AMT / N).round(0))
    print(f"quota <=26k (osservata): {N[:3].sum() / N.sum():.4f}")
    print(f"lognorm mu,sigma = {LN_PAR}; median {np.exp(LN_PAR[0]):,.0f}")
    print(f"dagum a,b,p = {DG_PAR}")
    for nm, F in [("lognorm", LN_CDF), ("dagum", DG_CDF)]:
        p = np.diff(F(EDGES)); print(nm, "classi attese vs osservate:", (p * N.sum()).round(0), N)
    print(f"T_ERP={T_ERP:,.0f}  T_GRIGIA={T_GRIGIA:,.0f}  canone ORD_L={RENT_ORD_L:,.0f}/anno "
          f"({RENT_ORD_L/12:,.0f}/mese)  T_MKT_lordo={T_MKT_GROSS:,.0f}  T_MKT_netto={T_MKT_NET:,.0f}")
    res = {}
    for right_name, tr in [("mercato 30% lordo", T_MKT_GROSS), ("fascia grigia ISEE 40k", T_GRIGIA),
                           ("mercato 30% netto", T_MKT_NET)]:
        for mode in ("dagum", "unif"):
            l = share_below(T_ERP, mode); r = share_below(tr, mode)
            res[(right_name, mode)] = (l, r - l, 1 - r)
            print(f"{right_name:24s} [{mode:5s}] sx={l:.3f} pancia={r-l:.3f} dx={1-r:.3f}")
    fig_concettuale()
    fig_empirica(T_ERP, T_MKT_GROSS, T_MKT_NET, res[("mercato 30% lordo", "dagum")])
