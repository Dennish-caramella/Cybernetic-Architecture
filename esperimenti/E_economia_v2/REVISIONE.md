# §7 Revisione indipendente — Base E v2 (ticket #19)

Revisore metodologico, 23/11/2026. Non ho eseguito la prova. Sono un'altra istanza dello stesso sistema dell'esecutore: **non è una verifica fatta da persone** [I]. Ho rieseguito `run.py` (che lancia anche i test `--reali`) in una copia nello scratchpad della sessione, con la cache OMI della v1 e la Base L v7 del repo in sola lettura. Ho poi scritto un controllo indipendente: le formule di cooperativa, developer e K1 sono riscritte dalla pre-registrazione, e da `run.py` prendo solo il caricamento dei dati e il campionamento. Nel repo ho scritto solo questo file. Nella cache ignorata, la riesecuzione ha riscritto `_cache/E_economia_v2/ripetizione/` con un contenuto identico. Ho anche rimosso due collegamenti simbolici che avevo creato per errore (uno in `_cache/E_economia/`).

**Esito proposto: PASSA per il calcolo e per i criteri E1–E7, nessuna ripetizione. Il REPORT però va corretto prima del congelamento.** La v2 risolve nella sostanza G1 e, nella forma, G2. G3 lo risolve solo in parte. Resta un difetto grave (V1), che non sta nel motore ma nel REPORT: l'uscita principale passata alla tesi (il canone di pareggio, "≈ 130") è riportata solo nella regione tarata. Quella regione è contraddetta dall'unica evidenza esterna disponibile (bandi deserti, [S]), e la pre-registrazione 1.12 chiede di riportarla accanto alle altre. Per la regola di arresto ci si ferma finché il REPORT non è corretto e Dennis non ha deciso (§7.9). In ogni caso il congelamento richiede la sua conferma di H1–H19.

## 7.1 Riproduzione e cronologia [V]
- **SHA-256** di `esecuzioni/00_preregistrazione.txt` = `01d50363…e769`. Coincide con il file `.sha256`, con la costante `SHA["prereg"]` in `run.py` (verificata a ogni esecuzione da `check_inputs`) e con il commit 34c09dc. Il file è invariato da 34c09dc a HEAD (`git diff --quiet`).
- **Cronologia dei commit**:
  - 34c09dc alle 01:28:13Z (pre-registrazione e DECISIONI);
  - bcd8038 alle 01:28:31Z (riga 1 del registro);
  - 977d02d alle 02:11:28Z, il primo commit che contiene `run.py`, i test, le tabelle e il REPORT.
- **Cache**: le tabelle della prima esecuzione, spostata in `_cache/E_economia_v2/esecuzione_1_superata/`, hanno data 01:38:23Z, cioè dopo la pre-registrazione. Ho confrontato quelle tabelle con le definitive: identiche byte per byte; in `E6_celle.csv` cambia solo l'etichetta `param_max_E6` dove il massimo è 0; il JSON è uguale salvo E1. La voce 5 del registro ("correzioni di sola forma") è quindi confermata.
- **Limite della cronologia** [L]: tra il commit della pre-registrazione e la prima tabella passano 10 minuti, in cui il registro colloca 5 chiamate web, la scrittura del codice, i test T1–T12 e la taratura. Per un agente è plausibile, ma non posso escludere che parte del codice esistesse prima. Le voci 2–11 del registro stanno in un solo commit e il loro ordine interno non è verificabile.
- **E1 si riproduce**: la mia esecuzione dà l'hash di contenuto `024ac9ea…5725454`, identico nelle due ripetizioni interne e al registro (quinta e sesta ripetizione complessiva). Sono identici byte per byte anche `esito_criteri.json` (diff vuoto su tutti i campi), tutte le tabelle e `fig/E6_celle.png`. Tempo: 11 min 26 s.
- **E2**: T1–T12, `ann` e `reali` passano.
- **m1 risolto**: il JSON è un'uscita dello script, non è completato a mano.

## 7.2 Ricalcolo a mano [V/I]
**Lotto E00173** (fascia E, zona E5): area 5.308,3 m², FAR 1, SL sotto 10.000 (s_ERS = 0), p_mid 3.350 €/m². Punto centrale pre-registrato, c₀ = 90, T = 60.
- **Tasso reale**: r = 0,7·2,2% + 0,3·(−0,5%) = **1,39%**.
- **Costi** per m² di SL: O = 100·3 + 0,075·484,78 = 336,36; C_tot = 2.000·1,12 + 336,36 = 2.576,36.
- **Cooperativa**. NOI₁ = 0,85·90·(0,96 − 0,20) − 0,008·2.000 = 42,14 (reale, costante). A(r, 0, 60) = (1 − 1,0139⁻⁶⁰)/0,0139 = 40,516. VA = 42,14·40,516/1,0139³ = 1.638,1. Costo = 2.576,36·(1 + 0,0139·1,5) = 2.630,1. **L\* = −991,9 €/m² di SL**, quindi **ΔL^(ces) = 991,9**.
- **Canone di pareggio con suolo gratuito**: c\* = 3.252,0/25,11 = **129,5** €/m²/anno a 60 anni; **107,7** a 90 anni.
- **Developer**. p = 1,15·3.350 = 3.852,5; GDV = 0,85·p = 3.274,6. Residuo = 3.274,6·0,82 − 2.576,36 − 139,12 = −30,3. K = 1,09·1,06³ = 1,2982. **VRA = −23,3**, quindi L_mkt = 0 e ΔL^(acq) = ΔL^(ces) = 991,9.
- **Controllo in fascia D** con il lotto E00182 (zona D39, p_mid 4.800): VRA = 871,9, quindi ΔL^(acq) = 1,09·871,9 + 991,9 = **1.942,4**.

Il controllo indipendente sullo stesso campione (seme 4519) riproduce tutti i valori seguenti, uguali a `esito_criteri.json` e a `delta_L_lotti.csv.gz`:
- regioni: |Θ\*| 18.982; |Θ\*_cal| **10.912**; |Θ_rov\*| **9.419**;
- quote su Θ\*_cal, cessione a c₀ = 90: **0,0206** a 60 anni e **0,1728** a 90 anni;
- acquisto a 60 anni: 0,000 per E00182 e 0,005 per E00173;
- c\* con suolo gratuito: **130 (97–162)** a 60 anni e **108 (78–137)** a 90 anni.

Le formule di §3 della pre-registrazione sono implementate come scritte. Θ_cal e Θ_rov\* **si sovrappongono in 1.349 punti**, quelli con −5% ≤ VAN/C < 0 (vedi V5).

## 7.3 I difetti della v1 sono risolti?
| Difetto v1 | Stato | Prova [V] |
|---|---|---|
| G1 r ≈ g | **Risolto nella sostanza** | Il canone è indicizzato ISTAT (DG 365), quindi g reale = 0 per costruzione: la taratura non può più spingere g verso r. In Θ_cal r ≤ 0,5 punti solo in 979 punti su 11.891. La cessione a 90 anni vale 0,17 con il vincolo e 0,21 senza: il vincolo H12 conta poco. Resta che **r decide**: 0,37 nello strato S2 contro 0,11 in S3. L'indicizzazione al 100% dell'ISTAT è assunta: con un'indicizzazione parziale g reale sarebbe < 0 [L]. |
| G2 E6 nel punto sbagliato | **Risolto nella forma, con riserve** (V5) | 135 celle, elenco preso dalle marche. Restano tre limiti: (a) un parametro alla volta, al punto base; (b) nella cessione ogni cella vale 0 o 1, perché il lato cooperativa non dipende dalla zona; (c) parametri fuori elenco ribaltano celle "robuste": c_new 1,00 in "edificabile, cessione, T 90, c₀ 130" e in "R1, cessione, T 60, c₀ 90"; ρ 1,00 in "R1, cessione, T 30 e 60". |
| G3 suolo nullo in periferia | **In parte** (V2) | E7 passa (rapporto 0,86) solo grazie a π_new, scelto conoscendo l'effetto della v1. Con π_new = 0 il rapporto è **0,20**, sotto 0,5, e tutte le celle D/E sarebbero "non informative". Nel 17,6% dei lotti in fascia D il L_mkt mediano è 0. |
| C1 valore finale | Risolto | VF0, VFs e VFe; T10 verifica VF = 0 in cessione e diritto di superficie. |
| C2 T come decisione | Risolto | c\* è l'uscita principale, per T e per scenario VF. |
| C3 K1 asserzione | **In parte** (V1) | Θ_rov\* è calcolata, ma nel REPORT accompagna solo la quota di cessione, non c\*. |
| C4 nessuna geografia | Risolto | Avviso in testa alle tabelle; conteggi soppressi per la cessione e per ds con α = 0. |
| C5 analisi mancanti | Risolto | PRCC, quantili, tornado per lotto, sintesi per proprietà, D1, bonifiche, DCF: le tabelle esistono. |
| C6 η | **In parte** (V6) | Forbice allargata; fonte non trovata [L]. η resta decisivo. |
| C7 riuso | **In parte** (V3) | E6 è esteso al riuso, ma ρ ([V/I], un solo listino) è fuori dall'elenco proprio dove decide; il REPORT mescola le durate. |
| m1–m7 | Risolti | m4: K1b = 14.559 punti; m5: tre varianti di bonifica; m6: T11; m7: "errore non misurato". |

## 7.4 Difetto grave
**V1 — L'uscita principale (F-c) e la "lettura per la tesi" stanno solo nella regione tarata, contro la regola 1.12 e contro l'unica evidenza esterna.**

La regola 1.12 della pre-registrazione dice: se i bandi vanno deserti, "si riportano i risultati su Θ_rov accanto a Θ\*_cal", e "tutti i risultati" anche sul cubo Θ\*. Il REPORT lo fa solo per la quota di cessione. Per c\*, la grandezza che passa alla tesi, ho ricalcolato le tre regioni [V].

c\* con suolo gratuito, mediana (5–95%), in €/m²/anno:

| Regione | 30 anni | 60 anni | 90 anni |
|---|---|---|---|
| Θ\*_cal (REPORT) | 198 (153–243) | **130 (97–162)** | 108 (78–137) |
| Cubo Θ\* | 223 (160–307) | 148 (102–212) | 124 (83–185) |
| Θ_rov\* (bandi deserti) | 255 (211–324) | **172 (140–226)** | 147 (117–198) |

Il motivo è la taratura. K1 sposta Θ\*_cal verso parametri favorevoli alla cooperativa. Le mediane di η, c_new e δ sono:
- 0,887 / 1.945 / 0,0087 in Θ\*_cal;
- 0,805 / 2.273 / 0,0104 in Θ_rov\*.

La direzione della lettura non cambia: 90 €/m² non basta in nessuna delle tre regioni. Cambia però il numero, e quello del REPORT ("pareggio ≈ 130") è il più favorevole alla cooperativa dei tre. Lo è proprio nella regione che i bandi deserti [S] mettono in dubbio.

Correzione, senza rieseguire il calcolo:
- F-c riportato sulle tre regioni;
- la lettura per la tesi scritta come intervallo: "130–172 €/m²/anno a 60 anni secondo la regione";
- c\* per regione aggiunto come uscita dello script, in un file nuovo, così le tabelle esistenti e il loro hash restano invariati. L'aggiunta va registrata nel registro come modifica di sola uscita dopo l'esecuzione.

## 7.5 Da correggere (non fatali)
- **V2. E7 dipende da H14.** Il rapporto 0,86 con l'asta del 2023 è prodotto dal premio del nuovo π_new (mediana circa 0,2 in Θ\*_cal), cioè dalla scelta presa sapendo che +20% portava il VRA di D/E da 189 a 634 (v1). Con π_new = 0 il rapporto è 0,20; con π_new = 0,40 è 1,51 [V]. Va scritto in §5 e §6: "l'acquisto in fascia D è informativo **solo se** il nuovo costa il 15–40% più dell'OMI OTTIMO". Le ancore sono [S], prezzi d'annuncio e listino non aperto. Inoltre la soglia 0,5 e il confronto con un prezzo di diritti volumetrici ([S], Il Giorno) restano scelte [H].
- **V3. Recupero: il REPORT mescola le durate.** In §4 si legge "recupero in cessione a 90 anni 0,46; con ρ < 0,8 circa 0,51, con ρ > 1,0 circa 0,01". Le classi di ρ in `esito_criteri.json` (`recupero_per_rho`) sono però calcolate a **60 anni**. Valori corretti [V]:

  | Durata | Totale | ρ < 0,8 | ρ 0,8–1,0 | ρ > 1,0 |
  |---|---|---|---|---|
  | 60 anni | 0,21 | 0,51 | 0,11 | 0,01 |
  | 90 anni | 0,46 | 0,86 | 0,40 | 0,12 |

  Inoltre le celle E6 di "R1, cessione, c₀ 90" non sono robuste: a 90 anni dipendono da σ; a 60 anni c_new ribalta il 100%. Il parametro che decide, ρ, è fuori dall'elenco E6. La quota del recupero va dichiarata "non robusta, dipende da ρ e dai costi".
- **V4. F-a è vera ma quasi vuota, e incompleta nella forma.**
  - La forma pre-registrata chiede "sempre con le condizioni VF e il vincolo r ≥ 0,5 punti"; il REPORT non le scrive.
  - Nel merito, la cooperativa non regge **nemmeno con suolo gratuito** nel 98% di Θ\*_cal a 60 anni (cessione 0,0206; 0 in Θ_rov\*). Quindi "non paga il suolo di mercato" segue da "non copre i costi" e non dice nulla sul suolo.
  - Con VFe (valore finale dell'edificio) la quota in fascia D è 0,088, cioè regge nel 9% dei casi e non nell'1%.

  Formulazione proposta [I]: "a c₀ = 90 e T = 60 la cooperativa non copre i costi nemmeno con suolo gratuito nel 98% di Θ\*_cal (100% di Θ_rov\*); con suolo a mercato, nelle fasce B, C e D, in oltre il 99% con VF0 e VFs e nel 91% con VFe".
- **V5. Θ_rov\* e la quota "0 nella regione dei bandi deserti" sono quasi per costruzione.**
  - L'operatore K1 ha gli stessi costi, lo stesso η, lo stesso δ e lo stesso r della cooperativa, più le funzioni libere e i canoni di mercato dopo 30 anni. Se l'operatore con sussidi incrociati è in perdita, una cooperativa a 90 €/m² senza sussidi lo è quasi necessariamente. Lo 0,000 è quindi un'implicazione del modello, non un'evidenza indipendente: va scritto così, come per F-d.
  - La definizione ("VAN < 0 in almeno un compendio") si sovrappone a Θ\*_cal in 1.349 punti.
  - I bandi possono andare deserti anche per cause fuori dal modello (rischio, bancabilità, liquidità), quindi Θ_rov\* è a sua volta [I].
  - L'esito dei bandi è [S]: due articoli aperti e un risultato di ricerca. La mia ricerca del 23/11 lo conferma, ma sempre da stampa (Il Foglio 05/09 e 01/11/2026, Il Sole 24 Ore); nessuna fonte comunale [L].
- **V6. η resta il parametro più forte e non ha fonte.**
  - Nel PRCC sulla cessione vale −0,82.
  - Ribalta il 100% della cella F-b.
  - La quota di cessione a 90 anni per terzi di η in Θ\*_cal è 0,07 (η 0,70–0,80), 0,14 (0,80–0,90) e 0,24 (0,90–1,00) [V].
  - K1 spinge η verso l'alto (mediana normalizzata 0,62). L'estremo 1,00, che favorisce la cooperativa, è stato aggiunto nella v2 conoscendo la v1.
  - Serve la fonte su superficie commerciale e SL: NdA del PGT 2030 e DPR 138/1998.
- **V7. La promessa della §0(ii) non è mantenuta per intero.** La §0 promette "ogni scelta nella direzione della cooperativa affiancata da una variante opposta con lo stesso peso". Non è così:
  - η = 0,70 compare solo come c\* al punto base (154), non come quote;
  - i_E reale fino a −2%, cioè capitale dei soci a rendimento nominale 0, favorisce la cooperativa (PRCC 0,72) e non ha una variante opposta;
  - π_new = 0 non è riportato.

  Giudizio complessivo sulla non-cecità [I]. Le scelte prese conoscendo la v1 vanno quasi tutte **contro** la cooperativa (tassi reali, π_new, Θ_rov), salvo η e i_E. La conclusione di direzione (90 non basta) è quindi robusta alla non-cecità; i numeri no. Il caso più netto è E7 (V2): l'esito del criterio è determinato da una scelta informata.
- **V8. E6 è robusto solo rispetto all'elenco.** `E6_celle.csv` contiene già i ribaltamenti di tutti i parametri. Va aggiunta una colonna "robusta anche fuori elenco", dichiarata come informativa (l'elenco è pre-registrato e non si cambia). Va scritto che il test è a un parametro alla volta, al punto base.

## 7.6 Minori
- **n1.** La "lettura per la tesi" del §8 è fuori dalle formulazioni F-a…F-f. Dice che "il divario si chiude con durate molto lunghe", ma a 90 anni c\* mediano vale 108 > 90 in Θ\*_cal e 147 in Θ_rov\*. Va riscritta a partire da F-c.
- **n2.** DCF del developer: in fascia E il segno cambia (VRA statico −132, flusso di cassa +15 al punto base). "Conferma l'ordine di grandezza" vale per B–D, non per E.
- **n3.** In VFs, L_acq viene dal ramo developer, che è nominale, ed è usato come valore reale costante. È una piccola incoerenza tra nominale e reale: va dichiarata.
- **n4.** La taratura taglia solo il 42,5% di Θ\*: è un vincolo debole. Con K1b (14.559 punti) diventa ancora più debole.
- **n5.** Il nome del parametro in `param_max_E6`, a parità di valore, è scelto in ordine alfabetico: è solo una questione di forma.
- **n6.** Deviazione di processo ripetuta, la terza dopo Base L v7 e Base P: H1–H19 sono accettate dal coordinatore e non da Dennis.

## 7.7 Peso delle tre questioni richieste
- **Non-cecità sulla v1.** È dichiarata (§0) e documentata, e le correzioni sono quelle chieste dalla revisione. Pesa poco sulla direzione delle conclusioni e molto su due numeri: E7 (V2) e il c\* di Θ\*_cal (V1, V6). Non è fatale, perché la pre-registrazione v2 ha hash, precede il codice ed elenca ciò che l'autore sapeva.
- **Bandi deserti (solo stampa).** Bastano per attivare la regola 1.12 come scritta, che però parla di bandi "deserti", mentre al terzo giro ci sono state 2 offerte su 3 aree: l'applicazione è difendibile ma va dichiarata. Non bastano per sostituire K1 come misura. La conseguenza corretta è riportare le due regioni con lo stesso peso, cosa che il REPORT non fa per c\* (V1).
- **Scelte provvisorie H1–H19.** Quelle che decidono gli esiti sono:
  - H14 (π_new) → E7;
  - H15 (η) → F-b e c\*;
  - H11 (i_E, i_D) → strati e c\*;
  - H17 (K1a) → dimensione di Θ\*_cal.

  H12 (vincolo su r) cambia poco (0,17 contro 0,21); H18 (y_exit 3%) conta solo per VFe. Finché Dennis non le conferma, la base è una "candidata" e non una base congelata.

## 7.8 Le formulazioni F-a…F-f
- **F-a**: sostenuta, ma va riformulata come in V4.
- **F-b**: correttamente non ammessa.
- **F-c**: sostenuta solo con le tre regioni (V1).
- **F-d**: sostenuta, con la precisazione di V5.
- **F-e**: sostenuta.
- **F-f**: sostenuta.

## 7.9 Condizioni per congelare
1. REPORT §4, §5 e §8 corretti: F-c su Θ\*_cal, Θ\* e Θ_rov\* (V1); F-a come in V4; recupero con le durate giuste e marcato "non robusto" (V3); E7 dichiarato condizionato a H14 (V2); Θ_rov\* come implicazione del modello (V5); lettura per la tesi riscritta (n1).
2. c\* per regione prodotto dallo script in un file nuovo, con la deviazione a registro. L'hash `024ac9ea…` delle tabelle esistenti resta invariato.
3. Colonna "robusta anche fuori elenco" in E6, informativa (V8).
4. Conferma, o modifica, di H1–H19 da parte di Dennis in `tesi/DECISIONI.md`. Se un intervallo cambia: pre-registrazione v3.
5. `VERSIONE.md` con gli hash e le avvertenze: taratura debole e contraddetta da fonti di stampa; errore non misurato; η senza fonte; nessun uso come vincolo in B0–B6.

## 7.10 Cosa deve decidere Dennis
- **(a) Congelare la v2 dopo le correzioni 1–3, o fare una v3.** Raccomando il **congelamento della v2**: il motore è riprodotto e verificato a mano, e i difetti restanti sono di resoconto. Una v3 servirebbe solo se Dennis cambia H14, H15 o H11.
- **(b) Quale regione per la tesi.** Raccomando di **riportarle tutte e tre** e di trattare Θ_rov\* come la lettura prudente. Oggi l'unica evidenza esterna, sia pure di stampa, va contro il segno di K1.
- **(c) H1–H19.** Raccomando la conferma, con due condizioni: cercare una fonte per η (H15); dichiarare H14 come scelta che decide E7.
- **(d) B0–B6.** Raccomando di mantenere l'esclusione della Base E come vincolo per lotto. c\* può entrare solo come informazione descrittiva, con la forbice tra le regioni.
- **(e) K1.** Rifare la taratura, in una nuova versione, quando ci sarà un'aggiudicazione con corrispettivo da fonte istituzionale. Raccomando di sì.

---
**Appendice — controlli rifatti** (seme 4519, N = 20.000; script nello scratchpad, fuori dal repo).
- Θ\*: r = D·i_D + (1 − D)·i_E ≥ 0,005.
- K1a con bonifica 0,25·(max − min) e soglia VAN ≥ −0,05·C nei tre compendi; Θ_rov\*: VAN < 0 in almeno uno.
- c\* = −L\*(0)/(L\*(1) − L\*(0)) con le formule riscritte dalla pre-registrazione §3.
- E7 con π_new fissato a 0 e a 0,40 sugli stessi punti: mediana sui lotti D/E (FAR 1) del VRA mediano su Θ\*_cal.
- Quote di cessione per terzi di η e di recupero per classi di ρ a 60 e 90 anni.
- Non verificato: esecuzione senza cache; fonti [S] (bandi, asta 2023, premio del nuovo, oneri); ordine interno del registro; assenza di codice anteriore alla pre-registrazione.

Fonti consultate dal revisore il 23/11/2026 [S]:
- [Il Foglio, 05/09/2026](https://www.ilfoglio.it/en/gran-milano/2026/09/05/news/builders-feedback-to-conte-following-the-latest-failure-of-the-tenders-for-the-housing-plan-figures-to-be-reviewed--406338)
- [Il Foglio, 01/11/2026](https://www.ilfoglio.it/gran-milano/2026/11/01/news/edilizia-popolarissima-gia-si-pero--411990)
- [Il Sole 24 Ore](https://en.ilsole24ore.com/art/milans-housing-plan-second-extension-granted-amid-difficulties-for-operators-AJHd4hx)

Ho letto solo i risultati della ricerca, non ho aperto gli articoli.
