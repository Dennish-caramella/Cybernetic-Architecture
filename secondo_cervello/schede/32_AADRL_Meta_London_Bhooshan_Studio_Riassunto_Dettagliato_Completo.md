# AADRL Meta London: Modelli matematici e AI (Bhooshan Studio)

> **Origine:** artifact Claude Docs `d394c35a-b5fa-4399-9311-0cbc7063c58f`, letto il 2026-10-19 tramite il connettore. Copia salvata senza modifiche di contenuto, tranne un frammento corrotto segnalato sotto.
> **Fonte primaria:** video "AADRL Meta London, Bhooshan Studio" (45 min, pubblicato il 2 febbraio 2024), trascrizione di 330 segmenti e descrizione ufficiale, letti dall'autore dell'artifact. **Non riverificata in questa sessione.**
> **Stato:** `da verificare`. I minuti citati sono quelli del video.
> **Legenda:** le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact. Sono **inferenza**.
> **Nota di integrità dell'artifact:** nella sezione "Gioco a turni con funzioni di ricavo" compare un frammento corrotto ("o di terra e unit", "il cost" + "à"). Nel file è ricostruito come "costo di terra e unità" per coerenza con il testo; verificare con l'originale.

## Sintesi

"Meta London" (Bhooshan Studio, 2023–24) è l'antenato diretto dei progetti 2026: lo stesso gioco urbano tra attori, ma giocato con regole scritte a mano, senza reti neurali né reinforcement learning.

Il progetto costruisce una "sandbox virtuale" di crescita urbana su un sito vicino a West Ham (Londra). Quattro giocatori-sviluppatori (tra cui residenziale, uffici e commercio) e un quinto giocatore pubblico che rappresenta i cittadini piazzano a turno unità su una griglia di voxel secondo funzioni di ricavo locali; il giocatore pubblico incassa tasse e reinveste in stazioni, piazze, parchi e ponti. Il risultato è una "simulazione 4D dell'uso del suolo" che genera torri cilindriche miste con nodi strutturali e facciate dipendenti dal programma.

La giuria loda la coerenza e il passaggio "da master plan a master model", ma critica il repertorio formale limitato (solo cilindri, griglia fissa), la mancanza di scenari di fallimento e la perdita della ricchezza delle prime simulazioni a slime mold. Un critico suggerisce proprio le reti neurali per gestire la complessità dei parametri (31:08): è la strada presa dallo studio nel 2026.

## Contesto: Meta London nel percorso del Bhooshan Lab

Secondo la descrizione del video, Meta London è il progetto del team composto da Aria Torabi Nejad Karmani, Karan Kaushikkumar Lotwala, Shubham Sharad Kale e Krish Rajesh Nasta. Studio master: Shajay Bhooshan; tutor: Henry Louth e Keerti Manney. L'obiettivo dichiarato è un "blueprint" di densificazione ad alta densità lungo le reti di trasporto per raddoppiare popolazione ed economia di Londra in 25 anni.

Nel commento di Bhooshan (34:05) questo è "il primo anno" in cui lo studio affronta la scala della città e i processi bottom-up di formazione dei quartieri. L'obiettivo era una sandbox virtuale per testare ipotesi (troppe o troppo poche residenze rispetto alle attività) e passare "da master plan a master model".

La linea che porta al 2026:

1. **2023–24, Meta London:** gioco a turni con regole scritte a mano, ispirato a Cities: Skylines.
2. **2025–26, UpBridge City e VertiCity (Day 1):** stesso gioco risolto con reinforcement learning; forme da autoencoder su SDF.
3. **2025–26, Make No Little Plans (Day 2):** equilibrio di Nash, spazio latente, Q-learning e statica grafica 3D.

Nel 2026 il team UpBridge cita esplicitamente Meta London come progetto in cui il gioco "era giocato a mano", e il Bhooshan Lab elenca un progetto "Meta Cities", il nome usato nella descrizione del video ([pagina del lab](https://drl.aaschool.ac.uk/bhooshan-lab)).

## Il progetto passo per passo

| Minuto | Fotogramma | Cosa mostra |
|---|---|---|
| 1:28 | Metodologia | Letteratura, casi studio, ricerca progettuale, proposta |
| 2:08 | Griglie urbane | Organiche vs a griglia: Tokyo, New York |
| 3:19 | Marina City | Caso pilota: "città nella città", 2.500 abitanti |
| 4:35 | Slime mold | Percorsi minimi e reti in ambiente voxel |
| 5:32 | Cities: Skylines | Indici di felicità e ricavo come valutazione |
| 6:17 | Quattro griglie | Lineare, griglia, radiale, organica a confronto |
| 7:07 | Sito West Ham | Mesh adattiva dei lotti, tre posizioni di partenza |
| 7:55 | Giocatori e regole | Funzioni di ricavo per tipo di sviluppatore |
| 9:24 | Partita | Crescita turno per turno dalla prima stazione |
| 10:23 | Valutazione | Luce naturale, altezze, valore dei voxel |
| 10:32 | Domanda di mercato | Turni saltati finché manca domanda |
| 11:04 | Investimento iniziale | Distribuito, massiccio, tardivo: tre esiti |
| 12:10 | Uso del suolo 4D | Iterazioni geometriche dipendenti dal percorso |
| 12:51 | Nodi strutturali | 8 nodi per il commercio, 4 per il verde |
| 13:59 | Catalogo di tile | Residenze, coworking, spazi pubblici |
| 16:01 | Modelli fisici | Catalogo S/M/L/XL, gioco manuale |
| 17:05 | Inizio critica | Giuria e commento di Bhooshan (34:05) |

**1. Ricerca e casi studio (0:06–4:30).** Le città sono sistemi complessi dove decisioni locali producono schemi globali. Marina City (Chicago, Goldberg) è il caso pilota di "città nella città"; secondo il team servirebbero 140 Marina City all'anno per far crescere Londra come previsto.

**2. Simulazioni esplorative (4:35–7:05).** Prima uno slime mold (Physarum) in ambiente voxel, per percorsi minimi e reti tra punti, con comportamenti di attrazione e migrazione. Poi Cities: Skylines come caso studio di simulazione ad agenti: quattro griglie testate e valutate con gli indici di felicità e ricavo. Lezione: l'allocazione dell'uso del suolo pesa più di tutto sulla felicità.

**3. Il gioco (7:07–12:05).** Ogni giocatore, al suo turno, compra un lotto e piazza un'unità secondo una funzione di ricavo:

- **residenziale:** vista sull'acqua, luce naturale, vicinanza a uffici, servizi pubblici e commercio;
- **uffici:** vicinanza e connettività al trasporto pubblico;
- **commercio:** passaggio pedonale, quindi vicinanza ad altre unità e ai fronti più frequentati;
- **pubblico:** riscuote tasse dagli altri e investe in stazioni, piazze, parchi e ponti.

Versioni successive aggiungono la domanda di mercato (turni saltati) e tre strategie di investimento pubblico iniziale. Ogni partita è dipendente dal percorso e produce una geometria diversa.

**4. Architettura (12:10–15:43).** Il programma di ogni piano determina i nodi strutturali dello scheletro (8 contatti dove serve vetrina commerciale, 4 per il verde) e la facciata. Un catalogo di tile parametrici (residenze da monolocale a famiglia, coworking, spazi pubblici) si aggrega in torri cilindriche: servizi verso il nucleo, spazi abitabili sul perimetro.

## Modelli matematici

I metodi sono quelli nominati nel video; le formule sono la forma standard di ciascun metodo, ricostruita dall'autore dell'artifact. Il progetto è interamente basato su regole: nessun modello viene addestrato. **Inferenza.**

**Slime mold (Physarum).** Il modello classico di Tero et al. tratta la rete come tubi il cui spessore cresce con il flusso che li attraversa: i tubi usati si rinforzano, gli altri si atrofizzano. Ne emergono reti vicine ai percorsi minimi.

$$\frac{dD_{ij}}{dt} = f\left(|Q_{ij}|\right) - \mu D_{ij}, \qquad Q_{ij} = \frac{D_{ij}}{L_{ij}}\left(p_i - p_j\right)$$

Qui D è la conduttività del tubo, L la sua lunghezza, p la pressione nei nodi, μ il decadimento. Nella versione ad agenti (Jones) ogni particella segue la scia chimica dei vicini e ne deposita altra.

**Gioco a turni con funzioni di ricavo.** Ogni giocatore i sceglie il voxel x che massimizza un ricavo locale pesato, meno il costo di terra e unità (ricostruzione, vedi nota in testa). Una forma plausibile, coerente con le regole descritte:

$$R_i(x) = \sum_k w_{ik}\, \phi_k(x) - c(x), \qquad x_i^* = \arg\max_{x \in \text{liberi}} R_i(x)$$

I fattori φₖ sono vista sull'acqua, luce naturale, distanza dal trasporto, distanza da unità di altri tipi. Le tasse T = τ Σ Rᵢ finanziano il giocatore pubblico. È una strategia "greedy" (miope): ogni giocatore guarda solo la mossa corrente.

**Funzione di valutazione.** Come in Cities: Skylines, l'esito è misurato con indici aggregati: ricavo per giocatore, valore dei voxel, luce naturale. Il team definisce "vincente" lo scenario più bilanciato, cioè quello che massimizza i ricavi minimi:

$$\text{scenario}^* = \arg\max_{s} \; \min_i R_i(s)$$

Un critico osserva (39:31) che non c'è cooperazione esplicita: è una "mano invisibile" in cui scelte egoistiche aggregate producono ordine. In termini di teoria dei giochi è una dinamica di best response sequenziale, non un gioco cooperativo.

**Dipendenza dal percorso.** Lo stesso insieme di regole con seed e investimenti iniziali diversi dà città diverse: è un sistema dinamico discreto sensibile alle condizioni iniziali, analizzato in tre scenari di investimento pubblico.

**Mappatura programma → struttura.** Una regola discreta assegna a ogni tipo di tile un numero di nodi di contatto (8 commercio, 4 verde); lo scheletro della torre è la sequenza di questi nodi lungo l'altezza.

## Sistemi computazionali: il ciclo del gioco

Meta London non usa AI nel senso di apprendimento automatico: è una simulazione ad agenti con regole esplicite, la cui unica retroazione passa per il giocatore pubblico.

| Componente | Tipo | Ruolo nel progetto | Erede nel 2026 |
|---|---|---|---|
| Slime mold in voxel | Simulazione bio-ispirata | Esplorazione di reti e crescita organica; poi abbandonata | Nessuno diretto |
| Analisi Cities: Skylines | Gioco come caso studio | Indici di felicità e ricavo come criteri | Reward dei giochi RL |
| Mesh adattiva dei lotti | Geometria procedurale | Tabellone del gioco | Circle packing e campi vettoriali (VertiCity) |
| Giocatori con funzioni di ricavo | Agenti a regole, greedy | Uso del suolo turno per turno | Agenti RL (UpBridge), Nash e Q-learning (Day 2) |
| Domanda di mercato | Vincolo di sistema | Turni saltati | Funzioni di stato con valore fondiario |
| Catalogo di tile parametrici | Kit di parti | Torri cilindriche miste | Autoencoder su SDF |
| Nodi per programma | Regola discreta | Scheletro e facciata | Statica grafica 3D (Day 2) |

La tabella mostra l'evoluzione: ogni regola scritta a mano nel 2023–24 diventa, due anni dopo, qualcosa che il sistema impara o ottimizza. **Inferenza**: la tabella è un confronto costruito dall'autore dell'artifact.

## Confronto con i progetti 2026

Tra il 2023–24 e il 2026 lo studio sostituisce le regole scritte a mano con sistemi che imparano, ma conserva la stessa idea: la città come gioco tra attori economici.

| Aspetto | Meta London (2023–24) | UpBridge / VertiCity (Day 1, 2026) | Make No Little Plans (Day 2, 2026) |
|---|---|---|---|
| Sito | West Ham, Londra | Thamesmead/Barking; Swansea | Milton Keynes |
| Catalizzatore | Densità lungo il trasporto | Industria e ricerca; data center edge | Startup tecnologiche |
| Giocatori | 4 sviluppatori + 1 pubblico | 2 agenti | 2 agenti |
| Decisione | Regole greedy a turni | RL multi-agente (PPO); gioco a reward | Nash/minimax, latente, Q-learning |
| Valutazione | Ricavi, luce, valore voxel, scenario bilanciato | Reward cumulata, regole rispettate | Agency score, posti di lavoro |
| Forma | Catalogo di tile, torri cilindriche | Autoencoder su SDF, mappa latente | MLP-SDF, poi grammatica SDF |
| Struttura | Nodi per programma | Casseri 3D; strutture sospese | Statica grafica 3D |

Due critiche del 2024 tornano identiche nel 2026: repertorio formale troppo uniforme e regole del gioco non abbastanza esposte. Una invece è stata accolta: nel 2024 un critico suggeriva reti neurali per gestire la complessità dei parametri (31:08), e nel 2026 lo studio le adotta. Al contrario, il numero di giocatori scende da cinque a due, il che rende i giochi più leggibili ma meno realistici.

## Valutazione critica

Meta London è coerente e ben presentato, e fonda il metodo dello studio; il limite è che la ricchezza delle simulazioni iniziali si perde in un sistema rigido di griglia e cilindri.

**Cosa funziona**

- Sistema leggibile: funzioni di ricavo per tipo di attore chiare e plausibili (25:16).
- Dal "master plan" al "master model": una sandbox in cui testare ipotesi di sviluppo (Bhooshan, 34:38).
- Idea di "prossemica funzionale": vicinanza tra funzioni, non solo tra persone, come motore della forma (21:36).
- Legame tra programma, nodi strutturali e facciata, da rafforzare ma già presente.

**Problemi aperti**

- **Nessuno scenario di fallimento.** Cosa succede se un giocatore perde, se il commercio sparisce, se arriva la decrescita (17:15, 18:19).
- **"Fisica selvaggia" addomesticata.** La complessità dello slime mold diventa una griglia regolare per esigenze di lottizzazione (23:12).
- **Repertorio formale limitato.** Solo torri cilindriche con impronte simili; servono taglie da molto piccolo a molto grande e atrii (27:51, 37:01).
- **Matrici di payoff non ispezionate.** Bhooshan stesso chiede di capire quali fattori producono quali esiti (36:23).
- **Scala umana e quartiere.** Manca la vita "tra gli edifici" e una definizione di quartiere in verticale (29:12, 40:19).

**Spunti**

- Rendere le funzioni di ricavo una tabella pubblica e mostrare le partite perse, non solo quelle bilanciate.
- Valutare con agenti-cittadino che si spostano tra casa e lavoro, come in Cities: Skylines, anche in 3D (42:09).
- Recuperare lo slime mold come generatore di lotti di taglie diverse invece di scartarlo.

## Fonti

- [Video: AADRL Meta London, Bhooshan Studio](https://www.youtube.com/watch?v=_vZRzNRhiHQ), trascrizione e descrizione lette dall'autore dell'artifact il 19 ottobre 2026. Stato: `da verificare` in questa sessione.
- [Bhooshan Lab, AA DRL](https://drl.aaschool.ac.uk/bhooshan-lab). Stato: `da verificare` in questa sessione.
- [Shajay Bhooshan, Zaha Hadid Architects](https://www.zha.com/people/shajay-bhooshan). Stato: `da verificare` in questa sessione.
- [Analisi del Day 1 (2026)](https://claude.ai/code/artifact/16c9875c-a5a1-4cbd-8a76-a99826cf1508). Vedi `01_AA_DRL_Phase_II_Day1_Bhooshan.md`.
- [Analisi del Day 2 (2026)](https://claude.ai/code/artifact/305b60f6-30a7-43d2-a3a9-b77ce03843f4). Vedi `02_AA_DRL_Phase_II_Day2_Bhooshan_Make_No_Little_Plans.md`.
- Riferimento citato nel testo (non verificato in questa sessione): Tero et al., modello Physarum; Jones, versione ad agenti. Da reperire e verificare prima di qualsiasi citazione in tesi.
