# Studio dei modelli: spiegazioni, matematica con esempi, schemi

Data: 2026-10-20. Versione di studio dei modelli elencati in `Analisi_approfondite_per_teoria.md` (schede brevi) e `Cronistoria_e_correlazioni_modelli.md` (storia e fonti). Qui ogni modello ha: l'idea in parole semplici, la matematica passo per passo, un esempio numerico o figurato, uno schema, i limiti.

**Legenda di affidabilità.** [V] verificato nelle passate di ricerca o sul testo primario · [S] formalismo standard, da controllare sul testo primario prima di citare · [I] interpretazione mia · [L] lacuna. Gli esempi numerici sono miei e servono solo a capire il meccanismo: non sono citazioni.

**Stato delle verifiche.** Il dettaglio di che cosa è stato letto sul testo primario e che cosa no è in `Verifiche_testi_primari.md`, nella stessa cartella. Le voci Nash e von Neumann-Burks sono verificate; Ashby (pagine su varietà e legge), Bertalanffy 1950 e 1957, Codd e Husserl restano [S] o [L].

---

## Indice

1. Bertalanffy: sistemi aperti e stato stazionario
2. Bertalanffy: crescita asintotica
3. Ashby: varietà e legge della varietà richiesta
4. Good regulator (Conant e Ashby)
5. Vicinato di von Neumann e vicinato di Moore
6. Automi cellulari: una dimensione, regola 90 (esempio guida)
7. Automa autoriproducente di von Neumann
8. Moore-Myhill e il Giardino dell'Eden
9. Nash: equilibrio e strategie miste
10. Minimax di von Neumann
11. Bogost: unit operations
12. Husserl: parte, dipendenza, confine
13. Come si collegano: schema d'insieme

---

## 1. Bertalanffy: sistemi aperti e stato stazionario

**Idea.** Un sistema aperto scambia materia, energia o informazione con l'ambiente. Può restare stabile anche se nulla è fermo: è un equilibrio dinamico, non l'equilibrio di un sistema chiuso che ha esaurito le differenze.

**Matematica.** Lo stato X(t) cambia secondo una legge che dipende da sé stesso e dagli ingressi U(t):

    dX/dt = f(X, U, t)

Lo stato stazionario X* è dove la variazione si annulla:

    f(X*, U*) = 0

**Esempio.** Un serbatoio riceve acqua a portata costante a = 10 e ne perde una quota proporzionale al livello, b·X con b = 2:

    dX/dt = 10 − 2X

Il livello stazionario è X* = 10/2 = 5. Se si parte da X(0) = 0, la soluzione è X(t) = 5(1 − e^(−2t)): il livello sale e si stabilizza su 5. Qualunque sia il punto di partenza, il livello converge a 5. Questo è il punto debole e forte insieme: la stabilità dipende dal sistema (a, b), non dallo stato iniziale.

**Schema.**

    ingresso U ──►  [ sistema X ]  ──► uscita
                      ▲      │
                      └──────┘  retroazione (dipende da X)

    X(t)
     5 ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   stato stazionario X* = 5
       │                    ╭──────────────
       │              ╭─────╯
       │          ╭───╯
     0 ┤──────────╯
       └───────────────────────────────────── t

**Equifinalità.** Due serbatoi con capacità diverse, ma stessi a e b, convergono allo stesso X*. Stesso esito, storie diverse. Questo è il senso dell'equifinalità [S, Bertalanffy 1950, *Science* 111; non raggiunto].

**Il punto di partenza nel testo primario.** Nella recensione di Bertalanffy su *Nature* (1949, "'Open Systems' in Physics and Biology") l'argomento è questo: gli organismi sono sistemi aperti che si mantengono scambiando materia con l'ambiente, e il secondo principio della termodinamica "applies only to closed systems". Quindi non definisce da solo lo stato stazionario di un organismo. [V, testo verificato] La recensione non parla di equifinalità: quella nozione viene dal lavoro successivo.

**Limiti.** La forma dX/dt = f non dice quale f scegliere per un sistema reale. La teoria dà un linguaggio comune, non una legge specifica. [V, cronistoria]

---

## 2. Bertalanffy: crescita asintotica

**Idea.** La crescita di un organismo rallenta man mano che si avvicina a una dimensione massima.

**Matematica.** Con L∞ lunghezza asintotica e k tasso di approccio:

    dL/dt = k (L∞ − L)

Soluzione:

    L(t) = L∞ (1 − e^(−k (t − t₀)))

**Esempio.** L∞ = 100 cm, k = 0.5 per anno, t₀ = 0:

| t (anni) | L(t) (cm) | Crescita in quell'anno |
|---|---|---|
| 0 | 0 | — |
| 1 | 39.3 | 39.3 |
| 2 | 63.2 | 23.9 |
| 4 | 86.5 | — |
| 8 | 98.2 | — |

La crescita annua si dimezza circa ogni anno: è il segno dell'approccio asintotico. [I, calcolo sul modello]

**Schema.**

    L
    100 ┤ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  L∞
        │                     ╭─────────────────────
     50 ┤             ╭───────╯
        │       ╭─────╯
      0 ┤───────╯
        └───────────────────────────────────────────── t

**Nota.** La forma generalizzata in peso, dW/dt = a W^(2/3) − b W, è citata come generalizzazione [S]; non l'ho riletta sul testo.

---

## 3. Ashby: varietà e legge della varietà richiesta

**Idea.** Per controllare un ambiente che produce molte perturbazioni diverse, il regolatore deve avere almeno altrettante risposte distinte. Non si controlla un sistema vario con un regolatore povero.

**Varietà.** Il numero di stati distinguibili, o il suo logaritmo in bit:

    V(S) = |S|        oppure        V(S) = log₂ |S|

Esempio: 8 stati distinti hanno varietà 8, cioè log₂ 8 = 3 bit. [V, Ashby 1956, pp. 125–126]

**La legge (versione logica).** Un regolatore deterministico assegna a ogni perturbazione una risposta. Se le perturbazioni sono D e le risposte R, gli esiti O sono al minimo:

    |O| ≥ |D| / |R|

In bit:

    V(O) ≥ V(D) − V(R)

**Esempio (principio dei cassetti).** Otto perturbazioni d1…d8, due risposte a e b. Ogni perturbazione deve ricevere una risposta. Almeno una risposta è usata per quattro perturbazioni (8 ÷ 2 = 4). Quindi esiste almeno un gruppo di quattro perturbazioni con quattro esiti possibili. Il minimo di esiti è 4, non 1. In bit: V(D) = 3, V(R) = 1, V(O) ≥ 2. [I, illustrazione del calcolo]

**Tabella del gioco a due giocatori.** Il disturbo sceglie la riga, il regolatore la colonna, la cella è l'esito. [V, Ashby 1956, p. 202]

|  | Regolatore: risposta a | Regolatore: risposta b |
|---|---|---|
| Disturbo d1 | esito 1 | esito 2 |
| Disturbo d2 | esito 2 | esito 1 |

Se il regolatore riesce a far finire ogni riga in un solo esito, la varietà degli esiti è 1: è il caso di regolazione perfetta.

**Limiti.** È una condizione necessaria, non sufficiente. Dice quanta varietà serve, non come costruirla. [V]

---

## 4. Good regulator (Conant e Ashby, 1970)

**Idea.** Un buon regolatore deve contenere, in qualche forma, un modello del sistema che regola. Non basta reagire: bisogna sapere come il sistema si comporta.

**Enunciato.** Un regolatore che minimizza l'errore in modo ottimale è isomorfo a un modello del sistema regolato. [S, Conant e Ashby 1970, *Int. J. Systems Science*]

**Esempio figurato.** Un termostato che sa solo "troppo caldo → accendi il raffreddamento" non ha bisogno di un modello complesso. Un sistema che deve prevedere il comportamento di un ambiente con ritardi (es. l'inerzia di una stanza) deve modellare quel ritardo, altrimenti oscilla.

**Nota.** L'attribuzione di questo risultato alla fonte arXiv 2008.04071 è scartata dalla verifica. [V]

**Schema.**

    perturbazioni ──► [ sistema ] ──► esito
                          ▲
                          │ modello interno
                      [ regolatore ]

---

## 5. Vicinato di von Neumann e vicinato di Moore

**Idea.** Un automa cellulare è una griglia di celle. Ogni cella decide il proprio stato guardando solo le celle vicine. Il vicinato è l'insieme delle celle "vicine" cui una cella guarda.

**Definizione formale.** Un vicinato è un insieme N di spostamenti (i, j) rispetto alla cella:

- **von Neumann:** N = {(0,0), (±1,0), (0,±1)}: cinque celle con il centro, quattro senza.
- **Moore:** N = {(i,j) : |i| ≤ 1, |j| ≤ 1}: nove celle con il centro, otto senza.

**Schema 2D.** Il centro è la cella C; le celle marcate con `x` appartengono al vicinato.

    von Neumann (5 con centro)        Moore (9 con centro)

        .   x   .                      x   x   x
        x   C   x                      x   C   x
        .   x   .                      x   x   x

Il vicinato di Moore contiene quello di von Neumann più le quattro diagonali. [V, convenzione]

**Numero di regole.** Con due stati e un vicinato di k celle, le regole possibili sono 2^(2^k). Con k = 5 (von Neumann con centro) si hanno 2^32 regole; con k = 9 (Moore con centro) si hanno 2^512 regole. [S] Il salto mostra perché serve restringere lo spazio delle regole.

**Regole totalistiche.** Una regola totalistica dipende solo dalla somma degli stati nel vicinato, non dalla loro disposizione. Il Game of Life di Conway è la regola B3/S23 sul vicinato di Moore:

- nasce (B, *birth*) una cella morta con esattamente 3 vicini vivi;
- sopravvive (S, *survival*) una cella viva con 2 o 3 vicini vivi;
- altrimenti muore per solitudine o sovraffollamento.

[S]

**Limiti.** La scelta del centro (incluso o escluso) cambia il conteggio. Il rapporto diretto tra Moore e von Neumann non è documentato da fonti verificate. [V, lacuna]

---

## 6. Automi cellulari: una dimensione, regola 90 (esempio guida)

Per capire la località senza perdersi nei dettagli 2D, si usa un automa unidimensionale con vicinato di raggio 1 (celle a sinistra e a destra). La regola 90 calcola il nuovo stato come XOR dei due vicini:

    nuovo stato = sinistra XOR destra

**Simulazione** partendo da una sola cella accesa al centro (0 = spenta, 1 = accesa):

    t=0 :  . . . . 1 . . . .
    t=1 :  . . . 1 . 1 . . .
    t=2 :  . . 1 . . . 1 . .
    t=3 :  . 1 . 1 . 1 . 1 .
    t=4 :  1 . . . . . . . 1

Il disegno d'insieme delle generazioni forma un triangolo di Sierpiński. Nessuna cella conosce la figura globale: ognuna guarda solo i due vicini. Questo è il meccanismo dell'emergenza locale-globale. [I, calcolo a mano sull'esempio, con i bordi trattati come spenti]

**Un calcolo a mano.** La cella in posizione 4 al tempo t = 2:

    t=1:   . . . 1 . 1 . . .      (posizione 3 = 1, posizione 5 = 1)
    t=2, pos 4:  sinistra = 1,  destra = 1  →  1 XOR 1 = 0

---

## 7. Automa autoriproducente di von Neumann

**Idea.** Von Neumann voleva mostrare che una macchina può costruire una copia di sé. Il problema è logico: come si può copiare qualcosa che contiene la descrizione di sé stesso?

**Struttura.** Tre componenti:

    [ costruttore universale ]  +  [ nastro di descrizione ]  →  copia della macchina
              ▲                                                    │
              └──────────── copia anche il nastro ◄────────────────┘

La macchina legge la descrizione, costruisce ciò che la descrizione dice, poi copia la descrizione stessa. Il nastro serve sia da istruzione sia da dato. [S, von Neumann e Burks 1966]

**Numeri.** 29 stati per cella. Il testo di von Neumann e Burks (1966) dice: "Each cell is capable of 29 different states", e il vicinato è "a neighborhood composed of a cell and the four cells with which it shares boundaries": cinque celle con il centro, cioè il vicinato di von Neumann. [V, testo verificato]

**Semplificazioni.** Codd (1968) ha ridotto il numero di stati a 8 [S]. Langton (1984) ha costruito un loop autoriproducente molto più piccolo, che si copia ma non costruisce altro. [V, abstract di Langton 1984]

**Architettura nel testo.** Il costruttore universale ha due unità, un'unità nastro e un'unità di costruzione. La descrizione della macchina è memorizzata in forma esplicita sul nastro; la macchina la legge e costruisce un nuovo automa, poi copia la descrizione sul nuovo nastro. [V, testo verificato]

**Lezione filosofica.** Il testo di von Neumann non dice che la costruzione sia sufficiente ma non necessaria per l'autoriproduzione: presenta l'autoriproduzione come "un caso speciale della costruzione". La tesi "sufficiente, non necessaria" è di Langton (1984), e va citata come sua. [V, correzione dopo verifica]

---

## 8. Moore-Myhill e il Giardino dell'Eden

**Due definizioni da distinguere.**

- **Suriettiva:** ogni configurazione possibile ha almeno un predecessore.
- **Iniettiva:** due configurazioni diverse non danno mai la stessa immagine.

**Giardino dell'Eden.** Una configurazione che non ha alcun predecessore: nessuna configurazione la produce. Può esistere solo se l'automa non è suriettivo.

**Teorema (Moore 1962, Myhill 1963).** Per un automa cellulare su griglia con alfabeto finito:

    suriettivo  ⟺  pre-iniettivo

dove pre-iniettivo significa iniettivo sulle configurazioni con supporto finito. [S]

**Esempio.** Un automa 1D con regola che "sposta a destra" ogni stato è iniettivo e suriettivo: nessun Eden. Una regola che "cancella" uno stato è non iniettiva (due configurazioni diverse diventano uguali) e quindi non suriettiva: ammette un Eden. [I, esempio illustrativo]

**Nota.** La formulazione "localmente iniettivo se e solo se suriettivo" è scartata dalla verifica. [V]

**Lezione.** Un automa che perde informazione (non iniettivo) non può essere reversibile. Il teorema lega la reversibilità dinamica alla struttura delle configurazioni. [I]

---

## 9. Nash: equilibrio e strategie miste

**Gioco in forma strategica.** Tre elementi: giocatori N, strategie S_i per ciascuno, payoff u_i che dà il risultato per ogni combinazione di strategie. [V, Nash 1951]

**Definizione nel testo di Nash.** Nel 1951 un punto di equilibrio σ è definito come quel profilo in cui il payoff di ogni giocatore è il massimo possibile rispetto alle strategie miste di quel giocatore, date le strategie degli altri: p_i(σ) = max p_i(σ; ρ_i). È la stessa condizione della disuguaglianza usata sopra, scritta come massimo. [V, p. 287]

**Perché "non cooperativo".** Nash contrappone la propria teoria a quella cooperativa di von Neumann e Morgenstern. Nella cooperativa i giocatori possono formare coalizioni; nella non cooperativa ogni partecipante agisce da solo, senza collaborazione né comunicazione con gli altri. Il termine è nel titolo, non nel corpo dell'introduzione. [V, p. 286]

**Dilemma del prigioniero.** Due giocatori, due strategie (C = collaborare, D = tradire). Payoff (riga, colonna):

|  | Colonna C | Colonna D |
|---|---|---|
| **Riga C** | (3, 3) | (0, 5) |
| **Riga D** | (5, 0) | (1, 1) |

**Equilibrio di Nash.** Un profilo in cui nessuno migliora cambiando da solo. Qui (D, D) è l'equilibrio: se l'altro sta su D, sta meglio anche io su D (1 > 0). Ma (C, C) darebbe (3, 3), meglio per entrambi. Il payoff dell'equilibrio è peggiore di un esito possibile. [S, dilemma del prigioniero]

**Strategie miste (esempio: monete).** Gioco "pari o dispari": il giocatore riga vince +1 se le due monete coincidono, −1 altrimenti. Il colonna vince se non coincidono. Non c'è un equilibrio in strategie pure. Con probabilità q che il colonna scelga Testa:

- se la riga sceglie Testa: payoff atteso = q − (1 − q) = 2q − 1;
- se la riga sceglie Croce: payoff atteso = −q + (1 − q) = 1 − 2q.

La riga è indifferente quando 2q − 1 = 1 − 2q, cioè q = 1/2. Simmetricamente la riga sceglie 1/2 e 1/2. L'equilibrio misto è (½, ½) per entrambi. [I, calcolo su esempio standard]

**Teorema di esistenza.** "Every finite game has an equilibrium point" (Teorema 1). La dimostrazione del 1951 usa il teorema del punto fisso di Brouwer: lo spazio delle strategie miste è un insieme convesso compatto, e la mappa che migliora le strategie ha almeno un punto fisso, che è un equilibrio. Il lavoro del 1950 usava Kakutani, che il 1951 migliora. [V, Nash 1951, Theorem 1, pp. 287–288]

**Limiti.** Non dice quale equilibrio scegliere se ce ne sono più di uno. Assume payoff noti e giocatori razionali. Non garantisce efficienza. [S]

---

## 10. Minimax di von Neumann

**Idea.** In un gioco a somma zero a due giocatori, quello che uno guadagna l'altro perde. Ciascuno sceglie la strategia che minimizza il danno nel caso peggiore.

**Enunciato.**

    max_σ min_τ u(σ, τ)  =  min_τ max_σ u(σ, τ)

Il valore del gioco è il payoff comune a entrambi i lati.

**Esempio (pari o dispari, di nuovo).** La matrice dal punto di vista del giocatore riga, con + vittoria e − sconfitta:

|  | Colonna Testa | Colonna Croce |
|---|---|---|
| **Riga Testa** | +1 | −1 |
| **Riga Croce** | −1 | +1 |

Con strategia mista (½, ½) il giocatore riga garantisce 0 in ogni caso; il valore del gioco è 0. Nessuna strategia pura garantisce un risultato migliore nel caso peggiore. [I, calcolo]

**Relazione con Nash.** In un gioco a somma zero a due giocatori, l'equilibrio di Nash coincide con il valore minimax. [S]

**Limiti.** Vale solo per giochi a somma zero a due giocatori. Il win-win non appartiene a questa classe. Questo è il punto da tenere presente quando si legge la scena urbana come gioco a somma zero (vedi `Analisi_approfondite_per_teoria.md`, sezione Nash). [I]

---

## 11. Bogost: unit operations

**Natura.** Non è un modello matematico. È un metodo per analizzare sistemi culturali e tecnici come insiemi di unità che interagiscono attraverso operazioni. [V, tesi generale]

**Come si usa.** Si scelgono le unità (un testo, un programma, un gioco), si descrive come si collegano e si trasformano. Esempio: in un gioco, l'unità "regola" e l'unità "turno" si collegano attraverso l'operazione "il turno attiva la regola". [I]

**Schema.**

    unità A ──[operazione]──► unità B ──[operazione]──► unità C
       ▲                                                  │
       └──────────── retroazione (se presente) ◄──────────┘

**Nota.** La definizione "sistema configurativo di unità di significato discrete e interconnesse" è scartata dalla verifica. Non usarla come definizione. [V, 0-3]

**Limiti.** Senza una definizione formale di unità e operazione il metodo non è verificabile. È la parte più debole della fonte. [V]

---

## 12. Husserl: parte, dipendenza, confine

**Idea.** Il tutto non è semplicemente la somma delle parti. Alcune parti possono stare da sole, altre no, e alcune relazioni sono di confine e contatto più che di inclusione.

**Mereologia formale (base).** Relazione di parte P(x, y) "x è parte di y":

- riflessività: P(x, x);
- antisimmetria: P(x, y) ∧ P(y, x) → x = y;
- transitività: P(x, y) ∧ P(y, z) → P(x, z). [S, Leśniewski, Tarski]

**Esempio.** Domino: un dominio di tre oggetti: a = tessera sinistra, b = tessera destra, c = la coppia a+b. Parti: P(a, c), P(b, c), P(c, c), P(a, a), P(b, b). Non c'è P(a, b) né P(b, a), e antisimmetria è rispettata. [I, esempio]

**Dipendenza (fondazione).** x dipende da y se x non può esistere senza un y di un certo tipo. Esempio: il colore di una mela non esiste senza una superficie; la superficie può esistere senza un colore specifico. Il colore dipende dalla superficie, non viceversa. [S, Husserl, *Ricerche logiche* III]

**Schema.**

    superficie ◄──── colore        (il colore dipende dalla superficie)
       ▲
       └── superficie può esistere senza un colore specifico (ma non senza un colore)

**Tripartizione (Smith e Mulligan 1983).** Tre relazioni: parte-tutto, dipendenza, confine-contatto. [V, voto 3-0]

**Limiti.** Le *Ricerche logiche* non sono state lette in questa sessione. La discrepanza bibliografica (*Topoi* 3 o 2(1)) è da risolvere. [V]

---

## 13. Come si collegano: schema d'insieme

| Teoria | Oggetto | Strumento matematico | Domanda che pone |
|---|---|---|---|
| Bertalanffy | sistema aperto | equazione differenziale, equilibrio | come si stabilizza un sistema con scambi? |
| Ashby | regolazione | cardinalità, logaritmo, tabella | quanta varietà serve per controllare? |
| Good regulator | regolatore | modello interno | il regolatore deve sapere come il sistema si comporta? |
| von Neumann / Moore | automa su griglia | vicinato, regole | quanta struttura globale nasce da regole locali? |
| Automa di von Neumann | autoriproduzione | costruttore, descrizione | come si copia qualcosa che contiene sé stesso? |
| Moore-Myhill | dinamica su griglia | suriettività, iniettività | l'informazione si conserva? |
| Nash | gioco | strategie miste, payoff | quale stabilità emerge dalle decisioni individuali? |
| Minimax | gioco a somma zero | max-min | come si limita il danno nel caso peggiore? |
| Bogost | sistemi culturali | unità e operazioni | come si analizza un sistema come rete di parti? |
| Husserl | ontologia formale | parte, dipendenza, confine | quali parti possono esistere da sole? |

**Ponti tra le teorie** (interpretazioni [I], non verificate su fonte primaria):

- **Ashby ↔ vicinato.** La varietà locale di una cella è limitata dal vicinato: il regolatore locale ha una varietà limitata.
- **Nash ↔ Ashby.** La tabella di Ashby è un gioco di risposta; un equilibrio di Nash tra regolatore e disturbo sarebbe un punto di stabilità reciproca. Non è documentato in letteratura che io abbia verificato.
- **Bertalanffy ↔ automi.** Lo stato stazionario di un sistema corrisponde a un attrattore nella dinamica locale. Il collegamento formale va costruito.
- **Husserl ↔ automi.** La dipendenza è più forte della prossimità: un automa tratta come vicini celle che husserlianamente non dipendono l'una dall'altra.

**Lacune.** I ponti sono interpretazioni. Vanno cercati in letteratura prima di essere citati come collegamenti verificati. [L]

---

## Prossimi passi per lo studio

1. Leggere i testi primari, in quest'ordine: Bertalanffy (1950); Ashby (1956, cap. 11); von Neumann e Burks (1966); Nash (1951); Husserl, *Ricerche logiche* III.
2. Verificare i formalismi [S] con un esempio numerico proprio, come quelli sopra.
3. Costruire la simulazione della regola 90 e del Game of Life per vedere il vicinato all'opera.
4. Risolvere la discrepanza bibliografica su Smith e Mulligan.
