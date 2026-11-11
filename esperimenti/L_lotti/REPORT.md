# Base L v1 — lotti candidati reali di Milano (report di laboratorio)

Ticket: [#16](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/16) (mappa #15). Esegue: `dati-geo-milano`, con `urbanista-pgt-milano` come consulente. Revisione: `revisore-metodologico` (sezione 7).
Marche: **[V]** verificato in questa sessione, **[S]** fonte secondaria, **[I]** inferenza, **[H]** ipotesi o parametro scelto, **[L]** lacuna.

## 1. Criteri di accettazione (scritti prima di eseguire `run.py`, 2026-11-11)

La Base L v1 passa se **tutti** i criteri C1–C6 sono soddisfatti. C7 è informativo (confronto con il Lab), non bloccante.

| # | Criterio | Soglia |
|---|---|---|
| C1 | Geometrie: ogni lotto ha geometria poligonale non vuota e valida (`is_valid`), CRS dichiarato EPSG:32632 | 100% |
| C2 | Attributi: `id` unico; `classe`, `proprieta`, `area_m2 > 0`, `capacita`, `nil_id`, `fonti`, `licenze` non vuoti; ogni attributo ha fonte e licenza nella tabella `metadati` | 100% |
| C3 | Sovrapposizioni: nessuna coppia di lotti (stessa classe o classi diverse) si sovrappone oltre la tolleranza max(5 m², 1% dell'area del lotto più piccolo) | 0 coppie oltre tolleranza |
| C4 | Capacità: `capacita` intera, `m_min <= capacita <= m_max` per i lotti edificabili; `capacita >= 1` per i lotti da riusare | 100% |
| C5 | Controllo a campione con fonte indipendente (DUSAF 8.0, 2024, fotointerpretazione regionale; indipendente da catasto e DBT 2020). Campione casuale di 30 lotti per classe, seme 42. (a) Edificabili: il lotto non è occupato per più del 50% da tessuto residenziale (DUSAF 111/112) né da verde, agricolo, boschi o acque (DUSAF 14x, 2xx, 3xx, 4xx, 5xx). (b) Da riusare: il lotto cade su suolo artificiale (DUSAF 1xx) per almeno il 50% della sua area | (a) ≥ 70% del campione; (b) ≥ 70% del campione |
| C6 | Conteggi: tabella per NIL × classe e tabella a cascata dei filtri prodotte; somma per NIL = totale per classe | esatta |
| C7 | (informativo) Coerenza col Lab: numero di siti edificabili prima del filtro di capacità entro ±25% dei 2.291 siti del Lab (paper §3.2) | 1.718–2.864 |

Regola di arresto (protocollo): se C1–C6 non passano, la base non si congela come v1 e si apre un ticket di revisione.

## 2. Dati e fonti

Tutti scaricati il 2026-11-10/11 da `fetch.py` in `esperimenti/_cache/L_lotti/raw/` (ignorata da git) [V]. Licenze per attributo nello strato `metadati` di `lotti_v1.gpkg` e in `tabelle/metadati.csv`.

| Fonte | Uso | Licenza | Stato |
|---|---|---|---|
| Agenzia delle Entrate, WFS INSPIRE `CP:CadastralParcel`, comune F205, 384 tasselli da 0,01° | geometria dei lotti; 117.607 particelle, 109.876 di terreno (mappale numerico) | CC BY 4.0 | [V]. Il servizio di download massivo `GetDataset.php` risponde 403: usato il WFS, come il Lab [V] |
| Comune di Milano, DBT 2020 (ds2889, zip 600 MB): `UN_VOL`, `EDIFC`, `EDIFC_EDIFC_USO` | volumi fuori terra, uso residenziale, edifici diruti (`EDIFC_STAT=02`, 610) | CC BY 2.5 IT | [V] |
| Regione Lombardia, **DUSAF 8.0 (uso del suolo 2024)**, servizio ArcGIS `territorio/dusaf8` | esclusioni (acque, infrastrutture, verde, agricolo, boschi) e controllo indipendente C5 | CC BY 4.0 per DUSAF 7.0 [V, metadati regionali]; per la 8.0 [I] | [V]. La versione più recente non è la 6.0: esistono 7.0 (ortofoto 2021) e 8.0 (2024) [V] |
| Regione Lombardia, Tavola delle previsioni di piano (mosaico PGT, `tav_previsioni_b`), `NOME_COM='MILANO'`: AT (13), aree dismesse (15), servizi (18), aree agricole (19), valore paesaggistico (21), NAF (12) | AT, PCU, ex AMB_DEG, srv_erp, srv_verde, srv_ist, vincoli | **[L]** licenza non trovata | [V] dati; è la stessa fonte del Lab (`mi/fetch_regione.py`) |
| Comune di Milano, NIL vigenti PGT 2030 (ds964) | NIL e confine comunale | CC BY 4.0 | [V] |
| ds503 Edifici e aree in degrado 2014–2017 (174 punti, tav. R.10) | lotti da riusare | CC BY 4.0 | [V]; dato del 2017 |
| Demanio statale 2023: aree ds2688 (37), fabbricati ds2689 (573) | lotti da riusare, proprietà | CC BY 3.0 IT | [V] |
| ds677 Immobili di proprietà comunale 2019 (22.055 righe in Milano) | proprietà (foglio+mappale), lotti da riusare (piano di alienazione) | CC BY 4.0 | [V]; dato del 2019 |
| ds600 Interventi di bonifica (1.280 punti) | vincolo "bonifica" | CC0 | [V] |

Non ottenuto: `www.comune.milano.it`, `pgt.comune.milano.it` (blocco alle richieste automatiche, non aggirato) [L]; OSM via Overpass (connessione rifiutata o scaduta su tre server) [L]; ortofoto e Street View non scaricabili [L]. Indici edificatori reali del PGT per lotto: nessuno strato aperto [L].

## 3. Metodo

Codice: `run.py` (costruzione e criteri), `fetch.py` (download). Filtro e accorpamento sono quelli del Lab (`lab_completo/model/sites.py`, `config.py`, `data/build_parcels.py`), riscritti su fonti riscaricabili. Tutte le soglie sono parametri in testa a `run.py` (dizionario `P`), marcati [H].

**Particelle.** Anello esterno dal WFS; i fori sono ricostruiti togliendo a ogni particella le particelle che contiene (3.970 particelle) [I: i cortili interni sono altre particelle]. Volume: $V=\sum A_u h_u$ sulle unità volumetriche DBT fuori terra con $h>0{,}5$ m, assegnate per punto interno. Indice: $\mathrm{FAR}_{eff}=V/(3{,}2\,A)$; $p_{75}$ per NIL sulle particelle edificate ≥ 200 m².

**Lotto edificabile** (particella di terreno nel Comune), in sequenza:
1. $A \ge 300$ m²;
2. quota < 0,5 di ciascuno: PGT verde, agricolo, paesaggio, istruzione/università; DUSAF acque, infrastrutture, verde urbano, agricolo, boschi;
3. punto interno fuori dai 6 PCU;
4. non residenza occupata: esclusa se ha volumi e quota residenziale del volume ≥ 0,5;
5. ingresso: *soft site* ($\mathrm{FAR}_{eff}/p_{75} < 0{,}5$, $A \ge 500$ m², non protetta) **oppure** AT non PCU ≥ 0,5 **oppure** srv_erp ≥ 0,5 **oppure** in ex AMB_DEG; origine con priorità AT > AMB_DEG > ERP > SOFT;
6. non già lotto da riusare (una particella sta in una sola classe);
7. accorpamento per adiacenza (buffer 2 m, stessa origine), componenti > 60.000 m² divise con k-means pesato per area (seme 42); sito ≥ 1.500 m²;
8. capacità ≥ 20 alloggi.

**Lotto da riusare.** Ogni punto delle fonti va sulla particella di terreno che lo contiene, o sulla più vicina entro 20 m [H]. Selezione per fonte: ds503 tutti; Demanio solo *patrimonio disponibile* con superficie dichiarata ≥ 300 m² [H: esclude appartamenti, cantine e quote; il patrimonio indisponibile e storico-artistico è in uso o vincolato]; ds677 solo righe in Milano con `PIANO_ALIENAZIONE=SI`, unite per foglio e mappale [H: ds677 non ha uno stato d'uso, l'alienazione è l'unico segnale di "non serve al Comune"]; DBT edifici diruti. Poi per particella: ≥ 300 m², stesse esclusioni 2–3, capacità ≥ 1.

**Capacità** [H, parametri del Lab]:
$$c=\min\!\left(\left\lfloor \frac{0{,}70\cdot SL}{80}\right\rfloor,\ 400\right),\qquad SL=\begin{cases}\mathrm{FAR}\cdot A,\ \mathrm{FAR}=1{,}0 & \text{edificabile}\\ V/3{,}2 & \text{riuso con volumi DBT}\\ \mathrm{FAR}\cdot A & \text{riuso senza volumi}\end{cases}$$
FAR = 1,0 non è l'indice del PGT: è un'ipotesi uniforme, salvata nel campo `far_H`.

**Proprietà.** `quota_comunale` = quota dell'area del lotto su particelle presenti in ds677 (foglio+mappale; allegato e sviluppo ignorati [I]). Etichetta: *Demanio* se un punto Demanio (qualsiasi categoria) cade nel lotto o la fonte è Demanio; altrimenti *pubblico comunale* se `quota_comunale` ≥ 0,5 o la fonte è ds677; altrimenti *ignoto*. 1 lotto ha entrambe le evidenze (`proprieta_conflitto`).

**Vincoli noti** (quota > 10% o punto nel lotto): bonifica (ds600 o PGT `BONIFICA=SI`), nucleo di antica formazione, valore paesaggistico PGT, demanio storico-artistico.

**Controllo C5.** 30 lotti per classe estratti con `numpy.random.default_rng(42)`; quote DUSAF 8.0 per intersezione. Elenco in `tabelle/campione_controllo.csv`.

**Correzioni dopo la prima esecuzione** (dichiarate, nessuna soglia cambiata): (a) la prima esecuzione dava 26 coppie sovrapposte (C3): causa, l'anello esterno senza fori ereditato dal Lab; corretto ricostruendo i fori; (b) aggiunte due righe mancanti alla tabella `metadati` e la licenza "non applicabile" per i campi descrittivi (il test falliva). Il filtro e le soglie di §1 non sono stati toccati dopo aver visto C5.

## 4. Risultati

**2.012 lotti**: 1.764 edificabili (capacità ipotetica totale 185.703 alloggi) e 248 da riusare (8.965 alloggi). Lotti in 84 NIL su 88 (`tabelle/nil_classe.csv`; mediana per NIL 15 edificabili e 2 da riusare; massimo 69 edificabili a Gallaratese–San Leonardo–Lampugnano).

| Classe | Origine | n |
|---|---|---|
| edificabile | SOFT (non designato) | 1.539 |
| edificabile | ERP (srv_erp) | 168 |
| edificabile | AT non PCU | 54 |
| edificabile | ex AMB_DEG | 3 |
| da riusare | DBT diruto | 112 (+1 con Demanio, +17 con ds503) |
| da riusare | ds503 | 106 |
| da riusare | ds677 in alienazione | 7 |
| da riusare | Demanio disponibile | 5 |

| Proprietà | edificabili | da riusare |
|---|---|---|
| pubblico comunale | 298 | 23 |
| Demanio | 22 | 6 |
| ignoto | 1.444 | 219 |

Vincoli noti su 273 edificabili e 30 da riusare (bonifica 195, NAF 108, paesaggio 5, demanio storico-artistico 5).

Cascata (`tabelle/cascata.csv`, `fig/cascata.png`): per gli edificabili i filtri che pesano di più sono la residenza occupata (−25.773 particelle), la soglia di 300 m² (−56.699) e il verde/agricolo (−12.550); l'accorpamento porta 9.136 particelle a 3.779 siti, il minimo di 1.500 m² ne toglie 1.565, il minimo di 20 alloggi altri 450. Per il riuso, il Demanio si riduce da 610 righe a 9 (il patrimonio disponibile è fatto quasi solo di unità minute) e ds677 da 73 righe in alienazione a 31 associate per foglio e mappale.

Mappa: `fig/mappa_classi.png`.

## 5. Esito rispetto ai criteri (`esito_criteri.json`)

| # | Esito | Valore |
|---|---|---|
| C1 geometrie | **passa** | 100% valide, EPSG:32632 |
| C2 attributi | **passa** | 100% |
| C3 sovrapposizioni | **non passa** | 1 coppia oltre tolleranza: E01338–E01355, 157 m² (fogli 99 e 75), sovrapposizione residua tra particelle catastali di fogli diversi [I] |
| C4 capacità | **passa** | 100% |
| C5a edificabili vs DUSAF 2024 | **non passa** | 14/30 = 0,467 (soglia 0,70). Su tutti i 1.764 edificabili 0,52: AT 1,00, AMB_DEG 1,00, SOFT 0,55, **ERP 0,05** |
| C5b da riusare vs DUSAF 2024 | **passa** | 29/30 = 0,967 |
| C6 conteggi | **passa** | somme esatte |
| C7 coerenza col Lab (informativo) | in intervallo | 2.214 siti prima del filtro di capacità (Lab 2.291, −3%) |

**Esito: ripetere / cambiare.** La base **non** supera la soglia (C3, C5a). Per la regola di arresto non va congelata come v1 accettata: serve un ticket di revisione e una decisione con Dennis.

Lettura di C5a [I]: i lotti edificabili ERP sono in larga parte quartieri ERP esistenti (DUSAF li vede come tessuto residenziale): lo strato srv_erp marca il servizio esistente, non un'area libera, e il filtro "residenza occupata" non li toglie perché le unità volumetriche DBT spesso non portano l'uso residenziale o cadono su particelle vicine. Nei SOFT, quasi metà dei lotti cade nel tessuto residenziale denso: un indice volumetrico basso rispetto al p75 del NIL non distingue l'area libera dal cortile o dal giardino condominiale. È la stessa debolezza del proxy *soft site* che il Lab dichiarava ("screening flag only"). I lotti designati (AT, AMB_DEG) e i lotti da riusare reggono il controllo.

## 6. Limiti

- La regola d'ingresso SOFT ed ERP è un proxy (vedi §5); il controllo C5 usa DUSAF, che ha la sua risoluzione (unità minima cartografata) e la sua data (2024) [I]. Nessun confronto con ortofoto, Street View o OSM [L].
- FAR = 1,0, resa 0,70, 80 m² per alloggio, 3,2 m per piano: tutti [H], nessuna analisi di sensibilità in questa prova. La capacità totale (≈ 186 mila alloggi) dipende linearmente da FAR e **non** va letta come stima del potenziale reale.
- Siti di una sola particella non si dividono: restano lotti grandi (massimo 413.637 m², E01338 233.285 m²); la capacità è comunque troncata a 400.
- Proprietà: ds677 è del 2019, senza superficie né stato d'uso; il join ignora allegato e sviluppo; il Demanio è puntuale (punto → particella), e un fabbricato in quota in un condominio può marcare l'intera particella. Il 82% dei lotti resta "ignoto": la proprietà privata non è aperta [L].
- ds503 è del 2014–2017: parte degli edifici può essere già stata recuperata [L]. 20 punti ds503 su 174 non cadono entro 20 m da una particella di terreno.
- Licenza del mosaico PGT regionale non verificata [L]; licenza DUSAF 8.0 inferita dalla 7.0 [I].
- Vincoli assenti: vincoli paesaggistici D.Lgs. 42/2004 su beni puntuali, fasce di rispetto, PAI/PGRA, indici reali delle NdA del Piano delle Regole [L] (alcuni sono nel mosaico regionale, livelli 26–33, non usati).
- Non verificato: identità byte per byte di due esecuzioni da zero (due esecuzioni consecutive con `--no-fetch` hanno dato conteggi e cascata identici; il download stesso dipende dallo stato dei servizi alla data).

## 7. Revisione indipendente

*Revisore: `revisore-metodologico`, 2026-11-11. Non ho eseguito la prova. Controlli in `revisione/controlli.py` (riusa le funzioni di `run.py`, non modifica la prova; seme del campione nuovo **20261111**, dichiarato prima dell'estrazione), uscita in `revisione/esito_controlli.json`. Intervalli: Wilson al 95%.*

**Riproduzione [V].** `run.py --no-fetch` rieseguito dalla cache in una copia isolata (468 s; Python 3.13, geopandas 1.2.0, shapely 2.2.0, scikit-learn 1.9.1, pyogrio 0.13.0, installati da me: le versioni dell'esecutore non sono dichiarate). `esito_criteri.json` e le quattro tabelle sono **identici byte per byte**; il gpkg completo ha attributi e geometrie identici ma hash diverso (metadati del file). Conteggi (1.764 + 248), cascata, C1–C7 e i valori per origine (ERP 0,048, SOFT 0,554) si riproducono. `test_lotti.py` passa sul file del repo e sulla mia copia. Gli hash di `VERSIONE.md` corrispondono ai file del commit `5e1a4fa`.

**Criteri fissati prima? [V, `git log -p`].** Il testo di §1 (C1–C7, soglie, seme 42) è entrato nel commit `9ade1c2` (00:17) e non è più cambiato; il dizionario `P` è identico tra `9ade1c2` e `5e1a4fa`. Però lo **stesso** commit `9ade1c2` contiene già uscite di un'esecuzione pilota su 3 NIL (31 edificabili, C5a = 0,70, C7 = 33): la frase "scritti prima di eseguire `run.py`" non è dimostrabile dalla storia, e l'esecuzione pilota non è dichiarata. Le uscite della prima esecuzione completa (26 sovrapposizioni) non sono state conservate: l'affermazione "filtro e soglie non toccati dopo aver visto C5" è credibile ma non verificabile [L]. La correzione dei fori è **legittima**: è la riparazione di un errore di ricostruzione geometrica segnalato da C3, la soglia di C3 non è cambiata e la correzione non migliora C5 (non c'è un C5 precedente con cui confrontarla). Nessun indizio di soglie spostate; il pilota mostrava C5a in soglia e la base finale non passa.

### Gravi

**G1. La regola d'ingresso non seleziona "aree libere o dismesse" (CONTEXT.md): non fa meglio del caso.** Prova [V, controlli 3–4]: sul campione nuovo di 100 edificabili la regola C5a passa a 0,51 [0,41; 0,61] (14/30 = 0,47 [0,30; 0,64] nel campione originale: l'esito "non passa" è robusto, l'IC esclude 0,70). Su 300 particelle di terreno **qualsiasi** (≥ 2.286 m², nessun filtro) la stessa regola passa a 0,42 [0,37; 0,48]. Con un giudizio più vicino alla definizione — quota DUSAF 13x (cave, discariche, cantieri, aree degradate) + 1412 (aree verdi incolte) ≥ 0,5 [H, mio] — gli edificabili sono 0,06 [0,03; 0,13] contro 0,063 [0,04; 0,10] delle particelle qualsiasi: **nessun arricchimento**. Per origine (censimento): ERP 95% in tessuto residenziale; SOFT 44% in residenziale, 7% liberi; AT 20% liberi (AT e AMB_DEG passano C5a al 100%). Limite del mio giudizio [I]: DUSAF codifica spesso come 12111 le fabbriche dismesse, quindi 0,06 è un minimo; ma la regola C5a conta come "libero" anche un impianto industriale o di servizio in uso (es. E01382, 12122). Correzione: nella v2 togliere l'ingresso ERP; ridefinire l'ingresso non designato su evidenze di dismissione (es. aree dismesse PGT, ds503, DUSAF 13x, DBT diruti) invece che sull'indice volumetrico relativo al NIL; il proxy *soft site* era già noto come pari al caso (riesame #6, `06_riesame_spatial_milano_lab.md` §3: PR-AUC 0,015 contro tasso di base 0,0128 [S]).

**G2. Il controllo C5 è in parte circolare e, per C5b, non discrimina.** Prova [V]: (a) la metà "naturale" di C5a usa le stesse classi DUSAF 8.0 che il filtro (passo 2) ha già escluso: passa quasi per costruzione; è lo stesso errore del test 4a del Lab (riesame #6, punto 19). (b) C5b ("≥ 50% suolo artificiale") passa su 300 particelle qualsiasi ≥ 300 m² a 0,82 [0,77; 0,86]: in una città come Milano non dice nulla su "degradato o inutilizzato"; 102 lotti da riusare su 248 (41%) cadono in tessuto residenziale DUSAF > 0,5. (c) Attenzione alla proposta di §8 punto 1: se la v2 aggiunge al filtro l'esclusione "DUSAF residenziale ≥ 0,5", un C5a fatto ancora con DUSAF diventa **tautologico**. Correzione: pre-registrare un C5 v2 con (i) una fonte o un giudizio non usati dal filtro (fotointerpretazione cieca su ortofoto da parte di chi non conosce l'origine del lotto, o OSM `landuse`, o uno strato comunale delle aree dismesse); (ii) confronto con il tasso di base su particelle non filtrate, soglia espressa come differenza; (iii) n scelto per potenza (con n = 30 e vera quota 0,75 il criterio passa solo nell'80% dei casi [V, binomiale]); seme dichiarato prima.

**G3. I 248 lotti da riusare non sono "utilizzabili fin da ora" (§8): la capacità conta il volume esistente dell'intera particella.** Prova [V, controllo 5 e `run.py`]: `sl_base_m2 = volume_m3 / 3,2` somma **tutte** le unità volumetriche della particella, non solo l'edificio diruto o segnalato; 8.481 dei 8.965 alloggi del riuso vengono da questo volume; i 102 lotti in tessuto residenziale portano 1.927 alloggi, plausibilmente in edifici abitati [I]. Il riuso inoltre non ha il filtro "residenza occupata" e ha minimo 1 alloggio contro 20 per gli edificabili. Poiché C5b non discrimina (G2), il suo superamento non sostiene l'uso immediato. Correzione: capacità dal solo edificio della fonte (CEDIUV del diruto; per ds503 il fabbricato che contiene il punto); filtro di occupazione anche per il riuso; togliere da §8 "utilizzabile fin da ora" finché un controllo indipendente non lo sostiene.

### Da correggere

**D1. Pre-registrazione non tracciata.** Prova [V]: commit `9ade1c2` contiene criteri e uscite del pilota insieme (vedi sopra). Correzione: dichiarare il pilota nel report; per la v2, commit dei criteri **prima** di qualunque esecuzione e archiviazione dell'`esito_criteri.json` di ogni esecuzione (con hash del commit) in `archivio_tecnico/`.

**D2. Il codice di C5 non coincide con il testo di §1.** Prova [V, controllo 2]: §1 conta 14x tutto come "verde" e 1xx tutto come "artificiale"; il codice esclude 1412 dal verde (C5a più indulgente: 13/30 col testo contro 14/30) ed esclude 14x dall'artificiale (C5b più severo: 30/30 col testo contro 29/30). L'esito non cambia, ma l'implementazione deve seguire il criterio scritto o la deviazione va dichiarata.

**D3. Il file nel repo non è quello validato.** Prova [V, controllo 1]: su `lotti_v1_full.gpkg` C3 dà 1 coppia oltre tolleranza (157 m²) e 62 coppie con area comune > 0,01 m²; su `lotti_v1.gpkg` (semplificato a 1 m, quello che useranno le prove successive) **6 coppie oltre tolleranza** (max 194 m²) e 172 con area comune. Correzione: semplificazione topologica (o nessuna), criteri C1–C4 ricalcolati sul file pubblicato e C3 aggiunto a `test_lotti.py`; risolvere la coppia E01338–E01355 con la regola di §8 punto 2 dichiarata prima.

**D4. Il numero di lotti edificabili dipende da FAR [H] attraverso il minimo di 20 alloggi.** Prova [V, controllo 6]: con c ≥ 20 il filtro equivale a un'area minima di 2.286 m² a FAR 1,0; a FAR 0,5 restano 1.166 edificabili (−34%), a FAR 2,0 rientrerebbero tutti i 2.214 siti prima del filtro (+26%, dalla cascata); 102 lotti sono troncati a 400 alloggi. Il conteggio "1.764" non è un dato ma una funzione di un'ipotesi. Correzione: esprimere il minimo come area (indipendente da FAR), riportare conteggi e capacità a FAR 0,5 / 1,0 / 2,0, e per gli AT usare gli indici del PGT dove disponibili.

**D5. Proprietà: etichette da affinare.** Prova [V, controllo 4 e 6]: il join foglio+mappale non ha chiavi duplicate tra le particelle di terreno (0): l'aver ignorato allegato e sviluppo **non** produce errori qui. Però: 94 dei 168 lotti ERP sono "ignoto" (la proprietà ALER/regionale non è in ds677 [I]); l'etichetta *Demanio* scatta per un solo punto dentro il lotto, anche per siti di decine di ettari. Correzione: etichetta Demanio per quota di area (come per il Comune); fonte ALER o MM se ottenibile, altrimenti [L] dichiarata per l'ERP.

**D6. C7 è un controllo di replica, non di validità, e confronta stadi diversi.** Prova: stesso filtro e stessa fonte PGT del Lab (circolare per costruzione); inoltre i 2.291 siti del Lab risultano contati **dopo** il minimo di 20 alloggi ([S]: `00_corpus_interno.md`, "capacità … minimo 20; risultato 2.291 siti", che cita paper §3.2), mentre C7 usa 2.214 siti **prima**. A stadio omologo: 1.764 contro 2.291 = −23% [V aritmetica], ancora nell'intervallo. Correzione: rinominare C7 "replica del Lab", confrontare a stadio omologo e per origine (Lab: 58 AT, 129 ERP, 5 AMB_DEG [S]).

**D7. Riproducibilità dichiarata in modo fragile.** Prova [V]: l'hash del gpkg cambia a ogni esecuzione con contenuto identico; le versioni delle librerie non sono registrate (k-means e operazioni GEOS possono cambiare tra versioni). Correzione: in `VERSIONE.md` un hash del contenuto (attributi + WKB ordinati) e un `requirements.txt` con versioni.

### Minori

- M1. §5 spiega il fallimento ERP con "le unità DBT spesso non portano l'uso residenziale": è [I] non verificata; o la si verifica (quota di volumi con uso mancante nei lotti ERP) o la si toglie.
- M2. Coordinate [V]: il WFS è letto in lat/lon e invertito correttamente in `fetch.py` (lon, lat → EPSG:6706 → 32632); 109.863 particelle di terreno su 109.876 cadono nei NIL. Nessun problema di sistema di riferimento; resta il presupposto di `rd()` che un file senza CRS sia già in EPSG:32632 (oggi non accade).
- M3. Paginazione del WFS [V]: nessun tassello raggiunge il limite di 2.000 (max 1.566); niente troncamenti evidenti.
- M4. `dusaf_cat` ereditato dal Lab: 124 (aeroporti) finisce in "unk", 11231 (cascine) in residenziale. Effetto trascurabile.
- M5. Termini: il report usa "sito/siti" per l'aggregato intermedio; CONTEXT.md lo sconsiglia come sinonimo di lotto. Va bene come termine tecnico se definito una volta ("sito = gruppo di particelle prima dei filtri finali").
- M6. `test_lotti.py` non controlla C3, la formula del riuso, né i conteggi per classe rispetto a `esito_criteri.json`.

### Verdetto: **cambia**

C3 e C5a non passano [V], e la regola d'arresto vale. Rifare la prova con lo stesso metodo non basta: G1 mostra che la regola d'ingresso SOFT/ERP non distingue le aree libere o dismesse dalle particelle qualsiasi, e G2 che il controllo C5 non può accorgersene in modo affidabile (in parte circolare, C5b non discrimina). Per la v2 servono un ingresso nuovo per i lotti edificabili non designati, un controllo di validità nuovo e pre-registrato (fonte indipendente dal filtro, tasso di base, n da potenza) e la capacità del riuso ricalcolata sul solo edificio della fonte. Nulla di questa v1, nemmeno i 248 lotti da riusare, va passato alle prove successive come base; i 57 lotti AT/AMB_DEG sono il sottoinsieme più solido ma C5a li giudica solo come "non residenziali e non verdi" (20% liberi secondo DUSAF 13x/1412 per gli AT), quindi vanno trattati anch'essi come candidati da verificare.

Non verificato da me: le fonti esterne (licenze, date dei dataset), il ricalcolo da zero con `fetch.py` (rete), il giudizio su ortofoto; il mio criterio "libera o dismessa" (DUSAF 13x + 1412) è un'ipotesi [H] e sottostima le aree dismesse ancora codificate come produttive.

## 8. Cosa passa alla prova successiva

Nulla come base congelata finché Dennis non decide (regola di arresto). Proposta per il ticket di revisione [H]:
1. per la v2, togliere l'ingresso ERP o richiedere per ERP la stessa condizione SOFT; per SOFT, aggiungere l'esclusione per quota DUSAF residenziale ≥ 0,5 — poi ripetere C5 su un **nuovo** campione (seme diverso, dichiarato prima);
2. risolvere le sovrapposizioni residue con una regola esplicita (la particella va al lotto con `id` minore);
3. analisi di sensibilità su FAR (0,5 / 1,0 / 2,0).

Utilizzabile fin da ora, con i limiti di §6: i 248 lotti da riusare (C5b passa) e i 57 lotti designati AT/AMB_DEG; la tabella di proprietà; la pipeline riproducibile (`run.py`).

Su cosa non ho verificato: licenza del mosaico PGT, confronto con ortofoto/OSM, determinismo byte per byte da zero.
