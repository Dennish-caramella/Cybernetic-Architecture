# Report fondativo: domanda di ricerca e assi della tesi

**Stato:** bozza di impianto scientifico, non la tesi. La scrittura finale è rimandata. Idee e scrittura finale restano dell'autore.
**Data:** 2026-10-20
**Base:** le 27 analisi in `03_Analisi Approfondite/`, l'indice 00, `cosa_parla_la_tesi.md`, `stato_avanzamento.md`, `CLAUDE.md`, l'Atlante dei modelli in `04_Fondamenta Matematiche/`.

## 0. Come leggere questo documento

Ogni affermazione porta una marca di statuto:

- **[V]** verificata sul testo primario (PDF o libro) in questa sessione. Al 2026-10-20 non è ancora stato fatto per nessuna fonte.
- **[S]** riportata dalle analisi del corpus. Le analisi sono riassunti redatti sui PDF, non verifiche indipendenti. Vanno controllate prima di essere citate.
- **[I]** inferenza o ipotesi mia, costruita sul corpus. Non è un fatto dei testi.
- **[L]** lacuna: un punto che il corpus non copre e che serve per la tesi.

Regola: nessuna citazione diretta entra nella tesi a partire da questo documento. Le citazioni vanno prese dal testo originale.

## 1. Problema e stato dell'arte

### 1.1 Il problema

L'edilizia contemporanea distribuisce le decisioni tra attori con interessi divergenti: residenti, sviluppatore, amministrazione, progettista, a volte gestori e finanziatori. Il progetto architettonico tradizionale concentra la decisione nell'autore, mentre la partecipazione arriva in una fase successiva, spesso come consultazione o approvazione [S, analisi 10 e 24].

Il tema è sempre stato presente nella disciplina. De Carlo ne fa la critica più radicale: il funzionalismo ha eliminato la gente dall'architettura, rappresentando un "uomo tipo" invece di chi usa lo spazio [S, analisi 24]. De Graaf descrive l'architetto come figura che dipende economicamente da tutti gli attori e per questo non controlla davvero l'esito [S, analisi 10]. Sanchez denuncia il lavoro gratuito nei concorsi e propone un'architettura dei beni comuni [S, analisi 11].

Nel frattempo gli strumenti computazionali sono cambiati. Il parametrismo, le simulazioni e l'ottimizzazione multicriterio permettono di esplorare molte alternative e di pesare obiettivi diversi [S, analisi 09, 11, 21, 22]. Ma questi strumenti spostano la questione: chi scrive la funzione di fitness, chi sceglie i pesi, chi ha accesso al modello? [I]

### 1.2 Lo stato dell'arte, per filoni

Il corpus copre quattro filoni che si toccano senza coincidere:

1. **Genealogia dei sistemi.** Alexander passa dall'oggetto al sistema generativo [S, analisi 01 e 26] e dalla gerarchia al semireticolo nella città [S, analisi 04]. Pask descrive l'architettura come ambiente reattivo, in cui il controllo è una conversazione [S, analisi 02 e 03]. Negroponte costruisce l'idea del computer come partner nel progetto [S, analisi 05 e 06]. Steenson ricostruisce questa genealogia come storia di un vocabolario, quello dell'intelligenza artificiale in architettura [S, analisi 07].
2. **Dal continuo al discreto.** Carpo sostiene che il passaggio dal parametrismo fluido al discreto segna la fine della modernità del progetto [S, analisi 08]. Sanchez propone il *combinatorial design* come alternativa non parametrica [S, analisi 09]. Erioli e Koehler portano la mereologia al centro: parti, tutto e partecipazione [S, analisi 17 e 18].
3. **Giochi, negoziazione e simulazione.** MVRDV, con The Why Factory, costruisce strumenti in cui i criteri sono espliciti e i pesi sono una scelta [S, analisi 19–23]. Meyboom e Reeves e Veloso et al. portano la stigmergia e il multi-agente nello space planning [S, analisi 12 e 13].
4. **Critica del potere.** Murphy, Mari, De Graaf, Sanchez e De Carlo mettono in discussione chi decide e a quale scopo [S, analisi 10, 11, 15, 16, 24].

### 1.3 La lacuna

Il corpus dà una genealogia delle regole, una tecnica per il discreto, esempi di strumenti di negoziazione e una critica del potere. Ma non unisce questi quattro filoni in un criterio verificabile. Mancano tre cose:

- **L1. Una definizione operativa di partecipazione e democratizzazione.** I testi usano i termini in sensi diversi: De Carlo come autogoverno, MVRDV come scelta del consumatore, Sanchez come commons [S, cosa_parla_la_tesi.md, §6]. Senza una definizione, nessuna prova può dire se il sistema democratizza.
- **L2. Un criterio per distinguere la mediazione dalla decisione nascosta.** Gli analisti 21 e 22 mostrano che pesi e fitness incorporano scelte politiche [S]. Il corpus non dice come renderle discutibili da chi non le ha scritte.
- **L3. Una prova della credibilità ingegneristica.** Le analisi 19, 20 e 22 rinviano a giunti, acustica, antincendio, catasto e costi come questioni aperte [S]. Il corpus non le risolve e nessun file le modella.

La tesi si colloca in questa lacuna. [I]

## 2. Domanda di ricerca

### 2.1 Domanda principale

> In che misura un sistema computazionale multi-attore può rendere visibili e discutibili i compromessi tra gli interessi di residenti, sviluppatore, amministrazione e progettista, senza che il modello o il suo autore diventino il decisore nascosto?

Questa formulazione è una proposta. Dalle fonti non emerge una domanda esplicita [S, cosa_parla_la_tesi.md, §1]. La decisione finale spetta all'autore.

### 2.2 Sottodomande

- **SQ1 (teorica).** Come definiscono i precedenti (Alexander, Pask, Negroponte) il ruolo del progettista come progettista di regole, e che cosa si perde in questa definizione? [I: la risposta va costruita sulle analisi 01, 02, 03, 05]
- **SQ2 (definitoria).** Quale definizione operativa di partecipazione può essere misurata in un processo di progetto? Il criterio deve distinguere almeno tre livelli: informazione, consultazione e potere di modificare le regole. [I, con riferimento a De Carlo, analisi 24]
- **SQ3 (rappresentazione).** Quale rappresentazione del conflitto (pesi, frontiera di Pareto, grafi, campi) rende visibili i trade-off, e quale li nasconde? [I, con riferimento a analisi 21, 22, Atlante §5]
- **SQ4 (empirica).** Il cambiamento dell'esito dipende dall'input degli attori, oppure il sistema restituisce sempre le stesse soluzioni? [I, da verificare con le prove della fase 2]
- **SQ5 (ingegneristica).** Quali vincoli tecnici (costo, normativa, acustica, antincendio, struttura) possono essere codificati in modo credibile, e con quale livello di approssimazione dichiarato? [I, con riferimento a analisi 19, 20, 22 e 23]

## 3. Ipotesi e tesi provvisoria

### 3.1 Tesi provvisoria

> Il ruolo dell'architetto può spostarsi da autore della forma a progettista di regole negoziabili. Un sistema computazionale è credibile come mediatore tra attori solo se espone le funzioni di valutazione (pesi, vincoli, criteri) e lascia agli attori il diritto di modificarle. Altrimenti riproduce la legittimazione criticata da De Carlo e De Graaf: la partecipazione diventa approvazione di decisioni già prese.

Questa tesi è un'ipotesi, non una conclusione. Lo statuto è [I]. Le fonti la rendono plausibile in alcuni punti (per esempio la critica di 21 e 22 alle funzioni di fitness nascoste) ma non la dimostrano.

### 3.2 Ipotesi falsificabili

Ogni ipotesi indica la prova che potrebbe smentirla.

- **H1 (mediazione visibile).** Un sistema che espone i pesi e li rende modificabili dagli attori produce un fronte di soluzioni non dominate che cambia quando cambiano i pesi. **Falsificata se:** il fronte resta invariato o cambia solo per effetti del caso, indipendentemente dai pesi.
- **H2 (potere sui criteri).** Il processo è partecipativo nel senso di SQ2 solo se gli attori possono modificare i criteri, non solo sceglierne una soluzione. **Falsificata se:** nelle prove gli attori scelgono tra soluzioni generate con criteri fissati dall'autore, e nessuno propone una modifica ai criteri.
- **H3 (costo dell'esplorazione).** L'uso del sistema riduce il costo di esplorare i trade-off rispetto a un processo manuale di confronto (tavoli, schemi, fogli di calcolo). **Falsificata se:** il tempo per arrivare a una scelta motivata non è inferiore o la qualità della scelta non migliora. La misura va definita prima della prova (vedi §5).
- **H4 (credibilità).** Un modello che include vincoli ingegneristici dichiarati e verificati produce soluzioni che un tecnico non scarta per errori evidenti. **Falsificata se:** i vincoli mancanti producono scarti sistematici alla revisione tecnica.

## 4. Assi di ricerca

Gli assi sono sei. Per ciascuno: domanda guida, letture di riferimento, concetti dal glossario (il glossario è in `second_brain_v3/01_GLOSSARIO.md` e non è stato letto in questa sessione [L]), e criterio di falsificabilità.

### Asse 1. Sistemi generativi e regole

- **Domanda:** il progettista può progettare regole invece di forme senza ridurre le regole a un unico ottimo?
- **Letture:** Alexander, *Systems Generating Systems* (analisi 01); Alexander, *Notes on the Synthesis of Form* (analisi 26); Alexander, *A City is not a Tree* (analisi 04); Gamma et al., *Design Patterns* (analisi 27) come trasposizione software.
- **Concetti:** misfit, goodness of fit, semireticolo, pattern, kit of parts.
- **Criterio di falsificabilità:** se le regole producono sempre un'unica soluzione ottimale, la tesi "regole invece di forme" si riduce a parametrismo e cade nella critica di Sanchez e Carpo [S, analisi 08, 09, 11].
- **Nota critica:** l'analisi 26 descrive un metodo di decomposizione su IBM 7090 e uno studio su 141 variabili [S]. Il metodo è storicamente datato e i suoi risultati vanno contestualizzati. Il corpus non dice quanto il metodo sia stato poi utilizzato o confutato [L].

### Asse 2. Cibernetica, conversazione e ambiente

- **Domanda:** il sistema può essere un ambiente reattivo in cui il controllo è una conversazione, e non un comando a senso unico?
- **Letture:** Pask, *An Approach to Cybernetics* (analisi 02); Pask, *The Architectural Relevance of Cybernetics* (analisi 03); Negroponte, *The Architecture Machine* (analisi 05); Steenson, *Architectural Intelligence* (analisi 07).
- **Concetti:** varietà necessaria (Ashby), conversazione, mutualismo, cibernetica del secondo ordine, *Fun Palace*.
- **Criterio di falsificabilità:** se il sistema reagisce solo a comandi predefiniti e non modifica né gli attori né le regole, non realizza una conversazione nel senso di Pask. [I]
- **Nota critica:** Pask e Negroponte hanno costruito sistemi interattivi nel contesto degli anni Sessanta e Settanta [S]. Il corpus non verifica i loro risultati e questo va detto in tesi. [L]

### Asse 3. Discreto, combinatoria e mereologia

- **Domanda:** la rappresentazione discreta (parti, mereologia) permette agli utenti di ricombinare il progetto, o è solo un altro modo di chiudere il sistema?
- **Letture:** Carpo, *Beyond Digital* (analisi 08); Sanchez, *Combinatorial Design* (analisi 09); Erioli, *Architectural Assemblages* (analisi 17); Koehler, *From Partitioning to Partaking* (analisi 18); Witt, *Architecture, Automata, and Artificial Memory* (analisi 25).
- **Concetti:** smoothness/chunkiness, unit operations, mereologia, partaking, memoria artificiale.
- **Criterio di falsificabilità:** misurabile con il numero di configurazioni distinte che gli utenti possono produrre con le parti a disposizione. Se la combinatoria produce solo varianti equivalenti, l'asse non sostiene la partecipazione. [I]
- **Nota critica:** l'analisi 18 segnala progetti RC17 e l'affiliazione Bartlett come non verificati [S, stato_avanzamento.md, avviso 2]. Non vanno citati senza verifica.

### Asse 4. Negoziazione, giochi e ottimizzazione multicriterio

- **Domanda:** la frontiera di Pareto e i pesi espliciti rendono i compromessi discutibili, oppure la matematica sostituisce la discussione?
- **Letture:** MVRDV, *The Vertical Village* (analisi 19); *(w)Ego* (analisi 20); *SpaceFighter* (analisi 21); *Functionmixer/OptiMixer* (analisi 22); *Climatizer* (analisi 23); Veloso, Rhee, Krishnamurti, *Multi-agent Space Planning* (analisi 13); Meyboom e Reeves, *Stigmergic Space* (analisi 12). Per i modelli, l'Atlante dei modelli (sezioni su teoria dei giochi e spazio combinatorio con simulated annealing; la frontiera di Pareto va ancora verificata nell'Atlante [L]).
- **Concetti:** fitness, pesi, Pareto, simulated annealing, minimax e Nash, war room.
- **Criterio di falsificabilità:** H1 (vedi §3.2). Inoltre: se il fronte di Pareto è prodotto da una sola funzione di fitness fissata dall'autore, la negoziazione è apparente. [I]
- **Nota critica:** l'analisi 21 dichiara che il software è in gran parte mock-up, e l'analisi 20 che le simulazioni sono state fatte con studenti in ruoli caricaturali [S]. Un risultato di questi giochi non è una prova empirica. Il limite va dichiarato. [I]
- **Nota critica sui dati:** le cifre di soddisfazione in 20 (75/72/65/53%) e del modello in 23 non sono verificate [S, stato_avanzamento.md, avviso 4].

### Asse 5. Partecipazione, potere e legittimazione

- **Domanda:** la partecipazione modificata dal sistema è reale o diventa legittimazione?
- **Letture:** De Carlo, *L'architettura della partecipazione* (analisi 24); De Graaf, *Four Walls and a Roof* (analisi 10); Sanchez, *We have always been parametric* (analisi 11); Murphy, *Last Futures* (analisi 16); Mari, *Autoprogettazione?* (analisi 15); MVRDV, *HUB Bridges* (analisi 14).
- **Concetti:** cooptazione, uomo tipo, rappresentazione di chi usa, autoprogettazione, commons, disalienazione.
- **Criterio di falsificabilità:** l'indice di partecipazione (vedi SQ2) rimane basso se gli attori non possono cambiare obiettivi o regole. [I] Se nelle prove il processo finisce sempre con la soluzione proposta dall'autore, H2 è falsificata.
- **Nota critica:** l'analisi 24 è, come dichiara lo stato di avanzamento, un testo scritto dall'autore durante la lettura del libro, quindi appunti personali e non fonte esterna [S]. Va citata come lettura dell'autore, e le citazioni dirette di De Carlo vanno verificate sul libro [L].

### Asse 6. Credibilità ingegneristica

- **Domanda:** un modello della negoziazione può includere vincoli reali (costo, normativa, struttura, acustica, antincendio) con un livello di approssimazione dichiarato?
- **Letture:** analisi 19, 20, 22 e 23 (questioni aperte su giunti, acustica, antincendio, catasto 3D, costi) [S]. Atlante dei modelli per la parte matematica.
- **Concetti:** vincolo, tolleranza, validità del modello, approssimazione.
- **Criterio di falsificabilità:** H4 (vedi §3.2).
- **Nota critica:** questo è l'asse con meno copertura nel corpus. Le analisi segnalano i problemi ma non li risolvono [S]. Per il corso di Ingegneria Edile è il punto più concreto e più debole: va trattato con prove, non con citazioni. [I]

## 5. Metodologia e piano di prove verificabili

La fase di ricerca (questo documento e il corpus) non produce dati. La fase 2 produce prove. Il piano è una proposta, da discutere.

### 5.1 Fase 1, chiusura della ricerca

1. Verifica delle fonti primarie: almeno le citazioni che entreranno in tesi vanno controllate sui PDF in cartella. Priorità: le 20 fonti PDF già presenti.
2. Chiusura degli avvisi aperti in `stato_avanzamento.md` (dati numerici, incoerenza dell'analisi 13 su 16 o 18 prototipi, datazione di Hillier in 17, residui di estrazione in 10).
3. Costruzione di una definizione operativa di partecipazione (SQ2).
4. Glossario unico dei termini usati in più analisi (misfit, fitness, Pareto, partecipazione, democratizzazione).

### 5.2 Fase 2, prove

Ogni prova deve dichiarare in anticipo che cosa misura, con quale criterio di successo, e quale risultato la smentirebbe.

- **P1. Baseline manuale.** Un caso (un quartiere reale o ipotetico, da scegliere) con quattro ruoli: residenti, sviluppatore, amministrazione, progettista. Il processo è svolto a mano, con schemi e tavoli. Misure: tempo alla scelta, numero di alternative considerate, numero di criteri esplicitati. Serve come termine di confronto per H3.
- **P2. Stesso caso con il sistema.** Gli stessi attori usano lo strumento. Misure: le stesse della P1, più il numero di soluzioni non dominate e la quota di soluzioni che cambiano quando cambiano i pesi (H1).
- **P3. Modifica dei criteri.** Gli attori possono proporre modifiche a pesi e vincoli. Misura: quante modifiche vengono proposte, da chi, e quanto cambia il fronte (H2).
- **P4. Revisione tecnica.** Un tecnico (strutturista, impiantista o esperto di normativa) valuta un campione di soluzioni. Misura: quante soluzioni vengono scartate per errori di vincolo, e perché (H4).
- **P5. Critica.** Un gruppo esterno (docenti o pari) critica il processo e l'esito. Misura: quali punti del processo vengono contestati e se la contestazione porta a cambiare il sistema.

### 5.3 Vincoli di metodo

- Non usare attori fittizi come prova di partecipazione reale. Se si usano simulazioni con ruoli, vanno dichiarate come tali. [S, analisi 20 e 21]
- Separare chiaramente il risultato del modello dalla valutazione degli attori.
- Dichiarare la dimensione del campione. Un caso singolo non generalizza. [I]
- Per le scale di soddisfazione o di partecipazione, scegliere strumenti già validati nella letteratura delle scienze sociali. Il corpus non ne contiene e va cercato. [L]

## 6. Limiti, rischi e critica onesta

### 6.1 Limiti del corpus

- **Il corpus è fatto di riassunti.** Le 27 analisi sono riassunti strutturati (quadripartiti, con diagrammi testuali e una formula conclusiva). Sono utili per orientarsi, ma non sono verifiche. Non vanno citati come fonte primaria. [S]
- **Il corpus è sbilanciato.** Pesa molto sulla genealogia americana e sul MVRDV (6 analisi su 27 riguardano MVRDV e The Why Factory, 19–23 e 14). Manca una voce critica sulla partecipazione digitale che non sia di architetti. [I]
- **Le fonti non sono recenti in ogni asse.** L'asse 2 si basa su testi degli anni Sessanta e Settanta. L'asse 6 non ha letteratura recente nel corpus. [I]
- **Nel corpus non compare nessuna analisi di scienze sociali sulla partecipazione.** Le fonti sono di architettura, filosofia e informatica. È il limite più grave per una tesi che si dichiara scientifica. [L]

### 6.2 Rischi per la tesi

- **Rischio 1, la mediazione che diventa decisione.** Il sistema può spostare il potere dall'architetto allo sviluppatore di software, o a chi definisce i pesi. È la critica che la tesi deve reggere, non aggirare. [S, analisi 21, 22, 23]
- **Rischio 2, la partecipazione simulata.** Se le prove usano attori fittizi, i risultati confermano l'ipotesi per costruzione. [S, analisi 20, 21]
- **Rischio 3, la credibilità ingegneristica.** Un modello che ignora i vincoli reali non è un progetto credibile, anche se è politicamente interessante. [S, analisi 19, 20, 22]
- **Rischio 4, la retorica del discreto.** Il passaggio dal continuo al discreto (Carpo, Sanchez, Erioli) può diventare uno slogan se non produce differenze misurabili. [I]
- **Rischio 5, l'AI come parola d'ordine.** Il tema richiede di chiarire che cosa significa "intelligenza artificiale" in questo contesto: ottimizzazione, apprendimento, linguaggio o simulazione. Le fonti usano il termine in sensi diversi (vedi Steenson e Witt), e la tesi non può usarlo come un'etichetta unica. [I]

### 6.3 Punti in cui il materiale esistente va contraddetto

- Il corpus converge su "l'architetto progetta regole", ma non mostra che le regole siano discusse. Questa convergenza è un'ipotesi dell'autore e va trattata come tale. [I]
- Le note di partenza (`01_Prime considerazioni.md`) dicono "AI ≠ AUTHOR, AI = MEDIATOR" e "from gamification to governance". È una chat, non una fonte [S, cosa_parla_la_tesi.md, §3]. La tesi non può usarla come argomento.
- De Carlo e De Graaf criticano la partecipazione come alibi. Una tesi che propone uno strumento partecipativo deve dire perché il proprio strumento non è un alibi. Questo è il test più duro, e il documento non lo supera ancora. [I]

## 7. Lacune di verifica (elenco di lavoro)

| # | Lacuna | Dove | Statuto |
|---|---|---|---|
| 1 | Nessuna citazione verificata su PDF | tutto il corpus | [L] |
| 2 | Cifre numeriche non verificate | analisi 08, 14, 20, 23 | [S] |
| 3 | Incoerenza 16/18 prototipi | analisi 13 | [S] |
| 4 | Progetti RC17 e affiliazione Bartlett | analisi 18 | [S] |
| 5 | Citazione diretta di De Carlo da verificare sul libro | analisi 24 | [L] |
| 6 | Datazione di Hillier (1989 o 2015) | analisi 17 | [S] |
| 7 | Refusi nel testo di Witt ("Gregory XII", datazione di Erone) | analisi 25 | [S] |
| 8 | Residui di estrazione PDF ("04_De Graaf…") | analisi 10 | [S] |
| 9 | Glossario non letto in questa sessione | `second_brain_v3/01_GLOSSARIO.md` | [L] |
| 10 | README delle correzioni di `04_Fondamenta Matematiche` non presente nel dispositivo (c'è solo l'Atlante) | cartella 04 | [L] |
| 11 | Scale di partecipazione e soddisfazione validate, da cercare | asse 5, fase 2 | [L] |
| 12 | Sito del caso studio non scelto | fase 2 | [L] |

## 8. Prossimi passi

1. Dall'autore: reazione alla domanda di ricerca, alle sottodomande e agli assi (vedi messaggio in chat).
2. Verifica delle citazioni che entreranno in tesi sui PDF, a partire da analisi 01, 02, 03, 24.
3. Scelta del caso studio per la fase 2.
4. Ricerca di letteratura di scienze sociali sulla partecipazione (asse 5), da fare prima della fase 2.
5. Aggiornamento di `02_MAPPA_CONCETTI.md` e del registro in `stato_avanzamento.md`.

---

> **Se dovessi condensare questo documento in una sola idea, direi questa:** la tesi è credibile solo se il sistema rende discutibili le sue regole, non solo i suoi risultati. Tutto il resto, cioè la domanda, gli assi e le prove, serve a verificare questa idea e non a confermarla.
