# Cosa mostra il Digital Planning Hub di ZHA (Bengasi 2050) e come lo traduciamo per Milano

Fonte: analisi di una sessione precedente sul post Instagram di ZHA del 16 settembre 2026 (14 slide, 4 video da 30-39 s, fotogrammi ogni ~2 s), più articoli di stampa (Designboom, Illustrarch). Non ho rivisto io i fotogrammi: gli screenshot non sono nella cartella condivisa. Marche: [V] visto nei video secondo quella analisi, [I] deduzione di chi ha analizzato o mia.
Nessun modello di IA, software o formula è dichiarato da ZHA. Quel che si vede è GIS classico.

## I 4 video [V salvo indicato]
1. **Idoneità e allocazione della crescita.** Layer in tre famiglie: EXC (esclusione: aeroporti, rischio alluvione/wadi, acqua, strade, morfologia), GRO (limiti di crescita, edifici demoliti, uso del suolo), ATT (attrattori: centri, rete stradale, costa, fasce lago). Compositi in un "suitability terrain" 3D; un piano di domanda lo taglia; contatore "Added 388,675 / 1,000,000" abitanti. [I] maschere binarie x somma pesata di attrattori, riempimento greedy fino alla domanda.
2. **Gemello 3D degli edifici.** Selettore 2026/2050; selezione di distretti con superficie lorda costruita, numero edifici, quota residenziale, istogrammi (uso, altezza, superficie, area). Esempio: 6 distretti = 77.186 edifici, 79,7% residenziali.
3. **Posti di lavoro.** Esagoni estrusi (colonne), 320.446 posti stimati, per commerciale/industriale/pubblico, filtro per 17 distretti. [I] stima da superficie per tipo d'uso x densità addetti.
4. **Accessibilità.** Su ~200.024 edifici: bacini a piedi 5/10/15 min verso clinica, ospedale, mercato, parco, scuole, università; indice pedonale 0-5; bacini in auto a 2 orari (13:00 punta, 23:00); indice di dipendenza dall'auto. [I] Dijkstra su grafo stradale.

## Tratti di interfaccia da riprodurre
- Un solo modello 3D della città reale (edifici estrusi), non la sola griglia.
- Selezione di aree/distretti con statistiche immediate e istogrammi.
- Strati accendibili; esagoni usati solo come aggregazione per alcuni indicatori.
- Accessibilità calcolata per edificio, non per cella.
- Selettore scenario/anno (2026/2050).
- "Terreno di idoneità" 3D e piano di domanda: l'idea più vicina alla nostra graduatoria dei lotti.

## Traduzione per Milano (tesi: dove stanno i lotti migliori per colmare il gap di accessibilità abitativa)
| Hub Bengasi | Milano |
|---|---|
| EXC maschere | vincoli (aree protette, idraulico, vincolo culturale), dati ufficiali dove esistono |
| ATT attrattori | metro, servizi, verde (dal Comune) |
| GRO / Available land | immobili comunali, dismessi PGT, demanio, bonifiche |
| Domanda 1.000.000 ab. | fabbisogno abitativo (OMI/reddito, famiglie): obiettivo da definire con Dennis, non inventato |
| Posti di lavoro per esagono | non centrale; eventualmente accessibilità ai lavoratori |
| Accessibilità per edificio | accessibilità per lotto/edificio con grafo stradale |
| Scenari 2026/2050 | scenari di pesi (4 preset) |

## Differenze nette
- Bengasi mostra allocazione di crescita; noi ordiniamo lotti esistenti. Il "piano di domanda" in tesi diventa: quanti alloggi/lotti servono per ridurre il gap, da definire.
- ZHA non espone i pesi; noi sì, ed è il contributo della tesi.
