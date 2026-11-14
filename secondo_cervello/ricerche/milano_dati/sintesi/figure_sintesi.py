"""Tre figure di sintesi sulla pressione abitativa a Milano, solo dai CSV già derivati in ../mercato (nessun dato nuovo).
Uso: python3 -I figure_sintesi.py   Output: fig1_prezzi_redditi.png, fig2_peso_canone.png, fig3_ampiezza_pancia.png
Ipotesi e limiti: vedi ../02_mercato_e_accessibilita.md e ../03_pancia_della_gaussiana.md."""
import os, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(H, "..", "mercato")
rd = lambda f: pd.read_csv(os.path.join(M, f))
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# 1. Canoni e prezzi OMI contro inflazione e reddito, base 2015 S1 = 100
s = rd("omi_milano_serie_semestrale_civili_normale.csv"); s["t"] = s.Anno + (s.Periodo.str[0].astype(int) - 1) / 2
b = s[(s.Anno == 2015) & (s.Periodo == "1 semestre")].iloc[0]
h = rd("eurostat_indici_hicp_costi_prezzi_IT.csv").iloc[:, :2]; h.columns = ["Anno", "hicp"]; h = h[h.Anno >= 2015]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.plot(s.t, 100 * s.loc_mid_mediana / b.loc_mid_mediana, color="#b5651d", lw=2, label="Canone OMI (mediana zone)")
ax.plot(s.t, 100 * s.compr_mid_mediana / b.compr_mid_mediana, color="#355c7d", lw=2, label="Prezzo OMI (mediana zone)")
ax.plot(h.Anno + .5, h.hicp, color="#777", lw=1.5, ls="--", label="Inflazione IT (HICP, 2015=100)")
ax.plot([2014.5, 2024.5], [100, 100 * 41865 / 32478], color="#2a9d8f", marker="o", lw=1, ls=":", label="Reddito medio contribuenti (2014=100; solo due anni, retta indicativa)")
ax.axvline(2015, color="#ccc", lw=.8); ax.set_xlim(2014.5, 2026); ax.set_ylim(70, 190)
ax.set_title("Milano: dal 2022 canoni e prezzi superano inflazione e reddito medio", loc="left", fontsize=11)
ax.set_ylabel("indice (2015 S1 = 100)"); ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.text(.01, .01, "Fonti: OMI-Comune di Milano [V]; Eurostat HICP [V]; MEF IRPEF 2014 e 2024 [V].\nReddito: solo due anni, base 2014; OMI e HICP hanno base 2015 [H].", fontsize=6.5, color="#555")
fig.tight_layout(rect=(0, .06, 1, 1)); fig.savefig(os.path.join(H, "fig1_prezzi_redditi.png"), dpi=200); plt.close(fig)

# 2. Quota del reddito netto per affitto (RTI), per tipo di nucleo, canone mediano cittadino, per percentile dei redditi
a = rd("accessibilita_famiglie_tipo.csv"); a = a[a.zona.str.startswith("citta")]
fig, ax = plt.subplots(figsize=(7.5, 4.2)); cols = ["#355c7d", "#b5651d", "#2a9d8f", "#c0392b", "#7d5ba6"]
for c, (t, g) in zip(cols, a.groupby("tipo", sort=False)):
    g = g.sort_values("percentile", key=lambda x: x.str[1:].astype(int)); ax.plot(g.percentile, 100 * g.RTI, marker="o", color=c, label=t)
ax.axhline(30, color="#333", ls="--", lw=1); ax.text(0.02, 31.5, "soglia 30% del reddito netto", fontsize=8)
ax.set_ylabel("canone / reddito netto del nucleo (%)"); ax.set_xlabel("percentile dei redditi dei contribuenti milanesi")
ax.set_title("Chi regge un affitto medio (canone OMI cittadino)", loc="left", fontsize=11); ax.legend(frameon=False, fontsize=7.5)
fig.text(.01, .01, "Fonti: MEF IRPEF a.i. 2024 [V]; OMI 2025 S2 [V]; ipotesi sul nucleo e sul netto [H] (vedi 02_mercato_e_accessibilita.md). Il percentile è individuale, non familiare.", fontsize=6.5, color="#555")
fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(os.path.join(H, "fig2_peso_canone.png"), dpi=200); plt.close(fig)

# 3. Ampiezza della pancia (punti percentili tra soglia ERP e soglia di mercato) per tipo e fonte del canone
p = rd("pancia_erp_mercato.csv"); p["f"] = p.zona.map(lambda z: "annunci [S]" if "annunci" in z else ("periferia" if "periferia" in z else "città"))
t = p.pivot(index="tipo", columns="f", values="ampiezza_pancia_pp")[["periferia", "città", "annunci [S]"]]
fig, ax = plt.subplots(figsize=(7.5, 4.2)); t.plot.barh(ax=ax, color=["#2a9d8f", "#355c7d", "#b5651d"], width=.75)
ax.set_xlabel("ampiezza della pancia (punti percentili)"); ax.set_ylabel("")
ax.set_title("La pancia varia molto con la fonte del canone", loc="left", fontsize=11); ax.legend(frameon=False, fontsize=8, title="canone", loc="lower right")
fig.text(.01, .01, "Fonti: MEF [V], OMI [V], annunci [S]; soglia ERP ISEE 16.000 € convertita in reddito [H]. Una persona = un percentile: non è la quota di famiglie.", fontsize=6.5, color="#555")
fig.tight_layout(rect=(0, .03, 1, 1)); fig.savefig(os.path.join(H, "fig3_ampiezza_pancia.png"), dpi=200); plt.close(fig)
