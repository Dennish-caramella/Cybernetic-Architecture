# Scelta sociale computazionale per criteri riscrivibili e scelta equa tra lotti (stato a novembre 2026)

Note di ricerca, 2026-11-09. Estende `secondo_cervello/ricerche/reports/Lotti ideali partecipazione e digital twin.md` (§ Equal Shares, generative social choice, Habermas Machine).

**Marche.** [V] verificato in questa sessione sul testo primario (abstract o pagine lette); [S] da fonte secondaria o riassunto di motore di ricerca; [I] inferenza mia; [H] ipotesi da testare; [L] lacuna: forma standard o dato ricordato dalla letteratura ma **non** verificato qui, da controllare sull'originale prima di citarlo.

**Limiti della sessione.** La rete dell'ambiente blocca `equalshares.net`, `nature.com`, `ncbi.nlm.nih.gov`, `en.wikipedia.org`, `comsoc-community.org`. Funzionano `arxiv.org` e la ricerca web. Di conseguenza: il paper Nature 2021 sul sorteggio e le pagine ufficiali di Wieliczka e Aarau non sono stati letti direttamente. Solo la definizione di Equal Shares è stata letta sul PDF (Peters, Pierczyński, Skowron, arXiv 2008.13276, p. 7). Nessun numero di pagina va usato per le altre fonti.

## 1. Aggregare pesi e criteri (non solo candidati)

### Takeaway
Se i residenti propongono **vettori di pesi** che sommano a 1 (un "bilancio" di importanza tra criteri), il problema è formalmente identico all'aggregazione di proposte di bilancio di Freeman–Pennock–Peters–Wortman Vaughan: la media è manipolabile, la regola utilitaria (minima distanza ℓ1) è strategyproof ma maggioritaria, i *moving phantom mechanisms* sono strategyproof e uno di essi (Independent Markets) è anche proporzionale. Se invece i residenti votano **giudizi logicamente collegati** (criterio rilevante sì/no, soglia rispettata sì/no, quindi lotto ammissibile sì/no), si cade nel paradosso dottrinale e nell'impossibilità di List–Pettit: non esiste un'aggregazione che sia insieme coerente, anonima, sistematica e a dominio universale.

### Cited Findings
- **Freeman, Pennock, Peters, Wortman Vaughan, "Truthful Aggregation of Budget Proposals"**, *Journal of Economic Theory* 193 (2021) 105234; arXiv 1905.00457 (EC 2019). Preferenze ℓ1 (disutilità = distanza ℓ1 tra il vettore proposto e quello scelto). Risultati dell'abstract: (a) il meccanismo che massimizza il benessere, cioè minimizza la distanza ℓ1 media dalle proposte, è incentive compatible ma **non proporzionale**, perché dà troppo peso alla maggioranza; (b) si definisce la classe dei **moving phantom mechanisms**, che contiene sia il meccanismo utilitario sia l'**Independent Markets mechanism**, costruito sulla connessione tra prezzi di mercato e mediane generalizzate di Moulin (1980); (c) **ogni moving phantom mechanism è incentive compatible**; Independent Markets è strategyproof **e** proporzionale; (d) il meccanismo utilitario è l'unico Pareto-ottimo della classe → compromesso Pareto/proporzionalità — [V, abstract] [arXiv 1905.00457](https://arxiv.org/abs/1905.00457)
- Forma standard del moving phantom (da verificare sul testo, §3 del paper) [L]: $n$ votanti, $m$ voci, proposte $\mathbf{p}_i \in \Delta^m$; una famiglia di $n+1$ "fantasmi" $f_0(t) \ge f_1(t) \ge \dots \ge f_n(t)$ continui e crescenti in $t\in[0,1]$; per ogni voce $j$
  $$a_j(t) = \operatorname{med}\big(f_0(t),\dots,f_n(t),\,p_{1,j},\dots,p_{n,j}\big)$$
  e si sceglie $t^*$ tale che $\sum_j a_j(t^*) = 1$. Per Independent Markets i fantasmi sono (forma ricordata, [L]) $f_k(t)=\min\{t(n-k),1\}$. In caso di proporzionalità: se ogni votante propone un solo vertice del simplesso, l'esito assegna a ciascuna voce la quota dei votanti che l'hanno proposta [L, definizione da verificare].
- La media aritmetica dei vettori non è strategyproof (chi vuole alzare il peso di un criterio ha incentivo a dichiarare 1 su quel criterio) [L: argomento standard, verificare formulazione in Freeman et al. §1].
- Conitzer et al. (2024) richiamano che in un contesto di valutazioni numeriche **la mediana è strategy-proof**, mentre "every reasonable voting rule will sometimes introduce incentives to manipulate" — [V, §7.2 testo HTML] [arXiv 2404.10271](https://arxiv.org/html/2404.10271v2)
- Conitzer et al. propongono anche di trattare **principi etici diversi come "votanti"** (§7.4) — [V] [arXiv 2404.10271](https://arxiv.org/html/2404.10271v2). È l'analogo formale di "criteri come votanti" [I].
- **Paradosso dottrinale e List–Pettit (2002)**: forma standard [L]. Agenda con proposizioni $p$, $q$, $p\wedge q$; tre giudici: (V,V,V), (V,F,F), (F,V,F). Maggioranza proposizione per proposizione: $p$ V, $q$ V, $p\wedge q$ F → insieme incoerente. Teorema (List & Pettit, *Economics and Philosophy* 18, 2002) [L]: per agende sufficientemente connesse non esiste una funzione di aggregazione con dominio universale, insiemi collettivi coerenti e completi, anonimia e sistematicità. Uscite note: regole *premise-based* o *conclusion-based*, regole a distanza (Kemeny-like), dittature di sottoagenda [L]. Non verificato in sessione: nessuna fonte primaria letta.

### Inferences
- [I] Per la tesi la scelta di **formato del voto** sui criteri è decisiva: "distribuisci 100 punti di importanza tra i criteri" rende applicabile Freeman et al. e garantisce strategyproofness + proporzionalità (Independent Markets); "approva/disapprova ogni criterio" o "assegna un punteggio libero" non hanno le stesse garanzie.
- [I] La proporzionalità di Independent Markets ha un significato politico preciso: un gruppo che è il 20% dei residenti e mette tutto il peso sul "verde" ottiene almeno il 20% del peso aggregato sul verde. La mediana coordinata per coordinata o il meccanismo utilitario non danno questa garanzia alla minoranza.
- [I] Il paradosso dottrinale colpisce i **vincoli di ammissibilità** (es. "lotto ammissibile se costo ≤ soglia E distanza dal trasporto ≤ soglia"). Il gruppo deve dichiarare prima se si vota sulle premesse (le soglie) o sulla conclusione (il lotto); il mediatore IA non deve scegliere in silenzio.
- [H] Test con agenti simulati: confrontare media, mediana coordinata, utilitaria ℓ1 e Independent Markets su (i) quota di peso ottenuta da minoranze coese, (ii) guadagno da manipolazione di un agente strategico.

### Gaps
- Testo completo di Freeman et al. non letto: formule dei fantasmi, definizione di proporzionalità e risultati su altri fantasmi (es. "piecewise uniform") da verificare.
- Lavori successivi (2022–2026) su aggregazione di bilanci/pesi con ℓ1 (es. Caragiannis et al., Brandt et al., "truthful budget aggregation" con altre metriche) non cercati per limite di chiamate.
- Teorema di List–Pettit e letteratura di judgment aggregation (Dietrich, List, Grossi–Pigozzi) non verificati in sessione.

## 2. Proporzionalità: JR, PJR, EJR, core; Method of Equal Shares; Phragmén; dispiegamenti reali

### Takeaway
La gerarchia degli assiomi è JR ⊂ PJR ⊂ EJR ⊂ (FJR) ⊂ core (dal più debole al più forte; l'esistenza del core nel caso approvazione è ancora un problema aperto). Il Method of Equal Shares (MES) soddisfa EJR nel bilancio partecipativo con costi arbitrari e voti di approvazione, ed EJR "up to one project" con utilità additive. È stato usato in casi reali (Wieliczka 2023, Aarau 2023) con più progetti finanziati e più votanti rappresentati rispetto al greedy, ma anche con un costo noto: un progetto molto popolare può essere sacrificato e il bilancio può restare in parte non speso.

### Cited Findings
- **Definizione di MES** (Peters, Pierczyński, Skowron, "Proportional Participatory Budgeting with Additive Utilities", NeurIPS 2021, arXiv 2008.13276, Definizione 1) [V, letta su PDF]:
  elezione $(N, C, b, \mathrm{cost}, \{u_i\})$, $|N|=n$. Ogni votante parte con $b/n$. Dato l'esito parziale $W$, il residuo è $b_i = b/n - p_i(W)$. Un candidato $c\notin W$ è **$\rho$-affordable** se
  $$\sum_{i\in N}\min\big(b_i,\; u_i(c)\cdot\rho\big) = \mathrm{cost}(c).$$
  Si sceglie il $c$ affordable con $\rho$ minimo; i pagamenti sono $p_i(c)=\min(b_i,\,u_i(c)\cdot\rho)$; ci si ferma quando nessun candidato è affordable per alcun $\rho$. Con utilità di approvazione il costo è ripartito "il più equamente possibile" tra i sostenitori. — [arXiv 2008.13276](https://arxiv.org/abs/2008.13276)
- Principi derivati nell'esempio del paper (p. 8): "more supporters is better", "cheaper is better", "richer supporters is better"; nell'esempio con $b=100$ MES spende solo 49 → servono regole di **completamento** (§3.4 del paper) — [V, PDF]
- **EJR** (formulazione del paper, p. 4): se un gruppo $S$ può finanziare un insieme $T$ con la quota $|S|/|N|$ del bilancio e ogni membro di $S$ approva tutto $T$, allora almeno un votante di $S$ approva almeno $|T|$ progetti dell'esito $W$. **Teorema 2**: per PB con approvazione MES soddisfa EJR — [V, PDF p. 4]
- Con utilità additive arbitrarie MES soddisfa EJR "up to one project"; esiste sempre un esito EJR ma, salvo P = NP, nessun metodo fortemente polinomiale lo garantisce; PAV non si estende ai costi arbitrari (Teorema 1: ogni regola che dipende solo da utilità e insiemi ammissibili fallisce la proporzionalità) — [V, abstract + PDF pp. 4–5] [arXiv 2008.13276](https://arxiv.org/abs/2008.13276)
- **Core** e **FJR**: un gruppo $S$ "blocca" $W$ se esiste $T$ finanziabile con quota $|S|/|N|$ che ogni membro preferisce strettamente; esistenza del core nel caso approvazione "unknown… even under the unit cost assumption"; per utilità additive generali il core può essere vuoto. FJR, più debole del core ma più forte di EJR, è sempre soddisfacibile con una regola greedy non polinomiale; PAV e MES lo violano — [V, PDF pp. 5–6]
- **Phragmén** e Chamberlin–Courant soddisfano solo assiomi più deboli (PJR, JR); Phragmén e MES soddisfano la **priceability** (Peters & Skowron 2020) — [V, PDF p. 5 e nota 1]
- **JR** (Aziz, Brill, Conitzer, Elkind, Freeman, Walsh): "if a large enough group of voters exhibits agreement by supporting the same candidate, then at least one voter in this group has an approved candidate in the winning committee"; PAV soddisfa JR ed EJR, RAV non soddisfa JR — [V, abstract] [arXiv 1407.8269](https://arxiv.org/abs/1407.8269). Forma standard [L]: per comitato di dimensione $k$, ogni gruppo $S$ con $|S|\ge n/k$ e $\bigcap_{i\in S}A_i\neq\emptyset$ ha almeno un membro con $|A_i\cap W|\ge1$; EJR: per ogni $\ell$, $|S|\ge \ell n/k$ e $|\bigcap_{i\in S}A_i|\ge \ell$ ⇒ $\exists i\in S: |A_i\cap W|\ge \ell$. Sede (*Social Choice and Welfare* 48, 2017) [L].
- **Wieliczka (Polonia), "Zielony Milion", aprile 2023**: 1 milione di zł (~220.000 €); la pagina ufficiale ospitata da equalshares.net afferma che è diminuita la quota di votanti senza influenza sull'esito e che si è evitata l'esclusione dei progetti della parte sud del comune — [S, riassunto di ricerca; pagina non raggiungibile] [equalshares.net/elections/zielony-milion](https://equalshares.net/elections/zielony-milion/). Valutazione dei promotori, non indipendente.
- **Aarau (Svizzera), "Stadtidee", giugno 2023**: MES ha selezionato **17 progetti su 33 contro 7** del greedy utilitario, sacrificando il terzo progetto più popolare; un preprint riporta **+27,8%** di votanti che raggiungono un livello minimo di rappresentanza (una figura supplementare riporta **22,6%**: discrepanza tra versioni) — [S] [Pournaras et al., arXiv 2505.14349](https://arxiv.org/html/2505.14349); [arXiv 2405.05085](https://arxiv.org/html/2405.05085v1)
- Pournaras et al. (arXiv 2505.14349, v2 dic. 2025): ad Aarau voto cumulativo ed Equal Shares finanziano più progetti a parità di bilancio, rappresentano meglio geografia e preferenze dei votanti prima sotto-rappresentati; evidenza causale che i cittadini preferiscono metodi proporzionali e li associano ad altruismo e compromesso — [V, abstract] [arXiv 2505.14349](https://arxiv.org/abs/2505.14349)
- Analisi degli effetti (Royal Society Phil. Trans. A 382, 2024): MES riallocherebbe bilancio con −7% per progetti di spazio pubblico e fino a +25% per progetti di welfare — [S, riassunto; non letto] [rsta 20240096](https://royalsocietypublishing.org/rsta/article/382/2285/20240096/108461/Fair-voting-outcomes-with-impact-and-novelty)
- Sotto-spesa: problema noto, affrontato da varianti ("Streamlining Equal Shares", "adaptive and verifiably proportional method") — [S] [arXiv 2502.11797](https://arxiv.org/html/2502.11797); [arXiv 2310.10215](https://arxiv.org/pdf/2310.10215)
- **Stanford (Goel)**: *Knapsack Voting* — ogni votante sceglie un insieme di progetti che rientra nel bilancio; strategy-proof sotto un modello naturale di utilità e "parzialmente" con utilità additive; usato come procedura ufficiale nel PB "Youth Lead the Change", Boston 2016; ACM TEAC 7(2), art. 8, 2019 — [S, risultati di ricerca] [arXiv 2009.06856](https://arxiv.org/pdf/2009.06856). La piattaforma Stanford PB è indicata come usata in "più di 150" processi — [S, citato in un listing arXiv non identificato; da verificare].

### Inferences
- [I] Per i lotti, MES va adattato: i "progetti" diventano lotti (o coppie gruppo–lotto) e il "bilancio" diventa capacità (numero di famiglie, superficie, fondi pubblici). Il principio "richer supporters is better" significa che chi non è ancora stato servito pesa di più nei turni successivi: è la protezione delle minoranze in forma algoritmica.
- [I] Il sacrificio del terzo progetto più popolare ad Aarau è il prezzo visibile della proporzionalità: va mostrato ai residenti prima del voto, altrimenti l'esito appare manipolato dal mediatore.
- [I] La gerarchia degli assiomi dà un **linguaggio di garanzie pubblicabili**: "ogni gruppo coeso che è l'x% può ottenere almeno ...". È la forma giusta per rendere il mediatore non nascosto.

### Gaps
- Pagine ufficiali di Wieliczka e Aarau e dati grezzi (Pabulib) non letti: rete bloccata.
- Altri dispiegamenti MES (es. Świecie, Assen, altri 2024–2026) non verificati.
- Nessuna applicazione di MES a lotti o alloggi trovata (conferma la lacuna del report precedente).
- Lavori di Elkind (Oxford) su PB e proporzionalità con vincoli non cercati per limite di chiamate.

## 3. Sorteggio e assemblee di cittadini: selezione equa

### Takeaway
Flanigan, Gölz, Gupta, Hennig, Procaccia (Nature 596, 2021) trattano la selezione di un panel come lotteria su panel che rispettano le quote, e scelgono la distribuzione che rende le probabilità individuali di selezione "il più uguali possibile" (LEXIMIN: massimizza la minima, poi la seconda minima, ecc.). È stato usato in oltre 40 assemblee. Lavori successivi mostrano che LEXIMIN è manipolabile e propongono l'obiettivo Goldilocks.

### Cited Findings
- Le probabilità di selezione sono rese "as close to equal as mathematically possible" con vincoli di rappresentatività (quote); LEXIMIN ha minime probabilità di selezione più alte del metodo LEGACY (greedy) su dati di **dieci** assemblee; LEGACY "often selects some pool members with near-zero probability"; l'implementazione "has already been used to select more than 40 citizens' assemblies around the world" — [S, abstract via risultati di ricerca; Nature non raggiungibile] DOI 10.1038/s41586-021-03788-6, [PMC8387237](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8387237/)
- Forma standard [L]: pool $N$ ($|N|=n$), dimensione $k$, quote $\ell_{f,v}\le |P\cap N_{f,v}|\le u_{f,v}$ per ogni attributo $f$ e valore $v$; un **panel** è un $P\subseteq N$ ammissibile; un algoritmo è una distribuzione $\mathcal D$ sui panel; $\pi_i=\Pr_{P\sim\mathcal D}[i\in P]$; LEXIMIN massimizza lessicograficamente il vettore ordinato $(\pi_{(1)},\pi_{(2)},\dots)$, cioè prima $\max_{\mathcal D}\min_i\pi_i$. Risolto con generazione di colonne (column generation) [L].
- **Baharav & Flanigan, "Fair, Manipulation-Robust, and Transparent Sortition"** (arXiv 2406.15009): LEXIMIN "raises low probabilities without regard for high probabilities" e permette a un membro del pool di portare la propria probabilità a 1 dichiarando falsi attributi; MINIMAX resiste ma dà spesso probabilità zero. Obiettivo proposto:
  $$\mathrm{Goldilocks}_\gamma(\pi)=\frac{\max(\pi)}{k/n}+\gamma\,\frac{k/n}{\min(\pi)}$$
  con $\gamma=1$ come caso principale; su **9** istanze reali raggiunge minimi quasi-LEXIMIN e massimi quasi-MINIMAX; reso **trasparente** arrotondando a una lotteria uniforme su $m$ panel pubblicati in anticipo, con $m\ge n\sqrt n$ — [V, testo HTML] [arXiv 2406.15009](https://arxiv.org/html/2406.15009v2)
- La pagina "Panelot" (panelot.org) e il ruolo della Sortition Foundation non sono stati verificati in sessione [L].

### Inferences
- [I] Il sorteggio con probabilità esplicite è il modello più maturo di "algoritmo che decide chi decide" reso pubblico: la lotteria uniforme su panel pubblicati è un esempio diretto di **trasparenza verificabile** che la tesi può copiare per la formazione dei gruppi misti.
- [I] Le quote di sorteggio sono l'analogo formale dei vincoli di diversità dei gruppi (età, condizione): la tesi può formulare la diversità come quote $\ell_{f,v},u_{f,v}$ e chiedere equità delle probabilità individuali di essere assegnati a un gruppo/lotto.
- [I] La manipolabilità di LEXIMIN avverte: ogni attributo autodichiarato usato per la diversità diventa un canale di manipolazione.

### Gaps
- Numeri esatti di Nature 2021 (minime probabilità per istanza) non letti: Nature e PMC bloccati.
- Aggiornamenti 2023–2026 su dropout, auto-selezione e numero corrente di assemblee non verificati.

## 4. Scelta sociale generativa, scelta sociale per l'allineamento, allineamento pluralista

### Takeaway
La generative social choice dà garanzie di rappresentanza solo assumendo oracoli che l'LLM approssima; la garanzia empirica è un sondaggio, non una prova. Il position paper di Conitzer et al. (2024) mostra che il RLHF aggrega già preferenze in modo implicito e poco trasparente (vicino al Borda), e propone di rendere esplicita la regola: è esattamente la critica del "decisore nascosto".

### Cited Findings
- **Conitzer, Freedman, Heitzig, Holliday, Jacobs, Lambert, Mossé, Pacuit, Russell, Schoelkopf, Tewolde, Zwicker**, "Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback", arXiv 2404.10271 (v2 giugno 2024; sede ICML 2024 non confermata dalla pagina [L]) — [V]
  - §2.2: l'aggregazione nel RLHF "implicitly amounts to a rather intransparent or flawed form of preference aggregation" — [V]
  - §2.5 / §7.1: approcci standard al RLHF usano implicitamente il **conteggio di Borda**, che "badly violates independence of clones" — [V]
  - §2.5: richiamo di Arrow ("the only aggregation functions satisfying these desiderata are dictatorships") e necessità di indebolire IIA — [V]
  - §4: chi dà il feedback (campioni rappresentativi, assemblee di cittadini, liquid democracy); §6.1 proposta **RLCHF** (Reinforcement Learning from Collective Human Feedback); §6.2 decisioni collettive simulate; §9 possibilità di **più sistemi IA** invece di uno — [V] [arXiv 2404.10271](https://arxiv.org/html/2404.10271v2)
- **Fish, Gölz, Parkes, Procaccia et al., Generative Social Choice**, JACM 73(2) 2026, arXiv 2309.01291: garanzie dimostrate con query oracolo, poi approssimate con LLM; 84/100 partecipanti statunitensi si sono detti rappresentati "excellently/exceptionally" da uno slate di 5 enunciati — [V, abstract, dal report precedente] [arXiv 2309.01291](https://www.arxiv.org/abs/2309.01291). Assioma di riferimento: forma di **BJR** (balanced justified representation) adattata a enunciati [L, da verificare sul testo].
- **Allineamento pluralista** (Sorensen et al. 2024, arXiv 2402.05070) e lavori DeepMind sulla mediazione (Habermas Machine, Science 2024): non riletti in sessione; vedi report precedente [L].

### Inferences
- [I] Per la tesi: ogni passo in cui un LLM riassume, raggruppa o riformula criteri è un **aggregatore** e va dichiarato come tale, con la regola e gli assiomi che soddisfa o viola. L'osservazione di Conitzer et al. sul Borda implicito vale anche per un LLM che "sintetizza le esigenze" del gruppo.
- [I] Independence of clones conta per i criteri: se il mediatore genera tre varianti quasi identiche del criterio "verde", la regola non deve dare al verde tre volte il peso.
- [I] La garanzia di Fish et al. è condizionata alla qualità dell'oracolo LLM: va trattata come ipotesi da testare con i residenti, non come proprietà acquisita.
- [H] Protocollo: il catalogo dei criteri è generato con generative social choice, poi i pesi sono aggregati con Independent Markets; si misura (a) quota di residenti che si sente rappresentata, (b) peso ottenuto dalle minoranze coese, (c) effetto di cloni introdotti apposta.

### Gaps
- Testo completo di Fish et al. e definizione esatta dell'assioma non riletti.
- Lavori 2025–2026 su social choice per LLM (es. Ge et al. "Axioms for AI alignment from human feedback", "pluralistic alignment" benchmark, DeepMind "Habermas Machine" seguiti) non cercati per limite di chiamate.

## 5. Impossibilità e manipolazione: cosa significano per i "criteri riscrivibili"

### Takeaway
Arrow e Gibbard–Satterthwaite dicono che nessuna regola con tre o più opzioni è insieme non dittatoriale, sensibile a tutte le preferenze e immune da manipolazione. Le uscite note sono restrizioni di dominio (preferenze single-peaked, ℓ1 su bilanci), randomizzazione e rinuncia esplicita a qualche assioma. Per criteri riscrivibili ne segue che la regola di aggregazione stessa va scelta e pubblicata, e che l'immunità totale alla manipolazione è disponibile solo nei formati ristretti (es. mediane, moving phantoms).

### Cited Findings
- Arrow: con le condizioni richiamate (IIA, completezza, transitività, unanimità) l'unica funzione di aggregazione possibile è dittatoriale — [V, come riportato in Conitzer et al. §2.5] [arXiv 2404.10271](https://arxiv.org/html/2404.10271v2)
- "Every reasonable voting rule will sometimes introduce incentives to manipulate"; la mediana è strategy-proof nel caso delle valutazioni — [V, §7.2] [arXiv 2404.10271](https://arxiv.org/html/2404.10271v2)
- Gibbard (1973), Satterthwaite (1975), forma standard [L]: ogni funzione di scelta sociale deterministica, suriettiva su almeno 3 alternative, a dominio universale e strategyproof è dittatoriale.
- Restrizione di dominio che salva la strategyproofness: preferenze ℓ1 su bilanci → moving phantoms strategyproof (Freeman et al.) — [V, abstract] [arXiv 1905.00457](https://arxiv.org/abs/1905.00457); Moulin (1980) mediane generalizzate per preferenze single-peaked [L].
- Knapsack Voting strategy-proof sotto un modello naturale di utilità, solo "parzialmente" con utilità additive generali — [S] [arXiv 2009.06856](https://arxiv.org/pdf/2009.06856)
- MES e EJR non sono strategyproof in generale [L: risultato noto in letteratura, non verificato qui]. Teorema 1 di Peters et al.: nessuna regola basata solo su utilità e insiemi ammissibili è proporzionale con costi → la proporzionalità richiede informazione sui costi e regole "di mercato" come MES — [V, PDF p. 4]

### Inferences
- [I] **Meta-livello**: se i residenti possono riscrivere anche la regola di aggregazione, il problema si sposta di un livello (scelta della regola = altra scelta sociale, con le stesse impossibilità). Serve un punto fisso dichiarato: una costituzione minima (formato del voto, regola, assiomi garantiti) che non è riscrivibile nello stesso processo.
- [I] Compromesso da rendere pubblico: strategyproofness + proporzionalità sui pesi (Independent Markets) è possibile; proporzionalità sui lotti (MES) sì, strategyproofness no; Pareto-ottimalità e proporzionalità insieme no nei moving phantoms.
- [I] Il mediatore IA non deve mai scegliere tra queste rinunce: la scelta va fatta dal gruppo con le conseguenze mostrate su casi simulati.

### Gaps
- Risultati su manipolabilità di MES/EJR e su complessità della manipolazione non verificati.
- Non sono stati cercati lavori di TU Wien/TU Berlin (Brill, Lackner, Lackner–Skowron *Multi-Winner Voting with Approval Preferences*, Springer 2023) né di CMU (Conitzer è a CMU/Oxford) oltre al position paper: da completare.
