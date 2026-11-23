# Banco di laboratorio — piano (ticket #17)

Versione 2, 2026-11-23, su richiesta di Dennis (tramite il coordinatore): il banco si costruisce **sulla pagina dello Spatial Milano Lab** (`tesi/DECISIONI.md`, 09/11), senza Leaflet né sfondi esterni, che il visualizzatore degli artifact blocca. La versione 1 (Leaflet + tile OSM, piano e test) è in `archivio/`, non cancellata.

## Cosa mostra
- La pagina del Lab così com'è (`lab_completo/prototype/site/spatial-milano-lab.html`, SHA-256 verificato contro `INVENTARIO_SCRATCH.txt`): mappa dei NIL disegnata in SVG, globo iniziale, fasi, chat SPATIAL in modalità demo (o Claude dove disponibile), dashboard Popolazione, Densità 3D (esagoni), Stipendi e affitti, Uso del suolo DUSAF, PGT 2030, Verde e calore, Metro, Edificato DBT 2020 (densità volumetrica, copertura, altezza mediana per NIL), strati Metro e Zone OMI.
- DUSAF e PGT incorporati nella pagina (prima erano file accanto alla pagina).
- Nuova dashboard e fase "Base L v7: lotti": strato SVG dei 701 lotti nel sistema di coordinate del Lab (edificabile, da riusare, attivazione; GFU tratteggiate e "non verificato"); il pulsante "Lotti Base L v7" li mette sopra ogni altra dashboard piatta.
- Nel pannello: le quattro avvertenze; filtri per classe, proprietà, ambito, stato attuativo, ricerca per id; totali con capacità come forbice; scheda del lotto con marche; Base E v2 (congelata il 23/11) per lotto (fasce B, C, D) e a livello di pagina; legenda delle marche; fonti e SHA-256.
- Tema chiaro e scuro secondo `prefers-color-scheme` (il Lab era solo scuro; il pulsante della mappa di base resta).

## Cosa non mostra
- Pannello "Cooperativa ed edificio": **non c'è nelle copie recuperate del Lab** (né in `proto.src.html` né nelle due pagine da artifact) [L]; nulla da togliere.
- Modelli di analisi del Lab (siti candidati, SMAA, portafogli, audit, voto, potere d'acquisto e domanda: dashboard `lab` e `pp`, `lab.json`): esclusi per la decisione del 09/11; gli strumenti della chat che li usano sono filtrati.
- Edifici 3D per quartiere (dashboard `city`): i tasselli DBT `data/t/*.json` non sono nel repo (solo cartella condivisa e PC) [L]. Restano gli indicatori DBT per NIL.
- Immagini AGEA o Sentinel-2; conteggi di lotti per la cessione; Base E per GFU, aree di attivazione e acquisto in fascia E (E7).

## Criteri di accettazione (`test_banco.cjs`, `build.py`)
B0. `build.py` si ferma se uno SHA-256 (pagina del Lab, DUSAF, PGT, Base L v7, tabelle Base E v2) non coincide con il riferimento, se una sostituzione nella pagina del Lab non è univoca o se i totali non coincidono con VERSIONE.md / `scenari_capacita.csv`.
B1. Risorse esterne solo Google Fonts; nessun `fetch` raggiungibile; con la rete bloccata la pagina si apre senza errori JS (prova per il visualizzatore).
B2. 701 lotti disegnati: 216 / 167 / 268 / 50, anche nei conteggi del pannello.
B3. 88 NIL del Lab; DUSAF, PGT e la mappa DBT per NIL si disegnano, con i lotti sopra.
B4. Dashboard `city`, `lab`, `pp` assenti; `lotti` presente.
B5. Zero errori JS a 1280 e 400 px, tema chiaro e scuro, prima e dopo le interazioni; a 400 px nessuno scorrimento orizzontale.
B6. Attivazione e GFU senza capacità; GFU tratteggiate e "non verificato"; totali edificabili 16.389 / 32.885 / 65.885.
B7. `banco.html` sotto 5 MB; cartella sotto 20 MB.
B8. Quattro avvertenze in pagina; nessun conteggio di lotti per la cessione.
B9. Zoom della mappa piatta (NIL, strati e lotti), aggiunto il 23/11 su richiesta di Dennis: rotella attorno al puntatore, pinch a due dita, pulsanti + / − / ⟳ del Lab (prima solo per il 3D) e trascinamento, sulla viewBox dell'SVG (`setVB` del Lab), senza librerie; spessore delle linee costante (`vector-effect: non-scaling-stroke`, già nel Lab). Il test verifica, a 1280 e 400 px e nei due temi: rotella e pulsanti cambiano la viewBox, il trascinamento la sposta, il pinch (eventi pointer simulati) avvicina, ⟳ torna alla vista iniziale, il clic su un lotto da zoomati apre la sua scheda, zero errori JS.
