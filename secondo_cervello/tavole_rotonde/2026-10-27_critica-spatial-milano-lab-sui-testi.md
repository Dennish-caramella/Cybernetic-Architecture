# Tavola rotonda sui testi: critica a "Spatial Milano Lab" e piano per portarlo a livello PhD

Data: 2026-10-27. Sostituisce la prima versione (`2026-10-27_critica-spatial-milano-lab.md`), fatta senza aver letto i testi.
Fonti lette dalle voci: `paper.md`, `review2.md` (integrali); `review1.md`, `results.md`, `config.py`, `README.md`, `summary` delle proposte (a campione o per le parti pertinenti), in `/mnt/project-files/spatial_milano_lab/`. Copia anche in `Desktop\TESI\spatial_milano_lab\`.
Etichette: [S] testo letto (file e sezione), [I] inferenza, [H] ipotesi, [L] lacuna. Voci: ingegnere edile (IE), De Carlo-Mari (DC), Pask (PK), Azadi (AZ), MVRDV (MV), De Graaf-Murphy (DG), **statistica spaziale (ST), voce ad hoc fuori dal corpus delle schede: la sua competenza non viene da schede ma dalla disciplina in generale.**

## 0. Limiti di questa tavola
- Le sette voci hanno letto gli stessi due testi: la loro convergenza non è conferma indipendente. Su pesi e MILP convergono perché tutte leggono paper §3.5. [I]
- Non letti da nessuno: codice eseguibile (`run.py`, `audit.py`, ecc., non copiati), dati di base, `tests.py` (solo in parte). Le cifre sono quelle riportate dai testi; nessuno le ha ricalcolate. [L]
- Il diritto urbanistico (PGT, L.R. 18/2019), economia immobiliare e la proprietà dei suoli restano fuori dal team. [L]
- Il secondo round (voci che rispondono tra loro) non è stato fatto.
- Le soglie numeriche proposte dalle voci (numerosità, Jaccard, quote) sono tutte [H] e arbitrarie finché non c'è un calcolo di potenza. Il criterio di fallimento va fissato prima della soglia.

## 1. Cosa i testi dicono già (la prima tavola lo trattava come lacuna)
- [S] Null per blocchi di NIL e correzione di calibrazione (paper §3.6, §5.2); AT = "problema di collocazione solo a livello di sito" (Tab. 4); AT con etichetta "risk" in 11 semi su 20 e in 2 punti su 14 della griglia (§5.2, §7.9; review2 Issue 3); deviazioni dalla pre-registrazione elencate (§3.7); ERP a prezzo di mercato 1,32 contro 1,58/1,39 (§4.4; review2 7a); persone contro PGT +48% / +22% / +5% (§4.4); preferenze sintetiche e nessun uso reale (§6.3, §8); ecologia a 38 CAP (§7.1); costi nozionali (§7.3).
- [S] Il paper conclude che la pre-registrazione "ha reso visibili le deviazioni, non le ha impedite" (§5.2). Resta senza timestamp esterno [I].

## 2. Correzioni alla prima tavola (verificate dal revisore sui testi)
1. **+43% contro +48%**: lo stesso confronto (L_people contro L_pgt) con solutore a 30 s (1.672) e a 300 s (1.732) (review2 Issue 5). Non erano "versioni diverse". Piccole discrepanze interne: +21% in paper §5.2 contro +22% in §4.4; 8 estrazioni (review2) contro 6 (paper). [S]
2. **rho 0,987 contro 0,939**: 0,987 è il valore della proposta A prima della correzione (review1; paper §5.1); 0,939 è nel paper §4.1 come Spearman tra tasso di domanda e canone OMI per NIL. Nessun testo dice che sia "dopo la scomposizione" né che sia un altro indicatore: resta [H] che il modello integrato usi una definizione di domanda diversa. Attenzione: `results.md` §6 ha una colonna 0,987 che è un Kendall τ, grandezza diversa e omonima. [S]
3. **"Sei modifiche"**: `config.py` (POSTHOC) ne elenca sei; il paper §3.7 le raggruppa in quattro punti includendo anche il bug del verdetto e i parametri di esecuzione (pool di 8 siti, 30 s, semplificazione a 1 m); review2 Issue 2 elenca tre deviazioni a parte. Il totale delle deviazioni dichiarate è quindi più di sei. [S]
4. **"Nessuna sensibilità sul costo"** era impreciso. [S] La griglia `SENS` contiene tau, basket, lam_km, kappa, far, sigma, buffer_m. **Non contiene** c_build, land_inc, c_demo, gfa_dw, yield né il regime del suolo. Sotto la griglia ERP "potential" resta in 14 punti su 14 (stabilità 1,00), quindi **vuota** rispetto al suolo. C'è però un controllo puntuale fuori griglia, ERP a prezzo di mercato (§4.4), in cui l'etichetta cade.
5. **"Pluralità apparente di P1-P6"**: non è un difetto automatico. [S] P1-P6 condividono al massimo il 70% dei siti **per costruzione** (taglio di diversità, §3.5): la diversità dei siti non è un risultato. Resta aperto se i pesi elicitati muovano i portafogli.
6. **PR-AUC 0,33 contro 0,93** riguarda il rilevatore ML della proposta C, non l'audit; non compare in paper né review2. Estenderlo era scorretto. [S]
7. **Cooptazione e proprietà fuori dal modello** passano da inferenza a [S]: paper §3.3 (nove criteri scelti dal laboratorio, mix sociale come vincolo κ, al cittadino restano i pesi), §2 e §8 (proprietà dei suoli tra le fonti mancanti).

## 3. Limiti che restano
**Statistici (ST)**
1. **RIG "il più robusto" non ha un null per blocchi**, né nel paper né in review2, che lo definisce "il segnale più robusto"; i p = 0,001 vengono dai null di sito, che il paper stesso mostra anti-conservativi con insiemi raggruppati (23,8% di falsi positivi con 3 NIL, §4.5). RIG tocca 53 NIL, quindi il rischio è minore ma non quantificato. [S, I]
2. Il null per blocchi riassegna capacità tra NIL la cui deprivazione viene dal reddito per CAP (38): tre NIL con lo stesso CAP non sono indipendenti, e i p per blocchi possono essere ancora ottimistici. [H]
3. Dipendenza spaziale e MAUP (CAP, NIL, altre zonizzazioni) non analizzati; potenza e effetto minimo rilevabile non quantificati: un esito nullo è "non informativo", non "negativo". [L]
4. Forking paths dopo i risultati (conc_q5 82%→41%, soglia 500 famiglie, famiglia BH, p unilaterali): la pre-registrazione è tracciabilità, non protezione (paper §5.2). Esiti ulteriori (null per blocchi, senza Stephenson, griglia) fuori da una famiglia di errore. [S, I]

**Partecipazione e cibernetica (DC, PK, AZ, MV)**
5. **I pesi non entrano nell'obiettivo del MILP.** [S] Il MILP massimizza (1−β)·media + β·CVaR₂₀ delle famiglie servite (§3.5). I pesi entrano nell'ordinamento dei portafogli per utilità media (§3.4), nella SMAA dei portafogli con cinque criteri fissi (§3.5) e in L_smaa, che serve il 30% di famiglie in meno di P1 (1.249 contro 1.795; accettabilità calcolata con pesi Dirichlet e archetipi sintetici, non pesi elicitati). Che i pesi muovano o no la scelta tra portafogli non è mai misurato. [L]
6. La regola "come i pesi vincolano la scelta" è una condizione dichiarata (§6.2), non implementata; nessun innesto istituzionale, nessun decisore, nessuna misura di comprensione o uso. [S, L]
7. Il ciclo di retroazione agisce solo sul livello oggetto (pesi). Criteri, κ, τ, paniere e budget sono scelte degli autori; nessuna risposta può cambiare le regole (PK, DC). [I]
8. La definizione di bisogno (9.259 / 2.274 / 102 famiglie) pesa più dei pesi; è dichiarata "scelta normativa" ma consegnata al Comune, non agli abitanti (§4.1, §6.2). [S, I]
9. Ashby non verificato sul testo (il paper lo dichiara, §1.2); "varietà" qui è dispersione dei pesi, non il confronto di repertori. [I, L]

**Economia, ingegneria, potere (IE, DG)**
10. Costi e capacità nozionali: FAR 1,0 su tutta la capacità AT (10.338 alloggi), tetto 400 alloggi, nessuna verifica tecnica; H4 non testata. [S, L]
11. La lente "persone" presuppone suolo a mercato (20% OMI): non è calcolato quanta parte del miliardo vada a proprietari privati (rendita). [H]
12. Licenza e riuso del codice e dei dati non trattati; percorsi locali. [L]

## 4. Cosa regge
[S] Catena riproducibile dalla particella al portafoglio, dati reali/assunzioni/sintetici separati (Tab. 1), 17 test superati, MILP uguale all'enumerazione esaustiva, revisioni avversariali che hanno ribaltato due etichette su tre e sono riportate come risultato (§5), affermazioni difendibili al posto delle etichette (Tab. 4). La domanda "PGT contro persone" riceve una risposta onesta e stretta. RIG (contesto) e la dipendenza della "pancia" dalla definizione di bisogno (da 9.259 a 102 famiglie) sono i risultati più solidi, con la riserva del punto 1.

## 5. Piano per portarlo a livello PhD
**Principio.** Prima il criterio di fallimento, poi la soglia, poi i dati; la soglia numerica si fonda su un calcolo di potenza dichiarato. Le soglie sotto sono [H] proposte dalle voci e vanno discusse.

| # | Intervento | Prova | Fallimento (da fissare prima) | Voci |
|---|---|---|---|---|
| 1 | Chiudere il buco di RIG e della potenza | Null per blocchi di NIL e di CAP per AT, ERP, RIG; potenza simulata piantando effetti noti in 3, 7, 12 NIL; effetto minimo rilevabile dichiarato | RIG non significativo per blocchi: "il più robusto" cade; potenza insufficiente: concludere "non rilevabile" | ST |
| 2 | Far entrare i pesi nell'obiettivo e misurare l'effetto | Funzione obiettivo con pesi; pesi agli estremi del simplesso; Jaccard dei siti, delta famiglie servite, a gap certificato | Jaccard mediano alto (proposta: > 0,9): la scelta tra portafogli è apparente e va dichiarata non testabile | MV, PK, DG, DC |
| 3 | Sensibilità su costi e regime del suolo | Griglia con c_build, land_inc, c_demo, yield, gfa_dw e tre regimi del suolo (gratuito, pubblico verificato, mercato), R ≥ 999 | Se il solo regime del suolo ribalta confronti o etichette, il "per euro" non si pubblica | IE, DG, MV |
| 4 | Proprietà del suolo e bilancio del miliardo | Incrociare AT e srv_erp con catasto e patrimonio Comune/MM/ALER; scomporre il costo in privati, costruzione, sussidio pubblico | Proprietà pubblica non confermata su gran parte dell'ERP (proposta: < 50-70%), o rapporti persone/PGT che cambiano segno | DG, IE |
| 5 | Persone reali che scrivono le regole | Elicitazione di criteri, soglie e definizione di bisogno con campione stratificato (inquilini di mercato, graduatoria, stranieri); regola "pesi → scelta" dichiarata prima | Criteri proposti coincidenti con i nove e portafogli invariati oltre la variabilità tra ripetizioni: partecipazione decorativa; divergenza forte: modello cooptato (entrambi sono risultati) | DC, AZ, PK, MV |
| 6 | Valutazione sociotecnica | Comprensione del teach-back, test-retest dei pesi, errore sulla minoranza (il paper osserva TV 0,232 con il prior di popolazione), confronto tra due versioni | Sotto soglia di comprensione o stabilità non oltre il rumore del posterior (TV 0,183 contro 0,287 del prior) | AZ, DC |
| 7 | Revisione tecnica cieca e capacità reale | 30 siti stratificati per origine valutati da tecnici contro una griglia di vincoli scritta prima; capacità FAR 1,0 contro indici reali del PGT | Scarti sistematici oltre soglia fissata prima, o scarto mediano della capacità fuori tolleranza: i risultati si riportano come ordinamento relativo, non come alloggi serviti | IE |
| 8 | Replica | Hash del codice e dei parametri, timestamp esterno, specificazione alternativa scritta da altri, licenza aperta | Etichette che cambiano con la specificazione alternativa | PK, DG, ST |

Numerosità: le voci propongono 12, 12-30, 30 e ≥ 60 partecipanti, senza fonte; 12 è la numerosità dei workshop della scheda 37, citata per confronto e non come soglia di potenza.

## 6. Decisioni che spettano a Dennis
1. **Natura del laboratorio.** Dispositivo esplorativo (e allora i limiti dei §3 fanno parte del risultato) oppure aspirazione a un'inferenza sulla segregazione (e allora servono gli interventi 1, 2, 3 e 8).
2. **Quali tre interventi** diventano la prossima fase sperimentale, con criteri di fallimento fissati da te.
3. **Chi scrive la definizione di bisogno e il vincolo "pesi → scelta":** il Comune, gli abitanti o la tesi. È il punto in cui il lavoro si collega al rischio di cooptazione del Report fondativo.
4. **Collocazione nella tesi:** lo stato dice che la fase attuale è ricerca e sintesi; questo filone è sperimentazione (Fase 3). Va deciso se entra come prova esplorativa o resta fuori finché il Report fondativo non è chiuso.
