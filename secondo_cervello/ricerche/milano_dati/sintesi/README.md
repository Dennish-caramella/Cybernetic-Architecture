# Sintesi socio-economica (potere d'acquisto, canoni, "pancia") — stato al 14/11/2026

Base teorica e dati per la domanda di ricerca. **Non nuovi calcoli**: le tre figure sono ridisegnate dai CSV già derivati in `../mercato/` (script `figure_sintesi.py`, riproducibile).

| Figura | Cosa mostra | Limite principale |
|---|---|---|
| `fig1_prezzi_redditi.png` | Canoni e prezzi OMI (2015–2025) contro inflazione e reddito medio dei contribuenti (2014 e 2024) | reddito solo su due anni, basi diverse [H] |
| `fig2_peso_canone.png` | Quota del reddito netto spesa per un affitto medio, per tipo di nucleo e percentile | percentile individuale, non familiare; ipotesi sul netto [H] |
| `fig3_ampiezza_pancia.png` | Ampiezza della "pancia" (punti percentili tra soglia ERP e soglia di mercato) per nucleo e fonte del canone | cambia molto con la fonte (annunci [S] contro OMI) |

Documenti di base: `../02_mercato_e_accessibilita.md`, `../03_pancia_della_gaussiana.md` (con le figure concettuale ed empirica in `../pancia/`), `../05_fasce_e_strumenti_abitativi.md` (soglie ERP, housing sociale, Piano Casa; figura in `../fasce/`), `../06_famiglie_studenti_nuovi_arrivi.md`.

## Ancora mancante
- Unità familiare (oggi contribuente individuale), ISEE aggregati INPS e redditi per famiglia.
- Canoni per NIL, zona OMI e dimensione del nucleo (oggi mediana cittadina o per fascia).
- Domanda latente (liste di attesa, coabitazione, chi lascia Milano): non misurabile dai registri; va dichiarata (vedi `../../11_bartlett_rc10_linx_civic_matrix_urban_sutures.md`, §"Cosa ne ricaviamo").
- Fonti primarie per i dati [S] (bandi ALER, Piano Casa).
- Costi di costruzione e manutenzione (rinviati, Base E).
