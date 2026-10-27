# Audit della cartella TESI (sola lettura)

Data: 2026-10-10. Nessun file esistente è stato modificato, spostato o cancellato.
Questo file è stato aggiunto in Fase 2 per documentare l'audit.

## Cosa funziona

- `03_Analisi Approfondite/`: 24 analisi (file 01–24) più l'indice `00_Indice_Generale_e_Guida_delle_Analisi.md`.
  - Tutte le 24 voci dell'indice puntano a file esistenti (verificato sui link).
  - Tutte le analisi hanno la chiusura richiesta dalle Linee Guida ("Se dovessi condensare…").
  - Lunghezze: da circa 1.750 a circa 4.400 parole. Nessun file vuoto.
- `01_Ricerche Teoriche/`: 18 PDF corrispondono alle analisi 01–18 (abbinamento per titolo e autore).
- `00_Istruzioni Progetto/00_Linee_Guida_Analisi_PDF_e_Materiali_Didattici.md`: completo, 41 sezioni.

## Cosa non funziona

1. **File letti "a inizio sessione" assenti.** `00_Istruzioni Progetto/istruzioni_progetto_tesi.md` e `04_avanzamento/stato_avanzamento.md` non esistono. In `00_Istruzioni Progetto/` ci sono solo `00_Linee_Guida…` e `01_Prime considerazioni.md`. Non esiste quindi uno stato di avanzamento leggibile.
2. **Second brain descritto ma non presente.** Mancano `01_schede/`, `02_sintesi/` (con `00_REPORT_FONDATIVO.md`, `01_temi_…`, `02_mappe_…`, `_profili/`), `02_sintesi/INDICE_SCHEDE.md`, `graphify-out/`, `.graphifyignore`, `04_avanzamento/aggiorna_indice.py`. Nel progetto non esiste alcuno script `.py`.
3. **Report fondativo assente.** Il `REPORT_FONDATIVO` ("da tenere sempre come riferimento") non è nella cartella.
4. **Avviso di verifica non propagato.** Il `CLAUDE.md` di root dice che le "schede 11–14 (Stigmergic Spaces, Bartlett)" sono state verificate il 2026-10-07 con report in `01_schede/00_verifica/` e NON corrette. Il report non esiste. Nella numerazione attuale: 11 = Sanchez, 12 = Meyboom/Reeves (Stigmergic), 13 = Veloso et al., 14 = MVRDV HUB. Nessuna analisi porta un avviso di verifica. Il riferimento a "Bartlett" è ambiguo: nel corpus Bartlett compare come sede accademica (analisi 08 su Carpo, analisi 18 su Koehler, RC17). Il riferimento a Horizon, InterX, Civic Canvas, Meta-CLT non compare in nessun file del corpus.
5. **Fonte non presente.** L'analisi 24 (De Carlo, *L'architettura della partecipazione*) non ha PDF in cartella. La bibliografia dice "questo non ce l'ho in formato digitale". La provenienza del riassunto non è verificabile dai file.
6. **Bibliografia non coperta.** `01_Ricerche Teoriche/bibliografia consigliatra.md` cita circa dieci opere senza PDF in cartella (Zevi, Dovey, Habraken, Hertzberger ×2, Hillier, Kipnis, Vidler, Leach, Mintrone & Erioli). Il file ha un refuso nel nome ("consigliatra").
7. **Nomi dei PDF non allineati.** In `01_Ricerche Teoriche/` i prefissi numerici sono duplicati (00, 01, 02, 03, 05, 08 con due file ciascuno) e non seguono la numerazione 01–24 delle analisi.
8. **`00_Schemi e Mappe/` quasi vuota.** Contiene solo `.archify/workflow-housingprime-ottimizzazione-20261010-162925/candidate.json`. Il suo campo `output` punta a `gioco/housingprime-ottimizzazione.html`, che non esiste. Nessuna mappa o schema del corpus è presente.
9. **Formato non uniforme.** Le analisi 01–18 aprono con `# 1. La tesi centrale di …`. Le analisi 19–24 usano un'intestazione diversa con blockquote di autori. La chiusura dell'analisi 10 usa una formula diversa da quella prescritta.
10. **Link assoluti.** L'indice 00 usa link `file:///C:/Users/…`. Funzionano solo su questo computer.
11. **`01_Prime considerazioni.md` non è un'analisi.** È la trascrizione di una conversazione in tono colloquiale ("tu") su gamification, Pareto, RL e Block'hood. Inizia con "# 43.", non ha fonte né data. Contiene riferimenti a progetti esterni non verificati nel corpus. Non va usato come fonte.
12. **Binari non letti.** `02_MVRDV Research/`: 368 file, circa 902 MB, di cui 274 TIF, 28 EPS, più `MVR001_book_inside_LOWRES.pdf` (155 MB) e `WEGO_Full Book.pptx` (137 MB). Non sono stati letti. I PDF leggibili più piccoli (Spacefighter, OptiMixer2_14, Climatizer exhibition 02/07) non sono stati aperti.

## Limiti di questo audit

- Letti per intero: indice 00 dell'analisi, bibliografia, le due Linee Guida e il file `01_Prime considerazioni.md` (solo struttura e coda).
- Verificati su tutte le 24 analisi: struttura, lunghezza, chiusure, link, riferimenti incrociati, presenza di avvisi.
- Non riletto riga per riga il corpo delle 24 analisi (circa 560 KB di testo).
- I PDF non sono stati aperti: il collegamento analisi→PDF è per titolo e autore, non per contenuto.
