# Milano: mercato abitativo e peso della casa sui redditi (stato al 10/11/2026)

> Note di ricerca, non testo di tesi. Calcoli riproducibili: `mercato/analisi_accessibilita.py` (input scaricati in sessione, non versionati) e `mercato/fetch_eurostat.py`. CSV derivati in `mercato/`.
> Marche: **[V]** = dato ufficiale scaricato/aperto in questa sessione (10/11/2026), URL indicato; **[S]** = fonte secondaria o non riaperta qui; **[L]** = solo citato in letteratura; **[I]** = inferenza/calcolo mio; **[H]** = ipotesi dichiarata.

## 0. Sintesi (per chi ha due minuti)

- [I] **Il canone di mercato a Milano diventa "non sostenibile" (>30% del reddito netto) attorno alla mediana dei contribuenti per una persona sola**, e già sotto la mediana per anziani soli e famiglie monoreddito con figli. Con i **canoni OMI** (valori di stima, più bassi degli annunci) una persona sola supera il 30% fino a circa il **56° percentile** dei contribuenti milanesi (lordo ~31.000 €); con i **canoni richiesti negli annunci** [S] fino all'**85° percentile** (lordo ~63.000 €).
- [I] La **"pancia"** — chi supera la soglia ERP (ISEE > 16.000 €) ma non regge il mercato al 30% — copre circa **8–21 punti percentili** della distribuzione dei redditi con i canoni OMI e **31–44 punti** con i canoni d'annuncio, a seconda del tipo di famiglia. Su ~781.000 famiglie anagrafiche [V] è un ordine di grandezza di **decine di migliaia (OMI) fino a ~300 mila (annunci) famiglie "equivalenti"**; solo la quota in affitto o in cerca di casa ne subisce davvero il costo (vedi §5, ipotesi forti).
- [V] In dieci anni (2015 S1 → 2025 S2) la **mediana tra zone OMI del canone** (abitazioni civili, stato normale) è salita da **8,0 a 13,6 €/m²/mese (+70%)** e del **prezzo** da **2.500 a 3.850 €/m² (+54%)**; l'inflazione italiana (HICP) è salita del **+24%** (2015→2025) [V] e il reddito complessivo medio dei contribuenti milanesi del **+29%** (2014→2024, nominale) [V].
- [V] Il tetto **Piano Casa** è stato portato da 80 a **90 €/m²/anno** di canone medio massimo (Delibera di Giunta 365 del 26/03/2026, fonte secondaria istituzionale Assolombarda): a 90 €/m²/anno l'affitto è sostenibile al 30% dal ~25°–44° percentile in su secondo il tipo di famiglia.

## 1. Redditi

### 1.1 MEF, dichiarazioni IRPEF 2025 (anno d'imposta 2024), Comune di Milano [V]
Fonte: MEF–Dipartimento Finanze, *Redditi e principali variabili IRPEF su base comunale*, CSV 2024, https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip (scaricato 10/11/2026). Elaborazione: `mercato/mef_milano_classi_reddito_2014_2024.csv`.

| Voce (Milano, a.i. 2024) | Valore |
|---|---|
| Contribuenti | 1.052.520 |
| Con reddito complessivo | 1.013.593; totale 42,43 mld €; **media 41.865 €** |
| Lavoro dipendente | 627.248 percettori, media 38.766 € |
| Pensione | 289.718 percettori, media 29.814 € |
| Imposta netta totale | 10,56 mld € |

| Classe di reddito complessivo | Contribuenti | Quota contribuenti | Quota reddito |
|---|---|---|---|
| ≤ 0 | 206 | 0,0% | — |
| 0–10k | 208.362 | 20,6% | 2,1% |
| 10–15k | 89.347 | 8,8% | 2,6% |
| 15–26k | 210.434 | 20,8% | 10,2% |
| 26–55k | 328.425 | 32,4% | 28,6% |
| 55–75k | 67.330 | 6,6% | 10,1% |
| 75–120k | 60.251 | 5,9% | 13,2% |
| > 120k | 49.238 | **4,9%** | **33,0%** |

- [I] Distribuzione molto asimmetrica: il 4,9% sopra 120k dichiara un terzo del reddito; la media (41,9k) è ingannevole, la **mediana stimata è ~25.900 €**.
- Confronto 2014 [V] (stesso dataset, CSV 2014): media 32.478 €, 961.612 contribuenti con reddito; **+28,9% nominale** in dieci anni, contro HICP Italia +24,3% (2014→2025, base 2015, Eurostat `prc_hicp_aind`) [V] → reddito medio reale quasi fermo; la crescita è concentrata in alto [I].

**Percentili dei contribuenti** (interpolazione lineare entro classe [I]; redditi ≤ 0 esclusi) — `mef_milano_percentili_contribuenti.csv`:

| | P20 | P40 | P50 | P60 | P80 |
|---|---|---|---|---|---|
| Lordo (compl.) 2024 | 9.727 | 20.627 | 25.924 | 34.820 | 52.717 |
| Lordo 2014 | 8.074 | 16.879 | 21.033 | 25.187 | 45.970 |
| Netto 2024 [H, calcolo] dipendente | 10.525 | 18.194 | 21.562 | 26.590 | 36.171 |
| Netto 2024 [H] pensionato | 9.246 | 16.784 | 20.281 | 25.690 | 36.171 |

Limiti [I]: (a) unità = contribuente, non famiglia; (b) la classe 0–10k (20,6%) contiene redditi parziali (part-time, studenti, chi ha altre entrate, chi ha lavorato parte dell'anno): il P20 sottostima il reddito familiare; (c) l'interpolazione uniforme entro classi larghe (26–55k) è grossolana; (d) mancano redditi esenti/cedolare secca e lavoro nero.

**Netto [H]**: IRPEF 2024 (23/35/43%, soglie 28k/50k), detrazioni art. 13 TUIR (dipendente o pensione), trattamento integrativo 1.200 € fino a 15k (dipendenti), addizionale regionale Lombardia 1,23/1,58/1,72/1,73% [S], comunale Milano 0,8% con esenzione fino a 23.000 € [S, da riscontrare sulla delibera comunale]. Nessun'altra detrazione.

### 1.2 Per CAP [V]
Stessa fonte, file *subcomunale* (CAP) 2024 → `mef_milano_cap_2024.csv` (38 CAP; per 18 CAP il MEF non pubblica le classi, quindi c'è solo la media).
- Media per CAP da **21.348 € (20157, Quarto Oggiaro/Roserio–Vialba)** a **97.222 € (20145)**; 20121/20122/20123 (centro) 85k/74k/90k. Mediana interpolata: da 18.557 € (20157) a 43.768 € (20145). Nel centro la mediana (≈23–38k) è molto sotto la media: dispersione interna altissima [I].
- Quota di contribuenti sotto 26k: dal 34% (20145) al 70% (20157).

### 1.3 Reddito delle famiglie, Lombardia e Italia [V]
Eurostat, API `nama_10r_2hhinc` e `ilc_di03`, `ilc_li01` (scaricati 10/11/2026, https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/…; CSV in `mercato/eurostat_*.csv`):
- Reddito disponibile netto delle famiglie per abitante (B6N), 2024: **Lombardia (ITC4) 26.600 €**, Nord-Ovest 25.700 €, Italia 22.000 €.
- Reddito equivalente mediano Italia (EU-SILC 2025, redditi 2024): **22.062 €**; media 25.011 €.
- Soglia di rischio povertà (60% mediana), Italia, EU-SILC 2025: **13.237 €/anno** persona sola; 19.856 € due adulti; 27.798 € due adulti + 2 figli < 14.
- Non scaricato: ISTAT reddito familiare netto per regione (SDMX ISTAT non rispondeva, timeout) → lacuna.

### 1.4 Famiglie a Milano [V]
Comune di Milano open data `ds1442` (famiglie anagrafiche per municipio, 1999–2025), https://dati.comune.milano.it/dataset/ds1442-famiglie-anagrafiche-residenti-per-municipio (scaricato 10/11/2026):
- 2025: **780.935 famiglie**; 1 componente **449.235 (57,5%)**, 2: 159.194, 3: 88.676, 4: 62.066, 5+: 21.764.
- Monocomponenti con capofamiglia ≥ 65 anni: 131.515 (65–79: 72.198; 80+: 59.317).
- Tipologia (ds139, 2021, 706.915 famiglie): single 335.921; coppie senza figli 122.325; coppie con figli minori 98.477; monogenitori con figli minori 31.081 [V]. [I] Le famiglie anagrafiche monocomponenti sovrastimano i single "reali" (residenze separate per ragioni fiscali/abitative).

## 2. Prezzi, canoni, compravendite

### 2.1 OMI (Agenzia Entrate) via Comune di Milano [V]
Fonte: Comune di Milano open data, che ripubblica le quotazioni OMI: `ds3024` (locazione 2025/2), `ds3025` (compravendita 2025/2), `ds1996` (riepilogo 2004–2025), https://dati.comune.milano.it/dataset?q=OMI (scaricati 10/11/2026; metadati aggiornati 27–28/10/2026). Tipologia "Abitazioni civili", stato "NORMALE"; €/m² di superficie **lorda**; canone €/m²/mese. **40 zone OMI** nel 2025 S2 (non 41 come nella nota 04 [S]).

| Fascia (2025 S2) | Zone | Canone: mediana dei punti medi | Canone min–max | Prezzo: mediana punti medi | Prezzo min–max |
|---|---|---|---|---|---|
| B centrale | 9 | 23,0 | 15,0–35,0 | 7.750 | 5.000–12.000 |
| C semicentrale | 8 | 17,2 | 11,5–24,0 | 5.475 | 4.000–7.100 |
| D periferica | 19 | 12,8 | 9,0–16,9 | 3.550 | 2.700–5.600 |
| E suburbana | 4 | 9,6 | 6,5–14,0 | 2.525 | 1.850–3.500 |
| **Tutte** | 40 | **13,6** | 6,5–35,0 | **3.850** | 1.850–12.000 |

- [I] Mediana *non ponderata* tra zone (nessun peso per stock o compravendite): sovrappesa la periferia (23 zone D/E su 40). Rendimento lordo implicito mediano 4,1%.
- Zona per zona: `omi_milano_2025S2_civili_normale_per_zona.csv`.

**Serie 2015–2025** (`omi_milano_serie_semestrale_civili_normale.csv`, mediana tra zone dei punti medi) [V]:

| Semestre | 2015 S1 | 2019 S2 | 2021 S2 | 2022 S2 | 2023 S2 | 2024 S2 | 2025 S2 |
|---|---|---|---|---|---|---|---|
| Prezzo €/m² | 2.500 | 2.600 | 2.650 | 3.200 | 3.525 | 3.775 | 3.850 |
| Canone €/m²/mese | 8,0 | 8,8 | 8,4 | 10,0 | 11,5 | 12,7 | 13,6 |

- [I] Piatto fino al 2021, poi scatto: canoni +62% in 4 anni (2021 S2→2025 S2), prezzi +45%. Confronto nazionale: indice prezzi abitazioni Italia (Eurostat `prc_hpi_a`, 2015=100) 116,2 nel 2025 [V] → Milano (+54%) cresce circa tre volte l'Italia (+16%).

### 2.2 Prezzi e canoni d'annuncio e rapporti di mercato [S]
Separati dai dati OMI: sono prezzi **richiesti**, non transati, spesso su superficie diversa, e non verificati in questa sessione (riportati dalla nota `04_modelli_economici_abitare.md`).
- Canone medio richiesto Milano **23,3 €/m²/mese** (Idealista, 2025) [S]; **24 €/m²** (Immobiliare.it Insights, +4,3% sul 2023) [S].
- Prezzo medio di vendita ~**5.750 €/m²**, I trim. 2026 (+1,0%) (Abitare Co su dati AdE) [S].
- [I] **Disaccordo**: annunci ≈ 1,7× la mediana OMI dei canoni. Ragioni: OMI su superficie lorda e su tutto lo stock in stato normale; annunci = flusso di offerta nuova, sovrarappresentate zone centrali e alloggi piccoli; nessuna delle due è il canone pagato dagli inquilini in essere. **Nell'analisi uso entrambi come estremi.**
- Non recuperati: Nomisma, Scenari Immobiliari (a pagamento); **compravendite NTN** OMI per Milano e "Statistiche regionali Lombardia" / "Rapporto immobiliare residenziale" (sito AdE raggiungibile ma PDF non estratti per tempo) → lacuna prioritaria.

## 3. Accessibilità per famiglie tipo

### 3.1 Ipotesi [H]
| Famiglia tipo | m² lordi | Percettori | Scala OCSE mod. | Scala ISEE |
|---|---|---|---|---|
| Persona sola < 65 | 45 | 1 (dipendente) | 1,0 | 1,00 |
| Anziano solo | 50 | 1 (pensionato) | 1,0 | 1,00 |
| Coppia senza figli | 60 | 2, entrambi allo stesso percentile | 1,5 | 1,57 |
| Monogenitore + 1 figlio < 14 | 65 | 1 | 1,3 | 1,57 |
| Coppia + 2 figli < 14 | 85 | 2, stesso percentile | 2,1 | 2,46 |

- Reddito: percentile *dei contribuenti milanesi* (§1.1), convertito in netto [H]. Coppie con **due redditi allo stesso percentile** = ipotesi ottimistica (assortative mating perfetto e doppio impiego); una coppia monoreddito è più vicina al caso "monogenitore".
- Assegno Unico per figli: importi 2024 [S] (199,4 €/mese per ISEE ≤ 17.090,61; 57 € per ISEE ≥ 45.574,96), interpolato linearmente; maggiorazioni ignorate.
- ISEE proxy: (redditi lordi − 7.000 € di detrazione affitto) / scala; patrimonio zero [H].
- Canoni: (a) mediana OMI periferia D/E 12,7; (b) mediana OMI città 13,6; (c) mediana OMI fascia C 17,2; (d) Piano Casa 80 €/m²/anno = 6,67/mese; (e) annunci [S] 23,3 €/m²/mese. Spese condominiali e utenze **escluse** (l'RTI vero è più alto).
- Mutuo: LTV 80%, 25 anni, tasso fisso 3,3% [H]. Risparmio per l'anticipo: 10% del netto all'anno [H].
- Paniere non abitativo (Stone, *shelter poverty*): soglia di rischio povertà Italia (Eurostat 2025) × scala OCSE [V/H]. È conservativa per Milano (costo della vita più alto). Variante "75%" del paniere come sensibilità. Le soglie ISTAT di povertà assoluta per Milano non sono state verificate: un sito riporta 1.175,15 €/mese per un adulto 30–59 anni solo in comune centro di area metropolitana lombarda, anno non indicato [S, da riscontrare sul calcolatore ISTAT].

### 3.2 Rapporto canone/reddito netto (RTI) — `accessibilita_famiglie_tipo.csv`
Canone OMI mediano città (13,6 €/m²/mese). **Grassetto = oltre 30%**; † = oltre 40% (soglia Eurostat di *overburden*).

| Famiglia | P20 | P40 | P50 | P60 | P80 |
|---|---|---|---|---|---|
| Persona sola (613 €/mese) | **70%†** | **40%†** | **34%** | 28% | 20% |
| Anziano solo (681 €) | **88%†** | **49%†** | **40%†** | **32%** | 23% |
| Coppia 2 redditi (818 €) | **47%†** | 27% | 23% | 18% | 14% |
| Monogenitore + 1 (886 €) | **82%†** | **52%†** | **44%†** | **37%** | 28% |
| Coppia + 2 figli, 2 redditi (1.158 €) | **54%†** | **34%** | 29% | 24% | 19% |

Con **canoni d'annuncio** [S] (23,3 €/m²) l'RTI si moltiplica ×1,7: persona sola P50 **58%**, P80 35%; anziano solo P50 69%; monogenitore P80 48%; coppia+2 P50 50%, P80 32%; coppia senza figli P60 32%. In fascia semicentrale (OMI C) la persona sola supera il 30% fino al P60 (35%).

Con **Piano Casa 80 €/m²/anno**: tutte le famiglie tipo stanno sotto il 30% dal P40 in su; al P20 persona sola 34%, anziano 43%, monogenitore 40%.

### 3.3 Reddito residuo (shelter poverty), canone OMI città [I]
Famiglie con residuo dopo l'affitto **sotto il paniere** (soglia povertà × scala): **tutte al P20**; al **P40**: persona sola (residuo 10.837 € vs 13.237), anziano solo, monogenitore, coppia + 2 figli (27.277 vs 27.798, al limite); al **P50**: anziano solo (12.106) e monogenitore (13.327 vs 17.208). Dal P60 nessuna. Con la variante 75% del paniere restano shelter-poor al P50 nessuna, al P40 anziano solo e monogenitore.

### 3.4 Acquisto (prezzo OMI mediano città 3.850 €/m²) [I]
- **Price-to-income** (prezzo alloggio / netto annuo familiare): persona sola P50 **8,0**; P80 4,8; coppia + 2 figli P50 6,9; monogenitore P50 10,4; anziano solo P50 9,5.
- **Rata mutuo / netto** (LTV 80%, 25 a., 3,3%): persona sola P50 38%, P60 31%, P80 23%; coppia + 2 figli P50 33%; coppia senza figli P40 30%.
- **Anni per risparmiare il 20% di anticipo** risparmiando il 10% del netto: persona sola P50 16 anni; coppia + 2 figli P50 14; coppia senza figli P50 11. [I] La barriera all'acquisto per il ceto medio è più l'anticipo che la rata.

### 3.5 Soglie di reddito per reggere il mercato al 30% — `soglie_reddito_rti30.csv`
Reddito lordo individuale necessario per percettore e percentile dei contribuenti milanesi corrispondente (AUU escluso, conservativo):

| Famiglia | OMI periferia | OMI città | OMI semicentro | Annunci [S] | Piano Casa 80 | Piano Casa 90 |
|---|---|---|---|---|---|---|
| Persona sola | 27,9k (P52) | 31,0k (P56) | 43,1k (P69) | 63,3k (P85) | 11,7k (P24) | 13,7k (P27) |
| Anziano solo | 34,3k (P60) | 37,5k (P63) | 49,6k (P77) | 71,9k (P88) | 15,6k (P31) | 18,0k (P35) |
| Coppia 2 redditi (per percettore) | 16,2k (P32) | 17,8k (P35) | 24,7k (P48) | 37,5k (P63) | 8,0k (P16) | 8,5k (P18) |
| Monogenitore + 1 | 46,9k (P74) | 51,3k (P79) | 68,5k (P87) | 97,5k (P92) | 19,3k (P38) | 22,6k (P44) |
| Coppia + 2 figli (per percettore) | 26,0k (P50) | 28,4k (P53) | 39,9k (P66) | 59,0k (P84) | 10,8k (P22) | 12,7k (P25) |

## 4. Confronto con gli indicatori ufficiali di overburden [V]
Eurostat EU-SILC (scaricati 10/11/2026; `eurostat_ilc_lvho07*.csv`). *Housing cost overburden rate* = quota di popolazione con costi abitativi totali > 40% del reddito disponibile (al netto dei trasferimenti per la casa). Anno indagine 2025.

| Indicatore | Italia | UE27 |
|---|---|---|
| Totale | **5,0%** | 7,6% |
| Città (DEG1) | 6,7% | 9,5% |
| Sotto soglia di povertà | 21,7% | 29,0% |
| **Inquilini a canone di mercato** | **22,3%** | 18,5% |
| Persona sola | 13,9% | 19,9% |
| Persona sola < 65 | 16,3% | 21,9% |
| Monogenitore con figli | 13,2% | 14,4% |
| Due adulti + 2 figli | 2,7% | 4,4% |

- Quota mediana dei costi abitativi sul reddito (`ilc_mded01`), Italia 2025: totale 14,1%; persona sola 21,8%; sotto soglia di povertà 28,6% [V].
- Non esiste un dato Eurostat per Milano né per la Lombardia (NUTS2) sull'overburden; servono microdati EU-SILC o indagini comunali [I].
- [I] Coerenza: il dato italiano è basso perché ~70% è proprietario; tra gli inquilini a mercato il 22% è in overburden, e il calcolo sopra mostra che a Milano, con canoni OMI, sono in overburden le persone sole fino a ~P40 e i monogenitori fino a ~P50 — compatibile con un tasso molto più alto della media italiana tra gli inquilini milanesi. Ma il confronto è imperfetto: EU-SILC conta i canoni effettivamente pagati (anche vecchi contratti), le mie famiglie tipo pagano il canone di nuovo contratto.

## 5. La "pancia": tra ERP e mercato — `pancia_erp_mercato.csv`
Soglia ERP Lombardia: **ISEE ≤ 16.000 €** (oltre a requisiti di residenza/lavoro e assenza di proprietà adeguate), L.R. 16/2016 e R.R. 4/2017 [V] — Regione Lombardia, https://www.regione.lombardia.it/politiche-sociali-e-abitative/abitare-in-lombardia/servizi-abitativi-pubblici--l-r--16-2016-e-r-r--4-2017 (aperto 10/11/2026). Tradotta in reddito lordo con l'ISEE proxy [H]:

| Famiglia | Soglia ERP (lordo per percettore, percentile) | Soglia mercato OMI città | Ampiezza pancia OMI | Ampiezza pancia annunci [S] |
|---|---|---|---|---|
| Persona sola | 23,0k (P44,5) | P55,7 | **11 pp** | 41 pp |
| Anziano solo | 23,0k (P44,5) | P62,9 | **18 pp** | 44 pp |
| Coppia 2 redditi | 16,1k (P31,4) | P34,7 | **3 pp** | 32 pp |
| Monogenitore + 1 | 32,1k (P57,0) | P78,5 | **21 pp** | 35 pp |
| Coppia + 2 figli | 23,2k (P44,8) | P52,9 | **8 pp** | 39 pp |

**Ordine di grandezza [I/H]**. Applicando ampiezze di ~10–20 pp (OMI) o ~35–44 pp (annunci) alle 780.935 famiglie anagrafiche [V]: **~80–150 mila famiglie "equivalenti" con i canoni OMI, ~270–340 mila con i canoni d'annuncio.** Avvertenze forti:
1. I percentili sono di contribuenti, non di famiglie: la posizione di una famiglia nella distribuzione familiare non coincide [I].
2. La pancia "morde" solo chi è in affitto o deve entrare nel mercato (giovani, nuovi residenti, separati). La quota di famiglie in affitto a Milano **non è stata verificata in questa sessione** (censimento ISTAT da riscontrare): se fosse ~30% [H], la pancia effettiva sarebbe **~25–45 mila famiglie (OMI) o ~80–100 mila (annunci)**.
3. Essere eleggibili ERP non significa avere un alloggio (graduatorie lunghe): anche sotto la soglia molti sono di fatto sul mercato [I].
4. Il target dichiarato del Piano Casa (lavoratori con 1.500–2.500 €/mese, Comune di Milano 9/10/2025 citato da Il Fatto Quotidiano [S]) cade proprio nella pancia: netto 18–30k/anno ≈ P40–P65 dei contribuenti [I].

**Dove la casa smette di essere sostenibile [I]**: con canoni OMI, sotto il ~P55 per i single, ~P63 per gli anziani soli, ~P79 per i monogenitori, ~P53 per le coppie con figli a doppio reddito (~P35 per coppie senza figli a doppio reddito). Con i canoni d'annuncio la soglia sale all'**85°–92° percentile** per chi vive con un solo reddito: il mercato dei nuovi contratti è accessibile solo al quinto superiore dei single milanesi.

## 6. Contesto di policy e costi
- **Piano Casa / Piano straordinario Casa Accessibile**: 10.000 alloggi in 10 anni, tetto 80 €/m²/anno, vincolo ≥ 30 anni [S, nota 04]. **DG 365 del 26/03/2026**: canone medio massimo **90 €/m²/anno**, vincolo almeno 30 anni, diritto di superficie 90 anni, aree a 1 €/m² (ex Palasharp, San Romanello, Bovisasca) [V-secondaria: Assolombarda, https://www.assolombarda.it/servizi/immobili-urbanistica-e-territorio/informazioni/casa-accessibile-nuove-linee-di-indirizzo-del-piano-straordinario-del-comune-di-milano, aperto 10/11/2026; testo della delibera non letto]. Primo bando: una sola area assegnata, 33 alloggi (Il Fatto Quotidiano, 02/11/2025) [S].
- **Edilizia convenzionata, prezzi massimi di cessione a Milano**: **non trovati** in questa sessione (cercati; comune.milano.it risponde 403 a richieste automatiche). Lacuna.
- **ERP**: ISEE ≤ 16.000 € [V]; quota 20% degli alloggi agli indigenti (ISEE ≤ 3.000) [S].
- **Costi di costruzione**: indice Eurostat del costo di costruzione di edifici residenziali, Italia (`sts_copi_a`, 2021=100): 2015 93,1 → 2021 100 → 2022 111,9 → 2023 114,2 [V] (+23% 2015→2023, quasi tutto nel 2022). Valori in €/m² per Milano: solo [S] (Cronoshare 1.500–2.000 €/m² "chiavi in mano", bassa affidabilità). DEI/Collegio Ingegneri e Architetti di Milano *Prezzi tipologie edilizie* e prezzario regionale: non consultati (a pagamento / non raggiunti). [I] Con prezzi OMI periferici ~3.400 €/m² e costo di costruzione ~2.000 €/m² + oneri + spese, il margine per terreno e profitto in periferia è sottile: coerente con il fatto che il nuovo si concentra dove i prezzi sono alti.
- **Oneri di urbanizzazione, Delibera CC 28/2023**: tabelle €/m³ non lette (solo [S], Osborne Clarke, vedi nota 04).

## 7. Lacune e prossimi passi
1. NTN e "Statistiche regionali Lombardia"/"Rapporto immobiliare 2026" (AdE, PDF): scaricare e estrarre compravendite e quotazioni medie per macroarea.
2. Quota di famiglie in affitto a Milano (censimento permanente ISTAT) → indispensabile per stimare la pancia "vera".
3. Distribuzione del reddito **familiare** (EU-SILC Lombardia, Banca d'Italia IBF; ISTAT SDMX non ha risposto): sostituire i percentili dei contribuenti.
4. Testo DG 365/2026 e bandi Piano Casa (requisiti di reddito), prezzi convenzionata, Delibera CC 28/2023: dall'albo pretorio (serve accesso a comune.milano.it).
5. Soglie ISTAT di povertà assoluta 2024 per Milano dal calcolatore ISTAT (paniere Stone più corretto).
6. Ponderare le zone OMI per stock abitativo o compravendite (oggi mediana semplice).

## Fonti aperte/scaricate in questa sessione (10/11/2026)
- MEF, redditi IRPEF comunali 2024 e 2014, subcomunali (CAP) 2024: https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?opendata=yes
- Comune di Milano open data: OMI ds1996, ds3024, ds3025; famiglie ds1442, ds139 — https://dati.comune.milano.it
- Eurostat API: ilc_lvho07a/c/d/e, ilc_mded01, ilc_li01, ilc_di03, nama_10r_2hhinc, prc_hicp_aind, prc_hpi_a, sts_copi_a — https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/
- Regione Lombardia, SAP: pagina citata in §5. Assolombarda su DG 365/2026: pagina citata in §6.
