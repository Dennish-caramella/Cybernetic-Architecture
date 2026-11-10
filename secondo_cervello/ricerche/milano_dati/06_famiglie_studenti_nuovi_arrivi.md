# Milano: famiglie, studenti, nuovi arrivi — le popolazioni che mancano (stato al 10/11/2026)

> Note di ricerca, non testo di tesi. Completa `02_mercato_e_accessibilita.md`, la cui analisi dei redditi copre solo i **contribuenti residenti** (MEF).
> Calcoli: `popolazioni/analisi_popolazioni.py` (input open data scaricati in sessione, non versionati); CSV derivati in `popolazioni/` (76 kB).
> Marche: **[V]** dato ufficiale aperto/scaricato in questa sessione (10/11/2026), URL indicato; **[S]** fonte secondaria (stampa, report privati, istituzionali citati da terzi) o non riaperta; **[L]** solo citato, non verificato; **[I]** inferenza/calcolo mio; **[H]** ipotesi dichiarata.

## 0. Sintesi

- [V] **Titolo di godimento, Milano 2021 (ISTAT, censimento permanente, famiglie):** su 713.971 famiglie, **62,8% proprietarie, 32,4% in affitto, 4,8% altro titolo**. È il parametro mancante della nota 02 (lì si ipotizzava 30%). Ma le fonti divergono: ISTAT 2019 *per abitazioni occupate* dà **70,0% / 25,4% / 4,5%**; il censimento 2011 (ds1457, abitazioni) **64,1% / 28,9% / 7,0%**. → Per il modello: **affitto 25–32%, valore centrale ~30–32% delle famiglie (≈ 230 mila famiglie in affitto)** [I].
- [V] **Famiglie 2025 (anagrafe, ds1441):** 780.935; monocomponenti 55,7%; famiglie con figli (di qualsiasi età) 212.733 (27,2%); anziani soli (≥65) 127.837 (16,4%); capofamiglia straniero 22,4%. **Con figli minori** (ds139, solo fino al 2021): 129.558 famiglie (18,3%), di cui **31.081 monogenitori** con minori.
- [V] **Reddito familiare (non per contribuente), Lombardia 2024 (ISTAT EU-SILC):** mediana **36.875 €** netti annui (senza fitti imputati), media 45.525 €. Per Milano non esiste un reddito familiare ufficiale pubblicato [V, cercato].
- [V] **Studenti:** **211.440 iscritti** negli atenei milanesi nel 2024/25 (7 atenei, MUR via ds752; esclusi NABA, Brera, IED, Conservatorio ecc.). **Fuori sede stimati 50–90 mila** [S, stime non ufficiali e discordanti]; **posti letto in residenze 11–16 mila** [S]; posti DSU a tariffa agevolata del Comune per il 2024/25: 897 [S]. **Copertura ≤ ~1/5 dei fuori sede; scarto ≥ 35–75 mila posti** [I]. Stanza singola: **~700–730 €/mese** (annunci, Immobiliare.it Insights) [S].
- [V] **Nuovi arrivi:** **~49 mila iscrizioni anagrafiche all'anno** (media 2015–2024) e ~39 mila cancellazioni; 2024: 46.568 iscritti, 44.006 cancellati. Il saldo naturale è negativo (~ −4.400/anno): **Milano cresce solo per immigrazione** [I].
- [V] **Pendolari in entrata (2011, ultima matrice aperta):** ~**475 mila** al giorno (368 mila per lavoro, 107 mila per studio); un terzo impiega oltre 60 minuti. La matrice 2021 esiste (ISTAT, pubblicata il 2/10/2025) ma non è scaricabile via API [V, tentato].
- [I] **Invisibili nei dati MEF dei contribuenti milanesi:** studenti fuori sede (non residenti e quasi sempre senza dichiarazione), pendolari (dichiarano nel comune di residenza), nuovi arrivati nell'anno (dichiarano l'anno dopo, e chi non è ancora residente altrove), minori, lavoro irregolare, e in generale **le famiglie come unità** (il MEF conta individui).

## 1. Famiglie

### 1.1 Tipologie 2025 (anagrafe) [V]
Fonte: Comune di Milano, `ds1441` *Famiglie anagrafiche: tipologie per NIL (1999-2025)*, https://dati.comune.milano.it/dataset/ds1441-famiglie-tipologie-per-quartiere (scaricato 10/11/2026, risorsa CSV in zip). Elaborazioni: `popolazioni/famiglie_2025_milano_ds1441.csv`, `famiglie_2025_per_NIL_ds1441.csv`, serie `famiglie_serie_tipologia_ds1441.csv`.

| Tipologia (2025) | Famiglie | Quota |
|---|---|---|
| Monocomponente | 435.044 | 55,7% |
| Coppia sposata con figli | 111.121 | 14,2% |
| Coppia sposata senza figli | 81.561 | 10,4% |
| Monogenitore con figli | 72.252 | 9,3% |
| Monogenitore con figli e almeno un convivente | 29.360 | 3,8% |
| Capofamiglia con almeno un convivente | 26.244 | 3,4% |
| In convivenza | 14.191 | 1,8% |
| Altre tipologie | 11.162 | 1,4% |
| **Totale** | **780.935** | |

- Per numero di componenti: 1 = 449.235 (57,5%), 2 = 159.194, 3 = 88.676, 4 = 62.066, 5+ = 21.764 [V]. (I "monocomponenti" per tipologia, 435.044, sono meno delle famiglie di 1 persona: la differenza sta in "altre tipologie" [I].)
- Età del capofamiglia: < 35 anni 127.178 (16,3%); 35–64 420.387 (53,8%); 65–79 138.495; 80+ 94.875 [V].
- **Anziani soli**: monocomponenti 65–79 = 71.049, 80+ = 56.788 → **127.837** [V/I]. (ds205 per il 2024: 57.073 ultraottantenni soli [V].)
- **Giovani soli**: monocomponenti < 35 anni = **99.249**; il 78% delle famiglie con capofamiglia < 35 è monocomponente [V/I].
- Capofamiglia con cittadinanza non italiana: 174.780 (22,4%) [V].
- **Attenzione [I]**: ds1441 non distingue figli minori e maggiorenni; le coppie non sposate con figli finiscono plausibilmente in "monogenitore con figli e almeno un convivente" o "in convivenza". Le famiglie anagrafiche gonfiano i single (residenze separate per ragioni fiscali o di accesso a servizi), come già notato in 02.
- Serie: monocomponenti da 321.165 (2005) a 435.044 (2025, +35%); coppie sposate con figli da 144.806 a 111.121 (−23%) [V]. Il totale cresce (676 mila → 781 mila) quasi solo per famiglie di una persona [I].
- Per NIL: la quota di famiglie con figli (qualsiasi età) va da 1,8% a 44,1%, mediana 27,7% [V/I, NIL con pochi residenti inclusi].

### 1.2 Famiglie con minori e monogenitori (2021) [V]
Fonte: `ds139` *Famiglie: tipologie per quartiere* (2007–2021), https://dati.comune.milano.it/dataset/ds139-popolazione-famiglie-tipologia-quartiere (scaricato 10/11/2026). Ultimo anno con la distinzione minori/maggiorenni. CSV: `famiglie_2021_con_minori_ds139.csv`, `famiglie_2021_con_minori_per_NIL_ds139.csv`.

| Tipologia (2021) | Famiglie |
|---|---|
| Coppia sposata con almeno un figlio minorenne | 72.797 |
| Coppia convivente con almeno un figlio minorenne | 25.680 |
| **Monogenitore con almeno un figlio minorenne** | **31.081** |
| Coppie con figli tutti maggiorenni (sposate + conviventi) | 53.928 |
| Monogenitore con figli tutti maggiorenni | 46.956 |
| Single | 335.921 |
| Coppie senza figli (sposate + conviventi) | 122.325 |
| Altre | 18.227 |
| Totale | 706.915 |

- **Famiglie con almeno un minore: 129.558 (18,3%)**; monogenitori con minori 4,4% [I]. Per NIL la quota con minori va dal 12,2% al 60% (mediana 19,1%) [I].
- Minori residenti 2024: 196.577 (ds205, somma NIL) [V].
- **Disaccordo [V]**: ds139 nel 2021 conta 706.915 famiglie, ds1441 nel 2021 ne conta 751.850 (definizioni o trattamento delle convivenze diversi; non chiarito nelle note). ISTAT censimento 2021: 713.971 famiglie. Le quote vanno lette dentro la loro fonte.

### 1.3 Reddito delle famiglie [V]
Nessuna fonte ufficiale aperta dà il reddito **familiare** per Milano [V, cercato in catalogo comunale e IstatData]. Il dato più vicino:
ISTAT, *Reddito netto delle famiglie – Regioni e tipo di comune* (EU-SILC), dataflow `32_292_DF_DCCV_REDNETFAMFONTERED_9`, https://esploradati.istat.it/SDMXWS/rest/data/IT1,32_292_DF_DCCV_REDNETFAMFONTERED_9,1.0/.ITC4............ (scaricato 10/11/2026) → `popolazioni/istat_reddito_netto_famiglie_lombardia_2021_2024.csv`.

| Lombardia, reddito netto familiare annuo | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|
| Mediana, senza fitti imputati | 30.276 | 32.485 | 33.336 | **36.875** |
| Media, senza fitti imputati | 40.277 | 41.428 | 43.825 | 45.525 |
| Mediana, con fitti imputati | 36.317 | 38.638 | 39.579 | 43.240 |

- Mediana 2024 per fonte principale di reddito [V, codici interpretati da me [I]: 1 = lavoro dipendente, 2 = autonomo, 3 = pensioni, 4 = altro]: 43.262 / 48.694 / 27.593 / 32.904 €.
- [I] Confronto con la nota 02: la mediana dei **contribuenti** milanesi è ~25.900 € **lordi**; la mediana delle **famiglie** lombarde è ~36.900 € **netti**. Le famiglie con due redditi stanno ben sopra il contribuente mediano; anziani soli e monogenitori sotto. Il dato regionale probabilmente **sottostima** Milano (reddito medio dei contribuenti milanesi 41,9k contro una media lombarda più bassa) [I, non quantificato].
- Non trovati: Banca d'Italia IBF per Lombardia/Milano (microdati con registrazione) [L]; il "tipo di comune" (centri metropolitani) nel dataflow 9 non era valorizzato per la Lombardia nella query [V].

### 1.4 Titolo di godimento (proprietà/affitto) — il parametro chiave [V]

| Fonte | Unità | Anno | Proprietà | Affitto | Altro | Totale |
|---|---|---|---|---|---|---|
| ISTAT `DF_DCSS_HUDW_1_COM` (censimento permanente) | **famiglie** | 2021 | 448.605 (**62,8%**) | 231.364 (**32,4%**) | 34.001 (4,8%) | 713.971 |
| ISTAT `DF_DCSS_ABITAZIONI_TV_2` | abitazioni occupate | 2019 | 504.563 (70,0%) | 183.227 (25,4%) | 32.734 (4,5%) | 720.524 |
| Comune `ds1457` (censimento 2011) | abitazioni occupate | 2011 | 387.714 (64,1%) | 174.556 (28,9%) | 42.240 (7,0%) | 604.510 |

URL: https://esploradati.istat.it/SDMXWS/rest/data/IT1,DF_DCSS_HUDW_1_COM,1.0/.015146........ e …/DF_DCSS_ABITAZIONI_TV_2,1.0/.015146....... (scaricati 10/11/2026; il dato abitazioni non ha valori per titolo nel 2021 e 2023, solo totali 700.586 e 722.273); https://dati.comune.milano.it/dataset/ds1457-censimento-abitazioni-occupate-suddivisione-per-nil. CSV: `istat_famiglie_titolo_godimento_milano_2021.csv`, `istat_abitazioni_titolo_milano_2019.csv`, `titolo_godimento_2011_per_NIL_ds1457.csv`.

- [I] La differenza 2019 (abitazioni, 25%) vs 2021 (famiglie, 32%) non è spiegata dalle note: unità diverse (più famiglie in una stessa abitazione in affitto, coabitazioni), stime campionarie del censimento permanente (valori decimali = stime pesate). **Per il modello uso le famiglie (32%)** perché l'agente è la famiglia; sensibilità 25–32%.
- [V/I] **Per NIL (2011)**, affitto dal 13,3% (QT8) al 57,1% (Gratosoglio–Ticinello), mediana 27,4% (NIL > 500 abitazioni). I NIL con più affitto sono quartieri ERP (Gratosoglio, Ponte Lambro 50%, Barona 48,8%): l'"affitto" 2011 mescola ERP e mercato. ISTAT 2024 (report Commissione periferie) conferma per il 2021 Parco Monluè–Ponte Lambro al 59,7% di famiglie non proprietarie e >50% in Triulzo Superiore, Selinunte, Quarto Oggiaro [V: https://www.istat.it/wp-content/uploads/2024/06/Approfondimento_Milano.pdf, aperto 10/11/2026].
- Contesto: Italia 2023 famiglie in affitto 19,6%, Nord-ovest 21,6% [V: ISTAT, *Abitazioni occupate. Anni 2021-2023*, https://www.istat.it/wp-content/uploads/2026/02/Abitazioni-occupate-Anni-2021-2023.pdf]. Milano ha 1,5 volte la quota di affittuari del Nord-ovest [I].
- **Conseguenza per la nota 02 §5** [I]: con affitto 32% la "pancia effettiva" stimata lì (~25–45 mila famiglie con canoni OMI; ~80–100 mila con canoni d'annuncio) sale di circa il 7%. Restano valide le avvertenze (percentili di contribuenti, non di famiglie).

## 2. Studenti

### 2.1 Iscritti [V]
Fonte: Comune di Milano `ds752` *Iscritti nelle Università milanesi 2017–2025* (fonte MUR/MIM), https://dati.comune.milano.it/dataset/ds752_iscritti-nelle-universita-milanesi-anno-accademico-2017-avanti (scaricato 10/11/2026) → `popolazioni/iscritti_universita_milanesi_ds752.csv`.

| Ateneo | 2019/20 | 2024/25 |
|---|---|---|
| Statale | 60.468 | 57.709 |
| Politecnico | 45.288 | 48.291 |
| Cattolica (sede Milano) | 41.049 | 41.709 |
| Bicocca | 33.418 | 36.131 |
| Bocconi | 13.503 | 13.981 |
| IULM | 6.764 | 7.814 |
| San Raffaele | 2.955 | 5.805 |
| **Totale** | 203.445 | **211.440** |

- Coerente con "quasi 212 mila" (University Observatory, Statale–Cineca–Deloitte, citato da Pagella Politica) [S].
- Esclusi: AFAM (NABA, Brera, Conservatorio), IED, Humanitas dopo il 2017, università telematiche [V/I]. Il 2018/19 ha un'anomalia (Cattolica 27.696): file "no_dupl" con trattamento diverso [V].
- **Fuori sede / internazionali: nessun dato ufficiale aperto per Milano trovato in sessione.** ISTAT `56_1045/56_1046` (iscritti per comune dell'ateneo e di residenza) arriva solo al 2017 [V]; il portale USTAT-MUR (dati-ustat.mur.gov.it) non ha risposto (connessione chiusa) [V, tentato] → **lacuna prioritaria**.

### 2.2 Fuori sede e posti letto [S]
Stime **discordanti**, nessuna ufficiale:

| Grandezza | Valore | Fonte |
|---|---|---|
| Studenti fuori sede a Milano | "oltre 90 mila" | Pagella Politica (Mappatura residenze universitarie milanesi) [S] |
| | ~70 mila (area, 2023) | Città metropolitana, tavolo università 5/4/2023 [S, solo citato] |
| | 50 mila su 221 mila | dichiarazione di un amministratore di Sesto S.G. (Il Giorno) [S] |
| Posti letto in studentati | poco più di 11 mila (2023) | Comune, *Piano triennale offerta abitativa 2023–2025* [S, via Pagella Politica] |
| | 14.500 (a.a. 2023/24) | Re/Scenari Immobiliari [S] |
| | ~16 mila | "Mappatura delle residenze universitarie milanesi" [S] |
| | 12.100 | Scenari Immobiliari (altro rapporto) [S] |
| Posti agevolati Comune 2024/25 | 897 in 6 strutture | Pagella Politica [S] |
| Bocconi / Politecnico | 2.100 / 1.612 posti | Pagella Politica [S] |
| Bicocca | +288 posti (+47%) nel 2025 | comunicato UniMiB [S] |
| In costruzione | Villaggio olimpico Porta Romana → ~1.700 posti | Pagella Politica [S] |

- [I] **Scarto domanda–offerta**: tra 50k − 16k = ~34 mila (ipotesi ottimistica) e 90k − 11k = ~79 mila (pessimistica) fuori sede senza posto in residenza; copertura 12–32%. Il riferimento europeo citato è 20% di copertura come minimo [S].
- [I] Molti posti nuovi sono privati a canone pieno (rapporti stampa su studentati "per figli di professionisti", Avvenire) [S]: la copertura per studenti a basso reddito è molto inferiore al rapporto posti/fuori sede.

### 2.3 Canoni per studenti
- Stanza singola Milano, annunci: **732 €/mese** (agosto 2025), **704 €/mese** (2026, −4% sul 2025) [S, Immobiliare.it Insights via Sky TG24 / VareseNews; rapporto primario non aperto]. Zone più care: centro ~823 €, Porta Romana ~812 € [S, Il Giorno 2026].
- Residenze Politecnico, **tariffa intera** 2025/26, per anno accademico: singola con bagno privato 6.545 €; singola bagno condiviso 6.040 €; doppia 4.330–5.185 € [V: bando integrativo DSU Polimi 2025/26, https://www.polimi.it/fileadmin/user_upload/studenti/tasse-borse-agevolazioni-economiche/dsu/bando-2025-2026/Bando_integrativo_DSU_aa_25_26_ita.pdf, aperto 10/11/2026; durata del periodo da verificare nel bando]. [I] ≈ 550–650 €/mese su 10–11 mesi: poco sotto il mercato.

### 2.4 Soglie DSU (Regione Lombardia) [V]
Bando ISU Bocconi 2026/27 (applica i limiti regionali): https://www.unibocconi.it/sites/default/files/media/attachments/a.a.%202026-27%20Bando%20DEFINITIVO%20Borse%20di%20studio%20ISU%20Bocconi_5.pdf (aperto 10/11/2026).
- **ISEE ≤ 26.887,93 €; ISPE ≤ 58.452,06 €** (2026/27); 2025/26: 26.516,70 € / 57.645,03 € [V, stesso bando].
- Borsa 2026/27 (incl. pasto 829 €): **fuori sede 8.248 / 7.172 / 5.857 €** (fasce ISU 1/2/3: ISEE fino a 13.443,97 / 17.925,29 / 26.887,93), pendolare 4.820–3.299, in sede 3.430–2.143 [V].
- Politecnico 2025/26: fuori sede non in residenza 8.134 € (1ª fascia, con pasto); in residenza 4.556 € + alloggio + pasto [V, bando citato].
- "Fuori sede" = non residente nel comune della sede del corso e alloggio a titolo oneroso (Polimi) [V].
- [I] Una borsa fuori sede massima (8.248 €/anno ≈ 690 €/mese) copre appena il canone medio di una stanza (700–730 €): **la borsa non basta per vivere a Milano nel mercato privato**; un idoneo senza posto letto paga la casa con la borsa e il resto con la famiglia o il lavoro.

## 3. Nuovi arrivi

### 3.1 Iscrizioni e cancellazioni anagrafiche [V]
Fonte: `ds71` *Popolazione calcolata Istat: movimento naturale e migratorio (1880–2024)*, https://dati.comune.milano.it/dataset/ds71-popolazione-movimento-naturale-migratorio; `ds205` per NIL (2024). CSV: `movimento_anagrafico_2010_2024_ds71.csv`, `nil_immigrati_emigrati_minori_ds205.csv`.

| Anno | Iscritti (immigrati) | Cancellati (emigrati) | Saldo migratorio | Saldo naturale |
|---|---|---|---|---|
| 2019 | 55.841 | 41.901 | +13.940 | −3.300 |
| 2020 | 41.171 | 43.842 | −2.671 | −8.261 |
| 2021 | 45.364 | 46.452 | −1.088 | −4.445 |
| 2022 | 50.338 | 40.322 | +10.016 | −5.547 |
| 2023 | 62.188 | 42.694 | +19.494 | −4.677 |
| 2024 | 46.568 | 44.006 | +2.562 | −4.418 |
| media 2015–24 | **48.880** | **39.382** | +9.498 | |

- [I] Ogni anno entrano ~3,5% dei residenti e ne escono ~3%: **in dieci anni ~490 mila iscrizioni**, un ricambio enorme. Una parte sono regolarizzazioni e rettifiche (2013: 109.249, effetto post-censimento) [I].
- **Non trovato**: la ripartizione per **origine (altro comune / estero) e per età** degli iscritti a Milano. ISTAT `28_185_DF_DCIS_MIGRAZIONI_*` ha dettaglio solo fino alla provincia [V, verificato sui codici disponibili]; il dato comunale per età e provenienza è sul sito comune.milano.it (non raggiungibile) [L].
- NIL con più iscrizioni nel 2024: Buenos Aires–Venezia (2.185), Loreto–NoLo (1.787), Bande Nere (1.510) [V]. La somma NIL 2024 (46.953) è vicina al dato ISTAT (46.568) [V].
- Nota: la popolazione anagrafica 2024 di ds205 (1.407.044) supera quella ISTAT calcolata (1.365.698): differenza tra anagrafe e popolazione censuaria [V].

### 3.2 Pendolari in entrata (2011) [V]
Fonte: `ds395` *Censimento 2011: pendolari in entrata per mezzo, tempo, orario, comune di provenienza e genere*, https://dati.comune.milano.it/dataset/ds395-popolazione-pendolari-in-entrata-mezzo-tempo-orario-uscita-genere-2011c → `pendolari_entrata_2011_motivo_provincia_ds395.csv`.
- **474.680 ingressi giornalieri**: lavoro 367.953, studio 106.727 [V].
- Provenienza: provincia di Milano 207.298 (lavoro) + 52.509 (studio); Monza-Brianza 51.412 (lavoro); Pavia 21.746; Varese 19.788; Bergamo 12.747 [V].
- Mezzo: auto (conducente) 174.832; treno 141.579; metro 58.049 [V]. Tempo: > 60 minuti 158.238 (33%); 31–60 minuti 217.832 [V].
- Matrice 2021 (lavoro e studio) pubblicata da ISTAT il 2/10/2025 in IstatData (`DF_BULK_PEND_LAV_2021_1`, `DF_BULK_PEND_STU_2021_1`), ma l'API SDMX risponde "no mapping set" [V, tentato]: va scaricata dal databrowser a mano [L].

### 3.3 Nuovi lavoratori e chi vorrebbe vivere a Milano
- Salari d'ingresso, nuovi posti di lavoro per Milano: **non trovati in sessione** [L]. Fonti candidate: INPS Osservatorio lavoratori dipendenti (per provincia), Assolombarda *Osservatorio Milano*, Regione/PoliS Lombardia, Excelsior-Unioncamere.
- Indagini su "chi vorrebbe vivere a Milano ma non può": **nessuna verificata** [L]. Da cercare: Assolombarda (Osservatorio Student Housing, citato per "5% posti letto/matricole" in Italia [S]), Politecnico DAStU, Fondazione Cariplo/Housing sociale, Nomisma *Rapporto affitti Milano* 2021 [S, link trovato non aperto].
- Indizio indiretto [I]: un terzo dei pendolari impiega > 60 minuti; parte di loro sono residenti fuori per ragioni di costo, ma il dato non distingue la scelta dal vincolo.

## 4. Sintesi per popolazione

Ordini di grandezza; "MEF" = visibile nei dati IRPEF dei contribuenti milanesi.

| Popolazione | Dimensione | Reddito / capacità di spesa | Bisogno abitativo tipico | Risposta abitativa attuale | Nel modello della tesi | MEF |
|---|---|---|---|---|---|---|
| Lavoratori residenti (single e coppie senza figli) | ~435k monocomponenti (di cui ~208k 35–64 anni) + ~120k coppie senza figli [V] | dipendenti media 38,8k lordi [V, nota 02]; famiglie Lombardia mediana 36,9k netti [V] | mono/bilocale 40–60 m² | proprietà (63%) o mercato; ~32% in affitto [V] | ancora **lavoro**; budget dai percentili MEF | Sì (individui) |
| Famiglie con figli minori | ~130k (2021) [V], ~18% | due redditi: sopra la mediana; mediana famiglie con dipendente 43k netti (Lombardia) [V/I] | trilocale/quadrilocale 75–95 m², spazi aperti | proprietà o affitto; esodo verso l'hinterland (calo coppie con figli −23% in 20 anni) [V/I] | ancore **scuola** (ds3014–3016) + lavoro; riserva di capacità per famiglie con minori | Solo come individui; i figli no |
| Monogenitori con minori | ~31k (2021) [V] | un reddito; RTI > 30% fino al ~P79 con canoni OMI [I, nota 02] | bi/trilocale 60–70 m² | mercato, ERP; alta vulnerabilità | ancore scuola + cura; **riserva prioritaria** | Parziale |
| Anziani soli | ~128k (2025) [V]; 57k over 80 | pensioni: mediana famiglie Lombardia 27,6k netti [V] | piccolo alloggio accessibile, servizi vicini; spesso sottoutilizzo di alloggi grandi | in prevalenza proprietari [H, non verificato per età] | ancore **cura** (RSA, ADI, MMG); possibile offerta di scambio alloggio | Sì |
| Giovani soli < 35 | ~99k monocomponenti [V] | redditi d'ingresso (non trovati) [L] | monolocale/stanza, flessibilità | affitto di mercato, coabitazione | ancora lavoro; riserva giovani | Sì se residenti da ≥1 anno |
| Studenti fuori sede | 50–90k [S] su 211k iscritti [V] | borsa DSU max 8.248 €/a [V]; famiglia d'origine | posto letto/stanza 12–20 m², spazi comuni | 11–16k posti in residenze [S]; il resto stanze private ~700 €/mese [S] | ancore **università** (ds94 sedi); riserva studenti; tipo "posto letto" | **No** (non residenti, senza reddito) |
| Nuovi arrivati (iscritti in anagrafe) | ~49k/anno [V] | sconosciuto [L] | dipende dal tipo; molti soli o giovani coppie [H] | mercato degli annunci (canoni ~1,7× OMI [S/I, nota 02]) | flusso annuo di agenti in ingresso nella simulazione | No nell'anno d'arrivo |
| Pendolari | ~475k/giorno (2011) [V]; 368k per lavoro | lavoratori, redditi non noti in Milano | potenziale domanda latente (non misurata) | casa fuori Milano | domanda potenziale: agenti con ancora lavoro a Milano e casa fuori | **No** (dichiarano altrove) |

### 4.1 Indicazioni per il modello [I]
1. **Popolazione sintetica**: marginali per NIL da ds1441 (2025: tipologia × età capofamiglia × componenti) e ds139 (2021: minori); titolo di godimento da ds1457 (NIL, 2011) riscalato sul totale ISTAT 2021 (32,4% affitto).
2. **Vettore dei desideri**: ancora primaria per tipo: lavoro (lavoratori, pendolari), scuola (famiglie con minori), università (studenti), cura (anziani, monogenitori).
3. **Riserve di capacità sul lotto** (accettazione differita): famiglie con minori, monogenitori, anziani soli, giovani < 35, studenti; le proporzioni di partenza possono seguire le quote cittadine (18% / 4% / 16% / 13% / —) o un obiettivo di policy, da decidere.
4. **Tre popolazioni oggi fuori dal modello economico** perché invisibili nei dati MEF: studenti fuori sede, nuovi arrivati, pendolari. Per loro il budget va costruito da fonti diverse (DSU, salari d'ingresso INPS, ipotesi esplicite [H]).

## 5. Lacune e prossimi passi
1. USTAT-MUR: iscritti per ateneo e **regione/provincia di residenza** e cittadinanza (fuori sede e internazionali) — il portale non ha risposto.
2. Matrice di pendolarismo ISTAT 2021 (lavoro e studio): download manuale dal databrowser IstatData.
3. Iscrizioni anagrafiche per **età e provenienza** (comune.milano.it, Annuario statistico) [L].
4. Salari d'ingresso (INPS, Excelsior) e indagini sulla domanda latente (Assolombarda, Politecnico) [L].
5. Titolo di godimento per **tipo di famiglia ed età** a Milano (microdati censimento o EU-SILC) [L].
6. Riaprire i rapporti primari citati [S]: Immobiliare.it Insights (stanze), Scenari Immobiliari / Re (posti letto), Piano triennale comunale 2023–2025.

## Fonti aperte/scaricate in questa sessione (10/11/2026)
- Comune di Milano open data (API CKAN): ds1441, ds139, ds1457, ds1449, ds71, ds205, ds752, ds395 — https://dati.comune.milano.it
- ISTAT IstatData SDMX: `DF_DCSS_HUDW_1_COM`, `DF_DCSS_ABITAZIONI_TV_2`, `32_292_DF_DCCV_REDNETFAMFONTERED_9` — https://esploradati.istat.it/SDMXWS/rest/
- ISTAT, *Report Comune di Milano* (Commissione periferie, 26/6/2024); *Abitazioni occupate. Anni 2021-2023* (2026) — URL nel testo.
- ISTAT, pagina *Matrici di contiguità, distanza e pendolarismo* — https://www.istat.it/notizia/matrici-di-contiguita-distanza-e-pendolarismo/
- Bandi DSU: Bocconi ISU 2026/27; Politecnico integrativo 2025/26 — URL nel testo.
- [S] Pagella Politica, *La risposta di Milano alla crisi abitativa degli studenti non è per nulla chiara*, https://pagellapolitica.it/articoli/milano-posti-letto-studenti-scarsa-trasparenza (aperto 10/11/2026, data dell'articolo non estratta); Sky TG24 4/8/2026 e 21/8/2025 (stanze); comunicato UniMiB luglio 2025.
