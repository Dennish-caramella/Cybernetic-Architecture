# Report di laboratorio — Base L v5: ambiti del PGT 2030 vigente (ticket #38)

Esecuzione: agente `dati-geo-milano`, 14/11/2026. REPORT assemblato dal coordinatore a partire dalla consegna dell'agente, che non può creare `REPORT.md`. Stato: **candidata, in attesa di C5 e C9**.

## 1. Ipotesi e soglia
Il testo completo è in `esecuzioni/00_preregistrazione.txt` (SHA-256 `5e2da4ab…`, scritto alle 10:24Z, prima del pilota delle 10:30Z). **Correzione dopo la revisione**: il commit della pre-registrazione (0490f98, 11:15Z) è successivo al pilota e alle esecuzioni 1–4 (10:30–11:14Z) e alla codifica 1 del censimento (11:04Z); precede solo le codifiche C5 e la codifica 2 del censimento. L'ordine tra testo ed esecuzioni si regge sul registro dell'esecutore e sull'hash; le soglie di C5 e C9 sono quelle di v4, committate il 12/11 (f287378). In sintesi:
- **Ambiti 2030 al posto dello strato AT del PGT 2012.** Comprendono i PA/AS del Piano delle Regole (strato 11 del mosaico regionale, schede MA del 05/02/2020), l'AdP Scali ferroviari e le GFU, queste con il perimetro 2012 come sostituto [H]. Precedenza: PA > ADP > GFU.
- **D4 sugli ambiti 2030**: se la residenza nel 2030 non è "si", la particella va tra le aree di attivazione con capacità 0.
- **C5-fisico**: soglie come v4. Precondizione kappa binario ≥ 0,60; C5a ≥ 0,70; C5b limite inferiore di Newcombe ≥ 0,25. Seme 5511, n = 120 lotti + 100 particelle qualsiasi.
- **C9, censimento dello stato attuativo** (29 poligoni). C9a: tutti i poligoni hanno una categoria A–D con fonte ufficiale. C9b: accordo prima della riconciliazione ≥ ceil(5n/6) = 25.
- **C1–C4, C6, C8**: come v4. C7 non è più un criterio (decisione di Dennis).

## 2. Dati e fonti
- **Fonti di v4**: invariate. Il catasto corretto si legge dalla cache v4 in sola lettura [V].
- **Ambiti 2030**:
  - strato 11 di `tav_previsioni_b`, EPSG:32632 [V]; licenza non dichiarata [L];
  - le 18 schede `015146_20200205_MA_<n>.pdf` sono scaricate in `_cache/pgt2030/` e lette tutte [V]. I PDF sono del 17/12/2019; la data 05/02/2020 come data di efficacia è [I];
  - campi estratti: dizionario `MA` in `run.py` e `tabelle/ambiti_2030.csv`. Che "funzioni urbane libere" ammetta la residenza è [I];
  - le schede non indicano la data di approvazione dei piani attuativi [L].
- **AdP Scali**:
  - servizio `programmi`, strato 1, geometrie ottenute con `identify` [V]; decreto n. 754, data del campo 01/08/2017;
  - il comunicato FS del 22/06/2017 conferma San Cristoforo al 100% verde e Porta Genova al 70% non residenziale [V];
  - gli allegati regionali non sono raggiungibili (host non risolto) [L].
- **GFU**: i nomi vengono da sintesi di ricerca di pagine del Comune non aperte [S]. Nessun perimetro aperto [L]: il geoportale del Comune risponde 502 (non aggirato) e il server di prova 404.
- **Strato 14** (1.498 ambiti di rigenerazione diffusa, 2025): usato solo per l'attributo informativo `quota_rig_diffusa`.
- **Immagini**:
  - l'Ortofoto 2021 della Regione risponde ancora 400 [V], quindi per la codifica si usa AGEA 2018–2019 (licenza di sola visione: non si diffonde);
  - per localizzare i lotti si usa EOX Sentinel-2 cloudless 2025, CC BY-NC-SA 4.0, 10 m [V];
  - il servizio Sentinel-2 della Regione non dichiara data né licenza [L]. Copernicus Data Space richiede un account e non è stato usato.

## 3. Metodo
- **Come v4**: catasto corretto, intorno di 10 m per il riuso (sensibilità a 5 e 20 m), D1–D7, proprietà "non agganciata". `quota_at` si calcola sull'unione degli ambiti 2030.
- **Filtro PCU**: resta quello del 2012 [H].
- **Censimento C9**: 29 poligoni, codificatore 1 = esecutore, codificatore 2 isolato.
- **Correzioni dopo la prima esecuzione**, registrate in `esecuzioni/registro.txt`:
  - correzione di codice per allinearlo al testo pre-registrato 1.3: alle particelle il cui punto interno cade fuori da ogni poligono si assegna l'ambito con la sovrapposizione maggiore. Riguarda 2 lotti edificabili;
  - correzione cosmetica: centroide in EPSG:32632 per l'immagine Sentinel-2;
  - prima di preparare i pacchetti l'esecutore ha guardato una sola immagine Sentinel-2 di prova (lotto E00252), dichiarata nel registro.
- **Riproducibilità**: esecuzioni 2–4 con hash identico `440bf046…`.

## 4. Risultati
**Conteggi**: 216 lotti edificabili, 176 lotti da riusare, 309 aree di attivazione (v4: 257 / 176 / 293).

| Capacità dei lotti edificabili (alloggi) | FAR 0,5 | FAR 1 | FAR 2 |
|---|---|---|---|
| v5 | 16.389 | 32.885 | 65.885 |
| v4 | 24.701 | 49.522 | 99.173 |

- **Lotti da riusare**: 739 / 1.564 / 3.212 alloggi con demolizione e ricostruzione, 3.029 con il recupero. Le aree di attivazione hanno capacità 0.
- **Cascata** (`tabelle/cascata.csv`, `fig/cascata.png`): 3.385 particelle in ingresso → 1.889 dopo i filtri → 1.094 verso l'abitazione e 795 verso l'attivazione.
- **Lotti fuori ambito**: 173 E, 147 R, 245 A. **In ambito**: 43 E, 29 R, 64 A; i lotti edificabili in ambito valgono 12.301 alloggi a FAR 1.
- **Ambiti 2030 senza residenza o GFU**: 45 lotti, 169,2 ha, 14.750 alloggi a FAR 1 se fossero edificabili; di questi, le GFU sono 37 lotti, 146,8 ha, 12.798 alloggi [I].
- **Sensibilità senza GFU** (`tabelle/sensibilita_senza_gfu.json`): 222 E, 175 R, 268 A; 34.051 alloggi a FAR 1.
- **Dentro i poligoni AT 2012** i lotti edificabili scendono da 306,9 ha (v4) a 96,5 ha:
  - passano all'attivazione le GFU (Bovisa 56,5 ha, Piazza d'Armi 54,6, Porto di Mare 20,9, Ronchetto 11,2) e San Cristoforo (10,9);
  - gli AT 2012 assenti nel 2030 perdono circa 54 ha.
- **Da AT 2012 ad ambiti 2030** (`tabelle/tabella_AT_2012_2030.csv`):

| Esito | Ambiti |
|---|---|
| Restano (AdP) | Farini, Romana, Lambrate, Rogoredo, Porta Genova, Greco-Breda |
| Restano (PA6) | Caserma Mameli |
| Cambiano destinazione | San Cristoforo (oasi) |
| Ridotti | Stephenson: solo PA1/b, residenza esclusa |
| GFU con perimetro 2012 [H] | Piazza d'Armi, Ronchetto, Porto di Mare, Bovisa-Goccia |
| Assenti nel 2030 [L] | Magazzini raccordati, Montello, Rubattino, XXIV Maggio, via Messina, Don Calabria, Litta Modignani, Toffetti |
| Nuovi | 15 dei 18 PA/AS |

- **Copertura degli ambiti** (`tabelle/copertura_ambiti_2030.csv`): Mameli al 35%, perché 6,7 ha restano fuori per il filtro D5 "residenza occupata" [I]; AS/1 e AS/2 allo 0%, per il filtro agricolo.
- **Censimento, codificatore 1** (SHA-256 `a3ad9dda…`): 8 A (7 AdP + Mameli), 1 B (Piazza d'Armi), 20 N.

## 5. Esito
Esecuzione 5 (15:20Z, con i fogli compilati; hash di contenuto `440bf046…` identico): **la base non passa**, perché C9 è falso.
- **C1–C4, C6, C8**: passano.
- **C5 passa di misura.** Kappa binario 0,945, kappa Q1 0,876. C5a = 170/240 = 0,708 (soglia 0,70): codificatore 1 0,700 [0,613; 0,775], codificatore 2 0,717 [0,630; 0,790]. Base su particelle qualsiasi 0,16 per entrambi; C5b, limite inferiore di Newcombe 0,419 e 0,436 (soglia 0,25). Per classe: attivazione 0,817, edificabile 0,703, riuso 0,532. Informativo [I, revisione]: sui soli lotti con capacità (E + R) la quota è circa 0,62.
- **C9 non passa.** Accordo prima della riconciliazione 11/29 (soglia 25). In 18 discordanze il codificatore 1 ha N e il codificatore 2 una categoria, per lo più su fonti secondarie.
- **Esito proposto dal revisore: cambia** (§7). La regola di arresto è scattata: decide Dennis.

## 6. Limiti
- Perimetri e destinazioni delle GFU mancano [L]; si usa il proxy 2012 [H].
- La licenza degli strati regionali non è dichiarata [L]. Lo stato "In attuazione" non ha una data di aggiornamento.
- 20 poligoni del censimento sono N, perché le fonti stanno su siti esclusi (es. PA7 Trotto, delibera n. 465 del 05/04/2023 [S]; PA3 Molise in VAS [S]).
- Gli altri AdP e PII di Milano (Cascina Merlata, MIND, PRU Rubattino…) non entrano [H].
- Sentinel-2 a 10 m serve solo a localizzare il lotto. Il test C4 verifica la formula, non la plausibilità della capacità.
- Non verificati: la corrispondenza tra le GFU Rubattino e San Siro e i perimetri; gli allegati dell'AdP; lo stato dei cantieri; le Norme di Attuazione sull'indifferenza funzionale.
- Fatto nuovo [V]: il protocollo Invimit del 23/12/2025 indica residenze a Piazza d'Armi. In v5 la regola GFU non è stata cambiata.

## 7. Revisione indipendente
Testo completo in `REVISIONE.md` (`revisore-metodologico`, che non ha eseguito la prova; è un'altra istanza dello stesso sistema, non una verifica umana). Ricalcolo dei numeri in `revisione/verifica.py`.
- **Esito proposto: cambia.**
- **G1**: C9 non può passare con lo strumento attuale. Le categorie N e C si sovrappongono; le istruzioni del codificatore 2 omettono la regola "le fonti secondarie non decidono"; entrambi indicano come decisivi documenti su comune.milano.it. Ne restano 136 lotti AT, il 37% della capacità edificabile, senza stato attuativo.
- **G2**: C5 passa di 2 successi su codifiche probabilmente non indipendenti: 21 note identiche parola per parola, 0 disaccordi sulle 100 particelle di base, stesso modello. Il kappa misura la ripetibilità del modello, non l'accordo tra codificatori indipendenti.
- **Da correggere**:
  - 146,8 ha di GFU a destinazione ignota contati come aree di attivazione, contro `CONTEXT.md` e contro la fonte Invimit su Piazza d'Armi; la capacità oscilla tra circa 32.900 e 45.700 alloggi a FAR 1;
  - 9 lotti da riusare in ambiti senza residenza conservano capacità (135 alloggi), contro il testo 1.3;
  - la classe riuso non è validata (0,532);
  - la cecità è affidata solo alla disciplina.
- **Minori**: Bovisa 56,5 ha in §4 contro 64,1 ha nel gpkg; codifica 2 del censimento in 7 minuti; gli intervalli per classe sono calcolati su giudizi doppi.

## 8. Cosa passa alla prova successiva
- **Codifica cieca** dei pacchetti `controllo_codificatore_1/` e `_2/`, isolati. Gli SHA-256 dei fogli vuoti (`ef22c48a…`) e della chiave (`d787a547…`) sono nel registro.
- **Codificatore 2 del censimento**: riceve `censimento_AT/` senza `codifica_1.csv`.
- **Dennis**: apre i documenti dei poligoni N e scrive `consenso.csv` (chiave `ambito_id`). Decide inoltre:
  - se includere gli altri AdP e PII;
  - se aggiornare la residenza delle GFU (Piazza d'Armi) in una v6.

Script della codifica 1 del censimento: `censimento_AT/censimento_c1.py`.
