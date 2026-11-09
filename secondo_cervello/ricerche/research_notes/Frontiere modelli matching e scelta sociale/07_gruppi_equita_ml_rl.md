# Gruppi eterogenei, equità e frontiera ML/RL per pianificazione e allocazione (nota 07)

Sessione 2026-11-09. Estende `secondo_cervello/ricerche/reports/Lotti ideali partecipazione e digital twin.md` (§ gruppi, righe 59–61, 98–99, 109).

**Legenda.** [V] letto in sessione su pagina primaria (abstract arXiv/AAAI o testo integrale estratto, indicato); [S] da snippet di ricerca, record secondario o riassunto di terzi; [I] inferenza mia; [H] ipotesi da testare; [L] lacuna o elemento noto ma non riaperto in sessione. **[forma standard]** = equazione nella forma canonica della letteratura, scritta da me e non copiata dal paper citato: va controllata sull'originale prima di entrare in tesi. Nessun numero di pagina è disponibile.

**Limite tecnico della sessione.** I domini nature.com, science.org, proceedings.neurips.cc, ar5iv, tsinghua.edu.cn e bengravell.github.io non erano raggiungibili dalla rete dell'ambiente. Zheng et al. 2023 e l'AI Economist su *Science Advances* sono quindi letti solo tramite arXiv, GitHub o snippet. Unico testo integrale letto: Boehmer & Elkind (AAAI 2020), estratto dal PDF arXiv.

---

## 1. Un gruppo misto può essere insieme diverso e stabile? Esistenza e complessità delle partizioni stabili con preferenze di diversità, e quali indebolimenti sono trattabili

### Takeaway
Sì, ma solo in un caso stretto. Con **due** tipi di agenti (per esempio "giovane/anziano") esiste sempre una partizione **individualmente stabile** (IS), calcolabile in tempo polinomiale [V]. Nash stabilità e core possono mancare, e deciderne l'esistenza è NP-completo [V]. Con **tre o più** tipi anche la stabilità individuale può non esistere; con k ≥ 5 deciderlo è NP-completo [V]. Una diversità a più attributi (età × condizione × reddito) cade proprio nel regime senza garanzie [I]. L'indebolimento che la teoria sostiene è "proposta + consenso": IS (serve il consenso di chi accoglie) o la stabilità contrattuale (serve anche il consenso di chi viene lasciato) [S/L], non il core.

### Cited Findings

**Concetti di stabilità (definizioni)**
- Gioco edonico: $G=(N,(\succeq_i)_{i\in N})$, dove ogni $\succeq_i$ è un ordine debole sulle coalizioni che contengono $i$. Un esito è una partizione $\pi$, e $\pi_i$ è la coalizione di $i$ [V, testo integrale] — [Boehmer & Elkind, AAAI 2020, arXiv 1911.08669](https://arxiv.org/pdf/1911.08669)
- **Deviazione NS**: $i$ ha una deviazione NS da $\pi$ se esiste $C\in\pi\cup\{\emptyset\}$ con $C\cup\{i\}\succ_i \pi_i$. **Deviazione IS**: in più, $C\cup\{i\}\succeq_j C$ per ogni $j\in C$, cioè chi accoglie non peggiora. $\pi$ è Nash stabile (NS) o individualmente stabile (IS) se nessun agente ha la deviazione corrispondente [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- **Core** [forma standard]: $\pi$ è nel core se non esiste $S\subseteq N$, $S\neq\emptyset$, con $S\succ_i\pi_i$ per ogni $i\in S$. Boehmer & Elkind descrivono il core come resilienza alle deviazioni di gruppo, mentre NS e IS riguardano deviazioni individuali [V, parafrasi] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- **Stabilità individuale contrattuale (CIS)** [forma standard, L]: la deviazione di $i$ verso $C$ è ammessa solo se $C\cup\{i\}\succ_i\pi_i$, se $C\cup\{i\}\succeq_j C$ per ogni $j\in C$ e se $\pi_i\setminus\{i\}\succeq_k\pi_i$ per ogni $k\in\pi_i\setminus\{i\}$. Le gerarchie NS ⇒ IS ⇒ CIS e "il core implica la core-stabilità debole" sono note; non le ho verificate su un testo primario in sessione.
- Bogomolnaia e Jackson (*GEB* 38(2), 2002, 201–230) danno condizioni sufficienti per il core. Si concentrano poi sulla stabilità individuale ("nessun giocatore guadagna spostandosi senza danneggiare la coalizione di arrivo") e mostrano che, senza condizioni aggiuntive, una partizione IS può non esistere [S, abstract via repository] — [Enlighten Glasgow](https://eprints.gla.ac.uk/86597); [EconPapers](https://econpapers.repec.org/RePEc:eee:gamebe:v:38:y:2002:i:2:p:201-230)
- L'attribuzione della CIS a Bogomolnaia–Jackson compare in Karakaya (*Mathematical Social Sciences*), secondo un riassunto di ricerca [S, da verificare] — [core.ac.uk](https://core.ac.uk/download/52922936.pdf)
- Drèze & Greenberg (1980), che introducono i giochi edonici: in sessione non ho trovato né letto record o testo [L].

**Hedonic diversity games (HDG)**
- Definizione: $N=R\cup B$. Ogni agente è indifferente tra coalizioni con la stessa frazione di rossi, quindi le preferenze sono un ordine su $\theta(C)=|C\cap R|/|C|$; $C\succeq_i D \iff \theta(C)\succeq'_i\theta(D)$. Le preferenze sono *single-peaked* se esiste un picco $\rho_i$ e $\succeq'_i$ decresce allontanandosi da $\rho_i$ [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- Il modello differisce da Schelling: alcuni agenti possono preferire gruppi misti o a maggioranza dell'altro tipo. Il core può non esistere e verificarne l'esistenza è computazionalmente difficile. Con preferenze single-peaked esiste un algoritmo efficiente per un esito IS [V, abstract] — [Bredereck, Elkind & Igarashi, AAMAS 2019, arXiv 1903.00303](https://arxiv.org/abs/1903.00303)
- Secondo Boehmer & Elkind, Bredereck et al. mostrano che un HDG può non avere esiti NS o core e che decidere se esiste un esito nel core è NP-completo [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- **Teorema 3.1**: decidere se un HDG ha un esito NS è NP-completo. **Teorema 3.2**: è decidibile in tempo $(np)^p\cdot\mathrm{poly}(n)$, con $p$ la dimensione della classe minore, quindi XP rispetto a $p$ [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- **Teorema 4.1**: in **ogni** HDG, anche senza single-peakedness, un esito IS si calcola in tempo polinomiale. Gli autori lo dicono "particularly surprising" perché non ogni gioco anonimo ammette un esito IS (Bogomolnaia & Jackson 2002). Né il loro algoritmo né quello di Bredereck et al. domina l'altro in senso Paretiano [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669); [AAAI record](https://ojs.aaai.org/index.php/AAAI/article/view/5549)
- **k classi**: nel k-tuple HDG ogni agente valuta il vettore delle frazioni di ciascuna classe nella coalizione. L'esempio 5.3, con 3 agenti di 3 classi e preferenze cicliche, **non ha alcun esito IS**. **Teorema 5.4**: per $k\ge5$ decidere l'esistenza di un esito IS è NP-completo (riduzione da X3C). Il risultato XP per NS si estende se le $k-1$ classi minori hanno dimensione costante [V, testo integrale] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- Il confronto empirico (algoritmo B&E, algoritmo Bredereck et al., dinamica di better response) misura benessere sociale, dimensione delle coalizioni e *mixedness*. Sul suo dominio l'algoritmo di Bredereck et al. va meglio empiricamente [V, testo integrale, senza cifre trascritte] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)
- Un lavoro successivo risolve per due colori una domanda aperta di Boehmer & Elkind. Risultato non letto [S] — [arXiv 2202.09210](https://arxiv.org/html/2202.09210v2)

**Fractional hedonic games (FHG)**
- L'utilità è il valore medio dato ai membri della coalizione; in forma standard $u_i(C)=\sum_{j\in C}v_i(j)/|C|$ [forma standard]. Il core può essere vuoto su grafi generali ed è non vuoto per classi ristrette (grafi multipartiti completi, alberi) [S, abstract via ricerca] — [Aziz et al., arXiv 1705.10116](https://arxiv.org/pdf/1705.10116)
- Il core può mancare anche con valutazioni simmetriche 0/1 ("mutual friendship") [S] — [Brandl, Brandt & Strobel](https://www.comp.nus.edu.sg/~mstrobel/paper/fhg_stability.pdf)
- Complessità: verificare l'appartenenza al core è coNP-completo e decidere se il core è vuoto è $\Sigma_2^p$-completo [S, da riassunto secondario, da verificare] — [Aziz et al. 1705.10116](https://arxiv.org/pdf/1705.10116); popolarità $\Sigma_2^p$-completa [S] — [Bullinger & Gilboa, arXiv 2411.05713](https://export.arxiv.org/pdf/2411.05713)
- Esistono FHG non rappresentabili come HDG [V, testo B&E] — [Boehmer & Elkind 2020](https://arxiv.org/pdf/1911.08669)

**Schelling games (controfattuale di segregazione)**
- Agenti di k tipi scelgono posizioni su un grafo. Un equilibrio di Nash puro esiste su stelle e su grafi di grado massimo 2, ma può mancare su grafi aciclici di grado massimo 4. Sugli alberi l'esistenza si decide in tempo polinomiale (programmazione dinamica). Il lavoro dà anche limiti su price of anarchy e price of stability [S, abstract via ricerca] — [Elkind, Gan, Igarashi, Suksompong & Voudouris, IJCAI 2019](https://ijcai.org/proceedings/2019/38)
- Varianti: swap Schelling games, in cui calcolare un'assegnazione ad alto benessere è NP-completo; modified Schelling games [S] — [arXiv 1909.02421](https://arxiv.org/pdf/1909.02421v1); [arXiv 2005.12149](https://arxiv.org/abs/2005.12149)

### Inferences
- [I] La risposta teorica onesta: "diverso **e** stabile" è garantito solo per un attributo binario e per la nozione debole IS. Con k ≥ 3 attributi di tipo anche IS può mancare. La tesi non può promettere stabilità per gruppi misti su molte dimensioni: deve **misurarla** (quota di famiglie con una deviazione ammissibile) invece di presupporla.
- [I] Negli HDG la diversità è una **preferenza degli agenti**. Nella tesi è soprattutto un **requisito collettivo dichiarato** (DECISIONI 9/11). Sono modelli diversi: nel primo un gruppo misto è stabile se le persone lo vogliono, nel secondo è imposto e la stabilità va controllata contro preferenze che possono essere omofile. Il caso peggiore per la tesi è un vincolo di mix con preferenze omofile, e lì la letteratura Schelling suggerisce pressione verso la ri-segregazione.
- [I] IS e CIS corrispondono a regole procedurali leggibili: IS = "entri in un gruppo solo se il gruppo acconsente"; CIS = "esci solo se chi resta acconsente". È la forma "proposta + consenso" che la nota precedente indicava [H], ora con un fondamento formale. Il core (deviazioni di gruppo) è troppo forte e computazionalmente proibitivo.
- [H] Uso possibile: ridurre la composizione obbligatoria a **un vincolo binario per volta** (per esempio "almeno un nucleo over-65 e almeno un nucleo con figli"), così da restare nel regime k = 2 con IS garantito, e trattare le altre dimensioni come obiettivi morbidi.

### Gaps
- Testo di Bredereck–Elkind–Igarashi non letto per intero: non so quale classe di preferenze garantisce NS né i dettagli della prova di NP-durezza del core [L].
- Drèze–Greenberg 1980: record e definizioni non verificati [L].
- Esistenza universale della CIS (ricordo, non verificato, Ballester 2004 *GEB*) [L].
- Non ho trovato lavori che applichino HDG o FHG alla formazione di gruppi di cohousing o a dati abitativi reali [L, assenza nella ricerca, non prova di assenza].
- Mancano le cifre empiriche di B&E sul benessere sociale [L].

---

## 2. Come codificare una "diversità dichiarata e negoziabile": vincolo o obiettivo, e curve di trade-off (price of fairness / price of diversity)

### Takeaway
La letteratura offre due codifiche. Come **vincolo**, con bilanciamento o limiti di proporzione per cluster (fair clustering) o quote nel matching (diverse b-matching). Come **obiettivo**, con un termine di diversità o welfare (Nash welfare, MNW). Il costo della diversità si misura come rapporto tra ottimo vincolato e non vincolato (price of diversity / price of fairness). In alcuni dati reali è piccolo (≈1% su MovieLens [S]), ma non esistono stime su dati abitativi [L]. Per i beni indivisibili, il massimo Nash welfare dà EF1 e approssima MMS, ed è stato usato davvero (Spliddit) [V/S].

### Cited Findings

**Fair clustering**
- Chierichetti, Kumar, Lattanzi e Vassilvitskii (NIPS 2017, pp. 5036–5044): ogni classe protetta deve avere "approximately equal representation in every cluster". Qualsiasi problema di fair clustering si scompone nella ricerca di *fairlet* (insiemi minimi bilanciati), seguita da clustering standard. Trovare buoni fairlet può essere NP-hard; gli autori danno approssimazioni via flusso a costo minimo. Nel clustering equo un punto può non essere assegnato al centro più vicino [V, abstract] — [arXiv 1802.05733](https://arxiv.org/abs/1802.05733)
- Bilanciamento, due colori [forma standard]: $\mathrm{balance}(Y)=\min\!\left(\frac{|Y\cap R|}{|Y\cap B|},\frac{|Y\cap B|}{|Y\cap R|}\right)\in[0,1]$, e il bilanciamento del clustering è il minimo sui cluster. Fattori di approssimazione per fair k-center e k-median non verificati (PDF NeurIPS irraggiungibile) [L].
- Bera, Chakrabarty, Flores e Negahbani (2019): l'utente fissa parametri che limitano la sovra- e sotto-rappresentazione di ogni gruppo in ogni cluster. Vale per ogni obiettivo $\ell_p$ (k-means, k-median, k-center) e ammette gruppi protetti sovrapposti. La perdita di qualità è "slight", e in pratica il metodo va meglio della garanzia teorica [V, abstract] — [arXiv 1901.02393](https://arxiv.org/abs/1901.02393)
- Vincolo di Bera et al. [forma standard]: per ogni cluster $C$ e gruppo $P_t$, $\beta_t\le |C\cap P_t|/|C|\le\alpha_t$. Natura del limite di violazione additiva non verificata [L]. Bercea et al. (fair clustering, APPROX 2019) non riaperto [L].

**Diversity nel matching / team formation**
- Ahmed, Dickerson e Fuge (IJCAI 2017): b-matching bipartito in cui un agente si abbina a *insiemi* di agenti, con funzione di diversità. Definiscono il **price of diversity** (perdita di efficienza imposta dalla diversità) con un limite teorico nel caso peggiore e mostrano che su tre dataset reali "is not bad in practice". L'algoritmo greedy polinomiale ha garanzie rispetto al problema principale NP-hard [S/V, abstract via ricerca] — [IJCAI 2017](https://www.ijcai.org/proceedings/2017/6); [arXiv 1702.07134](https://arxiv.org/pdf/1702.07134.pdf)
- Su MovieLens la perdita di utilità sarebbe ≈1% (PoD 0,99) [S, solo da un riassunto di terzi, da verificare sul paper] — [liner.com](https://liner.com/en/review/diverse-weighted-bipartite-bmatching)
- Price of diversity [forma standard]: $\mathrm{PoD}=\mathrm{OPT}_{\text{div}}/\mathrm{OPT}$ (≤ 1 per massimizzazione); analogo al price of fairness.

**Fair division di beni indivisibili** (rilevante per l'assegnazione dei lotti ai gruppi o delle unità nel villaggio verticale)
- Definizioni [forma standard; additività assunta]: allocazione $A=(A_1,\dots,A_n)$ e valutazioni $v_i$.
  - **EF1**: $\forall i,j\ \exists g\in A_j:\ v_i(A_i)\ge v_i(A_j\setminus\{g\})$ (o $A_j=\emptyset$).
  - **MMS**: $\mu_i=\max_{(P_1..P_n)}\min_k v_i(P_k)$; $A$ è MMS se $v_i(A_i)\ge\mu_i$ per ogni $i$, e $\alpha$-MMS se $v_i(A_i)\ge\alpha\mu_i$.
  - **Nash welfare**: $\mathrm{NW}(A)=\prod_i v_i(A_i)$; MNW = $\arg\max$ (massimizzando prima il numero di agenti con utilità positiva).
- Caragiannis, Kurokawa, Moulin, Procaccia, Shah e Wang, "The Unreasonable Fairness of Maximum Nash Welfare" (*ACM TEAC* 2019; EC 2016): MNW con beni indivisibili seleziona allocazioni **EF1** (e Pareto-ottime) e approssima la garanzia MMS, che può essere infeasible, "both in theory and even more so in practice". Calcolare MNW è difficile, ma l'implementazione scala sui dati reali ed è stata messa in uso su Spliddit [S/V, abstract via repository] — [Enlighten Glasgow](https://eprints.gla.ac.uk/198815); [PDF Toronto](https://www.cs.toronto.edu/~nisarg/papers/mnw.pdf)
- Spliddit ha usato MNW dal 2015 fino alla chiusura a fine 2022. Il paper ha vinto il premio Kalai 2024 [S, riassunto di ricerca] — [Game Theory Society](https://gametheorysociety.org/?p=4235)
- Il fattore preciso di approssimazione MMS garantito da MNW non è stato riletto [L].

### Inferences
- [I] Una "diversità dichiarata e negoziabile" si traduce bene nel vincolo di Bera et al.: i limiti $(\beta_t,\alpha_t)$ per gruppo sono **parametri pubblici e votabili**, e cambiarli genera una curva qualità–diversità leggibile. È l'oggetto "criteri e pesi pubblici e riscrivibili" della domanda di ricerca.
- [I] Attenzione: il fair clustering minimizza ancora una **distanza** dentro il cluster. Se la metrica è costruita su somiglianza di esigenze, il risultato resta "Housing Prime con quote". La metrica va scelta come complementarità o compatibilità (per esempio orari, bisogni di cura, competenze), non come somiglianza.
- [I] Vincolo o obiettivo: un vincolo duro rende la diversità garantita ma il costo cade sulla stabilità (§1). Un obiettivo morbido (penalità o welfare) rende la diversità negoziabile ma rischia che l'ottimizzatore la sacrifichi. In entrambi i casi, chi fissa soglie o pesi decide [I, coerente con la nota 00 §6].
- [H] Esperimento in simulazione: tracciare tre curve al variare delle soglie $\beta$: (a) costo della diversità (PoD); (b) quota di famiglie con una deviazione IS; (c) indice di Simpson o Shannon medio dei gruppi. È il "trade-off" della tesi, reso misurabile.
- [I] Per assegnare lotti a gruppi o unità a nuclei, MNW/EF1 è più adatto di una somma di utilità: protegge chi ha valutazioni basse e ha un precedente d'uso reale (Spliddit).

### Gaps
- Nessuna stima di price of diversity su dati di popolazione o abitativi [L].
- Formule esatte di Chierichetti (balance) e di Bera (violazione additiva) non lette sul testo [L].
- Teoria che leghi esplicitamente vincoli di proporzione e stabilità edonica (fair clustering + stabilità): non trovata in sessione [L].

---

## 3. Che cosa mostrano davvero i lavori di RL per la pianificazione e l'allocazione, e i loro limiti (chi scrive la ricompensa)

### Takeaway
Zheng et al. (2023) mostrano che un RL su grafo con GNN genera layout di comunità che **battono i piani di esperti sulle metriche del modello stesso**, cioè servizi ed ecologia. Il confronto è con 8 progettisti su due quartieri di Pechino [S]. Non c'è una valutazione con residenti, e le metriche sono scritte dagli autori [V/I]. L'AI Economist mostra un RL a due livelli (agenti + pianificatore) che migliora del 16% il trade-off equità–produttività rispetto alle baseline in simulazione [V], con esperimenti con persone [S]. In tutti questi lavori la ricompensa **è** la politica.

### Cited Findings
- Zheng, Lin, Zhao, Wu, Jin e Li, "Spatial planning of urban communities via deep reinforcement learning", *Nature Computational Science* 3(9), 748–762, 2023, DOI 10.1038/s43588-023-00503-5. Costruiscono un grafo per topologie urbane arbitrarie, formulano la pianificazione come decisione sequenziale sul grafo e usano RL con GNN. Il modello "outperforms plans designed by human experts in objective metrics" su comunità sintetiche e reali [V tramite abstract nella nota precedente; S in sessione] — [Nature Comp. Sci.](https://www.nature.com/articles/s43588-023-00503-5)
- Il confronto è con **otto progettisti professionisti invitati** su due comunità di Pechino (HLG, DHM), con metriche di servizio ed ecologia. Un flusso di lavoro collaborativo uomo–IA produce piani più efficienti "with much less time" [S, snippet] — [PDF autori](https://fi.ee.tsinghua.edu.cn/public/publications/77681512-6436-11ee-84fe-0242ac120002.pdf)
- Codice: dati da OpenStreetMap via OSMnx. I requisiti di piano (conteggi e aree minime/massime per uso) stanno in `objectives.yaml`. Baseline: euristiche centralizzate e decentralizzate a regole, GSCA (set coverage geometrico), algoritmo genetico. Durante l'addestramento si generano milioni di piani [V, README] — [GitHub tsinghua-fib-lab/DRL-urban-planning](https://github.com/tsinghua-fib-lab/DRL-urban-planning)
- Percentuali di miglioramento, formula esatta della ricompensa (pesi tra servizi a 15 minuti, verde e traffico) e dettagli dell'esperimento con esperti: non letti, perché nature.com è irraggiungibile [L].
- AI Economist (Zheng S., Trott, Srinivasa, Parkes, Socher): RL a due livelli in cui agenti economici e un pianificatore sociale co-adattano. È un problema "highly unstable" reso trattabile. In economie semplici a un passo recupera la politica fiscale ottima della teoria; in economie dinamiche migliora il welfare utilitarista e il trade-off equità–produttività. Le politiche apprese mostrano strategie emergenti di elusione fiscale (*tax gaming*) [V, abstract] — [arXiv 2108.02755](https://arxiv.org/abs/2108.02755)
- Versione precedente: le politiche IA migliorano il trade-off equità–produttività del **16%** rispetto alle baseline (incluso il quadro di Saez). In esperimenti con partecipanti umani il trade-off è simile a Saez, con welfare pesato sull'inverso del reddito più alto [V, abstract] — [arXiv 2004.13332](https://arxiv.org/abs/2004.13332). Pubblicazione su *Science Advances* 2022 (DOI 10.1126/sciadv.abk2607): record non raggiungibile [L].
- Formulazione a due livelli [forma standard, da verificare sul paper]: agenti $i$ con $\max_{\pi_i}\mathbb{E}\big[\sum_t\gamma^t r_{i,t}\big]$, ricompensa = variazione di utilità (reddito al netto del costo del lavoro); pianificatore $\max_{\pi_p}\mathbb{E}\big[\sum_t\gamma^t\,\Delta\mathrm{swf}_t\big]$. Ricordo, non verificato, la forma $\mathrm{swf}=\mathrm{eq}\cdot\mathrm{prod}$ con $\mathrm{eq}=1-\frac{N}{N-1}\mathrm{Gini}$ [L].
- Qian et al., "AI Agent as Urban Planner" (arXiv 2310.16772, preprint): agenti come rappresentanti di stakeholder votano usi del suolo; meccanismo di consenso nella ricompensa; grafo spaziale + GNN. Rivendicano maggiore beneficio globale e soddisfazione tra gruppi demografici. L'abstract non dice se gli input della comunità vengano da persone o da simulazione [V, abstract] — [arXiv 2310.16772](https://arxiv.org/abs/2310.16772)

### Inferences
- [I] "Batte gli esperti sulle metriche oggettive" vuol dire: batte gli esperti sulla funzione che l'RL ottimizza (o su metriche affini scritte dagli stessi autori). È un risultato di ottimizzazione, non una prova di qualità percepita né di aderenza alle esigenze degli abitanti.
- [I] In tutti e tre i lavori la ricompensa è fissata dagli autori: requisiti in `objectives.yaml`, funzione di welfare del pianificatore, regola di consenso. La domanda "chi scrive la ricompensa" coincide con quella della tesi su chi scrive criteri e pesi. Il *tax gaming* dell'AI Economist mostra anche che gli agenti sfruttano qualsiasi ricompensa: in un sistema partecipato le famiglie (o i loro agenti LLM) potrebbero fare lo stesso con la dichiarazione delle preferenze. Serve attenzione alla manipolabilità del meccanismo (strategy-proofness), non solo all'ottimo.
- [I] L'agente RL di Zheng piazza **usi del suolo**, non persone. Nessuno dei lavori letti forma gruppi di abitanti. La parte "gruppi" della tesi resta dominio della teoria dei giochi (§1–2), mentre l'RL serve eventualmente alla scala lotto/edificio.
- [H] Uso difendibile: RL a due livelli in simulazione, con agenti-famiglia e un "pianificatore" la cui ricompensa è un oggetto pubblico versionato. Si valuta su metriche fissate prima (accessibilità economica, deviazioni IS, diversità) e non sulla sola ricompensa.

### Gaps
- Numeri di Zheng et al. 2023 (miglioramenti, tempi, protocollo con gli esperti, eventuale studio di preferenza in cieco): da leggere sul PDF [L].
- Dettagli della sperimentazione umana dell'AI Economist (campione, piattaforma) e limiti dichiarati [L].
- Esiste una valutazione di RL urbano con **residenti** (non esperti) come giudici? Non trovata [L].

---

## 4. Frontiera ML utile ma onesta: GNN sui lotti, urban foundation models, agenti LLM come pianificatori

### Takeaway
Le GNN su grafi di lotti e strade sono già la base dei lavori RL di punta (Zheng 2023; Qian 2023) [V]. Gli urban foundation models hanno una rassegna di riferimento a KDD 2024 [V], ma servono rappresentazione e predizione, non decisione. Gli agenti LLM come rappresentanti di stakeholder sono finora preprint con valutazione in simulazione [V/I].

### Cited Findings
- GNN come codificatore della topologia urbana (lotti, strade, incroci) dentro l'RL [V, abstract] — [Zheng et al. 2023](https://www.nature.com/articles/s43588-023-00503-5); [Qian et al. 2310.16772](https://arxiv.org/abs/2310.16772)
- Zhang, Han, Xu, Ni, Liu e Xiong, "Urban Foundation Models: A Survey", KDD 2024, pp. 6633–6643. La tassonomia è data-centrica e organizzata per modalità di dato urbano; tratta sfide di costruzione e applicazioni. Versione arXiv: "Towards Urban General Intelligence…", 2402.01749, rivista (PDF datato marzo 2026) [S/V, record] — [HKUST](https://researchportal.hkust.edu.hk/en/publications/urban-foundation-models-a-survey-2/); [arXiv 2402.01749](https://arxiv.org/abs/2402.01749)
- Agenti LLM/RL come rappresentanti di stakeholder in pianificazione partecipata simulata [V, abstract] — [Qian et al.](https://arxiv.org/abs/2310.16772)
- Dalla nota precedente: la validazione spaziale casuale è "overly optimistic" (Meyer & Pebesma 2022), e nel Lab la PR-AUC scendeva da 0,93 a 0,33 con blocchi di 4 km [V nel report] — `secondo_cervello/ricerche/reports/Lotti ideali partecipazione e digital twin.md` riga 47.

### Inferences
- [I] Una GNN sui lotti serve a **descrivere** i lotti (embedding da vicinato, servizi, rete) per il matching. Non dà un'etichetta di "lotto ideale": manca una verità a terra, e addestrarla su ciò che si è costruito imparerebbe la redditività (stesso argomento del report precedente).
- [I] Gli agenti LLM che simulano famiglie sono utili nella fase "prima agenti" (DECISIONI), ma ogni risultato ottenuto con loro è una prova sul sistema, non sulle persone. Va dichiarato come tale ("le prove sono prove, non fonti").
- [H] Ordine prudente per la tesi: (1) teoria dei giochi e matching per gruppi e lotti, con garanzie; (2) GNN o foundation model solo come rappresentazione dei lotti, validata con CV spaziale; (3) RL e LLM solo in simulazione, con ricompensa pubblica.

### Gaps
- Non ho cercato lavori 2025–2026 su LLM agents per la pianificazione con valutazione umana (per esempio benchmark di "generative agents" urbani) [L].
- Nessuna fonte trovata su GNN o foundation model applicati a lotti edificabili in contesto italiano [L].
- La survey UFM non è stata letta oltre il record: non posso dire quali modelli coprano parcelle o catasto [L].
