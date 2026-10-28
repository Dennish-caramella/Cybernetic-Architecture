# 1. La tesi centrale di *Combinatorial Design*

Presentato alla conferenza ACADIA nel 2016 da Jose Sanchez (architetto, programmatore, game designer e docente alla University of Southern California), il saggio *Combinatorial Design: Non-parametric Computational Design Strategies* segna un momento di rottura fondamentale nella teoria dell'architettura digitale contemporanea.

Sanchez attacca frontalmente l'egemonia culturale e tecnica del **design parametrico**, che per oltre due decenni ha dominato le avanguardie computazionali identificandosi (specialmente attraverso i manifesti di Patrik Schumacher) come l'unico stile legittimo dell'era digitale. 

La tesi fondamentale di Sanchez è che:

> **L'architettura computazionale non coincide necessariamente con la variazione continua, i gradienti e le superfici lisce curvilinee (NURBS); esiste una strategia alternativa, radicale e non-parametrica — il *Combinatorial Design* — fondata sulla permutazione, sulla combinazione e sulla riconfigurazione di insiemi finiti di unità discrete.**

Mentre il modello parametrico opera attraverso domini numerici continui, funzioni matematiche infinitesime e forme organiche indistinte in cui le singole parti si dissolvono nel flusso della superficie, il design combinatorio opera attraverso la **granularità delle parti**, la sintassi dell'assemblaggio e l'interazione uomo-macchina mediata dal linguaggio dei videogiochi.

```text
DESIGN PARAMETRICO (Continuo):
Funzioni infinitesime → NURBS / Mesh → Variazione fluida / Gradienti → Forma fissa

DESIGN COMBINATORIO (Discreto):
Unità finite autonome → Regole di connessione → Patterning granulare → Riconfigurabilità
```

Da questa premessa scaturiscono le opposizioni concettuali decisive:

**continuo (calcolo infinitesimale) ↔ discreto (insiemi finiti combinatori)**

**superficie fluida (NURBS) ↔ assemblaggio granulare (*granular assembly*)**

**ottimizzazione tecnocratica chiusa (Terzidis) ↔ simulazione aperta e contingente**

**olismo totalizzante (la parte sottomessa al tutto) ↔ *Unit Operations* (autonomia delle parti)**

**catena logistica centralizzata fordista ↔ manifattura additiva distribuita a costo marginale zero**

**struttura permanente irreversibile ↔ kit tettonico reversibile e riciclabile**

---

# 2. Il contesto disciplinare: l'apogeo e la crisi del Parametricismo

Il saggio si colloca all'interno della transizione storica degli anni Dieci tra la prima stagione del digitale (caratterizzata dal "blob", dalle superfici a doppia curvatura e dal formalismo di Grasshopper/Rhino) e la nascita del movimento del **Discrete** (rappresentato da figure come Gilles Retsin, Daniel Koehler, Mollie Claypool e lo stesso Jose Sanchez):

- l'ascesa del "Parametricismo" teorizzato da Patrik Schumacher (Zaha Hadid Architects), criticato per l'eccessivo formalismo estetizzante e per i costi costruttivi insostenibili legati alla non-standardizzazione estrema di ogni singolo pannello;
- la diffusione dei motori grafici per videogiochi (come Unity3D e Unreal Engine) all'interno della ricerca architettonica;
- la rinascita dell'interesse filosofico per l'ontologia orientata agli oggetti (OOO) e per la teoria dei giochi;
- l'emergere della stampa 3D e della fabbricazione additiva distribuita come alternativa alla logistica industriale tradizionale.

Sanchez intende liberare la computazione architettonica dal monopolio delle superfici continue, dimostrando che il "discreto" non è un ritorno all'arretratezza prefabbricata del dopoguerra, ma il livello più avanzato dell'ecologia digitale.

---

# 3. La critica al paradigma parametrico: NURBS e calcolo infinitesimale

Sanchez spiega il meccanismo matematico che ha guidato l'architettura parametrica: essa ha prosperato all'interno degli ambienti geometrici basati sulle **NURBS** (*Non-Uniform Rational B-Splines*).

Nelle NURBS:
- la geometria è definita non da vertici e spigoli rigidi, ma da curve di Bézier e formule razionali continue;
- un punto su una curva rappresenta una posizione infinitesima lungo un dominio continuo, controllabile tramite uno slider numerico;
- la geometria viene espressa attraverso rapporti di curvatura e gradienti scalari.

Questo impianto matematico ha creato una *"via di minor resistenza formale"*: gli algoritmi generano spontaneamente forme aerodinamiche, fluide e contigue. 

Il problema denunciato da Sanchez è epistemologico: la disciplina ha scambiato un **particolare formalismo matematico continuo** per la totalità della computazione architettonica, soffocando altre tassonomie di calcolo radicalmente diverse, prime fra tutte la combinatoria discreta.

---

# 4. Combinatorial Design vs Permutation Design: la critica a Kostas Terzidis

Sanchez stabilisce una netta linea di demarcazione tra la sua proposta e quello che Kostas Terzidis definisce *Permutation Design* (2014).

### Il Permutation Design di Terzidis
- Considera ogni variabile di un problema di design come un grado di libertà.
- Sostiene che combinando esaustivamente tutti i parametri tramite un algoritmo di ricerca profonda (*deep search*), il calcolatore troverà la "soluzione ottimale assoluta" (*the best solution*).
- Terzidis rigetta l'intuizione, l'esperienza e la soggettività umana, considerate fonti di arbitrio e distorsione.

### La replica critica di Sanchez
Sanchez confuta la tesi dell'ottimizzazione esaustiva su due livelli:

1. **Impossibilità computazionale**: In un sistema ad assemblaggio combinatorio, lo spazio delle soluzioni cresce in maniera esponenziale con l'aggiunta di ogni singola unità. Cercare esaustivamente l'optimum globale diventa matematicamente non calcolabile in tempi utili (problema NP-completo).
2. **Mito tecnocratico**: Non esiste una "soluzione ottimale" eterna per un edificio. La pertinenza di un assetto spaziale è sempre **contingente, contestuale e temporale**.

Il design combinatorio non cerca l'algoritmo onnisciente che sostituisca l'architetto; progetta invece piattaforme interattive in cui l'intuizione umana e i vincoli algoritmici cooperano all'interno di un processo decisionale aumentato.

---

# 5. La matrice teorica di Ian Bogost: *Unit Operations* e ontologia delle parti

Per fondare teoricamente la nozione di assemblaggio discreto, Sanchez ricorre al pensiero del teorico dei media e game designer Ian Bogost (*Unit Operations: An Approach to Videogame Criticism*, 2006).

Bogost propone di leggere qualsiasi medium espressivo (poetico, letterario, cinematografico o computazionale) come un **sistema configurativo di unità discrete interconnesse** (*unit operations*).

Punti chiave del modello di Bogost applicati all'architettura da Sanchez:

- **Autonomia della parte rispetto al tutto**: In un sistema organico olistico tradizionale, le parti sono subordinate e sacrificate alla totalità superiore dell'edificio. Nelle *unit operations*, la parte mantiene la propria individualità ontologica e la propria autonomia funzionale.
- **Sistemi come moltitudini**: Il sistema non è una totalità assoluta e piramidale, ma il risultato spontaneo e complesso di **moltitudini di unità** che cooperano liberamente.
- **La lotta contro il collasso totalizzante**: Citando Heidegger, Bogost ricorda che le unità devono costantemente resistere alla tendenza dei sistemi a collassare in ordini autoritari totalizzanti.

Da qui nasce il concetto chiave di Sanchez:

# GRANULAR ASSEMBLIES (ASSEMBLAGGI GRANULARI)

La granularità non è un semplice dettaglio costruttivo, ma la condizione ontologica che garantisce **reversibilità, riconfigurabilità temporale e libertà aggregativa**.

---

# 6. Il programma di ricerca triennale: *Polyomino Studio* (USC)

Per testare operativamente la teoria combinatoria, Sanchez ha guidato dal 2013 un programma di ricerca sperimentale triennale alla School of Architecture della University of Southern California (USC), denominato *Polyomino*.

Il mandato dello studio consisteva nel progettare un **sistema costruttivo combinatorio** capace di generare una vasta gamma di condizioni architettoniche sia in ambito fisico (prototipi, modelli 1:1, stampa 3D) sia in ambito digitale (simulazioni interattive in Unity3D e Realtà Virtuale).

---

# 7. Evoluzione di Polyomino: Anno 1 — Rottura di simmetria

### A. Che cos'è
La prima iterazione della ricerca, incentrata sulla geometria dell'ottaedro troncato.

### B. Come funziona
- L'ottaedro troncato funge da volume di inviluppo spaziale entro cui inscrivere componenti complesse.
- Gli studenti applicano operazioni di rottura di simmetria (*symmetry breaking*) per definire connessioni strutturali orientate.
- Vengono codificati algoritmi in Unity3D per consentire l'ancoraggio magnetico e l'allineamento automatico dei pezzi durante l'interazione digitale.

### C. Perché è importante
Dimostra che la ripetizione di un componente geometrico discreto può produrre spazialità ricche e differenziate senza ricorrere alla deformazione fluida dei singoli pezzi.

---

# 8. Evoluzione di Polyomino: Anno 2 — Il giunto scorrevole (*Sliding Joint*)

### A. Che cos'è
Un esperimento ibrido concepito come punto di contatto tra combinatoria discreta e variazione continua parametrica.

### B. Come funziona
- Progettazione di un elemento dotato di due tipi di connessione:
  1. Connessione discreta faccia-a-faccia con 4 rotazioni prefissate;
  2. Connessione a scorrimento continuo (*sliding joint*) su facce parallele.
- Il giunto scorrevole introduce una serie infinitesima di posizioni relative tra due pezzi, consentendo la creazione di gradienti di densità e fasciature strutturali.

### C. Perché è importante
Funziona come banco di prova teorico: dimostra che un telaio combinatorio può assorbire al suo interno gradi di differenziazione analogica senza perdere la propria matrice discreta.

---

# 9. Evoluzione di Polyomino: Anno 3 — Pura combinatoria e padiglione ad alte prestazioni

### A. Che cos'è
Il culmine del programma: la messa a punto di un'unica unità intelligente combinata ricorsivamente per la realizzazione di un padiglione architettonico completo.

### B. Come funziona
- Definizione di una singola smart unit in legno e metallo capace di connettersi a se stessa secondo una vasta gamma di permutazioni.
- Creazione di un vocabolario formale di aggregazioni analizzate scientificamente per:
  - capacità strutturale;
  - porosità e passaggio della luce solare;
  - ricorsività e delineazione spaziale.
- Introduzione di un sistema di *packing* con eccezioni: l'80% delle unità rispetta la griglia principale, mentre il 20% infrange i piani di allineamento creando varchi, curve e tensioni spaziali.

### C. Perché è importante
Dimostra la piena maturità tettonica del Combinatorial Design: un'unica unità geometrica elementare genera fondazioni, pareti, aperture, coperture e texture superficiali.

### D. Principio generale

> **Una sola unità discreta + Regole di permutazione = Complessità architettonica totale**

---

# 10. Il videogioco come ambiente di progettazione: Unity3D e Realtà Virtuale

Uno degli apporti più originali del lavoro di Sanchez è la radicale ridefinizione dell'interfaccia di disegno.

Sanchez respinge l'interfaccia convenzionale dei software CAD/BIM tradizionali (modellazione vertice per vertice, comandi complessi di allineamento e rotazione) e sviluppa **piattaforme di gioco in Unity3D e Realtà Virtuale (VR)**.

Il meccanismo è profondamente cibernetico:
- Il computer calcola istantaneamente le regole di vincolo, collisione e snapping geometrico dei moduli.
- L'utente opera come un **giocatore all'interno di una simulazione guidata**, posizionando i moduli in tempo reale con feedback immediato su stabilità e prestazioni.
- La simulazione genera una **narrativa ramificata**: ogni mossa apre o chiude determinati percorsi geometrici.

Si realizza così un anello di feedback continuo:

```text
VINCOLI COMPUTAZIONALI DEL MOTORE DI GIOCO
                   ↕  [ feedback in tempo reale ]
INTUIZIONE, SENSIBILITÀ ED ESPERIENZA DELL'ARCHITETTO
```

---

# 11. Produzione distribuita e Crowdsourcing: la convergenza con Jeremy Rifkin

Sanchez connette la ricerca tettonica alle trasformazioni socio-economiche descritte dall'economista Jeremy Rifkin in *The Zero Marginal Cost Society* (2014):

- Nella società industriale fordistica, la produzione modulare richiedeva colossali catene di montaggio centralizzate e una logistica di trasporto planetaria ad alto impatto ecologico.
- Nell'era di Internet e della fabbricazione digitale, il file di un'unità discreta può essere trasmesso digitalmente via web e stampato localmente tramite macchine additive a controllo numerico (come le stampanti Stratasys utilizzate nella ricerca).

Questa convergenza abilita il **Crowd-sourced Design**:
- Gli utenti non sono consumatori passivi di scatole prefabbricate;
- Attraverso videogiochi interattivi accessibili (come *Block'hood*, il celebre videogame urbano sviluppato da Sanchez), comunità di cittadini possono negoziare, progettare e adattare i propri manufatti;
- Le parti difettose o obsolete vengono smontate, riciclate o ristampate singolarmente senza demolire l'intero edificio.

---

# 12. La struttura concettuale dell'intero saggio

L'impianto argomentativo di Jose Sanchez può essere sintetizzato in questa catena logica:

**CRITICA ALL'EGEMONIA DEL PARAMETRICISMO CONTINUO (NURBS)**

↓

**RIFIUTO DELL'OTTIMIZZAZIONE ESAUSTIVA CHIUSA (TERZIDIS)**

↓

**FONDAZIONE DEL COMBINATORIAL DESIGN (INSIEMI DISCRETI FINITI)**

↓

**RADICI ONTOLOGICHE: IAN BOGOST E LE "UNIT OPERATIONS"**
(autonomia delle unità vs olismo totalizzante)

↓

**GRANULAR ASSEMBLIES: TETTONICA DELLA REVERSIBILITÀ**

↓

**SPERIMENTAZIONE POLYOMINO STUDIO (USC)**
(dalla rottura di simmetria al padiglione ad alte prestazioni)

↓

**IL VIDEOGIOCO (UNITY3D/VR) COME AMBIENTE DI DECISIONE AUMENTATA**

↓

**FUSIONE CON I COMMONS E LA PRODUZIONE DISTRIBUITA (RIFKIN / STRATASYS)**

↓

# ARCHITETTURA COME SISTEMA DI GIOCO DISCRETO, PARTECIPATIVO E CIRCOLARE

---

## Il concetto più importante da portarsi via

Se dovessi condensare l'intero saggio di Jose Sanchez in una sola idea, direi questa:

> **Il Combinatorial Design dimostra che la vera avanguardia digitale non risiede nelle superfici lisce e deformabili del parametricismo, ma nell'intelligenza sintattica di assemblaggi granulari discreti, capaci di trasformare la progettazione in un gioco simulativo condiviso e l'architettura in un bene comune aperto, riparabile e continuamente riconfigurabile.**
