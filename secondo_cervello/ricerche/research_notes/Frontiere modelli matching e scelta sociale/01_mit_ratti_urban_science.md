# Modelli matematici, statistici e ML dei laboratori di scienza urbana (MIT City Science, Senseable City Lab, SFI, Sony CSL, Tsinghua, Stanford, UCL CASA) su abitazione, scelta residenziale, segregazione, accessibilità e supporto partecipativo

Nota di metodo. Ricerca del 9–10/11/2026. Estende il report `reports/Lotti ideali partecipazione e digital twin.md` e non ne ripete i contenuti (Finding Places in sintesi, Abbiasov come risultato, E2SFCA, Zheng et al. come citazione). Marche: **[V]** testo letto su arXiv o sul codice sorgente; **[S]** da snippet o fonte secondaria; **[I]** inferenza mia; **[L]** lacuna; **[forma standard]** formula scritta da me nella forma canonica, non vista sulla pagina del paper. Limite tecnico della sessione: nature.com, pnas.org, science.org, PMC e senseable.mit.edu **non erano raggiungibili** dalla rete dell'ambiente. Ho letto quindi i preprint arXiv (testo completo via pdftotext) e il repository GitHub di Zheng et al. Le versioni pubblicate su rivista possono differire dai preprint; lo segnalo dove lo so.

## 1. MIT City Science: quali sono le funzioni di utilità e di scelta reali di CityScope?

### Takeaway
Nel modello ABM "casa + mobilità" di CityScope (Yurrita et al. 2021) la scelta **non è un logit stimato**. È un punteggio lineare deterministico con pesi **sintetici** per fascia di reddito, una regola di trasloco "alla Schelling" (l'agente si sposta se l'alternativa estratta a caso ha punteggio maggiore) e una calibrazione per hill climbing su 64 parametri contro due RMSE. Finding Places non aveva alcun modello di scelta: c'era una classificazione GIS a tre classi di "non idoneità" con pesi non pubblicati, e l'esito si è fermato a 6 siti su 161 proposti (~750 posti, ~4% dell'obiettivo).

### Cited Findings
**A. Yurrita, Grignard, Alonso, Zhang, Jara-Figueroa, Elkatsha, Larson (2021), "Dynamic Urban Planning: an Agent-Based Model Coupling Mobility Mode and Housing Choice. Use case Kendall Square", arXiv:2106.14572 [cs.MA]** ([arXiv](https://arxiv.org/abs/2106.14572)) [V, testo integrale]. Pubblicazione: Springer LNNS vol. 284 secondo [aggregatori](https://www.aminer.org/pub/60dc012791e0117bb69ae699/dynamic-urban-planning-an-agent-based-model-coupling-mobility-mode-and-housing) [S].
- Scopo dichiarato: è il "first step in the development of a dynamic incentive system". Tra gli incentivi esplorati c'è "affordable housing within a 20-minute walking distance from one's workplace" ([arXiv](https://arxiv.org/abs/2106.14572)) [V]. Il paper **non contiene un modello di incentivo**, solo il modello di comportamento su cui testarlo [V].
- Entità: block group del censimento (GEOID, posti vacanti, affitto medio da web scraping di PadMapper, popolazione per fascia di reddito, presenza di T/bus); edifici; strade; agenti "people" che lavorano nell'area, ciascuno con un luogo di lavoro assegnato ([arXiv](https://arxiv.org/abs/2106.14572)) [V].
- **Scelta del modo di trasporto.** Il testo dice: "a final score for each mode will be calculated as a linear combination of the importance given to each of these factors. The option that maximizes the score will be the chosen mobility mode". Formalizzazione mia (il paper non scrive l'equazione) [I, fedele al testo]:
  $$U^{mob}_{g,m} = w^{price}_g\,c_m d + w^{time}_g\,t_m(d) + w^{diff}_g\,D_m + w^{pat}_g\,P_m,\qquad m^* = \arg\max_{m\in M_i} U^{mob}_{g,m}$$
  Qui $g$ è la fascia di reddito, $c_m$ il prezzo per km, $d$ la distanza casa–lavoro, $t_m$ il tempo (attesa + percorso sulla rete), $D_m$ la difficoltà e $P_m$ il "social pattern". $M_i$ sono i modi disponibili, cioè quelli posseduti e quelli con trasporto pubblico presente sia all'origine sia alla destinazione. Pesi della Tab. 1 (sintetici, "modified from working status profiles into income profiles"): fascia \$45–60k: −0,8 / −0,8 / −0,7 / 0,7; fascia \$60–100k: −0,7 / −0,85 / −0,75 / 0,8; fascia \$100–125k: −0,6 / −0,9 / −0,8 / 0,95. Tab. 2: bici 0,01 \$/km a 5 km/h; bus 0,1 \$/km a 20 km/h; auto 0,32 \$/km a 30 km/h. Pattern: bici 0,5, bus 0,4, auto 1 ([arXiv](https://arxiv.org/abs/2106.14572)) [V].
- **Scelta residenziale.** Iterazione $i$: a ogni agente si assegna a caso un'abitazione alternativa. L'agente "will decide to move in iteration 'i' if the score of the alternative housing unit is greater than the current one". I fattori sono prezzo, tempo di pendolarismo con il modo migliore, preferenza di zona, peso della zona e "diversity acceptance". La diversità è l'indice di Shannon-Weaver sulle fasce di reddito, calcolato sull'edificio o sul block group ([arXiv](https://arxiv.org/abs/2106.14572)) [V]. Formalizzazione [I]:
  $$U^{house}_{g,h} = w^{p}_g\,\mathrm{rent}_h + w^{div}_g\,H_h + w^{zone}_g\,\mathbb{1}[h\in Z_g] + \max_m U^{mob}_{g,m}(h),\qquad H_h = -\sum_{k} p_{k,h}\ln p_{k,h}$$
  Regola: $h_i^{t+1} = h'$ se $U(h') > U(h_i^t)$, con $h'$ estratta a caso. Si itera finché il numero di traslochi tende a 0. Tab. 3 (sintetica): prezzo −0,8 / −0,6 / −0,5; diversity acceptance 0 / −0,3 / −0,5; peso zona 0,4 / 0,5 / 0,6 ([arXiv](https://arxiv.org/abs/2106.14572)) [V]. La forma esatta di Shannon non è scritta nel paper, che rimanda a CityScope Volpe [forma standard]. Sul modo in cui il tempo entra nel punteggio residenziale il paper è ambiguo: dice solo che "the 'time' parameter is calculated" [L].
- **Calibrazione.** Due errori RMSE:
  $$\mathrm{RMSE} = \sqrt{\tfrac{1}{n}\sum_{i=1}^{n}(Y_i - \hat Y_i)^2}$$
  Il primo confronta la quota per fascia di reddito per block group: osservata da dati di trasporto e censimento, contro simulata. Il secondo confronta lo split modale con i dati PTDM di Cambridge (2014). Otto fattori per otto fasce danno **64 variabili**, esplorate con **hill climbing** in batch. Risultato: errore abitativo medio **3,87%**, errore di mobilità **2,30%**. Il limite è ammesso dagli autori: l'algoritmo "heavily relies on the selected starting point". Il calcolo in tempo reale non è ancora possibile ([arXiv](https://arxiv.org/abs/2106.14572)) [V].
- Il modello è implementato in **GAMA/GAML**. Riferimenti interni: modelli di mode choice "MoCho" con logit (Doorley et al., UrbComp 2019) e Grignard et al. 2018 (ICCS) ([arXiv, bibliografia](https://arxiv.org/abs/2106.14572)) [V come citazione; MoCho non letto, L].

**B. Noyman, Holtz, Kröger, Noennig, Larson (2017), "Finding Places: HCI Platform for Public Participation in Refugees' Accommodation Process", Procedia Computer Science (KES), arXiv:1811.10123** ([arXiv](https://arxiv.org/abs/1811.10123)) [V, testo integrale]. Questi dati chiudono le discrepanze aperte dal report precedente:
- Pre-screening: "geospatial data layers were intersected and weighted to create initial assessments of places, then sorted into three ranked classes". Le classi sono alta, media e bassa "indication of unsuitability" (soglia: criteri meno restrittivi su <50% dell'area). **I pesi non sono riportati** ([arXiv](https://arxiv.org/abs/1811.10123)) [V; pesi: L].
- Esito: 34 workshop, ~400 partecipanti (media 11 per workshop), 161 siti proposti per "almost 24,000 refugees". Il 24.000 è quindi la capacità proposta e il 20.000 l'obiettivo: le due cifre non sono in conflitto. 44 siti giudicati fattibili, 24 esclusi dopo esame, **6 raccomandati** e 10 tenuti per la pianificazione futura. I 6 siti valgono "approximately 750 refugees … ~4% of the initial target" ([arXiv](https://arxiv.org/abs/1811.10123)) [V]. Le cifre "6 costruiti" (URBACT) non trovano conferma qui [I].
- Autocritica degli autori (analisi SWOT): selection bias legato alla sede; dati difficili da leggere per i non esperti; "Pre-processing of data allows for manipulation of the overall process outcome (e.g. suggestive color-coding…)"; alcuni partecipanti parlavano di partecipazione "'faked'" ([arXiv](https://arxiv.org/abs/1811.10123)) [V].

**C. Altro di City Science.** La pagina di progetto "Algorithmic Zoning / Dynamic Urban Planning" del Media Lab collega il modello A a CityScope ([MIT Media Lab](https://www-prod.media.mit.edu/projects/algorithmic-zoning-dynamic-urban-planning/overview/)) [S, non aperta].

### Inferences
- Le "funzioni di utilità" di CityScope sono **punteggi lineari a pesi fissati dal modellista**. Non c'è un termine d'errore stocastico, non c'è stima econometrica dei pesi e non c'è un'identificazione che separi preferenze da vincoli. È proprio il "decisore nascosto" che la tesi teme: chi scrive le Tab. 1–3 decide prima degli abitanti [I].
- Per la pipeline il modello A è un buon **anti-esempio documentato**. Si può conservare l'architettura (ABM con scelta congiunta casa–mobilità, calibrazione su distribuzioni osservate). Vanno sostituiti: (i) il punteggio con un logit multinomiale o misto, $P_{ih} = \frac{e^{V_{ih}}}{\sum_{h'}e^{V_{ih'}}}$ [forma standard]; (ii) i pesi sintetici con pesi dichiarati e riscrivibili dai gruppi; (iii) l'hill climbing con una calibrazione che riporti l'incertezza (ABC o SMAA) [I].
- Finding Places mostra che il filtro di idoneità, cioè i pesi del pre-screening, decide più dei workshop: circa 3/4 dei siti proposti cadevano già nella classe "non idoneo". Il filtro va pubblicato come regola esplicita e contestabile [I].

### Gaps
- Tesi di Noyman (DSpace 1721.1/145128): il bitstream di DSpace restituiva una pagina HTML e il PDF non si è aperto. Non ho verificato se contenga modelli formali di ottimizzazione o incentivi [L].
- Un modello di "dynamic incentive" con funzione obiettivo pubblicata (es. bonus di densità contro quota di alloggi accessibili) **non l'ho trovato** nei testi accessibili [L].
- I modelli logit MoCho (Doorley et al. 2019) non sono stati letti [L].

## 2. Senseable City Lab e ambito MIT: segregazione sperimentata, città dei 15 minuti, percezione da street view. Con quali formule?

### Takeaway
La segregazione "sperimentata" si misura come differenza di reddito (o rango di reddito) tra chi co-visita gli stessi luoghi, aggregata per luogo e poi per residenza. La versione di Senseable (Abbiasov et al.) è scritta per esteso nel preprint. Quella di Moro et al. 2021 viene dal gruppo Human Dynamics/Connection Science del Media Lab, non da Senseable. Il risultato più utile per la tesi resta empirico e solo parzialmente causale: l'accesso locale spiega l'uso locale (con un IV su New York), ma per i quartieri poveri l'uso locale si associa a più segregazione. Quest'ultimo legame è solo correlazionale.

### Cited Findings
**A. Abbiasov, Heine, Glaeser, Ratti, Sabouri, Salazar-Miranda, Santi, "The 15-Minute City Quantified Using Mobility Data", arXiv:2211.14872 (2022)**. Versione rivista: Nature Human Behaviour 8 (2024) ([arXiv](https://arxiv.org/abs/2211.14872)) [V, preprint].
- Dati: SafeGraph, ~40 milioni di dispositivi, 418 aree urbane USA, 5,3 milioni di POI. Le otto categorie di POI coprono il 30% dei POI e il 35% dei viaggi ([arXiv](https://arxiv.org/abs/2211.14872)) [V].
- **Uso locale** (definizione verbale del preprint, scritta in formula da me) [I]:
  $$\mathrm{Usage}_j = \frac{\#\{\text{viaggi da }j\text{ verso POI}\in W_{15}(j)\}}{\#\{\text{viaggi da }j\}}$$
  dove $W_{15}(j)$ è il walkshed di 15 minuti del block group $j$.
- **Accesso**: per ogni categoria $c$ si contano i POI nel walkshed; si assegna il percentile del block group tra tutti i block group; si fa la media sulle 8 categorie e si ottiene un indice 0–100 ([arXiv](https://arxiv.org/abs/2211.14872)) [V].
  $$\mathrm{Access}_j = \tfrac{1}{8}\sum_{c=1}^{8}\mathrm{pct}_c\big(N_c(W_{15}(j))\big)$$ [I, fedele al testo]
- **Segregazione sperimentata** (Appendice 5.3, che segue Xu et al. 2019; formula vista sulla pagina) ([arXiv](https://arxiv.org/abs/2211.14872)) [V]:
  $$\mathrm{EI}_{k_i,L} = \frac{\sum_{k_j} p_{k_j,L}\, s_{k_i\to k_j}}{\sum_{k_j} p_{k_j,L}},\quad s_{k_i\to k_j} = |r_i - r_j|$$
  $$\mathrm{EI}_j = \frac{\sum_{L} \mathrm{EI}_{k_j,L}\, p_{j,L}}{\sum_L p_{j,L}},\qquad \mathrm{ES}_j = 1 - \mathrm{EI}_j$$
  Qui $p_{k,L}$ è il numero di visitatori di reddito $k$ al POI $L$, $r$ il rango di reddito e $p_{j,L}$ il numero di visitatori dal block group $j$ al POI $L$. L'indice è riscalato su 0–100. Nel preprint la seconda formula ha un refuso ("experienced segregation" al posto di "integration" al numeratore) [V].
- Risultati del preprint: il residente mediano fa il **12,1%** dei viaggi entro 15 minuti a piedi. Il report precedente cita il **14%** dalla versione su NHB: le due versioni differiscono, va citata quella pubblicata [V preprint; discrepanza da riconciliare, L]. L'accesso spiega l'**81%** della varianza tra aree urbane e il **74%** entro le aree. OLS: +1 percentile di accesso dà +0,76–0,8 p.p. di uso. **IV** con il FAR commerciale massimo dello zoning di New York del 1961: coefficiente ≈ **1,1**. Gli autori lo chiamano "a step towards causal inference rather than perfect estimates", perché resta l'auto-selezione residenziale ([arXiv](https://arxiv.org/abs/2211.14872)) [V].
- Trade-off: per i quartieri poveri la segregazione sperimentata sale da **67,6 a 71,4** (≈0,48 deviazioni standard) passando da uso locale minimo a massimo; nelle città con uso locale più alto la differenza è di 1,3 DS. Per i quartieri ricchi accade l'opposto ([arXiv](https://arxiv.org/abs/2211.14872)) [V]. È una relazione **correlazionale** [V].

**B. Moro, Calacci, Dong, Pentland (2021), "Mobility patterns are associated with experienced income segregation in large US cities", Nature Communications 12:4633, DOI 10.1038/s41467-021-24899-8** ([DOAJ](https://doaj.org/article/879d7d248594456c9903511066911e19); [DSpace](https://dspace.mit.edu/handle/1721.1/131211)) [S: record verificato, testo non raggiungibile]. Dati: 4,5 milioni di utenti e 1,1 milioni di luoghi in 11 città USA. Include una "Schelling extension of a well-known mobility model" (esplorazione e ritorno preferenziale) ([ricerca](https://www.nature.com/articles/s41467-021-24899-8)) [S].
- Indice [forma standard, da memoria, **non visto sulla pagina**; da verificare sui Methods prima di citarlo]:
  $$S_\alpha = \tfrac{2}{3}\sum_{q=1}^{4}\left|\tau_{q\alpha} - \tfrac14\right|,\qquad S_i = \tfrac{2}{3}\sum_{q}\left|\tau_{iq} - \tfrac14\right|$$
  dove $\tau_{q\alpha}$ è la quota di tempo trascorsa al luogo $\alpha$ da persone del quartile di reddito $q$, e $\tau_{iq}$ è l'esposizione dell'individuo $i$ al quartile $q$ pesata sul tempo che passa nei luoghi. Il fattore $2/3$ normalizza su $[0,1]$ [L: verifica].
- Studio successivo dello stesso gruppo: Tonin, Tizzoni, Lepri, Moro, "Experienced partisan segregation across patterns of mobility behavior in US cities", arXiv:2609.19285 (09/2026). Su 11 aree metropolitane, chi viaggia più lontano incontra ambienti più eterogenei, ma "exploring a wider range of places does not reduce partisan segregation and may even reinforce it" ([arXiv](https://arxiv.org/abs/2609.19285)) [V, abstract].

**C. Percezione da street view (Place Pulse).** Dubey, Naik, Parikh, Raskar, Hidalgo, "Deep Learning the City: Quantifying Urban Perception at a Global Scale", ECCV 2016, arXiv:1608.01769 (MIT Media Lab, Macro Connections; non Senseable) ([arXiv](https://arxiv.org/abs/1608.01769)) [V].
- Dataset Place Pulse 2.0: 110.988 immagini, 56 città, **1,17 milioni** di confronti a coppie da 81.630 volontari ([arXiv](https://arxiv.org/abs/1608.01769)) [V].
- Perdite: classificazione softmax sulla coppia, $L_c$, più ranking hinge (forma RankSVM) ([arXiv](https://arxiv.org/abs/1608.01769)) [V]:
  $$L_r = \sum_{(i,j,y)}\max\big(0,\; y\,(f_r(x_j) - f_r(x_i))\big),\qquad L = L_c + \lambda L_r$$
  dove $y=+1$ se vince l'immagine $i$. Accuratezza sui confronti a coppie (percezione "safety", per varianti): SS-CNN con VGGNet 65,3–72,4%, RSS-CNN con VGGNet 73,5% ([arXiv](https://arxiv.org/abs/1608.01769)) [V, tabella letta in forma estratta; attribuzione delle colonne da ricontrollare].
- **Treepedia** (Senseable): Cai, Li, Seiferling, Ratti, "Treepedia 2.0", arXiv:1808.04754 (2018). Usa il Green View Index, "green pixels as a percentage of total pixels in a GSV image", stimato con DCNN (segmentazione semantica ed end-to-end). Validazione con IoU medio $\overline{IoU} = \frac1n\sum_i \frac{TP_i}{TP_i+FP_i+FN_i}$ e con MAE del GVI ([arXiv](https://arxiv.org/abs/1808.04754)) [V]. GVI per punto [forma standard, Li et al. 2015, non visto]: $\mathrm{GVI} = \frac{\sum_{i=1}^{6}\sum_{j=1}^{3}A^{g}_{ij}}{\sum_{i}\sum_j A^{t}_{ij}}$ su 6 direzioni × 3 inclinazioni.

### Inferences
- Per la tesi conviene usare la formula di Abbiasov (rango di reddito, media sui co-visitatori), che è verificata ed esplicita. Da lì si può costruire una **metrica di esposizione attesa per gruppo e lotto**: al posto dei visitatori osservati si usano i flussi previsti dai servizi raggiungibili dal lotto. Questo affianca a ogni criterio di accessibilità un controllo di mescolanza, come chiedeva già il report precedente [I].
- Per gruppi abitativi eterogenei, $\sum_{k_j}p_{k_j}|r_i-r_j|$ è anche una **metrica di diversità interna del gruppo** (distanza media di rango). Va calcolata in modo trasparente e mostrata ai partecipanti, non imposta [I].
- Place Pulse misura giudizi di online volunteers per lo più stranieri al luogo (la provenienza è nel paper, non riportata qui). Usarlo per "qualità del lotto" importerebbe un'estetica di massa al posto delle esigenze dichiarate: al più può servire come variabile osservata [I].

### Gaps
- Formula esatta di Moro et al. 2021 e del loro modello Schelling–EPR: non verificata [L].
- Lavori Senseable sul digital twin e sull'abitazione (es. Salazar-Miranda su prezzi e amenità): non coperti per mancanza di accesso a senseable.mit.edu [L].
- Versione NHB 2024 di Abbiasov: le cifre finali (14% contro 12%) e l'eventuale revisione dell'IV non sono state viste [L].

## 3. Leggi di scala urbana (Bettencourt, West, SFI) e loro critiche; modelli di gravità e di radiazione

### Takeaway
La legge $Y=Y_0N^\beta$ (β≈1,15 per i prodotti socioeconomici, ≈0,85 per le infrastrutture) è una regolarità **descrittiva** e dipende da come si definiscono i confini urbani. UCL CASA (Arcaute et al.) trova in Inghilterra e Galles soprattutto scaling lineare. Il modello di radiazione (Simini et al. 2012) dà flussi pendolari senza parametri da stimare, ma serve a scala regionale, non per scegliere il lotto in un quartiere.

### Cited Findings
- **Ipotesi di scaling** (Bettencourt, Lobo, Youn, "The hypothesis of urban scaling: formalization, implications and challenges", arXiv:1301.5919, 2013). L'invarianza di scala $Y(\lambda N)/Y(N)=f(\lambda)$ implica $Y(N)=Y_0N^\beta$ con $\beta = d\ln Y/d\ln N$ ([arXiv](https://arxiv.org/abs/1301.5919)) [V].
- **Modello di Bettencourt (Science 340, 2013, "The origins of scaling in cities")**, nella ricostruzione di Ribeiro e Rybski, "Mathematical models to explain the origin of urban scaling laws: a synthetic review", arXiv:2111.08365 ([arXiv](https://arxiv.org/abs/2111.08365)) [V la review; Science non letto, S]:
  - densità di contatti $n_c = a/A$, con area esplorata $a = l_0 l$ indipendente da $N$, da cui $Y\sim N^2/A$;
  - costo di trasporto $c\sim L$, totale $T\sim N\sqrt{A}$; vincolo $y\sim c\Rightarrow T\sim Y$, da cui $A\sim N^{2/3}$;
  - area di rete $A_n\sim N\lambda$, $\lambda\sim N^{-1/6}$, quindi $A_n\sim N^{5/6}$ ($\beta_{sub}=5/6$) e $Y\sim N^{7/6}$ ($\beta_{super}=7/6$), con $\beta_{sub}+\beta_{super}=2$.
  - Limiti indicati dalla review: con l'area circoscritta l'esponente viene 0,67 invece di 0,85; il modello non considera amenità e volumi edificati ([arXiv](https://arxiv.org/abs/2111.08365)) [V].
- **Modello a collaborazione richiesta** (Yang et al. 2019, ripreso nella review): $Y\sim N\langle k\rangle^q$, quindi $\beta_{super}\approx 1 + q\,\frac{\Delta\log\langle k\rangle}{\Delta\log N}$ ([arXiv](https://arxiv.org/abs/2111.08365)) [V].
- **Evidenza da contatti telefonici** (Schläpfer, Bettencourt et al., "The scaling of human interactions with city size", arXiv:1210.5215; J. R. Soc. Interface 2014). Il grado cumulato riscalato $K_r\propto N^\beta$ ha β = 1,12 (IC 95% 1,11–1,14) in Portogallo e β = 1,08–1,14 nel Regno Unito (rete fissa). Il clustering medio resta ≈0,25, indipendente da $N$ ([arXiv](https://arxiv.org/abs/1210.5215)) [V].
- **Critica UCL CASA**: Arcaute, Hatna, Ferguson, Youn, Johansson, Batty, "Constructing cities, deconstructing scaling laws", arXiv:1301.1674 (J. R. Soc. Interface 2015). Costruiscono migliaia di sistemi urbani per Inghilterra e Galles, variando soglie di densità (scelta $\rho_c$ = 14 persone/ha) e di pendolarismo. Concludono: "most urban indicators scale linearly with city size regardless of the definition of the urban boundaries. However, when non-linear correlations are present, the exponent fluctuates considerably" ([arXiv](https://arxiv.org/abs/1301.1674)) [V].
- **Gravità** (in Simini et al.): $T_{ij} = \frac{m_i^{\alpha} n_j^{\beta}}{f(r_{ij})}$. Problemi elencati: parametri da adattare, nessuna base per $f(r)$, divergenza al crescere di $n_j$, determinismo. Esempio: 6 pendolari tra due contee dell'Alabama contro 44 nello Utah, a parità di popolazione e distanza ([arXiv:1111.0586](https://arxiv.org/abs/1111.0586)) [V].
- **Radiazione**: Simini, González, Maritan, Barabási, "A universal model for mobility and migration patterns", Nature 484 (2012), arXiv:1111.0586 ([arXiv](https://arxiv.org/abs/1111.0586)) [V]:
  $$\langle T_{ij}\rangle = T_i\,\frac{m_i n_j}{(m_i+s_{ij})(m_i+n_j+s_{ij})},\qquad T_i = m_i\frac{N_c}{N}$$
  Qui $s_{ij}$ è la popolazione nel cerchio di raggio $r_{ij}$ centrato in $i$, esclusi $i$ e $j$. Con densità uniforme si riduce a una gravità con $f(r)=r^4$. Il modello nasce da un processo di offerte di lavoro (ognuno accetta la migliore offerta più vicina che superi quella locale) ed è indipendente da $p(z)$. È validato sul pendolarismo tra contee USA del censimento e su migrazioni, telefonate e commercio ([arXiv](https://arxiv.org/abs/1111.0586)) [V].

### Inferences
- Per Milano lo scaling non serve a scegliere i lotti: è una legge tra città, non dentro la città [I]. Si può citare come contesto ("le grandi città mescolano meno", vedi Nilforoshan, §4).
- Il modello di radiazione è utile come **stima a zero parametri della domanda di pendolarismo** tra NIL o comuni dell'area metropolitana, e quindi del costo di pendolarismo di ciascun lotto candidato. Andrebbe confrontato con i dati O/D di Regione Lombardia, non dato per buono [I].

### Gaps
- Testo di Science 2013 non letto direttamente; le critiche successive (Leitão et al. 2016 sulla stima statistica, Cottineau et al. 2017) non sono state verificate [L].

## 4. Modelli di frontiera di altri laboratori: deep RL per layout di comunità (Tsinghua), modelli fondazionali urbani, GNN, accessibilità equa (Sony CSL), segregazione da esposizione (Stanford)

### Takeaway
Il modello di Tsinghua (Zheng et al. 2023) ottimizza **una ricompensa scritta dal programmatore**: una somma pesata di copertura dei servizi a 500 m, decentralizzazione e verde entro 300 m, con pesi 4:1 nel file di configurazione. Supera gli esperti sulle **sue** metriche. Sony CSL propone un'accessibilità con indice di Gini e un algoritmo greedy di ricollocazione dei servizi. Stanford mostra che l'esposizione è più segregata nelle grandi città. I modelli fondazionali urbani sono per ora una rassegna di promesse, senza evidenza su decisioni abitative.

### Cited Findings
**A. Zheng, Lin, Zhao, Wu, Jin, Li (Tsinghua FIB Lab), "Spatial planning of urban communities via deep reinforcement learning", Nature Computational Science 3:748–762 (2023), DOI 10.1038/s43588-023-00503-5** ([codice](https://github.com/tsinghua-fib-lab/DRL-urban-planning)) [V codice; paper S].
- Stato: grafo di contiguità (parcelle, segmenti stradali, incroci) codificato da una **GNN** a message passing e condiviso da rete di valore e policy. Due fasi: usi del suolo, poi strade ([ricerca su Nature/SI](https://www.nature.com/articles/s43588-023-00503-5)) [S].
- **Ricompense lette nel codice** `urban_planning/envs/plan_client.py` ([GitHub](https://github.com/tsinghua-fib-lab/DRL-urban-planning)) [V]:
  - Servizi ("life circle"): per ogni residenza $r$ e tipo di servizio $s$, $d_{rs}$ è la distanza dal servizio più vicino.
    $$R_{life} = \frac{1}{|Res|}\sum_{r}\frac{1}{S}\sum_{s}\mathbb{1}[d_{rs}\le 500\,\mathrm{m}] + 0{,}05\,\frac{\bar d_{pair}}{D_{ref}}$$
    Il primo termine è la quota di servizi entro 500 m (chiamata "10 minuti"). Il secondo è la distanza media tra servizi dello stesso tipo, normalizzata dalla diagonale della griglia (decentralizzazione). Le soglie 1000 m e 300 m sono solo riportate come "15 min" e "5 min".
  - Verde: $R_{green} = \frac{\mathrm{area}(Res\cap \mathrm{buffer}_{300m}(Green_{\ge soglia}))}{\mathrm{area}(Res)}$.
  - Rete stradale: media di 6 termini (inverso del numero di componenti connesse, densità/10, penalità $1/(n+1)$ per vicoli ciechi, strade <100 m e >600 m, isolati >800 m).
  - Pesi nella configurazione HLG: `life_circle_weight: 4.0`, `greenness_weight: 1.0`, `road_network_weight: 0.0` ([GitHub cfg](https://github.com/tsinghua-fib-lab/DRL-urban-planning)) [V].
- Dati: una comunità sintetica e due reali di Pechino (HLG, DHM) da OpenStreetMap. Gli obiettivi sono quantità e aree per funzione in `objectives.yaml`. Baseline: euristiche centralizzate e decentralizzate, set-coverage geometrico, GA ([GitHub README](https://github.com/tsinghua-fib-lab/DRL-urban-planning)) [V]. Il dato "3000 volte più veloce degli esperti" viene dalla stampa ([36kr](https://www.36kr.com/p/2428166967796482)) [S, non verificato].

**B. Sony CSL Roma: Bruno, Monteiro Melo, Campanelli, Loreto, "A universal framework for inclusive 15-minute cities", arXiv:2408.03794 (2024)**; versione pubblicata su Nature Cities secondo la mia memoria [L] ([arXiv](https://arxiv.org/abs/2408.03794)) [V preprint]. Formule viste sulla pagina:
  $$\langle t\rangle_{c,k} = \frac1n\sum_{i=1}^{n} t_i^{c,k}\ (n=20),\quad PT_k = \frac1m\sum_{c=1}^{m}\langle t\rangle_{c,k},\quad PT_{city} = \frac{\sum_k PT_k\,p_k}{\sum_k p_k}$$
  $$F_{15} = 100\cdot\frac{\sum_{k:PT_k\le 15}p_k}{\sum_k p_k},\qquad G = 1 - \frac{2\sum_{p=1}^{N_{pop}}\sum_{p'\le p}PT_{p'}}{N_{pop}\sum_{p}PT_p}$$
  Esagoni di lato 200 m, 9 categorie di servizi, tempi calcolati con OSRM su OpenStreetMap, popolazione da WorldPop. **Algoritmo di ricollocazione**: capacità $CAP_c = N_{pop}/N_c$; ogni POI si piazza (con un po' di casualità) nell'esagono con la massima domanda non servita raggiungibile entro 15 minuti; poi si sottrae $CAP_c$ alla domanda degli esagoni serviti. Risultato: ricollocare i POI esistenti migliora le periferie senza peggiorare il centro. Piattaforma: whatif.sonycsl.it/15mincity ([arXiv](https://arxiv.org/abs/2408.03794)) [V].

**C. Stanford (Leskovec), Nilforoshan et al., "Human mobility networks reveal increased segregation in large cities", Nature 624:586–592 (2023), DOI 10.1038/s41586-023-06757-3; arXiv:2210.07414** ([arXiv](https://arxiv.org/abs/2210.07414)) [V].
- **Exposure segregation** = correlazione tra lo SES di una persona e lo SES medio di chi incrocia (stimata con modello lineare a effetti misti per eliminare l'attenuation bias). Generalizza il Neighborhood Sorting Index, che è la correlazione con lo SES medio del proprio tract ([arXiv](https://arxiv.org/abs/2210.07414)) [V]. Forma [standard, mia]: $ES = \mathrm{corr}\big(SES_i,\ \frac{1}{|E_i|}\sum_{j\in E_i}SES_j\big)$.
- 1,6 miliardi di esposizioni tra 9,6 milioni di persone, 382 MSA. Lo SES è proxato dall'affitto stimato della casa. Le 10 MSA più grandi sono **+67%** più segregate (IC 95% 49–87%) delle MSA sotto i 100.000 abitanti; Spearman 0,62 ([arXiv](https://arxiv.org/abs/2210.07414)) [V].

**D. Modelli fondazionali urbani.** W. Zhang, Han, Xu, Ni, Lyu, H. Liu, Xiong, "Towards Urban General Intelligence: A Review and Outlook of Urban Foundation Models", arXiv:2402.01749. Propone una tassonomia per modalità di dato; secondo il PDF la sede è ACM TIST ([arXiv](https://arxiv.org/abs/2402.01749)) [S].

### Inferences
- Zheng et al. sono la prova concreta del problema di "chi scrive la ricompensa". La quota di servizi entro 500 m, la soglia del verde a 300 m e il rapporto 4:1 sono scelte di un programmatore, non preferenze di abitanti. Nella pipeline di tesi queste costanti dovrebbero diventare **parametri pubblici e riscrivibili dai gruppi**, con analisi di sensibilità che mostri come cambia il piano al variare dei pesi (stessa logica della SMAA) [I].
- Da Sony CSL la tesi può prendere $PT_k$, $F_{15}$ e Gini come **metriche di lotto** già riproducibili su OSM e OSRM per Milano. L'algoritmo greedy di capacità è un modello trasparente di "dove servono servizi", spiegabile a non esperti, a differenza di una policy RL [I].
- Nilforoshan e Abbiasov insieme dicono che più prossimità non garantisce più mescolanza. Un criterio di accessibilità senza un vincolo di esposizione può peggiorare la segregazione [I].

### Gaps
- ETH Future Cities Lab, NYU CUSP/Marron e UCL CASA (oltre Arcaute): nessun modello formale su abitazione e scelta residenziale è stato verificato in questa sessione per limiti di tempo e di rete [L].
- Valori numerici di Zheng et al. contro gli esperti (percentuali) e protocollo della valutazione con gli esperti: non letti [L].
- GNN e embedding urbani per la stima di idoneità residenziale: nessun lavoro verificato qui [L].

## 5. Limiti e frontiera: quali affermazioni hanno evidenza causale o validata, quali sono descrittive o speculative?

### Takeaway
Quasi tutto il corpus è **descrittivo** (scaling, segregazione da mobilità, percezione) o **normativo-simulativo** (ABM CityScope, DRL Tsinghua, ricollocazione Sony CSL), validato su metriche proprie o su errori di calibrazione aggregati. L'unico tentativo esplicito di identificazione causale trovato è l'IV sullo zoning del 1961 (Abbiasov et al.), che gli autori stessi giudicano parziale. Non ho trovato alcuna prova che un dispositivo partecipativo con IA abbia cambiato l'esito abitativo per le famiglie.

### Cited Findings
- Causale (parziale): +1 percentile di accesso dà ≈ +1,1 p.p. di uso locale (IV con il FAR commerciale del 1961, New York); resta l'auto-selezione ([arXiv:2211.14872](https://arxiv.org/abs/2211.14872)) [V].
- Validato come previsione: il modello di radiazione riproduce i flussi pendolari tra contee USA meglio della gravità, senza parametri ([arXiv:1111.0586](https://arxiv.org/abs/1111.0586)) [V].
- Calibrazione aggregata, non validazione fuori campione: l'ABM CityScope arriva al 3,87% e al 2,30% di RMSE su 64 parametri sintetici, con un algoritmo dipendente dal punto di partenza ([arXiv:2106.14572](https://arxiv.org/abs/2106.14572)) [V].
- Descrittivo e sensibile alle definizioni: gli esponenti di scaling cambiano con i confini e molti indicatori sono lineari ([arXiv:1301.1674](https://arxiv.org/abs/1301.1674)) [V].
- Correlazionale: segregazione sperimentata contro uso locale, per reddito ([arXiv:2211.14872](https://arxiv.org/abs/2211.14872)) [V]; dimensione della città contro exposure segregation ([arXiv:2210.07414](https://arxiv.org/abs/2210.07414)) [V].
- Partecipazione: in Finding Places 6 siti su 161 sono arrivati a raccomandazione (~4% dell'obiettivo); gli autori ammettono selection bias e possibile manipolazione tramite il pre-processing ([arXiv:1811.10123](https://arxiv.org/abs/1811.10123)) [V].

### Inferences
- Per la tesi ne segue una regola di metodo. I modelli urbani di questi laboratori vanno usati come **strumenti di misura dichiarati** (accessibilità $PT$/$F_{15}$, esposizione $ES$, flussi di radiazione), non come previsori del comportamento delle famiglie. Ogni costante (soglie, pesi, ricompense) va esposta nell'interfaccia e resa riscrivibile [I].
- Nessuno dei modelli tratta il **gruppo** come unità decisionale né la scelta tra lotti come un abbinamento. Questo è il vuoto in cui la tesi può collocarsi: matching gruppi–lotti con criteri pubblici e una metrica di esposizione come vincolo [I].
- Ipotesi falsificabile proponibile [H]: a parità di costo per famiglia, i lotti scelti con un vincolo esplicito di esposizione hanno un $ES$ atteso più basso di quelli scelti per sola prossimità, e il costo in accessibilità ($\Delta PT$) è sotto una soglia fissata prima dell'esperimento.

### Gaps
- Nessuna prova trovata, né causale né sperimentale, che CityScope o strumenti analoghi abbiano spostato decisioni sull'abitazione a favore dei redditi medi [L].
- Studi di replica dei modelli di segregazione da mobilità in Europa o in Italia: non cercati in questa sessione. In parte rimedia Liao & Gil, arXiv:2407.00404, sulla Svezia ([arXiv](https://arxiv.org/abs/2407.00404)) [S, solo titolo e riferimenti] [L].
