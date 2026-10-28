# 1. La tesi centrale di *An Approach to Cybernetics*

Pubblicato nel 1961 a Londra (Hutchinson) con la celebre prefazione del neurofisiologo Warren S. McCulloch, *An Approach to Cybernetics* di Gordon Pask è uno dei trattati fondativi e più visionari dell'intera storia della cibernetica.

Il punto di partenza di Pask è la constatazione che la scienza occidentale classica — frammentata in compartimenti stagni tra fisica, biologia, psicologia ed economia — è strutturalmente incapace di spiegare i comportamenti complessi che caratterizzano sia gli organismi viventi sia le macchine evolute: **l'adattamento, l'apprendimento, l'auto-regolazione, l'evoluzione e l'auto-organizzazione**.

La tesi fondamentale di Gordon Pask è che:

> **La cibernetica non è una branca dell'ingegneria o dell'informatica, ma una disciplina epistemologica transdisciplinare autonoma che studia la forma e l'organizzazione dei sistemi a prescindere dal loro supporto materiale; il suo nucleo risiede nella comprensione di come i sistemi mantengano la stabilità attraverso il controllo della varietà (*Ashby's Law of Requisite Variety*), evolvano attraverso l'interazione con l'osservatore e sviluppino un'intelligenza conversazionale condivisa.**

Pask dimostra che il controllo non è un atto autoritario unidirezionale, ma una **relazione circolare e dialogica**: un sistema di controllo apprende dall'ambiente tanto quanto l'ambiente è modificato dal sistema.

```text
CONTROLLO MECCANICO CLASSICO:
Controllore ──[ comando fisso ]──► Macchina/Processo inerte

CONTROLLO CIBERNETICO ADATTIVO (Pask):
Controllore Adattivo ◄──[ ciclo continuo di feedback e varietà ]──► Ambiente Dinamico
                      (co-evoluzione, apprendimento, conversazione)
```

Da questa premessa discendono le trasformazioni concettuali decisive del volume:

**osservatore esterno distaccato ↔ osservatore come partecipante sistemico attivo**

**macchina a stati finiti rigida ↔ artefatto adattivo ed evolutivo**

**riduzionismo fisico-meccanico ↔ teoria formale dell'organizzazione e dell'informazione**

**comando gerarchico discendente ↔ regolazione omeostatica circolare (*feedback loop*)**

**insegnamento come trasmissione passiva ↔ interazione simbiotica uomo-macchina (SAKI)**

**hardware elettronico fisso ↔ calcolatori elettrochimici auto-generativi (*chemical computers*)**

---

# 2. Il contesto storico ed epistemologico: la prima e la seconda cibernetica

Il testo si colloca all'apice dell'età dell'oro della cibernetica internazionale (fine anni '50 e primi anni '60), collegando direttamente le ricerche britanniche con quelle statunitensi:

- le conferenze Macy (1946–1953) promosse da Warren McCulloch e Norbert Wiener;
- la formulazione della Teoria dell'Informazione di Claude Shannon (1948) e del concetto di omeostasi di W. Ross Ashby (*Design for a Brain*, 1952; *An Introduction to Cybernetics*, 1956);
- le teorie sugli automi cellulari e l'auto-riproduzione delle macchine di John von Neumann;
- l'emergere della cibernetica del management industriale con Stafford Beer (*Cybernetics and Management*, 1959);
- la transizione verso la **Second-Order Cybernetics** (la cibernetica dei sistemi osservanti) formulata all'Università dell'Illinois da Heinz von Foerster (a cui Pask dedica espliciti ringraziamenti nel volume).

Nella densa prefazione, Warren McCulloch definisce il libro come *"l'ibridazione feconda tra Arte e Scienza che genera oggetti inanimati capaci di comportarsi come sistemi viventi: sopravvivono, si regolano, si adattano, calcolano e inventano"*.

---

# 3. Capitolo 1 — Le origini della cibernetica e i falsi miti

Pask apre il trattato definendo lo statuto epistemologico della disciplina:

La cibernetica taglia trasversalmente i dipartimenti delle scienze naturali: non guarda all'economia come un economista, alla biologia come un biologo o ai motori come un ingegnere. In ogni campo, il suo tema unificante rimane lo stesso: **come i sistemi si regolano, come apprendono, come si riproducono e, soprattutto, come si auto-organizzano**.

Pask sfata tre luoghi comuni pericolosi:
1. **La cibernetica non è la scienza dei calcolatori elettronici**: I computer digitali sono solo uno dei possibili supporti fisici per incarnare processi logici; la cibernetica si applica ugualmente al sistema respiratorio umano, alle colonie di insetti o alle fabbriche.
2. **La cibernetica non è pura automazione industriale**: L'automazione rigida (una pressa meccanica che ripete sempre lo stesso gesto) è anti-cibernetica; la cibernetica richiede plasticità, varietà e risposta all'imprevisto.
3. **La cibernetica non riduce l'uomo a una macchina**: Al contrario, eleva la macchina alla dignità dei processi cognitivi, relazionali ed estetici dell'essere umano.

---

# 4. Capitolo 2 — Apprendimento, Osservazione e Previsione: l'Osservatore sistemico

Uno dei contributi più originali di Pask è la ridefinizione dell'atto scientifico dell'osservazione.

Un **osservatore** (*observer*) non è una telecamera neutra posta all'esterno dell'universo, ma un uomo, un animale o una macchina capace di compiere rilevazioni empiriche, registrare stati ed elaborare previsioni sul comportamento futuro di un sistema.

Pask introduce formalmente:
- **Lo Spazio delle Fasi (*Phase Space*)**: Lo spazio multidimensionale in cui ogni asse rappresenta una variabile misurabile del sistema e ogni punto descrive lo stato istantaneo del sistema.
- **La fonte dell'incertezza**: L'incertezza scaturisce sia dalla complessità intrinseca delle interazioni tra le parti sia dai limiti di risoluzione sensoriale e temporale dell'osservatore.
- **La misura dell'informazione (Shannon)**: L'informazione trasmessa è calcolata rigorosamente come **riduzione dell'incertezza** (entropia negativa) nello spazio degli stati possibili.

---

# 5. Capitolo 3 — Il comportamento determinato dallo stato (*State Determined Behaviour*)

Pask analizza le condizioni matematiche sotto cui un sistema può essere modellato:

### Sistemi stazionari e deterministici
Sistemi in cui lo stato successivo al tempo $t+1$ è univocamente determinato dallo stato attuale al tempo $t$ e dagli input ambientali. Raggiungono stati di equilibrio stabile (attrattori).

### Sistemi stocastici e catene markoviane
Sistemi complessi in cui le transizioni tra stati sono probabilistiche: lo stato presente determina la *probabilità di transizione* verso gli stati futuri.

### Linguaggio oggetto e Metalinguaggio
Pask introduce una fondamentale distinzione logica:
- Il **linguaggio oggetto** (*object language*) è il codice utilizzato per descrivere gli stati interni e le operazioni dirette del sistema.
- Il **metalinguaggio** (*metalanguage*) è il linguaggio di livello superiore utilizzato dall'osservatore o dal supervisore per ridefinire le regole stesse del sistema quando l'ambiente muta.

### Il sistema auto-organizzante (*Self-Organizing System*)
Un sistema è autenticamente auto-organizzante quando non si limita a cambiare posizione nello spazio degli stati, ma **modifica internamente la propria struttura e le proprie regole di connessione**, aumentando la propria ridondanza e capacità di apprendimento.

---

# 6. Capitolo 4 — Sistemi di Controllo e la Legge della Varietà Necessaria di Ashby

Il quarto capitolo costituisce l'architrave teorica del volume: come si progetta un controllore capace di governare un ambiente mutevole?

Pask pone al centro la celebre **Legge della Varietà Necessaria** formulata da W. Ross Ashby (*Law of Requisite Variety*):

> **"Only variety can destroy variety" (Solo la varietà può assorbire o distruggere la varietà).**

Se un ambiente presenta una varietà di disturbi pari a $V_E$, il controllore potrà mantenere il sistema in uno stato di stabilità accettabile solo se possiede una capacità interna di varietà e di risposte $V_C$ almeno pari a quella dei disturbi:

$$V_C \ge V_E$$

Se il controllore è rigido e possiede meno varietà dell'ambiente, il sistema andrà inevitabilmente fuori controllo.

Pask classifica cinque generazioni di controllori:
1. **Controllori perfetti e imperfetti**: Controllori con informazione completa dello stato vs controllori con canali sensoriali degradati.
2. **Controllori predittivi**: Dispositivi capaci di anticipare l'evoluzione temporale dell'ambiente simulando scenari futuri prima di agire.
3. **Macchine a probabilità condizionata (*Conditional Probability Machines*)**: Algoritmi che aggiornano costantemente le probabilità a posteriori sulla base della storia passata.
4. **Controllori imitativi**: Sistemi capaci di apprendere copiando il comportamento di un operatore esperto.
5. **Controllori adattivi (*Adaptive Control Systems*)**: Dispositivi capaci di riorganizzare i propri parametri interni in ambienti non strutturati (*untidy environments*).

---

# 7. Capitolo 5 — Controllori Biologici e Omeostasi

Per dimostrare che i principi cibernetici sono universali, Pask esamina i meccanismi biologici di sopravvivenza negli organismi viventi.

### Il caso studio della regolazione respiratoria
- L'organismo umano deve mantenere costante la concentrazione di anidride carbonica ($CO_2$) nel sangue arterioso e nei tessuti cerebrali.
- **Meccanismo a doppio anello**: I chemiorecettori nel bulbo carotideo e nel midollo allungato rilevano il pH sanguigno; se la concentrazione di $CO_2$ sale, il centro respiratorio accelera il ritmo diaframmatico, espellendo il gas in eccesso.
- Questo ciclo omeostatico biochimico opera secondo le medesime equazioni servomeccaniche a circuito chiuso dei termostati industriali, ma con una resilienza e una ridondanza incomparabilmente superiori.

### Gli artefatti cerebrali e il riconoscimento delle forme (*Pattern Recognition*)
Pask analizza i modelli matematici delle reti neurali artificiali (Warren McCulloch e Walter Pitts, 1943; il *Perceptron* di Frank Rosenblatt, 1958; e il *Pandemonium* di Oliver Selfridge). Dimostra che l'estrazione di invarianti e l'astrazione di forme visive scaturiscono dalla competizione tra rilevatori locali di caratteristiche che cooperano per classificare lo stimolo visivo.

---

# 8. Capitolo 6 — Le Macchine per Insegnare (*Teaching Machines*) e SAKI

Questo capitolo descrive una delle invenzioni storiche più celebri di Gordon Pask: le **macchine adattive per l'istruzione**.

Pask rifiuta la visione comportamentista rigida di B.F. Skinner (macchine meccaniche che somministrano test a crocette standardizzati). Al contrario, progetta una macchina che instaura una vera e propria **conversazione simbiotica** con l'allievo.

### Il caso studio di SAKI (Self-Adaptive Keyboard Instructor, 1956)
- **Che cos'è**: Una macchina elettronica cibernetica progettata da Pask per addestrare gli operatori all'uso rapido delle tastiere per schede perforate (Hollerith card punching).
- **Come funziona**:
  - SAKI presenta all'allievo un esercizio su una matrice luminosa e misura istantaneamente il tempo di reazione (latenza) e gli errori di digitazione.
  - Se l'allievo è insicuro o commette errori, SAKI **rallenta il ritmo e accende spie luminose guida (cues)** per suggerire il tasto corretto.
  - Man mano che l'allievo acquisisce scioltezza, SAKI **ritira progressivamente gli aiuti luminosi e aumenta la velocità**, spingendo l'allievo al limite massimo delle sue facoltà cognitive.
- **La gestione della Varietà e dell'Attenzione**:
  Pask applica qui la legge di Ashby: per mantenere l'attenzione dell'allievo desta ed evitare noia o frustrazione, la macchina deve erogare un flusso di novità e sfida (*variety*) esattamente calibrato sulle capacità momentanee dello studente.

SAKI dimostra che l'apprendimento non è un'assimilazione passiva di dati, ma un processo di **auto-organizzazione condivisa** tra mente umana e macchina adattiva.

---

# 9. Capitolo 7 — Evoluzione, Riproduzione e i *Chemical Computers*

In questo capitolo visionario, Pask affronta la possibilità per le macchine di riprodursi ed evolvere spontaneamente.

Dopo aver analizzato i modelli formali di John von Neumann sugli automi cellulari capaci di produrre copie di se stessi, Pask introduce una tecnologia rivoluzionaria da lui personalmente inventata e brevettata: i **Calcolatori Elettrochimici (*Chemical Computers*)**.

### A. Che cos'è il Chemical Computer di Pask
Un computer non-digitale che non utilizza valvole termoioniche, transistor al silicio o fili di rame prefissati, ma una capsula poco profonda in Perspex riempita con una **soluzione acida conduttiva di solfato ferroso ($FeSO_4$)** e dotata di una matrice di elettrodi metallici immersi.

### B. Come funziona: la crescita di alberi metallici conduttivi
- Quando viene applicata una differenza di potenziale elettrico tra gli elettrodi, il ferro si deposita elettrochimicamente formando **sottilissimi filamenti metallici dendritici** (strutture ramificate simili ad assoni neuronali o radici arboree).
- Questi filamenti crescono spontaneamente nello spazio liquido seguendo le linee di flusso della massima densità di corrente (principio di minima resistenza).
- Se un percorso conduce troppa corrente, si riscalda e si dissolve; se ne conduce la giusta quantità, il filo metallico si consolida e si ispessisce per deposizione ionica.

### C. La comparsa dell'adattamento e dell'orecchio sensoriale
Pask compie un esperimento straordinario:
- Premia il sistema fornendo corrente elettrica ogni volta che i filamenti crescono in modo da correlare specifici stimoli esterni.
- In un celebre esperimento, posiziona un altoparlante vicino alla bacinella chimica: le vibrazioni sonore generano onde meccaniche nel liquido che perturbano la crescita dei filamenti.
- Nel giro di poche ore, **la rete elettrochimica sviluppa spontaneamente un "orecchio"**: la struttura ramificata impara a distinguere un tono a 50 Hz da un tono a 100 Hz per massimizzare l'afflusso di energia, auto-organizzando la propria connettività senza alcuna programmazione umana a monte!

### D. Quale principio generale possiamo estrarne

> **L'intelligenza computazionale non richiede un hardware rigido pre-disegnato dall'uomo: la materia chimica può auto-organizzare la propria struttura vivente attraverso processi evolutivi di crescita e selezione elettrochimica.**

---

# 10. Capitolo 8 — Cibernetica Industriale e Organizzativa: la convergenza con Stafford Beer

Nell'ultimo capitolo, Pask estende la cibernetica alla scala dei grandi sistemi produttivi, industriali e sociali:

- Citando il lavoro pionieristico di Stafford Beer, dimostra che un'azienda industriale o una fabbrica non possono essere gestite attraverso organigrammi piramidali statici.
- L'industria è un **sistema probabilistico ultra-complesso** immerso in un mercato economico instabile.
- La direzione aziendale deve operare come un controllore omeostatico capace di gestire le risorse attraverso filtri di varietà, bilanciando scorte di magazzino, cicli di produzione, domanda di mercato e benessere dei lavoratori.

---

# 11. La struttura concettuale dell'intero trattato

L'architettura teorica di *An Approach to Cybernetics* si sviluppa lungo questa catena consequenziale:

**LA CIBERNETICA COME SCIENZA FORMALE DELL'ORGANIZZAZIONE**

↓

**L'OSSERVATORE PARTECIPANTE E LO SPAZIO DEGLI STATI FONDAMENTALE**

↓

**I SISTEMI STOCASTICI E IL METALINGUAGGIO SUPERIORE**

↓

**LA LEGGE DELLA VARIETÀ NECESSARIA DI W. ROSS ASHBY**
(solo la varietà assorbe la varietà: equazione cardine della stabilità)

↓

**MODELLI DI CONTROLLO ADATTIVO IN AMBIENTI INCERTI**

↓

**L'OMEOSTASI BIOLOGICA: IL CICLO RESPIRATORIO E LE RETI NEURALI**

↓

**LE MACCHINE PER INSEGNARE: SAKI E L'APPRENDIMENTO SIMBIOTICO**
(conversazione adattiva tra mente umana e calcolatore)

↓

**LA MATERIA VIVENTE INORGANICA: I CHEMICAL COMPUTERS DI PASK**
(crescita elettrochimica di reti conduttive e comparsa dell'orecchio sensoriale)

↓

**LA CIBERNETICA INDUSTRIALE E ORGANIZZATIVA (STAFFORD BEER)**

↓

# LA CIBERNETICA COME SCIENZA DELL'AUTO-ORGANIZZAZIONE DELLA VITA E DELL'ARTEFATTO

---

## Il concetto più importante da portarsi via

Se dovessi condensare l'intero trattato di Gordon Pask in una sola idea, direi questa:

> **La cibernetica rivela che il controllo non è un atto autoritario di coercizione della materia, ma una conversazione circolare di mutuo adattamento: sia essa incarnata in un organismo biologico, in un'aula scolastica o in una bacinella chimica che sviluppa filamenti conduttivi, la vita e l'intelligenza emergono ovunque un sistema possieda sufficiente varietà interna per dialogare con la complessità del mondo.**
