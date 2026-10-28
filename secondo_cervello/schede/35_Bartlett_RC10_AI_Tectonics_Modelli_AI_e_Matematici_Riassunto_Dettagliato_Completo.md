# Bartlett RC10 (AI Tectonics): modelli AI e matematici

**Fonte:** The Bartlett Show Index, Architectural Design MArch, cluster RC10, 2021–2026
**Data analisi:** 19 ottobre 2026
**Metodo:** lettura dei testi di tutti i 20 progetti e visione di circa 120 tavole (render, diagrammi, schermate di software).

> Nel testo distinguo ciò che **si vede nelle tavole** da ciò che è una **mia deduzione**, segnata con *(probabilmente)*.

**Limiti:**

- I video Vimeo dei progetti 2026 non partono nel browser: si vede solo il fotogramma iniziale.
- Il sito B-Pro 2022 restituisce un errore 500. Per Neo-Liths e Brick(s) resta solo il testo letto in precedenza, mentre ReCASTING non è mai stato leggibile.

---

## 1. Quadro di sintesi

| Anno | Progetto | AI / ML | Metodi matematici e computazionali | Fabbricazione |
|---|---|---|---|---|
| 2026 | Urban Sutures | **Segmentazione semantica** delle facciate (dataset di maschere a classi) | Dataset basato su grafi, piante generate con regole | Blocchi prefabbricati in calcestruzzo |
| 2026 | LinX | Nessuna | **Generazione procedurale con seme** ("LinX Growth Engine"), abbinamento tra legno recuperato e ruoli strutturali | Legno recuperato e C16, DfMAD |
| 2026 | Crease Cell | Nessuna | **Origami rigido**, grammatica a regole | Lamiere piegate come cassaforma per calcestruzzo |
| 2026 | Lithic Pulse | Nessuna | **Statica grafica 3D**, strutture solo a compressione | Pietra colata in stampi in PLA stampati in 3D |
| 2026 | Re-Rock | Nessuna | **Signed Distance Fields**, teoria dei grafi, form finding, stereotomia | Taglio robotico della pietra, post-tensione |
| 2025 | Strata | Nessuna | Moduli solo a compressione | Stampa 3D, montaggio a secco |
| 2025 | Civic Canvas | **Graph autoencoder** addestrato sulle scelte dei giocatori | Grafi, PCA dello spazio latente | Nessuna |
| 2025 | Civic Matrix | **LLM** ("Living Space Customizer"), immagini generate con l'AI | **Algoritmo genetico multi-obiettivo** su griglia | Arredi robotici, partizioni mobili |
| 2025 | UtopiaLab | **Agenti conversazionali con LLM** (NPC con personalità MBTI), motore visivo AI | Suddivisione procedurale dei lotti, aggregazione esagonale | Nessuna |
| 2025 | Meta-CLT | AI addestrata su un dataset di piante che **genera grafi spaziali** | Dai grafi a stella alle unità 3D | CLT |
| 2024 | FlexFold | Nessuna | Pieghe curve | Lamiera tagliata al plasma e rivettata |
| 2024 | Horizon | **"Diffuser"** *(probabilmente un modello di diffusione)* addestrato su piante | **Punteggio basato su grafi** con regole di adiacenza (✓/✗) | Glulam, CLT, incastri |
| 2024 | InterX | Nessuna | Teoria dei giochi, allocazione a "pixel" sul sito | Robot a 6 assi, montaggio a secco |
| 2023 | Hive | Nessuna | Aggregazione per cluster, funzioni assegnate tramite campi, ottimizzazione strutturale | Prefabbricazione |
| 2023 | Oasis | Nessuna | Aggregazione automatica | Moduli |
| 2023 | Machiya | Nessuna | Kit di componenti | Legno massiccio, produzione off-site |
| 2022 | Neo-Liths | Machine learning (tipo non specificato) | Design procedurale, simulazioni di invecchiamento | Pietra stampata in 3D |
| 2022 | Brick(s) | Machine learning (tipo non specificato) | Modellazione procedurale, analisi di vento e sole | Non dichiarata |
| 2022 | ReCASTING | Non disponibile | Non disponibile | Non disponibile |
| 2021 | Syn-Katoikisis | Nessuna | Architectural Geometry, solai con nervature *(probabilmente sulle linee di tensione)*, grafi di accesso | Casseforme in schiuma tagliate a filo caldo CNC, robotica |
| 2021 | AIRS | Nessuna | Piante rappresentate a voxel, superfici rigate, form finding | Taglio robotico con sega a nastro, getti in casseforme flessibili |

---

## 2. Dettaglio per progetto

### 2026

**Urban Sutures** ([pagina](https://autumn2026.bartlettarchucl.com/rc10-ai-tectonics-2026/urban-sutures))

- **Tavole:**
  - una griglia di centinaia di facciate trasformate in maschere a colori su sfondo blu, cioè le etichette con cui si addestra un modello di **segmentazione semantica**;
  - un catalogo di 24 facciate di case a schiera londinesi;
  - un catalogo di piante di case vittoriane.
- **Pipeline:** la computer vision scompone le facciate dei vicini in elementi; un dataset collega questi elementi in un grafo; regole generano la pianta; il risultato sono blocchi prefabbricati.
- **Render:** fotorealistici, *(probabilmente)* fatti con l'aiuto dell'AI.

**LinX** ([pagina](https://autumn2026.bartlettarchucl.com/rc10-ai-tectonics-2026/linx))

- **Tavole:**
  - la web app "LinX Growth Engine", con seme casuale, strategia "Spine – on the site grid", pulsanti Regenerate/Randomize, animazione della crescita, statistiche (unità, superfici, pareti) e un programma di 18 voci;
  - l'inventario del legno recuperato con il suo catalogo, abbinato agli elementi della struttura reticolare;
  - un prototipo di nodo ramificato in legno.
- **Metodo:** generazione procedurale con seme e assegnazione ottimale delle travi recuperate ai ruoli strutturali.

**Crease Cell** ([pagina](https://autumn2026.bartlettarchucl.com/rc10-ai-tectonics-2026/crease-cell))

- **Tavole:** un catalogo di 18 prototipi piegati (volte, gusci e funghi a pieghe ripetute) e un modello a superficie piegata.
- **Metodo:** origami rigido con pieghe a tessellazione e grammatica architettonica a regole.

**Lithic Pulse** ([pagina](https://autumn2026.bartlettarchucl.com/rc10-ai-tectonics-2026/lithic-pulse))

- **Tavole:**
  - una matrice di poliedri delle forze che diventano capitelli ramificati, cioè **statica grafica 3D**;
  - un catalogo di tipi di alloggio (1b1p … 4b8p);
  - prototipi in pietra colata.
- **Metodo:** forme solo a compressione, configuratore digitale e stampi in PLA stampati in 3D.

**Re-Rock** ([pagina](https://autumn2026.bartlettarchucl.com/rc10-ai-tectonics-2026/rerock))

- **Tavole:**
  - una pianta con le **linee di livello di un campo di distanza (SDF)** che partono dai bordi delle stanze;
  - un'intradosso con corsi concentrici;
  - una volta divisa in conci numerati.
- **Metodo:** il grafo delle stanze definisce un SDF, da cui si ricava la geometria della volta e poi la sua divisione in conci per il taglio robotizzato.

### 2025

**Strata** ([pagina](https://autumn2025.bartlettarchucl.com/ad-rc10-ai-tectonics/rc10-project-1-team-strata))

- **Tavole:** nodi ramificati stampati in 3D e sopraelevazioni a scheletro leggero. Non si vedono algoritmi di AI.

**Civic Canvas** ([pagina](https://autumn2025.bartlettarchucl.com/ad-rc10-ai-tectonics/rc10-project-2-team-civic-canvas))

- **Tavole:**
  - grafici Python del **training di un graph autoencoder**: "Original Graph" e "Reconstructed Graph" per epoca, loss, matrice "Edge Probabilities" e "Latent PCA";
  - nodi etichettati come office, residential, commercial, recreation;
  - il gioco in terza persona, *(probabilmente)* in Unreal Engine, con interfaccia "Generate Map / Subdivision";
  - la mappa delle preferenze dei giocatori come punti colorati.
- **Metodo:** le azioni dei giocatori diventano grafi, che servono ad addestrare il graph autoencoder per l'analisi.

**Civic Matrix** ([pagina](https://autumn2025.bartlettarchucl.com/ad-rc10-ai-tectonics/rc10-project-3-team-civic-matrix))

- **Tavole:**
  - "Planar prototype under Genetic Algorithm": piante su griglia etichettate "Gen / Ind" con tre valori di fitness (FV1–FV3), cioè un **GA multi-obiettivo**;
  - lo schema "From user to planar": dati di stile di vita passano a un **LLM** ("Living Space Customizer") che produce il layout delle partizioni;
  - un sistema di arredi robotici;
  - immagini generate con l'AI.

**UtopiaLab** ([pagina](https://autumn2025.bartlettarchucl.com/ad-rc10-ai-tectonics/rc10-project-4-team-utopialab))

- **Tavole:**
  - un'interfaccia con vicini virtuali dotati di profilo, tratti MBTI e chat: **agenti conversazionali basati su LLM**;
  - una matrice di suddivisione procedurale dei lotti;
  - cluster esagonali.

**Meta-CLT** ([pagina](https://autumn2025.bartlettarchucl.com/ad-rc10-ai-tectonics/rc10-project-5-team-meta-clt))

- **Tavole:** grafi a stella (stanze come nodi) affiancati alle unità 3D in CLT generate da quei grafi.
- **Metodo:** un modello addestrato su un dataset di piante genera grafi, che vengono tradotti in volumi.

### 2024

**FlexFold** ([pagina](https://autumn2024.bartlettarchucl.com/rc10-ai-tectonics/flexfold))

- **Tavole:** sviluppo piano con pieghe curve tratteggiate e prototipo in lamiera rivettata.

**Horizon** ([pagina](https://autumn2024.bartlettarchucl.com/rc10-ai-tectonics/horizon))

- **Tavole:**
  - una matrice di oltre cento piante generate (colori per funzione);
  - una tavola di valutazione su griglia 3×4: ogni pianta diventa un grafo di adiacenze verificato con regole come "living room must connect living room" o "bedroom must connect living room", con esito ✓/✗.
- **Metodo:** il modello Diffuser *(probabilmente diffusione)* genera piante, un punteggio a grafo le valuta e il punteggio rientra nel ciclo di training.

**InterX** ([pagina](https://autumn2024.bartlettarchucl.com/rc10-ai-tectonics/interx))

- **Tavole:**
  - piattaforma con "Pixel availability / Pixel occupation" sul sito di Marylebone;
  - decine di varianti generate a strati;
  - cella robotica con due bracci a 6 assi.

### 2023

**Hive** ([pagina](https://bpro2023.bartlettarchucl.com/rc10-constructing-the-phygital/hive))

- **Tavole:** app su tablet strutturata in tre fasi più approvazione.
  - **Pre-aggregation:** sito, normativa, arretramenti, altezza massima.
  - **Aggregation:** scelta del tipo di cluster.
  - **Post-aggregation:** densità, definizione delle unità, "Field-based Functions Assignment", "Structural Optimization".

**Oasis** ([pagina](https://bpro2023.bartlettarchucl.com/rc10-constructing-the-phygital/oasis))

- **Tavole:** configuratore di interni e facciata, aggregazione a croce sul sito.

**Machiya** ([pagina](https://bpro2023.bartlettarchucl.com/rc10-constructing-the-phygital/machiya))

- **Tavole:** catalogo di 15 moduli del kit di componenti in legno.

### 2022 (immagini non accessibili)

- **Neo-Liths:** machine learning, design procedurale, simulazione di macchie solari e risalita capillare, pietra stampata in 3D (dal testo).
- **Brick(s):** machine learning, modellazione procedurale, analisi di vento e sole (dal testo).
- **ReCASTING:** pagina in errore.

### 2021

**Syn-Katoikisis** ([pagina](https://bpro2021.bartlettarchucl.com/rc10-habitat-tectonics/syn-katoikisis))

- **Tavole:**
  - unità abitative con i rispettivi grafi di accesso;
  - suddivisione dei piani in celle con percentuali residenziale/pubblico;
  - kit strutturali (interno, perimetro, angolo) per sagome regolari e irregolari;
  - solaio con nervature *(probabilmente sulle linee di tensione)* e casseforme in schiuma tagliate a filo caldo CNC;
  - piattaforma 3D con cursori per mix di alloggi, verde e luce solare.

**AIRS** ([pagina](https://bpro2021.bartlettarchucl.com/rc10-habitat-tectonics/airs))

- **Tavole:**
  - piante tradotte in voxel e aggregate su griglia;
  - piattaforma di personalizzazione in 5 step;
  - kit di componenti in legno;
  - nodi a superfici rigate gettati in casseforme flessibili.

---

## 3. Conclusioni

1. **Machine learning documentato** (dataset, training, grafici di loss): Urban Sutures (segmentazione semantica), Civic Canvas (graph autoencoder), Horizon (modello di diffusione con valutazione a grafo). Meta-CLT dichiara un training su piante, ma non ne mostra i dettagli.
2. **LLM come interfaccia verso gli utenti:** Civic Matrix (traduzione delle abitudini in layout) e UtopiaLab (vicini virtuali).
3. **Ottimizzazione evolutiva:** algoritmo genetico multi-obiettivo in Civic Matrix.
4. **Matematica e geometria strutturale**, il filone dominante:
   - SDF e stereotomia (Re-Rock);
   - statica grafica 3D (Lithic Pulse);
   - origami e pieghe curve (Crease Cell, FlexFold);
   - superfici rigate (AIRS);
   - teoria dei grafi (trasversale a quasi tutti i progetti).
5. **AI generativa per i render:** presente in quasi tutti i progetti 2024–2026, senza strumenti dichiarati.
6. **Filo comune:** piattaforma partecipativa, poi generazione computazionale, poi kit di componenti, infine fabbricazione digitale o robotica, applicati alla crisi abitativa di Londra.

**Ancora da verificare:** i software esatti (Grasshopper, PyTorch, Stable Diffusion, Unreal) non sono dichiarati. Potrebbero comparire nei video Vimeo dei progetti 2026.
