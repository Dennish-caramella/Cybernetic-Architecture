# AA DRL Phase II Day 1: Modelli matematici e AI (focus Shajay Bhooshan)

> **Origine:** artifact Claude Docs `16c9875c-a5a1-4cbd-8a76-a99826cf1508`, letto il 2026-10-19 tramite il connettore. Copia salvata senza modifiche di contenuto; formule e tabelle ricostruite dal formato originale.
> **Fonte primaria:** video "DRL (PG) MArch Phase II Final Presentations (Day 1)", trascrizione completa (7 h 33 min, 2.652 segmenti) letta dall'autore dell'artifact. **Non riverificata in questa sessione.**
> **Stato:** `da verificare` (trascrizione e pagine DRL non aperte da me). I minuti citati sono quelli del video.
> **Legenda:** le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché le presentazioni non mostrano le equazioni esatte. Sono **inferenza**, non dati del team.

## Sintesi

Nel Day 1 il Bhooshan Lab presenta due progetti: **UpBridge City** (7:42) e **VertiCity** (6:29:35). Entrambi usano la stessa architettura in due stadi: un gioco urbano a due agenti risolto con reinforcement learning ("Game AI") e un autoencoder su campi di distanza con segno (SDF) per generare le forme degli edifici ("Shape AI").

- **UpBridge City** (Thamesmead/Barking, modello Shenzhen): il progetto più tecnico sull'AI. Passa da un RL a modello unico a un RL multi-agente, confronta un agente LLM (actor-reflector) con PPO e costruisce una "mappa latente" con codifica posizionale.
- **VertiCity** (Swansea, modello Hong Kong): usa i data center "edge AI" come catalizzatore economico, un gioco con matrice di reward "di Nash", circle packing e campi vettoriali, e sviluppa la parte tettonica (strutture sospese).

La giuria apprezza il lavoro "dai principi primi" sull'AI ma critica in entrambi i casi zonizzazione troppo semplice, reward non spiegati e assenza di parametri ambientali ed energetici. Bhooshan stesso ammette che i risultati "non sono ancora convincenti dal punto di vista del progetto" (1:04:37).

## Contesto: il Day 1 e i due team del Bhooshan Lab

Il Day 1 (8 gennaio 2026) ha sei presentazioni e si chiude con la keynote di Claudia Pasquero ([programma DRL](https://drl.aaschool.ac.uk/phase-2-review-jan-2026)). Il Bhooshan Lab porta due dei suoi tre team; il terzo, "Make No Little Plans", presenta il Day 2.

| Ora | Team | Studio |
|---|---|---|
| 0:07:42 | UpBridge City (Atul, Fenling, Finen, Low) | Bhooshan |
| 1:17:57 | Ember | Angius |
| 2:20:23 | Tesser[act] | Schumacher |
| ~4:10 | Statera | Angius |
| 5:13:03 | Agentic Participator (team "Robotic") | Spyropoulos |
| 6:29:35 | VertiCity (Da, Yash, Ashwit) | Bhooshan |

L'agenda dello studio, "AI for New Cities", viene letta da Theodore Spyropoulos all'apertura (4:16): AI e nuove città come problemi che si condizionano a vicenda, con l'agenzia progettuale collocata nei dettagli tecnici dell'AI e non nell'automazione dei risultati. I nomi dei membri sono trascritti dall'audio e possono essere imprecisi.

Bhooshan nel commento finale su UpBridge (1:00:38) dichiara che questo è "il primo anno in cui come studio guardiamo a fondo nei dettagli tecnici dell'AI". UpBridge cita come antecedenti i progetti DRL "Meta London" e "Parti-Cities", in cui lo stesso gioco urbano era giocato a mano.

## UpBridge City: analisi passo per passo

**Sito:** Thamesmead e Barking (Londra), vicino a London City Airport e Barking Riverside. **Modello di riferimento:** Shenzhen come "gioco cooperativo tra Stato e mercato". **Programma:** tre poli (istruzione, industria high-tech, ricerca) in ciclo di retroazione.

| Minuto | Fotogramma | Cosa mostra |
|---|---|---|
| 0:08:01 | Metodi per scala | RL e LLM per la città, mappa latente per gli edifici |
| 0:13:41 | Campo scalare | Tre hub di trasporto, mappa del valore fondiario |
| 0:14:28 | Dilemma del prigioniero | Nash inefficiente vs obiettivo win-win |
| 0:15:21 | Agenti e regole | Council vs manufacturer, 1 mese = 1 turno |
| 0:19:30 | Iterazione 1 | Un solo modello RL: collasso della policy |
| 0:20:11 | Iterazione 2 | RL multi-agente, obiettivi separati |
| 0:20:53 | Sblocco azioni | Meccanica "Red Alert": economie di scala |
| 0:23:34 | LLM actor-reflector | Agenti linguistici per il layout dei piani |
| 0:24:34 | PPO | Reward da negativo a circa 4.000 in 1.000 episodi |
| 0:28:01 | Mappa latente | MLP con codifica posizionale su 4 forme |
| 0:29:44 | Direzioni semantiche | 4 assi latenti = 4 trasformazioni di pianta |
| 0:30:39 | Latente 3D | Z = interpolazione tra piani di piano |
| 0:36:38 | Casseri stampati 3D | Nodi strutturali prefabbricati in calcestruzzo |
| 0:40:17 | Inizio critica | Giuria |

**1. Game AI a due livelli (13:41–26:00).** Un campo scalare e campi vettoriali fissano i centri e le scelte iniziali dei lotti. Il gioco ha due agenti: il council (possiede la terra, costruisce infrastrutture, scuole, residenze) e il manufacturer (compra terra, costruisce fabbriche, genera profitto). Ogni azione ha costo iniziale e rendimento continuo; il prezzo del suolo è un campo dinamico.

Tre iterazioni RL documentano i problemi tipici:

1. Un solo modello controlla entrambi e somma le reward: collasso su un'unica azione ripetuta ("policy collapse"), letto come "Nash negativo".
2. Multi-agente con obiettivi separati: niente più collasso immediato, ma edifici lontani dal fiume e funzioni ripetute.
3. Sblocco di edifici avanzati a una certa soglia di sviluppo: la policy inizia a preferire rendimenti di lungo periodo.

Il secondo livello distribuisce sotto-funzioni per piano (commercio al piano terra, ecc.). Un framework LLM actor-reflector viola le regole (commercio ai piani alti); PPO le rispetta e sale da reward negativa a circa 4.000 in 1.000 episodi.

**2. Shape AI (26:15–32:12).** Un MLP impara piante come SDF. Le coordinate (x, y) del sito passano per una codifica posizionale multi-frequenza; quattro zone ricevono quattro forme-funzione. La "mappa latente" assegna a ogni punto del sito una forma intermedia. Poi il team introduce direzioni semantiche nel latente e un asse Z per interpolare tra i piani: ogni torre è un percorso nello spazio latente.

**3. Costruzione (36:38–37:53).** Analisi dei nodi ripetuti, casseri stampati in 3D e getto in calcestruzzo armato per nodi prefabbricati.

## VertiCity: analisi passo per passo

**Sito:** Swansea (Galles), stretto tra colline, mare e fiume, con poca terra edificabile. **Modello di riferimento:** l'urbanistica verticale di Hong Kong ("Cities Without Ground"). **Catalizzatore:** data center "edge AI" piccoli, vicini agli utenti, dedicati all'inferenza, che attirano gaming, fintech, AR/VR e sanità.

| Minuto | Fotogramma | Cosa mostra |
|---|---|---|
| 6:32:36 | AI 2025 vs AI 1986 | Modelli a prompt vs apprendimento di rappresentazioni |
| 6:33:06 | Mappa latente | SDF codificate e decodificate con autoencoder |
| 6:34:52 | Edge AI data center | Il data center come catalizzatore urbano |
| 6:37:55 | Simulazione ad agenti | Campi vettoriali da centri, orientamento degli edifici |
| 6:39:27 | Due giocatori | Economic developer vs city developer |
| 6:40:40 | Matrice di reward | Logica "Nash": esito negativo ferma lo sviluppo |
| 6:42:08 | Scelta dei centri | Punteggio su camminabilità e terra edificabile |
| 6:42:42 | Circle packing | Lotti di taglie diverse per tipo di agente |
| 6:44:55 | SDF 2D → 3D | La stessa logica dalla pianta alla torre |
| 6:45:28 | Loss dell'autoencoder | Ricostruzione dei valori SDF |
| 6:46:43 | Torre a 3 nuclei | Campo, esiti latenti, pianta risolta |
| 6:50:36 | Struttura sospesa | Solai appesi a travature dal nucleo |
| 6:53:10 | Residenze SDF | Densità che varia in altezza a GIA costante |
| 6:58:31 | Inizio critica | Giuria |

**1. Game AI (6:39–6:44).** Ciclo economico: il giocatore economico compra terra dal giocatore città e costruisce il data center; sopra mette uffici; con i ricavi il giocatore città avvia residenze e infrastrutture. Un ciclo completo = un data center da 4 MW. Lo sviluppo procede in fasi: regole semplici a massimo ricavo, poi matrice di reward (esito negativo blocca la crescita, positivo la estende), poi funzioni di stato con valore fondiario per lotto e retroazione continua. Il tabellone è specifico del sito: rete stradale esistente, tre centri scelti per punteggio, circle packing dei lotti, campi vettoriali con attrattori e deviatori sul terreno, campo delle altezze.

**2. Shape AI (6:44–6:55).** Primitive direzionali in SDF 2D, propagate in verticale per costruire torri con vuoti, gradienti e tagli. L'autoencoder ricostruisce i valori SDF nei punti campionati; navigare il latente cambia il mix di programmi lungo l'altezza (data center alla base, uffici, residenze, commercio). Tipi: torri a 1 e 3 nuclei, residenze medie, residenze basse sul pendio, residenze sul fronte d'acqua.

**3. Tettonica (6:50–6:52).** Torri con solai sospesi a travature in acciaio che sbalzano dal nucleo; il basamento si costruisce separatamente dal basso. Le stesse travature fanno da ponti tra torri, creando un "nuovo suolo" a quote alte.

## Modelli matematici

I metodi sono quelli nominati nel video; le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché le presentazioni non mostrano le equazioni esatte. **Inferenza.**

**Dilemma del prigioniero e Nash (UpBridge).** Il team usa il dilemma per spiegare perché agenti razionali finiscono in un equilibrio inefficiente. Con payoff T > R > P > S, "defezionare" è dominante per entrambi, quindi l'equilibrio (D, D) dà P a ciascuno anche se (C, C) darebbe R > P:

$$\begin{array}{c|cc} & C & D \\ \hline C & (R,R) & (S,T) \\ D & (T,S) & (P,P) \end{array} \qquad T > R > P > S$$

Il progetto legge il collasso della policy RL come un "Nash negativo" e cambia le regole (sblocco di edifici, economie di scala) per rendere conveniente la cooperazione. È una lettura corretta: si modifica il gioco, non i giocatori.

**Processo decisionale di Markov e PPO.** Ogni mese è un passo; stato = mappa, prezzi, fondi; azione = edificio e lotto (o passare); reward = rendimento meno costo. PPO aggiorna la policy limitando il passo con un rapporto troncato:

$$L^{CLIP}(\theta) = \mathbb{E}_t\left[ \min\left( r_t(\theta) \hat{A}_t,\; \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\, \hat{A}_t \right) \right], \quad r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$$

Il passaggio da un modello unico a due agenti indipendenti corrisponde a sostituire una reward congiunta r₁ + r₂ con due obiettivi separati: il problema diventa un gioco stocastico multi-agente, non più un'ottimizzazione singola.

**Campi scalari e vettoriali.** Il valore del suolo è un campo costruito dalle distanze dagli hub e dal fiume, ad esempio V(p) = Σ wᵢ e^(−d(p, hᵢ)/λᵢ). Il campo vettoriale è il suo gradiente, ∇V, e orienta lotti ed edifici. In VertiCity attrattori e deviatori sul terreno modificano lo stesso campo.

**Circle packing (VertiCity).** I lotti sono cerchi di raggio dipendente dal tipo di agente, disposti senza sovrapposizione: |cᵢ − cⱼ| ≥ rᵢ + rⱼ, con raggi maggiori vicino ai centri.

**SDF e autoencoder (entrambi).** Una pianta è il livello zero di f(x, y). L'MLP impara f dato un codice latente z e minimizza l'errore sui punti campionati. UpBridge aggiunge la codifica posizionale delle coordinate del sito, che permette all'MLP di rappresentare dettagli ad alta frequenza:

$$\gamma(p) = \left( \sin(2^0 \pi p), \cos(2^0 \pi p), \ldots, \sin(2^{L-1} \pi p), \cos(2^{L-1} \pi p) \right), \qquad \mathcal{L} = \frac{1}{N}\sum_i \left( f_\theta(\gamma(p_i), z) - f(p_i) \right)^2$$

Le "direzioni semantiche" sono vettori v nel latente tali che z + αv produce una trasformazione riconoscibile della pianta (apertura, orientamento). L'asse Z come interpolazione tra piani rende ogni torre una curva z(h) nel latente.

## Sistemi AI: pipeline e componenti

I due team condividono la stessa catena in quattro stadi; cambiano il tabellone del gioco e il sistema costruttivo. In entrambi il flusso è lineare: la costruzione non retroagisce sul gioco, critica ripetuta in giuria (7:14:04).

| Componente | Tipo | Progetto | Stato nel lavoro |
|---|---|---|---|
| RL a modello unico | Reinforcement learning | UpBridge | Collasso della policy; scartato |
| RL multi-agente (PPO) | Reinforcement learning, policy gradient | UpBridge | Funziona; reward da negativo a ~4.000 in 1.000 episodi |
| Agente LLM actor-reflector | Modello linguistico con auto-correzione | UpBridge | Viola le regole; scartato a favore di PPO |
| Gioco con matrice di reward | RL con funzioni stato/azione/reward | VertiCity | Implementato in tre fasi; dettagli dei payoff non mostrati |
| Simulazione ad agenti e campi vettoriali | Procedurale | VertiCity | Base del tabellone |
| MLP su SDF con codifica posizionale | Rete neurale (implicit neural representation) | UpBridge | Mappa latente con 4 direzioni semantiche |
| Autoencoder SDF | Rete neurale | VertiCity | Latente navigato per torri e residenze |

Il risultato tecnico più interessante è il confronto LLM contro PPO: su un compito con regole numeriche precise, un agente linguistico generico non addestrato sul compito rende molto meno di una policy addestrata. Schumacher però chiede di mostrare come è calcolata la reward, perché il divario dichiarato (circa 6–7 volte) gli sembra sospetto (46:21).

## Confronto con gli altri studi e con il Day 2

Gli altri studi del Day 1 usano soprattutto simulazione fisica e algoritmi di ottimizzazione classici; solo Bhooshan e Spyropoulos addestrano modelli di apprendimento.

| Team (studio) | Modelli matematici / AI | Uso |
|---|---|---|
| UpBridge City (Bhooshan) | RL multi-agente PPO, agente LLM, MLP-SDF con codifica posizionale | Distretto a Thamesmead/Barking |
| Ember (Angius) | Simulazione di propagazione degli incendi, flocking | Unità mobili anti-incendio |
| Tesser[act] (Schumacher) | Sistema multi-agente per il programma, algoritmi di rete per la circolazione, fluidodinamica euleriana, algoritmo genetico e simulated annealing | Mega-edificio |
| Statera (Angius) | Simulazione sismica, airbag, analisi tensione/deformazione | Unità aggregate in zona sismica |
| Agentic Participator (Spyropoulos) | Agenti generativi (riferimento Stanford), RL, robot con 6 camere | Architettura come sistema di agenti |
| VertiCity (Bhooshan) | Gioco a reward, circle packing, campi vettoriali, autoencoder SDF | Città verticale a Swansea |

**Evoluzione rispetto al Day 2.** "Make No Little Plans" (Day 2) riprende lo stesso schema ma aggiunge Q-learning su uno spazio latente economico e la statica grafica 3D per la struttura. I tre team mostrano quindi un'unica agenda di laboratorio declinata su tre siti e tre catalizzatori: industria e ricerca (UpBridge), data center (VertiCity), startup tecnologiche (Make No Little Plans).

## Valutazione critica

Il valore dei due progetti è metodologico: aprono la "scatola" dell'AI invece di usarla come generatore di immagini. Il limite è che i risultati urbani e architettonici non sono ancora all'altezza del metodo, come ammette lo stesso Bhooshan.

**Cosa funziona**

- Il percorso RL di UpBridge è didattico e onesto: mostra fallimenti reali (collasso della policy) e come cambiare le regole del gioco per uscirne.
- La mappa latente rende ispezionabile lo "spazio delle piante possibili", a differenza dei grandi modelli chiusi (Bhooshan, 1:02:15).
- VertiCity ha il gioco più chiaro e un'idea urbana forte (data center edge come catalizzatore) con una tettonica coerente.
- Produttività: secondo Bhooshan, ogni scala affrontata da VertiCity avrebbe richiesto in passato tre studenti per un anno (7:23:46).

**Problemi aperti**

- **Reward non spiegate.** Come si calcolano valore e reward, e perché PPO batte l'LLM di 6–7 volte (46:21).
- **Zonizzazione semplice.** Tre zone omogenee in UpBridge, troppo poca mescolanza di funzioni (40:30, 47:50).
- **Parametri ambientali assenti.** Vento, sole, calore, servizi ecosistemici, energia dei data center (53:05, 55:05, 7:01:11).
- **Uso del termine "latente".** Un critico osserva che le SDF in sé non sono AI e che parlare di "latent space" va giustificato (7:03:35).
- **Rigore strutturale e piante.** Sbalzi e aste sospese non sempre coerenti; mancano piante degli alloggi che dimostrino che le forme funzionano (7:04:14, 7:06:17).
- **Processo lineare.** Nessun ritorno dalla struttura al masterplan (7:14:04).

**Spunti**

- Pubblicare spazi di stato, azioni e reward come tabelle esplicite, con curve di apprendimento e confronto con una baseline casuale.
- Inserire nel gioco termini ambientali e energetici calcolati (es. fabbisogno e raffreddamento dei data center, rendimento solare).
- Lasciare che il modello produca varianti radicali, non solo ottimizzazioni: è la richiesta finale di Spyropoulos (7:30:09).

## Fonti

- [Video: DRL (PG) MArch Phase II Final Presentations (Day 1)](https://www.youtube.com/watch?v=9bQG8m6E3nk), trascrizione completa letta dall'autore dell'artifact il 19 ottobre 2026. Stato: `da verificare` in questa sessione.
- [DRL Phase 2 Review, gennaio 2026](https://drl.aaschool.ac.uk/phase-2-review-jan-2026). Stato: `da verificare` in questa sessione.
- [Bhooshan Lab, AA DRL](https://drl.aaschool.ac.uk/bhooshan-lab). Stato: `da verificare` in questa sessione.
- [Shajay Bhooshan, Zaha Hadid Architects](https://www.zha.com/people/shajay-bhooshan). Stato: `da verificare` in questa sessione.
- [Analisi del Day 2](https://claude.ai/code/artifact/305b60f6-30a7-43d2-a3a9-b77ce03843f4). Vedi `02_AA_DRL_Phase_II_Day2_Bhooshan_Make_No_Little_Plans.md`.
