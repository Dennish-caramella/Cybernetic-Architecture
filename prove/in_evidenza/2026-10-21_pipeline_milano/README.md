# Pipeline Milano (Fase 1, senza LLM)

Piattaforma che ricostruisce Milano su una griglia esagonale H3, ci attacca i dati, li analizza con PCA e K-Means,
calcola un'idoneità multicriterio con pesi modificabili e individua lotti candidati per il social housing.
Mostra tutto in un viewer 2D/3D che si apre con un doppio clic.

**Stato al 2026-10-21: il codice è scritto e collaudato, ma NON è mai stato eseguito su dati reali.**
La sessione che l'ha scritto non poteva raggiungere i portali dei dati (OpenStreetMap, Comune di Milano,
Agenzia delle Entrate, ISTAT: connessioni rifiutate dalla rete). Collaudo fatto con dati SINTETICI (`tests/make_fixture.py`):
verificano che il codice giri e che i calcoli siano corretti, non dicono nulla su Milano.

## Cosa fa, in ordine

1. **Griglia**: celle H3 (risoluzione 9 di default, circa 0,10 km²) ritagliate al confine di Milano.
2. **Ingestione**: OpenStreetMap in automatico (confine, rete pedonale, servizi, edifici, aree dismesse, aree protette);
   fonti ufficiali da `data_raw/` (popolazione, OMI, PGT, vincoli). Gli attributi dei poligoni sorgente passano alle celle
   per sovrapposizione areale (conteggi ripartiti per area, medie pesate per area e popolazione).
3. **Indicatori per cella**: densità di popolazione, reddito, quota anziani, canone e prezzo OMI, divario rispetto al canone
   obiettivo, tempi a piedi ai servizi (7 categorie), PAI, densità edificata, quota trasformabile.
4. **PCA + K-Means**: standardizzazione robusta (log, winsorizzazione), 3 componenti con caricamenti e varianza spiegata;
   K scelto con silhouette tra 2 e 8 (o forzato), con Davies-Bouldin, Calinski-Harabasz e stabilità bootstrap (ARI).
   **I cluster non hanno etichette**: li descrive il profilo medio e i tratti distintivi. L'interpretazione è tua.
5. **Idoneità (WLC)**: 4 criteri normalizzati (bisogno, accessibilità, trasformabilità, fattibilità), vincoli booleani,
   4 scenari di pesi, analisi di sensibilità (1000 perturbazioni Dirichlet dei pesi), frontiera di Pareto sui 4 criteri.
6. **Lotti candidati**: poligoni dismessi (PGT se presente, altrimenti OSM) con area minima, valutati con gli stessi criteri,
   accessibilità calcolata dal lotto, robustezza ai pesi, graduatoria per scenario.
7. **Esportazione**: GeoJSON, CSV, report JSON, manifest con provenienza e avvisi, `viewer/data.js`.

## Come eseguirla sul tuo computer

```
cd 05_Urbanistica/pipeline_milano
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tests/test_pipeline.py            # 6 test sui calcoli
python tests/make_fixture.py             # dati SINTETICI di collaudo
python run_pipeline.py --fixture         # prova completa sui sintetici (pochi secondi)
# poi apri viewer/index.html?test        # nel browser
```

Per Milano reale:

1. `python tools/discover_opendata.py --base <URL del portale open data> "NIL" "PGT" "edifici" "popolazione"`
   per trovare i dataset (script non testato). Scarica i file in `data_raw/` nei nomi indicati in `config/sources.yaml`.
2. Apri ogni file, guarda i nomi delle colonne, e compila i `col:` in `config/sources.yaml`. **Non indovinare**:
   un attributo con `col: null` viene saltato e il manifest lo segnala.
3. Imposta in `config/pipeline.yaml` il canone obiettivo da una fonte verificata e discuti i parametri marcati `[PARAMETRO]`.
4. `python run_pipeline.py` (la prima volta scarica OSM: può richiedere diversi minuti e molta memoria per la rete pedonale).
5. Apri `viewer/index.html`.
6. `python run_pipeline.py --sensibilita` confronta i risultati tra risoluzioni H3 (8, 9, 10).

## Dati che servono (da verificare tutti, nessuno è stato scaricato)

| Dato | Fonte prevista | Nota |
|---|---|---|
| Confine, rete pedonale, servizi, edifici, aree dismesse | OpenStreetMap (automatico) | completezza dei tag a Milano non nota |
| Popolazione, famiglie, over 65, reddito | Comune di Milano (NIL) o ISTAT (sezioni) | il reddito potrebbe non esistere a questa scala |
| Quotazioni affitto e vendita | Agenzia delle Entrate OMI | intervalli stimati, non transazioni |
| Ambiti del PGT e lotti dismessi | Comune di Milano | verificare nomi e perimetri |
| Vincoli idraulici | Regione / Autorità di bacino / Comune | scenario e tempo di ritorno da scegliere |
| Aree protette | Regione / Comune | in mancanza si usa OSM, fonte non ufficiale |

## Limiti noti (leggili prima di citare qualunque risultato)

- **Nessun risultato reale esiste ancora.** Cluster, classifiche e lotti mostrati nel viewer di collaudo sono sintetici.
- **PAI** è la somma pesata delle categorie raggiunte entro soglia (0–1). Non è un 2SFCA: servono capacità dei servizi.
- **Velocità pedonale** costante (4,5 km/h): Milano è pianeggiante, nessuna correzione di pendenza. Il tempo è su rete OSM
  dal centroide della cella (celle ritagliate al confine) o del lotto.
- **Cella H3 di livello 9 non è un lotto** (circa 10 ettari): la scelta dei lotti usa poligoni, non celle. Le celle descrivono il contorno.
- **MAUP**: la griglia esagonale elimina l'effetto dei confini amministrativi ma non il problema dell'unità di analisi.
  L'interpolazione areale assume distribuzione uniforme nei poligoni sorgente. Usa `--sensibilita`.
- **Lotti candidati sono ipotesi**: nessun controllo su proprietà, bonifiche, indici reali, vincoli, disponibilità. Il tag
  OSM `landuse=railway/industrial` include aree attive.
- **Quota di costo del suolo** è proxy dal prezzo OMI di zona (non dal valore del lotto). Nessun bilancio finanziario è calcolato:
  costi di costruzione, oneri e sussidiazione incrociata non sono modellati qui.
- **K-Means**: la silhouette tende a K piccoli (spesso 2). Valuta K maggiori guardando interpretabilità e stabilità.
- **Frontiera di Pareto** su 4 criteri contiene in genere una quota ampia delle celle: non è una graduatoria.
- **Vincoli**: se un dato di vincolo manca, il vincolo non è applicato e il viewer lo segnala.
- **Pesi**: sono parametri, non risultati. I preset sono punti di partenza. Nel viewer si cambiano a mano.

## Struttura

```
config/pipeline.yaml    parametri ([PARAMETRO] = scelta tua)
config/sources.yaml     registro fonti e adattatori di colonne (da compilare)
milano_pipeline/        moduli: grid, interpolate, osm_fetch, accessibility, features, clustering, suitability, lots, build, export
run_pipeline.py         esecuzione
tools/discover_opendata.py   ricerca dataset sui portali CKAN (non testato)
tests/                  test di calcolo e generatore di dati sintetici
viewer/index.html       piattaforma (nessuna dipendenza esterna, funziona offline)
viewer/data_test.js     dati sintetici di collaudo
data_raw/               qui vanno i file scaricati
data_output/            risultati reali (CSV, GeoJSON, report, manifest)
```
