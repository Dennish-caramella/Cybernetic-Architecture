# Banco di laboratorio — piano (ticket #17)

Scritto prima del codice, il 2026-11-23. Base: Spatial Milano Lab (artifact LHHSCseATyEEmS4g7SoTW5) come infrastruttura di mappa e NIL, **senza** il pannello "Cooperativa ed edificio" (`tesi/DECISIONI.md`, 09/11). Il Lab disegnava la mappa su canvas con coordinate proprie; qui si usa Leaflet con sfondo OSM, più semplice da estendere con gli strati delle prove successive [H, scelta di progetto].

## Cosa mostra
- Mappa di Milano, sfondo OpenStreetMap (ODbL, attribuzione in pagina). Nessuna immagine AGEA (sola visione) né Sentinel-2 EOX (CC BY-NC-SA).
- Strato NIL (ds964, Comune di Milano, CC BY 4.0): 88 perimetri, nome e conteggio dei lotti per classe.
- Strato lotti della Base L v7 (`lotti_v7.gpkg`, SHA-256 verificato al build contro `VERSIONE.md`): lotto edificabile, lotto da riusare, area di attivazione; lotto GFU separato, tratteggiato, con la nota "non verificato".
- Scheda del lotto: id, classe, superficie, capacità come forbice FAR 0,5 / 1 / 2 (e recupero per il riuso), origine, ambito PGT 2030 (nome, codice, strumento, data, fonte), stato attuativo (categoria A–D/N del censimento con marca), proprietà, vincoli noti, NIL, fonti e licenze; per le GFU la capacità solo come "scenario, non verificato" e la nota di verifica della destinazione.
- Base E v2 (candidata, non congelata) per i lotti edificabili e da riusare: zona e fascia OMI; per le fasce B, C, D canone di pareggio con suolo a mercato (60 anni, FAR 1, regione tarata, 5–50–95%) e quota della regione in cui l'acquisto regge a 90 €/m²/anno. A livello di pagina: canone di pareggio con suolo gratuito per tre regioni e tre durate (`c_star_per_regione.csv`) e la quota della cessione come quota della regione, uguale per tutti i lotti.
- Filtri: classe, proprietà, gruppo di ambito (PA, AdP, GFU, fuori ambito), stato attuativo; ricerca per id.
- Totali: conteggi per classe e capacità degli edificabili come forbice; GFU e attivazione fuori dai totali.
- Legenda delle marche [V] [S] [I] [H] [L] e avvertenze: capacità come forbice; GFU non validate; C5 inconcludente, base congelata per decisione di Dennis; la Base E non è un vincolo.

## Cosa non mostra
- Pannello Cooperativa ed edificio; modelli di analisi del Lab (domanda, audit, portafogli, SMAA, PU).
- Immagini AGEA o Sentinel-2.
- Conteggi di lotti per la cessione; Base E per GFU e aree di attivazione; acquisto in fascia E (E7 "non informativo"; REPORT E v2 §8: acquisto solo per B, C, D).
- Codifiche C5 per lotto.

## Criteri di accettazione (verificabili con `test_banco.mjs` e `build.py`)
A1. `build.py` si ferma se lo SHA-256 di `lotti_v7.gpkg` è diverso da `5d464a3c…` (VERSIONE.md) o se i totali non coincidono con VERSIONE.md / `scenari_capacita.csv`.
A2. Nella pagina ci sono tutti i 701 lotti: 216 edificabili, 167 da riusare, 268 attivazione, 50 GFU; 88 NIL.
A3. Le aree di attivazione hanno capacità nulla e la scheda non mostra capacità; le GFU non entrano nei totali, sono tratteggiate e la scheda dice "non verificato".
A4. Totali in pagina: edificabili 16.389 / 32.885 / 65.885 alloggi (FAR 0,5 / 1 / 2).
A5. Zero errori JavaScript in Chromium (Playwright), a 1280 px e a 400 px, tema chiaro e scuro; a 400 px nessuno scorrimento orizzontale.
A6. Script solo da cdnjs con versione esatta e SRI; nessun'altra risorsa esterna salvo le tile OSM.
A7. `banco.html` sotto 5 MB; dati derivati della cartella sotto 20 MB. Geometrie semplificate (tolleranza dichiarata nel README e in pagina).
A8. Le quattro avvertenze compaiono in pagina; nessun conteggio di lotti per la cessione.
