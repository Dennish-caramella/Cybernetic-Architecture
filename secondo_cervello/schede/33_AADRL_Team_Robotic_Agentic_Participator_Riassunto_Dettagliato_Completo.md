# Team Robotic (Agentic Participator): Modelli matematici e AI

> **Origine:** artifact Claude Docs `9a757aa9-6dbd-4fed-aab6-845c5f05c927`, letto il 2026-10-19 tramite il connettore. Copia salvata senza modifiche di contenuto.
> **Fonte primaria:** video "DRL (PG) MArch Phase II Final Presentations (Day 1)", segmento 5:13:03–6:12:12 più un'ora di critica, trascrizione letta dall'autore dell'artifact. **Non riverificata in questa sessione.**
> **Stato:** `da verificare`. I minuti citati sono quelli del video. I nomi dei membri sono trascritti dall'audio.
> **Legenda:** le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché la presentazione non mostra le equazioni usate. Sono **inferenza**.

## Sintesi

Il Team Robotic (studio Spyropoulos, Day 1, da 5:13:03 a 6:12:12) propone un'architettura fatta di robot che si auto-organizzano: moduli grandi (a scala di stanza) e piccoli (a scala di arredo) che si muovono, si arrampicano e si riconfigurano ogni giorno, ogni ora e in continuo, applicati al Centre Pompidou di Parigi. Il programma ufficiale lo chiama "Agentic Participator".

I sistemi AI sono quattro e lavorano a livelli diversi:

- **percezione:** YOLO per riconoscere persone, mani e altri robot; profondità stimata da immagini 2D;
- **decisione del singolo robot:** un modello visione-linguaggio (VLM) "di secondo ordine" che genera da sé il testo da cui decidere, tradotto in comandi JSON;
- **forma collettiva:** reazione-diffusione a doppia risoluzione come campo di valori spaziali verso cui i robot si muovono;
- **regia del sistema:** agenti LLM che osservano l'uso dello spazio e votano i parametri della reazione-diffusione, guidati da uno spazio latente addestrato su 150 configurazioni.

La giuria apprezza i prototipi fisici e l'approccio "da zero" alla tecnologia, ma chiede quale sia lo scopo finale, come si guidi la reazione-diffusione e quali nuove tipologie architettoniche ne derivino. Il momento citato come più interessante da Spyropoulos è il robot che si riconosce allo specchio (6:08:30).

## Contesto: lo studio Spyropoulos e il brief

Lo studio di Theodore Spyropoulos, direttore del DRL, lavora sotto il titolo "Everything Intelligence": intelligenza artificiale e naturale con enfasi sul non-umano, e architettura come "partnership in evoluzione con i sistemi" ([programma DRL](https://drl.aaschool.ac.uk/phase-2-review-jan-2026)). Il Team Robotic (Min, Susan Wong, Sing, Julie; nomi trascritti dall'audio) apre l'anno dello studio con il tema dell'intelligenza planetaria.

La tesi del team: l'intelligenza non è una proprietà ma un'interazione, una "conversazione" tra partecipanti, viventi o no. Gli antecedenti citati sono tre:

- **Gordon Pask** e la macchina per insegnare a scrivere a macchina: uomo e macchina imparano l'uno dall'altro (cibernetica);
- **AlphaGo**: anche nello scontro, entrambe le parti imparano dai pattern dell'altra;
- **Centre Pompidou e Fun Palace di Cedric Price**: architetture adattive, ma in cui l'edificio è il risultato della conversazione, non un interlocutore.

Da qui la richiesta: l'architettura deve avere agenzia propria, imparare dal pubblico e anche "curarlo", come sistema decentrato di agenti consapevoli di sé.

> **Collegamento con la tesi (inferenza):** il riferimento a Pask è già nel corpus (`tesi_out/arricchimenti/00_Pask_The_Architectural_Relevance_of_Cybernetics/`). La citazione è dichiarata dal team: non verificata qui sulla fonte di Pask.

## Il progetto passo per passo

| Minuto | Fotogramma | Cosa mostra |
|---|---|---|
| 5:14:02 | Pask e AlphaGo | L'intelligenza come conversazione |
| 5:16:59 | Agenti generativi | Macchine che dialogano via QR code |
| 5:17:40 | YOLO | Postura e stato dei pedoni, memoria temporanea |
| 5:18:34 | Dati spaziali condivisi | Latente come "memoria spaziale" |
| 5:19:18 | VLM di secondo ordine | Testo generato dalla macchina, azione in JSON |
| 5:21:10 | Specchio | Il robot riconosce sé stesso |
| 5:22:48 | Particelle | Regole locali, cluster, voxel |
| 5:23:37 | Reazione-diffusione | 25 run con parametri diversi |
| 5:24:28 | Doppia risoluzione | Agenti grandi prima, piccoli dopo |
| 5:25:26 | Locomozione | Cingoli magnetici, arrampicata |
| 5:27:14 | Pneumatica | Airbag, da 4 a 6 facce, attuatori lineari |
| 5:28:33 | Prototipo finale | Superficie gonfiabile, 6 micro-camere |
| 5:31:46 | Riconoscimento mano | Il cubo si ferma per evitare il contatto |
| 5:32:17 | RL di gruppo | Movimento coordinato |
| 5:33:29 | Centre Pompidou | Sito sperimentale, tre tempi di riconfigurazione |
| 5:34:40 | Agenti LLM osservatori | Decisione collettiva sui parametri |
| 5:35:48 | Spazio latente | 150 configurazioni raggruppate |
| 5:37:52 | Sequenza di un giorno | Struttura, funzioni, interni |
| 5:41:51 | Inizio critica | Giuria; risposta di Spyropoulos a 6:06:44 |

**1. Percezione e auto-consapevolezza (5:16–5:21).** I robot vedono con YOLO (postura, persone in movimento o ferme, relazioni con l'ambiente) e stimano la profondità da immagini 2D: un ambiente 3D "percepito", non misurato. Per ridurre i bias umani nella definizione di reward, il team usa un VLM "di secondo ordine": il prompt umano dice solo al robot il suo ruolo; il modello genera poi un proprio testo dalla visione e decide l'azione, tradotta in file JSON per gli attuatori. Il robot che si scopre allo specchio ripetendo il ciclo "vedi, agisci, rivedi" è il risultato più citato.

**2. Regole di auto-organizzazione (5:22–5:25).** Prima un sistema di particelle con regole per tipo, poi la reazione-diffusione (25 run). Ad alta risoluzione le forme sono definite ma servono centinaia di migliaia di agenti; da qui la doppia risoluzione: agenti grandi si organizzano prima, quelli piccoli suddividono l'interno.

**3. Robot fisici (5:25–5:32).** Cingoli con elettromagneti per arrampicarsi su pareti metalliche; telai grandi che si sollevano su ingranaggi; moduli pneumatici a 6 facce con airbag, poi attuatori lineari per muoversi in tutte le direzioni; superficie gonfiabile morbida al tatto; luci come segnali tra robot e verso le persone.

**4. Architettura al Pompidou (5:33–5:39).** Tre tempi: agenti grandi (stanze) si riconfigurano ogni giorno e trasportano fino a 1.000 agenti piccoli; i solai ogni ora; gli agenti piccoli (arredi) in continuo. Gli agenti LLM osservano come il pubblico usa lo spazio, scrivono osservazioni e decidono insieme i nuovi parametri della reazione-diffusione.

## Modelli matematici

I metodi sono quelli nominati nel video; le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché la presentazione non mostra le equazioni usate. **Inferenza.**

**Reazione-diffusione (Gray-Scott).** È il cuore formale del progetto. Due sostanze u e v diffondono a velocità diverse e reagiscono; i parametri di alimentazione F e di rimozione k decidono se nascono macchie, strisce o labirinti. Il nome del modello non è citato; Gray-Scott è il più usato in architettura.

$$\frac{\partial u}{\partial t} = D_u \nabla^2 u - u v^2 + F(1-u), \qquad \frac{\partial v}{\partial t} = D_v \nabla^2 v + u v^2 - (F+k) v$$

Nel progetto il campo v diventa un "valore spaziale": gli agenti si spostano verso le celle con valore più alto. La doppia risoluzione equivale a risolvere la stessa equazione su due griglie (grossa per la struttura, fine per gli interni), con la seconda limitata alla zona funzionale.

**Discretizzazione su griglia.** Il laplaciano diventa una somma sui vicini, cioè "come i pixel vicini si influenzano":

$$\nabla^2 u_{i,j} \approx u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - 4u_{i,j}$$

Il costo cresce con il numero di celle, da qui il problema delle "centinaia di migliaia" di agenti ad alta risoluzione.

**Sistema di particelle con regole per tipo.** Ogni particella di tipo a subisce forze dai vicini di tipo b con intensità G(a, b), che può attrarre o respingere; matrici asimmetriche producono cluster che si formano e si riformano:

$$\mathbf{F}_i = \sum_{j \ne i} G(\tau_i, \tau_j)\, f(|\mathbf{x}_j - \mathbf{x}_i|)\, \frac{\mathbf{x}_j - \mathbf{x}_i}{|\mathbf{x}_j - \mathbf{x}_i|}$$

**Rilevamento oggetti (YOLO).** Una rete convoluzionale divide l'immagine in celle e per ciascuna predice riquadri, confidenza e classe in un solo passaggio, abbastanza veloce per micro-camere su robot. Il team addestra un proprio modello per riconoscere gli altri robot.

**Decisione collettiva.** Gli agenti LLM osservatori producono ciascuno una proposta di parametri; la decisione finale è un'aggregazione, ad esempio una media o un voto. In forma semplice, con N osservatori: (F, k) nuovo = (1/N) Σ (Fᵢ, kᵢ). Il video non specifica la regola di aggregazione.

**Spazio latente delle configurazioni.** Le 150 configurazioni registrate vengono descritte da vettori di caratteristiche e proiettate in uno spazio a bassa dimensione in cui configurazioni simili si raggruppano. Serve a vedere quali zone dello spazio dei parametri (F, k) sono già state esplorate.

## Sistemi AI: architettura e componenti

Il sistema è a livelli: un campo matematico muove i robot, e un consiglio di agenti linguistici cambia il campo dopo aver osservato il pubblico.

| Componente | Tipo di AI | Ruolo | Stato nel progetto |
|---|---|---|---|
| YOLO (addestrato in proprio) | Rete convoluzionale di rilevamento | Riconoscere persone, mani, altri robot | Funziona su prototipi fisici |
| Profondità da immagine 2D | Stima monoculare | Ambiente 3D percepito | Dimostrato |
| VLM di secondo ordine | Modello visione-linguaggio | Decisione autonoma del singolo robot, output JSON | Dimostrato (episodio dello specchio) |
| Agenti con QR code | Agenti generativi (riferimento Stanford) | Comunicazione macchina-macchina | Esperimento iniziale |
| RL di gruppo | Reinforcement learning | Movimento coordinato tra più robot | Modello proprio, risultati preliminari |
| Reazione-diffusione | Modello matematico (non AI) | Forma collettiva e valore spaziale | Simulato in 2D e 3D |
| Agenti LLM osservatori | Modelli linguistici con prompt strutturati | Scelta dei parametri del campo | Proposto, regola di voto non mostrata |
| Spazio latente | Apprendimento non supervisionato | Mappa di 150 configurazioni | Proposto |

Punto notevole: il team usa il VLM proprio per evitare di scrivere a mano le reward del reinforcement learning, perché "la regola di premi e punizioni è sempre umana". È la critica opposta a quella rivolta ai team Bhooshan, a cui la giuria chiede invece reward più esplicite.

## Confronto con l'approccio del Bhooshan Lab

I due studi usano strumenti simili (reinforcement learning, LLM, spazi latenti) con scopi opposti: Bhooshan cerca equilibri ottimizzati e decisioni difendibili, Spyropoulos cerca comportamento, apertura e conversazione senza ottimizzare.

| Aspetto | Team Robotic (Spyropoulos) | Team Bhooshan (UpBridge, VertiCity, Make No Little Plans) |
|---|---|---|
| Scala | Edificio e arredo, con prototipi fisici | Città e distretto, con prototipi di struttura |
| Agenti | Robot fisici e agenti LLM | Attori economici astratti (2 giocatori) |
| Obiettivo dichiarato | Non ottimizzare: "provare nuove configurazioni" | Equilibrio win-win, ricavi, posti di lavoro |
| Ruolo del RL | Solo coordinamento del movimento; reward umane evitate | Motore delle decisioni urbane |
| Ruolo degli LLM | Osservatori che decidono insieme | Testati e scartati (UpBridge) |
| Spazio latente | Mappa di configurazioni spaziali | Mappa di piante e forme (SDF) |
| Forma | Reazione-diffusione, emergente | Grammatica SDF e statica, controllata |
| Critica principale | Manca lo scopo e la tipologia | Mancano reward chiare e varietà |

Le due posizioni si vedono bene nelle repliche finali: Bhooshan difende la produttività e la razionalità dei processi procedurali; Spyropoulos difende un'architettura che "ha dubbi", impara e non ha master plan (6:11:50).

## Valutazione critica

Il progetto è tra i più avanzati della giornata sul piano dei prototipi e dell'integrazione tra percezione, decisione e corpo fisico; resta aperto lo scopo architettonico del sistema.

**Cosa funziona**

- Lavoro "dal basso" sulla tecnologia: codice, robot e modelli costruiti dal team (5:41:51).
- Catena completa e dimostrata su hardware: vedere, decidere, muoversi, comunicare con luci.
- Doppia risoluzione: soluzione pratica al costo computazionale, con un corrispettivo architettonico (struttura e interno).
- L'episodio dello specchio: un caso reale di auto-riconoscimento emerso dal ciclo percezione-azione (6:08:30).

**Problemi aperti**

- **Come si guida la reazione-diffusione.** Patrick Schumacher chiede chi e come fissa i parametri e come entra il comportamento del pubblico (5:46:35). Il team risponde che il sistema impara dopo 20–100 iterazioni, ma non lo mostra.
- **Scopo e valore.** Cosa ottiene il pubblico e perché un investitore dovrebbe pagare questo sistema (5:58:34).
- **Tipologia.** Quale architettura nasce da una riconfigurazione continua; "appena la fissi perde il suo fascino" (6:05:08).
- **Linguaggio estetico.** Prototipi gonfiabili o nuvola di punti astratta: quale dei due è la proposta (5:51:05).
- **Presentazione chiusa.** I render "timidi" rispetto ai modelli; meglio cento varianti che un prodotto finito (5:54:42, 5:57:47).
- **Aggregazione degli LLM non specificata.** Non è chiaro come si combinano le opinioni degli osservatori né come si evitano i loro bias.

**Spunti**

- Pubblicare lo spazio dei parametri (F, k) con le 150 configurazioni e la traiettoria scelta dagli osservatori.
- Raccontare il progetto dal punto di vista del robot, come suggerisce Spyropoulos (6:10:42).
- Integrare reti di servizi (acqua, energia, aria) tra le unità, sul modello dei tubi del Pompidou (6:03:17).

## Fonti

- [Video: DRL (PG) MArch Phase II Final Presentations (Day 1)](https://www.youtube.com/watch?v=9bQG8m6E3nk&t=18783s), segmento 5:13:03–6:12:12, trascrizione letta dall'autore dell'artifact il 19 ottobre 2026. Stato: `da verificare` in questa sessione.
- [DRL Phase 2 Review, gennaio 2026](https://drl.aaschool.ac.uk/phase-2-review-jan-2026). Stato: `da verificare` in questa sessione.
- [Analisi Bhooshan, Day 1](https://claude.ai/code/artifact/16c9875c-a5a1-4cbd-8a76-a99826cf1508). Vedi `01_AA_DRL_Phase_II_Day1_Bhooshan.md`.
- [Analisi Bhooshan, Day 2](https://claude.ai/code/artifact/305b60f6-30a7-43d2-a3a9-b77ce03843f4). Vedi `02_AA_DRL_Phase_II_Day2_Bhooshan_Make_No_Little_Plans.md`.
- Riferimenti citati nel testo ma non verificati qui: Gordon Pask (macchina per insegnare a scrivere a macchina), Cedric Price (Fun Palace), modello Gray-Scott, riferimento Stanford sugli agenti generativi. Da reperire e verificare prima di ogni citazione in tesi.
