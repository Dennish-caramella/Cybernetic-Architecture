# Spostare le ipotesi dai segni alle condizioni

Report di ricerca, 2026-11-10. Sintesi delle note 01–10 in `research_notes/Frontiere modelli matching e scelta sociale/`, costruita sopra il report `Lotti ideali partecipazione e digital twin.md`. Non è un capitolo di tesi. Marche (CLAUDE.md): **[V]** verificato sulla fonte primaria o sul suo record; **[S]** fonte secondaria, abstract o sintesi; **[I]** inferenza; **[H]** ipotesi o soglia da fissare; **[L]** lacuna, forma da manuale o riferimento non riaperto. **Avvertenza di metodo:** la rete dell'ambiente bloccava `science.org`, `nature.com`, `nber.org`, `ideas.repec.org`, `compdemocracy.org` e altri domini editoriali; **la maggior parte dei risultati qui riportati viene da abstract, record bibliografici e preprint arXiv**, non dal testo integrale pubblicato. Nessun numero di pagina interno è verificato. Prima di citare in tesi vale il testo originale o la scheda completa.

La letteratura di frontiera offre strumenti maturi per ogni passo della pipeline lotti → famiglie → gruppi → abbinamento → criteri → economia, ma **nessun lavoro trovato unisce formazione di gruppi eterogenei e scelta di lotti**, e nessuno mostra che un dispositivo partecipativo con IA abbia cambiato l'esito abitativo delle famiglie [L, note 01–02]. Il market design dà meccanismi con proprietà dimostrate (RSD, accettazione differita con riserve e soft bounds, perturbazione minima delle capacità per i gruppi), la scelta sociale computazionale dà regole proporzionali e non manipolabili per aggregare pesi e criteri (moving phantoms, Method of Equal Shares), la teoria dei giochi edonici dice esattamente quando un gruppo eterogeneo è stabile (due tipi sì, tre o più non garantito), e l'economia urbana dà un motore di flussi di cassa a due regimi. Tutti hanno un prezzo dichiarabile: nessun meccanismo è insieme stabile, efficiente e non manipolabile; nessuna aggregazione è coerente, anonima e sistematica; la domanda per quartiere non è identificabile con i dati aperti di Milano. La revisione critica (note 08–10) trova due difetti **fatali** — il confronto cooperativa contro developer è vero per costruzione, e la fase ad agenti è circolare — e un vuoto centrale: la seconda metà della domanda, il "decisore nascosto", non ha ancora una metrica. La correzione non richiede dati nuovi ma un cambio di forma: ipotesi su **condizioni** (quale regime del suolo, quale soglia di diversità, quale regola) invece che sul **segno** del vantaggio. Per la prima parte della tesi la strada è un MVP F1 di ~310 ore che dimostra **proprietà dei meccanismi** su un caso milanese realistico, non stime della domanda, con il capitolo 2 (dati e "pancia") da scrivere per primo entro febbraio 2027.

## Ogni passo della pipeline ha un modello maturo e un prezzo da dichiarare

### Urban science: descrittiva, normativa, mai causale sull'abitare

Il corpus dei laboratori urbani è quasi tutto descrittivo o normativo-simulativo [I, nota 01]. Nel modello ABM "casa + mobilità" di CityScope la scelta residenziale **non è un logit stimato**: è un punteggio lineare con pesi **sintetici** per fascia di reddito, una regola di trasloco alla Schelling e una calibrazione per hill climbing su 64 parametri contro due RMSE ([Yurrita et al., arXiv 2106.14572](https://arxiv.org/abs/2106.14572)) [V]. Finding Places (Amburgo) non aveva alcun modello di scelta: 34 workshop, ~400 partecipanti, 161 siti proposti, **6 raccomandati** per circa 750 posti, "~4% of the initial target"; circa tre quarti dei siti cadevano già nella classe "non idoneo" del pre-filtro ([Noyman et al., arXiv 1811.10123](https://arxiv.org/abs/1811.10123)) [V, testo integrale]. La lezione per la tesi è diretta: **il filtro di idoneità decide più dei workshop**, e va reso regola pubblica e contestabile [I].

Senseable City Lab misura la segregazione "sperimentata" come differenza di rango di reddito tra chi co-visita gli stessi luoghi; Abbiasov et al. trovano che l'accesso locale spiega l'81% della varianza tra aree urbane nell'uso a 15 minuti, con un IV sullo zoning del 1961 che gli autori stessi giudicano parziale ([arXiv 2211.14872](https://arxiv.org/abs/2211.14872)) [V preprint]. Il DRL di Tsinghua genera layout che "battono gli esperti" su una ricompensa scritta dal programmatore — copertura dei servizi entro 500 m, verde entro 300 m, pesi nel file di configurazione ([codice](https://github.com/tsinghua-fib-lab/DRL-urban-planning); [Zheng et al. 2023](https://www.nature.com/articles/s43588-023-00503-5)) [V codice; S paper]. Sony CSL propone un'accessibilità a 15 minuti con indice di Gini ([Bruno et al., arXiv 2408.03794](https://arxiv.org/abs/2408.03794)) [V preprint]. **In tutti questi lavori la ricompensa è la politica** [I, note 01 e 07].

### Matching: scegliere quale proprietà sacrificare

Nessun meccanismo soddisfa insieme stabilità, efficienza paretiana e strategy-proofness; per l'allocazione casuale nessuno è insieme ordinalmente efficiente, strategy-proof e simmetrico (Bogomolnaia–Moulin 2001) [L, forma da manuale; nota 02]. Roth (1982) mostra che nessun meccanismo stabile è strategy-proof per entrambi i lati ([PDF autore](https://stanford.edu/%7Ealroth/papers/1982_MOR_EconomicsOfMatching.pdf)) [V record]. La scelta per la tesi è quindi **dichiarare il sacrificio**: RSD/TTC (efficienza + non manipolabilità), DA (stabilità + non manipolabilità lato famiglie), PS (efficienza ordinale + assenza di invidia), Hylland–Zeckhauser (efficienza ex ante, ma il calcolo dell'equilibrio esatto è in FIXP e l'approssimato in PPAD) ([Vazirani–Yannakakis, arXiv 2004.01348](https://arxiv.org/pdf/2004.01348v5)) [V abstract].

Per la diversità il risultato è netto: **vincoli rigidi possono rendere impossibili assegnazioni eque e non sprecone, mentre i soft bounds preservano stabilità e incentivi** ([Ehlers, Hafalir, Yenmez, Yildirim, JET 2014](https://econpapers.repec.org/RePEc:eee:jetheo:v:153:y:2014:i:c:p:648-683)) [V abstract]; le quote massime per la maggioranza possono danneggiare le minoranze, che le riserve con DA Pareto-dominano ([Hafalir–Yenmez–Yildirim, TE 2013](https://econtheory.org/ojs/index.php/te/article/viewArticle/20130325)) [V abstract, dal report precedente]. I sistemi di riserve con ordine di elaborazione esplicito sono stati recepiti dalla Corte Suprema indiana ([Sönmez–Yenmez, Econometrica 2022](https://econometricsociety.org/publications/econometrica/2022/05/01/affirmative-action-india-vertical-horizontal-and-overlapping)) [V abstract] e usati per razionare risorse sanitarie ([Pathak et al., arXiv 2008.00374](https://arxiv.org/abs/2008.00374v1)) [V abstract]. **L'ordine delle categorie è esso stesso un peso nascosto** [I, nota 02]. Il caso abitativo più vicino è Singapore: le quote etniche per blocco HDB rendono il problema intrattabile in generale ([Benabbou et al., arXiv 1711.10241](https://arxiv.org/abs/1711.10241v6)) [V abstract].

Il punto più delicato per la tesi: **appena l'agente è un gruppo che chiede più alloggi complementari nello stesso lotto, la stabilità può non esistere** ([Kojima–Pathak–Roth, QJE 2013](https://dspace.mit.edu/handle/1721.1/96158)) [V record]. Le vie d'uscita sono tre: mercati grandi con pochi gruppi e liste corte (ibid.); perturbare le capacità — esiste sempre un matching stabile in un'istanza con capacità aggregata mai ridotta e aumentata al più di 4, e ogni sede variata al più di 2 ([Nguyen–Vohra, AER 2018](https://www.aeaweb.org/doi/10.1257/aer.20141188)) [V record]; oppure modellare i gruppi come domanda multidimensionale tipo zaino ([Delacrétaz–Kominers–Teytelboym, AER 2023](https://econpapers.repec.org/RePEc:aea:aecrev:v:113:y:2023:i:10:p:2689-2717)) [V abstract]. In edilizia la capacità di un lotto è flessibile (densità), quindi la perturbazione alla Nguyen–Vohra è più plausibile che negli ospedali [H, nota 02]. Sull'evidenza empirica: lotterie indipendenti per unità e liste con perdita del posto al rifiuto spingono ad accettare unità marginali, una lotteria comune migliora l'abbinamento ([Arnosti–Shi, Management Science 2020](https://econpapers.repec.org/RePEc:inm:ormnsc:v:66:y:2020:i:6:p:2291-2307)) [V record]; nel matching dei rifugiati gli algoritmi data-driven danno guadagni stimati del 40–50% in occupazione predetta, ma la massimizzazione pura genera squilibri ([Bansak–Paulson, Operations Research 2024](https://econpapers.repec.org/RePEc:inm:oropre:v:72:y:2024:i:6:p:2375-2390)) [V abstract]. Sono guadagni **controfattuali su esiti predetti**, non osservati [I].

### Scelta sociale: criteri riscrivibili come problema formale

Se i residenti propongono **vettori di pesi** che sommano a 1, il problema coincide con l'aggregazione di proposte di bilancio: la media è manipolabile, la regola utilitaria ℓ1 è strategyproof ma maggioritaria, i **moving phantom mechanisms** sono strategyproof e uno di essi (Independent Markets) è anche proporzionale ([Freeman et al., arXiv 1905.00457](https://arxiv.org/abs/1905.00457)) [V abstract]. Se invece votano **giudizi collegati** (criterio rilevante → soglia rispettata → lotto ammissibile) si cade nel paradosso dottrinale e nell'impossibilità di List–Pettit [L, nota 03]. Per scegliere quali criteri entrano nel catalogo, il **Method of Equal Shares** soddisfa EJR con costi arbitrari ([Peters–Pierczyński–Skowron, arXiv 2008.13276](https://arxiv.org/abs/2008.13276)) [V, Definizione 1 letta sul PDF]; ad Aarau (2023) ha finanziato 17 progetti su 33 contro 7 del greedy, sacrificando il terzo più popolare ([Pournaras et al., arXiv 2505.14349](https://arxiv.org/abs/2505.14349)) [S]. Per i panel sorteggiati, LEXIMIN rende le probabilità di selezione "il più uguali possibile" ed è stato usato in oltre 40 assemblee ([Flanigan et al., Nature 2021, PMC8387237](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8387237/)) [S], ma è manipolabile dichiarando falsi attributi, da cui l'obiettivo Goldilocks ([Baharav–Flanigan, arXiv 2406.15009](https://arxiv.org/html/2406.15009v2)) [V testo HTML]. Conitzer et al. mostrano che l'RLHF **aggrega già preferenze in modo implicito**, vicino al Borda, e chiedono di rendere esplicita la regola ([arXiv 2404.10271](https://arxiv.org/html/2404.10271v2)) [V §7.2]: è la critica del decisore nascosto formulata dall'informatica.

### Mediazione: il consenso dipende da iperparametri dello sviluppatore

Community Notes, Polis e la Habermas Machine fanno la stessa mossa: premiano ciò che piace **trasversalmente** a gruppi latenti stimati dai voti [I, nota 04]. Community Notes usa una fattorizzazione con regolarizzazione delle intercette cinque volte più forte di quella dei fattori ([Wojcik et al., arXiv 2210.15723](https://arxiv.org/pdf/2210.15723)) [V]. Polis vincola $K\in[2,\min(5,2+\lfloor n/12\rfloor)]$ e, per un "warm path", il clustering esportato non è riproducibile: il $K$ ricalcolato coincide con quello riportato in **70 conversazioni su 112** ([Gelauff 2026, arXiv 2608.28368](https://arxiv.org/abs/2608.28368)) [V]. La Habermas Machine aggrega con Schulze; con Borda vincerebbero spesso enunciati diversi ([Revel–Penigaud, arXiv 2503.05830](https://arxiv.org/pdf/2503.05830)) [S]. L'evidenza più forte riguarda la persuasione: con personalizzazione GPT-4 aumenta dell'**81,7%** le odds di accordo con l'avversario su 820 partecipanti ([Salvi et al., arXiv 2403.14380 v1](https://arxiv.org/abs/2403.14380)) [V abstract v1], e dove cresce la persuasività cala l'accuratezza ([Hackenburg et al., arXiv 2507.13919](https://arxiv.org/abs/2507.13919)) [S]. **Metriche operative per un decisore nascosto non sono standardizzate**: vanno costruite [S, nota 04].

### Preferenze: il ML non risolve l'identificazione

La specificazione di riferimento per la scelta residenziale è un logit a coefficienti eterogenei nello stile BFM/BLP con strumento per il prezzo ([Bayer–Ferreira–McMillan, NBER w13236](https://www.nber.org/papers/w13236)) [S]. Con i soli dati aggregati di Milano si identificano al più $\delta_j$ e poche interazioni; il reddito per NIL manca [I, nota 05]. In equilibrio con offerta fissa, un indice di "domanda" che non strumenta il prezzo **deve** essere quasi monotono nei canoni: l'indice del Lab correlato 0,987 con gli affitti è la tautologia dell'equilibrio, non un errore numerico [I, nota 05]. Gli agenti LLM riproducono medie, non relazioni per sottogruppo né varianze: Park et al. raggiungono l'83–86% della consistenza test–retest umana ma solo con interviste di due ore ([arXiv 2411.10109](https://arxiv.org/abs/2411.10109)) [V abstract]; le distribuzioni generate sono sistematicamente più strette ([arXiv 2507.02919](https://arxiv.org/pdf/2507.02919)) [S]; sulle WTP le stime vanno da allineate a sovrastime dell'86% ([Journal of Marketing Analytics 2026](https://link.springer.com/article/10.1057/s41270-026-00542-7)) [S]. **Nessuna validazione su scelte residenziali né su famiglie italiane** è stata trovata [L]. DML, foreste causali e conformal migliorano flessibilità e incertezza, non l'identificazione; l'IRL ha un problema di identificabilità formalizzato ([Cao–Cohen–Szpruch, NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/671f0311e2754fcdd37f70a8550379bc-Abstract.html)) [S].

### Economia: un lotto sotto mercato crea una rendita di allocazione

L'evidenza causale migliore è statunitense e di segno opposto secondo il quartiere: alloggi LIHTC nuovi alzano i prezzi vicini del **6,5%** entro 0,1 miglia nei quartieri poveri e li abbassano del **2,5%** in quelli ricchi ([Diamond–McQuade, JPE 2019](https://econpapers.repec.org/RePEc:ucp:jpolec:doi:10.1086/701354)) [S]; l'espansione del controllo dei canoni a San Francisco riduce l'offerta in affitto ([Diamond–McQuade–Qian, AER 2019](https://www.aeaweb.org/doi/10.1257/aer.20181289)) [S]; la fine del controllo a Cambridge genera forti spillover ([Autor–Palmer–Pathak, JPE 2014](https://econpapers.repec.org/RePEc:ucp:jpolec:doi:10.1086/675536)) [S]. Nessuno studio riguarda cooperative a proprietà indivisa o l'Europa [L]. Nei modelli di equilibrio spaziale un singolo lotto sotto mercato non sposta i prezzi della città ma **crea una rendita per chi entra**: le regole di assegnazione diventano la politica distributiva [I, nota 06]. Gli effetti di città richiedono scala (Vienna, Zurigo con l'obiettivo di un terzo) ([Stadt Zürich](https://www.stadt-zuerich.ch/de/planen-und-bauen/bauberatung-und-dienstleistungen/foerderprogramme/wohnbaufoerderung/anforderungen.html)) [S].

### Gruppi: due tipi sì, tre o più senza garanzie

Con **due** tipi di agenti esiste sempre una partizione individualmente stabile calcolabile in tempo polinomiale; Nash stabilità e core possono mancare; con tre o più tipi anche l'IS può non esistere e con $k\ge5$ deciderlo è NP-completo ([Bredereck–Elkind–Igarashi, arXiv 1903.00303](https://arxiv.org/abs/1903.00303)) [V abstract]. Una diversità a più attributi (età × condizione × reddito) cade nel regime senza garanzie [I]. Il fair clustering impone proporzioni per tipo in ogni cluster ([Bera et al., arXiv 1901.02393](https://arxiv.org/abs/1901.02393)) [V abstract]; il massimo Nash welfare dà EF1 ed è stato usato su Spliddit ([Caragiannis et al.](https://www.cs.toronto.edu/~nisarg/papers/mnw.pdf)) [S/V]. L'AI Economist mostra un RL a due livelli che migliora il trade-off equità–produttività e, insieme, agenti che sfruttano la ricompensa (*tax gaming*) ([arXiv 2108.02755](https://arxiv.org/abs/2108.02755)) [V abstract]. **Non esistono stime del prezzo della diversità su dati abitativi** [L, nota 07].

## Formulario per passo della pipeline

Convenzioni: $i$ famiglia, $g$ gruppo, $\ell$ lotto con capacità $q_\ell$, $\mu$ assegnazione. "Testo" = equazione vista sulla fonte; "standard" = forma da manuale scritta dai ricercatori, da riscontrare sull'originale prima di citarla.

### Lotti e accessibilità

**Uso locale e accesso (Abbiasov et al.)** — [arXiv 2211.14872](https://arxiv.org/abs/2211.14872); formula fedele alla definizione verbale [I]:
$$\mathrm{Usage}_j=\frac{\#\{\text{viaggi da }j\text{ verso POI}\in W_{15}(j)\}}{\#\{\text{viaggi da }j\}},\qquad \mathrm{Access}_j=\tfrac18\sum_{c=1}^{8}\mathrm{pct}_c\big(N_c(W_{15}(j))\big)$$
$W_{15}(j)$ walkshed di 15 minuti del block group $j$; $N_c$ numero di POI della categoria $c$; $\mathrm{pct}_c$ percentile tra tutti i block group.

**Segregazione sperimentata** — stessa fonte, Appendice 5.3 [V, testo]:
$$\mathrm{EI}_{k_i,L}=\frac{\sum_{k_j}p_{k_j,L}\,|r_i-r_j|}{\sum_{k_j}p_{k_j,L}},\qquad \mathrm{ES}_j=1-\frac{\sum_L \mathrm{EI}_{k_j,L}\,p_{j,L}}{\sum_L p_{j,L}}$$
$p_{k,L}$ visite del gruppo di reddito $k$ al luogo $L$; $r$ rango di reddito.

**Ricompensa "life circle" del DRL Tsinghua** — [codice](https://github.com/tsinghua-fib-lab/DRL-urban-planning) [V, codice]:
$$R_{life}=\frac{1}{|Res|}\sum_r\frac1S\sum_s\mathbb 1[d_{rs}\le 500\,\mathrm m]+0{,}05\,\frac{\bar d_{pair}}{D_{ref}}$$
$d_{rs}$ distanza dalla residenza $r$ al servizio più vicino di tipo $s$.

**Città a 15 minuti inclusiva (Sony CSL)** — [arXiv 2408.03794](https://arxiv.org/abs/2408.03794) [V, testo preprint]:
$$F_{15}=100\cdot\frac{\sum_{k:PT_k\le15}p_k}{\sum_k p_k},\qquad G=1-\frac{2\sum_{p}\sum_{p'\le p}PT_{p'}}{N_{pop}\sum_p PT_p}$$
$PT_k$ tempo medio di prossimità della cella $k$, $p_k$ popolazione.

**Modello di radiazione** — [Simini et al., arXiv 1111.0586](https://arxiv.org/abs/1111.0586) [V]: $\langle T_{ij}\rangle=T_i\,\frac{m_i n_j}{(m_i+s_{ij})(m_i+n_j+s_{ij})}$, con $s_{ij}$ popolazione nel cerchio di raggio $r_{ij}$. Serve a scala regionale, non per scegliere un lotto.

### Domanda e preferenze

**Scelta residenziale CityScope** — [arXiv 2106.14572](https://arxiv.org/abs/2106.14572); formalizzazione fedele al testo [I]:
$$U^{house}_{g,h}=w^p_g\,\mathrm{rent}_h+w^{div}_g\,H_h+w^{zone}_g\,\mathbb 1[h\in Z_g]+\max_m U^{mob}_{g,m}(h),\qquad H_h=-\sum_k p_{k,h}\ln p_{k,h}$$
$g$ fascia di reddito, pesi sintetici; trasloco se $U(h')>U(h_i^t)$ con $h'$ estratta a caso.

**Logit di sorting BFM/BLP** — [standard, L]; [BFM, NBER w13236](https://www.nber.org/papers/w13236):
$$V^i_h=\delta_h+\lambda^i_h+\varepsilon^i_h,\quad \delta_h=\alpha_{0X}X_h-\alpha_{0p}p_h+\xi_h,\quad \delta^{t+1}_h=\delta^t_h+\ln S^{obs}_h-\ln\hat S_h(\delta^t)$$
$\lambda^i_h$ interazioni caratteristiche familiari × attributi; $\xi_h$ qualità non osservata; il prezzo $p_h$ è endogeno e va strumentato.

**Mixed logit e WTP** — [standard, L]:
$$P_{ni}=\int\frac{e^{\beta'x_{ni}}}{\sum_j e^{\beta'x_{nj}}}f(\beta\mid\theta)\,d\beta,\qquad WTP_k=-\frac{\beta_k}{\beta_p}$$

**Preferenze via processo gaussiano (elicitazione attiva)** — [standard, L]: $p(v\succ u\mid f)=\Phi\!\big(\tfrac{f(v)-f(u)}{\sqrt2\,\sigma}\big)$; utile per poche domande ai partecipanti.

### Gruppi

**Fair clustering (Bera et al.)** — [standard, L; arXiv 1901.02393](https://arxiv.org/abs/1901.02393): per ogni cluster $C$ e tipo $t$, $\beta_t\le\frac{|C\cap P_t|}{|C|}\le\alpha_t$.

**Prezzo della diversità, deviazione IS, diversità di Simpson** — proposte operative della nota 08 [H], costruite su definizioni standard:
$$PoD(\beta)=\frac{\mathrm{cost}(\pi^*_\beta)}{\mathrm{cost}(\pi^*)},\qquad \mathrm{IS\text{-}dev}(\pi)=\frac1N\sum_i\mathbb 1\big[\exists h:\ h\cup\{i\}\succ_i\pi(i)\wedge\forall j\in h:\ h\cup\{i\}\succeq_j h\big],\qquad D_g=1-\sum_t p_{g,t}^2$$

**Nash welfare** — [Caragiannis et al.](https://www.cs.toronto.edu/~nisarg/papers/mnw.pdf) [S]: $\mathrm{NW}(A)=\prod_i v_i(A_i)$; il massimo dà EF1 con beni indivisibili.

### Matching

**Matching e invidia giustificata** — [standard, L]: $\mu:N\to L\cup\{\varnothing\}$ con $|\mu^{-1}(\ell)|\le q_\ell$; $\mu$ è stabile se non esiste $(i,\ell)$ con $\ell\succ_i\mu(i)$ e $i\triangleright_\ell j$ per qualche $j\in\mu^{-1}(\ell)$ (o posto libero).

**Probabilistic Serial** — [standard, L]: $P_{i\ell}=\int_0^1\mathbf 1[\ell=\mathrm{top}_i(L_t)]\,dt$.

**Soft bounds** — [standard, L; Ehlers et al. 2014](https://econpapers.repec.org/RePEc:eee:jetheo:v:153:y:2014:i:c:p:648-683): limiti $\underline q^t_\ell\le\overline q^t_\ell$; il tipo $t$ ha precedenza assoluta finché $|\mu^{-1}(\ell)\cap N^t|<\underline q^t_\ell$, la perde (senza esclusione) quando $\ge\overline q^t_\ell$.

**Riserve** — [standard, L]: $q_\ell=\sum_{c\in C}r^c_\ell$, ogni categoria con priorità $\triangleright^c_\ell$ e un **ordine di elaborazione** dichiarato.

**Domanda multidimensionale dei gruppi** — [standard, L; Delacrétaz et al.](https://econpapers.repec.org/RePEc:aea:aecrev:v:113:y:2023:i:10:p:2689-2717): $G_\ell$ ammissibile se $\sum_{g\in G_\ell}d_g\le c_\ell$ componente per componente.

**Prezzo della diversità con quote per blocco** — [standard, L; Benabbou et al.](https://arxiv.org/abs/1711.10241v6): $\mathrm{PoD}=\frac{\max_\mu\sum_i u_i(\mu)}{\max_{\mu\in\mathcal F_{div}}\sum_i u_i(\mu)}$, $\mathcal F_{div}=\{\mu:|\mu^{-1}(b)\cap N^t|\le\lambda_t|b|\}$.

### Aggregazione dei criteri

**Moving phantoms** — [standard, L; Freeman et al.](https://arxiv.org/abs/1905.00457): $a_j(t)=\mathrm{med}\big(f_0(t),\dots,f_n(t),p_{1,j},\dots,p_{n,j}\big)$, con $t^*$ tale che $\sum_j a_j(t^*)=1$.

**Method of Equal Shares** — [Peters et al., Def. 1](https://arxiv.org/abs/2008.13276) [V, testo]: ogni votante parte con $b/n$; $c$ è $\rho$-affordable se
$$\sum_{i\in N}\min\big(b_i,\;u_i(c)\cdot\rho\big)=\mathrm{cost}(c)$$
e si sceglie il $c$ con $\rho$ minimo.

**Sortition Goldilocks** — [Baharav–Flanigan](https://arxiv.org/html/2406.15009v2) [V, testo]: $\mathrm{Goldilocks}_\gamma(\pi)=\frac{\max(\pi)}{k/n}+\gamma\frac{k/n}{\min(\pi)}$.

### Mediazione e deliberazione

**Community Notes** — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V, verbatim]:
$$\hat r_{un}=\mu+i_u+i_n+f_u\cdot f_n,\qquad \min\sum(r_{un}-\hat r_{un})^2+\lambda_i(i_u^2+i_n^2+\mu^2)+\lambda_f(\|f_u\|^2+\|f_n\|^2)$$
con $\lambda_i=0{,}15$, $\lambda_f=0{,}03$; $i_n$ è la "helpfulness" non spiegata dal punto di vista.

**Polis: consenso informato dai gruppi e priorità** — [Gelauff, arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V, dal codice]:
$$GAC(s)=\prod_{g\in G}\frac{A_{g,s}+1}{S_{g,s}+2},\qquad \text{priority}=\big[(1-p)(E+1)\,a\,(1+8\cdot2^{-S/5})\big]^2$$
Il prodotto dà a ogni gruppo un potere di veto.

**Habermas Machine** — [standard, non citata; S]: reward model Bradley–Terry $P(x_j\succ x_k\mid u)=\sigma(R_u(x_j)-R_u(x_k))$, poi Schulze.

### Economia del lotto

Tutte [standard, L] dalla nota 06, da riscontrare:
$$VRA=GDV-C_{hard}-C_{soft}-O_{urb}-C_{CC}-F-\pi B,\qquad R_t=i^{ref}_t(L+K)+q_{op}V^{ass}+\delta K+Z_{BR}$$
$$RTI=\frac{R+S}{Y^{disp}},\qquad RI=Y^{disp}-(R+S)-B^{nh}(n),\qquad \Delta_L=VRA^{dev}-L^*_{coop}$$
$GDV$ ricavo lordo, $O_{urb}$ oneri (Delibera CC Milano 28/2023), $C_{CC}$ contributo sul costo di costruzione, $\pi$ margine, $L$ terreno riconosciuto, $K$ costo dell'edificio, $q_{op}$ quota d'esercizio (Zurigo 3,25% [S]), $Z_{BR}$ canone del diritto di superficie, $B^{nh}(n)$ paniere non abitativo, $L^*_{coop}$ prezzo del terreno di pareggio della cooperativa al canone obiettivo. CLT, rivendita indicizzata: $P_t=P_0\,I_t/I_0$.

### Audit del decisore nascosto

Proposte delle note 08–09 [H], nessuna è uno standard:
$$H=\frac{\mathrm{Var}(E[Y\mid\Theta_D])}{\mathrm{Var}(Y)},\qquad H^T=1-\frac{\mathrm{Var}(E[Y\mid\Theta_P])}{\mathrm{Var}(Y)}$$
$$\Delta_A=\mathbb E[d(o^A,R(p^0))]-\mathbb E[d(o^H,R(p^0))],\qquad \alpha_a=\frac1N\sum_i\frac{\langle p^1_i-p^0_i,\,m-p^0_i\rangle}{\|m-p^0_i\|^2}$$
$$\beta_M=\Pr_{\theta'\sim\Theta}[o(\theta')\ne o(\theta)]\ \text{vs}\ \max_i\beta_i,\qquad E_{agenda}=\frac1N\sum_i\mathbf 1\Big[\max_{\ell\in F\setminus S}u_i(\ell)>u_i(o_i)\Big]$$
$$c_g=\frac{s_g}{n_g/N},\qquad \rho_s=\frac{n_s/n}{N_s/N_{pop}},\qquad K_{dev}=\mathrm{corr}(\mathbf 1[\ell\text{ scelto}],V^{dev}_\ell)-\mathrm{corr}(\mathbf 1[\ell\text{ scelto}],V^{coop}_\ell)$$
$\Theta_D$ parametri del progettista, $\Theta_P$ input dei partecipanti; $o^A,o^H$ esiti con mediatore IA o umano; $R(p^0)$ esito della regola dichiarata sulle preferenze iniziali; $m$ posizione del mediatore; $F$ lotti fattibili per legge, $S$ lotti mostrati.

## Due difetti fatali, nove gravi: la tesi misura ciò che assume

Le tre revisioni convergono: le intuizioni di impianto sono giuste (linea di base obbligatoria, LLM non come evidenza, criteri pubblici), ma le promesse centrali sono oggi verificabili solo in forma tautologica [I, nota 08].

| # | Difetto (nota) | Gravità | Correzione |
|---|---|---|---|
| 1 | "Cooperativa più accessibile del developer" è vero per costruzione: il divario dipende da costo del terreno e margine scelti dal ricercatore (08-D1) | fatale | Ipotesi sul prezzo del terreno di pareggio $L^*$ e su $\Delta_L$; motore tarato su casi reali; metrica di targeting accanto al guadagno |
| 2 | Circolarità della fase ad agenti; LLM con collasso della varianza (08-D2, 09-D12) | fatale se non disegnata | Generatore, meccanismo, valutatore separati; quattro generatori; LLM solo stress-test; una prova umana piccola e precoce |
| 3 | Metrica di successo = funzione obiettivo, Goodhart (08-D3) | grave | Almeno una metrica non ottimizzata: rango held-out, IS su compatibilità non usate, RTI dal paniere ISTAT |
| 4 | Domanda non identificata: indice ≈ affitti (08-D4; 10) | grave | Rinunciare alla stima strutturale; preferenze dichiarate in F2; test anti-artefatto pre-registrati |
| 5 | Caso unico, unità di inferenza non definita (08-D5) | grave | Distinguere affermazioni di meccanismo (unità = istanza) da empiriche (F2) |
| 6 | Troppi parametri del progettista (08-D6) | grave | Pre-registrazione, analisi multiverso, scomposizione di Sobol |
| 7 | Diversità rinviata ma decisiva per l'esistenza di soluzioni (08-D7, 09-D10) | grave | Ora: un vincolo binario duro ($k=2$), il resto soft; diversità come parametro votato con il suo prezzo visibile |
| 8 | Preferenze di gruppo sui lotti non definite (08-D8) | grave | Regola di aggregazione interna pubblica; confronto due stadi contro congiunto; perturbazione di capacità |
| 9 | Nesso mediazione IA → esito non isolabile (08-D9) | grave | Disegno fattoriale ad ablazione: tenure × allocazione × mediazione |
| 10 | F2 sottodimensionata, comitato etico assente (08-D10) | grave | Un solo contrasto entro soggetto; calcolo di potenza; comitato etico avviato in F0–F1 |
| 11 | Il decisore nascosto non ha un test (08-D11, 09 §0) | serio | Metriche H7–H8 e M1–M9 con soglie pre-registrate |
| 12 | Potere di agenda fuori dal riscrivibile: lotti candidati, filtri, definizione di "pancia" (09-D1, D9) | grave | Ogni filtro diventa criterio nel registro; misurare $E_{agenda}$; vincoli legali separati da scelte di progetto |
| 13 | Le impossibilità risalgono al meta-livello: chi cambia la regola (09-D2) | grave | Costituzione minima con emendamento esterno |
| 14 | Mediatore LLM persuasivo senza controllo; RL che deriva (09-D3, D4) | grave | Tre bracci (IA/umano/nessuno); ricompensa pubblica e versionata; ratifica attiva con controfattuale e placebo |
| 15 | Tokenismo: nessun ente si impegna prima (09-D5) | grave | Partner come variabile del disegno; senza atto vincolante la prova è dichiarata consultiva |
| 16 | Auto-selezione digitale; appropriazione da capitale e piattaforme (09-D6, D7) | grave | Panel sorteggiato + canale assistito; mappe di domanda pubblicate in differita; governance agganciata al regime del suolo |
| 17 | Classificazione giuridica (AI Act, GDPR, L. 132/2025) e responsabilità diffusa (09-D8, D11) | serio | Matrice architettura × norma validata da un giurista; titolare nominato per ogni decisione |
| 18 | Tre dati mancanti: proprietà dei suoli, reddito sotto il CAP, costi reali (10) | grave per F1 | Proprietà e regime del suolo come scenario; richiesta formale al Comune in F0; 1–3 lotti pubblici reali |

Il confine giuridico merita attenzione perché può diventare un risultato. Il Service Desk della Commissione indica come *in scope* dell'Allegato III, punto 5(a), un sistema che attribuisce punteggi ai richiedenti di alloggi sociali, e come *fuori ambito* uno strumento che abbina persone ai servizi senza valutare domande ([AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/essential-services)) [S]. **Il confine passa tra "abbinare chi ha scelto" e "dire chi ha titolo o priorità"** [I, nota 09]: un mediatore che filtra le famiglie per la "pancia" per conto di un ente scivola dentro.

## Otto ipotesi falsificabili e una costituzione non riscrivibile

### Ipotesi operative H1–H8

Ipotesi primaria unica: **H2**; le altre secondarie con correzione di Holm. Le soglie sono **segnaposto da fissare ex ante da Dennis** [H], non valori di letteratura (nota 08 §2).

| H | Enunciato | Metrica | Baseline | Soglia [H] | Falsificazione |
|---|---|---|---|---|---|
| H1 | Esiste un regime fondiario in cui il canone obiettivo è sostenibile | $\Delta_{L,\ell}$; quota $S(\theta)$ di lotti con $RTI\le0{,}30$ e $RI\ge0$ per il 3° quintile | stesso motore, regime developer a prezzi OMI | $S\ge$ [0,25] con diritto di superficie, stabile nel ≥[80%] della griglia | $S<$ soglia, o motore fuori di [±20%] sui casi di taratura |
| H2 (primaria) | La scelta conta: DA con riserve batte l'allocazione dall'alto | rango medio held-out $\bar r(\mu)$, $T_3$, invidia giustificata $J$ | MILP del Lab (M0a), RSD (M0b) | $\Delta>0$, $d\ge$ [0,2], $J(\mu_{M1})=0$ | $\Delta\le0$ o $d<$ soglia all'IC 95% |
| H3 | Le riserve proteggono la minoranza meglio delle quote rigide | $W_m$ quota di minoranza peggio sotto quote | DA senza vincoli | $W_m>$ [0,10]; minoranza peggio sotto riserve ≤[5%] | $W_m\le$ soglia |
| H4 | Gruppi diversi restano stabili a costo contenuto | $PoD$, IS-dev, Simpson $\bar D_g$ | clustering per somiglianza (Housing Prime), casuale | $k=2$: IS-dev $=0$; morbido: IS-dev ≤[0,10], $PoD\le$[1,15], $\bar D_g$ +[0,2] | IS-dev sopra soglia con omofilia moderata |
| H5 | Regola proporzionale non manipolabile contro media dei pesi | $\mathrm{Gain}_i$, violazioni JR, gap di quota | media aritmetica (Lab) | media manipolabile per ≥[50%] degli strategici; gap ≤[0,05] | nessuna differenza tra regole |
| H6 | La domanda non è un artefatto dei canoni | $\rho_S(D_{\cdot,t},p)$, Kendall $W$ tra tipi | indice del Lab ($\rho=0{,}987$) | $|\rho_S|<$[0,8], $W<$[0,7] | $|\rho_S|\ge0{,}8$ o $W\ge0{,}7$ |
| H7 | Chi progetta non decide più di chi partecipa | Sobol $H$, $H^T$ per blocco | Lab con pesi medi e filtro fisso | $H^T\le$[0,3]; ogni parametro con indice >[0,05] pubblicato e votabile | $H^T>$ soglia |
| H8 | Il mediatore LLM non persuade né cancella minoranze | Drift, MinRep | regola fissa pubblica; mediatore umano | MinRep ≥[0,8]; Drift ≤ baseline + [0,1 SD] | Drift maggiore senza aumento di informazione |

Per la potenza: un confronto appaiato in simulazione richiede $R\approx7{,}85/d^2$ repliche per cella, quindi ~197 per $d=0{,}2$; in F2 un contrasto entro soggetto con $d=0{,}3$ richiede circa 87 persone, un confronto tra soggetti circa 175 per braccio [I, calcolo nota 08]. **F2 regge un solo contrasto primario**. Il protocollo per la fase ad agenti usa quattro generatori — G1 strutturale (IPF dal censimento + mixed logit), G2 avversario (omofilia forte, minoranza polarizzata, risposte strategiche), G3 di recupero (parametri veri noti), G4 LLM solo per collaudo — e accetta un risultato solo se regge su G1 **e** G2 [I, nota 08 §3]. Gli agenti LLM si validano a livello di parametri, non di risposte, con un test di equivalenza TOST sui coefficienti stimati da uno stesso esperimento di scelta [H].

### La costituzione minima

Principio guida della nota 09: **il mediatore non può mai scrivere, né proporre in silenzio, una regola del livello in cui opera** [I]. Tre livelli:

| Livello | Contenuto | Chi modifica | Mai modificabile da |
|---|---|---|---|
| 0. Carta | diritti (uscita, accesso ai dati, ricorso, spiegazione); il mediatore non decide; ratifica umana attiva; voto sui pesi a 100 punti; insieme ammesso di regole con assiomi garantiti; vincoli legali con fonte; registro obbligatorio; metriche M1–M9 con soglie di blocco | solo fuori dal processo: ente garante + assemblea sorteggiata, maggioranza qualificata, raffreddamento, effetto dal ciclo successivo | mediatore, progettista da solo, partecipanti dentro il ciclo |
| 1. Regole | catalogo dei criteri; filtri non legali; soglie di diversità; scelta della regola nell'insieme ammesso; ricompensa dell'RL; soglia della "pancia" se non fissata dall'ente | assemblea con panel sorteggiato; garanzia proporzionale alle minoranze coese (Independent Markets) | mediatore (può solo segnalare incoerenze) |
| 2. Preferenze | pesi individuali, scelte di lotti e di gruppo | ogni partecipante per sé; testi suggeriti dall'LLM marcati e approvati | nessun altro |

Il regresso ("chi decide le regole del livello 0?") si ferma per **convenzione dichiarata**: il livello 0 è legittimato da un atto esterno (ente, statuto della cooperativa, approvazione etica) e va sottoposto a critica esplicita [I]. La traccia di audit comprende un registro append-only con hash concatenati (un repository git firmato basta), una model card del mediatore a ogni ciclo con gli iperparametri "politici", la riproducibilità come requisito ($\mathrm{Rep}=1$) e un revisore indipendente [H]. Polis mostra perché serve: oggi spesso non si ricalcola l'esito dai voti ([Gelauff 2026](https://arxiv.org/abs/2608.28368)) [V].

## La prima parte si scrive su proprietà dei meccanismi, non su stime della domanda

### MVP F1 (gen–apr 2027, ~310 ore)

Il collo di bottiglia non è il calcolo — tutto il nucleo F1 gira in minuti su un portatile con `numpy`, `geopandas`, `highspy`/`ortools`, `scikit-learn` — ma tre dati mancanti [I, nota 10]. Gli oggetti computazionalmente difficili (stabilità garantita con gruppi, equilibrio HZ, core) vanno **evitati per scelta di metodo**: sono anche i meno spiegabili [I].

| # | Passo | Prodotto verificabile | Ore [I] |
|---|---|---|---|
| 0 | Riproducibilità: ambiente bloccato, manifest dei dati con licenza e hash, un comando che rigenera tutto | script unico da zero | 15 |
| 1 | Acquisizione dati v1 (NIL, sezioni 2021, IRPEF per CAP, OMI, particelle GML, PGT 2030, DUSAF, OSM) | matrice dati con licenze verificate | 30 |
| 2 | Lotti: filtro del Lab (~2.291 siti), vincoli ambientali, indici reali del PGT al posto del FAR 1,0, tre classi di proprietà | verifica a campione di 30–50 siti con tasso d'errore | 40 |
| 3 | Famiglie sintetiche (IPF) e "pancia" per tipo di famiglia a scala di città | 3 scenari; sensibilità al paniere 1,0/1,25/1,5 | 35 |
| 4 | Motore economico: VRA contro cost-rent, tre regimi del suolo, oneri ufficiali, taratura su 1–2 casi milanesi | canone di pareggio, RTI, $\Delta_L$; tornado su 8 parametri | 45 |
| 5 | Gruppi: k-means per somiglianza contro fair clustering con un vincolo binario + controllo IS | curve PoD, IS-dev, diversità | 40 |
| 6 | Abbinamento: casuale, RSD di gruppo, DA con soft bounds, MILP del Lab | rango, invidia, coppie bloccanti, RTI, famiglie servite | 40 |
| 7 | Esperimenti pre-registrati, ≥20 semi, IC, sensibilità | tabella risultati e registro deviazioni | 25 |
| 8 | Scrittura: capitolo "Dati e lotti" + bozza paper 1 | testo | 40 |

Se in ritardo si toglie, in quest'ordine: agenti LLM, DA con soft bounds, Sobol (resta il tornado), vincoli ambientali di dettaglio, seconda taratura, metà della verifica a campione. **Mai togliere** riproducibilità, linee di base, sensibilità al paniere, verifica dei lotti: la loro assenza ha invalidato metà dei risultati del Lab [V, riesame citato nella nota 10]. MES, sorting logit, audit del PGT e matching dinamico vanno rinviati a F2 o oltre.

### Indice proposto della prima parte

| Capitolo | Contenuto | Che cosa gli serve |
|---|---|---|
| 1 Introduzione | problema, domanda nelle due metà, "il metodo è il contributo", ipotesi con soglie, convenzioni | domanda e ipotesi fissate in F0; una pagina su ciò che la tesi **non** fa (non stima la domanda per quartiere, non valuta il PGT, non sostituisce la decisione politica) |
| 2 Abitare a Milano: chi è la "pancia" | mercato e Piano Casa (ERSC ≤80 €/m²/anno [S]); accessibilità (RTI, overburden, reddito residuo); dati e limiti; la lezione del Lab: perché con reddito a CAP la domanda è una mappa degli affitti | dati del passo 1; atti del Piano Casa letti in originale; definizione operativa della "pancia" con sensibilità al paniere |
| 3 Cibernetica, partecipazione, mediazione | Pask, Beer/Cybersyn, Friedman, Morel; partecipazione e potere; requisiti del mediatore trasparente | letture F0 ancora aperte, solo da schede complete; Arnstein, Ostrom, Medina in originale; elenco di requisiti verificabili |
| 4 Strumenti formali (stato dell'arte critico) | matching, gruppi, scelta sociale, preferenze, economia del lotto; tabella proprietà garantite/sacrificate/spiegabilità/calcolabilità | verifica sul testo di ogni voce [L] di questo report |
| 5 Metodo | pipeline, linee di base e metriche per passo, pre-registrazione, costituzione minima, riproducibilità | ipotesi datate prima degli esperimenti; matrice architettura × norma |
| 6 Il caso Milano (risultati F1) | lotti, economia per lotto ($\Delta_L$), curve diversità/stabilità, abbinamento scelta contro dall'alto, che cosa i risultati dimostrano e che cosa no | MVP completato |

**Primo capitolo da scrivere: il 2, entro fine febbraio 2027** [I, nota 10]. Dipende solo dai dati del passo 1 e dal riesame del Lab, produce un risultato metodologico che sopravvive a qualunque esito successivo. Il 4 si scrive a pezzi mentre si verificano le voci [L]; il 3 dipende dalle letture F0.

## Conflitti nei dati da tenere aperti

Il report precedente lasciava aperta la discrepanza su **Finding Places**: la nota 01 la chiude sul testo integrale — 24.000 è la capacità proposta dai 161 siti, 20.000 l'obiettivo, e i 6 siti raccomandati valgono ~750 posti, ~4% dell'obiettivo ([arXiv 1811.10123](https://arxiv.org/abs/1811.10123)) [V]. Restano aperti: **Park et al.**, che il report precedente cita all'85% mentre l'abstract dà 83%/82%/86% secondo il tipo di agente (intervista, survey, entrambi) ([arXiv 2411.10109](https://arxiv.org/abs/2411.10109)) [V abstract], quindi l'85% va sostituito dalla cifra per condizione; **Abbiasov et al.**, 12,1% di viaggi entro 15 minuti nel preprint contro 14% nella versione Nature Human Behaviour citata prima ([arXiv 2211.14872](https://arxiv.org/abs/2211.14872)) [V preprint; L versione pubblicata] — citare la versione pubblicata; **Salvi et al.**, 81,7% su 820 partecipanti nell'arXiv v1 contro 64,4% su 900 nel report precedente, probabilmente dalla versione Nature ([arXiv 2403.14380](https://arxiv.org/abs/2403.14380)) [V v1; L Nature]; **Aarau/MES**, +27,8% contro 22,6% di votanti rappresentati tra versioni dello stesso preprint ([arXiv 2505.14349](https://arxiv.org/html/2505.14349)) [S]; **AI Act Digital Omnibus**: più studi legali concordano che il Reg. (UE) 2026/1744 sia stato pubblicato in GU il 24/07/2026 e sposti gli obblighi dell'Allegato III al 2/12/2027 ([Mondaq](https://www.mondaq.com/uk/new-technology/1825722/eu-digital-omnibus-on-ai-enters-into-force); [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines/)) [S, GU non letta] — aggiorna l'avviso del report precedente, ma va chiuso solo su EUR-Lex. Sulle WTP degli LLM il conflitto è sostanziale, non di versione: Brand et al. le trovano "strettamente allineate" ([sintesi, arXiv 2503.10652](https://arxiv.org/pdf/2503.10652)) [S], altri trovano sovrastime fino all'86% [S].

## Opportunità di contributo originale e verifiche prioritarie

Le due commissioni ordinano le opportunità in modo diverso; incrociandole con la fattibilità della nota 10, l'ordine che regge è il seguente [I]. **Primo**, la misura operativa del decisore nascosto: scomposizione di Sobol progettista contro partecipanti ($H^T$) più le metriche M1–M4 con disegno a tre bracci, applicata a una decisione spaziale con esiti materiali; la nota 04 non trova metriche standard né studi di mediazione IA su allocazioni, ed è la parte già annunciata dalla seconda metà della domanda (sedi: FAccT, CSCW, *Environment and Planning B*) — ma va prima controllata la letteratura su algorithmic auditing e contestability by design [L]. **Secondo**, il matching gruppi–lotti con complementarità, riserve di diversità e densità flessibile come perturbazione alla Nguyen–Vohra: 1.000 istanze sintetiche (30–60 gruppi, 20–40 lotti) per misurare quanto spesso manca la stabilità e quanta capacità extra serve. **Terzo**, il prezzo della diversità su una popolazione abitativa sintetica realistica: tre curve (PoD, IS-dev, Simpson) al variare della soglia, un grafico, un paper breve. **Quarto**, la mappa del gap fondiario $\Delta_L$ per particella con motore tarato, utile anche fuori dall'accademia perché dice **dove il terreno, non la forma giuridica, blocca l'accessibilità**. **Quinto**, la costituzione a livelli e la matrice architettura × norma (richiede un giurista). **Sesto**, la validazione di agenti LLM su scelte residenziali a livello di parametri, pubblicabile anche con esito negativo ma dipendente da F2. La rilettura di Cybersyn come caso di governance è un contributo minore a basso costo.

Le verifiche, in ordine di priorità: (1) **richiesta formale al Comune** su patrimonio pubblico disponibile e aree ERSC, in F0, perché i tempi dell'ente non dipendono da Dennis; (2) variabili ISTAT per sezione 2021 (titolo di godimento, tipo di nucleo) e rapporto con l'edizione 2023; struttura e licenza dell'IRPEF sub-comunale MEF; (3) tabelle ufficiali degli oneri (Delibera CC 28/2023) e atti del Piano Casa (DGC 365/2026); (4) testi integrali di Bredereck–Elkind–Igarashi, Bera et al., Ehlers et al., Freeman et al. per le definizioni formali di IS, vincoli di proporzione, soft bounds e moving phantoms; (5) versioni pubblicate di Salvi (Nature Human Behaviour), Abbiasov (NHB), Habermas Machine (Science), Moro et al. (Nature Communications); (6) EUR-Lex per il Reg. (UE) 2026/1744 e il testo consolidato dell'Allegato III, Normattiva per L. 132/2025 art. 14; (7) Arnstein 1969, Ostrom 1990, Medina 2011, Sadowski 2021 in originale; (8) Diamond–McQuade e la regola zurighese del canone a costo (Mietzinsreglement) per tarare il motore; (9) autenticità e versioni dei pacchetti Python (`pabutools`, `pyblp`, `SALib`, `ipfn`, `r5py`) prima di installarli. Per sbloccare i punti 4–8 servono i domini editoriali nella lista consentita o i PDF dal PC.

## Conclusione

Il risultato più utile di questa ricerca non è un modello, ma uno spostamento: la tesi non deve dimostrare che la cooperativa batte il developer o che il sistema rispetta le esigenze — affermazioni che il suo stesso motore rende vere — ma **sotto quali condizioni** (di suolo, di diversità, di regola, di mediazione) un esito accessibile e scelto esiste, e **quanto pesa chi progetta** rispetto a chi partecipa. Riformulata così, la seconda metà della domanda smette di essere un controllo etico in coda e diventa il contributo misurabile più originale, perché la letteratura ha tutti gli ingredienti (Sobol, indici di potere, disegni a bracci) ma non li ha mai applicati a una decisione abitativa con esiti materiali.

Ne segue un'implicazione pratica che rovescia il calendario implicito: le decisioni che sembrano rinviabili — come operativizzare la diversità, quale regola aggrega i pesi, chi firma il livello 0, quale ente si impegna — sono proprio quelle che determinano se il problema ha soluzione e se la prova reale significa qualcosa. Vanno prese in F0, per iscritto e con data, prima che mesi di simulazione su agenti le fissino in silenzio: altrimenti il decisore nascosto sarà il disegno stesso della tesi.
