# STATO

Aggiornato 2026-10-28. Storia completa: `giornale/CRONOLOGIA_COMPLETA.md`. Una riga per giorno: `giornale/GIORNALE.md`.

## Fase
Ricerca e sintesi, con prove sulla Fase 1 (urbanistica, Milano). Scrittura rimandata. Direzione dichiarata il 27/10 nell'issue #5: **un anno**, prove ed errori che definiscono la ricerca; Fase 1 scala urbana e lotti partecipativi, Fase 2 progetto sul lotto (kit of parts, negoziazione, Assembler, gioco/RL); solo persone, niente developer.

## Corpus
- 37 schede in `secondo_cervello/schede/` (01–37). 01–36 identiche tra PC e cartella condivisa (controllato il 27/10). La 37 (Azadi) è a livello abstract, testo sotto embargo fino al 23/09/2027.
- Modelli matematici: `secondo_cervello/modelli/` (Atlante, Catalogo, Cronistoria, Studio, Verifiche).
- Report fondativo: bozza di impianto del 20/10 (una versione più recente nella condivisa, una più vecchia sul PC archiviata). Riformulazione PhD del 25/10.

## Prove
- In evidenza: Spatial Milano Lab (`prove/in_evidenza/2026-10-25_spatial_milano_lab`), pipeline Milano (`2026-10-21_pipeline_milano`).
- Riesame (issue #6): nessun risultato del laboratorio è oggi una prova (domanda, rischio PGT e +48% sono artefatti o rumore). Preferenze dei cittadini: tutte sintetiche.

## Avvisi aperti
1. ~~Tesi magistrale o dottorato?~~ Chiuso il 27/10: dottorato, un anno (Dennis). Le istruzioni sono aggiornate; il topic del progetto su Claude dice ancora "tesi magistrale".
2. **Pipeline Milano su dati reali (22/10)**: la cronologia dice eseguita (1.911 celle H3, 348 tile 3D, `RAPPORTO_ESECUZIONE.md`, `MANIFEST.csv`), ma quei file non sono né nella cartella condivisa né in `Desktop\TESI\05_Urbanistica` (vuota). Qui c'è solo la versione con dati sintetici del 21/10.
3. ~~Spatial Milano Lab incompleto~~ Chiuso il 28/10: copiato tutto lo scratch (1024 file, hash verificati). Codice e dati leggeri nel repo, dati medi in cartella condivisa, grezzi sul PC (`RECUPERO.md`). Nessuno script rieseguito; `build_mi.py` richiede `istat_samples/` accanto a `mi/`.
4. Dati numerici non verificati nelle schede 08, 14, 20, 23. Incoerenza interna scheda 13 (16 o 18 prototipi). Residui di estrazione PDF nella scheda 10. Hillier 1989/2015 (scheda 17).
5. Scheda 24 (De Carlo): appunti dell'autore, non fonte; citazioni da verificare sul libro.
6. Tutto ciò che nel Report fondativo e nei modelli è [S]/[L] resta da verificare sui PDF.

## Prossimi passi
1. Rispondere all'avviso 2 (dove sono i file della pipeline su dati reali).
2. Issue #10 (domanda di ricerca e perimetro), #11 (attori e pesi), #12 (prove Fase 1).
3. Recuperare dal PC i file dell'avviso 2. Rieseguire `run.py` sul PC per confermare che i risultati si riproducono.
4. Fondere Report fondativo e Riformulazione PhD.
