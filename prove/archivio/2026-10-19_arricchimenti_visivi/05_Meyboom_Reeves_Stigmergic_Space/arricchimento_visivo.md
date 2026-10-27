# Meyboom, A.; Reeves, D. — *Stigmergic Space* — Arricchimento visivo

> **Stato:** arricchimento visivo. Il riassunto completo esistente non è accessibile da questa sessione (sta sul computer dell'autore). Questo file va agganciato alle sue sezioni.
> **Fonte:** `TESI/01_Ricerche Teoriche/05_StigmergicSpace_AnnaLisa Meyboom Dave Reeves.pdf` — 8 pagine PDF, circa 3.700 parole, testo integrale letto.
> **Riferimento come riportato nel PDF:** AnnaLisa Meyboom e Dave Reeves, "Stigmergic Space", ACADIA 2013 *Adaptive Architecture*, pp. 199–203 (paginazione stampata nel PDF). Affiliazione: University of British Columbia. **Da verificare** sul volume degli atti.
> **Avviso dal registro di verifica:** nel registro dei lavori la scheda di questo testo compariva sotto il nome "Bartlett" (vedi `stato_avanzamento`, avviso 2). Il PDF riporta invece la University of British Columbia. Da chiarire prima di citare l'affiliazione.

## Figure e schemi estratti

Il PDF contiene 22 immagini. Ne ho estratte 15, quelle che mostrano il meccanismo e il caso di studio. Le figure 16–21 (risultati, sei gruppi di pianta per scenario) non sono ancora estratte.

Le didascalie nel testo sono numerate ma il loro ordine nel PDF non è sempre lineare: l'associazione tra file e numero di figura è per pagina, quindi **incerta**. I file sono nominati per contenuto.

| File (cartella `figure/`) | Pagina PDF | Cosa mostra (osservazione diretta) | Didascalia / riferimento nel testo |
|---|---|---|---|
| `p01_a_termiti_costruzione.png` | 1 | Tre stadi della costruzione del nido di termiti: il feromone primario della regina, poi il secondario depositato dagli operai. | "Figure 1: Termite nest construction process" |
| `p01_b_vespe_celle_esagonali.png` | 1 | Tre stadi della costruzione delle celle di vespe: una cella aggiunta ha più probabilità di essere costruita se ha più vicini costruiti. | "Figure 2: Wasp nest construction process" |
| `p02_a_tracce_formiche_feromone.png` | 2 | Due formiche che seguono il gradiente di feromone; la traccia si diffonde e decade nel tempo. | "Figure 3: Ant colonies construction process" (testo di p. 2) |
| `p03_a_spazio_feromoni_RGB.png` | 3 | Lo spazio RGB usato come spazio dei feromoni: ogni agente ha un target di colore (un punto nel cubo RGB). | "Figure 4: Color space pheromone targets" |
| `p03_b_algoritmo_due_famiglie.png` | 3 | Algoritmo in corso con due famiglie di agenti (target ciano e magenta) che si spartiscono il volume. | "Figure 5: Algorithm in process where two distinct families of agents negotiate spatial territories" |
| `p03_c_nodi_vicinato_topologia.png` | 3 | Nodi della griglia volumetrica: vicini, topologia e singolo nodo, con gli assi della griglia X, Y, Z. | "Figure 6: Nodes" |
| `p04_a_influenze_esterne_esposizione_contesto_circolazione.png` | 4 | Tre schemi di volumi a nodi: esposizione (luce da un lato), contesto esistente con strada, circolazione verticale come percorso scuro. | "Nodes become pheromone sources" (probabile): sorgenti come influenze esterne |
| `p04_b_griglia_risultati_sei_opzioni.png` | 4 | Sei piccole piante, due righe da tre: risultati alternativi dello stesso scenario, con condizioni iniziali diverse. | Testo di p. 4–5 (sezione 5, scenari, opzioni per seed) |
| `p04_c_topografia_partizione_volumi.png` | 4 | Tre passi: topografia (piano inclinato con volumi a gradini), partizione e volumi finali. | Testo di p. 4 (masking della topografia) |
| `p04_d_diffusione_feromone_t1_t3.png` | 4 | Diffusione del feromone su una pianta in tre istanti (t1, t2, t3) da tre sorgenti con valori RGB. | "Nodes become pheromone sources" (probabile); meccanismo di diffusione della sezione 3.2 |
| `p05_a_sequenza_masse_programmi.png` | 5 | Sequenza di masse verticali per i programmi, con una piccola pianta di riferimento. | Testo di p. 5 (sezione 5), didascalia non certa |
| `p05_b_tabella_valori_feromone_programmi.png` | 5 | Tabella dei valori di feromone per tipo di programma: lounge, aule, laboratorio, aula magna, biblioteca, uffici, residenza, servizi. | "Pheromone values for programs with agent's desired number of nodes" |
| `p06_a_scenario_masking_sorgenti_perimetro.png` | 6 | Scenario A: masking della topografia e sorgenti sul perimetro per l'esposizione alla luce. | "External influences for scenario A representing exposure to light" |
| `p06_b_scenario_masking_sorgenti_facce_opposte.png` | 6 | Scenario B: masking con due tipi di sorgenti su facce opposte, gradiente pubblico-privato. | Testo di p. 6 (scenario B) |
| `p06_c_scenario_atrio_mascherato.png` | 6 | Scenario C: atrio o circolazione mascherati, con due tipi di sorgenti sulle facce opposte. | Testo di p. 6 (scenario C) |

**Nota per la tesi:** i diagrammi di p. 1–2 sono illustrazioni di biologia (termiti, vespe, formiche) di fonti citate nel testo. Per l'uso in tesi serve la fonte originale (Camazine et al. 2001; Grassé 1954; Bonabeau 1999, tutte da verificare) e, dove è riprodotto, il permesso.

## Schema 1 — il meccanismo stigmergico del software (testo, p. 2–4)

```
  AGENTI (programma: es. aula, laboratorio, uffici)
     |  target di feromone = colore RGB (es. ciano vs magenta)
     v
  NODI (griglia volumetrica discreta, ogni nodo: occupato/libero + valore di feromone)
     |  diffusione: ogni nodo fa la media con i vicini
     v
  ESPANSIONE: l'agente occupa il nodo libero con il feromone più vicino al suo target
     |  CONTRAZIONE: se ha troppi nodi, rilascia quello con deviazione maggiore
     v
  SORGENTI: nodi con valore fisso (es. luce dal perimetro, pubblico/privato)
     |  MASKING: nodi rimossi (topografia, atrio) che non partecipano alla diffusione
     v
  ADIACENZE EMERGENTI: agenti compatibili si raggruppano; l'esito non è progettato in dettaglio
```

**Lettura (inferenza mia):** la progettazione non è la disposizione dei programmi, ma la definizione delle regole (target, sorgenti, masking) e la valutazione dei risultati. Il testo lo dice esplicitamente: il progettista "tunes the distributed decision-making routines" dopo ogni run (p. 5). È il punto più utile per la tesi: l'architetto come progettista di regole, con un ciclo di feedback.

## Schema 2 — il ciclo di progetto e di valutazione (testo, p. 5)

```
  brief (programma, complessità calibrata)
     |
     v
  scenari (A: luce; B: pubblico-privato; C: atrio mascherato)
     |
     v
  8 opzioni per scenario (condizioni iniziali diverse)
     |
     v
  scelta dell'opzione più dominante -> analisi delle adiacenze
     |
     v
  regolazione delle regole (feedback) -> nuovo run
```

Il testo avverte che "success or failure can only be assessed by letting the system play out ecologically" (p. 5). La valutazione è quindi empirica e dipende dal seed.

## Passaggi citabili con pagina (per la scheda)

- Definizione: lo spazio è il "emergent product of a competitive ecology" (abstract, p. 1), e il compito di pianificazione spaziale, di solito di un "singular high-level decision-maker (the architect)", è affrontato "through the distributed decision-making of low-level collective intelligence" (abstract). Parafrasi consigliata.
- Architetto come progettista di regole: "This investigation has the architect designing the rules of the ecology of the system and allowing the agents within the system to play out the scenarios" (p. 1). Citazione breve utile.
- Limite dichiarato: "These examples are only a single run based on a single seed condition, so many more variations have been observed" (p. 6). Da segnalare come limite del metodo.

## Limiti, assunzioni e bias

- **Valutazione:** il caso di studio è un programma ipotetico per una residenza studentesca al Santa Fe Institute. Il testo non valuta i risultati con criteri esterni (costi, qualità, soddisfazione di chi usa lo spazio). Le "adiacenze soddisfatte" sono l'unico criterio.
- **Dipendenza dal seed:** il testo ammette che un solo seed non basta. La ripetibilità dei risultati non è dimostrata.
- **Visual feedback:** il testo afferma che il sistema "relies heavily on visual feedback" per valutare le configurazioni. Il giudizio resta al progettista.
- **Utente assente:** l'agente non rappresenta persone, ma programmi. Nessun utente finale partecipa alle regole. Per la tesi questo è il limite più importante: il sistema è partecipativo solo per il progettista.
- **Lessico:** il testo usa "SSAS" e "SASS" (typo nel PDF) per lo stesso software. Da uniformare in tesi.
- **Affiliazione e fonti:** i riferimenti biologici (Grassé 1954, Bonabeau 1999, Camazine et al. 2001) sono nel testo; da verificare prima della bibliografia.

## Collegamenti per la sintesi

- Con Alexander, *Systems Generating Systems* (1968): generare forme attraverso regole locali e interazioni, senza un controllo centrale. Qui le regole sono esplicite; in Alexander l'idea è più generale.
- Con Pask (1969): la regolazione dopo ogni run è un ciclo di feedback cibernetico, con il progettista come controllore.
- Con Sanchez, *Combinatorial Design*: le unità discrete e il pattern emergente qui sono agenti e nodi, non parti e connessioni.
- Con la tesi: il sistema è un esempio di collective intelligence senza partecipazione umana diretta: utile come contro-esempio di "democratizzazione" e come modello di come le regole possono incorporare vincoli di più attori (es. pubblico/privato).
