# Abitare Cinisello: tavola rotonda sulla specifica "v0.3"

**Data:** 2026-10-25. **Stato:** valutazione critica, nessun file HTML modificato.
**Marche:** **[S:NN]** riportato dalla scheda NN del corpus (le schede sono riassunti, non testi primari); **[C]** letto nel codice o nei dati del prototipo; **[I]** inferenza; **[H]** ipotesi da verificare; **[L]** lacuna o fonte non verificata; **[F]** conoscenza fuori corpus, non riaperta sul testo primario in questa sessione: da verificare prima di citare.
Le voci simulano competenze costruite dalle schede, non gli autori reali. Idee e scrittura finale restano di Dennis.

---

## 0. In breve

1. **La specifica è più vecchia del file.** `Abitare-Cinisello-prototipo.html` è già la **v0.4.0** («Laboratorio di ricerca»), non la v0.2. La v0.2 è nel backup. La v0.4 implementa già le sei sezioni, ma corregge quasi tutti i punti che le otto voci criticano: niente PCA/K-Means, niente −2,0 °C, niente entropia del consenso, niente attribuzioni a Pask o Southwark nell'interfaccia, dati dichiarati «di scenario». **Applicare la specifica alla lettera farebbe regredire il file.** [C]
2. **Da mantenere:** architettura client-side in un solo HTML, 4 criteri con pesi in vista, toggle somma pesata / Chebyshev, veti attivabili, sensibilità, MES come regola dichiarata, feedback come *proposta* di pesi prima dell'applicazione, contratto come brief esplorativo con verifiche aperte, trasparenza Misurato / Modellato / Assunto.
3. **Da scartare:** «−2,0 °C» e la «Dote Rigenerativa» calcolata da esso; PCA/K-Means su «cittadini iscritti»; «ente terzo che raccoglie le esigenze reali»; «Entropia del Consenso che scende»; «Multiplicative Weights *di Pask*»; «Goal-Conditioned RL» e «numero esatto di voxel»; il riferimento al Southwark Atlas (non verificato); le «barre di confidenza»; la promessa «<50 ms».
4. **Da modificare:** il nome «Misfit» (Alexander usa variabili binarie su un grafo, non indici 0-100); «Chebyshev raccomandata»; il bonus di sinergia; il feedback (testo libero, parametri esposti, ricostruzione dei motivi); il contratto (campo di vincoli duri/deboli con intervalli, non risultato esatto).
5. **Il buco vero non è nel codice ma nel processo.** Restano aperti i cinque nodi: regola di aggregazione, potere sui criteri, catalogo modificabile, personas prima del pilota, incentivo a gonfiare le esigenze (§5). Nella v0.4 l'abitante può spostare pesi e scegliere lotti, ma criteri, soglie, catalogo dei commons, personas e perfino i 18 immobili sono scritti dall'autore. Alla riformulazione PhD questo si chiama cooptazione (H2).

---

## 1. Che cosa ho trovato nei file locali

| File | Versione | Contenuto |
|---|---|---|
| `Abitare-Cinisello-prototipo-v02-backup.html` | v0.2 «Laboratorio civico» | un'unica vista live: preset di domanda, slider di budget e tempo di accesso, quattro pesi 0-10, soglie come veto, mappa che si ricalibra, campo «Aggiungi un bisogno non rappresentato» (non cambiava i punteggi), 6 immobili con indicatori «dimostrativi» su 18 |
| `Abitare-Cinisello-prototipo.html` | **v0.4.0** | 6 pagine + metodo: territorio e prove, domanda e commons (MES), confronto (WSM/Chebyshev, veti, sensibilità), valutazioni e dissenso, contratto di ricerca (JSON), studio spaziale (celle 6×6 m); 2,7 MB, quasi tutto geometrie PGT |
| `Abitare-Cinisello-protocollo-di-ricerca.md` | v0.4 | domande, H1-H3 del laboratorio, piano di validazione, minacce alla validità; dichiara 15 test automatici (`verify-research.cjs`, **non presente nella cartella**, quindi non verificato da me) |

Fatti verificati nel file v0.4 [C]:
- **Dati documentati:** 18 immobili dismessi dalla ricognizione comunale CC 51/2020 (identità catastale e grado di degrado) e 1.772 geometrie del PGT storico 2018. Posizioni da geocodifica di indirizzo. Zero perimetri verificati, zero fattibilità accertate, zero vuoti urbani validati.
- **Dati di scenario:** `f` 0-100 sui 4 criteri, `rentEstimate`, `rentIncomeRatio`, `overcrowding`, `vulnerability`, `tplMinutes`, `lstDelta` (3,2-4,2 °C nei lotti che ho letto), `soilSealingPct`, `minGreenPct`, `treesRequired`, `cleanupCostM2`. Ereditati dal dimostratore v0.3, **senza fonte puntuale**. Non si vede come `f` derivi da `x` (lotto 2: soc x=76, f=62; prox x=68, f=65): sono messi a mano. `tau` non è usato da nessuna riga di codice.
- **Non «non-speculativi».** La specifica parla di «lotti non-speculativi (aree pubbliche, ex-industriali)». I 18 immobili sono dismessi di proprietà in gran parte privata o mista (es. «Privata dismessa», «Immobile privato da rigenerare», «Ex-deposito privato con istanza di recupero»); uno solo è «Adiacente a comparto pubblico ALER». La proprietà non è accertata per nessuno. «Non speculativo» non è un attributo dei dati.
- **Quartieri.** I distretti nei dati sono: Crocetta, Campo dei Fiori, Robecco, Robecco / Bettola, Borgomisto, Cornaggia, Bellaria, Centro, Sant'Eusebio (con varianti Nord/Ovest). L'elenco della specifica coincide quasi del tutto; non ho verificato i confini dei quartieri [L].
- **«100% client-side» non significa offline.** Font da Google Fonts e immagini aeree richiedono Internet (lo dice il LEGGIMI). Il calcolo è locale, il file no.
- **Persa rispetto alla v0.2:** il campo «Aggiungi un bisogno non rappresentato». Nella v0.4 il catalogo dei criteri non si può nemmeno proporre di cambiare.

---

## 2. Come ho condotto la tavola rotonda (e i suoi limiti)

Otto voci in parallelo, ciascuna con il solo dossier del nodo (stato reale del prototipo, specifica, riformulazione PhD): `alexander-sistemi`, `pask-cibernetica`, `decarlo-mari-partecipazione`, `mvrdv-negoziazione`, `azadi-pianificazione-aumentata`, `ingegnere-edile`, `carpo-sanchez-discreto`, `aadrl-bartlett-agenti`.

Limiti, da leggere prima dei verdetti:
- **Un solo round.** Le voci hanno rivolto domande ad altre voci; non ho fatto il round 2. Le domande aperte sono in §6.
- **Revisore non indipendente.** Il controllo di integrità del §4 lo ha fatto l'orchestratore, non la voce `revisore-integrita`. Va ripetuto da una voce che non abbia scritto il documento.
- **Convergenza circolare.** Le voci hanno letto lo stesso dossier, che conteneva già le mie osservazioni su −2,0 °C, Alexander e Southwark. Il fatto che «tutte e otto» le ripetano è in parte effetto del dossier, non prova indipendente. Hanno aggiunto contenuto proprio su: grafo e semireticolo (Alexander), rapporto con il processo decisionale (Azadi), conformismo e recupero parametri (AADRL), costo della partecipazione (De Carlo), alfabeto delle parti (Carpo-Sanchez), cosa un contratto può promettere (ingegnere).
- **Copertura delle schede parziale.** Più voci dichiarano di aver letto solo parte delle schede; nessuna voce di scelta sociale, dati o urbanistica esiste nel team.
- **Mancano gli utenti.** Nessun abitante, nessun tecnico del Comune.

---

## 3. Verdetto per sezione

Legenda: **M** mantenere, **MOD** modificare, **S** scartare.

### Premessa: identità visiva, sidebar, architettura

| Elemento | Verdetto | Motivo |
|---|---|---|
| Identità visiva, `aside/header/main/footer`, palette, principio «Prima il lotto. Poi la scelta. Identità catastale, fattibilità e bisogni devono restare distinguibili.» | **M** | È già nella v0.4. Il principio è la spina dorsale epistemica del prototipo. |
| Zero-backend, calcolo nel browser | **M** | Tutte le voci. Va detto che font e immagini aeree richiedono rete [C]. |
| «<50 ms … nello stile del Southwark Retrofit Atlas di Arpan Bakshi» | **S (il riferimento), MOD (la promessa)** | **Southwark Retrofit Atlas / Bakshi: non verificato.** Due ricerche web non hanno trovato nulla [L]; non è dimostrato che sia falso, ma non entra nell'interfaccia né come garanzia. Il tempo di calcolo è plausibile (18 lotti × 4 criteri [I]) ma va misurato e riportato come quantile su un dispositivo dichiarato, non promesso (il protocollo v0.4 lo dice già). Il tempo di calcolo non misura la validità. |
| Backup della v0.2 | **M** | Già fatto. |

### Sezione 1: Il territorio e i «Misfit»

| Elemento | Verdetto | Motivo |
|---|---|---|
| Quartieri e catalogo lotti | **M, MOD** | Mantenere come contesto. Togliere «non-speculativi» e «aree pubbliche»: i dati non lo dicono (§1). Aggiungere «proprietà: da acquisire» come campo di stato. |
| Quattro sottosistemi con `x_k∈[0,100]` e soglia `τ_k`, chiamati «Misfit» di Alexander | **MOD (nome e statuto)** | In Alexander le variabili di misfit sono **binarie** (0 = fit, 1 = misfit) e collegate da un grafo G=(M,L) di interazioni, decomposto per minima interazione [S:26]. Indici continui 0-100 non sono misfit. Due strade oneste: (a) chiamarli «criteri di scenario» e basta; (b) binarizzarli davvero (soglia con autore dichiarato) e costruire un grafo piccolo ma esplicito (4 nodi, archi motivati). Alexander (voce): i quattro sottosistemi indipendenti e additivi sono essi stessi un *albero* [S:04]; l'interazione tra clima, bonifica e fattibilità è ignorata. |
| Dati OMI/IRPEF/ISTAT/LST come input dei lotti | **S (come dati dichiarati)** | Nessun valore per i 18 lotti ha una fonte puntuale nel file. Riammettere solo come campo con fonte, data e livello di elaborazione. OMI sono intervalli stimati, non transazioni [S:37 via riformulazione]; il reddito alla scala di sezione potrebbe non esistere [riformulazione §8.3]. LST e temperatura dell'aria sono grandezze diverse [I, ingegnere]; il legame non è nel corpus [L]. |
| Regola critica: «Dote Rigenerativa» = verde minimo e alberature come funzione diretta dell'anomalia termica, «per abbattere la temperatura locale di −2,0 °C» | **S** | Nessuna fonte, nessun modello, nessun lotto misurato (voci: ingegnere, MVRDV, Alexander, AADRL, Carpo-Sanchez, Azadi). Una funzione a un solo ingresso (ΔLST) non è difendibile: anche modelli con coefficienti dichiarati restano scatole nere semplificate [S:23]. La v0.4 lascia `coolingDeltaC: null`, correttamente. **Come rimpiazzo:** «requisito di programma dichiarato», cioè verde minimo come soglia scelta dall'architetto o dal PGT, con fonte e autore, etichettata *Assunto*; il raffrescamento resta una *verifica da fare* (confronto LST/temperatura dell'aria su un lotto misurato), non un risultato. |
| «Basamento aperto al quartiere» = funzioni mancanti a 15 minuti | **M, MOD** | L'idea è utile e coerente con il contratto. Le `missing15m` oggi sono di scenario: mostrarle come tali. |

### Sezione 2: «Ente terzo» e Commons

| Elemento | Verdetto | Motivo |
|---|---|---|
| «Ente terzo» che «raccoglie le esigenze reali» | **S** | Già da abbandonare nella riformulazione (§2). In termini di Pask non esiste un osservatore esterno neutro [S:02]; per De Carlo è il demiurgo che torna. Usare «modello di mediazione con osservatore dichiarato». «Pask & Sanchez» come fonte dell'ente terzo non compare nelle schede [L]. |
| Cluster estratti con PCA + K-Means/GMM sui «cittadini iscritti» | **S** | **Non esistono iscritti.** I cluster A/B/C sono tre personas scritte dall'autore, e nel codice ogni progetto ha il campo `clusters` che pre-assegna le approvazioni [C]. Presentarli come «estratti» sarebbe un dato inventato presentato come reale. Anche con dati veri, K=3 deciso a monte e un campione auto-selezionato non sosterrebbero un clustering (H7). |
| Tre categorie A giovani, B famiglie, C anziani autosufficienti | **MOD** | Sono un «Uomo Tipo» per fasce [S:24]. Mancano: anziani non autosufficienti, migranti, chi è in emergenza abitativa, chi non si iscrive online, chi già abita nel patrimonio degradato [L, De Carlo]. Aggiungere almeno una persona avversaria e una «non rappresentata»; consentire appartenenze sovrapposte (semireticolo, non partizione) [S:04]. |
| Method of Equal Shares | **M, MOD (claim)** | Mantenere come **regola dichiarata**. Verificato sull'abstract: Peters, Pierczyński e Skowron, *Proportional Participatory Budgeting with Additive Utilities*, arXiv 2008.13276: MES soddisfa EJR per costi arbitrari e utilità di tipo approvazione, e una garanzia «up to one project» per utilità additive arbitrarie; è calcolabile in tempo polinomiale. **Non riaperto il testo integrale.** Quindi: la frase «garantendo proporzionalità matematica» vale per la regola e per il modello di voto, **non** per la rappresentatività di chi vota; con elettori virtuali da 3 personas, dove tutti i votanti di un gruppo sono identici e le approvazioni sono pre-assegnate dal catalogo, il risultato è circolare e non prova nulla. Rinominare «votanti virtuali» e dichiarare costi in punti e superfici come assunzioni. |
| Commons come «servizi finanziati» (9 progetti) | **MOD** | In Koehler/Sanchez il bene comune è una condizione di proprietà e di regola, non una voce di costo [S:18, S:11; resa in [I]]. Va nominato chi gestisce ogni spazio e a quali condizioni (oggi assente). Il catalogo deve poter ricevere proposte degli abitanti (livello «catalogo aperto» della riformulazione §10). |

### Sezione 3: Prioritise e scelta del lotto

| Elemento | Verdetto | Motivo |
|---|---|---|
| Pesi, budget, soglie di veto, classifica e grafici reattivi | **M** | È il nucleo difendibile (MVRDV, H1). |
| Toggle WSM vs Chebyshev aumentata | **M** | Due letture affiancate. |
| «Chebyshev … non-compensativa, **raccomandata**» | **MOD** | «Raccomandata» è una scelta politica presentata come neutra (Azadi, De Carlo, Alexander, MVRDV). Mostrare le due letture senza default raccomandato. Dettagli tecnici in §4. |
| «Rank Reversal» | **MOD (nome)** | Mostrare la divergenza di ranking tra i due metodi: utile. Il termine «rank reversal» in letteratura indica di norma un cambio d'ordine quando si aggiungono o tolgono alternative [F]; qui non è il caso. Chiamarlo «divergenza tra metodi» e legarlo alla sensibilità, senza probabilità. Una divergenza ha poco significato finché `f` non ha fonte. |
| Soglie di veto | **M, MOD** | Non compensative per costruzione. Oggi solo su canone e tempo di accesso e solo se attivate, e `tau` non è usato. Ogni veto riporta autore e origine (livello 1 della riformulazione §10, a carico del progettista); un veto senza spiegazione è un potere nascosto. |
| Bonus di Sinergia Civica | **MOD** | 15 punti sono una costante arbitraria che sposta il ranking [C]. Nel codice il bonus è `15·(coperte)/(mancanti)`: un lotto senza funzioni mancanti prende 0, un lotto con molte funzioni mancanti coperte dai commons prende fino a +15. Premia il deficit, in parte annulla la penalità già contenuta in `f_prox`, ed è contabilità doppia con i commons già votati [H]. Mostrarlo separato dal punteggio base, sempre opzionale (già così), oppure scartarlo. |
| Aggregazione tra più persone | **assente: da progettare** | La classifica usa un solo vettore di pesi. Sezione 2 aggrega con MES, sezione 3 no. Vedi §5. |

### Sezione 4: Il loop conversazionale

| Elemento | Verdetto | Motivo |
|---|---|---|
| Pulsanti «Rifiuta questo lotto: …» | **M, MOD** | Il feedback con motivo corrisponde ai «continui anelli di retroazione» [S:24]. Ma il menu è chiuso (tre motivi dati dall'alto): aggiungere un campo libero, codificato da persone e non usato come etichetta di addestramento (riformulazione F1c). |
| Regola `w ← w·exp(η(f(B)−f(A)))/Z` | **M, MOD (statuto)** | Il segno è corretto (si aumentano i pesi dei criteri su cui l'alternativa preferita è migliore). È un aggiornamento esponenziale/moltiplicativo dei pesi, di tradizione *online learning* (Littlestone-Warmuth, Freund-Schapire, Arora-Hazan-Kale) [F: da verificare sui testi primari]. **Non è di Pask**: la scheda 02 non lo riporta; il richiamo a Pask regge solo su SAKI, la macchina che adatta la sfida all'allievo [S:02]. Nella v0.4 η=0,45/25 e il fattore 1,35 sul motivo sono convenzioni [C]: esporli come parametri editabili. Difetto di attribuzione dei motivi: l'aggiornamento tocca tutti e quattro i criteri, anche quelli non citati dal motivo; il «rifiuto per canone» aumenta anche il peso di criteri su cui B è migliore per caso. Meglio chiedere un confronto per criterio, o mostrare la proposta criterio per criterio. |
| Aggiornare automaticamente gli slider | **MOD** | Solo come *proposta* mostrata prima dell'applicazione (già così nella v0.4): i pesi appresi meno visibili dei dichiarati contraddicono H2 (riformulazione §6 F1d, R2). Mantenere un registro delle versioni. |
| «Entropia del Consenso H_comm che scende man mano che la scelta converge» | **S** | (1) L'entropia dei pesi di *una persona* cala per costruzione quando si ripete un aggiornamento moltiplicativo («rich-get-richer»): non misura accordo [I]. (2) Il consenso richiede più persone, qui non ci sono. (3) Premia la convergenza e nasconde le minoranze (MVRDV, De Carlo, AADRL); De Carlo accetta il conflitto [S:24]. (4) È il rischio «convergenza indotta, non consenso» della riformulazione §14. La v0.4 l'ha già tolta. Rimpiazzo: **dispersione** delle scelte per persona/gruppo, e una soglia minima sui pesi per evitare il collasso. |
| «Conversazione Cibernetica» | **MOD (nome)** | Per Pask la conversazione richiede che il sistema modifichi anche le proprie regole, non solo i pesi [S:02]; oggi è un feedback unilaterale. Si guadagna il nome solo con almeno una di queste tre cose [I]: il sistema motiva il ranking e l'utente può contestare la motivazione; l'utente può aggiungere o modificare criteri e catalogo; esiste una traccia di che cosa è cambiato dopo la contestazione. |
| Log History | **M** | Utile; è la traccia di audit. |

### Sezione 5: Contratto parametrico e ponte architettonico

| Elemento | Verdetto | Motivo |
|---|---|---|
| Contratto JSON Fase 1 → Fase 2 | **M, MOD** | La v0.4 ha già l'impostazione giusta: scopo `exploratory_design_brief_not_authorization`, quattro cancelli `pending` (geometria, disponibilità, disciplina urbanistica, ambiente), `coolingDeltaC`, `legalCompliance`, `communityConsensus`, `rlPolicy` = `null`. |
| Struttura del contratto | **MOD** | Distinguere **vincoli duri** (SLP massima, altezza, quota libera: soglie dell'architetto/ingegnere, con fonte e autore), **vincoli deboli negoziabili** e **parti pubbliche obbligatorie**. SLP e PGT come intervalli o massimi con fonte (PGT 2018 storico), non valori calcolati. È il «campo di vincoli per lotto» che Carpo-Sanchez ritiene l'unico ponte plausibile (riformulazione §8.4; il *Field* come vincolo è in [S:17], ma Erioli non tratta lotti). |
| «Numero esatto di voxel/moduli per tagli di alloggio» | **S** | Falsa precisione: nessuna evidenza che un Assembler lo consumi; lo spazio delle soluzioni non ha un optimum [S:09]. Nel (w)Ego/OptiMixer il «numero esatto di unità» è un input scelto dal progettista [S:22], non un risultato dedotto da bisogni e clima. Se serve, intervalli. |
| «Goal-Conditioned RL», «Assembler + RL», pulsante «per Assembler/RL» | **S (come requisito)** | Nel prototipo non c'è RL e non esiste policy addestrata (`rlPolicy = null`) [C]. Le schede mostrano RL solo come PPO su un gioco con reward scritte da umani [S:29] o con VLM per evitare reward a mano [S:33]. Il pulsante diventa «Esporta brief (.json)», e RL resta ipotesi H9 (esplorativa, Fase 2 separata). |
| Preview «Matrice Discreta dei Moduli (Kit-of-Parts)» | **MOD** | Lo studio spaziale v0.4 (celle 6×6 m) è un generatore di ingombri, non un kit di parti con regole di combinazione. Chiamarlo «studio di ingombro»; dichiarare 6 m, 20% distribuzione e 72 m²/alloggio come convenzioni [C, protocollo]. Chi decide l'alfabeto delle parti? Un kit calato dall'alto è partizione travestita [S:18]. |
| Cosa il contratto **non può** promettere | **M (da elencare)** | Raffrescamento, conformità normativa, consenso, fattibilità, costi. Aggiungere un elenco esplicito «non verificato»: struttura, impianti, acustica, antincendio, esodo, catasto 3D, i vuoti che (w)Ego segnala proprio come critici [S:20]. |

### Sezione 6: Metodo e trasparenza epistemica

| Elemento | Verdetto | Motivo |
|---|---|---|
| Distinzione Misurato / Modellato / Assunto | **M, rafforzare** | Tutte le voci: è la sezione più solida. Oggi quasi tutto è «Assunto», e va mostrato così. La v0.4 usa quattro stati: Documentato storico, Indicativo, Scenario, Da acquisire. |
| «Barre di confidenza» | **S** | Una barra suggerisce un intervallo statistico che non esiste (Azadi). Etichette discrete, più due colonne nuove: **«Chi l'ha deciso»** e **«Chi può cambiarlo»** (De Carlo). |
| «Come nel Southwark Atlas» | **S** | Non verificato [L]. |
| «Formule attive: Alexander G(M,L), Chebyshev, MES, Multiplicative Weights di Pask» | **MOD** | Mostrare solo ciò che il codice calcola davvero: WSM, Chebyshev, MES, aggiornamento dei pesi. G(M,L) è un grafo, non una formula, e non è nel codice [C]. Pask non va attribuito all'aggiornamento. |
| Identità / fattibilità / bisogni distinti | **M** | Principio cardine. |

### Requisiti tecnici

| Elemento | Verdetto |
|---|---|
| Un solo `.html`, modulare, commentato | **M** |
| Ogni modifica aggiorna KPI, grafici, mappa e JSON | **M**, con regola: non mostrare KPI che suggeriscano misure inesistenti |
| «In tempo reale <50 ms» | **MOD** (misurare e riportare) |
| Backup della v0.2 | già fatto |

---

## 4. Verifica di formule e fonti citate

| Voce | Esito | Dettaglio |
|---|---|---|
| **Chebyshev aumentata** | formulazione plausibile, **da usare con dichiarazioni** | Struttura: `100 − [max_k w_k(100−f_k) + ρ·Σ_k w_k(100−f_k)]`. Il punto ideale è fisso a 100 per ogni criterio (non l'ideale osservato nei 18 lotti) e ρ=0,05 è convenzionale [C]. I punteggi dei due metodi non sono sulla stessa scala (con pesi 0,25 e `f`=60, WSM = 60, Chebyshev ≈ 88): si confrontano solo gli ordini. Con pesi normalizzati a somma 1, un criterio con peso piccolo raramente è quello che fa da massimo: i pesi agiscono come tolleranze, non come tassi di scambio. «Non-compensativa» è imprecisa: con ρ>0 e per i criteri non-massimo il metodo compensa in misura ridotta; la non compensazione piena è dei veti. Il testo primario non è stato riaperto [F]. |
| **Method of Equal Shares / EJR** | **verificata sull'abstract** | Peters, Pierczyński, Skowron, arXiv 2008.13276 (abstract letto): EJR per costi arbitrari e utilità di approvazione; «up to one project» per utilità additive arbitrarie. Implementazione nel file: costi come utilità, parità per costo minore poi id, nessun completamento del budget [C]. Testo integrale non letto. |
| **Multiplicative Weights «di Pask»** | **attribuzione non sostenuta** | Non compare nella scheda 02 [S:02]. Famiglia di algoritmi di online learning di altra tradizione [F]. L'algoritmo si può usare, l'attribuzione a Pask no. |
| **Alexander, G(M,L)** | **mal rappresentato** | Variabili binarie su un grafo non orientato di interazioni [S:26, Atlante]. Non sono indici 0-100 con soglia. Nel codice non c'è alcun grafo [C]. |
| **Southwark Retrofit Atlas, Arpan Bakshi** | **non verificato [L]** | Due ricerche web senza esito. Può esistere con un altro titolo o autore; da chiedere a chi ha scritto la specifica (Dennis o lo strumento che l'ha generata). Fino ad allora: nessuna attribuzione, nessuna «garanzia». |
| **OMI, ISTAT, IRPEF, LST** | **nessuna fonte per i lotti** | Valori «del dimostratore» [C]. OMI = intervalli stimati [S:37 via riformulazione]. LST ≠ temperatura dell'aria [I]. |
| **−2,0 °C** | **senza fonte** | Nessun modello, nessuna misura, nessun lotto. È un obiettivo scelto, non una conseguenza calcolabile. |
| **PCA/K-Means su cittadini iscritti** | **dato inventato presentato come reale** | I «cittadini iscritti» non esistono; i cluster sono tre personas. |
| **Entropia del Consenso** | **concetto non fondato** | Vedi §3.4. |
| **Test del protocollo (15 verifiche)** | **non verificabile qui** | Il file `verify-research.cjs` non è nella cartella; dichiarazione del protocollo, non verificata. |

**Falsa precisione, elenco:** −2,0 °C; `lstDelta` 3,6 / 4,2 °C; `rentEstimate`; `tplMinutes`; `soilSealingPct`; `x` e `f` con `τ` mai usato; «<50 ms»; «numero esatto di voxel»; bonus ×15; η=0,45 e fattore 1,35; «EJR garantita»; «barre di confidenza»; 100 elettori virtuali come «partecipazione»; 72 m²/alloggio e 20% di distribuzione; punteggi con decimali che non corrispondono a nessuna misura.

---

## 5. I cinque nodi aperti

**5.1 Regola di aggregazione (scelta sociale).** È il buco più grosso: la classifica usa un solo vettore di pesi (una persona al mouse), MES aggrega solo i commons, e il corpus non contiene scelta sociale [L; MVRDV, Pask]. Media, mediana e maximin danno graduatorie diverse. **Proposta [H]:** mostrare *affiancate* la graduatoria per persona/gruppo, la media, il maximin e i lotti Pareto-non dominati rispetto ai gruppi, senza default; fissare in F0 la regola di arresto e di aggregazione prima di costruire altro (riformulazione §14).

**5.2 Potere sui criteri.** Nella v0.4 l'abitante può spostare i pesi e attivare i veti. Non può cambiare il catalogo dei criteri, le soglie, le personas, i 9 commons né i 18 immobili. È potere sulle scelte, non sui criteri (H2). **Proposta:** adottare i tre livelli della riformulazione §10 e renderli visibili e distinti: (1) soglie minime tecniche dichiarate dal progettista e verificate dall'ingegnere, non negoziabili e con autore; (2) criteri e pesi riscrivibili; (3) catalogo aperto a proposte. L'architetto-system designer risponde del livello 1 e rende contestabili gli altri.

**5.3 Catalogo modificabile.** La v0.2 aveva un campo «Aggiungi un bisogno non rappresentato», senza effetto sui punteggi; la v0.4 l'ha perso. **Proposta minima [H]:** un quinto criterio proposto dall'utente, con punteggi ordinali 1-5 *scritti dall'utente per ciascun lotto*, incluso nel suo ranking personale; ogni proposta registrata con autore e data. Misura di H5: quanto cambia il top-N quando il catalogo cambia.

**5.4 Personas prima del pilota.** Giusto l'ordine della riformulazione (stadio A prima di B). Ma le personas attuali sono circolari: l'approvazione di un progetto è pre-assegnata per cluster, quindi il MES ritrova le personas per costruzione. **Proposta [H, AADRL]:** *parameter recovery* con votanti simulati con pesi noti, generati indipendentemente dal catalogo, con rumore e almeno una persona in malafede; verificare l'errore di recupero e il numero di turni, con la soglia fissata *prima* (come H6, che oggi non è operativa). Personas generate da un LLM sono scenario, non evidenza [riformulazione §14].

**5.5 Incentivo a gonfiare le esigenze.** Tre piani diversi:
- *Pesi:* sono già normalizzati a somma 1 [C], quindi dichiarare tutto «alto» non produce nulla; gonfiare un criterio ne riduce altri. Il vincolo di budget sui pesi c'è già.
- *Veti e soglie:* nessuno costa nulla; chi abilita un veto per escludere un lotto non paga niente [De Carlo]. Mitigazione da progettare: veto con motivazione registrata e limite al numero.
- *Approvazioni dei commons (MES):* nessuna garanzia di non manipolabilità. In generale nessuna regola di voto non dittatoriale con almeno tre alternative è immune da manipolazione (Gibbard-Satterthwaite) [F]; MES ha altre garanzie di proporzionalità, non questa. Va testato in simulazione, con una persona strategica [H].
- *Il vero incentivo è l'uso dell'output.* Se «dichiarare un bisogno forte» desse accesso prioritario a un alloggio, gonfiare diventerebbe razionale. La v0.4 non assegna alloggi. **Principio:** separare la *preferenza di progetto* (che il modello usa per lotto e commons) dalla *priorità di accesso* (mai derivata da dichiarazioni non verificate) [I].

---

## 6. Convergenze, contraddizioni, lacune

**Convergenze (otto voci su otto, ma vedi §2 sulla circolarità):** −2,0 °C da scartare; PCA/K-Means da scartare; Pask-MW da togliere; entropia da togliere; Southwark non verificato; contratto come brief e non come risultato; trasparenza Misurato / Modellato / Assunto da rafforzare; sezione 3 da mantenere.

**Contraddizioni e posizioni diverse:**
- Alexander: sezione 2 da **scartare**; le altre sette voci: **modificare**. Il motivo è la partizione disgiunta delle personas (albero) contro il semireticolo [S:04].
- Misfit: *rinominare* (Pask, Azadi, Carpo-Sanchez, ingegnere) oppure *binarizzare con un grafo* (Alexander, Azadi in alternativa). Decisione di Dennis.
- MVRDV: gli slider restano arbitrari (difetto noto di OptiMixer [S:22]) e la soggettività passa nella formula [S:22]; Azadi/De Carlo: il problema è chi scrive il filtro dei 18 lotti.
- Pask: il loop non è una conversazione finché il sistema non cambia anche regole o catalogo. AADRL: apprendere preferenze rivelate in un gioco è legittimo se dichiarato e contestabile. Compatibili solo se le due condizioni valgono insieme.
- Ingegnere: «numero esatto di unità» è un input legittimo del progettista [S:22]; Carpo-Sanchez e AADRL: non va derivato come risultato. Sintesi: si può fissare come *ipotesi di lavoro dichiarata*, non dedurre da bisogni e clima.

**Lacune (nessuna voce, nessuna scheda):** scelta sociale; urbanistica italiana (PGT, oneri, edilizia convenzionata, proprietà dei lotti); modelli di prezzo e costo; legame LST / temperatura dell'aria / effetto del verde; reclutamento e consenso informato; un processo decisionale reale in cui l'output entri (Azadi: decisore, momento, azione concreta; senza, resta una dimostrazione); soggetto istituzionale che porti oltre il tool (De Graaf-Murphy).

**Domande scambiate tra le voci e senza risposta (round 2 non fatto):**
- Pask → Alexander: riscrivere i criteri come misfit binari o rinominarli? Chi stabilisce la tolleranza di un criterio?
- Alexander → voce di scelta sociale (assente): quale regola ammette approvazioni sovrapposte?
- De Carlo → Pask: «osservatore dichiarato» basta, o gli abitanti devono scrivere il modello di osservazione?
- AADRL → ingegnere: quali vincoli minimi rendono il contratto verificabile?
- Carpo-Sanchez → ingegnere: quali vincoli duri non negoziabili sono sicuri e quali non calcolabili oggi?
- Azadi → De Carlo: chi decide l'ingresso nel processo?

---

## 7. Specifica corretta (da implementare come v0.5)

*Nome:* il file è già v0.4. La specifica corretta è la **v0.5**; la «v0.3» dell'originale è un obiettivo funzionale già in gran parte coperto dalla v0.4. Non implementare nulla senza conferma di Dennis.

**Invarianti.** Identità visiva e layout della v0.4; principio «Prima il lotto. Poi la scelta. Identità catastale, fattibilità e bisogni devono restare distinguibili.»; un solo `.html`; calcolo locale (dichiarare che font e immagini aeree usano la rete); nessun backend; nessun dato personale lasciato dal browser; backup prima di ogni modifica (il backup v0.4 è da fare).

**1. Territorio.** Quartieri e 18 immobili; stato per campo (Documentato storico / Indicativo / Scenario / Da acquisire) con colonne «Chi l'ha deciso» e «Chi può cambiarlo». I quattro sottosistemi diventano «criteri di scenario» (o grafo binario esplicito, a scelta di Dennis). «Requisiti di programma dichiarati»: verde minimo e funzioni mancanti a 15 minuti come soglie *scritte da un autore dichiarato*, etichetta *Assunto*; nessun «−2,0 °C», nessuna dote calcolata. Aggiungere il campo «proprietà: da acquisire».

**2. Domanda e commons.** Personas A/B/C più una persona avversaria e una «non rappresentata», con appartenenze sovrapposte e approvazioni generate indipendentemente dal catalogo; etichetta «scenario». MES con testo «regola con proprietà note; non garantisce rappresentatività dei votanti». Ogni commons riporta chi lo gestisce e a quali condizioni (dato assente = «da definire»). Catalogo aperto: l'abitante può proporre un commons, registrato con autore e data.

**3. Confronto.** WSM e Chebyshev affiancati, senza «raccomandata»; ρ e punto ideale visibili e modificabili; riga «divergenza tra metodi» invece di «rank reversal»; bonus di sinergia separato dal punteggio base e spento di default; veti con motivazione registrata; sensibilità come oggi, «non una probabilità». Graduatoria *per persona/gruppo* più media, maximin e lotti non dominati affiancati. Quinto criterio proposto dall'utente con punteggi ordinali 1-5.

**4. Feedback.** Motivi predefiniti più campo libero; η e moltiplicatore del motivo come parametri visibili; proposta mostrata criterio per criterio prima di applicarla, con annullamento; registro delle versioni dei pesi e delle contestazioni; dispersione per persona/gruppo invece dell'entropia; soglia minima sui pesi. Nome: «Revisione dei pesi tramite feedback», non «conversazione cibernetica» finché non vale una delle tre condizioni di Pask (§3.4). Etichetta dell'algoritmo: «aggiornamento moltiplicativo dei pesi (famiglia online learning)», senza Pask.

**5. Contratto.** `exploratory_design_brief_not_authorization`, quattro cancelli `pending`, campi di verifica a `null`. Struttura: vincoli duri (con fonte e autore), vincoli deboli, parti pubbliche obbligatorie a piano terra (come *funzioni*, non come numero di moduli), intervalli per SLP e quota libera, elenco «non verificato» (struttura, impianti, acustica, antincendio, esodo, catasto 3D, costi, raffrescamento). Nessuna dicitura RL o Assembler; pulsante «Esporta brief (.json)». Preview come «studio di ingombro» con convenzioni dichiarate.

**6. Metodo.** Registro delle fonti con stato; formule *realmente calcolate* (WSM, Chebyshev, MES, aggiornamento pesi) con i parametri convenzionali evidenziati; nessuna barra di confidenza; nessun Southwark; nessuna attribuzione non verificata. Pagina «Limiti e cosa non è» (nessun consenso, nessuna fattibilità, nessuna rappresentatività).

**7. Test (prima del codice).** Mantenere i 15 test del protocollo (da recuperare il file); aggiungere: regressione per stato dei dati; *parameter recovery* con votanti simulati a pesi noti e una persona strategica; caso con tutti i veti attivi; MES con approvazioni sovrapposte; misura del tempo di calcolo su dispositivi dichiarati.

---

## 8. Decisioni che spettano a Dennis

1. **Misfit.** Rinominare i quattro indici come «criteri di scenario», oppure binarizzarli con un grafo esplicito? (Il secondo è più fedele ad Alexander e più costoso.)
2. **Quanto potere sui criteri entra nella v0.5.** Basta il quinto criterio proposto dall'utente, o si vuole il catalogo completamente aperto? Senza almeno il primo, H2 non è misurabile.
3. **Regola di aggregazione.** Mostrare le regole affiancate senza default (raccomandato), o sceglierne una e giustificarla in F0?
4. **Southwark Atlas.** Da dove viene il riferimento? Se ha una fonte, indicala e la verifico; altrimenti resta fuori.
5. **Round 2 e revisore indipendente.** Da fare prima di integrare questo documento nel Report fondativo, con almeno una voce di scelta sociale o di dati che il team non ha.

*La tavola rotonda non è una prova: indica dove la specifica è più esposta. Le citazioni alle schede restano da verificare sui testi primari.*
