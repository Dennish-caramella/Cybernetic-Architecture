# ISTAT and Italian official open datasets for a socio-economic dashboard of Provincia di Monza e della Brianza (code 108, 55 comuni)

All URLs below were requested by me on 2026-10-25 (curl) and resolved as stated. "CORS" = whether the response carried any `Access-Control-Allow-Origin` header when sent `Origin: https://example.com`. Result: NONE of the ISTAT or MEF endpoints tested sent CORS headers, so a browser-only prototype cannot fetch them directly. Pre-fetch to static JSON/GeoJSON (build step) or proxy.

Sample files saved in `C:\Users\Caredda Dennis\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\scratch-workspaces\a470af2b-033c-43bf-b939-4e491576ce55\1299d199-735c-4baa-abfb-4a387c77fa66\scratch-2026-10-25-2e192b\istat_samples\` (listed at the end).

## 1. Population by comune (residents, age, foreign residents, households)

### Takeaway
Best source is the ISTAT SDMX API (esploradati.istat.it), dataflow `22_289_DF_DCIS_POPRES1_6` (Lombardia, all comuni, by single year of age, 1 Jan 2026 provisional, 2025 definitive) plus `29_7_DF_DCIS_POPSTRRES1_23` (foreign residents, all comuni). Households come from permanent census comune tables (`DF_DCSS_FAM_POP_TV_1`, ref. year 2024). demo.istat.it is an interactive web app with no stable bulk-file URLs found; use SDMX instead.

### Cited Findings
- SDMX catalogue (2.28 MB XML, HTTP 200, no CORS): https://esploradati.istat.it/SDMXWS/rest/dataflow/IT1?detail=allstubs . Dataflow `22_289` "Popolazione residente al 1 gennaio" has sub-flows; `22_289_DF_DCIS_POPRES1_6` = Lombardia, `22_289_DF_DCIS_POPRES1_24` = "Tutti i comuni per singola età". Dimensions of `_6`: FREQ, REF_AREA, DATA_TYPE, SEX, AGE, MARITAL_STATUS. Dataflow LAST_UPDATE annotation: 2026-03-31. — [esploradati catalogue](https://esploradati.istat.it/SDMXWS/rest/dataflow/IT1?detail=allstubs)
- Working CSV call (HTTP 200, `Content-Type: application/vnd.sdmx.data+csv`, no CORS), Monza (108033) and Agrate Brianza (108001) total population: https://esploradati.istat.it/SDMXWS/rest/data/IT1,22_289_DF_DCIS_POPRES1_6,1.0/A.108033+108001.JAN.9.TOTAL.99?lastNObservations=1 with header `Accept: application/vnd.sdmx.data+csv;version=1.0.0`. Returned: 108001 -> 15891 (2026, OBS_STATUS `e`), 108033 -> 123672 (2026, `e`). Without `e` (definitive) Monza 1 Jan 2025 = 123032. Key order: FREQ.REF_AREA.DATA_TYPE.SEX.AGE.MARITAL_STATUS; SEX 9 = total; MARITAL_STATUS 99 = total; AGE codes `TOTAL`, `Y0`..`Y99`, `Y_GE100`. Exact column names: `DATAFLOW,FREQ,REF_AREA,DATA_TYPE,SEX,AGE,MARITAL_STATUS,TIME_PERIOD,OBS_VALUE,OBS_STATUS,NOTE_DS,NOTE_REF_AREA,NOTE_DATA_TYPE,NOTE_SEX,NOTE_AGE,NOTE_MARITAL_STATUS,BASE_PER,UNIT_MEAS,UNIT_MULT` — tested live.
- All ages for one comune (Monza, 2025+2026, 18,389 bytes, HTTP 200): `.../data/IT1,22_289_DF_DCIS_POPRES1_6,1.0/A.108033.JAN.9..99?startPeriod=2025&endPeriod=2025` (empty AGE = wildcard; server returned both 2025 and 2026 rows). Saved as t2.csv.
- Foreign residents 1 Jan, all comuni: dataflow `29_7_DF_DCIS_POPSTRRES1_23`, dims FREQ, REF_AREA, DATA_TYPE, SEX, AGE (5 dims). Query `.../data/IT1,29_7_DF_DCIS_POPSTRRES1_23,1.0/A.108033....?lastNObservations=1` returned Monza TOTAL = 7342 (2026, `e`). Columns: `DATAFLOW,FREQ,REF_AREA,DATA_TYPE,SEX,AGE,TIME_PERIOD,OBS_VALUE,OBS_STATUS,...`; DATA_TYPE=`JAN`, SEX=`1` appeared in first returned rows (note: SEX code semantic not decoded; add explicit `9`/totals filter when building). Saved as t3.csv. Related: `29_317_DF_DCIS_POPSTRCIT1_23` (by citizenship), `29_316_DF_DCIS_POPSTRBIL1_23` (balance), `22_315_DF_DCIS_POPORESBIL1_24` (demographic balance, all comuni) exist in catalogue (not queried).
- Households (permanent census, comuni, ref. year 2024): `DF_DCSS_FAM_POP_TV_1`, dims FREQ, REF_AREA, INDICATOR. Query `.../data/IT1,DF_DCSS_FAM_POP_TV_1,1.0/A.108033.?lastNObservations=1` returned for Monza 2024: RESPOP_AV 123032, POPHH_AV 121739, NPHH_AV 57702 (households), INST_RESPOP_AV 1293 (living in institutions). `DF_DCSS_FAM_POP_TV_2` = average household size; `DF_DCSS_FAMIGLIE_TV_1` households by size; `TV_2/TV_3` households with foreigners. Saved cp_fampop_monza.csv.
- IIS path-segment limit: a key with all 55 codes joined by `+` in one segment returned HTTP 400 "Invalid URL"; splitting into 3 requests (25+25+5 codes) works. Wildcard in REF_AREA returns the whole of Italy (large). — tested.
- Empty-key counting rule: number of dots must equal (number of dimensions - 1); otherwise error text "Not enough key values in query, expecting N got M". — tested.
- Server was slow/intermittent (some requests timed out at 60-90 s then succeeded on retry). — observed.
- demo.istat.it (HTTP 200, 33 KB HTML) is a dynamic app (`app/?i=POS&l=it`, `app/?i=D7B&l=it&a=2026`, `tavole/?t=indicatori&l=it`); pages load jQuery/DataTables; I found no direct CSV/XLSX URLs in the HTML. — [demo.istat.it](https://demo.istat.it/)

### Inferences
- Use `22_289...` for age structure (derive 0-14, 15-64, 65+ and mean age/old-age index client-side from single ages) and `29_7...` for foreign share. 2026 values are provisional (`e`); 2025 is the latest definitive 1 Jan.

### Gaps
- Did not decode the SEX code meaning in the foreign-resident flow (`1` seen); filter explicitly after checking `CL_SEXISTAT1`.
- Did not find stable bulk-file URLs on demo.istat.it.

## 2. Census 2021 / permanent census at comune and census-section level

### Takeaway
Two layers exist: (a) section-level 2021 indicators (population, age, education, employment 15-64, foreigners, households, dwellings, residential buildings) in one regional XLSX per region, and section polygons (Lombardia `R03_21.zip`); (b) comune-level permanent-census tables via SDMX with reference year 2024 (employment status, education, dwellings). Section data have no unemployment rate; unemployment rate must come from the comune SDMX table.

### Cited Findings
- ISTAT page "Basi territoriali e variabili censuarie" (HTTP 200 after redirect from /it/archivio/104317): https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/ . It states ISTAT publishes definitive 2021 permanent-census variables per section, and that the permanent census is based on registers plus annual sample surveys. — [ISTAT](https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/)
- Section indicators 2021, all regions (zip, 254,534,430 bytes, HTTP 200, `Accept-Ranges: bytes`, Last-Modified 2025-04-04, no CORS): https://esploradati.istat.it/databrowser/DWL/PERMPOP/SUBCOM/Dati_regionali_2021.zip . Contents: `R01..R20_indicatori_2021_sezioni.xlsx` + `TRACCIATO FILE REGIONALI.xlsx`. Lombardia = `R03_indicatori_2021_sezioni.xlsx` (37,633,662 bytes unzipped; sheet `R03`; 67,724 section rows for Lombardia). I extracted R03 and the layout via HTTP Range requests (no need for full 254 MB).
- Exact columns (header row of R03): `CODREG, REGIONE, CODPRO, PROVINCIA, CODCOM, COMUNE, PROCOM, SEZ21_ID, COM_ASC1, COM_ASC2, COM_ASC3, P1, P2, P3, P14..P29 (age classes <5 ... >74), P30..P45 (males by age), P67..P82 (females by age), P83..P85 (9+ pop), P86 (no title), P87 (elementare), P88 (media), P89 (diploma secondaria superiore incl. qualifiche), P90 (terziario), P91..P100 (same by sex), P101 (occupati 15-64 totale), P102, P103, IT1..IT12 (Italians by age 0-14/15-64/65+, sex, occupati), ST1..ST33 (stranieri: ST1 total, ST16 UE, ST19 extra-UE, ST22-24 by age, ST31 occupati), PF1 (famiglie), PF3..PF8 (1..6+ components), A2 (abitazioni occupate da residenti), A3 (abitazioni vuote/non residenti), A8 (abitazioni totali), E3 (edifici residenziali)`. Definitions: TRACCIATO sheet `TRACCIATO_2021`.
- Province 108 sample (first 3 of 40 saved rows): `CODREG=3, CODPRO=108, PROVINCIA="Monza e della Brianza", CODCOM=001, COMUNE="Agrate Brianza", PROCOM=108001, SEZ21_ID=1080010000001, P1=610, P89=228, P90=60, P101=305, ST1=45, PF1=255, A8=325, E3=84`. Filter province 108 with `PROCOM` starting `108` (or `CODPRO=108`). Saved: `censimento2021_sezioni_prov108_sample.csv`.
- Section geometries 2021: Lombardia https://www.istat.it/storage/cartografia/basi_territoriali/2021/R03_21.zip (HTTP 200, 61,888,278 bytes, Last-Modified 2026-02-27, no CORS); attribute classification `ASG_21.zip` (222,916 bytes); also `Localita_21.zip`, `Sezioni_21-kmz.zip`, `Limiti_21-kmz.zip`. I did not unzip R03_21.zip, so CRS/field names for sections are NOT verified. Earlier basi territoriali editions (1991/2001/2011, `.../WGS_84_UTM/2011/R03_11_WGS84.zip`) are in WGS84 UTM per file path naming. — [ISTAT page links](https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/)
- Older census variables per section also on that page, e.g. https://www.istat.it/storage/cartografia/variabili-censuarie/dati-cpa_2011.zip (HTTP 200, 52,442,848 bytes). `dati-cpa_2021.zip` returns 404 (does not exist).
- Comune-level permanent-census tables via SDMX (reference year 2024; HTTP 200; no CORS):
  - Employment status 15+: `DF_DCSS_ISTR_LAV_PEN_2_TV_3`, dims FREQ.REF_AREA.INDICATOR.GENDER.AGE_NOCLASS.CITIZENSHIP.EDU_ATTAIN.CUR_ACT_STAT.LOC_DEST.REAS_COMMUTING. Query `.../data/IT1,DF_DCSS_ISTR_LAV_PEN_2_TV_3,1.0/A.108033........?lastNObservations=1` (136 lines). Monza 2024, T, Y_GE15, TOTAL: CUR_ACT_STAT 99 (total) = 108247; 1 (occupato) = 57514; 12 (in cerca di occupazione) = 3488.28; 22 (forze di lavoro) = 61002.28; 23 (non forze di lavoro) = 47244.72. Labels confirmed from codelist `CL_FORZE_LAV` (1 occupato, 12 in cerca, 22 forze di lavoro, 23 non forze di lavoro, 99 totale). Values are fractional (weighted estimates). Derived: employment rate 15+ = 53.1%, unemployment rate = 5.7% (my arithmetic: 57514/108247, 3488.28/61002.28). Saved cp_tv3_monza.csv.
  - Education 9+: `DF_DCSS_ISTR_LAV_PEN_2_TV_1` (same 10 dims). Monza 2024, T, Y_GE9: ALL=114745 (total), codes BL, IL, LBNA, LSE, ML, ML_RDD, NED, PSE, RDD, USE_IF returned; values e.g. USE_IF 44186, LSE 24588, ML_RDD 23548. Label mapping of these education codes NOT decoded (codelist `CL_TITOLO_STUDIO` returned numeric placeholders). Saved cp_istruzione_monza.csv.
  - Dwellings: `DF_DCSS_ABITAZIONI_TV_1` (9 dims). Monza 2023: NUM_DW_AV 63700, NUM_OCC_DW_AV 56617, NUM_UNOCC_DW_AV 7083. Saved cp_abitazioni_monza.csv. Note reference year 2023 here vs 2024 for the other tables.
  - Bulk full-dataset zips are attached to dataflow annotations, e.g. `https://esploradati.istat.it/databrowser/DWL/PERMPOP/MUN/DCSS_ISTR_LAV_PEN_2 - Istruzione, lavoro e spostamenti per studio o lavoro - intero ds.csv.zip` (URL text copied from the DCSS_BULK_ISTR_LAV_PEN_2 annotation; NOT downloaded/verified).

### Inferences
- For first prototype use comune-level SDMX tables for rates (employment, unemployment, education) and the section XLSX only if a section-level choropleth is wanted. Section file `P101/P83` is not a standard employment rate (15-64 occupati over 9+ population), so don't mix definitions.
- Sections are numerous: 67,724 for Lombardia; provincial subset likely a few thousand (not counted by me).

### Gaps
- R03_21.zip contents/CRS not inspected; education code labels (BL, IL, LBNA, LSE, ML, ML_RDD, NED, PSE, RDD, USE_IF) not decoded.
- Bulk CSV zip URL for comune tables not tested.

## 3. Economy: firms/employees (ASIA) and income (MEF)

### Takeaway
ASIA local units and employees per comune are available on SDMX (ref. year 2024) in dataflow `183_1163_DF_DICA_ASIAULP_TERRIFDATA_3`; all 55 comuni verified. ISTAT does not publish comune-level income; MEF Dipartimento Finanze publishes IRPEF by comune (tax year 2024) as free CSV.

### Cited Findings
- ASIA unità locali e addetti, comuni, Ateco 3 digits: dataflow `183_1163_DF_DICA_ASIAULP_TERRIFDATA_3` (also `_7` = Ateco 2 digits by size class, `_1` = principal data returned NoRecordsFound for comune key). Dims FREQ.REF_AREA.DATA_TYPE.ECON_ACTIVITY_NACE_2007.PERS_EMPL_SIZE_CLASS. Working query (3 calls of 25/25/5 codes): `https://esploradati.istat.it/SDMXWS/rest/data/IT1,183_1163_DF_DICA_ASIAULP_TERRIFDATA_3,1.0/A.108001+108002+...+108025..0010.TOTAL?lastNObservations=1` (HTTP 200, 5.5 KB each, no CORS). Result: 111 lines = 55 comuni x 2 data types, TIME_PERIOD 2024. Columns: `DATAFLOW,FREQ,REF_AREA,DATA_TYPE,ECON_ACTIVITY_NACE_2007,PERS_EMPL_SIZE_CLASS,TIME_PERIOD,OBS_VALUE,OBS_STATUS,NOTE_DS,NOTE_REF_AREA,NOTE_DATA_TYPE,...`. Rows: `108001,LU,0010,TOTAL,2024,1644` (local units) and `108001,LUEMPDAA,0010,TOTAL,2024,15268.8` (employees, annual average; label inferred from code name). Monza LU total (earlier query) = 15074. Saved `asia_prov108_total.csv` (all 55 comuni). ECON code `0010` returned as total row (interpretation: all sectors). It counts unità locali, not imprese.
- A newer-looking older flow `183_285_DF_DICA_ASIAULP_3` also exists in catalogue (older edition; not queried).
- MEF Dipartimento delle Finanze, "Open data comunale - principali variabili IRPEF": page https://www.finanze.gov.it/it/statistiche-fiscali/open-data-comunale-principali-variabili-irpef/ (redirects to https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?search_class%5B0%5D=cCOMUNE&opendata=yes ; HTTP 200). Files tax years 2000-2024 per comune and (selected years 2011, 2015, 2019-2024) sub-comunale, CSV and RDF.
- Download (tested HTTP 200, 1,028,668 bytes zip, Last-Modified 2026-04-23, no CORS, no login): https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip?d=1615465800 . Contains one CSV (2,313,404 bytes), `;`-delimited, latin-1 encoded, 7,897 rows nationwide, 53 columns; 55 rows with `Codice Istat Comune` starting `108`. Key columns: `Anno di imposta; Codice catastale; Codice Istat Comune; Denominazione Comune; Sigla Provincia; Regione; Codice Istat Regione; Numero contribuenti; ... Reddito imponibile - Ammontare in euro; ... Reddito complessivo - Frequenza; Reddito complessivo - Ammontare in euro; Reddito complessivo minore o uguale a zero euro; ... da 0 a 10000; 10000-15000; 15000-26000; 26000-55000; 55000-75000; 75000-120000; oltre 120000 (each Frequenza/Ammontare)`. Sample row: `2024;F704;108033;MONZA;MB;Lombardia;03;94782`. Saved subset `mef/irpef2024_comunale_provincia108.csv`. Mean income per taxpayer = `Reddito complessivo - Ammontare` / `Reddito complessivo - Frequenza` (my derivation; compute after loading).
- MEF page links the licence http://creativecommons.org/licenses/by/3.0/it/ (CC BY 3.0 IT). — [MEF open data page](https://www.finanze.gov.it/it/statistiche-fiscali/open-data-comunale-principali-variabili-irpef/)
- MEF notes: data refer to declarations filed in 2025 for tax year 2024, and are subject to revision. — [MEF dichiarazioni](https://www1.finanze.gov.it/finanze/pagina_dichiarazioni/public/dichiarazioni.php) (search-result summary; page fetched HTTP 200)
- Definition of variables PDF: https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti/definizione_variabili_2024_irpef.pdf (appeared in search result, not fetched by me).

### Inferences
- "Reddito per contribuente" is by place of tax residence and covers declarants only (excludes non-filers); comparable year-to-year but not equal to per-capita income.

### Gaps
- Confirmed no comune-level income dataset found in ISTAT catalogue; I did not exhaustively prove absence, only searched dataflow names.
- Did not decode ASIA `LUEMPDAA` label via codelist; did not check ECON `0010` label.

## 4. ISTAT SDMX REST API: working queries and CSV

### Takeaway
Base `https://esploradati.istat.it/SDMXWS/rest`. Data endpoint returns CSV when sent `Accept: application/vnd.sdmx.data+csv;version=1.0.0`. No CORS, GET only.

### Cited Findings
- Pattern: `/data/IT1,{dataflowId},1.0/{key}?lastNObservations=1` (key dimension order = DSD order, `+` OR, empty = wildcard, dot count = dims-1). Structure: `/dataflow/IT1/{id}/latest?references=descendants` (≈10 MB XML each) gives dimensions and codelists. — tested
- Verified working URLs (all HTTP 200): (a) population: https://esploradati.istat.it/SDMXWS/rest/data/IT1,22_289_DF_DCIS_POPRES1_6,1.0/A.108033+108001.JAN.9.TOTAL.99?lastNObservations=1 ; (b) foreigners: https://esploradati.istat.it/SDMXWS/rest/data/IT1,29_7_DF_DCIS_POPSTRRES1_23,1.0/A.108033....?lastNObservations=1 ; (c) ASIA: see section 3; (d) census employment: see section 2.
- `&format=csv` query parameter was sent but I did not confirm it changes output; Accept header worked.
- Preflight: `OPTIONS` returns `405 Method Not Allowed`, `Allow: GET`, server `Microsoft-IIS/10.0`, `X-Powered-By: ASP.NET`; no `Access-Control-*` headers on GET either. — tested
- Request reliability: single requests occasionally exceed 60-120 s; use retries and cache outputs.
- Province code for REF_AREA: the SDMX flows above use 6-digit comune code (108xxx, same as PROCOM / MEF Codice Istat Comune / boundary `PRO_COM_T`), so one join key everywhere. Province-level NUTS3 code `ITC4D` was not tested.

### Gaps
- No filter-by-province shortcut found: need explicit comune list (3 chunks) or filter client-side after wildcard download.

## 5. Administrative boundaries (confini amministrativi, generalised)

### Takeaway
Use ISTAT `Limiti01012026_g.zip` (generalised, 1 Jan 2026), CRS WGS 84 / UTM zone 32N (EPSG:32632), reproject to EPSG:4326 for web. 55 comuni in province 108 verified.

### Cited Findings
- https://www.istat.it/storage/cartografia/confini_amministrativi/generalizzati/2026/Limiti01012026_g.zip — HTTP 200, 10,450,609 bytes, Last-Modified 2026-03-06, no CORS. Contains folders `Reg01012026_g`, `RipGeo01012026_g`, `ProvCM01012026_g`, `Com01012026_g` (each `*_WGS84.shp/.shx/.dbf/.prj`; Com .shp 12,730,288 bytes). Previous years also exist at `.../generalizzati/2025/Limiti01012025_g.zip`, 2024, 2023, 2022 (links on the ISTAT archive page). — [ISTAT page](https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/) lists these; 2026 URL tested.
- `.prj`: `PROJCS["WGS_1984_UTM_Zone_32N",... PROJECTION["Transverse_Mercator"], False_Easting 500000 ...` — read from the zip.
- Comune DBF has 7,896 records; fields: `OBJECTID, COD_RIP, COD_REG, COD_PROV, COD_CM, COD_UTS, PRO_COM, PRO_COM_T, COMUNE, COMUNE_A, CC_UTS, Shape_Leng, Shape_Le_1, Shape_Area`. Filter `COD_PROV=108` gives exactly 55 comuni, `PRO_COM_T` 108001..108055. Sample: `PRO_COM=108001, COMUNE=Agrate Brianza, Shape_Area=1.10073011012e+07` (m²). Attributes saved to `confini2026/com_attrs_prov108.json`.
- Non-generalised (detailed) versions exist under `.../confini_amministrativi/non_generalizzati/` (older years seen in page links; I did not test the 2026 non-generalised URL).

### Inferences
- OSM vs ISTAT (no source consulted, general knowledge, unverified here): ISTAT boundaries follow cadastral/administrative limits at a given date, are generalised (smoother, smaller files), and carry the official ISTAT codes that join to all datasets above; OSM boundaries are community-maintained relations that may differ slightly and lack ISTAT codes unless tagged (`ref:ISTAT`). For a data dashboard use ISTAT polygons so join keys and totals match.
- Conversion: `ogr2ogr -t_srs EPSG:4326 -where "COD_PROV=108" out.geojson Com01012026_g_WGS84.shp` then simplify (e.g. mapshaper) for web.

### Gaps
- Did not measure file size of the 55-comune GeoJSON; did not verify OSM comparison with a source.

## 6. Licence and attribution wording

### Takeaway
ISTAT site content is CC BY 4.0. MEF open data cites CC BY 3.0 IT. Attribution must name the source, link the licence, and flag modifications.

### Cited Findings
- ISTAT "Note legali": "Salvo diversa indicazione, tutti i contenuti pubblicati su questo sito sono soggetti alla licenza Creative Commons - Attribuzione - versione 4.0"; conditions: adequate credit, link to licence, indicate if changes were made, no suggestion of endorsement. — [ISTAT note legali](https://www.istat.it/note-legali/)
- MEF page links CC BY 3.0 IT. — [MEF](https://www.finanze.gov.it/it/statistiche-fiscali/open-data-comunale-principali-variabili-irpef/)

### Inferences
- Suggested footer (my wording): "Fonte: Istat (popolazione residente 2026, Censimento permanente 2021/2024, ASIA 2024, confini amministrativi 1.1.2026), licenza CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/deed.it); Ministero dell'Economia e delle Finanze - Dipartimento delle Finanze (redditi IRPEF, anno d'imposta 2024), licenza CC BY 3.0 IT (https://creativecommons.org/licenses/by/3.0/it/). Elaborazione dell'autore: dati aggregati/derivati, modifiche apportate." Do not imply ISTAT/MEF endorsement.

### Gaps
- Not verified whether specific dataflows (esploradati) override with different licence statements; no per-dataset licence field found.
- Regione Lombardia open data (dati.lombardia.it), dati.gov.it not examined.

## 7. Recommendation: minimal indicator set per comune (first prototype)

### Takeaway
Seven indicators from three sources, all joinable on 6-digit code 108001-108055, prefetched into one static JSON plus one GeoJSON.

### Cited Findings (all verified above)
| # | Indicator | Source / ref. year | Granularity |
|---|---|---|---|
| 1 | Resident population | SDMX `22_289_DF_DCIS_POPRES1_6`, 1 Jan 2026 (prov.) / 2025 (def.) | comune |
| 2 | Age structure (0-14, 15-64, 65+ share, old-age index) | same, single years | comune |
| 3 | Foreign residents share | SDMX `29_7_DF_DCIS_POPSTRRES1_23`, 1 Jan 2026 | comune |
| 4 | Employment rate and unemployment rate | SDMX `DF_DCSS_ISTR_LAV_PEN_2_TV_3`, 2024 (CUR_ACT_STAT 1, 12, 22, 99) | comune |
| 5 | Local units and employees | SDMX ASIA `..._TERRIFDATA_3`, 2024 (LU, LUEMPDAA) | comune |
| 6 | Mean taxable income per taxpayer | MEF IRPEF CSV, tax year 2024 | comune |
| 7 | Households / avg size, dwellings | SDMX `DF_DCSS_FAM_POP_TV_1` (2024), `DF_DCSS_ABITAZIONI_TV_1` (2023) | comune |
- Optional second step: education (section file P86-P90 aggregated or SDMX TV_1 after decoding codes), section-level map from R03 xlsx + R03_21 shapes.

### Inferences
- Because no endpoint sends CORS headers, do all fetching in a build script (Node/Python), emit `data/comuni.json` (~55 records) and `comuni.geojson`; no runtime calls to ISTAT/MEF from the browser. Mixed reference years (2023-2026) must be labelled per indicator in the UI.

### Gaps
- Not checked: Regione Lombardia open data, dati.gov.it catalogue entries, or INPS/other labour datasets.

## Files saved (istat_samples)
Base: `C:\Users\Caredda Dennis\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\scratch-workspaces\a470af2b-033c-43bf-b939-4e491576ce55\1299d199-735c-4baa-abfb-4a387c77fa66\scratch-2026-10-25-2e192b\istat_samples\`
- `t2.csv` (Monza single-age population 2025/2026), `t3.csv` (foreign residents Monza)
- `asia_prov108_total.csv` (ASIA LU and LUEMPDAA, 55 comuni, 2024)
- `cp_tv3_monza.csv`, `cp_istruzione_monza.csv`, `cp_fampop_monza.csv`, `cp_abitazioni_monza.csv` (permanent census, Monza)
- `censimento2021_sezioni_prov108_sample.csv` (40 section rows), `census_dl\R03_indicatori_2021_sezioni.xlsx`, `census_dl\TRACCIATO FILE REGIONALI.xlsx`
- `mef\irpef2024.zip`, `mef\irpef2024_comunale_provincia108.csv` (55 rows), `mef\h.txt` (headers)
- `confini2026\Limiti01012026_g.zip`, `confini2026\com_attrs_prov108.json`
- `h1.txt` (SDMX response headers)
