# Riesame critico di paper e review di Spatial Milano Lab (ticket #6)

Data: 2026-10-27. Tipo: lettura critica dei file, senza rieseguire il modello (23 minuti) e senza modificare gli originali.
Etichette: **[V]** verificato nei file (file e sezione indicati), **[I]** inferenza mia, **[H]** ipotesi da verificare. Le sigle dei file sono relative a `/mnt/project-files/spatial_milano_lab/lab/` (paper = `results/paper.md`, results = `results/results.md`, R1/R2 = `reviews/review1.md`/`review2.md`, A/B/C = `proposals/*/model.md` e `summary.md`).

## 0. Limiti di questo riesame

- **Letti per intero** [V]: paper, results, R1, R2, A/B/C (`model.md` di B solo fino al §4, `summary.md` di tutte e tre), `config.py`, `tests.py`, `parcels_schema.md`, il file di ripresa del 27/10, le due tavole rotonde del 27/10. Il `README.md` del lab l'ho letto in parte (regole e dati). Tutti i file erano leggibili.
- **Non letti**: i file di risultato citati ma non presenti nella cartella (`model.json`, `audit_*.csv`, `sensitivity.csv`, `portfolios.csv`, `tests.json`), il codice di `run.py`, `audit.py`, `portfolios.py`, `pu.py`, e `reports/Lotti per social housing partecipativo.md`. Le cifre sono quindi quelle riportate nei testi. Ho fatto solo controlli aritmetici sui testi (indicati dove usati).
- **Non verificato**: ogni fonte esterna (soglia ISTAT 1.256,37 €/mese, OMI, MEF, norme su ERP/ISEE, riferimenti bibliografici del paper). Non le cito come vere; segnalo solo come i file le trattano.
- Il testo del ticket #6 non l'ho letto: ho seguito la richiesta ricevuta.
- Il laboratorio è un unico lavoro di una sessione (tutti i file portano lo stesso mtime 27/10 19:45 [V, `ls -la`]), con revisori che sono altre istanze dello stesso sistema [I]: "revisione paritaria" non significa verifica indipendente da persone.

## 1. Verdetto generale

Il laboratorio è onesto sui propri limiti e le revisioni hanno ridimensionato bene le affermazioni, ma **nessuno dei risultati principali è una prova**. Quasi tutti sono o un artefatto di costruzione, o una stima su dati ecologici a risoluzione troppo bassa (reddito noto a 38 CAP, deprivazione letta a 88 NIL), o una conseguenza di assunzioni dichiarate non verificate (suolo ERP a 1 €/m², paniere 1,5×, FAR 1,0, σ = 0,5, quota affittuari 0,30). Il valore reale sta nei risultati *negativi* e nel metodo: i confronti con null appaiati, il null per blocchi di NIL, la scomposizione affitto/reddito.

## 2. Classificazione dei risultati principali

Legenda: **Evidenza** (regge entro i limiti dichiarati), **Artefatto** (prodotto dalla costruzione del modello o dei dati), **Ipotesi non testata** (plausibile, ma manca il test o il dato).

| # | Risultato | Classe | Sintesi del motivo |
|---|---|---|---|
| 1 | PR-AUC 0,93 casuale contro 0,33 a blocchi di 4 km | **Evidenza** (solo che la CV casuale è ottimista) e **ipotesi non testata** (che il rilevatore serva) | Il rilevatore non entra nel modello integrato; 0,33 è ancora gonfiato; il modello principale fa 0,099 |
| 2 | Domanda stimata = affitti, rho = 0,987, "artefatto di risoluzione" | **Artefatto** (la coincidenza); causa "risoluzione" = **ipotesi non testata** | Il difetto è confermato e non rimosso; l'attribuzione alla risoluzione non è isolata |
| 3a | PGT contro persone: AT, segregazione ("risk") | **Artefatto** (rumore Monte Carlo ed effetto meccanico) | 11 semi su 20, 2 punti su 14, 0,4% del DI, dipende da σ |
| 3b | AT, collocazione in NIL più poveri | **Ipotesi non testata** | Significativa solo col null di sito, noto anti-conservativo; sensibile alla specificazione |
| 3c | ERP "potential" | **Artefatto** (contabile) | Dipende dal suolo a 1 €/m², proprietà non verificata |
| 3d | AMB_DEG "neither" | **Nessuna informazione** (5 siti) | Assenza di potenza, non assenza di effetto |
| 3e | RIG, segnale di collocazione più robusto | **Evidenza descrittiva debole**, non prova di rischio | Zona, non sito; niente null per blocchi; indici instabili tra versioni |
| 3f | Persone contro PGT +48% / +22% / +5% | **Artefatto** per +48%; **evidenza** che il vantaggio sparisce a parità di bacino | A parità di anello il PGT sta dentro l'intervallo dei bacini casuali |
| 4 | Portafogli P1-P6 equivalenti | **Evidenza parziale** (piattezza dell'ottimo sulle famiglie servite), **artefatto** in parte (saturazione, paniere, prefiltro) | Equivalenti sul numero servito, non sui siti; vincolo Gini non vincolante |
| 5 | Dipendenza dal NIL Stephenson | **Artefatto di dato** (CAP imputato) | Gestito con una soglia post hoc; la lettura "dipende da un solo NIL" è superata |
| 6 | Preferenze sintetiche (archetipi, TV, teach-back) | **Ipotesi non testata** (sui cittadini); evidenza solo di coerenza interna | Nessun dato umano |

## 3. Analisi per risultato

### 3.1 PR-AUC 0,93 (CV casuale) contro 0,33 (blocchi di 4 km)

**Cosa dicono i file**
- [V, C model.md §2 tabella] "random K-fold, all features" PR-AUC 0,928; "block 4 km, all features" 0,326; "block 2 km" 0,363; modello principale (fisico + contesto) a blocchi di 4 km **0,099**, ROC 0,737, recall@10% 0,501; regola `soft_site` 0,015 con tasso di base 0,0128.
- [V, C §2] Il numero riguarda il **rilevatore PU di "somiglianza con i siti designati"**, non l'audit PGT. [V, results §8 limite 8] Il punteggio PU "non è usato da nessuna parte" nel modello integrato. [V, tavola "sui testi" §2.6] La stessa correzione era già stata fatta.
- [V, ripresa §3] Il file di ripresa riporta "Validazione: PR-AUC 0,93 con validazione casuale, 0,33 con blocchi di 4 km" tra i "risultati principali" senza dire che è il rilevatore C.

**Cosa regge**
- [V] La caduta 0,93 → 0,33 è una dimostrazione corretta di dipendenza spaziale: il testo di C la presenta come tale ("a random-CV figure would be dishonest").
- [V, C §2] Etichette: 1.440 particelle ma circa 83 oggetti di pianificazione, SCAR violata (c da 0,055 a 0,512), Brier uguale a quello del predittore costante (0,0126), Moran dei residui 0,738. C dichiara tutto questo.

**Cosa non regge**
- [V] La riga 0,326 usa "all features", che include DUSAF 2024 (scartato da C stessa come "post-designation leakage") e le variabili socio-economiche dei NIL (scartate perché copiano "chi abita lì"). Il confronto onesto del modello presentabile è 0,099 contro il tasso di base 0,0128, cioè 7,7 volte il caso, su circa 83 oggetti, senza intervalli di confidenza [V, nessun IC nei testi]. [I] Il "0,93 contro 0,33" accosta due numeri entrambi contaminati da variabili che C esclude dal modello principale.
- [V, R1 §7] Revisione 1 ha rieseguito solo `regions.py`; `pu.py` e `access.py` "not re-run", numeri confrontati solo con i file committati. [I] Quindi nessun controllo indipendente del 0,93/0,33.
- [V, R1 §3 punto 2; C model.md §3 e summary.md] Moran globale: i documenti dicono 0,406, il file di risultato e la riesecuzione di R1 dicono 0,57. R1 ha chiesto di correggere (F-C2). **Nei file attuali `summary.md` e `model.md` di C riportano ancora 0,406** [V, grep]. Nessun file spiega quale sia giusto [V].
- [V, C §2] "La regola `soft_site` è pari al caso" vale rispetto alle etichette di pianificazione (83 oggetti), non rispetto al potenziale reale di un lotto [I]. "Non ritrova ciò che i pianificatori hanno designato" non equivale a "non trova lotti adatti".

**Per farne una prova**
- Dati: una verità esterna al piano (proprietà, vincoli, bonifiche, esiti di gare) invece delle designazioni come etichette.
- Test: IC per blocchi (bootstrap sui blocchi), più dimensioni di blocco, risultati per oggetto e non per particella, confronto con la baseline con le stesse feature senza dati socio-economici.
- Ipotesi falsificabile [H]: "con feature solo fisiche e di contesto, la recall@10% a blocchi di 4 km supera 0,30 su tutti i blocchi esterni" (il valore 0,30 è una mia proposta, da fissare prima con un calcolo di potenza).

### 3.2 Domanda stimata = affitti (rho = 0,987), "artefatto di risoluzione"

**Cosa dicono i file**
- [V, R1 §1 difetto 1] Spearman 0,987 tra tasso di domanda per NIL e affitto OMI nella proposta A; con la quota di poveri −0,385. Attribuzione: reddito risolto a 38 CAP, affitto a 88 NIL.
- [V, paper §4.1 e results §4] Nel modello integrato: Spearman(tasso target, OMI) = **0,939**; quota della varianza tra NIL rimasta con affitti equalizzati **0,007**; ricerca in tutta la città: **14 famiglie contro 9.750**; con affitto mediano ovunque 6.531.
- [V, A summary] "Demand is concentrated in central and semi-central NIL... The indicator therefore measures displacement pressure"; la domanda è all'85% nei 20 NIL più cari.

**Valutazione**
- **Artefatto: sì, e non rimosso.** [V] La scomposizione richiesta da R1 (F-A1) è stata fatta e ha *confermato* il difetto: 99,3% della varianza tra NIL è affitto. Paper §5.1 scrive "La correzione è la decomposizione", ma una scomposizione è una diagnosi, non una correzione [I]. La domanda D_tau resta una mappa degli affitti (0,939).
- **Una parte è definitoria, non solo di risoluzione** [I]. Il test è `affitto > τ · reddito`: dove l'affitto varia di un fattore ~3 tra NIL (8-25,8 €/m²/mese [V, schema, `nil_rent` min/max]) e il reddito attribuito al NIL è mediato da pochi CAP, l'affitto domina. Con reddito osservato a risoluzione fine l'affitto resterebbe comunque un fattore forte. Dire che è "per artefatto di risoluzione" è [H]: nessuna corsa con reddito più fine esiste nei file.
- **La domanda D_res_decent (quella dei portafogli) non ha la stessa scomposizione.** [V] results §4 riporta la scomposizione per "target rate" senza dire per quale strato; per D_res_decent non c'è. [V, A summary "Localizzazione"] Anche il residuo a reddito è all'85% nei 20 NIL più cari. [I] I portafogli ereditano probabilmente la mappa degli affitti, e il prefiltro "8 siti più economici per NIL" [V, config `k_per_nil`] la rinforza.
- **"Pressione da espulsione" non è supportata** [V, R1]; A la riporta ancora nel summary (non corretto) [V, A summary Demand].
- **Il risultato "la pancia è sovraccarico da affitto, non povertà" dipende da due assunzioni** [I]: (a) la proxy ISEE ≤ 16.000 € con patrimonio = 0 e deduzione piena dell'affitto dichiara "idonee ERP" il 46% delle famiglie (un limite superiore, A §7 punto 1: "about 46%"; R1 difetto 2: "fragile, ×2,6 senza deduzione"); chi sarebbe povero materialmente viene tolto dalla domanda perché classificato ERP; (b) il paniere ISTAT è fissato al 60% della soglia, quota "da verificare" [V, paper §3.1; A summary]. Il "102 famiglie" nasce da questa combinazione.
- **Numeri non riconciliati** [V]: D_tau media 9.259 (paper Tab. 2, 20 scenari) contro 9.750 (baseline della variante di ricerca, §4.1) contro 10.503 (A, 40 scenari, R1 tabella "Reproduced"). D_res_decent 2.274 contro 2.067 (A summary); D_res_istat 102 contro 103. Le differenze sono verosimilmente scenari e semi diversi [I], ma nessun file lo spiega.

**Per farne una prova**
- Dati: reddito a sezione di censimento o ISEE aggregato per sezione con celle minime; tenure dal Censimento 2021 al posto di θ = 0,30 piatto [V, R1 difetto 4, paper §8]; contratti in essere (la proxy misura l'accesso a un affitto di mercato, non lo sfratto).
- Test: stessa scomposizione per D_res_decent; ripetere con reddito risolto a livello fine; sensibilità alla proxy ERP (con patrimonio > 0).
- Ipotesi falsificabile [H]: "con reddito a sezione, la quota di varianza tra NIL spiegata dal reddito sale sopra 0,25". Se resta sotto, la domanda è una funzione dell'affitto per costruzione. Soglia da fissare prima con una simulazione.

### 3.3 PGT contro persone

#### 3.3a AT, segregazione (etichetta "risk"): artefatto

- [V, results §1] Etichetta pre-registrata "risk" con dDI q = 0,029 / 0,030, ma ΔDI = −0,00052 contro −0,00085 / −0,00083: AT **riduce** la segregazione, di 0,00033 punti di DI in meno delle alternative, cioè 0,4% del DI di base 0,087 [V, R2 Issue 3].
- [V, R2 Issue 3; results §6] L'etichetta compare in 11 semi su 20 e in 2 punti su 14 della griglia (stabilità 0,14); col null per blocchi di NIL dDI p = 0,103 / 0,102 (AT in 12 NIL, 7,5 effettivi).
- [V, results §6 e config] ΔDI dipende da σ rispetto alla quota ERP simulata 0,463: con σ = 0,3 p ≈ 1,0; con σ = 1,0 etichetta "risk". [I] ΔDI è in larga parte una funzione meccanica di dove cade la capacità e di σ, non una misura indipendente. Il paper lo ammette in parte (limite 2).
- [V, R2 Issue 3] DI di base 0,0872 [I]: un indice di dissimilarità così basso è l'effetto della lisciatura a 38 CAP; la segregazione residenziale misurata su sezioni sarebbe verosimilmente più alta [H].
- [V, tests.py 1c, paper §4.5] Con insiemi concentrati in 3 NIL il null di sito (quello su cui si basa la regola pre-registrata) dà il **23,8%** di falsi positivi. [V] Il test 1c è segnato PASS perché il criterio riguarda il null per blocchi (0,3%), non il null della regola. [I] Per AT (12 NIL) il tasso di falsi positivi del null di sito non è quantificato.
- [I] La modifica della famiglia BH da 3 a 4 insiemi (aggiunta di RIG) ha abbassato i q di AT (dDI da 0,040/0,036 [R2 tabella finale] a 0,029/0,030 [results]); BH diventa più indulgente con molti p piccoli nella famiglia, e RIG ne porta molti (p = 0,001). Il cambio è dichiarato ma **favorisce** l'etichetta "risk".

#### 3.3b AT, collocazione in NIL più poveri: ipotesi non testata

- [V, results §1] Reddito residuo −92 €/mese contro −22 / −38 (p = 0,003 / 0,012 col null di sito); 41% in NIL del quintile ERP superiore contro 18%. Col null per blocchi: dep_resid p = 0,067 / 0,095; conc_q5 p = 0,092 / 0,198; dep_poor 0,241 / 0,275. **Nessun indice è significativo a 0,05** [V].
- **Sensibilità alla specificazione** [V]: lo stesso indice conc_q5 col null per blocchi era p = 0,011 / 0,023 in R2 (prima della ridefinizione sul solo p_erp e della soglia di 500 famiglie) e 0,092 / 0,198 in results. dep_resid era 0,015 / 0,014 e ora 0,067 / 0,095. La conclusione di R2 "la collocazione regge col null per blocchi (p ≈ 0,015)" è **superata dai suoi stessi numeri successivi** ma resta nella tabella finale di R2 [V, R2 "Final verdict per designated set"].
- [V, results §3 "AT variants"] Senza soglia: p = 0,001 su dep_poor, dep_resid, conc_q5; con soglia di 500 famiglie: 0,026 / 0,003 / 0,001. [I] La soglia è una scelta post hoc e arbitraria (500) che sposta i risultati di un ordine di grandezza.
- [I] I cinque indici (dDI, dIso, dep_poor, dep_resid, conc_q5) derivano dallo stesso reddito per CAP: "un solo segnale ecologico" [V, results §1 caveat; R2 Issue 4.3]. Nessuna delle sei forme di p è corroborazione indipendente.
- [V, results §3] L'indice di opportunità non distingue AT dal null (0,580 contro 0,584 / 0,595).
- Effetto piccolo: +1,0 punto percentuale di contribuenti poveri contro un intervallo interquartile tra NIL di circa 4 punti (`nil_poor` p25 26,94, p75 31,08 [V, schema]) [I].

#### 3.3c ERP "potential": artefatto contabile

- [V, results §1, R2 Issue 7a] L'etichetta nasce dal suolo `srv_erp` a 1 €/m² (costo fisso medio per alloggio 1.785 € contro 65.518 € per SOFT). A costo di mercato: 1,32 famiglie servite per M€ contro mediana nulla 1,58 / 1,39: "neither". In assoluto servono meno famiglie: 1.729 contro 2.254 / 1.921.
- [V, paper §8, results §1] "Designation is not ownership": la proprietà non è verificata.
- [V, results §6] La griglia di sensibilità non contiene i parametri di costo né il regime del suolo; l'etichetta ERP risulta "stabile" 14 punti su 14 [V, results §6], ma la stabilità è vuota rispetto all'unica assunzione che la determina [V, tavola "sui testi" §2.4, confermata da `config.SENS`].
- [I] La regola "potential" richiede solo che due indici siano ≥ alla mediana del null in entrambi i null: senza test di significatività (a differenza di "risk"). Sotto H0 ogni condizione è vera circa metà delle volte; l'etichetta è quindi asimmetricamente facile da ottenere.
- [V, results §3] conc_q5 per ERP era in parte tautologico (srv_erp definiva il quintile); corretto. Collocazione in NIL più poveri: p di sito 0,006 / 0,010; per blocchi 0,076 / 0,151.

#### 3.3d AMB_DEG: nessuna informazione

- [V] 5 siti, 5 NIL (3,7 effettivi), 348 alloggi. Il paper dice "nessuna informazione" (Tab. 4). L'etichetta "neither" nella griglia è "stabile" (1,00) [V, results §6]: **stabilità di un risultato vuoto**; [I] va letta come assenza di potenza.

#### 3.3e RIG: evidenza descrittiva debole

- [V, results §3] +0,97 punti di poveri contro +0,22; −68 €/mese contro −16; p = 0,001 su 53 NIL (26,6 effettivi), per i null di sito.
- **Manca il null per blocchi per RIG** [V, results §3 tabella "Robustness": solo AT, AMB_DEG, ERP]. Il paper stesso mostra che il null di sito è anti-conservativo con insiemi raggruppati (§4.5). [I] Con 26,6 NIL effettivi il rischio è minore ma non quantificato.
- [V, C §2] `rig` è "una politica di zona di 36,8 km²", "label a zone, not a site", 34,5 km² su suolo già urbanizzato. [I] Dire che un'intera zona di rigenerazione sta in NIL più poveri è un fatto geografico descrittivo, non una proprietà di siti di housing sociale. R1 §6 lo mostra con una tabella semplice [V]: rig zone % poor 30,3 contro 29,7 sul totale, netto 1.888 contro 2.086 €/mese.
- **Instabilità tra versioni** [V]: R2 riporta RIG a +1,25 contro 0,59 e −78 contro −30 con conc_q5 non significativo (p = 0,05); results riporta +0,97 / 0,22, −68 / −16 e conc_q5 p = 0,001 (0,319 contro 0,181). Un indice è passato da non significativo a p = 0,001 per ridefinizione.
- [V, paper §4.4] "Ogni indice di collocazione e di segregazione ha p = 0,001" è inesatto: l'indice di opportunità ha p = 0,998 (size) e 0,956 (ring) [V, results §3 tabella RIG].
- Il paper stesso dice "contesto, non verdetto" [V]; l'etichetta "il segnale più robusto dello studio" confronta segnali tutti deboli [I].

#### 3.3f Persone contro PGT: +48% / +22% / +5%

- [V, results §5; controllo aritmetico mio] 1.731/1.166 = +48%; 1.425/1.166 = +22%; 1.225/1.166 = +5%.
- [V, R2 Issue 5] Il +43% (poi +48% a 300 s) confronta un bacino di 150 siti / 16.226 alloggi in 36 NIL con uno di 620 siti / 47.234 alloggi in 82 NIL. Il +48% è dunque in gran parte effetto di dimensione del bacino.
- [V] A parità di dimensione e anello il PGT (1.166) sta **dentro** l'intervallo dei bacini casuali (1.124-1.317) e ne batte 2 su 6. [I] Il +5% non è distinguibile da zero con 6 estrazioni; nessun IC nei testi. Il +22% si appoggia anch'esso a 6 estrazioni (intervallo 1.303-1.536).
- **Asimmetrie residue** [V, config `k_per_nil`]: il bacino PGT include "tutti gli ERP" e gli altri siti sono limitati agli 8 più economici per NIL; il bacino PGT beneficia del suolo gratuito ERP (che il paper ritiene non verificato). [I] Entrambe le asimmetrie spostano il risultato in direzioni opposte; l'effetto netto non è misurato.
- Cosa regge [V, paper §4.4]: la tesi "lo svantaggio del PGT è soprattutto scarsità e perifericità del suolo, non siti peggiori" è coerente con i numeri, ma "perifericità" è letta tramite l'anello euclideo dal centro, non tramite la qualità del sito [I].
- Incoerenza [V]: paper §4.4 dice +22%, paper §5.2 e R2 dicono +21%; R2 usa 8 estrazioni (media 1.413), paper/results/config ne usano 6 (media 1.425).

### 3.4 Portafogli P1-P6 equivalenti

**Cosa regge** [V, results §5]: tutti ottimi certificati (gap massimo 0,004), famiglie servite 1.781-1.795 (spread 0,8%); quota designata 0,29-0,33.

**Cosa non regge o va qualificato**
- **Equivalenza sul numero servito, non sulla scelta dei siti.** [V, paper §3.5] I tagli di diversità impongono al massimo il 70% di siti in comune: la diversità dei siti è per costruzione. [V] La domanda aperta, se i pesi dei cittadini cambino il portafoglio, non è misurata: i pesi non entrano nell'obiettivo del MILP (obiettivo = (1−β)·media + β·CVaR di famiglie servite [V, config `PORT`]); L_smaa è l'unica lente che li usa e serve il 30% in meno di P1 (1.249/1.795 = 0,696, mio calcolo) [V, results §5].
- **Saturazione.** [V, results §8 limite 7; paper §4.3] Famiglie servite per euro "saturano"; CVaR20 è circa 654 per tutti i portafogli non PGT (identico a tre cifre in P1-P6 e L_people [V, tabella]). [I] Un CVaR identico indica che il caso peggiore è determinato dalla domanda degli scenari bassi, non dalla scelta dei siti: l'obiettivo discrimina poco, e l'"equivalenza" è in parte piattezza dell'obiettivo.
- **Il paniere decide tutto.** [V, config `decent_mult=1.5` [A], commento "coordinator: D_res_decent"; results §4] Con il paniere ISTAT puro D = 102, con 1,5× D = 2.274; è lo strato servito. [I] Il moltiplicatore 1,5 è l'unica scelta che rende la domanda non vuota; è una scelta normativa/ad hoc, non un dato. [V, results §6] Con basket 0,85 la sovrapposizione di P1 col caso base è **0,22**; con 1,15 è 0,78. Il paper commenta la stabilità del Kendall τ (0,98) ma non questo.
- **Rumore di soluzione dello stesso ordine della sensibilità.** [V, results §6] Con τ = 0,25 e τ = 0,35, parametri che [V, results §6 nota] non possono cambiare ΔDI e [I] non dovrebbero cambiare lo strato D_res_decent, la sovrapposizione di P1 è comunque 0,64. [I] Un 36% di variazione senza causa è il pavimento di rumore (solver a 20 s, 8 scenari, semi) oppure τ agisce su qualche parte non dichiarata; la griglia usa impostazioni più economiche del caso base, quindi confonde i due effetti [V, results §6 "cheaper than the base run"].
- **"L'equità è quasi gratuita"** (paper §4.3: L_gini serve quanto P1). [V] P1 ha già Gini 0,056 e il vincolo è ≤ 0,10 [V, config `PORT["gini"]`]: il vincolo **non è vincolante**, quindi l'enunciato è vuoto. In A il passaggio da Gini 0,29 a 0,08 costava 3,5% [V, A summary].
- **Classifica SMAA dei portafogli** [V]: P(top-3) varia tra 0,00 e 0,61 tra portafogli che servono lo stesso numero di famiglie; i valori sono cambiati tra R2 (P5 0,45, P6 0,59) e results (P4 0,59, P6 0,05). Il paper la definisce "indicativa" [V]; [I] è piuttosto non interpretabile.
- **Il prefiltro** [V, config] tiene gli 8 siti più economici per NIL (e tutti gli ERP): le alternative sono scelte da un sottoinsieme già orientato al costo.

**Per farne una prova**
- Dati: costi reali di costruzione e suolo per area; proprietà.
- Test: griglia su c_build, land_inc, c_demo, yield, FAR e regime del suolo [V, tavola "sui testi" §5 intervento 3]; rumore di riferimento (stesso input, semi diversi); pesi agli estremi del simplesso con indice di Jaccard sui siti; riscrittura dell'obiettivo con pesi.
- Ipotesi falsificabile [H]: "variando i pesi tra estremi del simplesso, il Jaccard mediano dei siti scende sotto 0,7 a parità di famiglie servite entro il 2%". Se resta alto, la scelta tra portafogli è apparente.

### 3.5 Dipendenza dal NIL Stephenson

- [V, R2 Issue 3] Stephenson: 92 famiglie (172 abitanti), riceve 1.641 alloggi AT (17,9 volte lo stock; 1.641/17,9 = 91,7, mio controllo), eredita dal CAP 20157 un 40,57% di poveri, il massimo cittadino (coincide con il massimo di `nil_poor` nello schema [V]). Quattro NIL tengono il 67% della capacità AT: Lodi-Corvetto 2.056, Bovisa 1.808, Stephenson 1.641, Forze Armate 1.440 (somma 6.945 su 10.338 = 67,2%, mio controllo).
- **Artefatto di dato**: la deprivazione di Stephenson descrive il CAP, non il luogo. [V, R2 Issue 7c] Sei NIL hanno meno di 130 famiglie; in tre il 40,57% di poveri è copiato dal CAP.
- **Il rimedio è post hoc e arbitrario** [V, config `hh_floor=500`]: i NIL con meno di 500 famiglie prendono la media cittadina. Non è detto quanti NIL tocchi la soglia [V, nessun file].
- **La lettura "dipende molto da un solo NIL" è superata dai numeri finali** [V, results §3 "AT variants"]: senza i siti di Stephenson (con soglia) i p di sito per dep_poor sono 0,009 / 0,055 (con Stephenson 0,026 / 0,047), dep_resid 0,002 / 0,023, conc_q5 0,001 / 0,001; col null per blocchi dep_resid 0,046 / 0,064 e conc_q5 0,047 / 0,086 (con Stephenson 0,067 / 0,095 e 0,092 / 0,198). Togliendo Stephenson il segnale di collocazione col null per blocchi **si rafforza** (per l'effetto di diluizione della soglia) e col null di sito è misto (size più forte, ring un poco più debole: dep_poor ring 0,055 contro 0,047, dep_resid ring 0,023 contro 0,012); il segnale di segregazione si indebolisce (dDI p 0,035 / 0,037 contro 0,011 / 0,010; per blocchi 0,164 / 0,141 contro 0,103 / 0,102). Quindi nessuna direzione univoca: "dipende da Stephenson" non è dimostrato né smentito. [I] Il file di ripresa e le conclusioni di R2 ("rests heavily on Stephenson") descrivono la versione precedente alla soglia [V, ripresa §3; R2 verdetto AT].
- Il test leave-one-NIL-out di R2 (Corvetto, Bovisa, Forze Armate, Stephenson) è stato fatto prima della soglia [V, R2 Issue 3] e non risulta ripetuto [V, nessun file]. [I] La dipendenza dai quattro NIL (67%) resta il problema vero.
- [H] Lo stesso vale per il paper: "Stephenson è neutralizzato dalla soglia" [V, results §1] è vero per costruzione, ma non rende vera la collocazione.

**Per farne una prova**
- Dati: reddito a sezione o per esagono osservato; elenco dei NIL con meno di 500 famiglie e loro capacità in ogni insieme.
- Test: leave-one-NIL-out e leave-one-CAP-out sulla specificazione finale; analisi di soglia (200, 500, 1.000) come curva, non come singolo valore.
- Ipotesi falsificabile [H]: "togliendo ciascuno dei quattro NIL maggiori, dep_resid per blocchi resta sotto 0,10". Da fissare prima.

### 3.6 Preferenze sintetiche

- [V, B summary; paper §2 Tab. 1, §6.3] Archetipi, rispondenti simulati e minoranza polarizzata sono **sintetici**; "nessun numero descrive cittadini reali".
- **Evidenza di coerenza interna soltanto.** [V, tests.py 3] TV media 0,136 (massimo 0,182) contro soglia 0,15 con 8 rispondenti simulati, 9 criteri, 25 domande. [I] Con 8 ripetizioni e la media a 0,136 contro una soglia 0,15, il margine è sottile e la soglia non ha giustificazione empirica. Il rispondente simulato usa lo stesso tipo di verosimiglianza logistica del recuperatore (β = 50 contro 15 [V, tests.py]): il test non misura l'errore di specificazione umana.
- [V, paper §4.2] Il prototipo web: TV da 0,287 (prior) a 0,183 con la scorciatoia di ricampionamento: il paper dice che è "peggiore del motore Python" ed è fatto "per spiegare, non per stimare".
- **Incoerenze interne** [V]: (a) paper §3.4 dice che B campiona con MH su 3.000 particelle; B model.md §3 parla di 2.000 particelle con resample-move, B summary dice che la dimensione non è stata verificata, e solo `tests.py` usa 3.000. (b) Esempio di teach-back: B summary "5,1% → 12,8%", B model.md "11,5% → 12,2%": R1 l'ha segnalato (§2 punto 6) e non è stato corretto.
- [V, paper §3.3] I nove criteri, i vincoli κ, τ, paniere e budget sono scelti dagli autori; ai cittadini restano i pesi. [I] Vale il rischio di cooptazione già indicato dalle tavole rotonde: la definizione di bisogno (9.259 / 2.274 / 102) pesa più dei pesi [V, tavola "sui testi" §3 punto 8].
- Il prior di popolazione peggiora la stima per la minoranza (TV 0,212 → 0,232) [V, B summary E3]: [I] differenza dentro la soglia di rumore che B stessa indica (0,03) [V, B summary "Limits"].

**Per farne una prova**
- Dati: preferenze dichiarate di un campione stratificato (inquilini di mercato, graduatoria, stranieri), con numerosità giustificata da un calcolo di potenza.
- Test: test-retest dei pesi; confronto tra pesi elicitati e archetipi; verifica che criteri proposti dai partecipanti coincidano o no con i nove.
- Ipotesi falsificabile [H]: "i pesi osservati cadono nella regione che contiene il 90% dei pesi simulati dagli archetipi" (da [V, tavola 1 §2 intervento 6], soglie [H]).

## 4. Elenco delle incoerenze interne

Raggruppate per tipo. Ognuna è verificata nei file indicati [V].

**Tra paper, results e review**
1. **Etichette "ribaltate"** [V]: l'abstract del paper dice che le revisioni "hanno ribaltato due delle tre etichette"; ma results §1 e Tab. 4 mantengono "risk", "potential", "neither". Sono cambiate le affermazioni difendibili, non le etichette.
2. **R2 "Final verdict" contro results** [V]: R2 AT −150 contro −45 €/mese, 82% contro 49%, collocazione che regge col null per blocchi (p ≈ 0,015 e 0,01-0,02). Results: −92 contro −22 / −38, 41% contro 18%, p per blocchi 0,067 / 0,095 e 0,092 / 0,198. Il paper §5.2 spiega "dopo le correzioni", ma R2 non è stata aggiornata.
3. **RIG** [V]: R2 +1,25 contro 0,59 e −78 contro −30, conc_q5 non significativo; results +0,97 / 0,22, −68 / −16, conc_q5 p = 0,001.
4. **q di AT** [V]: R2 0,040 / 0,036 (3 insiemi), results 0,029 / 0,030 (4 insiemi).
5. **Persone contro PGT** [V]: +21% (paper §5.2, R2) contro +22% (paper §4.4, results); 8 estrazioni (R2) contro 6 (paper, results, config); 1.413 contro 1.425.
6. **ERP in assoluto** [V]: nulli 2.262 / 1.942 (R2) contro 2.254 / 1.921 (results). Differenza dello 0,4-1%, [I] rumore di riesecuzione.
7. **"Ogni indice ... p = 0,001" per RIG** (paper §4.4) contro l'indice di opportunità con p = 0,998 / 0,956 (results §3).
8. **Durata dei test** [V]: results "tests 114 s", R2 "tests 78 s": versioni diverse dei test (`1c` aggiunto dopo).
9. **Conteggio delle deviazioni dalla pre-registrazione** [V]: config `POSTHOC` ne elenca sei; paper §3.7 le riporta in quattro punti più i parametri di esecuzione; R2 Issue 2 ne aggiunge tre (famiglia BH, unilaterale/bilaterale, p95 contro BH). [V, tavola "sui testi" §2.3] Il totale reale è più di sei.
10. **Numero di particelle di terreno** [V]: paper §3.2 "112.568"; schema e C "112.851". Non spiegato [I]; forse l'esclusione di quelle fuori città (382 con centroide fuori dal perimetro [V, schema]), ma 112.851 − 112.568 = 283, non 382.
11. **Domanda** [V]: 9.259 / 9.750 / 10.503 (D_tau); 2.274 / 2.067 (D_res_decent); non riconciliate (§3.2).
12. **Rho** [V]: 0,987 (A, R1) contro 0,939 (paper §4.1) contro 0,987 come τ di Kendall nella sensibilità (results §6) [V, tavola "sui testi" §2.2]. Due grandezze omonime.

**Tra documenti delle proposte**
13. **Moran globale** 0,406 (C `summary.md`, `model.md`) contro 0,57 (file di risultato, R1): non corretto.
14. **Teach-back** 5,1 → 12,8 contro 11,5 → 12,2 (B).
15. **Particelle del posterior** 2.000 (B model) contro 3.000 (paper, tests).
16. **PCU** [V]: A 6.478 su 7.990 particelle con tras ≥ 0,5; C 5.653 su 6.989. Soglie diverse, non confrontabili [I].
17. **A non corretto dopo R1** [V, A summary]: "displacement pressure" e "Piano Casa 10k vicino alla domanda" restano; R1 aveva detto che la corrispondenza è una coincidenza (τ da 0,25 a 0,40 sposta D di sei volte [V, R1]).

**Nei test** [V, tests.py]
18. Il test 5 (p uniformi) è tautologico (ammesso da R2).
19. Il test 4a verifica "nessun PCU, nessun verde" con le stesse colonne del filtro (circolare). Il 4b (`C.ref.is_unique and ps.ndim == 1`) non può fallire per costruzione: `ps` è un vettore che assegna un sito per particella. [I]
20. Il test 4j cerca solo nomi di chiavi vietati e percorre solo i primi 50 elementi delle liste (`o[:50]`).
21. Il test 1b passa con `fp ≤ 0,10 and ci.low ≤ 0,05`; R2 ritiene la soglia 0,10 lasca [V]; il test originale è stato rilanciato con 200 ripetizioni dopo un FAIL a 50 [V, R2 Issue 1].
22. Il test 1c è PASS sul null per blocchi mentre il null della regola fallisce (23,8%) [V].
23. [I] I 17 PASS verificano implementazione e invarianti (MILP = enumerazione, budget, κ, geometrie), non la validità del modello: "17 test superati" non è evidenza sui risultati principali.

**Pre-registrazione**
24. [V, config AUDIT rule, results §2] La regola è datata 27/10, lo stesso giorno di risultati, revisioni e paper, senza timestamp esterno; tutti i file hanno lo stesso mtime 19:45 [V, `ls`]. [I] Non è verificabile che sia stata scritta prima. È *tracciabilità interna*, non pre-registrazione. Il paper lo riconosce a metà ("non le ha impedite").

## 5. Cosa serve per trasformare ciascun risultato in una prova

| Risultato | Dati reali | Test | Ipotesi falsificabile [H] (soglie da fissare prima) |
|---|---|---|---|
| PR-AUC 0,93/0,33 | Esiti indipendenti dai piani (proprietà, vincoli) | IC per blocchi; blocchi 2/4/8 km; recall per oggetto | recall@10% > 0,30 su blocchi esterni con feature solo fisiche |
| Domanda = affitti | Reddito a sezione o ISEE aggregato; tenure | Scomposizione per D_res_decent; proxy ERP con patrimonio | quota di varianza tra NIL dovuta al reddito > 0,25 con reddito fine |
| AT segregazione | Reddito per sezione, quote ERP osservate | Potenza simulata con 3, 7, 12 NIL; null per blocchi per ogni insieme; DI su sezioni | effetto minimo rilevabile dichiarato; "risk" solo se p per blocchi < 0,05 in ≥ 90% dei semi |
| AT collocazione | Idem | Soglia come curva; leave-one-NIL-out sulla versione finale | dep_resid per blocchi < 0,10 togliendo ciascuno dei 4 NIL maggiori |
| ERP "potential" | Registro di proprietà del suolo `srv_erp` (Comune, MM, ALER, catasto) | Tre regimi di suolo nella griglia | la quota di ERP pubblico verificato > 50-70% (soglia [H] da discutere); altrimenti "neither" |
| AMB_DEG | Più osservazioni (storico delle designazioni) | Potenza | Nessuna: dichiarare non testabile |
| RIG | Reddito per sezione | Null per blocchi di NIL e di CAP; indici stabili tra specificazioni | p per blocchi < 0,05 su dep_resid e dep_poor in tutte le specificazioni |
| Persone contro PGT | Costi reali; proprietà | ≥ 30 estrazioni appaiate con IC; prefiltro simmetrico | l'IC al 95% della differenza a parità di anello esclude lo zero |
| P1-P6 | Costi reali | Griglia su costo, FAR, regime del suolo; semi; Jaccard sotto pesi estremi | Jaccard mediano dei siti < 0,7 a famiglie servite entro il 2% |
| Stephenson / NIL piccoli | Reddito osservato a livello fine | Curva di soglia; leave-one-out sulla versione finale | risultato invariato per soglie 200-1.000 |
| Preferenze | Campione reale stratificato | Test-retest; confronto con archetipi | pesi osservati dentro la regione al 90% degli archetipi |

Principio comune [H]: prima il criterio di fallimento, poi la soglia (con un calcolo di potenza), poi i dati; stessa logica già proposta dalle tavole rotonde (§5), che non ripeto per intero.

## 6. Note sulla ripresa e sulle tavole rotonde

- **Ripresa** (`sessioni/ripresa_spatial_milano_lab_2026-10-27.md`): dichiara di non aver aperto i file del PC ma di basarsi sulla trascrizione. [V] Tre punti non allineati ai file: (a) "0,93/0,33" senza dire che è il rilevatore C; (b) AT "dipende molto da un solo NIL (Stephenson)" è la lettura precedente alla soglia (§3.5); (c) "17 test superati" presentato tra i risultati senza dire che sono invarianti e non validità.
- **Tavola 1** (`critica-spatial-milano-lab.md`): marcata "superata" dalla tavola 2 [V]. Errori già corretti dalla tavola 2: confronto +43/+48, rho, PR-AUC.
- **Tavola 2** (`...-sui-testi.md`): le correzioni verificano con i file. Tre rilievi miei: (a) afferma che RIG e "la dipendenza della pancia dalla definizione" sono "i risultati più solidi" [V, tavola 2 §4]: il secondo è vero per costruzione (cambiare soglia cambia il conteggio), non un risultato empirico [I]; il primo non ha null per blocchi (lo dice la tavola stessa, §3 punto 1); (b) non nota che il vincolo Gini non è vincolante; (c) non nota la sensibilità del P1 al paniere (0,22) né il pavimento di rumore (0,64).
- **Tutti i documenti hanno la stessa origine** [I]: le tavole rotonde e le revisioni sono prodotte dallo stesso sistema; la convergenza non è indipendenza, come le tavole stesse dichiarano.

## 7. Domande aperte che potrebbero cambiare le conclusioni

1. Che cosa fanno i dati a livello di sezione? Se il reddito osservato a risoluzione fine produce una mappa molto diversa da quella a 38 CAP, tutti gli indici di collocazione e segregazione vanno rifatti. [H]
2. La proprietà dei suoli `srv_erp` (e degli AT) è pubblica? È il dato che decide il "potential" di ERP. [V, paper §8]
3. Le impostazioni della griglia di sensibilità (20 s, 8 scenari) spiegano il pavimento di rumore di P1 (0,64)? Serve una corsa di controllo con identiche impostazioni. [H]
4. Quanti NIL toccano la soglia di 500 famiglie, e quanta capacità di ogni insieme contengono? [V, mancante nei file]
5. I testi di `reports/Lotti per social housing partecipativo.md` e le fonti esterne (soglia ISTAT, regole ISEE/ERP, bandi del marzo 2026, che il paper marca "non verificati su atti ufficiali" [V, paper §1.1]) non sono stati controllati qui.

## In breve

Nessun risultato principale è una prova. Il 0,93 contro 0,33 è evidenza solo che la validazione casuale è ottimista, e riguarda un rilevatore non usato nell'audit; il 0,33 è ancora gonfiato (il modello principale fa 0,099). La domanda coincide con gli affitti per costruzione, e la scomposizione ha confermato il difetto senza rimuoverlo. AT "risk" è rumore (11 semi su 20, 0,4% del DI); la collocazione non è significativa col null per blocchi e cambia con le specificazioni. ERP "potential" è un'assunzione di suolo a 1 €/m². RIG è descrittivo, senza null per blocchi. Il +48% si riduce al +5% a parità di bacino, dentro il rumore. P1-P6 sono equivalenti per famiglie servite, non per siti; il vincolo Gini non vincola. Stephenson è un artefatto di dato. Le preferenze sono sintetiche.
