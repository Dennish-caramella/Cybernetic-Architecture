# 1. La tesi centrale di *Multi-agent Space Planning: A literature review (2008–2017)*

Condotta dai ricercatori della Carnegie Mellon University — Pedro Veloso, Jinmo Rhee e Ramesh Krishnamurti — questa rassegna sistematica della letteratura scientifica analizza l'evoluzione e lo stato dell'arte del **Multi-agent Space Planning (MASP)** nel decennio 2008–2017.

Lo *Space Planning* (SP) — ovvero la risoluzione della complessa scacchiera di adiacenze, dimensioni, geometrie, orientamenti e circolazioni di un edificio — è stato affrontato per decenni dall'informatica attraverso metodi di ottimizzazione globale centralizzata (programmazione lineare, algoritmi genetici, simulated annealing). Tuttavia, questi approcci convenzionali tendono a trattare il progetto come un problema statico a scatola chiusa (*black box*), rigido e computazionalmente intrattabile all'aumentare delle variabili.

La tesi centrale degli autori è che:

> **I sistemi multi-agente (MAS) e i modelli basati su agenti (ABM) trasformano radicalmente lo space planning, convertendolo da un problema di ottimizzazione combinatoria astratta e centralizzata a un processo interattivo, decentralizzato e dinamico, in cui la configurazione spaziale emerge dalle percezioni locali, dalle azioni e dalle negoziazioni di una popolazione di agenti autonomi operanti in tempo reale.**

Da questa rassegna emerge una triplice tassonomia fondamentale che ordina l'intera produzione scientifica del settore:

```text
TIPO 1: AGENTI COME UNITÀ SPAZIALI MOBILI
Ogni agente possiede una geometria fisica propria (bolla, poligono, massa 3D)
e si muove nello spazio spinto da forze fisiche (attrazione, repulsione, molle).

TIPO 2: AGENTI CHE OCCUPANO LO SPAZIO
Gli agenti non hanno forma fissa: navigano e colonizzano un'infrastruttura condivisa
(griglia 2D/3D, voxel) attraverso stigmergia, feromoni o apprendimento per rinforzo.

TIPO 3: AGENTI CHE PARTIZIONANO LO SPAZIO
Gli agenti sono punti generatori o semi topologici che suddividono geometricamente
il continuo spaziale tramite tassellazioni matematiche (diagrammi di Voronoi, grafi duali).
```

Le trasformazioni concettuali individuate dal paper sono:

**risolutore centralizzato a scatola chiusa ↔ ecologia distribuita di agenti decentralizzati**

**ottimizzazione statica una-tantum ↔ simulazione generativa interattiva in tempo reale**

**layout rigido predefinito ↔ stato di equilibrio dinamico (*equilibrium state*)**

**separazione tra forma e programma ↔ co-evoluzione morfologica e funzionale**

**algoritmo cieco ↔ co-progettazione interattiva uomo-macchina**

---

# 2. Il contesto teorico: dai primi tentativi degli anni '70 all'Agent-Based Modeling

Gli autori ricostruiscono la genealogia del computational space planning articolandola su due radici storiche:

- **La tradizione del CAD pionieristico (anni '60–'70)**: William J. Mitchell (*Computer-Aided Architectural Design*, 1977) e i sistemi storici come IMAGE di Johnson (1970), che per primi tentarono di automatizzare la disposizione delle piante ospedaliere e scolastiche;
- **La convergenza tra MAS e Agent-Based Modeling (ABM)**: L'influenza delle scienze della complessità (Wilensky e Rand, 2015). Mentre l'approccio classico dell'Intelligenza Artificiale punta a risolvere un task esplicito mediante coordinamento (*goal-oriented MAS*), l'approccio ABM esplora **comportamenti e pattern spaziali emergenti** non predicibili a partire dalle singole regole individuali.

Il paper analizza due illustri precedenti storici e sedici prototipi contemporanei sviluppati tra il 2008 e il 2017, offrendo un quadro comparativo basato su tre dimensioni: **rappresentazione**, **obiettivi spaziali** e **procedure di controllo**.

---

# 3. TIPO 1: Agenti come unità spaziali mobili (*Moving Spatial Units*)

Nel primo tipo, ciascun agente incorpora una rappresentazione geometrica esplicita dello spazio architettonico da allocare. Gli agenti si muovono fisicamente su un piano o in uno spazio tridimensionale, respingendosi o attraendosi a vicenda.

Gli autori esaminano nove prototipi cardinali:

### 2.1 IMAGE (IMG, 1970 — Johnson)
- **Precedente storico**: Sviluppato al MIT, rappresenta gli spazi come rettangoli su griglia. Gli agenti si muovono per soddisfare vincoli di adiacenza e minimizzare distanze di circolazione.

### 2.2 Fuzzy Layout Planner (FLP, 2008 — Akasaka et al.)
- **Meccanismo**: Diagramma a bolle (*bubble diagram*) dinamico. Le bolle modificano le proprie dimensioni mantenendo costante l'area target; forze repulsive impediscono sovrapposizioni e logica fuzzy gestisce le preferenze dell'utente.

### 2.3 Sniffing Space I (SS1, 2012 — Keng e Tang)
- **Ibrido Tipo 1 + Tipo 2**: Bolle circolari che rilasciano gradienti sensoriali ed espandono la propria circonferenza fino a raggiungere l'area desiderata.

### 2.4 Actants (ACT, 2013 — Narahara)
- **Meccanismo**: Ispirato alla teoria *Actor-Network*, tratta le stanze come poligoni sciolti che si impaccano liberamente. Gli agenti possono formare alleanze (sovrapponendosi ad agenti associati) o respingere stanze nemiche.

### 2.5 Floating Bubbles (FB, 2014 — Knecht e Koenig)
- **Meccanismo**: Sistema fisico 2D con particelle connesse da molle (*springs*). Le bolle circolari convergono verso l'equilibrio strutturale e possono essere convertite in poligoni rettangolari ortogonali.

### 2.6 Space-planning with Real-Time Physics (RTF, 2014 — Michalatos)
- **Meccanismo**: Simulazione fisica tridimensionale in tempo reale (sviluppata per ambienti come Rhino/Grasshopper). Gli spazi sono sfere con collisioni elastiche nello spazio volumetrico 3D, poi convertite in cubi e allineate a una griglia strutturale.

### 2.7 Interactive Bubbles (IB, 2014 — Li et al.)
- **Meccanismo**: Motore particellare interattivo in cui l'utente può afferrare e trascinare le bolle mentre il sistema ricalcola istantaneamente le adiacenze ottimali.

### 2.8 Narrative Landscape (NL, 2016 — Trendafilov et al.)
- **Meccanismo**: Poligoni convessi dotati di campi di forze che traducono narrative d'uso e sequenze spaziali in layout compatti.

### 2.9 Multi-agent + Evolutionary (MAE, 2016 — Rhee et al.)
- **Meccanismo**: Unisce la simulazione fisica 3D di agenti a forma sferica o a capsula con algoritmi evolutivi per ottimizzare orientamento solare, altezze e affacci.

---

# 4. TIPO 2: Agenti che occupano lo spazio (*Agents that Occupy a Space*)

Nel secondo tipo, gli agenti **non possiedono una forma geometrica autonoma predeterminata**.

Essi operano all'interno di un'infrastruttura spaziale preesistente e condivisa (griglia di celle, voxel tridimensionali, rete nodale di percorsi), navigando e appropriandosi progressivamente delle porzioni di territorio necessarie.

I prototipi analizzati includono:

### 3.1 Sniffing Space II (SS2, 2013 — Tang e Keng)
- Agenti che allocano funzioni lungo percorsi di circolazione predefiniti basandosi su tracce olfattive e densità di flusso pedonale.

### 3.2 Stigmergic Space Adjacency Software (SSAS, 2013 — Meyboom e Reeves)
- Gli agenti rappresentano entità del brief che colonizzano un reticolo di nodi 3D mediante feromoni virtuali mappati nello spazio colore RGB. La compatibilità programmatica guida l'attrazione, mentre il "feromone della regina" impone i vincoli ambientali del lotto.

### 3.3 Collective Construction (CC, 2015 — Gu e Wang)
- Un sistema di **apprendimento per rinforzo multi-agente** (*Q-learning*). Gli agenti depositano blocchi modulari imparando per tentativi ed errori quali combinazioni massimizzano le prestazioni strutturali e funzionali.

### 3.4 Artificial Life Space Planning (ALSP, 2016 — Veloso e Krishnamurti)
- Combina automi cellulari e agenti territoriali su griglia 2D/3D con cicli metabolici di crescita, competizione e assestamento morfologico.

---

# 5. TIPO 3: Agenti che partizionano lo spazio (*Agents that Partition Space*)

Nel terzo tipo, gli agenti non sono masse fisiche né occupanti di griglie: agiscono come **semi geometrici generatori (*seeds*) che partizionano continuamente lo spazio continuo**.

La geometria delle stanze non è disegnata direttamente, ma emerge dal calcolo matematico dei confini tra i semi:

### 4.1 YONA (2014 — Merrell et al.)
- Ispirato alle teorie della città spaziale di Yona Friedman. Utilizza grafi e partizioni gerarchiche per generare layout residenziali personalizzabili all'interno di una megastruttura.

### 4.2 Associative Spatial Networks (ASN, 2014 — Herr e Fischer)
- Generazione di spazi espositivi e padiglioni fieristici tramite reti associative e suddivisione geometrica continua del piano.

### 4.3 Dwelling Agglomerator (DA, 2014 — Coates et al.)
- Generazione di insediamenti urbani e agglomerati di alloggi a grappolo (*clustering*) attraverso la partizione dello spazio topologico.

### 4.4 Responsive Algorithms (RA, 2015 — Chronis et al.)
- Combina agenti mobili di Tipo 1 con **diagrammi di Voronoi pesati**. La posizione di equilibrio delle particelle determina istantaneamente le linee di divisione dei muri perimetrali.

### 4.5 Evolving Floorplans (EF, 2017 — Del Campo et al.)
- Generazione di piante complesse mediante partizioni voronoidali coadiuvate da algoritmi genetici per testare la qualità distributiva delle pareti divisorie.

---

# 6. Analisi incrociata e correlazioni statistiche

Gli autori costruiscono una rigorosa matrice comparativa (Tabelle 1–6 del paper) correlando tipologie, rappresentazioni, obiettivi e metodi di controllo:

```text
TIPO 1 (Unità Mobili):
Correlazione altissima con: Motori fisici particellari, bolle, molle elastiche.
Vantaggio: Massima intuizione visiva, manipolabilità in tempo reale dall'architetto.
Limite: Difficoltà a generare pareti ortogonali e layout costruttivi reali (fuga nella bolla).

TIPO 2 (Occupanti di Spazio):
Correlazione altissima con: Griglie 2D, Voxel 3D, Stigmergia, Feromoni biologici.
Vantaggio: Eccellente gestione della porosità, adattabilità a lotti irregolari complessi.
Limite: Forme risultanti spesso sfrangiate (*jagged edges*), richiedono post-processing.

TIPO 3 (Partizionatori):
Correlazione altissima con: Diagrammi di Voronoi, Tassellazioni matematiche, Algoritmi genetici.
Vantaggio: Riempimento perfetto e privo di buchi dello spazio disponibile.
Limite: Poca flessibilità nell'accogliere stanze ad angolo retto o geometrie standard.
```

---

# 7. Le lacune critiche e le sfide aperte per il futuro (Gap Analysis)

Nella discussione finale, Veloso, Rhee e Krishnamurti individuano cinque contraddizioni strutturali non ancora risolte dalla ricerca internazionale:

### 1. La "trappola del diagramma a bolle" e il realismo tettonico
La quasi totalità dei prototipi si ferma allo stadio di diagramma funzionale (cerchi colorati che rimbalzano sullo schermo). Manca il passaggio cruciale verso l'**architettura costruibile**: spessori murari, allineamenti strutturali, passaggi impiantistici e dettagli costruttivi.

### 2. La rimozione della circolazione (corridoi e atri)
I corridoi, le scale e gli spazi di transizione sono quasi sempre ignorati o trattati come un vuoto residuale non qualificato, laddove nell'architettura reale la circolazione costituisce la spina dorsale della vita sociale dell'edificio.

### 3. La scalabilità e i tempi di calcolo
Mentre i sistemi a 5–10 stanze raggiungono l'equilibrio in pochi secondi, l'applicazione a complessi ospedalieri o aeroportuali (centinaia di funzioni) produce rallentamenti esponenziali e frequenti blocchi in minimi locali imperfetti.

### 4. L'integrazione di obiettivi multi-criterio reali
I prototipi eccellono nel risolvere le adiacenze (chi sta vicino a chi), ma faticano a integrare simultaneamente luce naturale, efficienza termica, aerazione, acustica, normativa antincendio e costi.

### 5. Il ruolo del progettista: automazione cieca vs Co-Design
Il rischio maggiore del MASP è trasformarsi in un giocattolo tecnocratico che esclude l'architetto. Gli autori ribadiscono che il futuro non appartiene a sistemi che sputano piante definitive schiacciando un bottone, ma a piattaforme di **co-evoluzione e interazione aumentata**, in cui l'architetto agisce come agente cosciente all'interno dell'ecologia computazionale.

---

# 8. La struttura concettuale dell'intero saggio

La traiettoria analitica del paper segue questa sequenza organica:

**CRISI DEI METODI TRADIZIONALI DI OTTIMIZZAZIONE DELLO SPACE PLANNING**

↓

**EMERGENZA DEI MULTI-AGENT SYSTEMS (MAS) E AGENT-BASED MODELING (ABM)**

↓

**LA TRIPARTIZIONE FONDAMENTALE DEL MASP:**
- Tipo 1: Agenti come unità spaziali mobili (fisica particellare e bolle)
- Tipo 2: Agenti che occupano lo spazio (griglie, voxel e stigmergia)
- Tipo 3: Agenti che partizionano lo spazio (semi topologici e Voronoi)

↓

**ANALISI COMPARATIVA DEI 18 PROTOTIPI (2008–2017)**

↓

**MATRICE DELLE CORRELAZIONI: RAPPRESENTAZIONE, OBIETTIVI, CONTROLLO**

↓

**IDENTIFICAZIONE DEI GAP CRITICI DELLA RICERCA**
(assenza di tettonica, trascuratezza della circolazione, scalabilità)

↓

# VERSO PIATTAFORME DI CO-DESIGN INTERATTIVO UOMO-MACCHINA

---

## Il concetto più importante da portarsi via

Se dovessi condensare questa rassegna scientifica di Veloso, Rhee e Krishnamurti in una sola idea, direi questa:

> **Il Multi-agent Space Planning dimostra che l'organizzazione dello spazio architettonico non è una scacchiera statica da ottimizzare freddamente a priori, ma un'ecologia viva e dinamica in cui particelle mobili, occupanti cellulari e partizionatori geometrici possono negoziare dal basso una moltitudine di equilibri funzionali, a patto che il computer rimanga un partner di dialogo interattivo per l'architetto e non una scatola nera automatizzata.**
