# AA DRL Phase II Day 2: Modelli matematici e AI (focus Shajay Bhooshan)

> **Origine:** artifact Claude Docs `305b60f6-30a7-43d2-a3a9-b77ce03843f4`, letto il 2026-10-19 tramite il connettore. Copia salvata senza modifiche di contenuto; formule e tabelle ricostruite dal formato originale.
> **Fonte primaria:** video "DRL (PG) MArch Phase II Final Presentation (Day 2)", trascrizione completa (8 h, 2.754 segmenti) letta dall'autore dell'artifact. **Non riverificata in questa sessione.**
> **Stato:** `da verificare`. I minuti citati sono quelli del video.
> **Legenda:** le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché la presentazione non mostra le equazioni esatte usate dal team. Sono **inferenza**.

## Sintesi

Il progetto del laboratorio Bhooshan presentato il Day 2 ("Make No Little Plans", tesi *AI for New Cities*, dalle 4:38:21 alle 5:34:05 del video) è una catena di cinque modelli: un gioco a due giocatori con equilibrio di Nash, uno spazio latente e Q-learning per la crescita urbana, un autoencoder MLP su campi di distanza con segno (SDF), una grammatica di forma a campi parametrici, e la statica grafica 3D per la struttura. Il risultato dichiarato è un distretto a Milton Keynes che genera circa 140.000 posti di lavoro.

La giuria lo ha definito "il futuro del lavoro" (Patrick Schumacher) e "un progetto senza conflitto" per la sua procedura totale. Il limite principale emerso: le regole del gioco (benessere, produttività, costi) non sono definite in modo verificabile, e il modello ignora orientamento, ombreggiamento e pluralità di attori.

Le altre cinque presentazioni della giornata usano soprattutto ottimizzazione topologica, agenti e reti a grafo; nessuna integra AI, economia e statica in un'unica pipeline come questa.

## Contesto: DRL Phase II e il Bhooshan Lab

La Phase II Review del DRL (AA School of Architecture) si è svolta l'8–9 gennaio 2026, dopo 16 mesi di lavoro, con quattro studi: Angius, Bhooshan, Schumacher, Spyropoulos ([programma DRL](https://drl.aaschool.ac.uk/phase-2-review-jan-2026)). Il Day 2 ha sei team; quello di Bhooshan presenta alle 14:30.

[Shajay Bhooshan](https://www.zha.com/people/shajay-bhooshan) è Associate Director di Zaha Hadid Architects e co-fondatore di ZHA CODE. Ha un PhD all'ETH Zurigo (Block Research Group) e insegna al DRL dal 2006 (dati dalla pagina ZHA citata, `da verificare`). Da qui viene l'attenzione alla statica grafica e alla geometria strutturale (es. il ponte Striatus).

L'agenda 2026 del [Bhooshan Lab](https://drl.aaschool.ac.uk/bhooshan-lab) è "AI for New Cities": l'AI come strumento per ragionare su ottimizzazione, negoziazione e adattamento, non per generare immagini. L'agenzia del progettista sta "a monte della forma", in due leve:

- **paesaggi energetici geometrici**: campi scalari da cui la forma emerge per minimizzazione;
- **regole di gioco socio-economiche**: l'ordine urbano come equilibrio negoziato tra attori, non come tipologia imposta.

Nel dibattito (5:26:08) Bhooshan stesso inquadra il primo anno dello studio: servono circa 250 nuove città nei prossimi 25 anni, e la domanda è quale problema sia "degno dell'AI" oltre text-to-image e text-to-code. Il team di Day 2 è Palash, Raj, Sham e Taresh.

## Il progetto "Make No Little Plans" passo per passo

Il titolo cita Daniel Burnham (Chicago). La tesi: unire l'ordine civico di Chicago (griglia 100 × 100 m, densità downtown 26.000 ab/miglio², template edilizi) con l'intensità economica della Silicon Valley, su un sito a Milton Keynes (circa 300.000 abitanti, 27–30 alloggi/ha) nell'arco Oxford–Cambridge. La presentazione ha cinque capitoli: Thesis, Game AI, Shape AI, Procedural Buildings, Proposal.

| Minuto | Fotogramma | Cosa mostra |
|---|---|---|
| 4:39:34 | Indice (5 capitoli) | Struttura: Game AI + Shape AI + edifici procedurali |
| 4:43:54 | Phase I | RL su regole di adiacenza, policentri, reti stradali |
| 4:45:39 | Giocatori e azioni | Urban developer vs economic developer, scambio terra/materiali |
| 4:46:48 | Game UI | Mappa valore fondiario, punteggio di adiacenza, fondi dei giocatori |
| 4:47:39 | Spazio latente | Paesaggio di ottimizzazione condiviso sotto vincoli minimax |
| 4:49:24 | Q-learning | "Latent space = corpo, Q-learning = cervello" |
| 4:50:38 | MLP | Autoencoder su piante, ricostruzione SDF |
| 4:52:34 | Campi parametrici | SDF, blending, attrattori, programmi work/visit/live |
| 4:56:03 | Distribuzione centroidi | Punti equidistanti, soglie per feature, altezze 16–120 m |
| 4:57:39 | Duale topologico | Suddivisione della lastra per densità di programma |
| 4:58:52 | Statica grafica 3D | Poliedri forma/forza, copertura a compressione |
| 5:00:29 | Asse mediale | Suddivisione procedurale delle stanze |
| 5:02:03 | Vuoti "force-informed" | Rimozione materiale da relazioni vertice-faccia |
| 5:02:34 | Catalogo | Template edilizi "alla Chicago" |
| 5:03:30 | Distretto finale | 140.000 posti di lavoro dichiarati |
| 5:06:24 | Inizio critica | Giuria: Schumacher, Jan Bunge e altri |

**1. Game AI (4:44–4:50).** Due giocatori: l'urban developer (verde civico, logica Chicago, vuole la stazione) e l'economic developer (cluster di innovazione, logica Silicon Valley, vuole l'autostrada). Le azioni sono reciproche: P1 compra materiali da P2, P2 compra terra da P1. Le mosse sono locali, vincolate da una matrice di adiacenza. Nella Game 1, con mosse casuali, entrambi finiscono in negativo e non c'è convergenza. La Game 2 aggiunge lo spazio latente (valore fondiario, qualità della vita, connettività verde, costo opportunità). La versione finale aggiunge Q-learning per il valore di lungo periodo.

**2. Shape AI (4:50–4:57).** Un MLP comprime piante in uno spazio latente e le ricostruisce come curve SDF; interpolando nel latente si ottengono forme ibride. Poi il team passa a un approccio a regole: campi SDF con operazioni di unione, scala, svuotamento; attrattori locali che alzano gli edifici vicini, aprono vuoti e ritagliano piazze; terrazzamenti dove i volumi si fondono.

**3. Edifici procedurali (4:57–5:03).** Dalla SDF si estrae il contorno della lastra; un duale topologico la suddivide (spazi comuni a grande luce davanti, uffici dietro); moduli da 150 m² (15 persone) e 300 m² (30 persone). La struttura in legno nasce dalla statica grafica 3D: ogni cella è un poliedro chiuso, le aree delle facce sono proporzionali alle forze. Ne derivano mega-copertura, lucernario a telaio reciproco e balconi a sbalzo.

## Modelli matematici

I modelli sotto sono quelli nominati nel video; le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact, perché la presentazione non mostra le equazioni esatte usate dal team. **Inferenza.**

**Teoria dei giochi: minimax e Nash.** Il team cita von Neumann (1928) e Nash (1950). Lo scambio terra/materiali è descritto come gioco a somma zero, in cui ogni giocatore massimizza il guadagno minimo garantito:

$$v = \max_{x \in X} \min_{y \in Y} u_1(x, y), \qquad u_1(x,y) + u_2(x,y) = 0$$

L'obiettivo dichiarato però è "win-win", quindi un equilibrio di Nash in un gioco a somma non nulla: nessun giocatore migliora cambiando da solo strategia.

$$u_i(s_i^*, s_{-i}^*) \ge u_i(s_i, s_{-i}^*) \quad \forall s_i, \; \forall i$$

Qui c'è un'incoerenza concettuale: un gioco a somma zero non può produrre un esito in cui entrambi guadagnano. Il guadagno congiunto deve venire da un termine esterno (es. valore fondiario crescente o "agency score"), che il video non esplicita.

**Paesaggio latente come funzione di costo.** Lo spazio latente combina valore fondiario L, qualità della vita Q, connettività verde G e costo opportunità C. Una lettura plausibile è un campo scalare pesato su cui le mosse locali scendono di gradiente:

$$E(p) = -w_L L(p) - w_Q Q(p) - w_G G(p) + w_C C(p)$$

**Q-learning.** Serve a dare valore alle conseguenze future delle mosse, perché "le città sono irreversibili". Aggiornamento standard:

$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[ r + \gamma \max_{a'} Q(s',a') - Q(s,a) \right]$$

**Campi di distanza con segno (SDF).** La forma è il livello zero di una funzione: negativa dentro, positiva fuori. Fusioni e piazze ritagliate sono operazioni booleane morbide:

$$f_{A \cup B} = \min(f_A, f_B), \quad f_{A \setminus B} = \max(f_A, -f_B), \quad \mathrm{smin}_k(a,b) = -k \ln\left(e^{-a/k} + e^{-b/k}\right)$$

Gli attrattori modulano scala e porosità con la distanza d dall'attrattore, ad esempio con un fattore h(d) = h₀ + Δh·e^(−d/λ), fra 16 e 120 m di altezza.

**Autoencoder MLP.** Le piante vengono compresse e ricostruite minimizzando l'errore sui valori di distanza campionati:

$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} \left\| f(p_i) - D(E(f))(p_i) \right\|^2$$

Il blending tra due piante è un'interpolazione nel latente: z = (1 − t)·z₁ + t·z₂.

**Statica grafica 3D (3DGS).** È la parte più rigorosa e la più vicina alla ricerca di Bhooshan all'ETH. Diagramma di forma e diagramma delle forze sono reciproci: ogni asta della forma è perpendicolare a una faccia del poliedro delle forze, e l'area della faccia dà l'intensità della forza.

$$\mathbf{e}_{ij} \parallel \mathbf{n}_{f}, \qquad F_{ij} = A_f$$

Celle poliedriche chiuse garantiscono equilibrio nodale; orientando tutte le facce verso l'interno si ottiene una struttura solo compressa (copertura, lucernario, colonne).

**Suddivisione geometrica.** Il duale topologico (tipo Voronoi/Delaunay) e l'asse mediale (luogo dei centri dei cerchi massimi inscritti) servono a dividere lastre di forma libera in stanze a gerarchia di dimensione.

## Sistemi AI: architettura della pipeline

L'AI qui è usata per decidere, non per disegnare: nessun modello generativo di immagini, ma tre stadi in cascata dove l'output di uno vincola il successivo. Il flusso è a senso unico: l'edificio non retroagisce sul gioco urbano, ed è uno dei limiti sollevati dalla giuria.

| Componente | Tipo di AI | Input → output | Maturità nel progetto |
|---|---|---|---|
| Gioco urbano | Multi-agente, teoria dei giochi | Matrice di adiacenza, fondi → uso del suolo | Solo 2 giocatori; Game 1 non converge |
| Spazio latente | Campo di costo/valore | 4 indicatori → guida delle mosse | Pesi e normalizzazione non mostrati |
| Q-learning | Reinforcement learning tabellare | Esiti passati → politica di crescita | Reward e stati non specificati |
| Phase I | RL su regole di adiacenza | Regole → policentri, reti stradali | Prodotto nel primo anno |
| Autoencoder MLP | Rete neurale (deep learning) | Piante SDF → latente → ricostruzione | Poi sostituito da regole per controllo |
| Grammatica SDF | Procedurale (non AI) | Attrattori, densità → masse | Il cuore formale del progetto |
| 3DGS | Form-finding geometrico (non AI) | Poliedri → struttura in equilibrio | Il componente più rigoroso |

Nota chiave: le parti di AI "vera" (MLP, Q-learning) sono le meno sviluppate; il controllo formale finale è affidato a regole esplicite e alla statica. Il team stesso abbandona l'MLP per "guadagnare controllo sulla massa" (4:52:12).

## Confronto con gli altri studi del Day 2

Gli altri team usano AI e calcolo per parti singole (organizzazione del programma, struttura); solo Bhooshan collega economia urbana, forma e statica in una catena unica.

| Ora nel video | Team (studio) | Modelli matematici / AI | Uso |
|---|---|---|---|
| 8:15 | Atmosphere Intelligence (Spyropoulos) | Voxel + regressione su dati atmosferici; GNN per posizionare 162 spazi; crescita differenziale con attrattori/repulsori | Centro di ricerca sulla superconduttività al CERN |
| 1:14:23 | Khora (Schumacher) | Agenti tipo boids (allineamento, coesione, separazione); ottimizzazione topologica dell'endoscheletro | Mega-edificio verticale |
| 2:30:08 | Nautilus (Angius) | Simulazioni fluidodinamiche (scala Beaufort 1–11); ottimizzazione topologica delle pinne | Habitat mobile marino a Jeju |
| 4:38:21 | Make No Little Plans (Bhooshan) | Nash/minimax, latente, Q-learning, MLP-SDF, 3DGS | Distretto a Milton Keynes |
| 5:48:56 | Emergence (Schumacher) | Simulazione di percorsi punto-punto; ottimizzazione topologica in due fasi | Distretto 500 × 500 × 400 m a Wapping |
| 6:51:26 | Architecture of Co-Intelligence (Spyropoulos) | Modello predittivo di estinzione, K-means, self-organizing map, adiacenza pesata, ottimizzazione multi-fattore | Banca dei semi con microclimi |

## Valutazione critica

Il punto di forza è la procedura end-to-end; il punto debole è che le regole che la governano non sono esplicitate né validate.

**Cosa funziona**

- Pipeline completa dalla scala urbana al dettaglio strutturale, in cui ogni decisione è "testata e difendibile" (Schumacher, 5:09:35).
- La statica grafica 3D lega forma e forze in modo verificabile: è la parte con il fondamento matematico più solido.
- Il catalogo di template riprende un meccanismo storico reale: Chicago è cresciuta in 50 anni grazie a template riusati da molti sviluppatori (Bhooshan, 5:28:41).

**Problemi aperti**

- **Funzione di payoff non definita.** "Benessere" e "produttività" non hanno una metrica (critica in giuria, 5:13:16); senza payoff espliciti l'equilibrio di Nash non è verificabile.
- **Somma zero contro win-win.** Il modello dichiara un gioco a somma zero ma rivendica un esito in cui entrambi guadagnano: serve un termine di creazione di valore.
- **Due soli giocatori.** La città reale ha centinaia di sviluppatori e autori; più critici chiedono multi-autorialità e varietà (5:15:25 e 5:19:04).
- **Fisica ambientale assente.** Orientamento, ombreggiamento reciproco e densità per esposizione non entrano nel gioco.
- **AI poco profonda.** MLP abbandonato per perdita di controllo; Q-learning senza stati e reward documentati. Non ci sono metriche di convergenza o confronto con baseline.
- **Nessun ritorno.** La struttura non modifica il masterplan: manca un ciclo di feedback tra stadi.

**Spunti per sviluppare il metodo**

- Scrivere i payoff come funzioni esplicite e testare la convergenza con N giocatori (giochi a potenziale, dove la funzione potenziale coincide con il "paesaggio energetico" dell'agenda del lab).
- Aggiungere al campo latente termini solari e di vento calcolati, non solo economici.
- Usare modelli neurali come surrogati veloci di 3DGS o di simulazioni, invece che come generatori di forma.

## Fonti

- [Video: DRL (PG) MArch Phase II Final Presentation (Day 2)](https://www.youtube.com/watch?v=KESutP6LWHU), trascrizione completa letta dall'autore dell'artifact il 19 ottobre 2026. Stato: `da verificare` in questa sessione.
- [DRL Phase 2 Review, gennaio 2026](https://drl.aaschool.ac.uk/phase-2-review-jan-2026). Stato: `da verificare` in questa sessione.
- [Bhooshan Lab, AA DRL](https://drl.aaschool.ac.uk/bhooshan-lab). Stato: `da verificare` in questa sessione.
- [Shajay Bhooshan, Zaha Hadid Architects](https://www.zha.com/people/shajay-bhooshan). Stato: `da verificare` in questa sessione.
