# Audit dei dati e dei piani già disponibili online per Milano (prima della richiesta formale al Comune)

Data: 2026-11-10. Ruolo: analista dati della tesi. Oggetto: cosa c'è già online per alimentare il modello della decisione 2026-11-10 (`tesi/DECISIONI.md`: famiglie con vettore dei desideri → lotti raccomandati e spiegati → accettazione differita con riserve di capacità; ogni lotto costato developer vs cooperativa, gap fondiario ΔL) e cosa manca davvero.

**Marche.** **[V]** verificato direttamente in questa sessione: risposta dell'API o file scaricato e aperto, oppure pagina ufficiale aperta. **[S]** visto solo in risultati di ricerca o fonti secondarie (stampa, Assolombarda). **[L]** da verificare. **[I]** inferenza mia. Nessuna voce [S]/[L] va citata in tesi senza riscontro sulla fonte primaria.

**Limite di questa sessione [V].** I siti del Comune `www.comune.milano.it`, `pgt.comune.milano.it`, `geoportale.comune.milano.it`, `milanostatistica.comune.milano.it` e quello di MM (`www.mmspa.eu`) **non erano raggiungibili** da questo ambiente: risposta 403 (Microsoft Azure Application Gateway) o tunnel 502, e WebFetch non risolveva il dominio. Per questo le pagine ufficiali del Piano Casa, dell'Amministrazione trasparente, del PGT 2030 e del Geoportale comunale restano **[L]**. Il portale open data `dati.comune.milano.it` (API CKAN) invece rispondeva, ed è la base di questo audit.

File di riferimento salvati in `catalogo/` (2,4 MB in tutto):
- `package_list.json`: risposta grezza di `package_list` (2.618 dataset).
- `catalogo_dati_comune_milano_2026-11-10.csv`: catalogo completo ricavato da `package_search`. Per ciascun dataset: nome, titolo, publisher, maintainer, licenza, `modified`, copertura temporale, frequenza, data dell'ultima risorsa, formati, gruppi, tag, URL.
- `metadati_ckan/*.json`: record completi di `package_search`, equivalenti a `package_show`, per 68 dataset chiave.
- `ISTAT_2021_sezioni_TRACCIATO_FILE_REGIONALI.xlsx`: tracciato ufficiale delle variabili 2021 per sezione.
- `lombardia/`: risposte del catalogo e metadati di dati.lombardia.it (ALER, SACC, DUSAF, PGT).

---

## 0. Sintesi in dieci righe

1. **Patrimonio comunale: esiste un elenco aperto con foglio e mappale** [V]. Il dataset `ds677` ("Elenco immobili di proprietà del Comune di Milano") conta 23.640 righe (19.892 TERRENO, 3.748 FABBRICATO), tutte con FOGLIO e MAPPALE, e 636 righe con `PIANO_ALIENAZIONE=SI`. È fermo al **2019**. Riduce molto la lacuna "proprietà" per la parte pubblica comunale, ma va aggiornato.
2. **Proprietà privata: non aperta.** La cartografia catastale è CC-BY 4.0 ma contiene solo le particelle [V]. Gli intestatari si ottengono solo con visura [S].
3. **Reddito: la risoluzione più fine resta il CAP** [V]. Il dataset `ds3009` (MEF) riporta 38 CAP e 45 variabili, con 8 classi di reddito complessivo, anno d'imposta 2024. La pagina MEF classifica questi dati come "Sub-Comunale (CAP)" [V].
4. **Censimento 2021 per sezione: niente titolo di godimento né tipo di nucleo** [V]. Il tracciato ISTAT contiene età, sesso, istruzione, occupati, stranieri, famiglie per numero di componenti (da 1 a 6+), abitazioni ed edifici.
5. **Titolo di godimento per NIL esiste solo al 2011** [V]: `ds1457`, con proprietà / affitto / altro titolo per NIL. Basta a sostituire la quota piatta di affittuari 0,30 usata dal Lab, ma è vecchio di 15 anni.
6. **Tipologie familiari per NIL aggiornate al 2025** [V]: `ds1441`, da anagrafe, con tipologia, componenti ed età del capofamiglia.
7. **Titoli edilizi: c'è un dataset puntuale** [V]. `ds270` riguarda i nuovi fabbricati residenziali 2011–2024: 728 righe con titolo abilitativo, sezione, NIL, alloggi, superfici, tipo di titolare, coordinate.
8. **OMI già sul portale del Comune** [V]: quotazioni e perimetri dal 2004 al 2025/2, con licenza CC-BY indicata da CKAN ma con le condizioni d'uso dell'Agenzia richiamate nella descrizione.
9. **ERP (ALER/MM): nessun dataset con lo stock di alloggi** [V per i cataloghi CKAN e Lombardia]. I dataset ALER di Regione riguardano solo governance e bilanci (art. 22 del D.Lgs. 33/2013).
10. **PGT 2030 (ambiti, ERS, indici, servizi): nessuno strato sul portale open data comunale** [V, cercato]. C'è solo il perimetro dei NIL (`ds964`). Gli strati stanno sul Geoportale comunale, non raggiungibile da qui [L], e nelle "Tavole dei PGT" di Regione [V, esistenza nel catalogo].

---

## 1. Portale open data del Comune (CKAN): dataset rilevanti

Metodo [V]: `package_list` restituisce 2.618 dataset. Con `package_search` (`rows=1000`, tre pagine) ho scaricato i metadati di tutti, poi ho cercato nei titoli, nelle note e nei tag con parole chiave per tema.

Come leggere la tabella:
- "Agg." è il campo `modified` del dataset. Il campo `metadata_modified` non è usabile: per 2.404 dataset vale 2026-05-08, segno di un aggiornamento di massa.
- "Lic." viene da `license_title`. Il codice della risorsa (per esempio A21 = CC-BY 4.0) viene da `license_type`.
- L'URL è sempre `https://dati.comune.milano.it/dataset/<nome>`.
- Il nome completo di ogni dataset è nel CSV del catalogo.

Tutto ciò che sta in questa sezione è **[V]**, salvo dove indicato.

### 1.1 Suolo, particelle, patrimonio pubblico

| id | Titolo | Publisher | Agg. | Formati | Risoluzione | Lic. | Serve al modello? |
|---|---|---|---|---|---|---|---|
| ds677 | Elenco immobili di proprietà del Comune di Milano | Direzione Partecipate e Patrimonio Immobiliare | 28-08-2019 (copertura 2019) | CSV, JSON, GeoJSON | punto + foglio/mappale | CC-BY 4.0 | **Sì, molto: proprietà comunale dei lotti** (join per foglio e mappale con le particelle catastali). Campi: COD_INVENT, TIPO, INDIRIZZO, FOGLIO, MAPPALE, MILANO (SI/NO), PIANO_ALIENAZIONE, MUNICIPIO, ID_NIL. 22.055 righe in Milano, 1.585 fuori comune. Limiti: dati del 2019, nessuna superficie, nessuno stato d'uso. Le note rimandano alla pagina di Amministrazione trasparente [L, non raggiungibile] |
| ds616 | Aste di Vendita immobili pubblici nel Comune di Milano | ARCA Lombardia | 13-10-2026, settimanale | CSV, JSON, GeoJSON | unità | CC0 | Marginale: 14 righe, aste di enti lombardi |
| ds147 | Beni immobili confiscati alla criminalità organizzata | Direzione Politiche Sociali | 18-06-2026, mensile | CSV, JSON | unità (foglio/mappale/sub) | CC-BY 4.0 | Marginale: 274 unità (144 appartamenti); utile come stock sociale puntuale |
| ds2688 / ds2689 (serie 2014–2023) | Aree / Fabbricati del Demanio Statale – Anno 2023 | Agenzia del Demanio | 21-02-2024 | CSV, JSON, GeoJSON | punto + superficie fondiaria (aree) | CC-BY 3.0 IT | Sì per i lotti pubblici statali: 37 aree con superficie in m² |
| ds503 | Edifici degradati, abbandonati o dismessi 2014-2017 | Unità SIT e Gemello Digitale | 24-11-2020 | SHP (servizio), CSV, GeoJSON | punto | CC-BY 4.0 | Sì come candidati: 174 righe, immobili privati della tavola R.10 del PGT (art. 11 NdA PdR) |
| ds2889 / ds2892 | Database Topografico (DBT) 2020 / 2012 – SHP | Unità SIT | 05-02-2025 | SHP (zip) | edificio | CC-BY 2.5 IT (codice A25) | Sì: volumi ed edifici, già usati dal Lab. **Licenza chiarita: CC-BY 2.5 IT** |
| ds964 | NIL VIGENTI – PGT 2030 | Direzione Urbanistica | 12-02-2021 | GeoJSON, SHP, CSV | 88 NIL | CC-BY 4.0 | Sì: unità di sintesi. Anche lo SHP ha licenza CC-BY 4.0. ds61 contiene i NIL obsoleti |
| ds2845 | Sezioni di Censimento anno 2021 | Dir. Innovazione Tecnologica | 06-11-2024 | CSV, JSON, GeoJSON | sezione | CC-BY 4.0 | Sì: 7.095 sezioni con **POP21 e FAM21** (somme: 1.349.930 residenti, 720.361 famiglie) |
| ds98, ds95 | Sezioni 2011, ACE 2011 | idem | 2011/2019 | SHP, GeoJSON | sezione | CC-BY 4.0 | Ponte con i dati 2011 |
| ds634 | Numeri civici con coordinate geografiche | Unità SIT | 04-10-2026, mensile | CSV, JSON, GeoJSON | civico | CC-BY 4.0 | Sì: geocodifica degli indirizzi (ancore delle famiglie, ERP) |
| ds2841 | Confini amministrativi | Analytics e Open Data | 04-11-2024 | GeoJSON | comune | CC-BY 4.0 | Base |
| ds600 | Interventi di bonifica da contaminazioni ambientali | Città Metropolitana | 13-10-2026, settimanale | CSV, JSON, GeoJSON | punto/area | CC0 | **Sì: vincolo bonifiche**, assente nel Lab |
| ds1444 | Superficie impermeabile | DLR | 2016 | ZIP | raster | CC-BY 4.0 | Marginale |

**Risultato negativo [V].** Nel catalogo non c'è nessun dataset con questi termini nel titolo o nelle note: "Piano dei Servizi", "Piano delle Regole", "Documento di Piano", "ambiti di trasformazione", "perequazione", "ERS", "aree comunali disponibili", "Piano Casa" (come dataset). Le sole voci con "PGT" sono i NIL (ds964, ds61), gli indici di calore e verde per NIL e ds503.

### 1.2 Mercato: prezzi e canoni

| id | Titolo | Publisher | Agg. | Formati | Risoluzione | Lic. | Serve? |
|---|---|---|---|---|---|---|---|
| ds1996 | Quotazioni Immobiliari OMI: Compravendita e Locazione – Riepilogo | Agenzia delle Entrate | 26-10-2026 (fino al 2025) | CSV, JSON | zona OMI × tipologia × stato | CC-BY 4.0 (CKAN), **ma** la descrizione riporta le condizioni dell'Agenzia: "Le informazioni rese sono di proprietà esclusiva dell'Agenzia... possono essere utilizzate... purché, nel caso di pubblicazione, venga citata la relativa fonte" | **Sì: canone e prezzo di mercato per zona** (Loc_min, Loc_max in €/m²·mese) |
| ds3024, ds3022 (serie 2004/1–2025/2) | OMI Locazione semestre 2025/2, 2025/1 | idem | 26-10-2026 | CSV, JSON | zona OMI | idem | Sì: 446 righe nel 2025/2 |
| ds3023 (serie 2011/1–2025/2) | Zone e Perimetri OMI 2025/2 | idem | 26-10-2026 | CSV, JSON, GeoJSON | 43 zone (fascia, zona, microzona) | idem | Sì: geometrie per riportare l'OMI su lotti e NIL. **Non serve più lo specchio onData** |
| ds558 | Canoni di locazione versati e percepiti da Regione Lombardia | Regione Lombardia | 27-01-2021 | CSV | ente | CC0 | No |

### 1.3 Persone, famiglie, redditi

| id | Titolo | Publisher | Agg. | Risoluzione | Lic. | Serve? (variabile) |
|---|---|---|---|---|---|---|
| ds1441 | Famiglie anagrafiche: tipologie per NIL (1999-2025) | Unità Anagrafe | 31-03-2026, annuale | NIL × anno | CC-BY 4.0 | **Sì: tipi di famiglia per la popolazione sintetica.** Campi: Classe_eta_capofamiglia (<35, 35-64, 65-79, 80+), Genere, Numero_componenti (1…5+), Tipologia_familiare (Monocomponente, Coppia sposata con/senza figli, Monogenitore con figli, In convivenza, Altre…), Cittadinanza, Famiglie |
| ds1440 | Famiglie anagrafiche residenti per NIL (1999-2025) | idem | 31-03-2026 | NIL | CC-BY 4.0 | Sì: marginali |
| ds27 | Residenti per cittadinanza e quartiere (1999-2025) | idem | 31-03-2026 | NIL | CC-BY 4.0 | Sì |
| ds205 | Caratteristiche demografiche e territoriali dei quartieri | Dir. Innovazione | 14-09-2026 (2011–2024) | NIL | CC-BY 4.0 | Sì: minori, 65+, 80+, famiglie unipersonali, 80+ soli, numero di scuole, area |
| ds223 | Residenti per stato civile, genere, età e cittadinanza (2012-2025) | Anagrafe | 31-03-2026 | comune | CC-BY 4.0 | Marginale (solo totale comunale) |
| ds25 | Proiezioni della popolazione per quartiere 2023-2039 | Anagrafe | 15-11-2023 | NIL | CC-BY 4.0 | Scenario |
| ds1457 | Censimento 2011: Abitazioni occupate per NIL | Dir. Innovazione | 11-11-2020 | NIL | CC-BY 4.0 | **Sì: titolo di godimento per NIL (Proprietà / Affitto / Altro titolo)** e figura giuridica del proprietario (persona fisica / altro). Ma è il 2011 |
| ds1449, ds322 | Titolo di godimento per municipio; figura giuridica del proprietario (2011) | idem | 2015–2020 | municipio, comune | CC-BY 4.0 | Controllo |
| ds382, ds384, ds385 | Censimento 2011 per sezione (popolazione, alloggi, indicatori) | idem | 2017 | sezione 2011 | CC-BY 4.0 | Ponte |
| ds3009 | Redditi e variabili Irpef su base sub-comunale: 2025 a.i. 2024 | MEF | 30-06-2026 | **CAP (38)** | CC-BY 4.0 | **Sì, l'unico reddito sub-comunale**: 45 variabili, 8 classi di reddito complessivo (≤0, 0-10k, 10-15k, 15-26k, 26-55k, 55-75k, 75-120k, >120k) con frequenza e ammontare. Serie sub-comunale disponibile anche per a.i. 2019–2023 (ds1590, ds1830, ds2275, ds2734, ds2946) |
| ds3010, ds531 | IRPEF comunale; distribuzione del reddito complessivo (serie) | MEF / Comune | 2026 | comune | CC-BY 4.0 | Controllo |
| ds390–ds395, ds1486 | Pendolarismo 2011 (per sezione di origine/destinazione) | Dir. Innovazione | 2017 | sezione 2011 | CC-BY 4.0 | Sì per le ancore di lavoro e scuola (matrice O/D del 2011, vecchia) |

### 1.4 Servizi, scuole, verde, lavoro, trasporti

| id | Titolo | Agg. | Risoluzione | Lic. | Serve? |
|---|---|---|---|---|---|
| ds3014, ds3015, ds3016 | Scuole dell'infanzia / primarie / secondarie di I grado, a.s. 2025/2026 (Direzione Educazione) | 26-10-2026 | punto | CC-BY 4.0 | **Ancore scuola** |
| ds78 | Scuole secondarie di II grado | 2010 (GeoJSON 2020) | punto | CC-BY 4.0 | Vecchio. ds1863 (MIM, edifici scolastici statali 2020/21, IODL 2.0) è un'alternativa |
| ds47, ds709 | Asili nido (2016-2019); servizi integrativi all'infanzia | 2021, 2023 | punto | CC-BY 4.0 | Ancore cura 0-3 (non aggiornate) |
| ds586, ds620, ds618 | RSA/RSD, RIA geriatriche, ADI (Regione Lombardia) | 13–15-10-2026 | punto | CC0 | **Ancore cura anziani** |
| ds234 | Medici di medicina generale (ATS Milano) | 10-11-2026, settimanale | punto | CKAN dice "Non-Commercial", la risorsa dice CC-BY-SA 3.0 IT: **licenza incoerente** [V], da chiarire | Servizi |
| ds501, ds561 | Farmacie, consultori pubblici | 2026 | punto | CC0 | Servizi |
| ds3018, ds89, ds2484 (alberi), ds2186 (orti) | Parchi e aree verdi (Spazi freschi 2026); parchi e giardini (2012); alberi (2025) | vari | poligono/punto | CC-BY 4.0 | Criterio verde. ds89 è del 2012 |
| ds2813, ds2812, ds2816 | Indice di verde e rischio calore per NIL e per sezione 2011 (luglio 2024) | 10-09-2024 | NIL, sezione | CC-BY 4.0 | Criterio calore e verde (sostituisce il "rischio calore del NIL" del Lab) |
| ds929 | GTFS | 29-10-2026, bisettimanale | fermata/orario | CC-BY 4.0 | **Sì: accessibilità con trasporto pubblico** (zip da 60 MB, non scaricato) |
| ds535, ds534, ds539, ds538 | Fermate e percorsi di metro e superficie ATM | 24-07-2026 | punto/linea | CC-BY 4.0 | Sì |
| ds49, ds50, ds58 | Esercizi di vicinato, media e grande distribuzione, pubblici esercizi | 31-08-2026 | punto | CC-BY 4.0 | Servizi di prossimità e **proxy dei luoghi di lavoro** |
| ds201 | Unità locali per settore e quartiere | 2010 | NIL | CC-BY 4.0 | Luoghi di lavoro (vecchio) |
| ds691 | Imprese attive per settore (serie) | 19-06-2026 | comune | CC-BY 4.0 | Controllo |

### 1.5 Edilizia e titoli

| id | Titolo | Publisher | Agg. | Contenuto | Serve? |
|---|---|---|---|---|---|
| ds270 | Edilizia: nuovi fabbricati con destinazione d'uso residenziale – serie storica | Direzione Urbanistica | 01-09-2026 (2014–2024) | 728 righe: titolo abilitativo (Permesso di costruire 347, SCIA alternativa 253, SCIA 127), sezione di censimento, NIL, n. abitazioni, stanze, piani, volume, superficie utile abitabile, alloggi per classi di superficie, **tipo di titolare**, "Piano Casa" (sì/no), impianti, coordinate | **Sì: calibrazione della produzione edilizia reale** (dimensioni, tagli degli alloggi, chi costruisce dove). È la rilevazione ISTAT dei permessi di costruire (modello ISTAT/PDC), non l'archivio delle pratiche [I]. Il significato del campo "Piano Casa" (regionale o comunale) va chiarito [L] |
| ds271, ds2983–ds2985 | Ampliamenti residenziali; fabbricati per collettività; non residenziali | Dir. Urbanistica | 10-06-2026 | idem | Complementari |
| ds1546 | Sportelli di quartiere: sportelli MM | Dir. Innovazione | 08-04-2026 | 1–2 punti | No: unico dato "MM" del catalogo |

**Risultato negativo [V].** Nel catalogo non ci sono:
- lo stock ERP (alloggi comunali gestiti da MM, alloggi ALER);
- graduatorie, bandi o assegnazioni SAP;
- sfratti o morosità;
- oneri di urbanizzazione o costo di costruzione;
- l'archivio completo dei titoli edilizi (CILA, SCIA, PdC con stato e indirizzo oltre ai nuovi fabbricati).

---

## 2. Altre fonti pubbliche

### 2.1 Geoportale del Comune (SIT) e PGT 2030
- `geoportale.comune.milano.it` dava tunnel 502; `pgt.comune.milano.it` rispondeva 403 [V: tentativo fallito]. Contenuto, servizi WMS/WFS e licenze restano **[L]**. Il Lab ha usato gli strati PGT 2030 AT, ex AMB_DEG, srv_erp e rig [V, paper §2], che quindi in qualche forma sono scaricabili [I].
- **Regione Lombardia, catalogo "PGT. Piani di governo del territorio"** (`ijqk-ahfp`, aggiornato 10-11-2026) [V]. Per Milano risultano voci "Vigente": le varianti al Piano delle Regole (PAI/PGRA, approvate con atti n. 4 del 23-01-2023 e n. 44 del 03-07-2023, in vigore dal 13-10-2023).
- **"PGT – Elenco documenti"** (`pxty-e6fu`) [V]: per Milano "Vigente" restituisce 73 file, quasi tutti della Componente geologica e del Piano delle Regole della variante, tra cui `PR_R05_Vincoli_Amministrativi`, `PR_R06_Vincoli_Tutela_Salvaguardia` e `CG_G04_Carta_dei_vincoli`, con link a `multiplan.servizirl.it`.
- **Il corpus completo del PGT 2030** (Documento di Piano, Piano dei Servizi, NdA con indici) **non risulta** tra i documenti "Vigente" di quel dataset [V]. Va preso dal sito del Comune [L].
- "Tavole dei PGT della Provincia di Milano" (`e4jf-ahvw`, tipo href, 20-07-2023) [V esistenza]: è il mosaico regionale degli azzonamenti. Contenuto e licenza per Milano [L].
- **Indici edificatori reali**: nessun dataset aperto li espone in forma tabellare [V per i cataloghi]. Vanno letti nelle NdA del Piano delle Regole e nelle schede degli AT [L].

### 2.2 Regione Lombardia
- **DUSAF**: su dati.lombardia.it ci sono solo DUSAF 6.0 (2018, `7rae-fng6`), 5.0 (2015) e 4.0 (2012), tutti CC-BY 4.0 e di tipo href [V]. Il "DUSAF 2024" usato dal Lab non compare in questo catalogo e va riscontrato sul Geoportale regionale [L]. Il Geoportale regionale rispondeva HTTP 200, ma non l'ho esplorato.
- **DBT**: per il Comune c'è ds2889 su CKAN (CC-BY 2.5 IT) [V]. Nel catalogo Lombardia la ricerca "DBT database topografico" restituisce 0 risultati [V].
- **ALER su dati.lombardia.it**: 18 risultati per "aler" [V]. Sono "Dati", "Elenco" e "Amministratori" delle ALER ai sensi dell'art. 22 del D.Lgs. 33/2013 (per esempio `b6r3-f7ye`, anno 2026). Le colonne riguardano oneri, rappresentanti e risultati di bilancio. **Niente stock di alloggi né localizzazioni** [V].
- **SACC – Servizi Abitativi a Canone Convenzionato** (`vmvb-epzv`, CC0, 19-11-2025) [V]: 24 interventi regionali, di cui **6 a Milano**. Riporta indirizzo, n. alloggi, investimento complessivo, contributo regionale, stato e soggetto attuatore, sempre una cooperativa (Solidarnosc, LUM). Esempio: via Cascella 5, 28 alloggi, 2.964.504 €. **È un dato reale di costo per alloggio di cooperative milanesi**, utile per tarare il ramo cooperativa [I]. Va capito se l'investimento include il suolo [L].
- "Comuni lombardi con indice di fabbisogno abitativo" (`99xm-9rgg`, 2021) [V esistenza]: livello comunale, marginale.
- Piattaforma regionale SAP (bandi e graduatorie ERP): nessun dataset aperto trovato con la ricerca "piattaforma servizi abitativi" [V: 0 risultati].

### 2.3 ISTAT – Censimento permanente 2021 per sezione
- Pagina "Basi territoriali e variabili censuarie" aperta [V]. Le basi 2021 sono in shapefile (WGS84 UTM 32N), con file regionali `R03_21.zip` per la Lombardia. Le variabili 2021 per sezione stanno in `esploradati.istat.it/.../Dati_regionali_2021.zip`, che pesa 254 MB: non l'ho scaricato.
- **Tracciato ufficiale letto** [V] (`TRACCIATO FILE REGIONALI.xlsx`, copiato in `catalogo/`). Variabili per sezione 2021:
  - popolazione per sesso e classi quinquennali d'età;
  - titolo di studio (9+);
  - occupati 15-64;
  - stranieri per età, sesso e UE/extra-UE;
  - **famiglie per numero di componenti (1, 2, 3, 4, 5, 6+)**;
  - abitazioni occupate da residenti, abitazioni vuote o di non residenti, abitazioni totali, edifici residenziali.
- **Risposta alla domanda della nota 10 [V]: il dato per sezione 2021 NON contiene il titolo di godimento (proprietà/affitto) e NON contiene il tipo di nucleo** (coppie, monogenitori, ecc.). Il tipo di nucleo per NIL si prende dall'anagrafe (ds1441). Il titolo di godimento è disponibile solo al 2011 (ds1457, per NIL).
- Il dato del Comune `ds2845` contiene già POP21 e FAM21 per sezione [V].

### 2.4 MEF – Redditi IRPEF
- La pagina open data MEF (`www1.finanze.gov.it/finanze/analisi_stat/public/index.php?opendata=yes`) è stata aperta [V]. Il rilascio "2025 a.i. 2024 / IRPEF / Persone fisiche" (data 23 aprile 2026) ha "Classificazione: Sub-Comunale(CAP)" [V]. **Il livello più fine è il CAP** [V]: sotto il CAP non c'è altro sul portale MEF [I, nessuna classificazione più fine elencata].
- Il Comune ripubblica lo stesso dato (ds3009) con 38 CAP [V]. Restano i limiti già noti: si tratta di contribuenti, non di famiglie; di classi, non di microdati [V per la struttura del file].

### 2.5 Agenzia delle Entrate – OMI
- Pagina "Condizioni contrattuali" delle quotazioni aperta [V]. Uso consentito "anche ai fini della loro elaborazione purché, nel caso di pubblicazione, venga citata la relativa fonte". I valori "non possono intendersi sostitutivi della stima" e si riferiscono "all'ordinarietà degli immobili". C'è un avviso: le rivisitazioni delle zone fino al 2004 rendono alcune serie "non utilizzabili" per ricostruzioni storiche [V].
- Per Milano le quotazioni e le zone semestrali dal 2004 al 2025/2 sono già sul CKAN comunale, senza autenticazione [V]. Il "Rapporto immobiliare" e le "Statistiche" OMI (NTN, compravendite) non sono stati aperti in questa sessione [L].

### 2.6 Catasto
- Pagina "Consultazione cartografia catastale – Che cos'è" (aggiornata il 1 settembre 2026) aperta [V]. Dice: "disponibile per la fruizione libera, in formato vettoriale, mediante servizi puntuali e di download massivo dei dati relativi alle particelle catastali"; "i dati per il download massivo sono aggiornati con cadenza semestrale"; "licenza CC-BY 4.0". Servizi elencati: WMS, Geoportale cartografico, WFS, Download massivo [V].
- **La proprietà (intestatari) non fa parte di questi servizi** [V: la pagina parla solo di particelle]. È accessibile solo con visura catastale e ipotecaria, per particella [S, conoscenza generale non riscontrata qui]. **Confermato: non aperta.**
- Il Catasto fabbricati (unità immobiliari, categorie, rendite) non è disponibile come open data [L].

### 2.7 Piano Casa Milano ("Casa accessibile")
- **Pagine ufficiali non raggiungibili** da questo ambiente [V: 403]. Quello che segue è **[S]**, da risultati di ricerca e fonti secondarie (Assolombarda, Il Foglio, Il Giorno, Affaritaliani):
  - Delibera di Giunta n. 1299 del 24/10/2024: linee di indirizzo, ~10.000 alloggi.
  - Delibera di Giunta n. 365 del 26/03/2026: indirizzi operativi per i bandi sulle aree ex Palasharp, San Romanello e Bovisasca.
  - Delibera di Giunta n. 359 del 26/03/2026: "Casa ai lavoratori", programma distinto.
- **Avvertenza sul canone [S].** Una fonte secondaria (Il Foglio, via sintesi della ricerca) riporta che il tetto del canone medio sarebbe passato **da 80 a 90 €/m²/anno** con le delibere del 2026, con locazione calmierata per almeno 30 anni e aree in concessione a 1 €/m². Altre testate citano ancora 80. **Il valore 80 €/m²/anno usato nelle note non va usato finché non si legge la DG 365/2026** [L].
- Altri casi citati [S]: via Demostene (4 offerte), via Trivulzio 18, Porto di Mare, Zama-Salomone. Il documento C40 "Reinventing Cities – Bovisasca – requisiti specifici" è online (c40reinventingcities.org) [S, non aperto].

### 2.8 ALER Milano / MM Casa
- Sito ALER raggiungibile [V]. La sezione Amministrazione trasparente ha le pagine "Patrimonio" e "Beni immobili e gestione patrimonio" [V]. Nell'HTML statico non c'è un elenco scaricabile degli alloggi: solo normativa (L.R. 16/2016, R.R. 4/2017, D.Lgs. 33/2013) [V]. La presenza di un elenco caricato via JavaScript o in altra pagina resta [L].
- MM (www.mmspa.eu) rispondeva 403 [V]. I dati sullo stock ERP comunale gestito da MM restano **[L]**.

---

## 3. Gap analysis rispetto al modello

Il modello ha bisogno di tre cose:
- **famiglie** (vettore dei desideri: ancore, pesi, budget) per la popolazione sintetica;
- **lotti** (posizione, capacità, vincoli, proprietà, costo developer vs cooperativa, ΔL);
- **regole di assegnazione** (riserve di capacità per categoria).

| Variabile del modello | Stato | Fonte e risoluzione | Note |
|---|---|---|---|
| Famiglie per tipo (nucleo, età del capofamiglia, componenti) | **Disponibile** | ds1441, NIL × anno fino al 2025 [V]; ds2845, sezione 2021, solo FAM21 [V]; ISTAT 2021 per sezione, solo per n. componenti [V] | Tipo di nucleo per sezione: mancante [V]. Il NIL basta per le marginali dell'IPF [I] |
| Età, stranieri, istruzione, occupati | **Disponibile** | ISTAT 2021, sezione [V]; anagrafe, NIL [V] | — |
| Titolo di godimento (affittuari) | **Parziale** | ds1457, NIL, **2011** [V] | Nessun dato 2021 sub-comunale [V per la sezione]. Sostituisce lo 0,30 piatto, ma con dati vecchi di 15 anni |
| Reddito (budget) | **Parziale** | IRPEF per CAP, 38 CAP, classi [V] | Sotto il CAP: mancante. ISEE aggregato per zona: non trovato [V per i cataloghi]. Il titolare è INPS/Comune (ISEE delle domande di servizi) [I] |
| Ancore scuola | **Disponibile** | ds3014–3016 (2025/26), punto [V] | Secondarie di II grado: ds78 vecchio, ds1863 al 2020/21 |
| Ancore cura (nidi, RSA, MMG) | **Disponibile/parziale** | ds586, ds234, ds501 aggiornati [V]; nidi ds47 fermi al 2019 [V] | Licenza di ds234 incoerente [V] |
| Ancore lavoro | **Parziale** | O/D 2011 per sezione (ds390–395) [V]; commercio puntuale (ds49/50/58) [V]; unità locali per NIL 2010 [V] | Addetti per luogo di lavoro aggiornati: mancanti in open data comunale. Fonte possibile: ISTAT ASIA unità locali [L] |
| Trasporto pubblico | **Disponibile** | GTFS ds929 (bisettimanale) [V] | — |
| Verde, calore | **Disponibile** | ds3018, ds2813/2816, ds2484 [V] | — |
| Canoni e prezzi di mercato | **Disponibile** | OMI 2004–2025/2, zone con perimetri [V] | Valori di zona, non contratti. Canoni dei contratti in essere: Agenzia Entrate (registrazioni), non aperti [L] |
| Geometria dei lotti | **Disponibile** | Particelle catastali CC-BY 4.0, semestrali [V]; DBT 2020 CC-BY 2.5 IT [V] | — |
| **Proprietà comunale** | **Parziale (datata)** | ds677, 2019, foglio e mappale [V] | **Da aggiornare**: elenco 2025/2026, superfici, stato d'uso, vincoli di destinazione, aree già messe a bando |
| Proprietà statale | **Disponibile** | Demanio ds2688/2689, 2023 [V] | — |
| Proprietà ERP (ALER/MM) | **Mancante** | — | Titolari: Comune/MM (alloggi comunali), ALER Milano, Regione |
| Proprietà privata | **Mancante (non apribile)** | Catasto, visure [S] | Fuori portata: si usano classi pubblica / presunta / ignota (nota 10) |
| Aree candidate pubbliche (Piano Casa) | **Mancante come dato** | Solo atti e stampa [S] | Elenco e perimetri delle aree messe e da mettere a bando: Comune |
| Strati PGT 2030 (AT, ERS, servizi, vincoli) | **Parziale / [L]** | Geoportale comunale non raggiungibile [L]; varianti PdR via Regione [V] | Da riscaricare quando il dominio sarà raggiungibile. Non è materia di richiesta formale se gli strati sono pubblicati [I] |
| Indici edificatori (IT, perequazione, premialità ERS) | **Parziale** | NdA del Piano delle Regole (testo) [L] | Da codificare a mano. Richiesta solo se esiste una tabella per ambito o lotto [H] |
| Vincoli | **Parziale** | Bonifiche ds600 [V]; tavole R05/R06 e carta dei vincoli (PDF) [V esistenza]; PAI/PGRA tramite variante [V] | Vettoriali dei vincoli [L] sul Geoportale |
| Edifici dismessi o degradati | **Parziale** | ds503, 2014–2017 [V] | Aggiornamento dell'art. 11 NdA: Comune |
| Produzione edilizia reale (calibrazione) | **Disponibile** | ds270/271 (2014–2024) [V] | Senza costi |
| Costo di costruzione | **Parziale** | SACC Regione: 6 casi milanesi di cooperativa con investimento [V] | Nessun dato aperto sui costi dei developer [V per i cataloghi]. Il Comune riceve i computi metrici (contributo sul costo di costruzione) [I] |
| Oneri di urbanizzazione, costo base | **Mancante come dataset** | Delibere [S] | Tabelle negli atti: va letto l'atto, non serve una richiesta [I] |
| Canone e regole Piano Casa (tetto €/m², durata, canone concessorio) | **Da riscontrare** | DG 365/2026 [S] | Si risolve leggendo l'atto, non con una richiesta formale [I] |
| Domanda reale (graduatorie SAP, ISEE dei richiedenti, sfratti) | **Mancante** | — | Titolari: Comune (Direzione Casa), Regione (piattaforma SAP), Prefettura/Tribunale per gli sfratti [I] |
| Preferenze delle famiglie | **Mancante (per costruzione)** | — | Solo F2 con persone reali [V, DECISIONI] |

### 3.1 Il FOIA è lo strumento giusto?
- La **richiesta di accesso civico generalizzato** (art. 5 c. 2 D.Lgs. 33/2013) è adatta a dati e documenti già detenuti dall'ente, in forma aggregata e senza dati personali [S, conoscenza della norma, non riscontrata in sessione]. Non obbliga l'ente a fare elaborazioni nuove [S]: per questo la richiesta va formulata come **estrazione di archivi esistenti**, non come analisi.
- **Adatta** per: elenco aggiornato del patrimonio comunale; stock ERP comunale per edificio; aree Piano Casa; statistiche SAP aggregate; computi o quadri economici dei bandi Piano Casa e degli interventi convenzionati.
- **Non adatta** per:
  - la proprietà privata (dati personali, limite dell'art. 5-bis);
  - microdati di reddito o ISEE (dati personali e fiscali);
  - documenti già pubblicati (PGT, delibere), che si scaricano.
- **ALER Milano** è un ente pubblico economico regionale soggetto al D.Lgs. 33/2013 (lo dichiara il sito, che ha una sezione Amministrazione trasparente [V]). La richiesta sullo stock ALER va fatta **ad ALER**, non al Comune [I].

---

## 4. Richiesta formale al Comune di Milano: cosa chiedere (solo ciò che manca davvero)

Destinatario: Comune di Milano, accesso civico generalizzato (D.Lgs. 33/2013, art. 5 c. 2). Formato richiesto: CSV/XLSX o vettoriale (SHP/GeoJSON), aggregato e senza dati personali.

1. **Patrimonio immobiliare comunale aggiornato**: è la versione corrente del dataset ds677, fermo al 2019. Per ogni bene: codice inventario, foglio, mappale, tipo (terreno/fabbricato), superficie, destinazione e stato d'uso (libero, in concessione, ERP, servizio), eventuale inserimento nel piano delle alienazioni o valorizzazioni.
2. **Aree e immobili del Piano straordinario Casa accessibile**. Elenco e perimetri (anche solo foglio e mappale) di tutte le aree e gli immobili individuati, messi a bando o in programma, con: superficie territoriale e SL ammessa, canone concessorio, canone massimo, durata, esito del bando e soggetto aggiudicatario.
3. **Stock ERP di proprietà comunale gestito da MM**, per edificio (indirizzo o foglio/mappale): n. alloggi, n. alloggi sfitti o non assegnabili, superficie media. Niente dati sugli inquilini.
4. **Quadri economici o piani economico-finanziari** già presentati nei bandi Piano Casa conclusi (per esempio via Demostene, via Trivulzio 18, Porto di Mare, Zama-Salomone). Servono costo di costruzione, oneri e costi tecnici per tarare il confronto developer/cooperativa. Si chiedono omettendo le parti coperte da segreto commerciale.
5. **Statistiche aggregate della domanda abitativa pubblica**, per NIL o municipio: n. domande SAP nell'ultimo avviso per composizione del nucleo e classe ISEE, n. assegnazioni. Solo se le detiene il Comune; altrimenti la richiesta va a Regione.
6. **Aggiornamento del censimento degli edifici degradati o abbandonati** (art. 11 NdA PdR) successivo al 2017, cioè l'equivalente aggiornato di ds503.

**Da NON chiedere**, perché è già online o si risolve leggendo un atto:
- strati e NdA del PGT 2030;
- delibere Piano Casa (DG 1299/2024, 365/2026, 359/2026);
- tabelle degli oneri;
- quotazioni OMI;
- IRPEF per CAP;
- famiglie per NIL;
- sezioni 2021.

Vanno scaricati e letti appena i domini comunali saranno raggiungibili.

**Richieste separate, da valutare:**
- **ALER Milano**: stock per edificio nel comune di Milano.
- **Regione Lombardia**: dati aggregati della piattaforma SAP; dettaglio SACC (l'investimento include il suolo?).

---

## 5. Prossimi passi pratici [I]

1. Rendere raggiungibili `www.comune.milano.it`, `pgt.comune.milano.it` e `geoportale.comune.milano.it` (impostazioni di rete dell'ambiente) e completare le voci [L]: PGT 2030, Geoportale, DG 365/2026, pagina del patrimonio.
2. Fare il join di ds677 (foglio e mappale) con le particelle catastali e con i 2.291 siti del Lab, per misurare quanti siti diventano "pubblica nota".
3. Sostituire la quota di affittuari 0,30 con ds1457 (2011, per NIL) e dichiararne l'età.
4. Leggere SACC e ds270 come primi riferimenti di costo e dimensione per la taratura.

**Fonti delle voci [S]** (risultati di ricerca, non aperti):
- [Assolombarda – Casa Accessibile, nuove linee di indirizzo](https://www.assolombarda.it/servizi/immobili-urbanistica-e-territorio/informazioni/casa-accessibile-nuove-linee-di-indirizzo-del-piano-straordinario-del-comune-di-milano)
- [Il Foglio, 02/04/2026](https://ilfoglio.it/gran-milano/2026/04/02/news/il-piano-casa-del-comune-di-milano-alla-prova-dei-fatti-arrivano-tre-bandi--268556)
- [Affaritaliani – Piano casa](https://www.affaritaliani.it/milano/milano-affitti-da-375-euro-per-50-metri-quadri-via-al-piano-casa-del-comune.html)
- [Assolombarda – DG 359/2026 all. 1](https://www.assolombarda.it/servizi/immobili-urbanistica-e-territorio/documenti/delg-359-2026_all1)
- [C40 Reinventing Cities – Bovisasca](https://www.c40reinventingcities.org/data/sites_134e6/fiche/398/ita_requisiti_specifici_-_bovisasca_-_reinventing_cities.docx_8e8c3.pdf)
