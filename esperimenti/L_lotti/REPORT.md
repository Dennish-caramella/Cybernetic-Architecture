# Base L v1 — lotti candidati reali di Milano (report di laboratorio)

Ticket: [#16](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/16) (mappa #15). Esegue: `dati-geo-milano`, con `urbanista-pgt-milano` come consulente. Revisione: `revisore-metodologico` (sezione 7).
Marche: **[V]** verificato in questa sessione, **[S]** fonte secondaria, **[I]** inferenza, **[H]** ipotesi o parametro scelto, **[L]** lacuna.

## 1. Criteri di accettazione (scritti prima di eseguire `run.py`, 2026-11-11)

La Base L v1 passa se **tutti** i criteri C1–C6 sono soddisfatti. C7 è informativo (confronto con il Lab), non bloccante.

| # | Criterio | Soglia |
|---|---|---|
| C1 | Geometrie: ogni lotto ha geometria poligonale non vuota e valida (`is_valid`), CRS dichiarato EPSG:32632 | 100% |
| C2 | Attributi: `id` unico; `classe`, `proprieta`, `area_m2 > 0`, `capacita`, `nil_id`, `fonti`, `licenze` non vuoti; ogni attributo ha fonte e licenza nella tabella `metadati` | 100% |
| C3 | Sovrapposizioni: nessuna coppia di lotti (stessa classe o classi diverse) si sovrappone oltre la tolleranza max(5 m², 1% dell'area del lotto più piccolo) | 0 coppie oltre tolleranza |
| C4 | Capacità: `capacita` intera, `m_min <= capacita <= m_max` per i lotti edificabili; `capacita >= 1` per i lotti da riusare | 100% |
| C5 | Controllo a campione con fonte indipendente (DUSAF 8.0, 2024, fotointerpretazione regionale; indipendente da catasto e DBT 2020). Campione casuale di 30 lotti per classe, seme 42. (a) Edificabili: il lotto non è occupato per più del 50% da tessuto residenziale (DUSAF 111/112) né da verde, agricolo, boschi o acque (DUSAF 14x, 2xx, 3xx, 4xx, 5xx). (b) Da riusare: il lotto cade su suolo artificiale (DUSAF 1xx) per almeno il 50% della sua area | (a) ≥ 70% del campione; (b) ≥ 70% del campione |
| C6 | Conteggi: tabella per NIL × classe e tabella a cascata dei filtri prodotte; somma per NIL = totale per classe | esatta |
| C7 | (informativo) Coerenza col Lab: numero di siti edificabili prima del filtro di capacità entro ±25% dei 2.291 siti del Lab (paper §3.2) | 1.718–2.864 |

Regola di arresto (protocollo): se C1–C6 non passano, la base non si congela come v1 e si apre un ticket di revisione.
