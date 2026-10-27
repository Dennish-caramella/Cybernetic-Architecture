# Stato di avanzamento della tesi

Aggiornato: 2026-10-18. Questo file è il registro dello stato. Va aggiornato ad ogni sessione di lavoro: una voce datata per ogni cambiamento, senza cancellare le voci precedenti.

## Fase attuale

**Ricerca e sintesi** (come da istruzioni di progetto). La scrittura della tesi è rimandata. Il Report fondativo (basi teoriche e tecniche) non esiste ancora: va redatto.

## Stato del corpus

| Voce | Stato | Note |
|---|---|---|
| Analisi approfondite 01–27 (`03_Analisi Approfondite/`) | 27 presenti, redatte integralmente | Tutte con struttura quadripartita, diagrammi testuali e chiusura "Se dovessi condensare". |
| Indice 00 (`03_Analisi Approfondite/00_Indice_Generale_e_Guida_delle_Analisi.md`) | Presente, coerente con i file | 27 link relativi a percorsi assoluti `file:///C:/...` |
| Linee guida di analisi (`00_Istruzioni Progetto/00_Linee_Guida_…`) | Presenti, complete | Metodo di riferimento per ogni nuova analisi |
| Bibliografia (`01_Ricerche Teoriche/bibliografia consigliatra.md`) | Presente | Circa dieci opere senza PDF in cartella |
| PDF teorici (`01_Ricerche Teoriche/`) | 20 PDF corrispondono alle analisi teoriche (01–18, 25, 26, 27) | Tutte le fonti PDF in cartella hanno ora un'analisi dettagliata corrispondente |
| Materiali MVRDV (`02_MVRDV Research/`) | 368 file, circa 900 MB, in gran parte TIF/EPS | Fonti PDF/PPTX analizzate in 19–23 |
| `01_Prime considerazioni.md` | Letto integralmente | È una chat, non una fonte. Trattare come ipotesi di progetto |
| Second brain (`00_Schemi e Mappe/Second_Brain_Analisi_Approfondite/`) | Aggiornato il 2026-10-18 | `01_INDICE_BREVE.md` include le schede 01–27 |

## Avvisi di verifica aperti

1. ~~**Schede 11–14 (Stigmergic Spaces, Bartlett)**~~: chiuso il 2026-10-10 dall'autore. Il report di verifica non serve più.
2. **"Bartlett"**: nel corpus compare come sede accademica (analisi 08 su Carpo, analisi 18 su Koehler con il gruppo RC17). I progetti Horizon, InterX, Civic Canvas e Meta-CLT non compaiono in nessun file. Resta come nota, non come avviso.
3. ~~**Analisi 24 (De Carlo)**~~: chiuso il 2026-10-10. È un testo scritto dall'autore durante la lettura del libro: appunti personali, non fonte esterna. Le citazioni dirette di De Carlo vanno comunque verificate sul libro.
4. **Dati numerici non verificati nei testi**: percentuali e cifre citate nelle analisi (es. 08: "40% delle emissioni"; 14: quote di reddito e di solitudine; 20: punteggi di soddisfazione 75/72/65/53%; 23: cifre del modello climatico). Da verificare sulle fonti prima di citarli.
5. **Incoerenza interna analisi 13**: la sezione 2 dice "sedici prototipi", le conclusioni "18 prototipi" (il conteggio dei tre tipi dà 18).
6. **Residui di estrazione PDF**: l'analisi 10 contiene in più punti la riga "04_De Graaf, R. _ Four Walls an…". Da ripulire.
7. **Datazione da verificare**: analisi 17 cita *Space is the Machine* di Hillier nel 1989; la bibliografia cita l'edizione 2015.

## Cronologia

- **2026-10-21 (pipeline Milano, senza LLM)**: scritta e collaudata la pipeline in `05_Urbanistica/pipeline_milano/` (griglia H3, interpolazione areale, accessibilità pedonale su grafo, PCA e K-Means con validazione, idoneità multicriterio con pesi e sensibilità, lotti candidati, viewer 2D/3D). 6 test di calcolo passano; esecuzione completa su dati SINTETICI in pochi secondi. **Mai eseguita su dati reali**: la sessione non raggiungeva i portali dei dati. Da fare sul computer dell'autore: scaricare le fonti, compilare le colonne in `config/sources.yaml`, eseguire. Lettura critica dei documenti Orchestratore, Pipeline e Modelli ZHA/MIT in `00_Avanzamento/02_sintesi/LETTURA_CRITICA_FASE_1_MILANO.md` (se presente) con i punti da correggere: risultati scritti prima dell'analisi, agenti LLM che muovono i pesi, T1 attribuito ad Alexander, fonti non verificabili.
- **2026-10-20 (report fondativo, bozza)**: redatto `02_sintesi/REPORT_FONDATIVO.md` come bozza di impianto: problema e lacuna (L1–L3), domanda principale e 5 sottodomande, tesi provvisoria e 4 ipotesi falsificabili (H1–H4), 6 assi di ricerca con letture, concetti, criterio di falsificabilità e nota critica, piano di prove P1–P5, limiti e rischi, elenco di 12 lacune di verifica. Ogni affermazione è marcata [V]/[S]/[I]/[L]; nessuna fonte è ancora verificata sul PDF. Proposta di domanda e assi inviata all'autore per reazione. Non aggiornati `02_MAPPA_CONCETTI.md` e il grafo del second brain (un altro thread lo sta costruendo: non toccato). Rilevato che `04_Fondamenta Matematiche/` contiene solo l'Atlante, non il README con le correzioni citato in precedenza.
- **2026-10-18 (grafo)**: costruito il grafo graphify del second brain, su autorizzazione esplicita dell'autore. Perimetro: le 28 file in `03_Analisi Approfondite/` (27 analisi più l'indice 00), circa 75.600 parole. Esclusi i PDF teorici (294 MB in totale, di cui 115 MB il solo MVRDV HUB) e i materiali MVRDV. Estrazione semantica in due blocchi con subagenti. Risultato: 356 nodi, 371 archi, 34 comunità; 82% EXTRACTED, 17% INFERRED, 1% AMBIGUOUS. Output in `00_Schemi e Mappe/Second_Brain_Analisi_Approfondite/graphify-out/` (`graph.html`, `graph.json`, `GRAPH_REPORT.md`). Gli archi INFERRED e AMBIGUOUS sono inferenze della pipeline, non fatti dei testi: non citarli in tesi. Non ricostruito il grafo sui PDF. Non aggiornati `02_MAPPA_CONCETTI.md` e `00_LEGGIMI_come_aggiornare.md`, che restano al 2026-10-10 e dicono ancora "grafo non costruito".
- **2026-10-18**: audit completo delle cartelle `01_Ricerche Teoriche/` e `02_MVRDV Research/`. Individuati due nuovi PDF privi di scheda analitica: `00_Alexander_Christopher_Notes_on_the_Synthesis_of_Form.pdf` e `00_Design Patterns_Elements of Reusable Object Oriented Software.pdf`. Redatte le analisi dettagliate [26](file:///C:/Users/Caredda%20Dennis/Desktop/TESI/03_Analisi%20Approfondite/26_Alexander_Notes_on_the_Synthesis_of_Form_Riassunto_Dettagliato_Completo.md) e [27](file:///C:/Users/Caredda%20Dennis/Desktop/TESI/03_Analisi%20Approfondite/27_Gamma_Design_Patterns_Elements_of_Reusable_Object_Oriented_Software_Riassunto_Dettagliato_Completo.md) secondo le 10 sezioni delle linee guida (decomposizione HIDECS 2 su IBM 7090, studio di Bawains a 141 variabili, catalogo dei 23 pattern GoF, architettura Lexi, due principi aurei della composizione). Aggiornati `00_Indice_Generale_e_Guida_delle_Analisi.md` e `01_INDICE_BREVE.md` (includono ora le schede 25, 26 e 27). Tutto il materiale sorgente in cartella è ora coperto al 100%.
- **2026-10-11**: aggiunta l'analisi 25 di Andrew Witt, *Architecture, Automata, and Artificial Memory* (`03_Analisi Approfondite/25_Witt_Architecture_Automata_and_Artificial_Memory_Riassunto_Dettagliato_Completo.md`). Il PDF in cartella è l'intero numero 4(1) 2026 di *Khōrein* (tema *Automata*): analizzato il saggio di Witt (pp. 117–139) e letta l'introduzione dell'editoriale di Vanucci (pp. 1–4); gli altri saggi e le interviste non sono stati letti. Segnalati in analisi 25 i punti da verificare: "Gregory XII" (probabile refuso per Gregorio XIII), datazione di Erone, incoerenze bibliografiche (Witt 2004/2024, Grillo/Francesco). Non aggiornati `01_INDICE_BREVE.md`, la mappa e l'indice 00, perché fuori dal perimetro richiesto: da fare se si vuole.
- **2026-10-10**: rilettura integrale del corpo delle 24 analisi e dei file di istruzione (sola lettura). Creata questa cartella. Rigenerato il second brain. Aggiornato `CLAUDE.md`.
- **2026-10-10 (precedente)**: audit della struttura, creazione del second brain in prima versione (basato su indici e chiusure, non sul corpo).

## Prossimi passi

1. Recuperare o ricostruire il report di verifica delle "schede 11–14", oppure confermare che non esiste e chiudere l'avviso.
2. Reperire la fonte di De Carlo (analisi 24) o segnalarla come non verificabile in tesi.
3. Verificare le cifre elencate negli avvisi 3–4 sulle fonti PDF.
4. Redigere il Report fondativo in `02_sintesi/` (cartella da creare) a partire dal second brain.
5. ~~Decidere se costruire il grafo (skill graphify) sul second brain~~: fatto il 2026-10-18 sulle sole analisi (vedi Cronologia). Resta da decidere se estendere il grafo ai PDF teorici, con un costo molto più alto.
6. Aggiornare `02_MAPPA_CONCETTI.md` e `00_LEGGIMI_come_aggiornare.md` con le analisi 25–27 e con la presenza del grafo.
