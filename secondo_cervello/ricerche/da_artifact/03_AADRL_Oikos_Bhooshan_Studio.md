# AADRL Oikos: Modelli matematici e AI (Bhooshan Studio)

> **Origine:** artifact Claude Docs `f2248619-680f-4909-877e-2bcf03b7fb6b`, letto il 2026-10-19 tramite il connettore. Copia salvata senza modifiche di contenuto.
> **Fonte primaria:** libro "Oikos" (AADRL 17/19, Nahmad Bhooshan Studio, Team Oikos), 224 pagine, letto sulle pagine di Issuu indicate. **Il testo non è estraibile**: le citazioni sono parafrasi delle pagine viste dall'autore dell'artifact.
> **Stato:** `da verificare` per il contenuto; il libro è da confrontare con l'originale prima di citare pagine.
> **Legenda:** le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact. Sono **inferenza**.

## Sintesi

"Oikos" (Nahmad Bhooshan Studio, AADRL 2017–19) è il primo esperimento dello studio sulla casa come gioco: gli abitanti costruiscono la torre giocando in realtà virtuale, e i loro dati diventano la regola di crescita.

Il progetto parte da due conflitti londinesi: affitto contro proprietà e vivere da soli contro condividere. Su una griglia esagonale i giocatori agganciano unità private a una circolazione pubblica. Ogni unità ha un costo legato a sbalzo, vista, luce e altezza. Il gioco misura soddisfazione, unità condivise, unità in affitto e costo strutturale. I dati raccolti vengono raggruppati in cluster di giocatori e usati per simulazioni ad agenti, che generano una torre a capsule organiche. Il libro chiude con un prototipo in scala 1:1 tagliato da un robot a filo caldo.

La forza del progetto è la catena continua che va dal tema sociale al gioco, ai dati, alla forma e alla fabbricazione. Il limite è che il problema economico resta un punteggio di gioco, e il tempo di cui parla la tesi non si vede nelle immagini finali. **Nessuna rete neurale**: è un sistema a regole con un clustering statistico dei dati di gioco.

## Contesto: Oikos nel percorso dello studio

Il team è composto da Cesar Fragachan, Jianfei Chu, Melis Kucuktunc e Taizhong Chen. Tutor: Alicia Nahmad Vazquez e Shajay Bhooshan (copertina del libro). È il ciclo 2017–19 del DRL, quando lo studio univa due agende: il gioco come strumento di progetto (Bhooshan) e la fabbricazione robotica (Nahmad).

La tesi (p. 21) sostiene che il fallimento più grave dell'architettura moderna sia l'idea di un edificio statico e senza tempo. Le dinamiche sociali cambiano di continuo, quindi serve un set di regole in cui ognuno partecipa al progetto senza rompere la coerenza dell'insieme. Il riferimento è Frei Otto: case progettate "dalle mani di chi le abita" (parafrasi).

La linea che porta al 2026:

1. **2017–19, Oikos:** gioco VR giocato da persone reali; i dati alimentano agenti a regole.
2. **2023–24, Meta London:** gioco urbano a turni tra sviluppatori, con regole scritte a mano.
3. **2025–26, UpBridge, VertiCity, Make No Little Plans:** lo stesso gioco risolto con reinforcement learning, equilibrio di Nash e forme da autoencoder su SDF.

## Il progetto passo per passo

| Pagine | Sezione | Cosa mostra |
|---|---|---|
| 9–17 | Introduzione | Agenda AADRL e dello studio, contesto londinese |
| 21 | Tesi | Architettura adattiva e partecipata contro l'edificio statico |
| 25–40 | Precedenti | Città verticali, Nakagin, Habitat 67, co-living, autocostruzione |
| 45–48 | Giochi di riferimento | Palagonia, Blockhood, The Sims |
| 50–83 | Esercizi di gioco | Game theory, Lego, griglia, creature, Game of Life, share-mate, soddisfazione |
| 84–85 | Packing e aggregazione | Griglia esagonale sul sito; crescita per direzione, figli e vicini |
| 86–99 | Oikos Game in VR | Interfaccia, come si gioca, costo delle unità |
| 102–103 | Raccolta dati | Profilo del giocatore e azioni di gioco |
| 104–105 | Clustering | 80 giocatori in uno spazio 3D, 4 tipi |
| 106–107 | Agenti e flusso | Studente, freelance, famiglia, investitore; ciclo utenti → gioco → dati |
| 108–109 | Simulazioni ad agenti | Mix 25% investitori / 75% studenti con 4 indicatori |
| 122–125 | Form finding | Ottaedro troncato, film di sapone, rilassamento delle superfici |
| 128–141 | Unità | Circa 30 tipi, libreria, aggregati da 2 a 12 unità, arredo |
| 142–147 | Edificio | Circolazione, facciate, assemblaggio, variazione strutturale a gradiente |
| 157–176 | Filo caldo | Precedenti, end effector, traiettorie del robot ABB |
| 185–212 | Prototipo 1:1 | Componenti, taglio, finiture, montaggio in sito |

**1. Ricerca (pp. 9–40).** Il problema è la casa a Londra vista da due lati: chi affitta e chi possiede, chi vive solo e chi condivide. I precedenti sono le megastrutture a capsule (Nakagin, Habitat 67) e le comunità che si costruiscono da sole.

**2. Esercizi di gioco (pp. 45–83).** Prima giochi semplici su carta e Lego. Nel primo esercizio di game theory (p. 50) quattro giocatori partono dal centro di una scacchiera e conquistano caselle: quelle nel territorio altrui valgono di più (da ×1 a ×4), e se due giocatori scelgono la stessa casella nessuno segna.

**3. Oikos Game (pp. 84–99).** Su un sito londinese si stende una griglia esagonale; le unità sono celle impacchettabili. Il giocatore, con visore e controller, pianta un "seme" e aggancia la sua unità a una faccia della circolazione pubblica. Ogni unità costa punti in base alla posizione strutturale: un'unità a sbalzo costa di più perché richiede struttura extra (nell'esempio, unità da 30 e da 40 punti). Vista, luce e altezza cambiano il prezzo.

**4. Dati e agenti (pp. 102–109).** Il gioco registra profilo (età, genere, interessi, con chi si vive) e azioni (numero, funzione, dimensione e posizione delle stanze, arredi, verde). Ottanta partite vengono proiettate in uno spazio 3D e raggruppate in quattro tipi. I tipi diventano agenti che popolano simulazioni con mix diversi.

**5. Architettura e fabbricazione (pp. 119–212).** Il form finding (film di sapone, rilassamento) dà la forma delle cellule. Una libreria di unità si aggrega in una torre a capsule con struttura a gradiente. Le superfici sono rigate per poter essere tagliate a filo caldo da un robot, fino al prototipo 1:1 in EPS.

## Modelli matematici

I metodi sono quelli mostrati nel libro; le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact. Il libro non riporta equazioni né il nome dell'algoritmo di clustering. **Inferenza.**

**Packing esagonale e aggregazione.** L'unità base è un ottaedro troncato, uno dei pochi solidi che riempiono lo spazio senza vuoti. In pianta dà una griglia esagonale. La crescita è una regola locale con tre parametri (p. 85): direzione di crescita, numero massimo di "figli" per cella e numero massimo di vicini.

$$c_{t+1} \in N(c_t), \qquad |\text{figli}(c)| \le k_{\max}, \qquad |N_{\text{occ}}(c)| \le n_{\max}$$

Qui N(c) sono le celle adiacenti a c nella direzione consentita. Con kmax e nmax bassi la crescita resta lineare; con valori alti diventa a grappolo. È un'aggregazione a regole, parente degli automi cellulari (Game of Life è tra gli esercizi, p. 66).

**Gioco della scacchiera (p. 50).** Quattro giocatori muovono in simultanea. Il guadagno di una casella dipende da chi la possiede, e una collisione annulla il punto:

$$u_i = \sum_{s \in S_i} v_i(s), \qquad v_i(s) \in \{1, 2, 4\}, \qquad s_i = s_j \Rightarrow v_i(s) = v_j(s) = 0$$

È un gioco simultaneo con interferenza: introduce il conflitto tra espandersi nel territorio altrui (più valore) e rischiare la collisione.

**Costo dell'unità.** Ogni unità virtuale riceve un costo dalla sua posizione strutturale, e il costo si aggiorna con i vicini. Una forma plausibile, coerente con le regole descritte (pp. 90–91):

$$C(u) = C_0 + \alpha\, \text{sbalzo}(u) + \beta\, \text{vista}(u) + \gamma\, \text{luce}(u) + \delta\, h(u) - \epsilon\, |N_{\text{occ}}(u)|$$

L'ultimo termine rende più economica un'unità appoggiata ad altre. Il giocatore spende un budget: è una scelta vincolata, non un'ottimizzazione.

**Clustering dei giocatori (pp. 104–105).** Ottanta partite diventano vettori di caratteristiche (profilo + azioni), proiettati in uno spazio tridimensionale e divisi in quattro gruppi. La forma più probabile è una riduzione di dimensione seguita da k-means con k = 4:

$$\min_{\{\mu_j\}} \sum_{i=1}^{80} \min_{j \in \{A,B,C,D\}} \lVert \mathbf{x}_i - \mu_j \rVert^2$$

I centroidi diventano quattro profili: studente (budget basso, circa 3 unità, molto sociale), freelance (circa 5), famiglia (circa 6, poco sociale), investitore (budget alto, circa 8 unità, compra per affittare).

**Simulazione ad agenti e indicatori (pp. 108–109).** Si fissa un mix di agenti (per esempio 25% investitori, 75% studenti) e li si lascia crescere la torre. L'esito è letto con quattro indici su 100: soddisfazione media 72, unità condivise 51, unità in affitto 46, costo della struttura 39.

$$\text{esito}(\mathbf{m}) = \big(\bar{S},\; \%_{\text{condivise}},\; \%_{\text{affitto}},\; C_{\text{struttura}}\big), \qquad \mathbf{m} = (m_A, m_B, m_C, m_D),\; \textstyle\sum m = 1$$

Cambiando il mix m si confrontano scenari sociali, ma il libro non combina gli indici in un unico punteggio né cerca il mix migliore.

**Form finding fisico (pp. 122–125).** Il film di sapone sezionato secondo tre piani trova superfici minime, a curvatura media nulla (H = 0). Il rilassamento digitale ne è l'analogo: una rete di molle che si sposta fino all'equilibrio. Da qui nasce la libreria di stanze.

**Superfici rigate per il filo caldo (pp. 162–176).** Il filo è un segmento tra due punti dell'end effector, quindi taglia solo superfici rigate:

$$\mathbf{r}(u, v) = (1 - v)\, \mathbf{a}(u) + v\, \mathbf{b}(u), \qquad v \in [0, 1]$$

Le curve a(u) e b(u) sono le traiettorie dei due capi del filo, convertite in piani di lavoro del robot ABB. Questo vincolo spiega le pareti a pieghe verticali del prototipo.

## Sistemi computazionali: il ciclo del gioco

Oikos non usa AI nel senso di apprendimento automatico: è un gioco giocato da persone, un clustering statistico dei loro dati e agenti a regole che ne imitano i comportamenti.

La riga superiore produce conoscenza sociale, quella inferiore la costruisce; il libro collega le due solo attraverso il gioco, non con un passaggio automatico dai dati alla forma.

| Componente | Tipo | Ruolo nel progetto | Erede nel 2026 |
|---|---|---|---|
| Packing di ottaedri troncati | Geometria che riempie lo spazio | Tabellone del gioco e cellula base | Circle packing e campi vettoriali (VertiCity) |
| Regola di aggregazione | Crescita locale, tipo automa cellulare | Torri lineari o a grappolo | Grammatica SDF (Day 2) |
| Oikos Game in VR | Gioco con giocatori umani | Raccolta di scelte reali sulla casa | Giochi multi-agente risolti con RL |
| Costo delle unità | Funzione di prezzo vincolata | Lega struttura, vista e luce al budget | Reward e funzioni di stato con valore fondiario |
| Clustering di 80 giocatori | Statistica non supervisionata | Quattro profili: studente, freelance, famiglia, investitore | Agenti RL (UpBridge) |
| Simulazioni ad agenti | Agenti a regole | Scenari per mix sociale con 4 indicatori | Equilibrio di Nash e Q-learning (Day 2) |
| Film di sapone e rilassamento | Form finding fisico e digitale | Forma delle stanze | Autoencoder su SDF |
| Traiettorie a filo caldo | Superfici rigate, robotica | Prototipo 1:1 | Casseri 3D, statica grafica |

Ogni pezzo del 2017–19 ha un erede nel 2026: il gioco resta, ma i giocatori umani diventano agenti che imparano. **Inferenza**: la tabella è un confronto costruito dall'autore dell'artifact, non una dichiarazione del libro.

## Confronto con Meta London e i progetti 2026

Oikos è l'unico dei quattro progetti in cui il gioco è giocato da persone reali e in cui si arriva a un prototipo 1:1; gli altri cambiano scala (la città) e sostituiscono i giocatori con regole o reti.

| Aspetto | Oikos (2017–19) | Meta London (2023–24) | UpBridge / VertiCity (Day 1, 2026) | Make No Little Plans (Day 2, 2026) |
|---|---|---|---|---|
| Scala | Torre residenziale | Quartiere, West Ham | Distretto; Thamesmead/Barking, Swansea | Città, Milton Keynes |
| Problema | Affitto/proprietà, solo/condiviso | Densità lungo il trasporto | Industria, ricerca, data center | Startup tecnologiche |
| Giocatori | Persone in VR + 4 tipi di agenti | 4 sviluppatori + 1 pubblico | 2 agenti | 2 agenti |
| Decisione | Scelte umane, poi agenti a regole | Regole greedy a turni | RL multi-agente (PPO) | Nash/minimax, latente, Q-learning |
| Dati | 80 partite reali, clustering | Nessuno: regole a mano | Episodi simulati | Episodi simulati |
| Valutazione | Soddisfazione, condivise, affitto, costo | Ricavi, luce, valore dei voxel | Reward cumulata | Agency score, posti di lavoro |
| Forma | Ottaedri troncati, film di sapone | Tile, torri cilindriche | Autoencoder su SDF | MLP-SDF, grammatica SDF |
| Fabbricazione | Filo caldo robotico, prototipo 1:1 | Modelli fisici in scala | Casseri 3D | Statica grafica 3D |

Tre critiche tornano in tutti i progetti: repertorio formale uniforme, regole del gioco poco esposte e tempo dichiarato ma non mostrato. Oikos ha però un vantaggio che i progetti successivi perdono: i dati vengono da persone, non da agenti che giocano contro se stessi.

## Valutazione critica

Oikos è coerente dall'inizio alla fine e verifica le sue idee nella materia; il limite è che i dati sociali raccolti con cura non arrivano davvero a decidere la forma.

**Cosa funziona**

- Il gioco come strumento di progetto partecipato: l'abitante diventa coautore e le sue scelte diventano dati misurabili (pp. 102–103).
- Dati da persone reali: 80 partite e quattro profili riconoscibili, una base più solida di agenti inventati (pp. 104–106).
- Forma e fabbricazione legate: il form finding e le superfici rigate nascono dal vincolo del filo caldo (pp. 124, 164).
- Prototipo 1:1: la ricerca esce dal render (pp. 200–212).

**Problemi aperti**

- **Dai dati alla forma manca un passaggio.** Il diagramma di flusso (p. 107) collega gioco e progetto con frecce grigie: le simulazioni producono indici, non geometrie.
- **Il conflitto economico resta un punteggio.** Affitto contro proprietà diventa la percentuale "unità in affitto"; mancano chi possiede la struttura e come si scambiano le unità.
- **Indici non confrontati.** Quattro indicatori per scenario, ma nessun criterio per dire quale mix sia migliore né una serie di scenari a confronto (p. 109).
- **Il tempo è dichiarato, non mostrato.** La tesi parla di adattamento continuo, ma le immagini finali mostrano una configurazione ferma.
- **Repertorio formale uniforme.** Trenta tipi di unità con lo stesso linguaggio bianco e organico: la libertà dell'utente sta nell'aggregazione e negli interni.
- **Dal padiglione alla torre.** Il prototipo in EPS prova la tecnica, non struttura, involucro e impianti di un edificio abitato.

**Spunti**

- Mostrare una griglia di scenari (mix di agenti × indici) e scegliere quello migliore con un criterio esplicito.
- Far scrivere agli agenti la geometria: il cluster "investitore" che genera unità da affittare, la "famiglia" che chiede più stanze vicine.
- Simulare la torre nel tempo: cosa succede quando uno studente diventa famiglia o un investitore vende.

## Fonti

- [AADRL 17/19, Nahmad Bhooshan Studio, Team Oikos (Issuu)](https://issuu.com/c_tz/docs/oikos_final_book), libro di 224 pagine, letto sulle pagine indicate il 19 ottobre 2026. Stato: `da verificare` (testo non estraibile, parafrasi).
- [Analisi di Meta London (2023–24)](https://claude.ai/code/artifact/d394c35a-b5fa-4399-9311-0cbc7063c58f). Vedi `04_AADRL_Meta_London_Bhooshan_Studio.md`.
- [Analisi del Day 1 (2026)](https://claude.ai/code/artifact/16c9875c-a5a1-4cbd-8a76-a99826cf1508). Vedi `01_AA_DRL_Phase_II_Day1_Bhooshan.md`.
- [Analisi del Day 2 (2026)](https://claude.ai/code/artifact/305b60f6-30a7-43d2-a3a9-b77ce03843f4). Vedi `02_AA_DRL_Phase_II_Day2_Bhooshan_Make_No_Little_Plans.md`.
- [Bhooshan Lab, AA DRL](https://drl.aaschool.ac.uk/bhooshan-lab). Stato: `da verificare` in questa sessione.
