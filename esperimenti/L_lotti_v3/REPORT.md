# Report di laboratorio — Base L v3: ambiti di trasformazione prevalenti e terreni comunali confermati

Ticket: [Base L v3](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/35). Esecutore: agente dati-geo-milano (con urbanista-pgt-milano). Report assemblato dal coordinatore con il testo dell'esecutore (i sub-agenti non possono creare file di report).

## 1. Pre-registrazione
Testo integrale in `esecuzioni/00_preregistrazione.txt` (13:09Z dell'11/11/2026, hash `39e4c160…` in `00_preregistrazione.sha256`, commit `907e0ed` alle 13:18Z), prima di ogni esecuzione. Criteri C1–C8 come in v2, stesse soglie, seme 3511. Conflitto dichiarato prima: gli ambiti di trasformazione (AT) entrano anche se oggi in uso (D1), mentre C5 misura "libero o dismesso oggi".

## 2. Dati e fonti
Fonti di v1 e v2 dalla cache (catasto WFS CC BY 4.0, DBT 2020 CC BY 2.5 IT, DUSAF 8.0, mosaico PGT regionale licenza [L], NIL ds964, ds503, Demanio ds2688/2689, ds677, ds600, ds2813) [V]. Mosaico PGT: 30 AT di cui 6 PCU. `pgt_dism`: CONTAMINAZ sempre "Da verificare"; nessuna fonte aperta dice se una bonifica è risolta [L], quindi la bonifica è segnalata ma non esclude. Ortofoto AGEA 2018–2019 (Regione Lombardia ImageServer), licenza di sola visione [S], immagini non versionate. Corretto un errore ereditato da v2: il campo bonifica PGT è `DBONIFICA`, non `BONIFICA` (in v2 la quota di bonifica PGT era sempre 0).

## 3. Metodo
Regole di v2 più le sole modifiche v3: particelle AT (quota ≥ 0,5 di un AT non PCU) senza filtri DUSAF di uso attuale, salvo acque e filtri di piano; ds677 solo con quota ≥ 0,5 dei codici DUSAF {131, 132, 133, 134, 1412}; ds503 solo se diruto DBT o screening Q1 = D / tetto T2–T3. Filtro "residenza occupata" valido anche negli AT [H]. Screening ds503 cieco su 111 candidati (seme 3513, hash `e92d4f2d…`), confermati 31. Campione C5 cieco (C001–C200, hash `d4211b46…` prima dell'unione); cecità parziale (codificatore = esecutore; 4 lotti già visti nello screening: senza di essi C5a = 0,573). Registro completo in `esecuzioni/registro.txt`.

## 4. Risultati

| Classe | n | ha | FAR 0,5 | FAR 1 | FAR 2 | recupero |
|---|---|---|---|---|---|---|
| lotto edificabile | 245 | 548,8 | 23.888 | 47.898 | 95.913 | — |
| lotto da riusare | 171 | 68,5 | 2.904 | 5.903 | 11.899 | 2.973 |
| area di attivazione | 258 | 182,4 | 0 | 0 | 0 | — |

Edificabili per origine: AT 88 (323 ha), DUSAF 133/134 114, terreno comunale confermato 38, ex AMB_DEG 4, Demanio 1. Riuso: 130 diruti DBT, 26 ds503 confermati, 15 entrambi; scenario principale 134 demolizione e ricostruzione, 37 recupero. Proprietà ignota: 173/245 edificabili, 154/171 da riusare. 72 NIL su 88.

Copertura degli ambiti (ha coperti / totali, `tabelle/copertura_ambiti.csv`): Farini-Lugano 43,6/62,9; Lambrate 6,2/7,1; Rogoredo 1,9/2,1; Greco-Breda 5,7/7,2; San Cristoforo 15,4/17,2; Porta Genova 8,9/10,9; Romana 21,1/21,7; Piazza d'Armi 54,6/61,8; Porto di Mare 26,2/35,9. Totale AT non PCU 0,78 (358,3 ha su 455,9).

| # | Esito | Valore |
|---|---|---|
| C1–C4, C6 | passano | geometrie, attributi, 0 sovrapposizioni, capacità, conteggi |
| C5a ortofoto, 100 lotti | **non passa** | 0,58 [0,482; 0,672], soglia 0,70 |
| C5b differenza con la base | passa | base 0,11 [0,063; 0,186]; differenza 0,47 [0,346; 0,573] |
| C7 controllo di Dennis | in attesa | `controllo_umano/` |
| C8 riproducibilità | passa | hash `4f41a0af…` in tre esecuzioni |

C5 per origine: AT 0,29 (binari, stazioni, capannoni e uffici in uso); DUSAF 13 0,54; terreno comunale confermato 0,83 (v2: 0,11); diruti DBT 0,60; ds503 confermati 3/4. Senza AT: 0,64 [I]. Recuperabilità del riuso [H, screening visivo]: alta 7, media 10, bassa 4.

## 5. Esito
**Cambia.** C5a 0,58 sotto 0,70 (v2: 0,34); C5b passa con ampio margine. La base non si congela; decide Dennis.

## 6. Limiti
Conflitto dichiarato AT/C5; scarto temporale delle fonti (ortofoto 2018–2019, DUSAF 2024, ds503 2014–2017); codificatore = esecutore; regola R3 che trasforma intere particelle ferroviarie in lotti da riusare per un solo edificio diruto (es. R00047, Farini, 9,9 ha); mancano dati aperti su occupazione, proprietà ERP/ALER, stato delle bonifiche, indici reali del PGT, licenza e aderenza del mosaico PGT [L]; resa 0,70 e 80 m²/alloggio [H].

## 7. Revisione indipendente

Revisore-metodologico (11/11/2026, ~21:45–22:30Z). Non ho eseguito la prova. Non ho aperto `controllo_umano/chiave_da_aprire_dopo.csv` né `controllo_secondo_codificatore/`: l'accordo con il secondo codificatore lo calcola e lo riporta il coordinatore, e non entra in questa revisione. Sono un'altra istanza dello stesso sistema dell'esecutore, quindi questa non è una verifica fatta da persone (vedi `06_riesame_spatial_milano_lab.md` §0) [I]. Script in `revisione/`: `riesegui.sh` (riesecuzione su una copia), `c5.py`, `strutturale.py`, `sovrapposizione_v2.py`. La skill `ponytail` non era disponibile in questa sessione come strumento: ne ho seguito il principio (script minimi, nessuna dipendenza nuova).

### 7.1 Riproduzione [V]
- `run.py --no-fetch` rieseguito da cache su una copia fuori dal repo (21:41→21:49Z, 510 s). Hash del contenuto `4f41a0afb504…` identico; conteggi 245 / 171 / 258; C1–C4, C6, C8 veri, C5 falso. Le 8 tabelle in `tabelle/` (campione, cascata, esito ortofoto, copertura, attributi, metadati, NIL, chiave dello screening) sono identiche byte per byte. `esito_criteri.json` è identico salvo `registro`. Il gpkg ha un hash di file diverso (`2d03db…` contro `22f293…`, metadati GPKG) ma lo stesso contenuto: il riferimento corretto è l'hash del contenuto, come dice `VERSIONE.md`.
- `test_lotti.py` passa sull'originale e sulla copia. Gli SHA-256 di `VERSIONE.md` coincidono con i file (`lotti_v3.gpkg`, `run.py`, `test_lotti.py`, `esito_criteri.json`, tutte le tabelle).
- Report §4: i conteggi per origine, le aree (AT 323,0 ha), la proprietà e la copertura delle 9 voci citate corrispondono alle tabelle. Il totale 358,3 / 455,9 ha (0,78) è corretto.
- C5 ricalcolato da `controllo_ortofoto_esito.csv`: 58/100 = 0,580 [0,482; 0,672]; base 11/100 [0,063; 0,186]; differenza 0,470 [0,346; 0,574]. Il report dà 0,573: la differenza viene dall'arrotondamento di p prima del calcolo di Newcombe ed è irrilevante.

### 7.2 Pre-registrazione, cronologia, correzioni [V salvo dove indicato]
- Il testo della pre-registrazione nel commit `907e0ed` (13:18:56Z) ha lo stesso SHA-256 di oggi (`39e4c160…`). Il `run.py` usato nelle esecuzioni complete 2 e 3, cioè quelle che hanno prodotto il campione e C5, ha SHA `2f2197…`, uguale al file committato in `907e0ed`. Quindi regole, soglie e codice erano fissati in git prima della prima esecuzione completa (13:28Z) e prima che C5 fosse visto (13:56Z).
- La precedenza sui due piloti (13:12–13:14Z) si basa solo sul registro scritto a mano e sull'mtime del file (13:09:48Z), perché il commit è successivo ai piloti e li contiene [I]. Il rischio è basso: il pilota non produce immagini né C5.
- Le soglie e i parametri di `P` coincidono con v2, salvo i semi e `dusaf_conf_comune`, dichiarati. Nessuna regola o soglia è cambiata dopo C5. La sola modifica di codice dopo C5 è una riga (diff `907e0ed..d3d64f1`): svuota la colonna derivata `rimossi` della cascata per le righe di fonti e di ingresso. L'hash del contenuto non cambia (esecuzioni 3, 4 e 5) e C6 si calcola su `rimasti`, non su `rimossi`. È davvero una correzione di sola presentazione ed è stata registrata prima delle esecuzioni 4 e 5.
- Correzione `DBONIFICA` (dopo il pilota 2, prima di ogni esecuzione completa). Nel mosaico, `BONIFICA` è numerico (2 = 1.520, 1 = 137, 0 = 59) e `DBONIFICA` è testuale (NO / SI = 137) [V]. È un errore di codice puro ereditato da v2 e tocca solo `vincoli_noti` e `copertura_ambiti`, non le classi. È ammissibile. Il report di v2 andrebbe annotato: la sua quota di bonifica PGT è sempre 0.
- Gli hash delle codifiche manuali (screening `e92d4f2d…`, ortofoto `d4211b46…`) stanno solo nel registro: nessun commit tra la codifica e l'unione. L'integrità prima dell'unione è quindi auto-dichiarata [I].

### 7.3 Campionamento e C5 [V; interpretazioni I]
- Seme 3511 e allocazione 50/30/20 come pre-registrati. L'allocazione non è proporzionale alla popolazione (36 / 25 / 38 %): C5a descrive il campione, non i lotti. Stima post-stratificata per classe × AT: 0,621.
- C5 con e senza AT (Wilson 95 %; differenza con la base, Newcombe):

| Insieme | k/n | p [IC 95 %] | differenza con la base [IC] |
|---|---|---|---|
| tutti (pubblicato) | 58/100 | 0,580 [0,482; 0,672] | 0,470 [0,346; 0,574] |
| senza edificabili AT | 53/83 | 0,639 [0,531; 0,734] | 0,529 [0,397; 0,635] |
| senza ogni origine AT (anche attivazione AT) | 53/80 | 0,662 [0,554; 0,757] | 0,552 [0,419; 0,658] |
| senza AT e senza i 4 visti nello screening | 50/76 | 0,658 [0,546; 0,755] | 0,548 [0,412; 0,656] |
| solo AT | 5/20 | 0,250 [0,112; 0,469] | — |
| solo edificabili non AT | 20/33 | 0,606 [0,437; 0,753] | 0,496 [0,310; 0,651] |

  **Anche senza AT, C5a resta sotto 0,70.** Il conflitto D1/C5 non spiega da solo l'esito: DUSAF 133/134 (0,54) e i diruti (0,60) sono deboli di per sé. La stima post-stratificata dei soli lotti non AT vale 0,704. Non è la statistica pre-registrata e non va usata per dichiarare che "senza AT passa": sarebbe una soglia spostata dopo i dati, lo stesso errore di `06_riesame` §2 n. 5.
- Il report dice "AT 0,29" e "senza AT 0,64 [I]". È corretto ed equo, purché si dica che 0,64 esclude solo gli edificabili AT, non le 3 aree di attivazione di origine AT (tutte U/I).
- C5 per lotto, non per area: pesando per area i lotti del campione si ottiene 0,512 (edificabili 0,434). Gli AT sono pochi lotti molto grandi. Lo schema non dice come si codifica Q1 su un lotto di 10 ha in parte libero e in parte in uso [L].
- Indipendenza. Codificatore, esecutore e autore delle regole sono la stessa persona. `campione_ortofoto.csv` (la chiave codice → classe e origine) era già scritto su disco quando la codifica è iniziata (lo scrive l'esecuzione 2, prima della codifica) [V, codice]: la cecità è solo di disciplina.
  - Durata: i fogli C sono stati creati alle 13:45:13Z e la codifica è stata scritta alle 13:48:23Z, cioè circa 1 s per caso. Lo screening: circa 111 casi in meno di 3 minuti [V, mtime].
  - Coerenza interna: dei 4 lotti dello screening finiti nel campione, uno (R00113) ha Q1 = D nello screening e U in C5. Il "3/4" dei ds503 confermati non è quindi indipendente, e c'è anche un'incoerenza dello stesso codificatore.
  - Dipendenza non dichiarata: 10 lotti del campione v3 coincidono (IoU > 0,5) con lotti già codificati in v2 sulla stessa ortofoto. Q1 è uguale in 8 su 10 (R00100: U contro D in v2; R00113: U contro D) [V, `sovrapposizione_v2.py`].
  - Nessuna di queste cose può aver prodotto un falso "non passa" in modo sistematico. Ma l'esito di C5 si regge oggi su un solo codificatore non cieco: il controllo decisivo è l'accordo con il secondo codificatore, calcolato dal coordinatore.
- Il conflitto D1/C5 è stato dichiarato prima (pre-registrazione 1.3) ed è stato gestito correttamente: C5 è rimasto il criterio, senza ritocchi. Ma è un conflitto di costrutto, non di campione (vedi G1).

### 7.4 Rischi specifici [V numeri, I interpretazioni]
- **R3** (lotto da riusare = particella intera meno gli altri edifici): 55 lotti su 171 hanno un'area oltre 10 volte l'impronta degli edifici fonte. Valgono 48,8 ha su 68,5 e 4.238 alloggi su 5.903 a FAR 1. Rapporto mediano 4,4; 99° percentile 493.
  - R00047 (Farini, particella `F205_022100.106`, DUSAF infrastrutture 1,0): 9,87 ha, 863 alloggi a FAR 1, per un diruto di 2.496 m² di impronta.
  - R00106 (Greco-Breda): 2,25 ha per 14 m² di edificio. R00058 (Farini): 3,0 ha per 96 m².
  - 20 lotti da riusare (26,3 ha) stanno su particelle AT e, per la precedenza riuso > edificabile, tolgono quelle particelle agli edificabili AT (Farini: 12,85 ha da riusare).
- **Residenza occupata negli AT**: tra le particelle AT che passano i filtri precedenti (680), 89 sono tolte da questo filtro (34,0 ha; 915.306 m³ residenziali). Caserma Mameli 6,31 ha, Farini 8,41, Stephenson 6,29. Di queste, 11 hanno copertura edificata < 0,10, quindi la quota residenziale del volume classifica come "occupata" una particella quasi libera. La regola era pre-registrata [H], quindi l'applicazione è corretta, ma il suo effetto sugli AT va controllato caso per caso.
- **Particelle mancanti negli ambiti**: l'universo catastale copre 421,6 ha su 455,9 degli AT non PCU, quindi 34,3 ha (7,5 %) non possono diventare lotti in nessun caso. Farini: 49,7 su 62,9 (13,2 ha fuori). Via Messina: 0 su 3,18 ha, cioè ambito interamente fuori dall'universo. La causa non è verificata [L]: possibili sedimi ferroviari o particelle senza mappale numerico [I]. Il report §4 cita 9 ambiti su 24 non PCU e omette, tra gli altri, Bovisa (0,739) e Stephenson (0,699).
- **Funzione prevalente degli AT** (`DFUN_PREV1` del mosaico): Stephenson e Toffetti sono TERZIARIO, un poligono di San Cristoforo è SERVIZI. 15 lotti edificabili AT (45,0 ha) ricadono lì e portano 3.933 alloggi a FAR 1 (8,2 % degli edificabili) come capacità abitativa. Nel mosaico `SL` coincide con l'area del poligono (rapporto mediano 1,00) e `DSTR_ATT` vale ovunque "Non presente strumento attuativo di livello regionale". Dai dati aperti in cache non si ricavano quindi né l'indice né lo stato attuativo: servono le schede `AT_n_15146.pdf` [L].
- **Capacità**: le formule sono applicate come pre-registrate (C4 vero). Il test però ricalcola la stessa formula: verifica l'implementazione, non la plausibilità. La capacità di demolizione e ricostruzione del riuso eredita l'artefatto di R3.
- **Proprietà**: delle chiavi foglio+mappale di ds677 (MILANO = SI), solo il 71 % (TERRENO 72 %: 13.278 su 18.442) trova una particella di terreno nell'universo. "Ignoto" (173 su 245 edificabili) significa "non agganciato", non "privato". Il riscontro spaziale (punto ds677 dentro una particella con chiave uguale: 0,54) non decide, perché i punti sono geocodificati da indirizzo [I].
- **Bonifica**: la correzione è giusta. 137 poligoni hanno `DBONIFICA = SI` e Magazzini raccordati (1,00) e Stephenson (0,52) entrano con il solo segnale. È coerente con la pre-registrazione: lo stato di risoluzione manca come dato aperto [L].

### 7.5 Difetti
**Gravi**
- **G1. C5 non può validare gli AT: costrutto, non campione.**
  - Prova: D1 fa entrare suolo in uso; C5 misura "libero o dismesso" sull'ortofoto 2018–2019. Gli AT valgono 5/20. `CONTEXT.md` definisce il lotto edificabile come "area libera o dismessa": un AT in uso non rientra nella definizione.
  - La proposta (1b) del §8, una categoria Q1 "in trasformazione di piano", è circolare. Sull'immagine non si vede il piano: la si assegnerebbe riconoscendo il perimetro AT, cioè la regola d'ingresso. Contando ogni lotto AT come successo, C5a passerebbe da 0,58 a 0,73 [0,636; 0,807] senza alcun dato nuovo (`c5.py`, ultima riga).
  - Correzione: due costrutti e due controlli, decisi con Dennis e registrati in `CONTEXT.md`/ADR.
    - (a) C5 fisico invariato, soglia 0,70, solo sui lotti non AT, con nuovo campione e nuova pre-registrazione.
    - (b) Per gli AT, un controllo separato C9 sullo **stato attuativo da documenti**: censimento dei 24 poligoni non PCU, non un campione. Fonte con URL e data per ciascuno (scheda AT, accordo di programma o piano attuativo, titolo edilizio, cantiere). Categorie pre-registrate: non avviato / strumento approvato / in cantiere / attuato. Due codificatori. Soglia: 100 % degli AT con stato e fonte. Ogni lotto AT riceve gli attributi `stato_attuativo` e `disponibile_da` (oggi / dopo l'attuazione).
    - Il C5 fisico degli AT resta solo informativo, come misura dello scarto temporale.
    - In alternativa, un termine nuovo nel glossario (es. "lotto di piano") distinto dal lotto edificabile.
- **G2. R3 genera lotti da riusare che sono interi sedimi.**
  - Prova: 7.4. Il 71 % dell'area e il 72 % della capacità a FAR 1 del riuso viene da lotti oltre 10 volte l'impronta della fonte. R00047 vale 863 alloggi per un diruto in uno scalo.
  - Correzione: il perimetro del riuso diventa l'impronta della fonte più un intorno fisso pre-registrato [H, con sensibilità], intersecato con la particella. Il resto di una particella AT torna all'ingresso AT. Un tetto al rapporto area/impronta va riportato come controllo.

**Da correggere** (bloccanti per una v4 se non risolti)
- **D1. `run.py` è distruttivo verso i controlli in corso.** `secondo_codificatore()` riscrive sempre `codifica_secondo.csv` vuoto. `controllo_umano()` riscrive sempre `modulo_dennis.csv` vuoto e la chiave. Rieseguire `run.py` nella cartella cancellerebbe il lavoro del secondo codificatore e le risposte di Dennis [V, codice]. Correzione: scrivere solo se il file non esiste. Fino ad allora, rieseguire solo su copia (`revisione/riesegui.sh`).
- **D2. C5 deciso da un solo codificatore non cieco** (7.3: chiave su disco, circa 1 s per caso, incoerenza R00113, 10 lotti già codificati in v2 non dichiarati). Correzione per v4:
  - il C5 che decide è quello del codificatore indipendente, o il consenso dopo l'accordo;
  - la chiave viene scritta solo dopo l'hash della codifica;
  - l'hash della codifica va committato prima dell'unione;
  - si escludono o si dichiarano i lotti già visti (v2, screening);
  - si registra la durata della codifica.
- **D3. Unità di misura di C5.** Va definito come si codifica un lotto grande ed eterogeneo, per esempio Q1 prevalente per area o k punti casuali per lotto. Va riportato anche il C5 pesato per area (0,51).
- **D4. AT non residenziali**: 3.933 alloggi a FAR 1 su AT a prevalenza terziaria o di servizi. Correzione: escluderli o pesarli con `PERCRES`/SL delle schede [L], con una regola pre-registrata.
- **D5. Residenza occupata negli AT**: verifica delle 89 particelle (34 ha), con priorità alle 11 con copertura < 0,10 e alle caserme.
- **D6. Universo incompleto negli AT** (34,3 ha, via Messina assente): diagnosticare la causa sul catasto. La tabella di copertura completa (24 righe) va nel report, non una selezione.
- **D7. Semantica della proprietà**: "ignoto" va rinominato o documentato come "non agganciato a ds677/Demanio" e va riportato il tasso di aggancio (72 %).

**Minori**
- La pre-registrazione dice "Scritto: 13:10Z", ma l'mtime è 13:09:48 e il registro dice 13:09Z.
- La pre-registrazione dice "BONIFICA = SI in 137" e "1.657 poligoni": in realtà il campo è `DBONIFICA` e i poligoni sono 1.716, di cui 59 ex AMB_DEG senza CONTAMINAZ.
- Nella cascata, `rimossi` è ancora riempito su righe di aggregazione ("particelle con edifici fonte": 86; "gruppi per adiacenza": 1.010), che non sono filtri.
- Lo `scenario_principale` dei lotti da riusare campionati dipende dalla codifica C5. Il trattamento non è omogeneo tra lotti campionati e non campionati e cambia l'hash tra le esecuzioni 2 e 3.
- Il test di C4 è tautologico (vedi 7.4).
- L'IC di Newcombe va calcolato su p non arrotondato.

### 7.6 Verdetto
**Cambia.** Concordo con l'esecutore. Ripetere con lo stesso disegno non serve: il conflitto D1/C5 resterebbe e C5a fallisce anche senza AT (0,64–0,66). La base non si congela (regola di arresto: G1 e G2 sono gravi; decide Dennis).

Su come C5 deve trattare gli AT: raccomando la via (a)+(b) di G1, cioè C5 fisico sui soli non AT più un controllo separato dello stato attuativo da documenti. Sconsiglio la categoria Q1 "in trasformazione di piano", perché è circolare.

Per v4 servono: G1, G2, D1–D7, una nuova pre-registrazione con un nuovo seme e un'ortofoto più recente se il servizio la rende disponibile. Riutilizzabili come sono: pipeline, registro, screening ds503 (salvo D2), tabella di copertura.

Non verificato da me: il contenuto delle immagini (non ho ricodificato), la causa delle particelle mancanti, i documenti attuativi degli AT, l'accordo con il secondo codificatore e C7.

### 7-bis. Secondo codificatore cieco e accordo (coordinatore)
Dettaglio in `controllo_secondo_codificatore/ESITO.md` e `accordo.json`. Secondo codificatore in cartelle isolate (solo immagini e istruzioni), hash dei fogli registrati prima del confronto. Accordo binario 0,90 (kappa 0,785), su Q1 a 7 categorie 0,835 (kappa 0,768). C5a con il secondo codificatore: 0,65 [0,553; 0,736]; con entrambi d'accordo sul sì: 0,55 [0,452; 0,644]. Base: 0,12. AT: 0,41 [0,22; 0,64]. Poiché il revisore (D2) rileva che il primo codificatore non era pienamente cieco, la stima di riferimento è quella del secondo codificatore: anche con essa C5a resta sotto 0,70.

## 8. Cosa passa
Nulla come base congelata. Proposte [H] per Dennis: (1) come C5 tratta gli AT — valutarli con lo stato attuativo del piano letto sui documenti, oppure una categoria Q1 "in trasformazione di piano" (nuova pre-registrazione); (2) ortofoto più recente per DUSAF 13; (3) perimetro dei lotti da riusare nelle grandi particelle ferroviarie limitato a un intorno dell'edificio; (4) attendere l'accordo con il secondo codificatore e C7. Riutilizzabili: pipeline, registro, schema di codifica, screening ds503, tabella di copertura.
