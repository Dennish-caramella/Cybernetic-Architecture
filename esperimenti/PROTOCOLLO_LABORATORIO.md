# Protocollo del laboratorio

Vale per ogni agente del team (`.claude/agents/`) e per ogni prova della mappa [Mappa: scala urbana collaudata su dati reali di Milano](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/15). Leggerlo prima di qualsiasi lavoro.

## Prima di iniziare
1. Leggi `CONTEXT.md` (glossario: usa solo i termini canonici), `tesi/DECISIONI.md`, `tesi/CONFRONTO_APPROCCI_ALLOCAZIONE.md` e il ticket della prova (`gh api repos/Dennish-caramella/Cybernetic-Architecture/issues/<n>`).
2. Lavora solo nella cartella della prova: `esperimenti/<ID>_<nome>/` (es. `esperimenti/L_lotti/`). Non modificare basi congelate, altre prove, `tesi/` o `STATO.md`.

## Integrità (non negoziabile)
- Mai inventare fonti, numeri, dataset, formule o risultati. Ogni affermazione porta una marca: **[V]** verificato in questa sessione (file aperto, dato scaricato, URL e data); **[S]** fonte secondaria; **[I]** inferenza; **[H]** ipotesi o parametro scelto; **[L]** lacuna.
- Se un dato manca, dichiaralo e fermati su quel punto: non sostituirlo con un valore plausibile senza marcarlo [H] e senza un'analisi di sensibilità.
- Non aggirare blocchi di rete o di permesso: segnalali nel report.

## Codice
Prima di scrivere codice carica la skill `ponytail` (livello full) e seguila: il minimo codice che risolve tutta la prova, librerie standard prima di quelle nuove, nessuna astrazione non richiesta. Chiudi con una riga su cosa non hai verificato.

## Riproducibilità
- Tutto si rifà da zero con uno script (`run.py` o equivalente) e un `README` di due righe. Seme casuale fisso e dichiarato.
- Dati grezzi pesanti fuori da git (scaricati dallo script in `esperimenti/_cache/`, ignorata); nel repo solo dati derivati piccoli (< 20 MB per prova) e i metadati con fonte, licenza e data.
- Test minimi sugli invarianti (es. ogni lotto ha geometria valida e fonte; la capacità assegnata non supera quella del lotto).

## Basi congelate
Una base chiusa (L, P, E) riceve `VERSIONE.md` con data, hash dei file e numero di versione. Non si modifica: una correzione è una nuova versione con un nuovo ticket.

## Report di laboratorio (`esperimenti/<prova>/REPORT.md`)
1. **Ipotesi e soglia**, fissate prima (per le basi: criteri di accettazione).
2. **Dati e fonti** (con marche).
3. **Metodo** (formule in LaTeX dove servono).
4. **Risultati** (tabelle, figure in `fig/`).
5. **Esito** rispetto alla soglia: passa / ripeti / cambia.
6. **Limiti**.
7. **Revisione indipendente**: scritta dal `revisore-metodologico` (e, dove indicato, dal `revisore-governance-etica`), che non ha eseguito la prova.
8. **Cosa passa alla prova successiva**.

## Regola di arresto
Se la prova non supera la soglia o il revisore segnala un difetto grave, ci si ferma: si apre un ticket di revisione e si decide con Dennis.

## Metodi B0–B6 (indipendenza)
Ogni metodo è eseguito da un agente che **non legge** le cartelle degli altri metodi né i loro esiti. Input: solo le basi congelate e `esperimenti/prereg/`. Output: `esito_sigillato.parquet` + hash in `SIGILLO.txt`. Il confronto lo fa un agente che non ha eseguito nessun metodo.

## Chi fa cosa
| Ticket | Esegue | Supporta | Revisiona |
|---|---|---|---|
| Base L: lotti | dati-geo-milano | urbanista-pgt-milano | revisore-metodologico |
| Banco di laboratorio | visualizzazione-banco | dati-geo-milano | revisore-metodologico |
| Base P: popolazione | demografo-popolazioni-sintetiche | econometrico-preferenze | revisore-metodologico |
| Base E: economia | economista-abitativo | urbanista-pgt-milano | revisore-metodologico |
| Pre-registrazione | scelta-sociale-computazionale (con Dennis) | revisore-metodologico | — |
| A1 multicriterio | analista-decisionale-mcda | — | revisore-metodologico |
| A2 accessibilità | analista-accessibilita | dati-geo-milano | revisore-metodologico |
| A3 fattibilità | economista-abitativo | — | revisore-metodologico |
| A4 raccomandazione | econometrico-preferenze | analista-decisionale-mcda | revisore-metodologico, revisore-governance-etica |
| B0–B6 | market-design-matching (un'istanza per metodo) | — | — |
| Confronto cieco | revisore-metodologico (in ruolo di analista del confronto) | scelta-sociale-computazionale | revisore-governance-etica |
| Sintesi | coordinatore (sessione principale) | tutti | revisore-metodologico |
