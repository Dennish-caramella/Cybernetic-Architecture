# Mappe

## 1. Sette costellazioni

Le costellazioni sono quelle dell'indice 00 di `03_Analisi Approfondite/`.

```mermaid
flowchart LR
    A["A. Sistemi e morfogenesi<br/>01, 04, 07, 26, 27"]
    B["B. Cibernetica<br/>02, 03"]
    C["C. Architettura macchina<br/>05, 06, 25"]
    D["D. Discreto e mereologia<br/>08, 09, 17, 18"]
    E["E. Multi-agente<br/>12, 13"]
    F["F. Politica e partecipazione<br/>10, 11, 14, 15, 16, 24"]
    G["G. Giochi e simulazione<br/>19–23, 28–36"]
    A --> B
    B --> C
    C --> D
    B --> E
    D --> F
    E --> G
    F --> G
```

## 2. Linea dalla regola alla partecipazione

Il grafo mostra l'ordine con cui le analisi si riferiscono l'una all'altra, come si legge nelle schede.

```mermaid
flowchart TD
    Alex["Alexander 01, 04, 26<br/>sistemi generativi, semireticolo"] --> Pask["Pask 02, 03<br/>conversazione, controllo di controllo"]
    Pask --> Neg["Negroponte 05, 06<br/>macchina come partner"]
    Neg --> Steen["Steenson 07<br/>genealogia"]
    Alex --> Sanch["Sanchez 09, 11<br/>combinatorio e parametrico"]
    Sanch --> Carpo["Carpo 08<br/>smoothness e chunkiness"]
    Carpo --> Koeh["Koehler 18<br/>partitioning e partaking"]
    Koeh --> DeCarlo["De Carlo 24<br/>Uomo Tipo, retroazioni"]
    DeCarlo --> Mari["Mari 15<br/>autoprogettazione"]
    Koeh --> Games["Giochi<br/>MVRDV 19–23, AADRL 29–32"]
```

## 3. Fondamenta matematiche (Atlante, sez. 1–6)

```mermaid
flowchart LR
    Sys["Sistemi dinamici<br/>Bertalanffy, Gray-Scott, Physarum"] --> Aut["Automi<br/>von Neumann, Moore, Eden"]
    Aut --> Cyb["Cibernetica<br/>Ashby, Pask"]
    Cyb --> Game["Teoria dei giochi<br/>Nash, Prigioniero, Schelling"]
    Game --> Opt["Ottimizzazione<br/>simulated annealing, SDF"]
    Opt --> AI["IA<br/>RL, PPO, GNN, positional encoding"]
    AI -. usata in .-> Games2["Analisi 29–36"]
```
