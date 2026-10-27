# 1. La tesi centrale di *Architectural Assemblages as Computational Medium*

Presentato alla conferenza internazionale eCAADe nel 2023 da Alessio Erioli (ricercatore all'Università di Bologna e co-fondatore di Co-de-iT), questo saggio introduce e teorizza **Assembler**, uno strumento computazionale avanzato sviluppato per l'ambiente Rhino-Grasshopper dedicato alla progettazione e allo studio degli assemblaggi architettonici.

Erioli affronta una contraddizione aperta nella teoria architettonica contemporanea: da un lato, la filosofia post-strutturalista e il pensiero computazionale celebrano la nozione di "assemblaggio" (*assemblage*) e di mereologia; dall'altro lato, gli strumenti software disponibili per gli architetti sono rimasti vincolati a modellazioni geometriche passive oppure ad aggregazioni combinatorie superficiali che ignorano la complessità relazionale, la circolazione e la porosità spaziale.

La tesi fondamentale di Erioli è che:

> **L'assemblaggio architettonico non è una semplice composizione formale né una cieca combinatoria di pezzi (*ars combinatoria*), ma un medium computazionale scalabile e interscalare in cui parti ripetute, vuoti abitabili e relazioni topologiche co-determinano le proprietà emergenti dell'edificio attraverso una rete automatizzata di decisioni distribuite.**

Erioli stabilisce che un assemblaggio architettonico si distingue ontologicamente da un mero "aggregato" inerte (come un mucchio di sassi) proprio per la sua **struttura topologica connettiva**: la capacità computazionale di preservare e calcolare le linee di circolazione, i flussi, le adiacenze e i campi di forze contestuali.

```text
MERO AGGREGATO INERTE:
Accumulo caotico di parti → Nessuna connettività calcolabile → Forma chiusa

ASSEMBLAGGIO ARCHITETTONICO (Assembler):
Unità discrete (solidi e vuoti) + Relazioni sintattiche + Campi tensoriali (Field)
                              ↓
              Topologia connettiva della circolazione
                              ↓
             Proprietà emergenti e identità interscalare
```

Da questa premessa discendono le trasformazioni concettuali del saggio:

**modellazione formale continua ↔ assemblaggio mereologico discreto**

**decisione umana accentrata ↔ cascata decisionale automatizzata (Bratton)**

**parte subordinata al tutto ↔ co-determinazione reciproca parte-tutto**

**composizione di solidi ↔ computazione del vuoto come parte primaria**

**forma statica permanente ↔ sistema aperto guidato da campi di dati (*Tensor Fields*)**

**ars combinatoria cieca ↔ sintassi architettonica connettiva della circolazione**

---

# 2. Il contesto teorico e filosofico: Deleuze, DeLanda e la Mereologia

La ricerca di Erioli poggia su tre pilastri filosofici ed epistemologici rigorosi:

### 1. La Teoria dell'Assemblaggio (*Assemblage Theory*)
Fondata da Gilles Deleuze e Félix Guattari (*Mille Piani*, 1987), sistematizzata dal filosofo Manuel DeLanda (2006, 2016) e applicata alla teoria architettonica da Kim Dovey (*Assembling Architecture*, 2013). L'assemblaggio definisce un insieme eterogeneo le cui proprietà non sono riducibili alla somma delle sue componenti, ma emergono dalle **relazioni di esteriorità** tra le parti: ogni componente gode di una propria autonomia ontologica e può essere staccata e ricombinata in altri contesti.

### 2. La Mereologia
La branca della logica formale che studia i rapporti tra le parti e il tutto (Stanisław Leśniewski, Achille Varzi, Daniel Koehler). A differenza della geometria metrica tradizionale che misura distanze e angoli, la mereologia indaga la condizione di appartenenza (*parthood*) e il modo in cui l'identità del tutto retroagisce sull'identità delle parti.

### 3. L'Automazione Planetaria e le cascate decisionali (Benjamin Bratton)
Citando Benjamin Bratton (*The Terraforming*, 2019), Erioli ridefinisce il concetto stesso di automazione: essa non consiste semplicemente nel sostituire le braccia dell'uomo con quelle della macchina, ma nella **dissoluzione della decisione umana all'interno di reti composite di relè biologici, protesici e algoritmici**. L'automazione si propaga attraverso scale dimensionali differenti (dal livello molecolare alla scala planetaria) generando "cascate trofiche" di effetti indiretti.

---

# 3. I precursori architettonici: da Alexander a Cedric Price e Yona Friedman

Erioli traccia una genealogia esplicita dei sistemi computazionali e sistemici in architettura:

- **Christopher Alexander**: Il concetto di semireticolo (*A City is not a Tree*, 1965) e la doppia dimensione dei sistemi in *Systems Generating Systems* (1968), in cui la regola generativa combina parti discrete per far emergere qualità olistiche stabili.
- **Yona Friedman e il *Flatwriter* (1971)**: Uno dei primi esempi storici di co-progettazione algoritmica partecipativa. Una macchina con cui i futuri residenti potevano comporre la propria cellula abitativa all'interno della *Ville Spatiale* secondo regole di compatibilità e preferenze individuali.
- **Cedric Price e il *Generator* (1976)**: Concepito con John e Julia Frazer, il Generator integrava microprocessori che monitoravano l'uso dei blocchi mobili, suggerendo autonomamente modifiche e riconfigurazioni agli utenti quando il sistema avvertiva noia o stagnazione d'uso.
- **Shape Grammars e Combinatoria**: George Stiny (1980), Terry Knight (1991), Bill Hillier (*Space is the Machine*, 1989), fino ai contemporanei Jose Sanchez, Gilles Retsin, Daniel Koehler, Andrea Rossi (*Wasp*) e Petras Vestartas (*Fox*).

Assembler nasce per superare i limiti operativi degli strumenti parametrici esistenti, colmando la necessità di un motore deterministico, personalizzabile e scalabile fondato sulla manipolazione del vuoto.

---

# 4. Architettura del software: la logica operativa di *Assembler*

Sviluppato come libreria compilata in C# (.dll) per Rhino-Grasshopper, *Assembler* è concepito come un sistema **agnostico rispetto alla scala** (*scale-agnostic*): può generare indifferentemente un dettaglio tettonico, un edificio, un quartiere o una struttura temporanea.

Il sistema opera come un **agente computazionale iterativo** guidato da una domanda operativa fondamentale:

> **"Dove posiziono il prossimo oggetto?"**

Questa domanda genera due decisioni complementari ad ogni ciclo temporale:
1. *In quale posizione geometrica aggiungere il nuovo elemento?*
2. *Quale tipo di oggetto inserire e con quale orientamento spaziale?*

Il ciclo algoritmico si ripete aggiungendo un oggetto alla volta fino al raggiungimento di una condizione di terminazione (numero massimo di elementi, saturazione del volume, raggiungimento di una soglia prestazionale).

```text
LOOP OPERATIVO DI ASSEMBLER (3 STADI):
1. SELEZIONE DEL RICEVENTE (Receiver) tra gli oggetti già assemblati
2. SELEZIONE DEL TRASMETTITORE (Sender) coerente con le euristiche e privo di collisioni
3. CONNESSIONE E AGGIORNAMENTO del grafo topologico e del campo di dati
```

---

# 5. Componenti strutturali: AssemblyObjects (AO) e Handles

Erioli scompone l'assemblaggio in unità elementari rigorosamente codificate:

### AssemblyObjects (AO)
- Le parti ripetibili dell'assemblaggio.
- Ciascun AO contiene: mesh di collisione per il calcolo delle interferenze fisiche, mesh di visualizzazione e dati semantici.
- **La centralità del vuoto**: A differenza dei tipici sistemi combinatori che assemblano solo "mattoni" pieni, Assembler permette di trattare geometrie vuote (spazi d'aria, stanze, logge) come componenti primari di assemblaggio (*void geometries as basic parts*).

### Handles (Maniglie di connessione)
- Punti vettoriali e piani locali di ancoraggio che definiscono le regole geometriche di aggancio tra due oggetti.
- Supportano connessioni asimmetriche, rotazioni prefissate e allineamenti controllati.
- Una tabella di combinazioni genera automaticamente tutte le permutazioni ammissibili ed esclude le combinazioni geometricamente incoerenti o fisicamente impossibili.

---

# 6. Il contesto ambientale e i campi tensoriali (*Tensor Fields*)

Come risponde l'assemblaggio ai vincoli fisici, climatici o programmatici del mondo reale?

Erioli introduce due costrutti di eccezionale potenza:

### L'Environment
Poliedri chiusi che definiscono limiti solidi (ostacoli fisici invalicabili) o volumi di inviluppo (confini entro cui la crescita deve rimanere confinata per inclusione).

### Il Field (Campo Tensoriale Voxel 3D)
Una matrice tridimensionale di voxel capace di mappare dati eterogenei dello spazio attraverso una classe dedicata (*Tensor*). Ogni singolo punto nello spazio può contenere:
- **Scalari** (valori a virgola mobile): generano segnali di intensità continua (es. radiazione solare, gradiente termico, livello di rumore, distanza da una strada);
- **Vettori**: definiscono direzioni preferenziali verso cui orientare o spingere l'aggregazione (es. traiettoria dei venti dominanti, linee di forza strutturali);
- **iWeights** (interi): definiscono indici che impongono **quali set di regole e quali pezzi utilizzare in una specifica regione dello spazio**.

L'assemblaggio legge i valori locali del Field in tempo reale: la forma non nasce da un'ispirazione astratta, ma si plasma crescendo lungo i gradienti del contesto informativo.

---

# 7. La circolazione come discriminante tra aggregato e architettura

Uno dei passaggi più brillanti dell'argomentazione di Erioli è la distinzione tra scultura combinatoria e spazio architettonico vivibile:

> **Ciò che trasforma un mero aggregato di pezzi in un autentico assemblaggio architettonico è la capacità di calcolare e garantire la continuità dei flussi di circolazione.**

Assembler registra e conserva per tutta la durata della simulazione il **grafo topologico di connettività** tra gli ambienti:
- Ogni volta che due pezzi si agganciano tramite i loro Handles, il software memorizza la relazione di adiacenza nel grafo.
- Da questa rete di connessioni è possibile estrarre istantaneamente i percorsi di circolazione pedonale interni, i corridoi virtuali, le uscite di emergenza e i nodi di congestione.
- Il sistema può dialogare con motori di navigazione avanzati usati nei videogiochi, come le **NavMesh** (*Recast*, Mikko Mononen), permettendo a folle virtuali di verificare in tempo reale l'accessibilità dell'edificio generato.

---

# 8. Oltre l'Ars Combinatoria: il monito contro il "Martello di Maslow"

Nelle conclusioni, Erioli inserisce un fondamentale avvertimento epistemologico citando il teorico della sintassi spaziale Bill Hillier (*Space is the Machine*, 1989):

L'architettura non può essere ridotta a un'arida e cieca *ars combinatoria* di lettere geometriche disarticolate. 

Citando la nota legge dello strumento ("il martello di Maslow", per cui se l'unico strumento che possiedi è un martello, tutto il mondo comincerà a sembrarti un chiodo), Erioli mette in guardia i progettisti computazionali:

> **L'uso acritico e meccanico di un algoritmo combinatorio rischia di trasformare ogni problema architettonico in una sequenza insensata di blocchi ripetuti.**

L'architettura richiede la costruzione di filtri semantici, scale identitarie e una costante apertura mentale critica. La stanza non è solo un voxel: al variare della sua posizione nell'assemblaggio (all'angolo, nel nucleo cieco o a sbalzo sulla piazza) muta il proprio significato antropologico e la propria identità.

---

# 9. Sviluppi futuri: Integrazione con Deep Reinforcement Learning

Come evolverà la piattaforma? Erioli delinea l'orizzonte futuro di *Assembler*:

- Attualmente, la scelta di dove piazzare il prossimo pezzo è guidata da euristiche parametriche fisse o da script procedurali in C#.
- Il passo successivo consiste nell'integrare Assembler con **reti neurali artificiali profonde addestrate tramite Deep Reinforcement Learning (DRL)**.
- La rete neurale fungerà da "cervello decisionale" capace di apprendere per tentativi ed errori all'interno dell'ambiente voxelizzato, sviluppando un'autonoma sensibilità spaziale per bilanciare contemporaneamente requisiti strutturali, climatici, distributivi e formali.

---

# 10. La struttura concettuale dell'intero saggio

L'impianto argomentativo di Alessio Erioli si snoda lungo questa catena consequenziale:

**IL PARADOSSO DELL'ASSEMBLAGGIO COMPUTAZIONALE IN ARCHITETTURA**

↓

**FONDAZIONE FILOSOFICA: DELEUZE, DELANDA E LA MEREOLOGIA**
(relazioni di esteriorità e co-determinazione parte-tutto)

↓

**L'AUTOMAZIONE COME RETE DECISIONALE DISTRIBUITA (BENJAMIN BRATTON)**

↓

**I PRECURSORI: ALEXANDER, FRIEDMAN (*FLATWRITER*), PRICE (*GENERATOR*)**

↓

**ARCHITETTURA DI ASSEMBLER: PLUGIN PER RHINO-GRASSHOPPER**
(approccio scale-agnostic e ciclo operativo iterativo a 3 stadi)

↓

**ANATOMIA DELLE COMPONENTI: ASSEMBLYOBJECTS (CON FOCUS SUL VUOTO) ED HANDLES**

↓

**INTERAZIONE CON IL CONTESTO: CAMPI TENSORIALI VOXEL (*TENSOR FIELDS*)**
(scalari, vettori e pesi interi che guidano la crescita spaziale)

↓

**LA CIRCOLAZIONE COME DISCRIMINANTE ONTOLOGICA TRA AGGREGATO E ARCHITETTURA**

↓

**IL MONITO DI BILL HILLIER CONTRO L'ARS COMBINATORIA CIECA**

↓

# VERSO UN'INTEGRAZIONE TRA MEREOLOGIA COMPUTAZIONALE E REINFORCEMENT LEARNING

---

## Il concetto più importante da portarsi via

Se dovessi condensare l'intero saggio di Alessio Erioli in una sola idea, direi questa:

> **L'assemblaggio architettonico non è una sommatoria decorativa di blocchi geometrici, ma un processo mereologico e relazionale in cui parti, vuoti e connessioni co-evolvono attraverso campi informativi e flussi di circolazione, trasformando il design in una rete decisionale automatizzata capace di generare una straordinaria ricchezza spaziale da una sintassi minima di elementi.**
