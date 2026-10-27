# Parere della tavola rotonda su "Spatial agent prototipo"

**Data:** 2026-10-25. **Oggetto:** https://claude.ai/artifact/MbDwdncXk3bYQNv41N7U1B (1 MB, letto, aperto in browser, screenshot a 1440 e 390 px, codice letto salvo i blocchi di dati).
**Marche:** **[C]** letto nel codice o provato; **[S:NN]** scheda del corpus; **[I]** inferenza; **[H]** ipotesi; **[L]** lacuna o non verificato; **[F]** conoscenza fuori corpus da verificare.
Cinque voci (Azadi, ingegnere, De Carlo-Mari, Pask, MVRDV), un solo round; il revisore indipendente non c'è. Le voci hanno letto lo stesso dossier, quindi la convergenza è in parte circolare. Nessuna ha verificato i dati contro le fonti primarie, io nemmeno.

---

## 0. In breve

1. **Non è una nuova versione di Abitare Cinisello.** È un atlante di contesto territoriale per **Monza e Brianza (55 comuni)**. **Cinisello Balsamo non è tra i 55** [C: elenco nei dati]; il comune è nella Città metropolitana di Milano [F]. Nessun dato dell'artifact vale per i 18 lotti.
2. **Il valore vero è nella parte meno vistosa:** fonti e data accanto a ogni numero, chip di citazione in ogni risposta, ipotesi dichiarate (densità uniforme nella sezione, quartieri approssimati, altezze stimate). È la trasparenza più vicina a Misurato / Modellato / Assunto che esista nel progetto. La parte più debole è la più vistosa: chat «agente» e 3D.
3. **L'«agente» non è un agente.** Il dispatcher è una catena di regex che sceglie una scena preconfezionata; il commento nel codice dice «nessun LLM»; l'indicatore «sta scrivendo» è un `sleep(700)` fisso; il piè di pagina dice «L'IA può sbagliare» [C]. Va rinominato o fatto diventare vero (vedi §3).
4. **Uso consigliato: Fase 0 («contesto»), separata dal laboratorio decisionale, rifatta su Cinisello e comuni confinanti.** Non fusa nella v0.4/v0.5.
5. **Grafica:** tenere struttura e leggibilità, cambiare identità. Per Abitare la palette è carta #f6f6f0 e verde #245346 (richiesta di Dennis). Il giallo ha doppio significato, un KPI si spezza, il mobile è quasi inutilizzabile.

---

## 1. Che cosa è (fatti)

- **Struttura:** mappa (globo → SVG piatto → canvas 3D) con pannello dashboard sovrapposto (selettore vista, chip indicatore, KPI, scala a 6 classi, istogramma, classifica «primi 8», strati), chat a destra, stepper a 8 fasi (Contesto, Profilo, Popolazione, Densità 3D, Economia, Uso del suolo, Mobilità, Monza) [C].
- **Dati dichiarati:** Istat popolazione, età, stranieri al 1.1.2026 (provvisorio); MEF IRPEF 2024 (reddito per contribuente); Istat Censimento 2021 per sezioni, ripartite su esagoni da 0,53 km² «in proporzione all'area, densità uniforme nella sezione»; OSM per confini, strade, ferrovie, stazioni, verde, uso del suolo, ~10.453 edifici di Monza di cui il 38% con altezza taggata, gli altri «stimata dal tipo», altezze «esagerate ×4» nel 3D; quartieri di Monza come aree di influenza dei punti OSM `place=suburb/neighbourhood` [C].
- **Verifica dei dati:** i totali che ho controllato sono plausibili (Monza ~124.000 residenti, provincia 870.400 al censimento 2021), ma non li ho confrontati con Istat/MEF. Gli script che rigenerano i dati (`build_osm_data.py` ecc.) citati nel commento **non sono nella cartella** [L]: non riproducibile da qui.
- **Provato in browser:** funziona senza errori di script; l'unico errore è il caricamento dei font Google, bloccato nella mia rete di prova (quindi uso del font di ripiego) [C].

---

## 2. Verdetto per elemento

| Elemento | Verdetto | Motivo |
|---|---|---|
| **Territorio (55 comuni MB)** | **SCARTARE per Abitare, tenere come metodo** | Cinisello non c'è. Serve la stessa pipeline su Cinisello, Sesto San Giovanni, Cormano, Bresso, Cusano Milanino e Milano nord (tutte voci d'accordo; elenco dei comuni confinanti da verificare [I]). |
| **Dati Istat/MEF per comune** | **MANTENERE come contesto** | Fonte e data sul numero, «provvisorio» dichiarato: più onesto di OMI/IRPEF/LST della specifica v0.3. Ma sono medie comunali, non valori di lotto: confondere le scale sarebbe falsa precisione. Il comune nasconde le differenze interne dove stanno i bisogni (De Carlo). |
| **Chip di fonte nelle risposte** | **MANTENERE, estendere** | Aggiungere la terza classe: ogni dato Misurato / Modellato / Assunto (le etichette sono già nel progetto, v0.4). |
| **Esagoni 3D (sezione → esagono, densità uniforme)** | **MODIFICARE; tenere solo come esplorazione** | Ipotesi dichiarata ma nel piè di pagina; una colonna da 6488 residenti suggerisce precisione che l'ipotesi non regge. Un esagono da 0,53 km² è molto più grande di un lotto. Il censimento (2021) e i dati comunali (2026) hanno anni diversi. Test proposto: rifare la mappa con un altro esagono o con le sezioni originali e confrontare (effetto di zonizzazione, MAUP [F]). |
| **Edifici 3D di Monza** | **MODIFICARE, non usare per la tesi finché le altezze non sono marcate** | 62% delle altezze stimate dal tipo, ×4 dichiarato solo in nota: marcare graficamente taggato vs stimato e scrivere «×4» accanto alla vista. Non usare per volumi, SLP, ombre. Solo Monza ha gli edifici. |
| **Quartieri di Monza (aree da punti OSM)** | **MODIFICARE** | Diagrammi di tipo Voronoi disegnati come confini; i residenti per quartiere sono un'interpolazione su un'interpolazione. Mostrare come punti «indicativo», tratteggiare; lasciare agli abitanti nominarli e correggerli (catalogo aperto). |
| **Mappa coropletica** | **MANTENERE con modifiche** | Rampa leggibile. Le soglie sono **sestili sui 55 comuni** (`breaks`, riga 211 [C]): ogni classe contiene per costruzione circa lo stesso numero di comuni, quindi il colore dice il rango, non la distanza. La legenda mostra solo minimo e massimo. L'istogramma usa invece 10 intervalli uguali: due logiche di classificazione nello stesso pannello. Mostrare le soglie e offrire quantili / intervalli uguali, oppure allinearle. |
| **KPI** | **MODIFICARE** | Un numero grande senza dire come è calcolato; bug: «11.899.610 m²» va a capo spezzandosi a 1440 px [C]. |
| **Classifica «primi 8»** | **SCARTARE nella forma attuale** | Classifica a criterio singolo: l'ordine dipende interamente dal chip attivo e invita a leggere «alto = meglio». È la caricatura del ranking di Abitare. Tenere come tabella di sola lettura, accanto alla classifica dei lotti con pesi visibili. |
| **Strati (strade, ferrovia, verde)** | **MANTENERE** | Poco carichi di giudizio, verificabili a vista; il testo sull'uso del suolo (poligoni sovrapposti, resto non classificato) è onesto. |
| **Chat «Spatial Intelligence / L'IA può sbagliare»** | **MODIFICARE (rinominare) oppure SCARTARE come agente** | Vedi §3. |
| **Stepper a 8 fasi** | **MANTENERE come guida, MODIFICARE i nomi** | Percorso ordinato e onesto. Ma è una narrazione lineare, non un processo decisionale (Azadi). Nomi in linguaggio d'uso («Chi abita», «Quanto si guadagna», «Come ci si muove»). |
| **Grafica scura con accento giallo** | **MODIFICARE** | Vedi §4. |

---

## 3. L'«agente» e la conversazione

- **Che cosa fa** [C]: regex su parole chiave → scena fissa (`SC[i].html()`) o scheda del comune; la risposta non dipende dalla storia; fuori vocabolario risponde «In questa demo rispondo a…»; «sta scrivendo» è un ritardo fisso; il nome «Spatial Intelligence» e il piè «L'IA può sbagliare» attribuiscono un'IA che non c'è. L'errore, se c'è, è dei template.
- **Pask:** non è una conversazione. Per Pask il sistema adattivo (SAKI) cambia il proprio comportamento in base al partner [S:02]; qui la varietà è fissa e l'utente naviga. Mancano osservatore dichiarato [S:03], motivazione contestabile, traccia, metalinguaggio. Voce: «un menu a parole chiave con veste di dialogo».
- **De Carlo:** per un non esperto un campo libero che risponde a poche parole è frustrante e opaco; il tono sicuro nasconde che non c'è ragionamento.
- **Rinomina immediata:** «Domande guidate» (o «Guida al contesto»), elenco delle domande possibili visibile, nessun finto «sta scrivendo», niente «L'IA può sbagliare».
- **Per diventare davvero una conversazione** (Pask, tutte [I]): (1) ogni risposta dice da quali dati e quale regola nasce e l'utente può contestarla («questo dato non vale perché…») con ricalcolo e differenza visibile; (2) dichiarare chi ha scelto indicatori, classi e dati (osservatore dichiarato); (3) un log delle contestazioni con ciò che cambia; (4) un minimo metalinguaggio: l'utente può proporre un indicatore o un'etichetta mancante. Solo allora ha senso un LLM, dichiarato come strumento di lettura dei dati e non come agente che «capisce».
- **Implicazione zero-backend:** un LLM vero richiede un servizio esterno o una capacità dell'artifact; ciò contrasta con il vincolo «100% client-side» della v0.4. Decisione di Dennis (§6) [I].

---

## 4. Grafica

**Tenere:** gerarchia chiara (mappa grande, pannello dati, conversazione, percorso), tipografia leggibile, citazioni di fonte come elementi grafici, toggle LIGHT/DARK della mappa già presente, reduced-motion rispettato [C], contrasti corretti (grigio #8b8b8b su #0f0f10: 5,6:1; testo scuro su giallo: 14,9:1) [C, calcolati].

**Cambiare:**
1. **Identità.** Dennis aveva chiesto di preservare quella di Abitare (carta #f6f6f0, verde #245346, DM Sans/Manrope). L'artifact è nero con giallo, riferito a un «Hub» che non conosco [L]. Proposta: *adattare, non adottare* (Azadi, De Carlo, Pask). Mappa chiara di default; il nero resta come opzione di base della mappa.
2. **Giallo con doppio significato.** È accento dell'interfaccia (chip selezionati, barre, bordi) e massimo della scala coropletica; il 3D usa un'altra rampa (arancio-marrone). Un abitante non sa se «giallo» vuol dire selezionato o massimo. Separare: accento UI in verde Abitare, scala dati in rampa percettiva distinta, una sola per tutte le viste.
3. **Mobile (390 px):** il pannello dati aperto ricopre quasi tutta la mappa, la chat ha poco spazio [C: mobile.png]. Pannello chiuso di default, mappa in primo piano, chat come foglio inferiore. Controllare su un telefono reale [L].
4. **Gergo e testi piccoli:** «res 8», «layer», «Densità 3D» (nel pannello) e testi da 10-11 px. Linguaggio ordinario, una domanda per vista («dove vivono più anziani?»).
5. **Incertezza visibile:** «stima» accanto ai valori ripartiti; edifici con altezza stimata in tratteggio o tono diverso; «×4» sulla vista; scala con soglie.
6. **Bug:** KPI che si spezza.

---

## 5. Come implementarlo

Posizione comune delle voci (Azadi, Pask, ingegnere, De Carlo, MVRDV), con i limiti di §0:
1. **Separare:** *Fase 0, atlante di contesto* (questo tipo di strumento) e *laboratorio decisionale* (v0.4/v0.5). Collegarli con un link e con una mappatura esplicita indicatore → criterio. Oggi i chip (Residenti, Densità, Over 65, Stranieri) non coincidono con i quattro criteri (soc, prox, clim, comm) [L, MVRDV]: il rischio è il passaggio silenzioso da indicatore a criterio con `f` 0-100 senza fonte.
2. **Dati:** rifare la pipeline su Cinisello e comuni confinanti; recuperare gli script di build o riscriverli e metterli in versione con data e licenza (ODbL per OSM; CC BY per Istat/MEF come dichiarato nel piè). File di dati separato dalla logica, versionato e datato (ingegnere).
3. **Dentro Abitare, una schermata «Perché questo valore?»:** scheda dell'indicatore, fonte, classe di incertezza, chi l'ha scelto e chi può cambiarlo; il tavolo dei pesi accanto (MVRDV, De Carlo).
4. **Test prima del rilascio** (ingegnere): somma dei residenti per esagono = totale (870.400); medie pesate con dati mancanti trattate come «n/d»; confronto con un altro esagono; controllo a campione di 5 comuni contro la fonte; test sulle soglie dei sestili.
5. **Peso di file:** 1 MB è adeguato per una demo; aggiungendo Cinisello a livello di sezione e di edificio, il file cresce. Il codice codifica già le coordinate a delta; si può tenere un solo HTML con dati compressi, ma l'aggiornamento resta manuale. [I]
6. **Processo (Azadi):** senza un decisore, un momento decisionale e un'azione concreta, resta una rappresentazione. Valutazione sulle tre dimensioni AUP [S:37]: Interdisciplinary Integration parziale; Consensual Contextualization assente; Procedural Operationalization assente. Nessuno stakeholder rappresentato, tranne un osservatore tecnico.

---

## 6. Obiezioni delle voci e decisioni per Dennis

**Obiezioni principali:**
- *Azadi:* il valore percepito (3D, chat) è nella parte più debole, quello reale (fonti, ipotesi dichiarate) è nella meno vistosa.
- *De Carlo:* se diventa il front-end di Abitare, l'abitante è informato ma non potente; una schermata che dà impressione di oggettività precede la v0.4. Meglio che la Fase 0 mostri *cosa il dato non sa*.
- *Pask:* presentarlo come «agente» fa attribuire una competenza che non c'è, quando la tesi riguarda proprio la qualità della relazione tra utenti e sistema.
- *Ingegnere:* un artifact elegante non sostituisce la prova di validità; l'effetto «dato ufficiale» nasce da grafica e fonti citate, non da un controllo.
- *MVRDV:* la dashboard è un tavolo di lettura, non di negoziazione; la soggettività sta a monte, nella scelta di indicatori e classi.

**Punti ciechi dichiarati:** nessuna voce ha verificato i valori; il corpus non ha schede su Istat/MEF/OSM, MAUP o interpolazione areale [L]; nessuna voce conosce come abitanti non esperti leggerebbero la schermata.

**Domande aperte:** chi è l'osservatore dichiarato dell'atlante? chi sceglie gli indicatori mostrati e chi può aggiungerne uno? come mostrare a un cittadino che un numero è «assunto» senza far perdere fiducia nell'intera mappa (domanda dell'ingegnere ad Azadi, senza risposta)?

**Decisioni per Dennis:**
1. **Che cos'è questo artifact per la tesi:** Fase 0 di contesto (raccomandato), parte del laboratorio, o esperimento a parte?
2. **L'agente:** rinominarlo e tenerlo deterministico (coerente con zero-backend) oppure investire in un agente vero (richiede una dipendenza esterna)?
3. **Identità visiva:** Abitare chiara/verde (raccomandato) o nero/giallo?
4. **Chi ha costruito i dati?** Servono gli script di build per sapere se i numeri sono riproducibili. Se li hai, caricali; altrimenti li ricostruiamo su Cinisello.
5. **Che cos'è l'«Hub» di riferimento del commento «come nell'Hub»?** Non l'ho identificato.
