# Lotti per la "pancia della distribuzione": un modello cibernetico e partecipativo per il social housing a Milano, e un audit del PGT contro i bisogni delle persone

*Prototipo di ricerca del laboratorio `lab/`. Versione del 27 ottobre 2026. Tutti i numeri provengono dai file di risultato del laboratorio (`lab/results/results.md`, `model.json`, `audit_*.csv`, `tests.json`, `lab/proposals/*/summary.md`, `lab/reviews/review1.md`, `review2.md`); dove un numero viene da un singolo file lo si indica.*

## Abstract

Ci chiediamo dove costruire alloggi sociali a Milano per la fascia di famiglie che non è idonea all'edilizia residenziale pubblica (ERP) ma non regge l'affitto di mercato, la "pancia della distribuzione" dei redditi. E ci chiediamo se le aree che il PGT 2030 già destina a trasformazione, a servizi ERP o a recupero coincidano con i bisogni di queste persone o rischino di concentrare la nuova offerta dove la deprivazione è già alta. Il modello integra quattro componenti: (i) una stima della domanda per NIL basata su redditi IRPEF 2024 per CAP, affitti OMI e un test di reddito residuo con paniere ISTAT; (ii) 2.291 siti candidati ottenuti da 112.568 particelle catastali di terreno, valutati su 9 criteri con SMAA-2 e con un apprendimento bayesiano dei pesi da confronti a coppie con domande attive; (iii) un insieme di portafogli di siti generati con un MILP robusto (media più CVaR₂₀) e tagli di diversità; (iv) un audit pre-registrato di segregazione e potenziale dei siti designati dal PGT contro null appaiati per dimensione e per distanza dal centro, con correzione di Benjamini-Hochberg e un null per blocchi di NIL aggiunto in revisione. Risultati: la definizione di bisogno decide la dimensione della "pancia" (9.259 famiglie con la regola del 30%, 2.274 con un paniere dignitoso, 102 con il paniere ISTAT puro), che è quindi un problema di sovraccarico da affitto più che di povertà materiale. Le aree designate, in particolare gli ambiti di trasformazione (AT) e gli ambiti di rigenerazione, stanno in NIL più poveri; non c'è però evidenza robusta che costruirvi aumenterebbe la segregazione, e il vantaggio apparente delle aree ERP dipende da un'assunzione contabile sul costo del suolo. Una lente "delle persone" serve il 48% di famiglie in più del "PGT così com'è", ma il vantaggio scende al 22% a parità di dimensione del bacino e al 5% a parità anche di distanza dal centro. Due revisioni paritarie avversariali hanno ribaltato due delle tre etichette pubblicate in prima versione: riportiamo questo processo come risultato.

## 1. Introduzione

### 1.1 Domanda di ricerca

Il Piano Casa milanese e i bandi del marzo 2026 si rivolgono a nuclei con 1.500-2.500 euro netti al mese, con canoni medi massimi di 90 €/m² all'anno e terreni ceduti a 1 €/m² in diritto di superficie (fonti giornalistiche raccolte nel rapporto di riferimento del laboratorio, *non verificate su atti ufficiali*). La domanda operativa è dove collocare questi alloggi. Il laboratorio l'ha formulata in tre parti:

1. **Chi è la "pancia".** Quante famiglie, e in quali NIL, sono escluse dal mercato dell'affitto ma non idonee all'ERP, e con quale definizione di esclusione.
2. **Quali lotti.** Quali siti, e soprattutto quali *insiemi* di siti, servono meglio queste famiglie sotto pesi dei criteri diversi, senza designare un unico vincitore.
3. **PGT contro persone.** Le aree già designate dal PGT (AT, aree a servizi ERP, ex ambiti degradati AMB_DEG; gli ambiti di rigenerazione RIG come contesto) hanno potenziale reale per questa domanda, oppure sovrapporre i bisogni delle persone a quelle aree rischia di concentrare l'offerta sociale dove la deprivazione è già alta?

### 1.2 Cibernetica e partecipazione

L'impostazione è cibernetica in due sensi. Il primo è la legge della varietà richiesta di Ashby (*canonico, non verificato in questa sessione*): un unico vettore di pesi comunale attenua la varietà delle preferenze fino a renderla invisibile. Per questo il modello pubblica distribuzioni di accettabilità (SMAA) e insiemi di portafogli quasi equivalenti, non un ottimo. Il secondo è il circuito di retroazione: il cittadino risponde a confronti tra due siti reali, il modello aggiorna una stima dei suoi pesi, sceglie la domanda successiva dove l'incertezza è massima e restituisce una frase di *teach-back* ("il sito B passerebbe davanti ad A se il peso del verde salisse dal 5% al 13%"). La "pancia della distribuzione" va letta come una **popolazione bersaglio** nel corpo della distribuzione dei redditi, non come la media delle preferenze espresse. Questa lettura è un'inferenza del rapporto di riferimento: l'attribuzione della metafora a Sanchez (2020) non è stata verificata sul testo. Il modello non valuta mai singole famiglie: classifica lotti e portafogli. Un sistema che assegnasse priorità a nuclei per un servizio pubblico essenziale ricadrebbe nell'Allegato III, punto 5(a), dell'AI Act.

### 1.3 Contributi

- Una catena riproducibile dalla particella catastale al portafoglio, con dati reali, assunzioni e dati sintetici separati in modo esplicito.
- Tre strati di domanda affiancati invece di un indice unico, perché le definizioni di bisogno delle tre proposte iniziali erano in disaccordo, fino all'anti-correlazione.
- Un audit di segregazione pre-registrato con null appaiati e un null per blocchi di NIL, con le deviazioni dalla pre-registrazione dichiarate una per una.
- Un prototipo web in cui il ciclo "domanda, risposta, aggiornamento, spiegazione" gira nel browser senza conservare alcun dato sulla persona.

## 2. Dati

La Tabella 1 classifica le fonti come in `model.json` (`meta.data_status`) e in `results.md` §8.

**Tabella 1. Stato dei dati.**

| tipo | contenuto |
|---|---|
| **Reale** | particelle catastali (Agenzia delle Entrate, INSPIRE) e volumi DBT 2020; strati PGT 2030 (AT, ex AMB_DEG, srv_erp, rig); DUSAF 2024; celle del Censimento 2021 su griglia esagonale; IRPEF 2024 per CAP (MEF, 38 CAP); canoni OMI 2019-2024; indicatori dei NIL; soglia ISTAT di povertà assoluta (valore da verificare) |
| **Assunzione** | FAR 1,0; resa 0,7; 80 m² per alloggio; modello di costo (costruzione 2.000 €/m², suolo al 20% del prezzo OMI, demolizione 25 €/m²); τ = 0,3; paniere 1,5 × ISTAT; quota di affittuari 0,30; occupazione a basso reddito σ = 0,5; tetti di concentrazione κ = 0,03 (0,015 dove srv_erp > 5%); decadimento λ = 1,5 km; buffer di adiacenza 2 m; suolo srv_erp a 1 €/m² |
| **Sintetico** | le distribuzioni dei pesi dei 4 archetipi (giovane lavoratore, famiglia con figli, anziano, pendolare); le famiglie simulate, che sono un modello delle distribuzioni per NIL e CAP, non record; la città sintetica dei test |

Mancano tre fonti decisive: la proprietà dei suoli, i costi di costruzione reali e le preferenze reali dei cittadini. Il reddito è osservato solo a livello di CAP (38) mentre affitti e popolazione sono a livello di NIL (88). Questa asimmetria di risoluzione condiziona i risultati (§4.1, §7).

## 3. Metodi

### 3.1 Domanda e potere d'acquisto

La domanda viene dal simulatore della proposta A, integrato nel modello:

- Una distribuzione di Dagum è stimata per massima verosimiglianza sui dati IRPEF raggruppati di ciascun CAP (Dagum in 36 CAP, lognormale in 2).
- Famiglie sintetiche sono costruite dalle ampiezze del Censimento 2021, con il reddito lordo convertito in netto familiare.
- L'idoneità ERP è approssimata con un proxy ISEE ≤ 16.000 €.
- 20 scenari bootstrap propagano l'incertezza.

Sono definiti tre strati di domanda per NIL:

- **D_tau**: famiglie affittuarie non ERP che pagherebbero più del 30% del reddito per un alloggio adeguato a canone OMI ma reggerebbero il canone sociale.
- **D_res_decent**: famiglie non ERP con reddito residuo negativo dopo l'affitto di mercato e un paniere non abitativo "dignitoso" pari a 1,5 volte quello ISTAT. È lo strato servito dai portafogli.
- **D_res_istat**: lo stesso test con il paniere ISTAT puro (754 €/mese per un adulto solo, cioè il 60% della soglia di 1.256,37 €/mese; la quota del 60% è un'assunzione).

Il test di reddito residuo segue la logica della *shelter poverty* di Stone (citata nel rapporto di riferimento via Planetizen/Harvard JCHS). Il prototipo mostra lo strato per NIL come mappa del potere d'acquisto. Per ciascun NIL riporta la mediana del residuo dopo affitto e paniere, la quota di famiglie simulate con residuo negativo e il rapporto affitto/reddito.

### 3.2 Siti candidati

Una particella di terreno entra nel pool dei candidati se soddisfa tutte queste condizioni:

- ha almeno 300 m²;
- ha meno del 50% di verde, agricolo, paesaggio, istruzione, acque o infrastrutture;
- non sta nei 6 parchi PCU;
- non è un alloggio occupato (quota d'uso residenziale ≥ 0,5);
- è un *soft site* oppure sta in un AT non PCU, su srv_erp o in un ex AMB_DEG.

Gli strati rig e dism non sono condizioni d'ingresso, perché la proposta C ha mostrato che non marcano siti (dism ≡ rig, r = 0,998). Le particelle adiacenti (buffer 2 m) e della stessa origine sono accorpate in siti di almeno 1.500 m² e al massimo 60.000 m². La capacità è min(⌊0,7 · FAR · area / 80⌋, 400) alloggi, con un minimo di progetto di 20. Delle 112.568 particelle di terreno ne restano 9.989 candidate; 7.651 finiscono in **2.291 siti**: 58 AT, 129 ERP, 5 AMB_DEG e 2.099 non designati.

### 3.3 Criteri

I nove criteri sono a livello di sito e orientati al beneficio, normalizzati min-max sui percentili 2-98 del pool:

1. accesso alla metro;
2. lavoro entro 5 km (rango);
3. scuole e servizi (E2SFCA, rango);
4. accesso al verde (E2SFCA, rango);
5. rischio calore del NIL;
6. famiglie bisognose raggiunte entro 3 km, con decadimento esponenziale (λ = 1,5 km) su celle esagonali;
7. peso dell'affitto (affitto OMI di 60 m² sul reddito netto per contribuente);
8. capacità (log₁₀ alloggi);
9. costo per alloggio.

Il "mix sociale" non è un criterio negoziabile con i pesi. È un vincolo (κ) e un oggetto dell'audit. Lo score PU della proposta C non è usato, perché importerebbe il bias socio-economico che C stessa ha documentato.

### 3.4 SMAA e apprendimento bayesiano a coppie con domande attive

Per la SMAA-2 (Lahdelma, Hokkanen e Salminen 1998; Lahdelma e Salminen 2001) si usa il motore della proposta B, invariato. Un filtro esatto di profondità di dominanza (k = 10) riduce il pool. Si stimano poi, per pesi Dirichlet uniformi e per i 4 archetipi sintetici, la probabilità di essere primo (b1), quella di stare tra i primi 10, l'accettabilità olistica, il minimo tra archetipi e un indice di consenso di gruppo.

L'apprendimento delle preferenze usa particelle sul simplesso dei pesi con verosimiglianza logistica:

P(a ≻ b | w) = ε + (1 − 2ε) · σ(β · w · (x_a − x_b)), con β = 15 ed ε = 0,05.

Nel modello Python (B) il posterior si campiona con Metropolis-Hastings su 3.000 particelle. Nel prototipo web la stessa verosimiglianza gira su 1.000 particelle con ricampionamento sistematico e rumore log-normale quando la dimensione campionaria efficace scende sotto un terzo. È una scorciatoia dichiarata nel codice: evita di tenere in memoria lo storico delle risposte. La domanda successiva è la coppia di siti reali su cui il posterior è più in disaccordo, cioè quella che massimizza min(P(a ≻ b), P(b ≻ a)) tra 300 coppie estratte da un bacino di 300 siti: i 200 migliori con i pesi correnti più 100 casuali.

Il *teach-back* è in forma chiusa. Con pesi w e differenza d = x_a − x_b, aumentare il peso del criterio j di t e rinormalizzare dà w' = (w + t·e_j)/(1 + t). Il segno di w'·d coincide con il segno di w·d + t·d_j, quindi la preferenza si inverte a t* = −(w·d)/d_j, ammissibile se t* ≥ −w_j. Il prototipo riporta il criterio con il cambio minimo della quota, (w_j + t*)/(1 + t*) − w_j. Se nessun criterio è ammissibile, lo dice. Le risposte aggiornano anche l'ordine dei portafogli, valutati con l'utilità media dei loro siti pesata per alloggi.

### 3.5 Portafogli MILP robusti con diversità

Il MILP della proposta A, risolto con HiGHS, sceglie siti e alloggi. L'obiettivo massimizza (1 − β)·media + β·CVaR₂₀ delle famiglie D_res_decent servite (β = 0,5), con decadimento per distanza. I vincoli sono:

- budget di 1 miliardo di euro;
- dimensione di progetto 20-400 alloggi;
- tetti di concentrazione per NIL κ;
- al massimo 8 siti candidati per NIL nel pool del solutore.

**Diversità.** Dopo il portafoglio P_k con insieme S_k si aggiunge il taglio Σ_{s∈S_k} y_s ≤ 0,7·|S_k|, così ogni alternativa condivide al massimo il 70% dei siti con ciascuna precedente. Si generano fino a 6 portafogli e ci si ferma se il servizio scende sotto l'85% di P1.

**Lenti di policy.**

- **L_pgt**: solo aree designate.
- **L_people**: solo aree non designate.
- **L_gini**: Gini ≤ 0,1.
- **L_smaa**: massimizza Σ capacità × accettabilità olistica (lente partecipativa).
- **L_dtau**: ottimo per D_tau.

La scelta finale gira con un limite di 300 s e gap 0,01. Una SMAA sui portafogli usa cinque criteri a intervallo fisso: quota servita, 1 − Gini, opportunità, peso dell'affitto e bassa quota di poveri nella collocazione.

### 3.6 Audit di segregazione

Per ogni insieme designato G (AT, AMB_DEG, ERP; RIG come contesto) si calcolano indici di **collocazione** e di **segregazione**.

Indici di collocazione:

- punti di contribuenti poveri rispetto alla città (dep_poor);
- reddito residuo rispetto alla città (dep_resid);
- quota di alloggi nei NIL del quintile più alto di idonei ERP (conc_q5);
- indice di opportunità (opp).

Indici di segregazione, calcolati come se G fosse costruito a FAR 1,0 con una quota σ = 0,5 di famiglie a basso reddito:

- variazione dell'indice di dissimilarità di Duncan (ΔDI);
- variazione dell'isolamento (ΔIso).

**Null a livello di sito.** Per ciascun indice si confronta G con R = 999 insiemi estratti dal pool di tutte le aree candidate, G compreso, con capacità entro ±5%. Il null *size* appaia per decile di area; il null *ring* appaia per decile di area × quintile di distanza dal centro. Il p è empirico e a una coda nella direzione del danno: p = (1 + #{null almeno altrettanto dannosi}) / (R + 1).

**Correzione multipla.** Benjamini-Hochberg (1995) a q = 0,05 su 4 insiemi × 6 indici, separatamente per ciascun null.

**Regola pre-registrata** (scritta in `config.py` il 27/10/2026 prima di ogni esecuzione dell'audit):

- *rischio di segregazione* se ΔDI o ΔIso è significativo in entrambi i null;
- *potenziale reale* se le famiglie servite per euro e l'opportunità sono almeno pari alla mediana del null in entrambi i null.

**Null per blocchi di NIL** (aggiunto in revisione come controllo co-primario, fuori dalla regola). Riassegna la capacità di ciascun NIL toccato da G a NIL casuali distinti in grado di assorbirla, eventualmente nello stesso anello, con 4.999 estrazioni. La deprivazione è osservata a livello di NIL, quindi la numerosità effettiva è il numero di NIL toccati, non il numero di siti.

**Domanda servita a confronto.** Il confronto "persone contro PGT" risolve lo stesso MILP su bacini di aree non designate estratti a caso, con la stessa composizione per decile di area e la stessa capacità del bacino designato (150 siti, 16.226 alloggi), con e senza appaiamento per anello; 6 estrazioni.

### 3.7 Pre-registrazione e deviazioni

Il testo della regola non è cambiato. Sono dichiarate queste deviazioni:

1. Una prova precedente aveva un bug nella ricerca del verdetto (`Q.index` al posto della colonna indice) che rendeva impossibile l'etichetta di rischio. Il bug è stato corretto senza toccare la regola.
2. Dopo la prova sono cambiati i parametri di esecuzione: pool di 8 siti per NIL, limite di 30 s, semplificazione delle geometrie a 1 m.
3. Il pool del null è passato da "solo aree non designate" a "tutte le aree candidate, G compreso" (correzione di calibrazione, §5).
4. Dopo la revisione 2: conc_q5 usa solo il quintile di p_erp; gli indici di collocazione usano una soglia minima di 500 famiglie per NIL; la famiglia BH è ora quella dichiarata, 4 × 6 (prima erano 3 insiemi); tutti i p sono a una coda, come in `config.py` e diversamente dalla specifica di review1; è stato aggiunto il null per blocchi di NIL.

## 4. Risultati

### 4.1 La "pancia" dipende dalla definizione

**Tabella 2. Domanda insoddisfatta per definizione (20 scenari bootstrap).**

| strato | media famiglie | p05 | p95 |
|---|---|---|---|
| D_tau (τ = 0,3) | 9.259 | 6.305 | 16.334 |
| D_res_decent (paniere 1,5 × ISTAT) | 2.274 | 663 | 4.826 |
| D_res_istat (paniere ISTAT) | 102 | 17 | 200 |

Il test con il paniere ISTAT puro lascia circa 100 famiglie: chi non arriva al minimo dopo l'affitto di mercato quasi sempre non ci arriva neppure con il canone sociale, oppure è già idoneo all'ERP. La "pancia" è quindi **sovraccarico da affitto**, non povertà materiale.

Gli indicatori del potere d'acquisto della proposta A vanno nella stessa direzione:

- il reddito netto familiare mediano per NIL è 2.303 €/mese nominali;
- il 31% delle famiglie avrebbe un residuo negativo affittando a prezzi di mercato;
- dal 2019 al 2024 i canoni OMI sono cresciuti del 41,4% contro un'inflazione NIC del 17,4%;
- il livello dei prezzi di Milano rispetto all'Italia (1,047) non sposta la fascia.

La domanda è anche geograficamente un'immagine degli affitti. La correlazione di Spearman tra tasso di domanda e canone OMI per NIL è 0,939. Con gli affitti equalizzati resta lo 0,007 della varianza tra NIL dovuto al reddito. In una variante in cui ogni famiglia cerca nel NIL più economico entro 5 km, la domanda scende da 9.750 a 14 famiglie; con il canone mediano ovunque è 6.531. Nel prototipo la mappa del residuo dopo affitto e paniere mette Brera (55 €/mese), Duomo (193) e Giardini di Porta Venezia (201) agli ultimi posti, per lo stesso effetto. Il residuo mediano medio dei NIL, pesato per famiglie, è 737 €/mese.

### 4.2 Siti: nessun vincitore

145 siti sono dominati e hanno probabilità zero di entrare tra i primi 10. Con pesi uniformi il sito più forte è primo solo nel 15% dei vettori di pesi; quello con la più alta probabilità di stare tra i primi 10 (S1778, Cimiano-Rottole-Quartiere Feltre, 227 alloggi, area non designata) arriva al 58%. La graduatoria olistica è stabile ai parametri: il τ di Kendall mediano sulla griglia di sensibilità è 0,9815. Nel test di recupero dei pesi (9 criteri, 25 domande, motore B) la distanza in variazione totale tra pesi veri e stimati è in media 0,136 (massimo 0,182). La proposta B aveva mostrato che le domande attive raggiungono in 8-10 domande l'accuratezza di 25 domande casuali (TV 0,091 contro 0,181 in condizioni di basso rumore). Nel prototipo web, con la scorciatoia di ricampionamento, 25 risposte simulate sugli archetipi portano la TV media da 0,287 (prior uniforme) a 0,183 su 8 esecuzioni (`lab/prototype/test_proto.mjs`). È un risultato peggiore del motore Python: il prototipo serve a spiegare, non a stimare.

### 4.3 Portafogli: molte alternative quasi equivalenti

**Tabella 3. Insieme di scelta (budget 1 miliardo di €; famiglie D_res_decent servite).**

| id | lente | siti | alloggi | servite (media) | CVaR₂₀ | Gini | quota designata | D_tau servite | SMAA P(top-3) |
|---|---|---|---|---|---|---|---|---|---|
| P1 | nessuna | 117 | 4.520 | 1.795 | 654 | 0,056 | 0,33 | 2.470 | 0,61 |
| P2 | diversa | 108 | 4.473 | 1.788 | 654 | 0,062 | 0,31 | 2.445 | 0,00 |
| P3 | diversa | 103 | 4.500 | 1.787 | 654 | 0,059 | 0,33 | 2.470 | 0,32 |
| P4 | diversa | 102 | 4.457 | 1.786 | 654 | 0,067 | 0,29 | 2.467 | 0,59 |
| P5 | diversa | 100 | 4.481 | 1.781 | 654 | 0,069 | 0,32 | 2.476 | 0,25 |
| P6 | diversa | 101 | 4.490 | 1.782 | 654 | 0,060 | 0,33 | 2.441 | 0,05 |
| L_pgt | solo PGT | 74 | 4.870 | 1.166 | 517 | 0,205 | 1,00 | 1.637 | 0,12 |
| L_people | solo non designate | 111 | 4.092 | 1.731 | 654 | 0,073 | 0,00 | 2.312 | 0,00 |
| L_gini | Gini ≤ 0,1 | 116 | 4.473 | 1.795 | 654 | 0,055 | 0,31 | 2.472 | 0,78 |
| L_smaa | partecipativa | 79 | 4.637 | 1.249 | 615 | 0,169 | 0,62 | 1.585 | 0,24 |
| L_dtau | domanda D_tau | 93 | 4.214 | 2.812 | 2.732 | 0,422 | 0,17 | 2.812 | 0,02 |

P1-P6 sono tutti ottimi certificati (gap massimo 0,004) e differiscono dello 0,8% nelle famiglie servite. Il loro ordine è quindi **indicativo**: sono alternative quasi equivalenti che il cittadino deve confrontare per *dove* collocano gli alloggi, non per il numero. Sotto il vincolo Gini l'equità è quasi gratuita: L_gini serve quanto P1. Il costo è invece alto nelle lenti estreme. L_smaa, che massimizza l'accettabilità, serve il 30% di famiglie in meno di P1 e spende 896 milioni. L_dtau mostra cosa succede se si cambia la definizione di bisogno: serve 2.812 famiglie D_tau, ma con Gini 0,422, perché insegue la domanda concentrata nei NIL cari.

### 4.4 PGT contro persone

**Tabella 4. Etichette pre-registrate e affermazioni difendibili.**

| insieme | siti / alloggi / NIL (effettivi) | etichetta | affermazione difendibile |
|---|---|---|---|
| AT | 58 / 10.338 / 12 (7,5) | rischio | problema di collocazione solo a livello di sito, non un rischio di segregazione robusto |
| ERP | 129 / 6.197 / 33 (12,8) | potenziale | conveniente solo se il suolo è gratuito |
| AMB_DEG | 5 / 348 / 5 (3,7) | nessuna | nessuna informazione: lo studio non ha potenza statistica |
| RIG (contesto) | 855 siti / – / 53 (26,6) | – | il segnale di collocazione più robusto |

**AT.** La capacità AT sta in NIL con reddito residuo di −92 €/mese rispetto alla media cittadina, contro −22 (null size) e −38 (null ring) delle aree confrontabili (p = 0,003 e 0,012). Il 41% è in NIL del quintile più alto di idonei ERP, contro il 18% (p = 0,001 in entrambi i null). ΔDI vale −0,00052 contro −0,00085 e −0,00083 del null (BH q = 0,029 e 0,030): costruire negli AT **riduce** la segregazione, solo di 0,00033 punti di DI meno delle alternative, cioè lo 0,4% del DI di base (0,087). Con il null per blocchi di NIL nessun indice è significativo (ΔDI p = 0,103 e 0,102; residuo p = 0,067 e 0,095; concentrazione p = 0,092 e 0,198). L'etichetta resta nella griglia di sensibilità solo nel 14% dei punti. L'indice di opportunità non distingue gli AT dal null (0,580 contro 0,584 e 0,595).

**ERP.** L'etichetta di potenziale viene dalle famiglie servite per milione di euro: 1,73 contro una mediana del null di 1,60 e 1,42. Ma dipende dal suolo srv_erp valutato 1 €/m². Valutato a prezzo di mercato come le altre aree, scende a 1,32 contro 1,58 e 1,39, e l'etichetta cade. In valore assoluto le aree ERP servono 1.729 famiglie target contro 2.254 e 1.921 delle aree confrontabili. Sono in NIL più poveri (+1,34 punti di contribuenti poveri contro +0,36 e +0,61; p = 0,006 e 0,010), ma non in modo significativo col null per blocchi (p = 0,076 e 0,151).

**RIG.** Le aree candidate negli ambiti di rigenerazione stanno in NIL più poveri: +0,97 punti di poveri contro +0,22, residuo −68 €/mese contro −16. Ogni indice di collocazione e di segregazione ha p = 0,001 in entrambi i null di sito, su 53 NIL (26,6 effettivi). È il segnale più robusto dello studio, ma come contesto e non come verdetto.

**Persone contro PGT.** L_people serve 1.731 famiglie, L_pgt 1.166: +48%. Contro bacini non designati della stessa dimensione la media è 1.425 (intervallo 1.303-1.536): +22%. Se i bacini sono appaiati anche per anello, 1.225 (1.124-1.317): +5%, e L_pgt batte 2 dei 6 bacini. Lo svantaggio del PGT dipende soprattutto dal fatto che le aree designate sono **scarse e periferiche**, non da siti individualmente peggiori.

### 4.5 Validazione

In `tests.py`, 17 test PASS e uno informativo:

- Il MILP coincide con l'enumerazione esaustiva (114,4252).
- Un effetto di segregazione inserito artificialmente viene rilevato (p = 0,001).
- Il tasso di falsi positivi sotto H0 è 0,031 [0,021; 0,044] su 1.000 ripetizioni.
- Con insiemi concentrati in 3 NIL il null di sito dà il 23,8% di falsi positivi, quello per blocchi lo 0,3%. Per questo il null per blocchi va letto come co-primario.
- I p sotto H0 sono uniformi (KS p = 0,985), test comunque tautologico (§5).
- Nessun sito è in parchi PCU o nel verde.
- Le aree dei siti coincidono con la somma delle particelle.
- Budget e κ sono rispettati.
- L'esportazione non contiene record di famiglie.
- Le geometrie esportate restano entro il 2% di area nel 99,56% dei siti.

Il prototipo aggiunge i suoi controlli in `test_proto.mjs`: sintassi dello script, inversione corretta del teach-back su 200 casi casuali, recupero dei pesi, coerenza tra sito, NIL e portafogli in `lab.json`.

## 5. Processo di revisione come risultato

Il laboratorio ha lavorato in tre proposte indipendenti: A (economia e ricerca operativa), B (decisione e partecipazione), C (ML e analisi spaziale). Sono seguite un'integrazione e due revisioni avversariali. Le revisioni hanno cambiato le risposte, non solo la forma.

### 5.1 Revisione 1: le tre proposte non rispondevano alla domanda

- **A**: la domanda per NIL era al 99% una mappa degli affitti (ρ = 0,987 tra tasso di domanda e canone) perché il reddito è risolto solo a 38 CAP. "Pressione da espulsione" era un'etichetta non supportata. La correzione è la decomposizione rent/income e la variante di ricerca cittadina (§4.1), più lo strato di reddito residuo con il paniere ISTAT.
- **B**: il pool lasciava passare i parchi, con 31 dei primi 100 lotti dentro ambiti PCU, compreso uno dei quattro lotti "di consenso" (Parco Forlanini). Il criterio di verde premiava lo stare dentro un parco. La correzione è un filtro unico e il verde misurato come accessibilità E2SFCA.
- **C**: riportava AUC senza segno. Ri-firmate, mostravano che le aree designate in passato stanno in NIL con più stranieri (AUC 0,711) e più contribuenti poveri (AUC 0,697): il primo segnale quantitativo di rischio, che ha motivato l'audit con null appaiati. Un Moran's I riportato come 0,406 era 0,57 nel file di risultato.
- **Tra proposte**: i tre indicatori di bisogno erano in disaccordo. Quello di A era anti-correlato con B e C (ρ = −0,25 e −0,20), mentre B e C coincidevano (ρ = 0,94). Da qui la scelta di strati di domanda espliciti e plurali invece di un indice medio.

### 5.2 Revisione 2: due etichette su tre non reggono

- **Calibrazione.** Il null estratto dal solo complemento di G era anti-conservativo: falsi positivi 0,061 [0,051; 0,072] contro 0,042 [0,034; 0,052] del null per permutazione. Con il pool corretto il ΔDI di AT è passato da p = 0,003 a 0,011.
- **AT = rischio era un lancio di moneta.** L'etichetta compariva in 11 semi su 20 e spariva col null per blocchi di NIL (p = 0,10). Era trainata in parte da Stephenson: un NIL di 92 famiglie che riceve 1.641 alloggi AT, 17,9 volte il suo stock, e che eredita le statistiche di reddito del CAP. La soglia di 500 famiglie e conc_q5 sul solo p_erp hanno ridotto lo scarto di collocazione. La stima di revisione era circa −150 €/mese contro −45, con l'82% nel quintile ERP contro il 49%; dopo le correzioni è −92 contro −22/−38, con il 41% contro il 18%.
- **ERP = potenziale era contabilità.** Dipendeva dal suolo a 1 €/m²; a prezzo di mercato l'etichetta cade (§4.4). conc_q5 per ERP era in parte tautologica, perché srv_erp definiva il quintile.
- **"+43%" era in gran parte un effetto di dimensione del bacino**: +21% a parità di dimensione, +5% a parità anche di anello. Dopo il nuovo calcolo a 300 s le cifre sono +48 / +22 / +5%.
- **Gap del solutore.** A 30 s i gap di P1-P6 erano del 2,3-7,4%. P1 è passato da 1.742 a 1.795 famiglie con la certificazione a 300 s, e il ranking tra P1-P6 è diventato "indicativo". CVaR₂₀, saturato a circa 654 per tutti i portafogli non PGT, è stato escluso dalla SMAA dei portafogli.

La decisione della revisione 2, "accettare con revisioni maggiori", è stata applicata: le affermazioni difendibili della Tabella 4 sostituiscono le etichette come titolo. Ne traiamo una conclusione metodologica: **la pre-registrazione ha reso visibili le deviazioni, ma non le ha impedite**. Ciò che ha protetto i risultati sono stati i null aggiuntivi e la scomposizione dei confronti.

## 6. Discussione

### 6.1 Cosa è nuovo e cosa no

Non è nuovo il quadro GIS-MCDA. È un campo maturo (Malczewski 2006; Malczewski e Rinner 2015), e gli studi sulla localizzazione di alloggi accessibili usano quasi sempre pesi da esperti con AHP, a volte TOPSIS (per esempio Fang et al. 2022). Non sono nuovi neppure SMAA-2, il campionamento Dirichlet dei pesi, la CVaR come misura di rischio (Rockafellar e Uryasev, *a memoria, non verificato*) né la correzione BH.

Riteniamo nuovi, nei limiti della ricerca bibliografica del laboratorio (che non ha trovato studi italiani o spagnoli con revisione paritaria sulla localizzazione GIS-MCDA dell'edilizia sociale):

1. Pesi partecipativi con dispersione visibile, appresi da confronti a coppie su siti reali con domande attive e restituiti con un teach-back in forma chiusa.
2. Un MILP per portafogli con tagli di diversità e lenti di policy esplicite, che produce un *insieme di scelta* invece di un ottimo. Il rapporto di riferimento non ha trovato in letteratura un MILP per il mix sociale nell'edilizia sociale; la formulazione è dell'autore.
3. Un audit pre-registrato della pianificazione esistente contro null appaiati per dimensione, per distanza dal centro e per blocchi di NIL.
4. La dimostrazione empirica che, a Milano, la scelta della definizione di bisogno (τ, paniere) cambia la domanda di due ordini di grandezza e sposta il portafoglio ottimo tra centro e periferia.

### 6.2 Implicazioni per il Comune

- **Dichiarare la definizione di bisogno come scelta normativa.** Con τ = 0,3 la "pancia" è di circa 9.000 famiglie concentrate nei NIL cari; con il reddito residuo dignitoso è di circa 2.300 famiglie. Sono due politiche diverse: la prima è anti-espulsione dai quartieri centrali, la seconda è sostegno al reddito disponibile.
- **Non leggere le aree designate come "pronte".** Il potenziale ERP dipende dalla proprietà pubblica del suolo, che il laboratorio non ha potuto verificare. Va controllata prima di ogni altra cosa.
- **Gli AT non sono una trappola di segregazione,** ma la loro capacità sta in pochi NIL (12, di cui 7,5 effettivi) più poveri della media. Il rischio va gestito con tetti di concentrazione per NIL (κ), che il MILP già rispetta, e con un monitoraggio a livello di sezione, non a livello di NIL.
- **Pubblicare insiemi di alternative, non un ottimo.** Esistono almeno sei portafogli quasi equivalenti con una quota designata tra il 29% e il 33%. La scelta tra loro è politica e partecipativa, non tecnica. Nella scala di Arnstein (1969, *canonico*) la piattaforma sale da "consultazione" a "partnership" solo se il Comune dichiara *prima* come i pesi espressi vincolano la scelta tra alternative.

### 6.3 Implicazioni per i cittadini

Il prototipo restituisce una spiegazione invece di un verdetto. Mostra quali siti vincono sotto quasi tutti i profili di pesi, quali solo sotto il proprio, e quanto dovrebbe cambiare un peso perché due siti si scambino. I dati restano sul dispositivo: nel browser vivono solo i pesi, in memoria, e nessuna risposta viene salvata. Gli archetipi che colorano la mappa sono sintetici: non dicono nulla di ciò che i milanesi preferiscono. Su questo deve dirsi esplicitamente ogni uso pubblico.

## 7. Limiti

1. **Deprivazione ecologica.** Il reddito è osservato a 38 CAP e la deprivazione a 88 NIL. La collocazione dentro il NIL è invisibile, salvo la pressione modellata su esagoni dalla proposta C, che a sua volta varia solo con la quota di laureati. Gli indici di collocazione e di segregazione sono un unico segnale ecologico, non prove indipendenti.
2. **Basso reddito = quota ERP simulata.** DI e isolamento usano la quota idonea ERP come "basso reddito". Con una quota cittadina di 0,46, vicina a σ, ΔDI è dell'ordine di 10⁻⁴-10⁻³ ovunque.
3. **Capacità e costo nozionali.** Mancano proprietà, vincoli, beni tutelati e indici reali del PGT. FAR 1,0 e il modello di costo sono assunzioni; gli insiemi designati sono valutati come se costruiti per intero.
4. **AMB_DEG ha 5 siti.** Un "nessuna" lì non è evidenza di assenza.
5. **Distanze euclidee,** non di rete.
6. **Saturazione.** Le famiglie servite per euro saturano negli insiemi grandi (capacità molto superiore a D_res_decent), quindi seguono soprattutto il costo.
7. **Preferenze sintetiche.** Il prototipo web usa una scorciatoia di ricampionamento senza MCMC, che recupera i pesi peggio del motore Python. Il modello lineare non rappresenta veti né preferenze lessicografiche.
8. **Fonti da verificare.** Soglia ISTAT del 2024, inflazione NIC di Milano, quota del 60% del paniere, mappatura dei NIL sulle fasce OMI.
9. **Etichetta AT instabile.** Varia con i parametri (stabilità 0,14) e con i semi del Monte Carlo. La griglia di sensibilità usa R = 299 contro 999 del modello base e misura in parte rumore.

## 8. Lavoro futuro

- **Preferenze reali.** Un panel sorteggiato dall'anagrafe, stratificato per municipio, età, tipo di nucleo e titolo di godimento, affiancato al canale aperto riponderato sui margini censuari. Inquilini a canone di mercato e nuclei in graduatoria vanno rappresentati esplicitamente. Va misurato l'errore sulle minoranze come condizione di rilascio, perché la proposta B ha mostrato che il prior di popolazione peggiora la stima per la minoranza (TV da 0,212 a 0,232). Va pubblicato un insieme seq-PAV accanto al consenso.
- **Proprietà dei suoli.** Incrociare le aree srv_erp e AT con il patrimonio comunale, MM e ALER e con il catasto. È il test decisivo per il potenziale ERP.
- **Redditi sotto il CAP.** Sezioni di censimento e, dove possibile, microdati amministrativi aggregati (ISEE per sezione con celle minime), per sostituire la deprivazione ecologica per NIL. Titolo di godimento dal Censimento 2021, al posto della quota di affittuari fissa a 0,30.
- **Validazione con i cittadini.** Sessioni in presenza sul prototipo per misurare comprensione del teach-back, stabilità test-retest dei pesi e divergenza tra canale aperto e panel. Il caso FindingPlaces di Amburgo (circa 400 partecipanti, 160 siti individuati, 44 superati i controlli legali, 6 costruiti; Noyman et al.) ricorda di gestire le aspettative.
- **Tecnica.** Posterior esatto nel browser (MCMC sulle risposte in memoria di sessione), distanze di rete, recupero degli sfitti ERP come strato di offerta alternativo, R ≥ 999 nella griglia di sensibilità.

## Riferimenti

Solo riferimenti presenti nei file del team (`reports/Lotti per social housing partecipativo.md`, `lab/proposals/*/model.md`, `lab/reviews/*`). Con *[non verificato]* sono marcati i riferimenti citati a memoria o non ricontrollati nelle fonti del laboratorio.

- Anselin, L. (1995). Local indicators of spatial association, LISA. *Geographical Analysis* 27:93.
- Arnstein, S. (1969). A ladder of citizen participation. *[non verificato: canonico, a memoria]*
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. *[non verificato: canonico, a memoria]*
- Benjamini, Y., Hochberg, Y. (1995). Controlling the false discovery rate. *JRSS-B* 57:289.
- Bottomley, P. A., Doyle, J. R., Green, R. H. (2000). Testing the reliability of weight elicitation methods.
- Bramley, G. et al. (2010). *Estimating housing need*. DCLG.
- Costanza-Chock, S. (2020). *Design Justice*. *[non verificato: canonico, a memoria]*
- Duque, J. C., Anselin, L., Rey, S. (2012). The max-p-regions problem. *Journal of Regional Science*.
- Elkan, C., Noto, K. (2008). Learning classifiers from only positive and unlabeled data. *KDD*.
- Fang, C. et al. (2022). Localizzazione di alloggi accessibili a Nanchino. *Land* 11(9):1403.
- Feizizadeh, B., Kienberger, S. (2017). Sensibilità globale spazialmente esplicita in GIS-MCDA. *Journal of Environmental Planning and Management* 60(11).
- Geertman, S. (2017). PSS: beyond the implementation gap. *Transportation Research Part A* 104.
- Lahdelma, R., Hokkanen, J., Salminen, P. (1998). SMAA, stochastic multiobjective acceptability analysis. *European Journal of Operational Research*.
- Lahdelma, R., Salminen, P. (2001). SMAA-2. *Operations Research*.
- Lienert, J. et al. (2016). Weight elicitation (SWING). *European Journal of Operational Research* 253(3).
- Malczewski, J. (2006). GIS-based multicriteria decision analysis: a survey. *IJGIS*.
- Malczewski, J., Rinner, C. (2015). *Multicriteria Decision Analysis in Geographic Information Science*. Springer.
- Noyman, A. et al. FindingPlaces, Amburgo (CityScope); URBACT, buona pratica "Finding Places".
- Rockafellar, R. T., Uryasev, S. CVaR. *[non verificato: a memoria]*
- Sanchez, J. (2020). *Architecture for the Commons*. Routledge. (Attribuzione della metafora della "gaussiana" *[non verificata]*.)
- Spielman, S. E. et al. (2020). Evaluating social vulnerability indicators (SoVI). USGS.
- Stone, M. E., "shelter poverty" / reddito residuo, citato tramite Planetizen su Harvard JCHS. *[fonte secondaria]*
- Vonk, G., Geertman, S. (2008). Improving the adoption and use of planning support systems. *Applied Spatial Analysis and Policy*.
- Unione Europea, Regolamento sull'IA (AI Act), Allegato III, punto 5(a).
- Eurostat, Housing cost overburden rate (glossario e dati Italia).
- Aziz, H. et al., Justified Representation nel voto per comitati (citato dalla proposta B per l'audit JR). *[riferimento incompleto nei file]*
