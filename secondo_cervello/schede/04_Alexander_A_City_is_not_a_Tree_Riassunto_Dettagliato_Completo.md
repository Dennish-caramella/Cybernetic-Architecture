# 1. La tesi centrale di *A City is not a Tree*

Pubblicato nel 1965 sulla rivista *Architectural Forum*, *A City is not a Tree* di Christopher Alexander è uno dei saggi più celebri e dirompenti della teoria urbana del Novecento.

Alexander parte da una constatazione empirica drammatica: le città contemporanee progettate a tavolino dagli urbanisti e dagli architetti moderni sono asettiche, prive di vitalità, incapaci di sostenere la complessità della vita umana e fonte di profonda alienazione sociale. Al contrario, le città storiche sorte spontaneamente nel corso dei secoli possiedono un'incredibile ricchezza relazionale, resilienza e fascino.

La causa di questo fallimento non risiede in un deficit di gusto estetico, nell'uso di materiali sbagliati o nella carenza di alberi ed edifici scenografici. La causa è puramente **strutturale e topologica**:

> **La città naturale è un semireticolo (*semi-lattice*); ma quando gli architetti e i pianificatori progettano una città artificiale, la concepiscono invariabilmente come un albero (*tree*).**

L'albero e il semireticolo sono due strutture matematiche astratte che organizzano le relazioni tra le parti di un insieme.

Mentre l'albero impone una gerarchia rigida di contenimento a compartimenti stagni senza sovrapposizioni, il semireticolo consente a elementi e sottosistemi diversi di **sovrapporsi, intersecarsi e condividere componenti** (*overlap*).

```text
ALBERO (Tree):
Ogni elemento appartiene a un solo ramo. Nessuna sovrapposizione tra rami fratelli.
Compartimentazione rigida, isolamento funzionale.

SEMIRETICOLO (Semi-lattice):
I sistemi si intersecano liberamente. Un elemento può appartenere a molteplici insiemi.
Molteplicità relazionale, complessità viva, ambiguità fertile.
```

Da questa frattura derivano le opposizioni concettuali decisive del saggio:

**città naturale (spontanea) ↔ città artificiale (pianificata)**

**gerarchia ad albero ↔ rete a semireticolo**

**compartimentazione disgiunta ↔ sovrapposizione (*overlap*) di insiemi**

**semplicità cognitiva della mente ↔ complessità sistemica del mondo reale**

**isolamento sociale dei sobborghi ↔ vitalità polifonica dello spazio pubblico**

**forma estetica esteriore ↔ principio generativo profondo**

---

# 2. Il contesto storico e culturale: la crisi dell'urbanistica modernista

Il saggio nasce a metà degli anni Sessanta, in un momento di aperta contestazione dei paradigmi della Carta d'Atene e della pianificazione funzionalista:

- la costruzione delle *New Towns* britanniche del dopoguerra (come Cumbernauld, Hook, Stevenage), elogiate dalla critica tecnica ma percepite dagli abitanti come noiose e disumanizzanti;
- l'inaugurazione monumentale di grandi capitali pianificate ex-novo: Chandigarh di Le Corbusier (1951) e Brasilia di Lúcio Costa e Oscar Niemeyer (1960);
- la pubblicazione nel 1961 di *Vita e morte delle grandi città americane* di Jane Jacobs, che denunciava lo sventramento dei quartieri tradizionali newyorkesi operato dal modernismo e dal traffico automobilistico;
- la diffusione della topologia, della teoria dei grafi e della cibernetica nelle scienze umane e ambientali.

Alexander, forte della sua doppia formazione in matematica a Cambridge e in architettura ad Harvard, non si limita a una critica impressionistica o nostalgica: fornisce una **dimostrazione logico-matematica** dell'errore epistemologico commesso dall'urbanistica moderna.

---

# 3. Città naturali vs Città artificiali

Alexander stabilisce in apertura una distinzione fondamentale tra due tipologie di insediamenti:

### Città naturali (*natural cities*)
- Sorti più o meno spontaneamente attraverso processi incrementali durati secoli o millenni.
- Esempi: Siena, Kyoto, Manhattan, Liverpool, i villaggi medievali italiani, Greenwich Village.
- Caratteristica: un'infinita complessità relazionale, un tessuto a maglia fitta in cui residenza, commercio, socialità, istituzioni e movimento si intrecciano continuamente.

### Città artificiali (*artificial cities*)
- Create deliberatamente a tavolino da progettisti, urbanisti e amministrazioni pubbliche in un unico atto pianificatorio.
- Esempi: Levittown, Chandigarh, Brasilia, le New Towns britanniche, i grandi quartieri suburbani americani.
- Caratteristica: ordine visivo geometrico evidente sulla carta, ma totale povertà funzionale e assenza di vitalità urbana reale.

Alexander mette in guardia: il problema non si risolve tentando di imitare lo stile esteriore delle città storiche (costruendo finte piazze rinascimentali o vicoli pittoreschi). Finché non si comprende il **principio d'ordine astratto** che rende viva la città naturale, qualsiasi tentativo di imitazione produrrà solo un parco a tema privo di anima.

---

# 4. Definizione matematica: che cos'è un Albero (*Tree*)

Per comprendere la critica di Alexander occorre definire matematicamente le due strutture a partire dalla teoria degli insiemi.

Sia data una collezione di elementi che formano un insieme $S$. Una collezione di sottoinsiemi di $S$ costituisce una **struttura ad albero** se e solo se:

> **Per ogni coppia di insiemi $A$ e $B$ appartenenti alla struttura, o uno è interamente contenuto nell'altro ($A \subset B$ oppure $B \subset A$), oppure essi sono completamente disgiunti ($A \cap B = \emptyset$).**

In una struttura ad albero:

- non esiste alcuna sovrapposizione parziale;
- due insiemi non possono mai condividere alcuni elementi senza che uno inglobi interamente l'altro;
- l'organizzazione segue una rigida catena gerarchica di scatole cinesi.

```text
ALBERO:
         [ Grande Insieme ]
         /                \
   [ Sottoinsieme 1 ]   [ Sottoinsieme 2 ]
      /          \          /          \
   [A]           [B]      [C]          [D]
   
Regola: [A] e [C] non possono MAI comunicare se non risalendo fino alla radice!
```

---

# 5. Definizione matematica: che cos'è un Semireticolo (*Semi-lattice*)

Al contrario, una collezione di sottoinsiemi di $S$ costituisce un **semireticolo** se e solo se:

> **Per ogni coppia di insiemi $A$ e $B$ appartenenti alla struttura la cui intersezione non è vuota ($A \cap B \neq \emptyset$), anche l'insieme dato dalla loro intersezione ($A \cap B$) appartiene alla struttura.**

In un semireticolo:

- gli insiemi possono incrociarsi liberamente;
- le parti possono appartenere contemporaneamente a più sistemi differenti;
- non vi è una rigida linea di comando discendente, ma una fitta rete di connessioni orizzontali e trasversali.

```text
SEMIRETICOLO:
       [ Insieme 1 ] ─────── [ Insieme 2 ]
             \               /
              \             /
           [ Intersezione Condivisa ]
             /               \
       [ Insieme 3 ] ─────── [ Insieme 4 ]
```

Il semireticolo possiede una capacità combinatoria esponenzialmente superiore rispetto all'albero: un insieme di 20 elementi ammette poche decine di rami in un albero, ma può generare oltre un milione di sottoinsiemi in un semireticolo.

---

# 6. I nove casi studio: le utopie moderne smascherate come alberi

Alexander passa in rassegna nove dei più prestigiosi piani urbanistici moderni del XX secolo, dimostrando che, dietro una finta complessità o un'apparente varietà formale, tutti nascondono la medesima struttura rigida ad albero.

Ciascuno incarna la filastrocca satirica citata da Alexander:
> *"Le grandi pulci hanno piccole pulci sul dorso che le mordono, e le piccole pulci hanno pulci minori, e così via all'infinito."*

### 1. Columbia, Maryland (Community Research and Development Inc.)
- Cinque quartieri elementari formano un villaggio; una serie di villaggi forma la nuova città.
- Struttura: albero perfetto a scatole chiuse.

### 2. Greenbelt, Maryland (Clarence Stein)
- La celebre città-giardino è suddivisa in super-isolati ermetici (*super-blocks*), ciascuno dotato di scuole e parchi interni, collegati da parcheggi periferici.
- Nessuna interpenetrazione tra isolati adiacenti.

### 3. Greater London Plan del 1943 (Patrick Abercrombie e J.H. Forshaw)
- Londra viene riorganizzata come un insieme di comunità autosufficienti e rigidamente separate tra loro da cinture verdi e arterie di traffico, ulteriormente suddivise in quartieri (*neighbourhoods*). Nessuna sovrapposizione tra unità contigue.

### 4. Piano per la Baia di Tokyo (1960) di Kenzo Tange
- Un capolavoro del Metabolismo giapponese strutturato su quattro anelli giganti sulla baia, ciascuno suddiviso in tre anelli medi (stazione, porto, uffici), a loro volta suddivisi in anelli residenziali minori.
- Nonostante la sofisticata tecnologia navale ed espandibile, la logica organizzativa è un albero impeccabile.

### 5. Mesa City di Paolo Soleri
- Le forme biologiche e scultoree sembrano fluide e organiche a prima vista; ma sezionando il piano, il centro universitario è separato dal quartiere residenziale, diviso a sua volta in torri da 4.000 abitanti, a loro volta suddivise in villaggi minori da centinaia di persone.
- Struttura: albero camuffato da scultura biomorfa.

### 6. Chandigarh (1951) di Le Corbusier
- Il settore urbano come cellula autonoma. Un centro monumentale e amministrativo alla testa, un asse commerciale centrale, arterie rigide che dividono la città in 20 settori autosufficienti.
- Ogni settore ha i suoi servizi interni e non dialoga trasversalmente con i settori limitrofi.

### 7. Brasilia (1960) di Lúcio Costa
- Il piano a croce/aeroplano gravita su un asse monumentale centrale da cui dipartono due ali servite da un'unica arteria principale, che alimenta arterie secondarie, che a loro volta alimentano le *superquadras*.
- Totale assenza di intersezioni diagonali o scambi intermedi: un albero puro.

### 8. *Communitas* (Percival e Paul Goodman)
- Quattro zone concentriche disgiunte: centro commerciale cilindrico, anello universitario, anello residenziale e medico, campagna aperta.

### 9. La città di Ludwig Hilberseimer: l'archetipo dell'accampamento militare romano
- Hilberseimer esplicita la matrice ideale della città ad albero: il *castrum* romano. L'esercito è la struttura ad albero per eccellenza, progettata appositamente per imporre disciplina meccanica, eliminare l'ambiguità e impedire iniziative spontanee dal basso.
- Quando una città viene disegnata come un albero, produce sugli abitanti lo stesso effetto disumanizzante di una caserma.

---

# 7. La vita reale come semireticolo: il caso dell'angolo di strada

Per dimostrare come opera la vita in una città naturale, Alexander descrive una minuscola scena di vita quotidiana all'incrocio tra Telegraph Avenue e Bancroft Way a Berkeley.

### La situazione concreta
In questo angolo convivono:
- una farmacia;
- un semaforo pedonale;
- un'edicola con distributori di giornali;
- una fermata dell'autobus;
- una ragazza in attesa dell'autobus che sfoglia una rivista mentre aspetta il verde.

### Il meccanismo dei sistemi sovrapposti
In una manciata di metri quadrati si intersecano quattro sistemi indipendenti:
1. Il sistema del trasporto pubblico urbano (la fermata e la linea dell'autobus);
2. Il sistema commerciale dell'informazione (l'edicola e i quotidiani);
3. Il sistema della regolazione del traffico veicolare (il semaforo);
4. Il sistema sanitario-commerciale (la farmacia).

Ciascuno di questi sistemi fa capo a reti spaziali e istituzionali su scala metropolitana completamente diverse. Eppure, in quell'angolo, la presenza congiunta di questi elementi crea un evento di vita urbana: la ragazza può leggere il giornale, ripararsi dalla pioggia sotto la tenda della farmacia e salire sull'autobus non appena arriva.

Se un urbanista ad albero avesse progettato quello spazio, avrebbe collocato la farmacia nel settore medico, l'edicola nel centro civico commerciale e la fermata su un'arteria di scorrimento isolata, distruggendo la scintilla della vita urbana.

---

# 8. Il fallimento sociale dell'unità di vicinato (*Neighbourhood Unit*)

Alexander demolisce l'idolo indiscusso dell'urbanistica riformista americana ed europea: l'**unità di vicinato**.

I pianificatori hanno postulato che la società moderna debba essere raggruppata in comunità chiuse, gerarchicamente scalari:
```text
Famiglia → Isolato → Vicinato → Quartiere → Città
```

Ma Alexander dimostra che **questa gerarchia non corrisponde ad alcuna realtà sociologica**:

- Nelle società urbane avanzate, le reti di amicizia e di collaborazione professionale di un individuo non coincidono con i vicini di pianerottolo.
- Se chiediamo a un cittadino chi siano i suoi migliori amici e poi poniamo la stessa domanda a ciascuno di questi amici, non otterremo mai un circolo chiuso coincidente con il quartiere, ma una rete aperta a semireticolo dispersa nell'intera area metropolitana.
- Quando i pianificatori confinano le persone all'interno di quartieri chiusi e autosufficienti, pretendendo che le loro relazioni sociali si esauriscano nel raggio di 500 metri, non creano comunità: creano **ghetti fisici e psicologici**.

Il risultato sociologico delle *suburbs* e delle *new towns* ad albero è documentato: solitudine cronica, depressione, nevrosi delle casalinghe isolate e frammentazione atomizzata della società.

---

# 9. Il potere politico reale: il caso di Chicago e Edward Banfield

Alexander rafforza la sua tesi citando lo studio del politologo Edward Banfield (*Political Influence*), dedicato a come vengono prese le decisioni politiche reali nella città di Chicago.

- Se si guarda l'**organigramma formale** nell'ufficio del sindaco, la struttura dell'amministrazione pubblica è un classico **albero**: sindaco → assessori → direttori di dipartimento → funzionari.
- Tuttavia, l'analisi delle dinamiche con cui vengono approvati i grandi progetti urbani dimostra che le linee gerarchiche formali vengono costantemente scavalcate da **linee di influenza *ad hoc***: alleanze trasversali tra imprenditori, comitati civici, sindacati, banche e consiglieri di quartiere.
- La struttura informale che controlla realmente l'azione pubblica cambia da settimana a settimana, da delibera a delibera: è un **semireticolo politico vivente**.

Tentare di rinchiudere la complessa vita democratica di una metropoli dentro un albero burocratico rigido è un'illusione tecnocratica destinata al fallimento.

---

# 10. L'origine psicologica dell'errore: perché la mente concepisce solo alberi?

Se il semireticolo è palesemente più efficiente, vitale e realistico, **perché gli architetti continuano pervicacemente a progettare alberi?**

Alexander risponde con un'intuizione psicologica profonda:

> **In un singolo atto mentale, la mente umana non è in grado di visualizzare un semireticolo: può visualizzare soltanto un albero.**

Le ragioni cognitive individuate da Alexander sono radicali:

1. **Intolleranza per l'ambiguità**: La mente umana, davanti a un mondo caotico e sovraccarico di stimoli (*information overload*), ha il bisogno primario di semplificare la realtà catalogando le esperienze in categorie chiuse e non sovrapponibili (*pigeon-holes*).
2. **Gli esperimenti di Sir Frederic Bartlett**: Negli esperimenti di memoria percettiva condotti dallo psicologo britannico Bartlett, ai soggetti venivano mostrate per una frazione di secondo (1/4 di secondo) figure geometriche complesse e parzialmente sovrapposte. Quando veniva chiesto loro di ridisegnarle a memoria, quasi tutti **cancellavano le sovrapposizioni**, separando i cerchi dai triangoli e riducendo l'immagine a forme isolate e gerarchizzate.

L'albero è dunque una **scorciatoia cognitiva consolatoria**: offre una sensazione di ordine, igiene mentale e controllo, sacrificando però la complessità della realtà vivente.

---

# 11. La contro-prova estetica: il dipinto di Simon Hantaï

Per dimostrare visivamente come la sovrapposizione generi struttura e non disordine, Alexander analizza un dipinto astratto del pittore Simon Hantaï composto da una serie di triangoli scuri su fondo chiaro.

### Meccanismo
- Nessun triangolo è isolato in una scatola.
- Il triangolo 3 e il triangolo 5 formano un rettangolo; i triangoli 2 e 4 un parallelogramma; i triangoli 5 e 6 condividono orientamento e colore; i triangoli 4 e 7 una simmetria speculare.
- Ogni singolo elemento appartiene contemporaneamente a quattro o cinque sottoinsiemi visivi differenti, nessuno dei quali ingloba l'altro.

### Principio
Il dipinto non è caotico: possiede una struttura ferrea, ma tale struttura è un **puro semireticolo di sovrapposizioni simultanee**.

---

# 12. Il monito contro il falso disordine: il bidone della spazzatura

Alexander inserisce a questo punto un avvertimento metodologico fondamentale per evitare fraintendimenti romantici:

> **Non basta inserire sovrapposizioni casuali per ottenere una città viva. Anche un bidone della spazzatura è pieno zeppo di sovrapposizioni.**

Il punto non è generare caos o confusione pittoresca a tutti i costi (errore commesso da molte proposte dense degli anni Sessanta che celebravano il disordine fine a se stesso).

La sfida del vero progettista consiste nell'individuare **le giuste sovrapposizioni** (*the right overlap*): quelle relazioni sistemiche che rispondono ai reali bisogni associativi, biologici e psicologici degli abitanti della società contemporanea.

---

# 13. La struttura concettuale dell'intero saggio

L'intera argomentazione di Alexander si sviluppa lungo questa impeccabile catena logica:

**IL FALLIMENTO DELLE CITTÀ PIANIFICATE MODERNE**

↓

**CITTÀ NATURALI (VIVE) vs CITTÀ ARTIFICIALI (STERILI)**

↓

**DEFINIZIONE TOPOLOGICA: ALBERO vs SEMIRETICOLO**
(insiemi disgiunti vs sovrapposizioni parziali / *overlap*)

↓

**ANALISI DEI 9 PIANI URBANISTICI MODERNI**
(Columbia, Chandigarh, Brasilia, Tange, Soleri smascherati come alberi)

↓

**L'ARCHETIPO DELL'ACCAMPAMENTO MILITARE (HILBERSEIMER)**
(l'albero come strumento di disciplina e coercizione della vita)

↓

**I CASI DI VITA REALE COME SEMIRETICOLO**
(l'angolo di strada a Berkeley e le reti amicali non-geografiche)

↓

**IL FALLIMENTO DELL'UNITÀ DI VICINATO**
(la segmentazione gerarchica genera solitudine e nevrosi)

↓

**LA MATRICE PSICOLOGICA DELL'ERRORE**
(Bartlett, intolleranza per l'ambiguità e limiti cognitivi della mente umana)

↓

**LA SFIDA DEL DESIGN CONTEMPORANEO**
(superare l'albero per progettare il "right overlap")

↓

# LA CITTÀ È UN MECCANISMO AD ALTA MOLTEPLICITÀ RELAZIONALE

---

## Il concetto più importante da portarsi via

Se dovessi condensare l'intero saggio di Christopher Alexander in una sola idea, direi questa:

> **La vita urbana autentica può fiorire soltanto all'interno di una struttura a semireticolo fatta di sovrapposizioni e intersezioni molteplici; riducendo la città a una gerarchia ad albero per comodità mentale o ansia di controllo, l'urbanistica moderna finisce inevitabilmente per distruggere le relazioni umane e l'anima stessa dell'abitare.**
