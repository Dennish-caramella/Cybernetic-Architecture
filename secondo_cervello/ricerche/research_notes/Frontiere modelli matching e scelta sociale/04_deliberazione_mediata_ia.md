# Deliberazione mediata da IA, consenso e piattaforme di intelligenza collettiva (stato a novembre 2026)

Note di ricerca per la seconda metà della domanda: *a quali condizioni il mediatore LLM resta trasparente e non diventa un decisore nascosto?* Estendono il §"mediazione IA" di `reports/Lotti ideali partecipazione e digital twin.md` (riga 37–39).

Marche: **[V]** verificato sul testo primario letto in questa sessione · **[S]** fonte secondaria o abstract/metadati · **[I]** inferenza mia · **[H]** ipotesi da testare · **[L]** lacuna (non verificato).
Le equazioni marcate "forma standard" sono forme da manuale, **non** citate dal paper.

Limite di sessione: la rete dell'ambiente blocca `science.org`, `nature.com`, `compdemocracy.org`, `communitynotes.x.com`, `rivista.ai`. Il paper Science della Habermas Machine, il paper Nature Human Behaviour di Salvi et al. e la documentazione ufficiale di Polis e di Community Notes **non sono stati letti in originale**. Ho usato preprint arXiv e analisi secondarie. Per verificare servono quei domini nella lista consentita, oppure i PDF dal PC.

---

## 1. Che cosa ottimizzano questi sistemi e come (equazioni)

### Takeaway
Tutti i sistemi fanno la stessa mossa: premiano ciò che piace *trasversalmente* a gruppi latenti stimati dai voti. Community Notes stima i gruppi con una fattorizzazione matriciale, Polis con PCA e k-means, la Habermas Machine con un reward model per persona seguito da un voto Schulze simulato. Il "consenso" quindi dipende da come il sistema definisce i gruppi e da parametri scelti dallo sviluppatore (regolarizzazione, soglie, K, metodo di voto). È qui che può nascere il decisore nascosto [I].

### Cited Findings

**Community Notes (ex Birdwatch), Wojcik et al. 2022, arXiv 2210.15723** [V: PDF arXiv letto]
- Autori: Stefan Wojcik, Sophie Hilgard, Nick Judd, Delia Mocanu, Stephen Ragain, M.B. Fallin Hunzaker, Keith Coleman, Jay Baxter — [arXiv 2210.15723](https://arxiv.org/abs/2210.15723) [V]
- Modello di predizione del voto (verbatim): $\hat r_{un} = \mu + i_u + i_n + f_u \cdot f_n$, dove $\mu$ è l'intercetta globale, $i_u$ l'indulgenza del valutatore, $i_n$ l'intercetta della nota ("helpfulness" non spiegata dal punto di vista) e $f_u, f_n$ i vettori latenti — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- Perdita (verbatim, minimizzata con discesa del gradiente): $\min_{i,f,\mu} \sum_{r_{un}} (r_{un}-\hat r_{un})^2 + \lambda_i (i_u^2 + i_n^2 + \mu^2) + \lambda_f (\lVert f_u\rVert^2 + \lVert f_n\rVert^2)$, con $\lambda_i = 0{,}15$ e $\lambda_f = 0{,}03$, cioè regolarizzazione sulle intercette 5 volte più forte. I fattori sono **monodimensionali** — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- Questo è il cuore del bridging: il modello spiega quanta più varianza possibile con i fattori di punto di vista, e solo dopo con le intercette. Per gli autori, una nota ottiene un'intercetta alta solo se la giudicano utile "raters with a diversity of factor vectors" — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- Soglie: la nota è "helpful" se $i_n \ge 0{,}40$, "not helpful" se $i_n \le -0{,}08$, altrimenti "needs more ratings" — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- Filtri di densità: note con almeno 5 voti, valutatori con almeno 10. Il secondo passaggio tiene solo i valutatori con *rater helpfulness* ≥ 66%. Gli autori di note devono avere un rapporto tra note "helpful" e "not helpful" di almeno 5:1 e un'intercetta media ≥ 0,05. I filtri eliminano circa metà di valutatori e voti. Dataset: 7.088 note, 124.241 voti, 3.261 valutatori; punteggi finali per 5.787 note — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- Scelta dichiarata: gli autori privilegiano la precisione sul richiamo per il rischio reputazionale — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]. Le regole di produzione attuali (vincolo su $|f_n|$, più fattori, versioni successive) **non** sono verificate: documentazione bloccata [L].

**Polis (Computational Democracy Project)**
- Pipeline. Ogni "tick" del motore applica le decisioni di moderazione (azzerando partecipanti ed enunciati colpiti) e calcola una PCA a 2 dimensioni con *power-iteration EM PCA* (Roweis 1998). Poi esegue k-means e "group k-means" per diversi K candidati. Una funzione di smussamento sceglie il K riportato, con *warm path*: ogni tick riparte dallo stato precedente — [Gelauff 2026, arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V: PDF letto]
- Vincolo dello sviluppatore: $K \in [2,\ \min(5,\ 2+\lfloor n/12 \rfloor)]$, applicato sia ai gruppi sia ai sottogruppi. Il sistema non può mai restituire *un solo* gruppo — [arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V]. Il K si sceglie con il coefficiente di silhouette — [compdemocracy.org](https://compdemocracy.org/clustering-algorithms/) [S: snippet di ricerca]
- Matrice dei voti: nel database "agree" vale −1 e "disagree" +1; nell'export il segno è invertito; "pass" vale 0 [I: lo zero per pass è implicito nel testo e va confermato sul codice]. Entra nei risultati solo chi ha almeno 7 voti, o ha votato il 100% degli enunciati — [arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V]
- Instradamento degli enunciati (dal codice `conversation.clj`). Con $A, D, P$ voti agree, disagree e pass, $S$ voti totali ed $E$ distanza dall'origine nella proiezione PCA: $p=\frac{P+1}{S+2}$, $a=\frac{A+1}{S+2}$, $\text{importance}=(1-p)(E+1)\,a$, $\text{priority}=\big[\text{importance}\cdot(1+8\cdot 2^{-S/5})\big]^2$ — [arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V]. A parità di 10 voti, un enunciato tutto-agree ha priorità **121×** rispetto a uno tutto-disagree; a 30 voti **961×**. La formula è asimmetrica e premia gli enunciati che separano i gruppi — [ibid.] [V]
- Bug documentato: tra marzo 2025 e luglio 2026 l'instradamento era di fatto uniforme. Il *warm path* rende inoltre il clustering esportato **non riproducibile** dai voti: il K ricalcolato senza warm path coincide con quello riportato in 70 conversazioni su 112 — [arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V]
- Consenso informato dai gruppi (*group-aware consensus*, GAC), nella forma usata da Anthropic: $GAC(s)=\prod_{g\in G} P(\text{agree}\mid g,s)$ — [Huang et al. 2024, arXiv 2406.07814](https://arxiv.org/html/2406.07814) [V/S: HTML arXiv letto tramite estrazione]. Nel codice Polis (`:group-aware-consensus`) la probabilità è stimata con un prior di Laplace e moltiplicata su tutti i gruppi: $GAC(s)=\prod_{g\in G}\frac{A_{g,s}+1}{S_{g,s}+2}$, dove $A$ conta gli agree e $S$ i voti espressi nel gruppo (commento nel codice: "+1 acts as a dumb prior") — [conversation.clj](https://github.com/compdemocracy/polis/blob/edge/math/src/polismath/math/conversation.clj) [V: sorgente letto il 10/11/2026, ramo `edge`]. Logica dichiarata da CDP: un 90% di accordo può nascondere una minoranza importante — [compdemocracy.org/Analysis](https://compdemocracy.org/Analysis/) [S]
- *Representativeness* ("repness") di un enunciato $s$ per il gruppo $g$, dal codice — [repness.clj](https://github.com/compdemocracy/polis/blob/edge/math/src/polismath/math/repness.clj); [stats.clj](https://github.com/compdemocracy/polis/blob/edge/math/src/polismath/math/stats.clj) [V: sorgente letto]:
  - $p_a=\frac{n_a+1}{n_s+2}$; rapporto di rappresentatività $r_a = p_a \big/ \frac{1+\sum_{h\ne g} n_{a,h}}{2+\sum_{h\ne g} n_{s,h}}$ (lo stesso vale per il disaccordo, $p_d$ e $r_d$);
  - test su una proporzione: $p_{at} = 2\sqrt{n_s+1}\,\big(\frac{n_a+1}{n_s+1}-0{,}5\big)$; per $r_{at}$ si usa un test a due proporzioni tra il gruppo e il resto;
  - si sceglie agree o disagree secondo quale ha la statistica di test maggiore, e si ordina per la metrica $\text{repness}\cdot\text{repness-test}\cdot p\cdot p_{test}$; serve significatività $z>1{,}2816$ (90%, una coda) su entrambi i test;
  - gli enunciati di consenso globale si ordinano per $p_a\cdot p_{at}$ con $p_a>0{,}5$.

**Habermas Machine (Google DeepMind), Tessler et al. 2024, *Science*, DOI 10.1126/science.adq2852**
- Procedura, ricostruita da Revel & Penigaud 2025 [S: analisi secondaria letta]:
  1. Ognuno scrive privatamente la propria opinione.
  2. Un LLM genera enunciati di consenso candidati.
  3. Un *personalized reward model* (PRM) predice per ogni persona un punteggio per ogni candidato, cioè una matrice delle opinioni *inferita* e non chiesta.
  4. I ranking si aggregano con il **metodo Schulze**; si ripete 4 volte e si ottengono 4 vincitori, che i partecipanti reali ordinano; Schulze sceglie il vincitore.
  5. Ognuno scrive una critica e il ciclo si ripete.
  
  Fonte: [Revel & Penigaud 2025, arXiv 2503.05830](https://arxiv.org/pdf/2503.05830)
- Schulze è scelto per l'indipendenza dai cloni (Tessler et al. 2024, SM p. 38, secondo [Revel & Penigaud](https://arxiv.org/pdf/2503.05830)) [S]. Con un altro metodo, per esempio Borda, vincerebbero spesso enunciati diversi — [snippet di ricerca su arXiv 2603.16751](https://arxiv.org/pdf/2603.16751) [S, da leggere]
- Reward model addestrato su ranking umani convertiti in preferenze a coppie con un modello Bradley-Terry — [snippet di ricerca](https://arxiv.org/pdf/2603.16751) [S]. Forma standard (non citata): $P(x_j \succ x_k \mid u) = \sigma\big(R_u(x_j)-R_u(x_k)\big)$ [forma standard].
- Metodo Schulze, forma standard (non citata). Sia $d[j,k]$ il numero di votanti che preferiscono $j$ a $k$. Si calcola $p[j,k]$, la forza del cammino più forte da $j$ a $k$ nel grafo dei duelli (larghezza = minimo degli archi lungo il cammino, massimizzata sui cammini). Vince $j$ se $p[j,k] \ge p[k,j]$ per ogni $k$ [forma standard].
- Gruppi di circa 5 persone. Il PRM personalizzato richiede una fase preliminare di raccolta dati e non scala — [Revel & Penigaud 2025](https://arxiv.org/pdf/2503.05830) [S]

**Collective Constitutional AI (Anthropic + CIP), Huang et al., FAccT 2024**
- Campione di 1.002 adulti USA (PureSpectrum), rappresentativo per età, genere, reddito e area. Su Polis: 1.127 enunciati e 38.252 voti; 275 enunciati dopo la moderazione. Polis trova 2 gruppi. Soglia effettiva di inclusione GAC = 0,723 (media 0,64, mediana 0,70). Circa 50% di sovrapposizione concettuale con la costituzione di Anthropic — [arXiv 2406.07814](https://arxiv.org/html/2406.07814) [V/S]
- Esiti: MMLU 72,3 contro 72,4; GSM8K 85,6 contro 85,2. Harmlessness Elo 0,0 ± 8,9 contro 22,0 ± 8,9 (lo Standard è più "harmless"). Bias BBQ più basso su tutte e 9 le dimensioni (valori solo in figura). OpinionQA: rappresentatività circa 2–3 punti più bassa — [arXiv 2406.07814](https://arxiv.org/html/2406.07814) [V/S]

**Talk to the City (AI Objectives Institute)**
- Strumento open source: un LLM estrae gli argomenti dagli input qualitativi e li raggruppa in cluster e sotto-cluster. La *process card* dice che i report vanno letti come "accurate but not precise" — [ai.objectives.institute (copia gwern)](https://gwern.net/doc/www/ai.objectives.institute/fa46182a810da5bfde418b21016574027d1dd94f.html) [S]. Algoritmo di clustering esatto (embedding? k-means? HDBSCAN?) non verificato [L].

### Inferences
- [I] In tutti i casi un "parametro politico" è nascosto in un iperparametro. In Community Notes è $\lambda_i/\lambda_f$ insieme alla soglia 0,40. In Polis sono il prodotto nel GAC, che dà a ogni gruppo un potere di veto, e il vincolo $K\ge2$, che impone almeno due gruppi. Nella Habermas Machine sono la scelta di Schulze e il PRM che *inferisce* le preferenze invece di chiederle. Per la tesi: criteri e pesi pubblici e riscrivibili (DOMANDA_DI_RICERCA) significa anche iperparametri di aggregazione pubblici e riscrivibili.
- [I] Il GAC come prodotto premia l'accettabilità minima su tutti i gruppi: è un criterio maximin "morbido". Se i gruppi sono stimati male (K forzato, warm path), il veto va ai gruppi sbagliati.
- [I] Per il problema "individui → gruppi → lotti", il bridging (intercetta oltre i fattori) è un candidato diretto per scegliere *criteri* condivisi da gruppi eterogenei. Polis-GAC si presta meglio a enunciati brevi. La Habermas Machine è utile per testi di sintesi, ma richiede dati per persona.

### Gaps
- Chiusa il 10/11: repness e GAC verificati sul sorgente GitHub (sopra). Resta da verificare la pagina di documentazione di compdemocracy.org (dominio bloccato) [L].
- [L] Regole di produzione attuali di Community Notes (più fattori, vincolo su $|f_n|$, scoring per gruppo): serve l'accesso a communitynotes.x.com.
- [L] Dettagli del PRM della Habermas Machine (modello base Chinchilla? numero di candidati per round?): il testo Science non è stato letto.

---

## 2. Evidenza causale (RCT, campioni, effetti) e rapporti di campo

### Takeaway
Gli RCT solidi esistono per Community Notes (survey sperimentale con N≈15.900 più A/B test in piattaforma), per la Habermas Machine (esperimenti con gruppi da 5, N complessivo dichiarato 5.734 ma letto solo da fonte secondaria) e per la persuasione LLM. Polis, vTaiwan, Meta Community Forums, CIP e OpenAI Democratic Inputs hanno soprattutto rapporti di campo, oppure confronti pre/post senza un controllo con mediatore umano.

### Cited Findings
- **Community Notes, survey sperimentale randomizzata.** Campione stratificato di utenti Twitter: Wave 2 (dicembre 2021) N=7.387; Wave 3 (aprile 2022) N=15.935 — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
  - Chi vede una nota scelta dall'algoritmo MF ha il 41% di probabilità in meno di essere d'accordo con il tweet fuorviante, contro il 22% in meno di media degli altri algoritmi testati. Chi è "strongly disagree" passa dal 29% al 44% (+52%) [V].
  - Circa l'80% degli utenti trova le note scelte utili o le apprezza, ed è il 70% o più in ciascun partito [V].
  - Il vantaggio percepito rispetto ai baseline è di circa +3 punti percentuali tra i Democratici e +10 tra i Repubblicani [V].
- **Community Notes, A/B test in piattaforma:** chi vede le annotazioni fa like o retweet il 25–34% in meno. Gli autori stimano un effetto sottostimato per diluizione del trattamento — [arXiv 2210.15723](https://arxiv.org/pdf/2210.15723) [V]
- **Habermas Machine, Science 2024.** Training su un campione di convenienza britannico (n=2.110) da piattaforma di crowdsourcing; replica su un campione demograficamente rappresentativo del Regno Unito; gruppi fino a 5 persone, round di circa 15 minuti — [Tessler et al. 2026, arXiv 2601.05904](https://arxiv.org/html/2601.05904v1) [S: gli stessi autori riassumono il proprio studio]
  - Gli enunciati della HM sono preferiti a quelli dei mediatori umani, giudicati meno imparziali. I gruppi risultano "less divided" dopo la deliberazione, senza numeri riportati in questa fonte. I round di critica aumentano l'approvazione anche controllando per tempo e sforzo [S].
  - Dopo il round di critica, la HM "tended to over-weight minority viewpoints". I partecipanti dicono di non aver quasi mai sentito pressione indebita [S].
  - Il "voto simulato" (reward model + aggregazione) è la componente più responsabile dell'approvazione [S].
  - N totale **5.734** e preferenza del **56%** sugli umani — [MIT Technology Review, citato nel report precedente](https://www.technologyreview.com/2024/10/17/1105810/ai-could-help-people-find-common-ground-during-deliberations/) [S; non riletto qui].
- **Tessler et al. 2026, "Can AI mediation improve democratic deliberation?"**, arXiv 2601.05904, gennaio 2026. Autori: Tessler, Evans, Bakker, Gabriel, Bridgers, Jain, Koster, Rieser, Dragan, Botvinick, Summerfield. È un pezzo di **prospettiva** (Knight Institute), **non** un nuovo RCT — [arXiv 2601.05904](https://arxiv.org/abs/2601.05904) [V: abstract]
- **Polis, confronto randomizzato:** Venkat (2024) mette a confronto, su un campione nazionale rappresentativo, il riassunto Polis con uno da scelta sociale computazionale e uno da argomentazione astratta. Il metodo di scelta sociale fa sentire i partecipanti meglio rappresentati — citato in [Gelauff 2026](https://arxiv.org/abs/2608.28368) [S: da leggere in originale]
- **Polis, analisi su larga scala:** 119 conversazioni con almeno 100 partecipanti (da 271). I partecipanti vedono meno della metà degli enunciati. Il 18,5% degli enunciati scritti dai partecipanti (1.289 su 6.980 valutabili) ha una posizione predetta *contraria* all'"agree" che Polis attribuisce d'ufficio all'autore — [arXiv 2608.28368](https://arxiv.org/abs/2608.28368) [V]
- **vTaiwan:** riduzione della polarizzazione in un workshop, con effetti variabili per enunciato. È uno studio di campo, non un RCT — [Yang & Bachmann, arXiv 2502.05017](https://arxiv.org/abs/2502.05017) [S, dal report precedente]
- **Meta Community Forum 2023 (Stanford Deliberative Democracy Lab + Meta + BIT):** Deliberative Polling sui principi dell'IA generativa, 1.545 partecipanti da Brasile, Germania, Spagna e USA, sondaggi pre e post — [FSI Stanford](https://fsi.stanford.edu/publication/meta-community-forum-results-analysis-april-2024) [S]
- **Stanford Online Deliberation Platform:** il moderatore automatico gestisce i turni con una coda visibile e interventi fino a 45 secondi; il gruppo vota per passare al punto successivo dell'agenda — [sintesi della ricerca su FSI](https://fsi.stanford.edu/node/36099) [S]. Non ho trovato un confronto controllato tra moderatore automatico e umano [L].
- **CIP Alignment Assemblies** (da febbraio 2023): Polis e una valutazione dei rischi su AllOurIdeas, con OpenAI come "committed audience" — [CIP blog](https://cip.org/blog/alignment-assemblies-nine-months-in) [S]. **OpenAI Democratic Inputs to AI** (maggio 2023), seguito da un team "Collective Alignment" — [OpenAI](https://openai.com/index/democratic-inputs-to-ai/) [S]. Esiti dei 10 grantee non letti [L].

### Inferences
- [I] Gerarchia dell'evidenza per la tesi:
  1. RCT con outcome comportamentale (Community Notes A/B) e RCT di laboratorio (Habermas Machine, persuasione);
  2. confronti randomizzati tra metodi di sintesi (Venkat 2024);
  3. pre/post senza controllo (Deliberative Polls, Meta);
  4. rapporti di campo (vTaiwan, CIP).
  
  Per il criterio "più aderenti alle esigenze" servono almeno i livelli 1–2.
- [I] Nessuno studio trovato misura gli esiti *materiali* di una decisione presa con mediazione IA (costi, allocazioni). Gli outcome sono atteggiamenti, approvazione e condivisione. La scala urbana (lotti) richiede outcome nuovi.

### Gaps
- [L] Effect size esatti della Habermas Machine (variazione di accordo, distanza tra gruppi, test statistici): il testo Science non è stato letto.
- [L] Risultati quantitativi del Meta Community Forum e di vTaiwan.
- [L] Seguiti empirici DeepMind 2025–2026 dopo Science 2024: trovata solo la prospettiva 2601.05904. Da cercare: deploy con assemblee reali.

---

## 3. Rischi: persuasione, sycophancy, omogeneizzazione, soppressione delle minoranze; metriche per un decisore nascosto

### Takeaway
L'evidenza più forte riguarda la persuasione: gli LLM persuadono almeno quanto gli umani, di più con la personalizzazione, e più persuadono meno sono accurati. Esiste evidenza preliminare che i riassunti LLM sotto-rappresentano le minoranze e dipendono dall'ordine dell'input. Paradossalmente, la Habermas Machine *sovra-pesa* le minoranze dopo la critica. Metriche operative per un "decisore nascosto" non sono standardizzate: vanno costruite.

### Cited Findings
- **Salvi et al. 2025** (autori verificati: Francesco Salvi, Manoel Horta Ribeiro, Riccardo Gallotti, Robert West), *Nature Human Behaviour*, DOI 10.1038/s41562-025-02194-6. RCT preregistrato con disegno fattoriale 2×2 (avversario umano o GPT-4, con o senza personalizzazione sociodemografica) in dibattiti a più turni. Con personalizzazione, GPT-4 dà l'**81,7%** di odds in più di aumento dell'accordo con l'avversario (p<0,01); senza, l'effetto non è significativo (p=0,31). Il dato riguarda **820** partecipanti — [arXiv 2403.14380 (versione v1)](https://arxiv.org/abs/2403.14380) [V: abstract arXiv v1]. Il **64,4%** e i **900** partecipanti del report precedente vengono probabilmente dalla versione pubblicata; una versione arXiv v3 non esiste (404, 10/11). **Discrepanza da risolvere sul testo Nature** [L].
- **Hackenburg et al. 2025**, "The levers of political persuasion with conversational AI", *Science* 390(6777), dicembre 2025. Tre esperimenti, N=76.977, 19 LLM, 707 temi, 466.769 affermazioni verificate. Post-training e prompting aumentano la persuasività fino a +51% e +27%. Dove cresce la persuasività, cala sistematicamente l'accuratezza fattuale — [arXiv 2507.13919](https://arxiv.org/abs/2507.13919); [OII Oxford](https://www.oii.ox.ac.uk/oxford-researchers-reveal-how-conversational-ai-can-change-political-opinions/) [S: snippet; preprint da leggere]
- **Costello, Pennycook & Rand 2024**, *Science*: dialoghi con GPT-4 Turbo riducono la credenza in una teoria del complotto di circa il 20% (N≈2.190), effetto stabile a 2 mesi — [MIT Sloan](https://mitsloan.mit.edu/node/48296) [S]. È la prova che la persuasione LLM è *durevole*: è un bene se corregge, un rischio se il mediatore orienta [I].
- **Minoranze nei riassunti:** un benchmark di 18 LLM su dati deliberativi su larga scala trova sotto-rappresentazione persistente delle posizioni minoritarie e bias legato all'ordine dell'input — [arXiv 2510.05154](https://arxiv.org/abs/2510.05154) [S: snippet]
- **Supporto alle minoranze:** esperimento con 96 persone in 24 gruppi. L'invio anonimo mediato dall'IA aumenta la discussione ma *riduce* sicurezza psicologica e soddisfazione dei membri di minoranza — [arXiv 2606.31762](https://arxiv.org/html/2606.31762) [S]. "Devil's advocate" LLM per le minoranze (IUI '25) — [arXiv 2502.06251](https://arxiv.org/html/2502.06251) [S]
- **Omogeneizzazione:** una sintesi sostiene che, se più utenti passano dallo stesso LLM, espressione e pensiero si standardizzano — [arXiv 2508.01491](https://arxiv.org/html/2508.01491v2) [S]
- **Rischi dichiarati dagli autori della Habermas Machine:** rappresentazione strategica (il sistema "assumes that individuals sincerely input their preferences"); dati di training omogenei; difficoltà di supervisione su grandi gruppi; "hallucinated opinions"; avversione algoritmica; privacy — [arXiv 2601.05904](https://arxiv.org/html/2601.05904v1) [S]. Nel lavoro originale manca fact-checking e l'obiettivo è massimizzare l'approvazione [S, report precedente].
- **Il decisore nascosto in Polis (sviluppatore e convener):** il convener decide gli enunciati iniziali, la politica di moderazione e gli invitati. Lo sviluppatore fissa K tra 2 e 5 e la priorità degli enunciati. Il clustering esportato non è riproducibile. Raccomandazione: rianalizzare i dati a processo chiuso e rendere esplicite le priorità di analisi — [Gelauff 2026](https://arxiv.org/abs/2608.28368) [V]
- **Critica di Revel & Penigaud:** la Habermas Machine *inferisce* la matrice delle volontà, mentre Polis la *chiede*. Le loro domande di ricerca: gli LLM sono più maggioritari o più proporzionali nelle sintesi? Propongono test con input costruiti con prospettive sbilanciate per misurare sovra- o sotto-rappresentazione della maggioranza — [arXiv 2503.05830](https://arxiv.org/pdf/2503.05830) [S]
- **Mitigazioni proposte da DeepMind:** analisi degli embedding per misurare quanto i candidati coprono le diverse prospettive; valutazioni per sottogruppo demografico; strumenti di visualizzazione per ispezionare e correggere le preferenze predette; domande di chiarimento quando il reward model è incerto; red teaming contro gli input insinceri — [arXiv 2601.05904](https://arxiv.org/html/2601.05904v1) [S]

### Inferences
- [H] Metriche candidate per rilevare un **decisore nascosto** nella tesi (costruite da me sulle fonti sopra, non standard):
  1. *Divergenza deriva/maggioranza:* spostamento medio pre→post delle opinioni verso la posizione maggioritaria iniziale, confrontato con un controllo umano. Un mediatore neutrale non dovrebbe aumentarlo.
  2. *Copertura delle minoranze:* quota di argomenti dei cluster minoritari presenti nella sintesi finale, normalizzata per la dimensione del cluster (proporzionalità).
  3. *Sensibilità all'iperparametro:* quanto cambia il vincitore cambiando metodo di aggregazione (Schulze, Borda, GAC), ordine dell'input, K o $\lambda$. Alta sensibilità = potere nascosto nel design.
  4. *Fedeltà del modello di preferenze:* accordo tra preferenze predette (PRM o LLM) e ranking dichiarati, per sottogruppo.
  5. *Omogeneizzazione:* diversità lessicale e semantica (dispersione degli embedding) delle posizioni individuali prima e dopo.
  6. *Riproducibilità:* l'esito si ricalcola dai dati pubblici? Polis mostra che oggi spesso no.
- [I] Il caso Habermas Machine, che sovra-pesa le minoranze dopo la critica, mostra che il rischio non è solo "maggioranza". Il mediatore può spostare il peso in *qualsiasi* direzione, e proprio questo lo rende un decisore. La metrica giusta è lo scarto da una regola dichiarata, non da una neutralità astratta.

### Gaps
- [L] Studi specifici su sycophancy del mediatore in deliberazione di gruppo: non trovati in questa sessione.
- [L] Risultati di "Empty Chair" (arXiv 2503.13812) e "Finding Common Ground in a Sea of Alternatives" (arXiv 2603.16751): visti solo i titoli.

---

## 4. Protocollo di valutazione adottabile dalla tesi

### Takeaway
Combinare tre disegni già validati in letteratura:
- il confronto randomizzato "mediatore IA contro mediatore umano" della Habermas Machine;
- il pre/post con controllo dei Deliberative Polls;
- il confronto tra metodi di sintesi (Venkat 2024).

A questi si aggiungono le metriche di minoranza e di sensibilità della §3. Gli iperparametri vanno preregistrati e pubblicati.

### Cited Findings
- Il disegno con mediatore umano come controllo e round di critica è stato usato dalla Habermas Machine — [arXiv 2601.05904](https://arxiv.org/html/2601.05904v1) [S]
- Il pre/post sulle opinioni è il metodo dei Deliberative Polls (Meta Forum, 1.545 partecipanti) — [FSI Stanford](https://fsi.stanford.edu/publication/meta-community-forum-results-analysis-april-2024) [S]
- Il confronto randomizzato tra sintesi Polis e sintesi da scelta sociale è in Venkat 2024 — citato in [Gelauff 2026](https://arxiv.org/abs/2608.28368) [S]
- La preregistrazione con disegno fattoriale è in Salvi et al. — [arXiv 2403.14380](https://arxiv.org/abs/2403.14380) [V]
- Raccomandazione di rianalisi e trasparenza delle priorità — [Gelauff 2026](https://arxiv.org/abs/2608.28368) [V]

### Inferences
- [H] Protocollo proposto, da discutere con Dennis e coerente con "prima agenti, poi test reale":
  1. **Fase agenti:** gruppi simulati con minoranze costruite ad arte, come suggeriscono Revel & Penigaud. Misurare metriche 2, 3, 5 e 6 della §3 al variare di aggregatore e prompt.
  2. **Fase umana, disegno a 3 bracci randomizzato per gruppo:**
     - (a) mediatore LLM;
     - (b) facilitatore umano;
     - (c) solo voto/Polis senza sintesi.
     
     Outcome: accordo con la sintesi, cambiamento pre→post, deriva verso la maggioranza (metrica 1), copertura delle minoranze (2), impatto percepito e pressione percepita.
  3. **Fattore aggiuntivo:** trasparenza, cioè criteri, pesi e aggregatore visibili e modificabili contro nascosti. Questo misura direttamente la seconda metà della domanda.
  4. **Soglie preregistrate** prima delle prove (per esempio: deriva verso la maggioranza del braccio LLM non superiore a quella del braccio umano oltre un margine fissato).
- [I] Dimensione del campione: con gruppi di circa 5 l'unità di analisi è il gruppo. Servono decine di gruppi per braccio. Va fatto un calcolo di potenza su ICC; non ho trovato un valore di riferimento [L].

### Gaps
- [L] Nessun protocollo standard accettato per "minority-voice metrics" in deliberazione mediata da IA: le metriche sopra sono proposte [H], non riprese da una fonte.
- [L] Fonti da recuperare in originale (domini bloccati): Tessler et al. 2024 Science con supplementari; Salvi et al. 2025 NHB; Small et al. 2021 (Polis, *Recerca*); Ovadya & Thorburn 2023 (bridging systems); documentazione di Community Notes; report finale di Meta e Stanford.
