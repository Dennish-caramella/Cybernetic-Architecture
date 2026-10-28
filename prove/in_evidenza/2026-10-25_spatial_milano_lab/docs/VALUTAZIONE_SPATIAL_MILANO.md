# Valutazione di "Spatial Milano" come base per la tesi

**Data:** 2026-10-26. **Oggetto:** artifact `claude.ai/artifact/GaPJf4tLYL8WZTkokBZkMn` (pagina HTML, 88 NIL di Milano, mappa/globo, dashboard, chat con Claude, vista 3D di lotti ed edifici).
**Marche:** **[S]** verificato leggendo il codice e i dati incorporati nella pagina; **[I]** inferenza mia; **[H]** ipotesi da verificare; **[L]** lacuna.
**Cosa ho fatto e cosa no.** Ho letto il codice della pagina, il prompt di sistema e gli strumenti della chat, e fatto controlli di coerenza interna sui dati incorporati (88 NIL, oltre 40 campi per NIL). **Non ho aperto nessuna delle fonti dichiarate** (MEF, OMI, DUSAF, DBT, catasto, Istat): i valori non sono verificati contro l'origine. **Non ho usato il team di voci**: la valutazione è mia, letta contro `RIFORMULAZIONE_PHD.md` (H1-H9, R1-R9, §12). Nel team mancano proprio le competenze che qui servirebbero (urbanistica, dati), vedi §6.

---

## 1. Verdetto in breve

1. **Come base del contributo della tesi: no.** È un visualizzatore di dati con un oracolo conversazionale. Nessun criterio, peso o catalogo è riscrivibile da chi lo usa; l'unico parametro modificabile è la superficie dell'alloggio (30-130 m²) [S]. Per la definizione operativa del dottorato (H2: partecipativo solo se si modificano i criteri) non è uno strumento partecipativo [I].
2. **Come strato di dati e di interfaccia per la Fase 1: sì, in parte, ed è il suo valore reale.** Colma la lacuna "nessun dato reale" (R6, §8.3 della riformulazione) meglio di `pipeline_milano`, ferma ai file sintetici. Ma l'unità è il NIL (88 quartieri, in media circa 2 km²), non la cella H3 da circa 10 ha della pipeline [S per il NIL; il confronto con H3 dal README della pipeline, S]. Va deciso quale scala vale per lo screening.
3. **Il rischio principale è di posizionamento.** La pagina si presenta come "SPATIAL per il Comune di Milano" [S: saluto della chat] mentre è un prototipo privato. Per la tesi va riformulata come osservatore dichiarato (chi l'ha scritta, con quali fonti, con quali scelte), non come servizio ufficiale.

---

## 2. Che cosa contiene davvero [S]

| Blocco | Contenuto | Fonte dichiarata nella pagina |
|---|---|---|
| Indicatori per NIL | popolazione e variazione 2015-2025, età, cittadinanza, laureati, reddito, affitto OMI, prezzo, verde, calore, metro, uso del suolo | Comune di Milano, Istat 2021, MEF IRPEF 2024 per CAP, OMI 2024 sem. 2, DUSAF 2024, Spotted (calore e verde, luglio 2024) |
| Piano | servizi, ambiti di rigenerazione, aree dismesse, ambiti di trasformazione (PGT) | Regione Lombardia, tavola delle previsioni di piano |
| Edificato | unità volumetriche con altezza reale; particelle catastali con quota coperta | Comune di Milano DBT 2020; Agenzia delle Entrate, particelle INSPIRE |
| Chat | Claude legge i dati tramite sette strumenti (`get_ranking`, `get_nil_profile`, `show_on_map`, `show_buildings`, `set_rent_size`, `get_transformation_areas`, `list_nils`) e aggiorna la mappa | prompt: "non inventare numeri", "se è una stima, dillo", chiusura con riga "Fonte" |
| Modalità demo | se Claude non è disponibile, risposte a parole chiave (regex) | |

Cose fatte bene, in linea con le regole di integrità del progetto [S]: ogni indicatore ha la propria fonte; le stime sono dichiarate come stime (es. "Stima su MEF…" per il netto); il prompt vieta di inventare numeri; c'è un'avvertenza visibile ("L'IA può sbagliare").

---

## 3. Confronto con l'impianto del dottorato

| Voce della riformulazione | Che cosa offre la pagina | Giudizio |
|---|---|---|
| Lacuna "dati reali" (R6, §8.3) | oltre 40 campi per 88 NIL, con fonti | **Colma in parte** |
| Lotti candidati (F1a) | Layer PGT con rigenerazione, aree dismesse, trasformazione; particelle catastali | **Fonte migliore degli OSM `landuse` della pipeline**, che includono aree attive [I; S per la critica OSM nel README]. Manca la proprietà: le particelle INSPIRE non la contengono [I, da verificare] |
| H1-H2 (pesi esposti e riscrivibili) | Nessun peso, nessun punteggio composito | **Non coperto** |
| H5 (catalogo scritto da gruppi diversi) | Catalogo fisso, scritto dall'autore | **Non coperto; è l'obiezione di Alexander** (scheda 26: il catalogo è già la forma) [I] |
| H6-H7 (apprendimento, bias) | Nessuna scelta delle persone registrata | **Non coperto** |
| H8 (sopravvivenza dei lotti alla verifica tecnica) | Fornisce materiale (ambiti, particelle, altezze) per costruire il campione | **Abilita la prova, non la esegue**. Mancano FAR per lotto, vincoli, bonifica |
| R1 (mediazione che diventa decisione) | Vedi §4.3 | **Presente in piccolo** |
| Ponte Fase 1 → Fase 2 | Il passo "Scendi di scala" porta dal quartiere ai lotti e agli edifici in 3D | Ponte **visivo**, non un campo di vincoli leggibile da un sistema di parti (H9) [I] |

---

## 4. Critiche, in ordine di peso

### 4.1 Non è partecipativo, e questo conta più dei dati
Un cittadino può chiedere e guardare. Non può cambiare cosa si misura, come si pesa, che cosa è "buono". Sulla scala di potere del dottorato (scelte, criteri, catalogo) la pagina sta sotto il primo livello. Va detto senza attenuanti, perché il progetto è stato presentato come base per una tesi sulla democratizzazione dei processi [I].

### 4.2 Problemi di dati verificabili dal file [S]
- **Il reddito è per CAP, riportato ai NIL tramite indirizzi OSM** (dichiarato nella fonte del netto). Conseguenze visibili: Parco Sempione, senza residenti, mostra reddito complessivo 77.126 € e affitto 18,95 €/m²; Giardini P.ta Venezia (38 residenti) mostra 80.818 €; Roserio e Stephenson hanno lo stesso reddito (21.348,07), probabilmente perché condividono il CAP [I]. Sono artefatti dell'assegnazione, non misure.
- **Il "netto" è una stima per un solo reddito** (dichiarato). L'indice di incidenza dell'affitto (affitto OMI per la superficie scelta diviso netto) è quindi un'indicazione grossolana, non il carico reale di una famiglia.
- **L'indicatore di basso reddito discrimina poco.** La quota di contribuenti fino a 15.000 € è 32,5% in Duomo e 27,7% a Niguarda [S: dati incorporati]. Come proxy dell'esigenza abitativa è debole: il motivo (CAP, composizione dei dichiaranti) è [H].
- **Epoche miste:** 2015, 2020 (DBT), 2021 (Istat), 2024 (MEF, OMI, DUSAF, Spotted), 2025 (anagrafe). Non è un errore, ma il confronto tra indicatori va datato [S].
- **Unità di analisi:** la media per NIL nasconde la distribuzione. La "pancia" della curva (obiettivo politico del progetto) non è visibile in una media di quartiere [I].
- **Non verificato:** nessun valore è stato controllato contro la fonte. Il controllo di coerenza interna (densità = residenti / superficie) torna su 79 NIL su 87 (uno non ha residenti); sugli 8 restanti non ho indagato la causa [S sul conteggio; causa L].

### 4.3 La chat è un mediatore con potere nascosto
Il prompt dice a Claude di scegliere "dashboard e indicatore più adatti" quando la domanda è generica [S]. Chi chiede "dove si vive bene?" riceve una risposta costruita su un indicatore scelto dal modello, secondo un elenco scritto dall'autore. È in piccolo il rischio R1: la soggettività passa a monte (MVRDV, scheda 22) e l'utente non la vede [I]. Mitigazione possibile: mostrare l'indicatore scelto e perché, e permettere di cambiarlo [H].

### 4.4 Nessuna prova che la chat risponda giusto
Il modello usato è di livello "quick" [S]. Gli strumenti riducono il rischio di numeri inventati, ma non c'è un test: nessuna batteria di domande con risposta nota. Senza di essa, "non inventare numeri" è un'intenzione, non una proprietà [I].

### 4.5 Posizionamento e attribuzione
"Ciao, sono SPATIAL per il Comune di Milano" e il tema grafico "Hub di riferimento" (commento nel CSS) danno l'impressione di un servizio istituzionale [S]. In tesi o in una demo pubblica va tolto il riferimento al Comune e dichiarato che si tratta di un prototipo di ricerca. Verificare anche le licenze delle fonti prima di ripubblicare i dati incorporati (la pagina dichiara CC BY 4.0 solo per il catasto) [L].

---

## 5. Che cosa si può dire e che cosa no

- **Si può dire:** esiste un prototipo che mostra come dati aperti su Milano, con fonte per indicatore, possano stare dietro un'interfaccia conversazionale; costituisce un candidato come strato di osservazione di Fase 1.
- **Non si può dire:** che sia uno strumento partecipativo, che individui le esigenze degli abitanti, che i lotti proposti siano edificabili, che le cifre siano verificate.

---

## 6. Domande che il pezzo apre per la pianificazione

Elenco di materiale per `/supermatt:wayfinder`, **non** un piano. Sono domande, alcune già nella riformulazione (§12).

1. **Scala:** NIL (88, dati già pronti), cella H3 (pipeline) o lotto (catasto)? Cambia il significato di "screening" e di H8.
2. **Che cosa sono la pagina e la pipeline l'una per l'altra:** la pagina come front-end della pipeline, la pipeline sostituita dai dati della pagina, o due tracce separate?
3. **Dov'è il primo atto partecipativo minimo** che si può costruire sopra questi dati senza persone reali (pesi riscrivibili e visibili), così da provare H1-H2 prima dell'etica?
4. **Chi verifica i dati:** serve un tecnico o una fonte primaria per un campione di indicatori e di lotti (H8). Senza questo, tutto il resto poggia su numeri non controllati.
5. **Le voci mancanti:** urbanistica italiana e dati territoriali, scelta sociale, scienze sociali sulla partecipazione. Il team (PR #2 e #3) non le copre, e le otto voci hanno letto le stesse schede (§8.7 della riformulazione).
6. **Persone reali sì o no** (§12.3): determina se il dottorato regge o se l'ambito torna a una magistrale con screening e scenari.
7. **Stato di Abitare Cinisello e dell'atlante di Monza e Brianza** rispetto a questa traccia: un caso locale (Cinisello) o la scala di Milano come caso?

## 7. Nota sulle ipotesi
La versione di `RIFORMULAZIONE_PHD.md` letta qui arriva a H9. H10 (la convergenza del ciclo di feedback non deve dipendere dall'ordine di presentazione né dal seme casuale) sta nel §14 del ramo della PR #4 e non è stata considerata in questa valutazione.
