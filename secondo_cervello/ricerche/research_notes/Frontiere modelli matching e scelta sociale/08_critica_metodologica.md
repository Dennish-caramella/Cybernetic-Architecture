# Critica metodologica del disegno di ricerca: difetti, ipotesi pre-registrabili, protocollo per gli agenti, opportunità (nota 08)

Nota di ricerca, 2026-11-10. Punto di vista: revisore metodologico (statistica, identificazione, falsificabilità, disegno della valutazione). Non è un capitolo di tesi. Le soglie numeriche proposte sono **decisioni da prendere**, non risultati: sono marcate [H] e vanno fissate da Dennis prima delle prove.

**Letto:** `tesi/DOMANDA_DI_RICERCA.md`, `tesi/DECISIONI.md`, `tesi/CALENDARIO.md`, `secondo_cervello/modelli/MAPPA_MODELLI_ANALISI.md`, `secondo_cervello/ricerche/reports/Lotti ideali partecipazione e digital twin.md`, note 02–07 di questa cartella (la nota 01 non era presente al momento della lettura). Delle note ho letto takeaway, inferenze e lacune; non tutte le sezioni "Cited Findings" per intero [L].

**Marche.** [V] verificato (qui: nel file del repo indicato, o su record/abstract in questa sessione); [S] secondario (citato da una nota senza riscontro qui); [I] inferenza mia; [H] ipotesi o soglia da fissare; [L] lacuna, o riferimento da manuale non riscontrato in sessione. Ogni fonte citata "da nota NN" eredita la marca della nota.

**Verifiche fatte in sessione (3 ricerche web):**
- Nguyen e Vohra, "Near-Feasible Stable Matchings with Couples", **American Economic Review 108(11), 2018, 3154–69**, DOI 10.1257/aer.20141188: con coppie la stabilità può mancare, ma esiste in un'istanza vicina con capacità perturbate (capacità aggregata mai ridotta, al più +4; ogni sede al più ±2) ([AEA](https://www.aeaweb.org/doi/10.1257/aer.20141188); [IDEAS](https://ideas.repec.org/a/aea/aecrev/v108y2018i11p3154-69.html)) [V, record]. Conferma la nota 02 §3.
- Stefanelli e Lukac, "Subjects, Trials, and Levels: Statistical Power in Conjoint Experiments" (SocArXiv 2020, DOI 10.31219/osf.io/spkcy): anche con campioni e numero di task relativamente grandi, i conjoint con molte condizioni e effetti piccoli non sono adatti all'inferenza; pacchetto R `cjsimPWR` per calcolare potenza ed errori di tipo S e M ([IDEAS](https://ideas.repec.org/p/osf/socarx/spkcy.html); [pagina autore](https://mblukac.github.io/portfolio/CJpoweranalysis)) [V, abstract/record]. Le regole pratiche attribuite al paper da fonti terze (es. AMCE mediano 0,05) **non** sono verificate [L].
- *Pattern-oriented modelling* (Grimm et al., *Science* 2005) come criterio di validazione multipla per ABM: il concetto è confermato da letteratura secondaria ([PLOS One, PMC3457952](https://pmc.ncbi.nlm.nih.gov/articles/PMC3457952)) [S]; il paper originale non è stato aperto [L].

---

## 1. I difetti metodologici più seri (11)

Ordinati per gravità. "Fatale" = se non corretto, la tesi non può sostenere la sua affermazione principale.

### D1. Il confronto "cooperativa contro developer" è vero per costruzione — **fatale**
**Che cosa.** La promessa centrale ("esiti più accessibili rispetto al modello guidato dai developer", `DOMANDA_DI_RICERCA.md`) sarà misurata con un motore di flussi di cassa in cui il canone a costo $R_t$ non contiene la rendita di mercato e il developer massimizza il valore residuo (nota 06 §2) [V nel file]. A parità di lotto, il divario è quasi interamente funzione del **costo del terreno** e del **margine richiesto** $\pi$, cioè di due parametri scelti dal ricercatore. Senza vincolo sul terreno, "la cooperativa è più accessibile" è una tautologia contabile, non una scoperta [I].
**Perché grave.** Un revisore leggerà il risultato come assunzione. Inoltre la nota 06 §3 mostra che un lotto sotto mercato non cambia i prezzi di città ma crea una **rendita di allocazione** per chi entra [S da nota 06]: "più accessibile" per 40 famiglie non è "più accessibile" per la pancia.
**Fix.** (a) Spostare l'ipotesi dal *segno* del divario al **prezzo del terreno di pareggio** $L^*_{coop}$ e al gap $\Delta_L = VRA^{dev}-L^*_{coop}$ (nota 06, formula 6): la domanda falsificabile diventa "per quale quota di lotti esiste un regime fondiario realistico (asta, diritto di superficie, cessione) in cui il canone obiettivo è sostenibile?". (b) Tarare il motore su casi reali prima di usarlo (VRA di un'area comunale venduta all'asta; canoni di una cooperativa a proprietà indivisa milanese; divario Zurigo), come già proposto in nota 06 [I]. (c) Riportare insieme al guadagno per gli ammessi una metrica di **targeting** (chi entra, rispetto alla popolazione bersaglio) — è il punto di Waldinger (AER 2021, scelta contro targeting) [V abstract, da report].

### D2. Circolarità della fase ad agenti — **fatale se non disegnata**
**Che cosa.** "Prima agenti, poi test reale" (`DECISIONI.md`). Se le famiglie simulate sono generate con le stesse funzioni di utilità, la stessa metrica di diversità e lo stesso catalogo di criteri usati dal meccanismo, la simulazione mostra solo che l'ottimizzatore ottimizza ciò che gli si dà [I]. Con agenti LLM la circolarità è peggiore: le note 05 §3 e il report documentano collasso della varianza, appiattimento dei gruppi identitari, inversione delle inferenze per sottogruppo (Bisbee et al. 2024; Wang, Morgenstern, Dickerson) [V/S da note], e **nessuna validazione su scelte residenziali né su famiglie italiane** [L da nota 05].
**Perché grave.** Il collasso della varianza fa sembrare facile proprio ciò che la tesi deve dimostrare difficile-ma-possibile: formare gruppi eterogenei e stabili [I].
**Fix.** Separazione generatore/valutatore (§3 sotto): popolazioni generate da processi **diversi** dal modello del meccanismo, metriche di valutazione distinte dall'obiettivo ottimizzato, test di recupero con verità nota, e LLM solo come stress-test, mai come stima di esigenze.

### D3. La metrica di successo coincide con la funzione obiettivo (Goodhart) — **grave**
**Che cosa.** "Più aderenti alle esigenze" rischia di essere misurato con l'utilità che il meccanismo stesso massimizza (pesi elicitati → punteggio dei lotti → soddisfazione = punteggio). La nota 07 §3 lo dice per l'RL: Zheng et al. "battono gli esperti sulle metriche del modello stesso" [V/I da nota 07].
**Fix.** Ogni ipotesi deve avere almeno una metrica **non ottimizzata** dal meccanismo: (i) rango del lotto assegnato in una preferenza raccolta **separatamente** e tenuta fuori dalla stima (*held-out*); (ii) deviazioni di stabilità (IS) misurate su preferenze di compatibilità non usate per formare i gruppi; (iii) RTI e reddito residuo calcolati con il paniere ISTAT, non con l'utilità.

### D4. La domanda non è identificata con i dati disponibili — **grave**
**Che cosa.** L'indice di domanda del Lab coincide con gli affitti (rho 0,987) [V, MAPPA]; la nota 05 §2 spiega perché è la tautologia dell'equilibrio: senza strumento per il prezzo, "domanda" = mappa dei canoni [I da nota 05]. Con un solo mercato e un solo periodo il secondo stadio BLP/BFM è fragile; il reddito per NIL manca (MEF per CAP) [I/L da nota 05]. Per la pancia milanese il budget è quasi sempre attivo: le localizzazioni osservate sono **esigenze adattate**, non preferenze [I da nota 05].
**Fix.** Rinunciare dichiaratamente alla stima strutturale piena. Usare: $\delta_j$ per zona solo se c'è variazione esogena (2011 contro 2021; aperture M4/M5 come esperimento naturale [H]); eterogeneità individuale **solo da preferenze dichiarate** (esperimento di scelta) in F2; test anti-artefatto della nota 05 come criteri di accettazione pre-registrati (H6 sotto).

### D5. Caso unico e unità di inferenza non definita — **grave**
**Che cosa.** "Un caso continuo" (Milano) e "il metodo è il contributo, il progetto ne è la prova" (`DECISIONI.md`). Un caso unico è una **dimostrazione di esistenza** (il metodo si può fare), non una prova di superiorità. Inoltre non è dichiarato su quale unità si fa inferenza: lotti (~2.291 siti candidati [V, MAPPA]), famiglie, gruppi, istanze simulate, o sessioni con persone.
**Fix.** Dichiarare due tipi di affermazione distinti: (a) **affermazioni di meccanismo** (proprietà dimostrate o misurate su molte istanze simulate: unità = istanza, con $R$ repliche, §3); (b) **affermazioni empiriche** (F2: unità = persona o gruppo, campione piccolo, solo stime d'effetto con intervalli, nessuna generalizzazione oltre il campione). Nella tesi le prime sono il contributo; le seconde sono una prova di fattibilità.

### D6. Giardino dei sentieri che si biforcano: troppi parametri del progettista — **grave**
**Che cosa.** Soglie del filtro dei lotti (≥300 m², verde, accorpamento), FAR, catalogo dei criteri, metrica di distanza del clustering, soglie di diversità $(\beta,\alpha)$, ordine di elaborazione delle riserve, regola di aggregazione dei pesi, parametri economici (6–8 secondo nota 06). Ognuno sposta l'esito. Il caso Hammersmith & Fulham mostra che il **filtro iniziale** può determinare il risultato più dei criteri pesati [S, report]; la nota 02 avverte che l'ordine delle riserve "è esso stesso un peso nascosto" [I da nota 02].
**Fix.** (a) Pre-registrazione dei valori di default e delle ipotesi (OSF o file datato nel repo con hash di commit). (b) **Analisi multiverso**: riportare la distribuzione dei risultati su tutta la griglia dichiarata, non il punto migliore. (c) Scomposizione della varianza dell'esito tra parametri del progettista e input dei partecipanti: è anche la misura operativa del "decisore nascosto" (H7).

### D7. "Diversità" rinviata, ma le ipotesi dipendono da essa — **grave**
**Che cosa.** `DECISIONI.md` rinvia l'operativizzazione della diversità. Ma la nota 07 §1 mostra che la scelta determina se il problema ha soluzione: con due tipi esiste sempre una partizione individualmente stabile calcolabile in tempo polinomiale; con tre o più tipi anche IS può mancare; per $k\ge5$ deciderlo è NP-completo [V da nota 07, Bredereck–Elkind–Igarashi; testo integrale non letto, L]. Diversità a più attributi (età × condizione × reddito) cade nel regime senza garanzie [I da nota 07].
**Fix.** Decidere **ora**, in F0, almeno la forma: un vincolo binario duro per volta (regime $k=2$, IS garantita) e le altre dimensioni come obiettivo morbido o soft bound [H, già in nota 07]. Misurare la stabilità invece di presupporla (quota di famiglie con una deviazione IS ammissibile).

### D8. Le preferenze di gruppo sui lotti non sono definite — **grave**
**Che cosa.** Nella pipeline a due stadi (gruppi, poi gruppi scelgono lotti; nota 02 §3) il gruppo diventa un agente con una preferenza sui lotti. Ma quella preferenza è un'**aggregazione interna** (scelta sociale dentro il gruppo), che può essere ciclica (Condorcet) o manipolabile; e i gruppi chiedono $k$ alloggi complementari nello stesso lotto, caso in cui la stabilità può non esistere [V, Nguyen–Vohra 2018, record]. Inoltre la formazione dei gruppi è **endogena** ai lotti disponibili: chi forma un gruppo senza sapere dove andrà decide su un oggetto diverso [I].
**Fix.** (a) Dichiarare la regola di aggregazione interna (es. Borda o mediana dei ranghi, pubblica). (b) Confrontare architettura a due stadi e congiunta (preferenze su coppie gruppo–lotto) almeno su istanze piccole. (c) Usare la flessibilità della densità come perturbazione di capacità alla Nguyen–Vohra e misurare quanto serve [H].

### D9. Il nesso causale "mediazione IA → esito" non è isolabile nel disegno attuale — **grave**
**Che cosa.** La domanda attribuisce gli esiti al "sistema cibernetico" (agenti + LLM + RL). Ma il sistema cambia contemporaneamente: meccanismo di allocazione, tenure economica, presenza della scelta, presenza del mediatore LLM. Confrontato con "il developer" come blocco unico, nessun effetto è attribuibile a nessuna componente [I].
**Fix.** Disegno **fattoriale ad ablazione**: tenure (developer/cooperativa) × allocazione (dall'alto MILP / casuale / scelta con DA o RSD) × mediazione (nessuna / regola fissa / LLM). In simulazione costa poco; in F2 si testa solo il fattore "mediazione" (randomizzato), gli altri restano simulati.

### D10. Prova reale (F2) sottodimensionata e non confrontabile con il controfattuale — **grave**
**Che cosa.** Tre mesi (mag–lug 2027, `CALENDARIO.md`), partner non scelto, comitato etico non menzionato. Le persone non "vivono" l'esito (né il lotto né il canone): si misura soddisfazione dichiarata verso un'allocazione ipotetica. Il bias ipotetico è documentato (Murphy et al., rapporto mediano 1,35 sulla WTP) [V abstract, da report]; l'autoselezione dei partecipanti è documentata nei processi partecipativi (Chicago PB) [S, report]. Stefanelli e Lukac mostrano che con molte condizioni ed effetti piccoli anche campioni grandi non bastano [V abstract].
**Fix.** (a) Ridurre F2 a **un solo contrasto randomizzato entro soggetto o entro gruppo** (es. mediazione LLM contro regola fissa pubblica, oppure scelta contro assegnazione) con outcome pre-registrati. (b) Calcolo di potenza prima del reclutamento (§3.5). (c) Campione a due canali: aperto + panel sorteggiato stratificato (report) [I]. (d) Avviare la richiesta al comitato etico in F0–F1, non in F2.

### D11. La seconda metà della domanda ("decisore nascosto") non ha un test — **serio**
**Che cosa.** "A quali condizioni la mediazione resta trasparente" è formulata come domanda aperta; nessuna metrica è definita. La nota 04 §3 conferma che metriche operative per un decisore nascosto **non sono standardizzate** [S da nota 04]. Sappiamo però che i sistemi di consenso dipendono da parametri dello sviluppatore (K di Polis, regolarizzazione di Community Notes, regola di voto della Habermas Machine) [S da nota 04], e che la Habermas Machine accresce il sostegno alla posizione maggioritaria [S].
**Fix.** Definire il decisore nascosto come **quota di varianza dell'esito spiegata da scelte non visibili o non modificabili dai partecipanti** (H7), più due metriche di deriva del mediatore: spostamento delle posizioni verso la proposta del mediatore non giustificato da nuove informazioni, e perdita di rappresentanza delle minoranze nei riassunti (H8).

### Difetti minori da tenere in lista
- **Validazione spaziale** dei descrittori dei lotti: CV casuale ottimista (Meyer e Pebesma 2022) [V, report]; il PU del Lab aveva PR-AUC gonfiata [V, MAPPA].
- **Equilibrio parziale**: gli spillover di vicinato possono superare l'effetto diretto e cambiano segno col reddito del quartiere (nota 06 §1, LIHTC) [S da nota 06]; nessuna evidenza causale europea su cooperative [L].
- **Molteplicità**: con 8+ ipotesi servono correzione (Holm o BH) o una gerarchia pre-registrata (ipotesi primaria unica + secondarie esplorative) [I].

---

## 2. Ipotesi operative pre-registrabili per la scala urbana

Convenzioni. $i$ famiglia, $g$ gruppo, $\ell$ lotto con capacità $q_\ell$, $\mu$ assegnazione prodotta da un meccanismo. $r_g(\ell)$ rango del lotto $\ell$ nella preferenza **held-out** del gruppo (1 = migliore). Ogni ipotesi è testata su $R$ istanze simulate (popolazioni generate come in §3) e, dove indicato, in F2. Le soglie tra parentesi quadre sono **proposte da fissare ex ante** [H]; i valori numerici sono ordini di grandezza ragionevoli, non derivati da fonti.

**Ipotesi primaria (una sola, per evitare la molteplicità):** H2. Le altre sono secondarie con correzione di Holm.

### H1 — Economia: esistenza di un regime fondiario sostenibile (cost-rent contro valore residuo)
- **Variabili.** Per lotto $\ell$: $VRA^{dev}_\ell$; prezzo del terreno di pareggio della cooperativa $L^*_{\ell}$ al canone obiettivo $\bar R$; reddito disponibile $Y$ del 3° quintile (pancia) per tipologia familiare $n$; paniere non abitativo $B^{nh}(n)$.
- **Metrica.** Gap fondiario e quota di lotti sostenibili:
$$\Delta_{L,\ell} = VRA^{dev}_\ell - L^*_\ell,\qquad S(\theta) = \frac{1}{|\mathcal L|}\sum_{\ell}\mathbb 1\!\left[\frac{R_\ell(\theta)+S_\ell}{Y_{Q3}}\le 0{,}30\ \wedge\ Y_{Q3}-(R_\ell+S_\ell)-B^{nh}(n)\ge 0\right]$$
con $\theta$ = regime fondiario ∈ {asta a VRA, diritto di superficie a canone ridotto, cessione}.
- **Baseline.** Lo stesso motore con regime developer (vendita/affitto a prezzi OMI) sugli stessi lotti.
- **Soglia ex ante.** H1 sostenuta se, nel regime "diritto di superficie", $S \ge$ [H: 0,25] e il risultato regge nel ≥ [H: 80%] della griglia di sensibilità sui 6–8 parametri della nota 06.
- **Falsificazione.** $S<$ soglia, oppure il motore non riproduce entro [H: ±20%] i tre casi di taratura (nota 06). Nota: con terreno a VRA di mercato **ci si attende** che la cooperativa non sia accessibile (H-a di nota 06): è un controllo di coerenza, non un risultato.

### H2 (primaria) — La scelta conta: matching con scelta contro allocazione dall'alto
- **Variabili.** Assegnazione gruppi–lotti con: (M1) accettazione differita con riserve e soft bounds (Ehlers et al.; Sönmez–Yenmez, nota 02 §2) [S da nota 02]; (M0a) MILP di portafoglio del Lab che massimizza un'utilità del pianificatore; (M0b) RSD con ordine casuale.
- **Metrica (non ottimizzata da M1).** Rango medio e quota top-3 su preferenze held-out:
$$\bar r(\mu)=\frac{1}{|G|}\sum_g r_g(\mu(g)),\qquad T_3(\mu)=\frac{1}{|G|}\sum_g \mathbb 1[r_g(\mu(g))\le 3],\qquad \Delta = \bar r(\mu_{M0a})-\bar r(\mu_{M1})$$
più l'invidia giustificata: $J(\mu)=\#\{(g,\ell): \ell \succ_g \mu(g)\ \wedge\ g \text{ ha priorità su qualcuno in } \ell\}$.
- **Baseline.** M0a (pianificatore) e M0b (casuale).
- **Soglia ex ante.** $\Delta>0$ con effetto standardizzato appaiato $d\ge$ [H: 0,2] e $J(\mu_{M1})=0$ per costruzione (verifica di correttezza dell'implementazione).
- **Falsificazione.** $\Delta\le 0$ o $d<$ soglia sull'intervallo di confidenza al 95%. Interpretazione onesta: se M0a vince sul rango, il guadagno della scelta stimato da Waldinger (>30% di benessere, [V abstract]) non si trasferisce a questo setting.

### H3 — Riserve contro quote rigide per la diversità
- **Variabili.** Tipo di famiglia $t\in\{m,M\}$ (minoranza rispetto a un attributo binario dichiarato, es. over-65 o monogenitore); politiche: quota massima per la maggioranza (Q) contro riserva per la minoranza (Rv) con DA.
- **Metrica.** Quota di famiglie di minoranza che stanno **peggio** sotto Q che sotto Rv:
$$W_m = \frac{1}{|I_m|}\sum_{i\in I_m}\mathbb 1\!\left[r_i(\mu_Q(i)) > r_i(\mu_{Rv}(i))\right]$$
- **Baseline.** DA senza vincoli.
- **Soglia ex ante.** $W_m >$ [H: 0,10] e nessuna famiglia di minoranza peggio sotto Rv rispetto a DA senza vincoli in più del [H: 5%] dei casi.
- **Falsificazione.** $W_m\le$ soglia. È il trasferimento al caso abitativo del risultato di Hafalir–Yenmez–Yildirim (fino al 25% delle minoranze peggio con quote, scuola) [V abstract, report]: il trasferimento stesso è [H].

### H4 — Diversità e stabilità dei gruppi (fair clustering + stabilità individuale)
- **Variabili.** Partizione $\pi$ delle famiglie in gruppi di dimensione $s$; vincolo di proporzione per tipo $(\beta_t,\alpha_t)$ (Bera et al., nota 07 §2) [S]; distanza costruita su **compatibilità** (orari, cura, competenze) e non su somiglianza (nota 07) [I].
- **Metriche.** Prezzo della diversità, tasso di deviazione IS, diversità di Simpson:
$$PoD(\beta)=\frac{\mathrm{cost}(\pi^*_\beta)}{\mathrm{cost}(\pi^*)},\quad \mathrm{IS\text{-}dev}(\pi)=\frac{1}{N}\sum_i \mathbb 1\!\left[\exists\, h:\ h\cup\{i\}\succ_i \pi(i)\ \wedge\ \forall j\in h:\ h\cup\{i\}\succeq_j h\right],\quad D_g = 1-\sum_t p_{g,t}^2$$
- **Baseline.** Clustering per somiglianza alla Housing Prime [V, scheda 09] e partizione casuale con gli stessi vincoli.
- **Soglia ex ante.** Con un vincolo binario duro ($k=2$): IS-dev $=0$ (garantito dalla teoria; è un test dell'implementazione). Con vincoli multi-attributo morbidi: IS-dev $\le$ [H: 0,10] e $PoD\le$ [H: 1,15] mentre $\bar D_g$ supera la baseline per somiglianza di almeno [H: 0,2].
- **Falsificazione.** IS-dev sopra soglia nel regime morbido sotto preferenze moderatamente omofile: la diversità imposta non tiene. È un risultato pubblicabile in sé (non esistono stime di PoD su dati abitativi [L, nota 07]).

### H5 — Aggregazione dei pesi dei criteri: proporzionalità e manipolabilità (MES / moving phantoms contro media)
- **Variabili.** Vettori di pesi individuali $w_i\in\Delta^{K-1}$ sui $K$ criteri dei lotti; regole: media aritmetica, mediana coordinata-per-coordinata normalizzata, *moving phantom* Independent Markets (Freeman et al., nota 03 §1) [S]; per l'approvazione di criteri da inserire nel catalogo: MES (Peters–Pierczyński–Skowron) [V abstract, report].
- **Metriche.** Guadagno da manipolazione e violazioni di proporzionalità:
$$\mathrm{Gain}_i = \max_{\tilde w_i}\ \big(\|w_i - F(w_{-i},w_i)\|_1 - \|w_i - F(w_{-i},\tilde w_i)\|_1\big),\qquad V_{JR}=\mathbb 1[\text{JR violata}]$$
e per gruppi coesi di quota $\rho$ la distanza tra la loro quota di peso e $\rho$.
- **Baseline.** Media aritmetica (usata dal Lab).
- **Soglia ex ante.** Con una minoranza polarizzata di quota [H: 0,2–0,3], la media mostra $\mathrm{Gain}>0$ per almeno [H: 50%] degli agenti strategici e la regola proporzionale riduce il gap di quota a $\le$ [H: 0,05]; la perdita di soddisfazione totale resta nell'ordine già osservato (0,05–0,08 per seq-PAV, [V nel file 07_azadi..., report]).
- **Falsificazione.** Nessuna differenza in quota rappresentata o in lotti selezionati tra media e regola proporzionale: allora la scelta della regola è irrilevante sul caso e si può usare la più spiegabile.

### H6 — La domanda non è un artefatto dei canoni (logica BLP/sorting)
- **Variabili.** Indice di domanda per NIL e per tipo di famiglia $D_{j,t}$; canone OMI $p_j$.
- **Metriche.**
$$\rho_S\big(D_{\cdot,t},\,p_{\cdot}\big)\ \ \forall t,\qquad W=\text{coefficiente di concordanza di Kendall tra le classifiche } \{D_{\cdot,t}\}_t$$
più l'errore di previsione fuori campione su scelte non usate in stima (traslochi successivi o scelte dichiarate F2).
- **Baseline.** Indice del Lab ($\rho=0{,}987$ [V, MAPPA]).
- **Soglia ex ante.** $|\rho_S|<$ [H: 0,8] (regola della nota 05) e $W<$ [H: 0,7] (i tipi di famiglia non hanno la stessa classifica); coefficiente di prezzo negativo e strumentato.
- **Falsificazione.** $|\rho_S|\ge 0{,}8$ o $W\ge 0{,}7$: l'indice non aggiunge informazione e va sostituito da preferenze dichiarate.

### H7 — Decisore nascosto: peso dei parametri del progettista
- **Variabili.** Esito $Y$ (es. $T_3$, $S$, $\bar D_g$); parametri del progettista $\Theta_D$ (soglie del filtro, metrica, ordine delle riserve, $K$ del clustering, prompt del mediatore); input dei partecipanti $\Theta_P$ (pesi, ranghi, soglie votate).
- **Metrica.** Indici di Sobol del primo ordine e totali per blocco:
$$H = \frac{\mathrm{Var}\big(E[Y\mid\Theta_D]\big)}{\mathrm{Var}(Y)},\qquad H^{T} = 1-\frac{\mathrm{Var}\big(E[Y\mid\Theta_P]\big)}{\mathrm{Var}(Y)}$$
- **Baseline.** Lab (pesi medi + filtro fisso), dove $\Theta_P$ ha poco peso [I].
- **Soglia ex ante.** Mediazione "trasparente" se $H^T\le$ [H: 0,3] e ogni componente di $\Theta_D$ con indice totale > [H: 0,05] è **pubblicata e votabile**.
- **Falsificazione.** $H^T>$ soglia: chi progetta decide più di chi partecipa, qualunque sia l'interfaccia.

### H8 — Deriva del mediatore LLM (solo F2 o simulazione dichiarata come tale)
- **Metriche.** Spostamento verso la proposta del mediatore e rappresentanza della minoranza nei riassunti:
$$\mathrm{Drift}=\frac{1}{N}\sum_i \big(\|x_i^{pre}-m\| - \|x_i^{post}-m\|\big),\qquad \mathrm{MinRep}=\frac{\text{quota di enunciati della minoranza nel riassunto}}{\text{quota della minoranza nell'input}}$$
- **Baseline.** Regola fissa pubblica (riassunto estrattivo o slate della generative social choice) e mediatore umano se disponibile.
- **Soglia ex ante.** $\mathrm{MinRep}\ge$ [H: 0,8] e Drift non superiore alla baseline oltre [H: 0,1 SD].
- **Falsificazione.** Drift significativamente maggiore della baseline senza aumento di informazione: il mediatore persuade. È coerente con l'evidenza sulla persuasione LLM (nota 04 §3) [S].

---

## 3. Protocollo di valutazione per la fase ad agenti (non circolare)

### 3.1 Principio: tre ruoli separati
1. **Generatore** delle popolazioni (chi sono le famiglie e che cosa vogliono).
2. **Meccanismo** (formazione dei gruppi, aggregazione, matching, economia).
3. **Valutatore** (metriche di §2).
Regola: il meccanismo non vede la "verità" del generatore se non tramite i segnali che vedrebbe da persone reali (risposte a domande, rango, pesi dichiarati con rumore). Il valutatore usa preferenze **held-out** generate dallo stesso stato latente ma non mostrate al meccanismo [I].

### 3.2 Quattro famiglie di generatori (non una)
| Generatore | Come | Uso | Rischio |
|---|---|---|---|
| G1 strutturale | popolazione sintetica (IPF da censimento 2021) + utilità mixed logit con parametri presi da letteratura dichiarata | caso base | eredita le assunzioni del ricercatore |
| G2 avversario | stessi individui con preferenze **diverse dal modello del meccanismo**: forte omofilia, minoranza polarizzata, preferenze lessicografiche, rumore elevato, risposte strategiche | robustezza | nessuno: è il test contro la circolarità |
| G3 recupero | parametri veri noti estratti a caso; si misura se l'elicitazione li recupera | validità dell'elicitazione | — |
| G4 LLM | agenti LLM condizionati su profili G1 | solo stress-test di interfaccia e negoziazione | collasso varianza, stereotipi (nota 05) |

**Criterio di validità del meccanismo** [I]: un risultato è accettato solo se regge su G1 **e** G2 (stesso segno, effetto sopra soglia). Un risultato che regge solo su G1 o solo su G4 è dichiarato "dipendente dal generatore". È l'idea della validazione per *pattern multipli* (pattern-oriented modelling, Grimm et al. 2005 [L, non aperto; concetto S]).

### 3.3 Che cosa si chiede agli agenti LLM, e come li si controlla
- Mai usati per stimare esigenze o pesi di popolazione (regola già in MAPPA e nota 05) [V nel file].
- **Test di fedeltà a livello di parametri, non di risposte** (nota 05 §3): far rispondere gli agenti LLM allo **stesso esperimento di scelta** che si userà in F2; stimare un MNL/mixed logit; confrontare con i parametri delle persone reali in F2 tramite test di equivalenza (TOST) con margine $\epsilon$ pre-registrato:
$$H_0:\ |\beta^{LLM}_k-\beta^{hum}_k|\ge\epsilon_k\quad\text{contro}\quad H_1:\ |\beta^{LLM}_k-\beta^{hum}_k|<\epsilon_k$$
più rapporto delle varianze delle classi latenti (collasso se $\hat\sigma^2_{LLM}/\hat\sigma^2_{hum}<$ [H: 0,5]).
- Prima di F2: controlli interni che non richiedono umani: sensibilità al prezzo (il coefficiente di canone deve essere negativo e non nullo), stabilità test–retest con seed diversi, invarianza all'ordine delle opzioni, risposta a profili controfattuali (cambiare solo il reddito deve cambiare le scelte nel verso atteso). Fallire uno di questi = agenti esclusi dalle prove sul meccanismo [H].
- Pre-registrare modello, versione, temperatura, prompt, numero di campioni; pubblicare i log.

### 3.4 Potenza e numero di repliche in simulazione
Per un confronto appaiato tra meccanismi sulla stessa istanza (stessa popolazione, stesso seed) con differenza standardizzata $d$, $\alpha=0{,}05$ bilaterale, potenza $1-\beta=0{,}8$ [formula standard, I]:
$$R \approx \left(\frac{z_{1-\alpha/2}+z_{1-\beta}}{d}\right)^2 = \frac{(1{,}96+0{,}84)^2}{d^2}\approx\frac{7{,}85}{d^2}$$
quindi $d=0{,}2\Rightarrow R\approx 197$; $d=0{,}1\Rightarrow R\approx 785$ repliche per cella [I, calcolo]. Con un disegno fattoriale (D9) e correzione di Holm su $m$ ipotesi secondarie si usa $\alpha/m$ nel caso peggiore. In simulazione $R=1.000$ per cella è in genere economico per matching e clustering su centinaia di famiglie [I]; non lo è con agenti LLM (costo per chiamata), dove si fissa $R$ a priori sul budget e si dichiara la $d$ minima rilevabile. Riportare sempre intervalli di confidenza, non solo p-value; con $R$ grande qualunque differenza diventa "significativa", quindi la soglia sostanziale (es. $d\ge0{,}2$) conta più del test [I].

### 3.5 Potenza per F2 (persone reali)
- **Contrasto randomizzato entro soggetto** (es. allocazione con scelta contro dall'alto, valutate dalla stessa persona): con $d=0{,}3$, $n\approx 7{,}85/0{,}09\approx 87$ persone [I, calcolo]. Fra soggetti servirebbero $n=2(z_{1-\alpha/2}+z_{1-\beta})^2/d^2\approx 15{,}7/0{,}09\approx 175$ persone per braccio con $d=0{,}3$ [I, calcolo]: il disegno entro soggetto è l'unico realistico.
- **Se l'unità è il gruppo** (deliberazione in gruppi di $m$ famiglie): effetto di disegno $DE = 1+(m-1)\,ICC$; con $m=5$ e ICC [H: 0,2], $DE=1{,}8$, quindi il campione efficace si quasi dimezza [I].
- **Conjoint per i pesi**: dimensionare con `cjsimPWR` (Stefanelli–Lukac) dato il numero di attributi e livelli; limitare attributi e livelli perché effetti piccoli con molte condizioni non sono stimabili [V abstract].
- Conclusione [I]: con le risorse realistiche di una tesi magistrale (un partner, tre mesi), F2 regge **un** contrasto primario entro soggetto e analisi descrittive per il resto. Va scritto così nella pre-registrazione.

### 3.6 Regole di condotta
- Pre-registrazione datata nel repo (ipotesi, metriche, soglie, generatori, seed, analisi) **prima** di eseguire le prove; deviazioni registrate in `giornale/`.
- Valutatore "cieco": lo script delle metriche è scritto e congelato prima di guardare i risultati dei meccanismi.
- Analisi multiverso sui parametri del progettista (D6) con grafico della distribuzione degli esiti.
- Le prove sono prove, non fonti (`CLAUDE.md`): ogni risultato ad agenti è una proprietà del sistema, non delle famiglie.

---

## 4. Le cinque opportunità più promettenti per un contributo originale (in ordine)

### O1. Matching gruppi–lotti con complementarità, riserve di diversità e densità flessibile
**Perché originale.** Nessun lavoro trovato unisce formazione di gruppi eterogenei e scelta di lotti [L, nota 02 §3]. Nguyen–Vohra garantiscono stabilità con capacità perturbate di poco [V, record AER 2018]; in edilizia la capacità di un lotto è flessibile (densità) e quindi la perturbazione è più plausibile che negli ospedali [H, nota 02]. Si combina con riserve e soft bounds (nota 02 §2).
**Esperimento minimo.** 1.000 istanze sintetiche (G1 + G2): 30–60 gruppi di 3–8 famiglie, 20–40 lotti; misurare (a) tasso di inesistenza di matching stabile senza perturbazione; (b) perturbazione media necessaria in alloggi per lotto; (c) H2 e H3 sulle stesse istanze. Pubblicabile come paper di market design applicato [I].

### O2. Il "prezzo della diversità" su una popolazione abitativa reale
**Perché originale.** Non esistono stime di PoD su dati abitativi o di popolazione [L, nota 07 §2]; la letteratura teorica dice dove la stabilità manca (k ≥ 3) ma non quanto costi in pratica [V/I, nota 07].
**Esperimento minimo.** Popolazione sintetica della pancia milanese (IPF, censimento 2021); tracciare le tre curve PoD, IS-dev, Simpson al variare di $\beta$ (H4), sotto preferenze da neutre a omofile. Un grafico, un risultato chiaro, un paper breve [I].

### O3. Mappa del gap fondiario $\Delta_L$ per particella, con motore tarato
**Perché originale.** Nessun confronto lotto per lotto developer contro cooperativa a proprietà indivisa trovato per una città italiana [L, note 06]; nessuna evidenza causale europea sulle cooperative [L]. Una mappa di $\Delta_L$ dice **dove** il terreno, non la forma giuridica, blocca l'accessibilità: è la leva politica (diritto di superficie, cattura del valore) [I].
**Esperimento minimo.** Motore unico a due regimi su 50–100 lotti del Lab; taratura sui tre casi della nota 06; output: distribuzione di $\Delta_L$ e quota $S(\theta)$ per regime fondiario, con analisi di sensibilità globale. Utile anche fuori dall'accademia [I].

### O4. Una misura operativa del "decisore nascosto" (Sobol sul blocco progettista contro partecipanti)
**Perché originale.** Metriche per il decisore nascosto non sono standardizzate [S, nota 04 §3]; i quadri di governance dei digital twin regolano i dati, non le assunzioni del modello [I, report]. H7 trasforma la seconda metà della domanda di ricerca in un numero confrontabile tra sistemi (Lab, sistema della tesi, Polis, mediatori LLM).
**Esperimento minimo.** Applicare l'analisi di Sobol a due pipeline (Lab originale e nuova pipeline con riserve e regola di aggregazione pubblica) sulle stesse istanze; mostrare che $H^T$ scende. Generalizzabile come strumento di audit [I].

### O5. Validazione di agenti LLM su scelte residenziali, a livello di parametri
**Perché originale.** Nessuna validazione di rispondenti LLM su scelte residenziali né su famiglie italiane [L, nota 05 §3]. Un confronto parametri LLM contro umani sullo stesso esperimento di scelta (TOST, varianza delle classi; §3.3) è un contributo metodologico autonomo, anche se l'esito è negativo.
**Esperimento minimo.** Un esperimento di scelta tra lotti ipotetici (4–5 attributi, budget esplicito) somministrato a un panel di persone in F2 e a agenti LLM condizionati sugli stessi profili; confronto di $\beta$, WTP relative e varianze. Rischio: dipende da F2 e dalla potenza (§3.5); per questo è quinta [I].

---

## Inferenze di sintesi
- [I] Il disegno ha già intuizioni giuste (linea di base obbligatoria, LLM non come evidenza, criteri pubblici). Il punto debole è che le promesse centrali ("più accessibile", "più aderente") sono oggi verificabili solo in forme tautologiche (D1, D3). La correzione non richiede nuovi dati: richiede di spostare le ipotesi su **condizioni** (quale terreno, quale soglia di diversità, quale regola) invece che su **segni**.
- [I] Il contributo più solido e più a basso rischio è nelle affermazioni di meccanismo in simulazione (O1, O2, O4); F2 va ridotta a un contrasto pulito.
- [H] Ipotesi primaria suggerita: H2. Ridurre il numero di ipotesi secondarie se il tempo stringe; H1, H4 e H7 sono le più legate alla domanda di ricerca.

## Lacune
- Nota 01 non letta (assente al momento della lettura).
- Testi integrali di Bredereck–Elkind–Igarashi, Bera et al., Ehlers et al., Freeman et al., Grimm et al. non letti: definizioni formali di IS, dei vincoli di proporzione e dei moving phantoms vanno riscontrate prima di citarle.
- Le soglie di §2 e §3 sono proposte metodologiche, non valori della letteratura: vanno discusse e fissate da Dennis.
- Nessuna verifica dei costi di calcolo reali (LLM, MILP) per dimensionare $R$.
