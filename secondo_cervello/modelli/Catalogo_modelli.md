# Catalogo dei modelli matematici, filosofici, economici e di IA

Data: 2026-10-20. Raccoglie in un solo file i modelli incontrati finora nel progetto. È un catalogo di lavoro, non un capitolo di tesi.

**Fonti spogliate.**
- `03_Analisi Approfondite/` 00–36, in particolare 02, 04, 12, 13, 20, 21, 22, 26 e 28–36.
- `tesi_out/ricerche_teoriche/`: `Studio_modelli_con_esempi.md`, `Cronistoria_e_correlazioni_modelli.md`, `Analisi_approfondite_per_teoria.md`, `Verifiche_testi_primari.md`.

Per formule ed esempi svolti rimando a `Studio_modelli_con_esempi.md`. Questo file non li ricopia.

**Legenda di affidabilità** (la stessa dei file di ricerca):
- **[V]** verificato sul testo primario, oppure dato riportato dalla fonte di progetto e controllato nel file di analisi.
- **[S]** formalismo standard, o dato ancora da controllare sul testo primario prima di citarlo.
- **[I]** interpretazione o ricostruzione: non è un dato della fonte.
- **[L]** lacuna: niente di verificato.

**Avvertenze di metodo.**
1. Lo stato di ogni voce è quello assegnato dai file di analisi e di ricerca. Per questo catalogo non ho riaperto PDF, video o pagine web.
2. Le formule delle analisi 29–33 (AADRL, Bhooshan e Spyropoulos) non vengono dai progetti. Le ha ricostruite l'autore dell'artifact come forma standard del metodo nominato nel video o nel libro, e i file stessi le dichiarano "inferenza". Qui sono quindi [I] se applicate al progetto, [S] come formalismo generale.
3. Dove due file del progetto si contraddicono, la voce lo segnala ed è riassunta nella sezione 6.

---

## Indice

1. Modelli matematici e computazionali
2. Modelli filosofici e teorici
3. Modelli economici e di teoria dei giochi
4. Modelli di IA e apprendimento automatico
5. Indici e coefficienti di progetto con valori dichiarati
6. Discrepanze tra i file del progetto
7. Indice incrociato per fonte
8. Lacune principali

---

## 1. Modelli matematici e computazionali

### 1.1 Sistemi dinamici e campi

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Sistema aperto e stato stazionario (Bertalanffy) | Un sistema che scambia materia ed energia con l'ambiente può restare stabile senza essere fermo | dX/dt = f(X, U, t); stato stazionario quando f(X*, U*) = 0 | Studio §1; Analisi per teoria | Bertalanffy, *Nature* 1949 (letto); *Science* 111, 1950 (non raggiunto) | Sistemi aperti [V] su *Nature* 1949; formula [S] |
| Equifinalità | Lo stesso stato finale si raggiunge da condizioni iniziali diverse | — | Studio §1 | Bertalanffy 1950 | [S]: non compare nella recensione del 1949 |
| Crescita asintotica (Bertalanffy) | La crescita rallenta avvicinandosi a una dimensione massima | dL/dt = k(L∞ − L); L(t) = L∞(1 − e^(−k(t−t₀))) | Studio §2 | Bertalanffy, *Human Biology* 1957 | [S]: testo non raggiunto |
| Reazione-diffusione (Gray-Scott) | Due sostanze che diffondono e reagiscono generano macchie, strisce o labirinti | ∂u/∂t = D_u∇²u − uv² + F(1−u); ∂v/∂t = D_v∇²v + uv² − (F+k)v; parametri F, k; 25 run dichiarate | Analisi 33 (Team Robotic) | Video DRL Day 1 (5:22–5:25) | Uso [V] da trascrizione non riverificata; il nome Gray-Scott è [I] perché il video non lo cita; formula [S] |
| Laplaciano discreto su griglia | Il campo di una cella è influenzato dalle quattro celle vicine | ∇²u ≈ u(i+1,j) + u(i−1,j) + u(i,j+1) + u(i,j−1) − 4u(i,j) | Analisi 33 | — | [S] |
| Physarum (slime mold, modello di Tero) | Tubi che si rinforzano con il flusso e si atrofizzano senza: ne emergono reti vicine ai percorsi minimi | dD/dt = f(\|Q\|) − μD; Q = (D/L)(p_i − p_j) | Analisi 32 (Meta London); 36 (Eco Stack, RC14) | Video Meta London; pagine RC14 | Uso [V] nelle fonti di progetto; formula [S] (Tero et al., da verificare) |
| Campo di valore del suolo e gradiente | Valore del suolo che decade con la distanza dagli hub; il gradiente orienta lotti ed edifici | V(p) = Σ wᵢ e^(−d(p,hᵢ)/λᵢ); campo vettoriale ∇V | Analisi 29 (UpBridge, VertiCity) | Video DRL Day 1 | Uso dei campi [V] (trascrizione); forma della formula [I] |
| Paesaggio energetico geometrico | Campo scalare da cui la forma emerge per minimizzazione | E(p) = −w_L L − w_Q Q − w_G G + w_C C, con L valore fondiario, Q qualità della vita, G verde, C costo opportunità | Analisi 28 (Bhooshan Lab, agenda); 30 (Make No Little Plans) | Pagina bhooshan-lab; video DRL Day 2 | Concetto [V], solo descrizione verbale; formula [I] |
| Attrattore di scala e porosità | L'altezza varia con la distanza dall'attrattore | h(d) = h₀ + Δh·e^(−d/λ), tra 16 e 120 m | Analisi 30 | Video DRL Day 2 | Intervallo 16–120 m dal video, non riverificato [S]; formula [I] |
| Sistema dipendente dal percorso | Stesse regole con semi diversi producono città diverse | — | Analisi 32 | Video Meta London | [V] da trascrizione; la lettura come sistema dinamico è [I] |

### 1.2 Automi cellulari, vicinati e regole locali

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Vicinato di von Neumann | Le quattro celle ortogonali, più il centro se incluso | N = {(0,0), (±1,0), (0,±1)} | Studio §5; Cronistoria cap. 3 | von Neumann e Burks 1966 | [V]: "a cell and the four cells with which it shares boundaries" |
| Vicinato di Moore | Le otto celle della griglia 3×3, più il centro se incluso | N = {(i,j): \|i\|, \|j\| ≤ 1} | Studio §5 | Convenzione | [V] come convenzione; il nome attribuito a E. F. Moore è [S] |
| Numero di regole possibili | Lo spazio delle regole esplode con la dimensione del vicinato | 2^(2^k): 2^32 con k = 5, 2^512 con k = 9 (due stati) | Studio §5 | — | [S] |
| Game of Life (Conway) | Regola totalistica sul vicinato di Moore | B3/S23 | Studio §5; Analisi 31 (esercizio di Oikos, p. 66) | Conway | [S] |
| Regola 90 | Automa 1D: il nuovo stato è lo XOR dei due vicini; genera un triangolo di Sierpiński | nuovo = sinistra XOR destra | Studio §6 | — | Esempio didattico [I] |
| Automa autoriproducente di von Neumann | Costruttore universale con nastro di descrizione, che copia anche il nastro | 29 stati per cella, vicinato a 5 celle | Studio §7; Cronistoria cap. 3 | von Neumann e Burks 1966 | [V] (Verifiche) |
| Semplificazione di Codd | Automa autoriproducente con meno stati | 8 stati | Studio §7 | Codd 1968 | [S]/[L]: non verificato |
| Loop di Langton | Loop autoriproducente minimo. La costruzione universale è sufficiente ma non necessaria per l'autoriproduzione | — | Studio §7 | Langton 1984, *Physica D* 10 | [V] su abstract; la tesi è di Langton, non di von Neumann |
| Teorema del Giardino dell'Eden (Moore-Myhill) | Un automa è suriettivo se e solo se è pre-iniettivo; un Eden è una configurazione senza predecessori | — | Studio §8 | Moore 1962; Myhill 1963 | [S]; la formulazione "localmente iniettivo ⟺ suriettivo" è scartata |
| Aggregazione esagonale a regole (Oikos) | Crescita locale su griglia esagonale (ottaedro troncato) | Tre parametri: direzione, figli massimi k_max, vicini massimi n_max | Analisi 31 | Libro *Oikos*, p. 85 (parafrasi da Issuu) | Parametri [S], letti su pagine non estraibili; formula [I] |
| Automaton Game ((w)Ego) | Celle che si espandono, si fermano o arretrano secondo la densità vicina e soglie di vicinato | Soglie non riportate | Analisi 20 | *(w)Ego*, The Why Factory 2017 | [V] come descrizione; soglie [L] |
| Agenti a regola locale stile formica di Langton (TetrAgora) | Assemblaggio collettivo a regole locali | 800 "builder", wandering pari a zero | Analisi 34 | Pagina TetrAgora, Bartlett 2026 | [V] (dato di fonte); le regole non sono riportate [L] |
| Wave Function Collapse in un MDP (Spatial Assembly) | Generazione procedurale in cui le transizioni di stato sono definite dal WFC | Nessuna formula | Analisi 34 | arXiv 2101.07579 | [V], solo descrizione |

### 1.3 Ottimizzazione e ricerca nello spazio delle soluzioni

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Spazio delle soluzioni a voxel (OptiMixer) | Ogni voxel ospita una sola funzione | 2^(2·2·1) = 16 nel caso minimo; 8^50.000 per 100×100×5 voxel con 8 funzioni | Analisi 22 | Dekkers, *OptiMixer2_14.pdf* (in `TESI/02_MVRDV Research`) | [V] secondo l'analisi; da ricontrollare sul PDF [S] |
| Fitness multi-obiettivo pesata (OptiMixer) | Somma pesata di punteggi parziali; i pesi sono slider in mano al progettista | f(s) = Σ λᵢ fᵢ(s). Criteri: diversità, costo di costruzione, luce, rumore, vista | Analisi 22 | Dekkers, OptiMixer | [V] secondo l'analisi; valori dei λ [L] |
| Local Search contro Simulated Annealing | La ricerca locale si blocca negli ottimi locali; il simulated annealing può uscirne | Schedule di temperatura non riportato | Analisi 22 | Dekkers, OptiMixer | [V] come confronto; parametri [L] |
| Mappe di influenza e di accumulo | Rumore e ombra che decadono con la distanza | Legge di decadimento non riportata | Analisi 22; file `NoiseMap`, `ShadowMap` nella cartella TESI | OptiMixer | [V] come esistenza; legge [L] |
| Algoritmo genetico multi-obiettivo | Evoluzione di layout su griglia | Nessun parametro | Analisi 35 (Civic Matrix, RC10 2025); 36 (Wallacei, circa 8 progetti RC14) | Pagine Bartlett | [V] (menzione); parametri [L] |
| Circle packing (VertiCity) | Lotti come cerchi che non si sovrappongono | \|cᵢ − cⱼ\| ≥ rᵢ + rⱼ | Analisi 29 | Video DRL Day 1 | Uso [V] (trascrizione); vincolo [S] |
| Packing e scoring (TetrAgora) | Criteri: aderenza al brief, compattezza, spazio residuo | Pesi non riportati; seed "multiple" | Analisi 34 | Pagina TetrAgora | [V]; pesi [L] |
| Scenario max-min (Meta London) | Lo scenario "vincente" è quello che massimizza il ricavo minimo | scenario* = argmax_s min_i R_i(s) | Analisi 32 | Video Meta London | Criterio a parole [V]; formula [I] |

### 1.4 Geometria, grafi e statica

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Albero contro semireticolo (Alexander) | Strutture di insiemi: l'albero non ammette sovrapposizioni, il semireticolo sì | Due insiemi che si sovrappongono: la loro intersezione appartiene alla struttura | Analisi 04; arricchimento visivo 01 | Alexander, *A City is not a Tree*, 1965 | [V] (PDF nella cartella TESI) |
| Decomposizione del grafo dei misfit (Alexander) | I requisiti sono nodi di un grafo di interazioni, scomposto in sottoinsiemi poco connessi | Formula non riportata nell'analisi | Analisi 26 | Alexander, *Notes on the Synthesis of Form*, 1964 | Concetto [V] nell'analisi; formalismo [L] perché l'analisi non lo riporta |
| Signed Distance Fields (SDF) | La forma è il livello zero di una funzione, negativa dentro e positiva fuori | f(A∪B) = min(f_A, f_B); f(A∖B) = max(f_A, −f_B); smin_k(a,b) = −k ln(e^(−a/k) + e^(−b/k)) | Analisi 29, 30; 34 e 35 (Re-Rock) | Video DRL; pagina Re-Rock | Uso [V]; formule [S] |
| Statica grafica 3D | Diagrammi di forma e di forza reciproci: ogni asta è perpendicolare a una faccia, l'area della faccia dà la forza | e_ij ∥ n_f; F_ij = A_f | Analisi 30; 35 (Lithic Pulse) | Video DRL Day 2; pagina Lithic Pulse | Uso [V]; formula [S] (ricerca Block Research Group, da citare) |
| Superfici minime e form finding | Film di sapone con curvatura media nulla; rilassamento digitale a molle | H = 0 | Analisi 31 (pp. 122–125); 35 (AIRS, Re-Rock) | *Oikos*; pagine Bartlett | [S] |
| Superfici rigate (filo caldo) | Il filo è un segmento, quindi taglia solo superfici rigate | r(u,v) = (1−v)a(u) + v·b(u) | Analisi 31 (pp. 162–176); 35 (AIRS) | *Oikos*; pagina AIRS | [S] |
| Origami rigido e pieghe curve | Grammatica a regole di piegatura | — | Analisi 35 (Crease Cell, FlexFold) | Pagine RC10 | [V] (menzione) |
| Voronoi, Delaunay, asse mediale | Suddivisione di lastre in stanze; partizionatori Voronoi negli agenti | — | Analisi 13; 30; 36 | Veloso et al. 2017; video DRL; RC14 | [V] (menzione); [S] |
| Space Syntax e VGA | Integrazione, scelta, angular step depth, isovist | Software Depthmap | Analisi 36 (circa 16 progetti RC14) | Pagine RC14 | [V] (menzione) |
| Campi tensoriali e computazione del vuoto (Assembler) | Unità discrete, relazioni sintattiche e campi di dati | Nessuna formula | Analisi 17 | Erioli 2023 (PDF nella cartella TESI) | [V] come concetto; algoritmo [L] (vedi la voce del 20/10 sul tool Assembler in `stato_avanzamento.md`) |

### 1.5 Probabilità e informazione

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Catene di Markov | Lo stato presente determina la probabilità di passare agli stati futuri | — | Analisi 02 | Pask, *An Approach to Cybernetics*, 1961 | [V] nell'analisi; formalismo [S] |
| Teoria dell'informazione (Shannon) | Ponte tra varietà e informazione; Ashby lega la sua legge al teorema di Shannon sul canale di correzione | — | Analisi 02; Cronistoria cap. 2 | Shannon e Weaver 1949; Ashby 1956 | [S] (confermato solo su fonte secondaria) |

---

## 2. Modelli filosofici e teorici

| Modello | Definizione breve | Formula o struttura | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Teoria generale dei sistemi (GST) | Programma di isomorfismi tra discipline | — | Cronistoria cap. 1 | Bertalanffy | [S]; "fondamento di tutte le scienze dei sistemi" è scartato |
| Varietà (Ashby) | Numero di stati distinguibili, o il suo logaritmo in bit | V = \|S\| oppure log₂\|S\| | Studio §3; Analisi 02 | Ashby 1956, pp. 125–126 | [S]: pagine non lette (vedi sezione 6) |
| Legge della varietà richiesta | Solo un regolatore con varietà sufficiente può contenere le perturbazioni | V(O) ≥ V(D) − V(R); necessaria, non sufficiente | Studio §3; Analisi 02 (via Pask); 07 | Ashby 1956, cap. 11 | [S]; la massima "only variety can destroy variety" va controllata [S] |
| Regolazione come gioco a due (Ashby) | Il disturbo sceglie la riga, il regolatore la colonna, la cella è l'esito | Tabella, senza payoff | Studio §3 | Ashby 1956, p. 202 | [S]: pagina non letta. Ashby non usa la teoria dei giochi di von Neumann [I] |
| Good regulator (Conant e Ashby) | Un buon regolatore contiene un modello del sistema che regola | Isomorfismo regolatore-modello | Studio §4 | Conant e Ashby 1970, *Int. J. Systems Science* | [S] |
| Sistema auto-organizzante; linguaggio oggetto e metalinguaggio (Pask) | Il sistema cambia le proprie regole, non solo il proprio stato | — | Analisi 02 | Pask 1961 | [V] (PDF nella cartella TESI) |
| SAKI (macchina per insegnare adattiva) | Regola il ritmo e gli aiuti in base agli errori dell'allievo | Varietà calibrata sull'allievo | Analisi 02; 07 | Pask 1961 | [V] |
| Architettura a obiettivo aperto, ambiente mutualistico (Pask) | L'edificio come sistema in conversazione con chi lo usa | — | Analisi 03; arricchimento 00_Pask | Pask 1969 | [V] (PDF nella cartella TESI) |
| Goodness of fit e misfit (Alexander) | Il progetto azzera gli attriti tra forma e contesto | Misfit = 0 come obiettivo | Analisi 26 | Alexander 1964 | [V] nell'analisi (testo non presente nella cartella TESI) |
| Sistemi che generano sistemi (Alexander) | Il progettista disegna il kit di parti e regole, non l'oggetto | — | Analisi 01; arricchimento 00_Alexander | Alexander 1968 | [V] (PDF nella cartella TESI) |
| Stigmergia | Il coordinamento passa per la struttura costruita, non per la comunicazione diretta; deposito di feromone, diffusione ed evaporazione | Tassi di diffusione ed evaporazione non quantificati nell'analisi | Analisi 12; arricchimento 05_Meyboom | Meyboom e Reeves 2013 (PDF nella cartella TESI) | [V] come meccanismo; coefficienti [L] |
| Tassonomia dei sistemi multi-agente nello space planning | Agenti come unità mobili, agenti occupanti, partizionatori | — | Analisi 13 | Veloso, Rhee, Krishnamurti 2017 | [V] (PDF nella cartella TESI) |
| Mereologia e dipendenza (Husserl, nella ricostruzione di Smith e Mulligan) | Parte-tutto, dipendenza (fondazione), confine e contatto | P riflessiva, antisimmetrica, transitiva | Studio §12; Cronistoria cap. 6 | Smith e Mulligan 1983, *Topoi*; Husserl, *Ricerche logiche* III | Tripartizione [V] (abstract); assiomi [S]; Husserl non letto [L] |
| Mereologia politica: partitioning contro partaking | Le parti discrete come dispositivo civico di partecipazione | — | Analisi 18 | Koehler 2020 (PDF nella cartella TESI) | [V] come tesi dell'autore |
| Unit operations (Bogost) | Metodo che analizza i media come unità discrete e operazioni, non un modello matematico | — | Studio §11; Analisi 09 (via Sanchez) | Bogost 2006 | Tesi generale [V]; definizione in conflitto, vedi sezione 6 |
| Discreto contro continuo (Carpo) | Dalla formula compressa alla correlazione statistica e al "chunky" | — | Analisi 08 | Carpo 2023 | [V] come tesi dell'autore |
| Retroazione reticolare forma-uso (De Carlo) | Progetto come processo continuo di retroazioni con gli abitanti | — | Analisi 24 | De Carlo 1971–73 | [V] come tesi dell'autore; nessuna formalizzazione |
| Città come sistema termodinamico aperto (Entropia) | Il territorio sopravvive importando negentropia; l'energia è la moneta di scambio | Cinque forme di energia; bilancio netto negativo porta al collasso | Analisi 21 | van Bilsen, Batstra, Pinilla in *SpaceFighter* 2007, pp. 32–47 | [V] come contenuto del libro; uso di Schrödinger e Prigogine dichiarato, non verificato [S] |
| Memoria artificiale come medium spaziale (Witt) | La memoria macchina nasce come problema di spazio e di riconfigurazione | — | Analisi 25 | Witt, *Khōrein* IV(1), 2026 | [V] come tesi dell'autore |

---

## 3. Modelli economici e di teoria dei giochi

| Modello | Definizione breve | Formula o coefficienti | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Equilibrio di Nash | Nessun giocatore migliora cambiando da solo strategia | u_i(σ*_i, σ*_−i) ≥ u_i(σ_i, σ*_−i) | Studio §9; Cronistoria cap. 4; Analisi 21, 29, 30, 31 | Nash 1951, *Annals of Mathematics* 54(2), p. 287 | [V] |
| Teorema di esistenza | Ogni gioco finito ha un equilibrio in strategie miste (Brouwer nel 1951, Kakutani nel 1950) | — | Studio §9 | Nash 1951, Teorema 1 | [V] |
| Gioco non cooperativo | Ogni giocatore agisce senza coalizioni né comunicazione | — | Studio §9; Verifiche | Nash 1951, p. 286 | [V] |
| Dilemma del prigioniero | L'equilibrio (D, D) è peggiore di (C, C) | T > R > P > S; esempio (3,3), (0,5), (5,0), (1,1) | Studio §9; Analisi 29 (UpBridge, 0:14:28) | Standard | [S]; uso nel progetto [V] da trascrizione non riverificata |
| "Nash negativo" e cambio delle regole (UpBridge) | Il collasso della policy RL viene corretto cambiando il gioco, non i giocatori | — | Analisi 29 | Video DRL Day 1 | Uso [V] (trascrizione); la lettura è [I] |
| Strategie miste: pari o dispari | Nessun equilibrio puro; quello misto è (½, ½) | q = 1/2 | Studio §9 | — | [I] (esempio svolto) |
| Minimax di von Neumann | Nel gioco a somma zero tra due giocatori, max-min = min-max | v = max_x min_y u(x,y) | Studio §10; Analisi 30 | von Neumann 1928 | [S] |
| Somma zero dichiarata con obiettivo win-win (Make No Little Plans) | Il team dichiara un gioco a somma zero ma cerca un esito win-win | — | Analisi 30 | Video DRL Day 2 | Contraddizione segnalata nell'analisi [I]; da verificare sul video |
| Teoria dei giochi spaziale (SpaceFighter) | La città come matrice di payoff tra attori; strategie evolutivamente stabili | Nessuna matrice numerica riportata | Analisi 21 | *SpaceFighter* 2007 (cita Nash, Maynard Smith, Schelling) | [V] come contenuto; matrici [L] |
| Micromotivi e macrocomportamento (Schelling) | Scelte individuali aggregate producono esiti collettivi non voluti | — | Analisi 21 | Schelling, *Micromotives and Macrobehavior* | [S]: citato tramite SpaceFighter, non letto |
| Tassa energetica compensativa (SpaceFighter) | Chi inquina paga crediti energetici che finanziano parchi e trasporti | Calcolo non riportato | Analisi 21 | *SpaceFighter* 2007 | [V] come descrizione; formula [L] |
| Gioco a turni con funzioni di ricavo (Meta London) | Ogni giocatore occupa il voxel col ricavo locale migliore; le tasse finanziano il giocatore pubblico | R_i(x) = Σ w_ik φ_k(x) − c(x); T = τ Σ R_i | Analisi 32 | Video Meta London | Regole [V] (trascrizione); formula [I]; dinamica di best response [I] |
| Gioco simultaneo con interferenza (Oikos) | Quattro giocatori in simultanea; una collisione annulla il punto | v_i(s) ∈ {1, 2, 4}; con collisione v = 0 | Analisi 31 (p. 50) | *Oikos* | Valori [S] (parafrasi di pagine non estraibili); formula [I] |
| Costo dell'unità (Oikos) | Il costo dipende da sbalzo, vista, luce e altezza, e cala con i vicini | C(u) = C₀ + α·sbalzo + β·vista + γ·luce + δ·h − ε·\|N_occ\| | Analisi 31 (pp. 90–91) | *Oikos* | Fattori [S]; formula e pesi [I] |
| Quattro motori di gioco ((w)Ego) | Blind, Trading, Automaton e Strategic: quattro modi di risolvere le collisioni | Vedi Satisfaction Score (§5) | Analisi 20 | *(w)Ego* 2017 | [V] come contenuto del libro |
| Agenti negoziali (ANIMA) | Ogni agente rappresenta i bisogni di un utente e negozia il layout | Nessuna formula | Analisi 34 | Pagina ANIMA, Bartlett 2024 | [V]; meccanismo [L] |
| Allocazione a "pixel" con teoria dei giochi (InterX) | Teoria dei giochi applicata all'allocazione sul sito | — | Analisi 35 | Pagina InterX, RC10 2024 | [V] (menzione); modello [L] |
| Gioco cooperativo Stato-mercato (modello Shenzhen) | Riferimento di scenario per UpBridge | — | Analisi 29 | Video DRL Day 1 | [V] (trascrizione) come dichiarazione del team |

---

## 4. Modelli di IA e apprendimento automatico

| Modello | Tipo | Formula, dati o parametri | Dove compare | Fonte originale | Stato |
|---|---|---|---|---|---|
| Processo decisionale di Markov (UpBridge) | Formulazione per RL | Passo = un mese; stato = mappa, prezzi, fondi; azione = edificio e lotto, oppure passare; reward = rendimento meno costo | Analisi 29 | Video DRL Day 1 | [V] (trascrizione non riverificata) |
| Proximal Policy Optimization (PPO) | Policy gradient | L^CLIP = E[min(r_t·Â_t, clip(r_t, 1−ε, 1+ε)·Â_t)] | Analisi 29 (UpBridge); 34 (Spatial Assembly, arXiv 2101.07579) | Video DRL; arXiv 2101.07579 | Uso [V]; formula [S]; iperparametri [L] |
| Agente LLM actor-reflector contro PPO | Confronto tra agenti | — | Analisi 29 | Video DRL Day 1 | [V] (trascrizione) |
| RL multi-agente (da reward congiunta a reward separate) | Gioco stocastico multi-agente | r₁ + r₂ diventa due obiettivi distinti | Analisi 29; 34 (DMARL, IRAAS) | Video DRL; UCL Discovery 10200300, 10165846 | [V] (solo abstract e trascrizione); la lettura come gioco stocastico è [I] |
| Q-learning | RL basato sul valore | Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') − Q(s,a)] | Analisi 30 | Video DRL Day 2 | Uso [V]; formula [S]; α e γ [L] |
| Self-play e tree search (Spatial Assembly) | Auto-gioco "fino a convergenza" | Criterio di convergenza non definito; la tree search compare solo nel titolo | Analisi 34 | arXiv 2101.07579 | [V] |
| Ricompensa per stabilità | Reward da spostamento massimo in Unity3D | Nessun valore | Analisi 34 | arXiv 2101.07579 | [V], solo a parole |
| RL in altri progetti RC3 (ANIMA, Autopoesis, TetrAgora) | Navigazione, reward e penalità, assemblaggio reversibile | Algoritmi e reward non riportati | Analisi 34 | Pagine Bartlett 2024–2026 | [V]; dettagli [L] |
| Autoencoder MLP su SDF | Compressione e ricostruzione di piante | Loss = (1/N)Σ‖f(pᵢ) − D(E(f))(pᵢ)‖²; blending z = (1−t)z₁ + t·z₂ | Analisi 29, 30 | Video DRL | Uso [V]; formule [S] |
| Codifica posizionale | Permette all'MLP di rendere dettagli ad alta frequenza | γ(p) = (sin 2^k πp, cos 2^k πp), con k = 0…L−1 | Analisi 29 | Video DRL Day 1 | Uso [V]; formula [S] |
| Direzioni semantiche nel latente | z + αv produce una trasformazione riconoscibile della pianta | — | Analisi 29 | Video DRL Day 1 | [V] (trascrizione); formula [I] |
| Graph autoencoder (Civic Canvas) | Addestrato sulle scelte dei giocatori, con PCA del latente | Dataset dai giocatori | Analisi 35 | Pagina RC10 2025 | [V] (dataset e loss mostrati nelle tavole) |
| "Diffuser" (Horizon) | Probabilmente un modello di diffusione su piante, con punteggio a grafo nel ciclo di training | Regole di adiacenza ✓/✗ | Analisi 35 | Pagina RC10 2024 | Esistenza [V]; tipo di modello [I] |
| Segmentazione semantica (Urban Sutures) | Rete di visione su maschere di facciata | Dataset di maschere a classi | Analisi 35 | Pagina RC10 2026 | [V] |
| Modello su dataset di piante che genera grafi (Meta-CLT) | Generativo su grafi | Dettagli non mostrati | Analisi 35 | Pagina RC10 2025 | [V] (dichiarazione); dettagli [L] |
| LLM come interfaccia (Civic Matrix, UtopiaLab) | Dalle abitudini al layout; vicini virtuali NPC con personalità MBTI | — | Analisi 35 | Pagine RC10 2025 | [V] (menzione) |
| VLM "di secondo ordine" e agenti LLM osservatori (Team Robotic) | Decisione del robot tradotta in comandi JSON; voto sui parametri (F, k) | Aggregazione (F,k) = (1/N)Σ(Fᵢ,kᵢ); regola reale non specificata | Analisi 33 | Video DRL Day 1 | Uso [V] (trascrizione); regola di aggregazione [I] |
| YOLO | Rilevamento di oggetti con CNN | Modello addestrato dal team per riconoscere gli altri robot | Analisi 33 | Video DRL Day 1 | [V] (trascrizione) |
| Spazio latente delle configurazioni (Team Robotic) | Proiezione di configurazioni registrate | 150 configurazioni | Analisi 33 | Video DRL Day 1 | [V] (trascrizione) |
| K-means sui giocatori (Oikos) | Clustering di 80 partite in 4 profili | min Σ min_j ‖xᵢ − μ_j‖², k = 4; il libro non nomina l'algoritmo | Analisi 31 (pp. 104–105) | *Oikos* | 80 partite e 4 gruppi [S]; k-means [I] |
| Pipeline RC14: PCA, t-SNE, K-Means, DBSCAN, SOM | Riduzione delle dimensioni e clustering di dati urbani aperti | Circa 20 progetti su 32 per ciascuna delle due famiglie | Analisi 36 | Bartlett Show Index, RC14 2020–2026 | [V]; i conteggi sono indicativi |
| Pix2Pix, GAN, 3D GAN, Stable Diffusion | Modelli generativi di immagini | Circa 15 progetti su 32 | Analisi 36 | RC14 | [V]; i conteggi sono indicativi |
| CNN, pose detection, RNN, word2vec, sentiment analysis | Visione artificiale e linguaggio | Rispettivamente circa 4 e circa 3 progetti | Analisi 36 | RC14 | [V] |
| Simulazione ad agenti | Pedoni, flussi, comportamento dei cittadini | — | Analisi 28 (Meta Cities); 32; 36 (circa 13 progetti) | Pagine DRL e RC14 | [V] (menzione) |
| Decision tree (Meta Cities) | Strumento di modellazione | Non riportato | Analisi 28 | Pagina metacities | [V] (menzione) |
| "Learning systems", "data-driven design" (agende DRL 2026) | Tecnica non specificata | — | Analisi 28 | Pagine bhooshan-lab e angiuslab | [V] come termine; tecnica [L] |
| Machine learning contro il bias antropocentrico (RC10) | Non specificato | — | Analisi 34 | Pagina cluster AD MArch | [V], solo descrizione |

---

## 5. Indici e coefficienti di progetto con valori dichiarati

Questa sezione riporta solo valori scritti nelle fonti.

| Indice o coefficiente | Valore | Contesto | Fonte (analisi) | Stato |
|---|---|---|---|---|
| Compression Safety Index (CSI) | CSI = A_p · f_c · φ / N_p; valori non riportati | Tessellated Biomes | 34; arXiv 2606.20647 | Formula [V]; valori [L] |
| Volume Coverage | N_occ / N_total | Tessellated Biomes | 34; arXiv 2606.20647 | [V] |
| Structural Connectivity Index | Somma pesata di grado medio di contatto, articolazione e frazione a terra; pesi α, β, γ non riportati | Bartlett | 34 | Struttura [V]; pesi [L] |
| Moduli e robot di Tessellated Biomes | Blocchi 5×5×5 cm con incastri da 1,25 cm; robot di 1,45 kg con 12 servo AX-12A; errore sotto 2,5 cm; pendenze fino a 45° | — | 34 | [V] |
| Carico trasportato | Coppia di robot fino a 8,23 kg, dichiarata "2,84 volte il peso"; il conto con 1,45 kg dà circa 5,7 | — | 34 | Incongruenza della fonte, da verificare sul PDF |
| Resistenza a compressione | Calcestruzzo circa 100 kN a 4 mm; quercia rossa circa 54 kN a 9 mm; PLA circa 12 kN a 2 mm | — | 34 | [V] su estrazione automatica, da controllare |
| Combinazioni di TetrAgora | 9 geometrie × 24 rotazioni = 216, contro 303 dichiarate | — | 34 | Scarto non spiegato dalla fonte |
| Dataset di TetrAgora | 160.000 aree di piano reali | — | 34 | [V]; origine del dato [L] |
| Satisfaction Score ((w)Ego) | Blind 75%, Trading 72%, Automaton 65%, Strategic 53% | Aderenza alla "casa dei sogni" | 20 | [V] secondo l'analisi; metodo di misura da ricontrollare sul libro [S] |
| Indicatori di Oikos | Con un mix di 25% investitori e 75% studenti: soddisfazione 72, unità condivise 51, in affitto 46, costo della struttura 39 (su 100) | Simulazione ad agenti | 31 (pp. 108–109) | [S]: parafrasi di pagine non estraibili |
| Profili dei giocatori di Oikos | Studente circa 3 unità, freelance circa 5, famiglia circa 6, investitore circa 8 | Centroidi dei cluster | 31 | [S] |
| Nodi strutturali per tipo di tile (Meta London) | 8 contatti per il commercio, 4 per il verde | Programma → struttura | 32 | [V] (trascrizione) |
| Target di Meta London | Raddoppio di popolazione ed economia in 25 anni | Obiettivo di scenario, non parametro | 28 | [V] |
| Altezze in Make No Little Plans | Da 16 a 120 m | Attrattori | 30 | [S] |
| Automa di von Neumann | 29 stati, vicinato a 5 celle | — | Studio §7 | [V] |

---

## 6. Discrepanze tra i file del progetto

1. **Pagine di Ashby.** `Studio_modelli_con_esempi.md` e `Analisi_approfondite_per_teoria.md` marcano [V] la varietà (pp. 125–126) e la tabella del gioco (p. 202). `Verifiche_testi_primari.md` dice invece che quelle pagine non sono state lette, e la Cronistoria le dà come confermate solo su fonte secondaria. In questo catalogo sono [S]. Prima di citarle vanno lette le pp. 121–125 e 202–213.
2. **"Only variety can destroy variety".** L'analisi 02 la riporta come citazione di Ashby attraverso Pask. La Cronistoria scarta l'attribuzione alla pagina e chiede di controllarla. Resta [S].
3. **Definizione di unit operation.** L'analisi 09 attribuisce a Bogost, attraverso Sanchez, la formula "sistema configurativo di unità discrete interconnesse". La Cronistoria ha scartato come definizione una formulazione quasi identica ("…di unità di significato…"). Non è chiaro se l'errore stia nella ricerca web o nella parafrasi di Sanchez. Va controllato su Bogost 2006 e sul PDF di Sanchez, che è nella cartella TESI.
4. **Vicinato di Moore a nove celle.** La Cronistoria scarta come "definizione standard" la versione con il centro incluso. Studio e Analisi per teoria la presentano come convenzione. La differenza è solo di formulazione, ma in tesi la convenzione va dichiarata.
5. **Formule AADRL.** Le analisi 29–33 sono state copiate da artifact con formule ricostruite. Non vanno citate come formule dei team.

---

## 7. Indice incrociato per fonte

| File del progetto | Modelli (sezione del catalogo) |
|---|---|
| Analisi 01 Alexander, *Systems Generating Systems* | Sistemi che generano sistemi (2) |
| Analisi 02 Pask, *An Approach to Cybernetics* | Varietà e legge di Ashby, Markov, auto-organizzazione, SAKI, Shannon (1.5, 2) |
| Analisi 03 Pask, *Architectural Relevance* | Architettura a obiettivo aperto (2) |
| Analisi 04 Alexander, *A City is not a Tree* | Albero contro semireticolo (1.4) |
| Analisi 07 Steenson | Pask, SAKI, Fun Palace (2) |
| Analisi 08 Carpo | Discreto contro continuo (2) |
| Analisi 09 Sanchez, *Combinatorial Design* | Unit operations (2, 6) |
| Analisi 12 Meyboom e Reeves | Stigmergia (2) |
| Analisi 13 Veloso et al. | Tassonomia MAS, Voronoi (1.4, 2) |
| Analisi 17 Erioli | Campi tensoriali, computazione del vuoto (1.4) |
| Analisi 18 Koehler | Mereologia politica (2) |
| Analisi 20 *(w)Ego* | Quattro motori di gioco, Automaton Game, Satisfaction Score (1.2, 3, 5) |
| Analisi 21 *SpaceFighter* | Entropia, teoria dei giochi spaziale, Schelling, tassa energetica (2, 3) |
| Analisi 22 *OptiMixer* | Spazio a voxel, fitness pesata, Local Search contro Simulated Annealing, mappe di influenza (1.3) |
| Analisi 24 De Carlo | Retroazione reticolare (2) |
| Analisi 25 Witt | Memoria artificiale (2) |
| Analisi 26 Alexander, *Notes* | Goodness of fit, grafo dei misfit (1.4, 2) |
| Analisi 28 AADRL, ricerca web | Parametricismo, agent-based, decision tree, paesaggi energetici; nessuna formula reperita (1.1, 4, 5) |
| Analisi 29 DRL Day 1 (UpBridge, VertiCity) | Dilemma del prigioniero, MDP, PPO, campi, circle packing, SDF, autoencoder, codifica posizionale (1, 3, 4) |
| Analisi 30 DRL Day 2 (Make No Little Plans) | Minimax, Nash, paesaggio latente, Q-learning, SDF, autoencoder, statica grafica 3D, Voronoi (1, 3, 4) |
| Analisi 31 *Oikos* | Aggregazione esagonale, gioco simultaneo, costo dell'unità, k-means, indicatori, superfici minime e rigate (1, 3, 4, 5) |
| Analisi 32 Meta London | Physarum, gioco a turni, max-min, dipendenza dal percorso (1, 3) |
| Analisi 33 Team Robotic | Gray-Scott, laplaciano, particelle, YOLO, VLM e LLM, latente (1.1, 4) |
| Analisi 34 Bartlett RC3/RC10/RC11/RC14 | CSI, Volume Coverage, PPO, DMARL, WFC, TetrAgora (1, 4, 5) |
| Analisi 35 Bartlett RC10 | Graph autoencoder, Diffuser, segmentazione, LLM, GA, SDF, statica grafica, origami (1, 4) |
| Analisi 36 Bartlett RC14 | PCA, clustering, Space Syntax, GAN, GA, physarum, agenti (1, 4) |
| `Studio_modelli_con_esempi.md` | Bertalanffy, Ashby, good regulator, vicinati, automi, Moore-Myhill, Nash, minimax, Bogost, Husserl (1, 2, 3) |
| `Cronistoria_e_correlazioni_modelli.md` | Storia e stato delle fonti delle stesse teorie (1, 2, 3) |
| `Verifiche_testi_primari.md` | Stato [V] di Nash, von Neumann-Burks, Bertalanffy 1949 (1, 3) |

Analisi non citate perché non contengono modelli formali, almeno nelle parti lette: 05 e 06 (Negroponte), 10 (De Graaf), 11 (Sanchez, *We Have Always Been Parametric*), 14 (HUB Bridges), 15 (Mari), 16 (Murphy), 19 (*Vertical Village*), 23 (*Climatizer*), 27 (Gamma). L'analisi 19 nomina HouseMaker e VillageMaker con coni solari, e la 23 una simulazione biofisica ad attori: le ho lette solo per titoli, quindi vanno riviste se servono come modelli [L]. Le analisi 15 (19 modelli di arredo) e 27 (23 design pattern) contengono "modelli" in senso progettuale, non matematico.

---

## 8. Lacune principali

- **Testi primari da leggere:** Ashby 1956, cap. 7 e 11; Bertalanffy 1950 e 1957; Codd 1968; Moore 1962; von Neumann e Morgenstern 1944; Schelling; Husserl, *Ricerche logiche* III; Smith e Mulligan 1983, dove resta aperta la discrepanza tra *Topoi* 3 e 2(1); Bogost 2006.
- **Progetti AADRL e Bartlett:** nessuna metrica di performance dei modelli di IA, nessun iperparametro, nessuna funzione di reward scritta.
- **MVRDV:** i pesi λ di OptiMixer, lo schedule del simulated annealing, le matrici di payoff di SpaceFighter e le soglie dell'Automaton Game non sono riportati nelle analisi. Il PDF `OptiMixer2_14.pdf` è nella cartella TESI e può chiudere parte di queste lacune.
- **Correlazioni tra teorie:** tutte [I]. Nessun collegamento tra Ashby, Nash, gli automi e Husserl è verificato in letteratura.
