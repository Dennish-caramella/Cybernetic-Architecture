# Report di laboratorio — Base L v2: lotti edificabili, da riusare e aree di attivazione

Ticket: [Base L v2](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/34). Esecutore: agente dati-geo-milano (con urbanista-pgt-milano). Report assemblato dal coordinatore con il testo dell'esecutore (lo strumento di scrittura dei sub-agenti non permette di creare file di report).

## 1. Ipotesi, criteri e piano di campionamento (pre-registrati)

Testo integrale in `esecuzioni/00_preregistrazione.txt`, scritto alle 09:49Z dell'11/11/2026 prima di qualsiasi esecuzione (prima esecuzione pilota 09:55Z); hash SHA-256 in `esecuzioni/00_preregistrazione.sha256`. Criteri: C1 geometrie, C2 attributi, C3 sovrapposizioni, C4 capacità, C5a ortofoto ≥ 0,70 su 100 lotti, C5b differenza con la base di 100 particelle qualsiasi ≥ 0,25 (limite inferiore dell'IC), C6 conteggi, C7 accordo di Dennis ≥ 16/20, C8 riproducibilità.

Precisazione dichiarata (comunicata da Dennis l'11/11): capacità degli edificabili = superficie del lotto × FAR; lotti da riusare con due scenari, recupero (solo edificio dismesso della fonte) e demolizione e ricostruzione (lotto × FAR), scenario principale legato allo screening del degrado; aree di attivazione senza capacità abitativa.

## 2. Dati e fonti
- Fonti di v1 dalla cache: catasto WFS (CC BY 4.0), DBT 2020 (CC BY 2.5 IT), DUSAF 8.0, mosaico PGT regionale (licenza [L]), NIL ds964, ds503, Demanio ds2688/2689, ds677, ds600 [V].
- Nuova: ds2813, indice di verde urbano per NIL, luglio 2024 (CC BY 4.0), scaricata l'11/11 [V].
- Ortofoto AGEA 2018–2019, servizio a tasselli di Regione Lombardia `BaseMap/Ortofoto2018_2019/ImageServer`, livelli 9–13, fino a 0,26 m/pixel [V]. L'ortofoto 2021 risponde con errore 400 (WMS ed `exportImage`) [V, 09:40Z]; scarto dichiarato nella pre-registrazione.
- Licenza ortofoto: proprietà AGEA, sola visione e stampa con citazione [S]; record INSPIRE non aperto [L]. Per questo le immagini non sono versionate e si rigenerano con `run.py`.

## 3. Metodo
Regole R1–R4, E1–E4, A1–A4, capacità e campionamento come da pre-registrazione; `run.py` riusa da v1 i moduli `parcels`, `share`, `rd`, `fetch`. Registro in `esecuzioni/registro.txt`: 2 piloti (3 NIL) e 6 esecuzioni complete, archiviate con commit, hash di `run.py` e durata. Correzioni di solo codice, nessuna regola o soglia toccata: errore di tipo nel pilota; classi invertite nel pilota; disegno del contorno con coordinate 3D; C8 falso nelle esecuzioni 3–4 per una coordinata Z ereditata dal DBT (corretto con `force_2d`). Codifica cieca delle 200 immagini (C001–C200) fatta senza aprire il campione; hash della codifica `4ed06c05…` registrato prima dell'unione. Cecità parziale: il codificatore è l'esecutore.

Schema di codifica: Q1 copertura prevalente (L libera, C cantiere, D dismesso o degradato, U in uso, V verde curato o agricolo, I infrastruttura, X non giudicabile; "libera o dismessa" = {L, C, D}); Q2 per gli edifici: tetto T0–T3, vegetazione V0–V2, uso apparente U+ / U− / U?.

## 4. Risultati

| Classe | n | ha | FAR 0,5 | FAR 1 | FAR 2 | recupero |
|---|---|---|---|---|---|---|
| lotto edificabile | 553 | 653,8 | 28.330 | 56.936 | 114.143 | — |
| lotto da riusare | 242 | 68,3 | 2.858 | 5.850 | 11.824 | 9.740 |
| area di attivazione | 854 | 319,7 | 0 | 0 | 0 | — |

- Edificabili per origine: 375 terreno comunale libero, 113 DUSAF 133/134, 60 AT, 4 ex AMB_DEG, 1 Demanio. 34 edificabili anche candidati all'attivazione.
- Riuso: 122 diruti DBT, 105 ds503, 15 entrambi; scenario principale 129 demolizione e ricostruzione, 113 recupero (22 da screening, 220 da regola di default).
- Proprietà: pubblico comunale 402 edificabili e 676 aree di attivazione; "ignoto" 224 dei 242 da riusare. 83 NIL su 88.
- Filtri più pesanti: particella ≥ 300 m² −5.832; verde, acque, infrastrutture −3.174; PCU −1.147; minimo 1.500 m² −413 gruppi. Vincoli noti su 64 edificabili, 24 da riusare, 120 aree di attivazione (bonifica in 81 casi).

| # | Esito | Valore |
|---|---|---|
| C1 geometrie | passa | 100% valide, EPSG:32632 |
| C2 attributi | passa | 100% |
| C3 sovrapposizioni | passa | 0 coppie oltre 1 m² |
| C4 capacità | passa | 3 FAR e recupero |
| C5a ortofoto, 100 lotti | **non passa** | 0,34 [0,255; 0,437] (Wilson), soglia 0,70 |
| C5b differenza con la base | **non passa** | base 0,09 [0,048; 0,162]; differenza 0,25 [0,139; 0,356] (Newcombe) |
| C6 conteggi | passa | somme esatte |
| C7 controllo di Dennis | **in attesa di Dennis** | 20 casi in `controllo_umano/` |
| C8 riproducibilità | passa | hash `011672c6…` identico in due esecuzioni |

C5 per classe (informativo): edificabili 0,22 [0,13; 0,35]; da riusare 0,50 [0,33; 0,67]; aree di attivazione 0,40 [0,22; 0,61].

Lettura a posteriori [I], non un criterio: il fallimento viene dall'ingresso "terreno comunale libero" (0,11 [0,04; 0,25]: cortili, strade, parcheggi, verde condominiale, pertinenze ERP); gli altri ingressi degli edificabili danno 0,54 [0,29; 0,77]. Nel riuso i diruti DBT danno 0,65, ds503 da solo 0,31 (dati 2014–2017, molti edifici di nuovo in uso). 14 lotti da riusare su 30 hanno uso "incerto": l'esclusione degli edifici abitati non è dimostrata.

Screening del degrado su 22 edifici [H, screening visivo, non perizia]: recuperabilità alta 14, media 5, bassa 3.

## 5. Esito
**Cambia.** C5 non passa: per la regola di arresto la base non si congela e la decisione passa a Dennis. Il controllo distingue i lotti dal caso (+0,25, contro nessun arricchimento in v1), ma non abbastanza.

## 6. Limiti
Ortofoto 2018–2019 contro DUSAF 2024 e ds503 2014–2017; un solo codificatore, non indipendente; unità di screening del riuso = particella meno gli altri edifici (8 lotti su 30 senza edificio visibile); nessun dato aperto sull'occupazione degli edifici, sulla proprietà ERP/ALER e sugli indici reali del PGT [L]; resa 0,70 e 80 m² per alloggio [H]; 30 edificabili oltre 400 alloggi a FAR 1; licenza del mosaico PGT [L].

## 7. Revisione indipendente
_Da scrivere a cura del revisore-metodologico._

## 8. Cosa passa
Nulla come base congelata. Proposta [H] per la decisione di Dennis: togliere o restringere l'ingresso "terreno comunale" (es. richiedere anche DUSAF 13x o 1412, o escludere le pertinenze); per ds503 richiedere una conferma (diruto DBT o screening); nuovo campione con seme nuovo dichiarato prima; un secondo codificatore cieco. Riutilizzabili subito: pipeline, registro, schema di codifica.
