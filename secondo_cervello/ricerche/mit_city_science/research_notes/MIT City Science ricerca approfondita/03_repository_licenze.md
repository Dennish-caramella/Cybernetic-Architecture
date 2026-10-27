# Repository, licenze e riusabilità di CityScope (MIT City Science)

Data dei controlli: 2026-10-27. Legenda: [V] verificato su pagina/file del repo in questa sessione; [I] inferenza; [H] ipotesi.

**Limiti di metodo (dichiarati).** `git clone`, `codeload`, `raw.githubusercontent.com`, `api.github.com`, `docs.cityscope.media.mit.edu` e la home `cityscope.media.mit.edu` via curl sono bloccati dal proxy (403/404). `gh api` e i tool MCP GitHub (`get_file_contents`, `list_commits`) sono limitati al solo repo di sessione. Funzionano: la ricerca repository del tool MCP GitHub (solo metadati: stelle, linguaggio, `updated_at`, archiviato) e il fetch (con riassunto di modello) delle pagine HTML di github.com, PyPI e `cityscope.media.mit.edu/...`. Quindi: **nessun file di codice è stato letto direttamente; nessun clone**; le pagine sono riassunti di seconda mano. Le date degli ultimi commit **non** sono state ottenute (colonna vuota nel fetch; i feed .atom sono bloccati da robots). `updated_at` dell'API non è la data dell'ultimo commit (molti repo mostrano 2026-08-22/23 in blocco: [I] probabile aggiornamento di massa dell'organizzazione, non attività reale).

## 1. Quali repository esistono

### Takeaway
L'organizzazione GitHub `CityScope` ha 64 repository pubblici [V]. Il nucleo attivo e documentato è: cityscopeJS (front-end), CS_Brix (libreria Python per moduli/indicatori), CS_CityIO (server, Rust), CS_CityScoPy (scanner), CS_Urban_Indicators, CS_Simulation_GAMA. Molti progetti legacy (CityMatrix, CityScopeAR, Unity, Grasbrook) sono archiviati. Convenzione: `CS_*` = strumenti, `CSL_*` = repository per città.

### Cited Findings
Fonte elenco/metadati: ricerca MCP `org:CityScope` (pagine 1-2, 2026-10-27), dati GitHub; pagine per repo come indicato.

| Repo | URL | Licenza | Stelle / fork | Lingua | Stato | Note |
|---|---|---|---|---|---|---|
| cityscope.github.io | https://github.com/CityScope/cityscope.github.io | non indicata [V] | 66 / 14 | JS | attivo (83 commit) | sorgente della documentazione; nessuna licenza dichiarata per i contenuti |
| CS_Simulation_GAMA | https://github.com/CityScope/CS_Simulation_GAMA | GPL-3.0 [V] | 37 / 22 | GAML | 676 commit | modelli GAMA; compatibile GAMA 1.8.1 secondo README |
| CS_cityscopeJS | https://github.com/CityScope/CS_cityscopeJS | GPL-3.0 [V] (file `licence`) | 24 / 20 | JS | 816 commit | front-end web |
| CS_CityScoPy | https://github.com/CityScope/CS_CityScoPy | GPL-3.0 [V] | 16 / 11 | Python | 226 commit | scanner tavolo LEGO -> cityIO |
| CS_CityIO | https://github.com/CityScope/CS_CityIO | non visibile nella pagina [V: nessun LICENSE nell'elenco] | 15 / 10 | Rust (da Cargo.toml, [I]) | 314 commit, branch main | server; README assente nel fetch |
| CS_Brix | https://github.com/CityScope/CS_Brix | GPL-3.0 [V] (PyPI: GPL-3.0-only) | 6 / 4 | Python | 1.218 commit; PyPI ultima release 0.0.10 il 2 giu 2021 | libreria moduli/indicatori |
| CS_Urban_Indicators | https://github.com/CityScope/CS_Urban_Indicators | GPL-3.0 [V] | 9 / 6 | Python | 177 commit | indicatori urbani, Docker |
| CS_Mobility_Service | https://github.com/CityScope/CS_Mobility_Service | GPL-3.0 [V] | 11 / 7 | Jupyter | 200 commit | simulazione mobilità come servizio web |
| CS_Accessibility | https://github.com/CityScope/CS_Accessibility | non indicata [V] | 4 / 2 | Jupyter | 25 commit | accessibilità a piedi/TPL con urbanaccess e pandana |
| CS_cityscopeJS_grid_maker | https://github.com/CityScope/CS_cityscopeJS_grid_maker | non indicata [V] | 2 / 1 | JS | 3 commit | crea griglie, esporta JSON |
| CS_cityscopeJS_Scanner | https://github.com/CityScope/CS_cityscopeJS_Scanner | non controllata | 3 / 4 | JS | metadati soli | scanner nel browser |
| CityMatrix_Sim_AI | https://github.com/CityScope/CityMatrix_Sim_AI | non indicata [V] | 11 / 4 | Jupyter | **archiviato** 7 nov 2019; 254 commit | ABM + ML di CityMatrix |
| CS_AI_Python, CS_CityMatrix_Viz_Unity | https://github.com/CityScope/CS_AI_Python ; .../CS_CityMatrix_Viz_Unity | non controllata | 5 / 6 | Jupyter / C# | archiviati (metadati API) | parti di CityMatrix |
| CS_CityScopeAR | https://github.com/CityScope/CS_CityScopeAR | **AGPL-3.0** [V] | 4 / 2 | JS/Unity | **archiviato** 8 nov 2019; 28 commit | AR/MR |
| CSL_Hamburg_Grasbrook | https://github.com/CityScope/CSL_Hamburg_Grasbrook | non indicata [V] | 5 / 3 | TypeScript (Angular) | **archiviato** 20 dic 2020; 423 commit; cartella `DATA` | front-end progetto Grasbrook |
| CSL_Hamburg_HPA, CSL_Hamburg_Noise | https://github.com/CityScope/CSL_Hamburg_HPA ; .../CSL_Hamburg_Noise | non controllata | 4 / 2-6 | GAML / Python | attivi per metadati | moduli Amburgo |
| CS_Dynamic_Urban_Planning | https://github.com/CityScope/CS_Dynamic_Urban_Planning | non controllata | 5 / 4 | GAML | metadati soli | "joint choice model" casa+mobilità in ABM (descrizione API): potenzialmente rilevante per housing |
| CS_ESG_Community_Metrics, AmenitiesDistribution, CS_NTT_Rome (15-min city), CSL_* varie | vedi `github.com/CityScope` | non controllate | 1-5 | varie | metadati soli | |

- **FindingPlaces:** nessun repository con questo nome nei 64 risultati dell'organizzazione [V: ricerca `org:CityScope`, pagine 1-2]. Il front-end di Amburgo (CSL_Hamburg_Grasbrook) non menziona FindingPlaces nella pagina [V]. Il legame è [H]; il codice FindingPlaces **non risulta pubblicato** sotto questa organizzazione.
- **CS_Scanner** non esiste con questo nome: gli scanner sono CS_CityScoPy (Python) e CS_cityscopeJS_Scanner (browser) [V].
- **CityMatrix:** parti separate e archiviate (Sim_AI, AI_Python, Viz_Unity) [V metadati].
- Documentazione ufficiale: https://cityscope.media.mit.edu/intro/github distingue repo `CS_` (strumenti comuni) e `CSL_` (città, con strumenti come submodule) [V].
- Un'organizzazione correlata (es. MIT Media Lab, Spatial Milano Lab) non è stata censita: fuori da questa passata.

### Inferences
- [I] L'ecosistema è di ricerca, con 2-3 manutentori (PyPI: crisjf, doorleyr per Brix); la pagina PyPI di Brix è ferma al 2021 e il README avverte che la libreria è "in sviluppo".
- [I] 64 repository con poche stelle: comunità piccola, bus factor basso.

### Gaps
- Data dell'ultimo commit per tutti i repo (git/API/atom bloccati).
- Licenze di CS_CityIO, CS_Accessibility, grid_maker, docs, CityMatrix_Sim_AI, Grasbrook (nessun file visibile nel fetch: "nessuna licenza dichiarata" va letto come *non confermata*; in assenza di licenza il copyright resta riservato).
- Lettura diretta del codice e dei file LICENSE.
- Stato di cityscope.media.mit.edu (home) e CityIO API non raggiunto.

## 2. Architettura del protocollo e "funzione di valutazione"

### Takeaway
Il protocollo ruota attorno al server cityIO: una "tabella" è un progetto con GEOGRID (celle e tipi) e GEOGRIDDATA (stato corrente delle celle, aggiornato a ogni modifica). Moduli esterni (Python con Brix) si iscrivono via WebSocket, ricalcolano indicatori a ogni modifica e li restituiscono a cityIO; cityscopeJS li mostra. La "funzione di valutazione" non è centrale: vive in ogni modulo, come codice Python scritto a mano (`return_indicator`). I pesi non sono forniti dal framework.

### Cited Findings
- Sezioni della documentazione: CityScopeJS, Modules, CityIO, Tangible User Interfaces — [docs](https://cityscope.media.mit.edu/intro/github)
- Il canale `/module` di cityIO è un WebSocket: il modulo invia SUBSCRIBE, calcola, risponde; a ogni messaggio di aggiornamento della griglia ricalcola e rimanda — [CityIO Module](https://cityscope.media.mit.edu/cityio/CityIO%20-%20Module)
- Brix: tavolo = progetto; indicatori = risultati calcolati dai dati del tavolo e postati su cityIO; flusso `Handler` -> `add_indicators()` -> `listen()` — [README CS_Brix](https://github.com/CityScope/CS_Brix)
- Un indicatore è una sottoclasse di `Indicator` con `setup()`, `load_module()` (opzionale), `return_indicator(geogrid_data)`; tipi: numeric, heatmap, textual, hybrid; la visualizzazione numerica di default è un radar — [Getting started Brix](https://cityscope.media.mit.edu/CS_Brix/getting_started.html)
- `geogrid_data` è una lista di dizionari, una per cella, con proprietà come `Type` (uso del suolo) e `Height` (piani); ha metodi `as_df()` (pandas), `as_graph()`, `bounds()` — stessa fonte
- La documentazione Brix **non spiega pesi né schema di scoring**: sono "lasciati all'autore"; i valori nell'esempio (0.3, 0.5) sono segnaposto — stessa fonte
- L'esempio di modulo usa valori casuali (`random.random()`) come segnaposto da sostituire — [Module example](https://cityscope.media.mit.edu/modules/brix/Module%20example)
- Gli indicatori "reali" stanno in CS_Urban_Indicators: diversità d'uso del suolo (entropia di Shannon), Innovation Potential, Mobility Impact, Economic Impact, Social Wellbeing, Environmental Impact (nomi nell'output d'esempio); dati: BLS OES 2018, shapefile Census 2019, Zip Code Business Patterns; licenze dei dati non dichiarate nel repo — [CS_Urban_Indicators](https://github.com/CityScope/CS_Urban_Indicators)
- Mobility Service: modelli logit (scelta modale, scheduler di attività, scelta della residenza) che restituiscono CO2, mode split, impatti sanitari — [CS_Mobility_Service](https://github.com/CityScope/CS_Mobility_Service)
- Scanner: CS_CityScoPy legge una griglia LEGO a tag binari e la pubblica su `GEOGRIDDATA` — [CS_CityScoPy](https://github.com/CityScope/CS_CityScoPy)
- grid_maker: strumento web per creare/editare griglie ed esportare JSON — [grid_maker](https://github.com/CityScope/CS_cityscopeJS_grid_maker)
- Indicatori di tipo "simulation" (strati ABM dinamici) non supportati da Brix secondo il README — [CS_Brix docs](https://cityscope.media.mit.edu/CS_Brix)

### Inferences
- [I] La logica di valutazione è codice Python (pandas/geopandas): riscrivere i pesi richiede di modificare uno script, non un file di configurazione. Per non esperti è fattibile solo per modifiche minime (costanti) con supporto; non esiste un editor di pesi nel framework [non trovato].
- [I] Per un tool di screening di lotti il concetto trasferibile è lo schema "stato della griglia -> funzione -> vettore di indicatori -> radar", non il codice.
- [H] Con cityscopeJS si potrebbe mostrare lotti come celle, ma la griglia regolare è ipotesi di progetto poco adatta a lotti catastali irregolari.

### Gaps
- Struttura esatta del JSON GEOGRID/GEOGRIDDATA (pagina Architecture del docs non raggiunta).
- Dove cityscopeJS legge pesi/indicatori nel codice `src/` (non letto).
- Se esistono interfacce di modifica pesi lato front-end.

## 3. Licenze e compatibilità con una tesi

### Takeaway
La maggior parte del codice verificato è GPL-3.0 (cityscopeJS, Brix, CoScoPy, Urban_Indicators, Mobility, GAMA); CityScopeAR è AGPL-3.0. Per una tesi la GPL consente studio, uso e modifica; obblighi di copyleft scattano alla distribuzione di opere derivate. Diversi repo non dichiarano licenza: non riusabili senza permesso.

### Cited Findings
- GPL-3.0 verificato su: cityscopeJS, Brix (anche PyPI "GPL-3.0-only"), CityScoPy, Urban_Indicators, Mobility_Service, Simulation_GAMA — pagine repo sopra; [PyPI cs-brix](https://pypi.org/project/cs-brix)
- AGPL-3.0: CityScopeAR — [repo](https://github.com/CityScope/CS_CityScopeAR)
- Nessuna licenza visibile: CS_CityIO, CS_Accessibility, grid_maker, cityscope.github.io, CityMatrix_Sim_AI, Grasbrook — pagine sopra
- Le fonti dati di Urban_Indicators (BLS, Census, ZBP) non hanno licenza dichiarata nel repo; sono dati federali USA ([I] di norma pubblici, da verificare)
- Cartella `DATA` in Grasbrook: contenuto e licenza non verificati

### Inferences
- [I] Citare e studiare il codice in una tesi è compatibile con la GPL. Redistribuire una versione modificata (es. in un annesso o repo pubblico) impone GPL-3.0 per l'opera derivata. Usare solo le idee/le architetture non impone nulla.
- [I] Dati: licenze separate dal codice; i dati OSM (ODbL) sarebbero usati per Milano, non quelli inclusi nei repo.
- [H] Parere legale non dato; da confermare con l'ufficio dottorato.

### Gaps
- Testo integrale dei LICENSE; licenza dei dati nei repo CSL_* e nelle cartelle `DATA`; licenza dei contenuti della documentazione.

## 4. Cosa è riusabile per lotti a Milano

### Takeaway
Riusabile come metodo: modello a moduli/indicatori, radar di indicatori, GeoDataFrame in/out, accessibilità con pandana/urbanaccess, entropia di uso del suolo, scheda indicatore per lotto. Non riusabile: dati USA, griglia regolare di celle, hardware (scanner/LEGO), pesi e indicatori di innovazione/economia calibrati su Detroit/Cambridge.

### Cited Findings
- Accessibilità a piedi e TPL su una tabella cityIO con pandana/urbanaccess — [CS_Accessibility](https://github.com/CityScope/CS_Accessibility)
- Urban_Indicators include funzioni OSM (`osm_amenity_tools.py`, `osm_amenities.json`) e geofencing — [CS_Urban_Indicators](https://github.com/CityScope/CS_Urban_Indicators)
- Brix lavora con `as_df()` (pandas) e restituisce heatmap come GeoDataFrame — [Getting started](https://cityscope.media.mit.edu/CS_Brix/getting_started.html)
- GAMA contiene modelli "Housing Choice", "Economy" ed "Energy" (senza descrizioni) — [CS_Simulation_GAMA](https://github.com/CityScope/CS_Simulation_GAMA)
- Progetto 15-minute city per Roma con NTT Data — [CS_NTT_Rome](https://github.com/CityScope/CS_NTT_Rome) (solo metadati)

### Inferences
- [I] Riusabili (idee): schema indicatore -> radar; diversità d'uso; accessibilità; scelta residenziale (GAMA, se letti i modelli).
- [I] Non riusabili: tipi LEGO/BinaryCode, dati BLS/Census, ABM calibrati su aree USA, dipendenza da cityIO, stack Rust/WebSocket per un contesto "solo persone, senza sviluppatori".
- [H] Un foglio di calcolo con gli stessi indicatori (per lotto) replica il valore utile senza l'infrastruttura.

### Gaps
- Nessuna analisi del codice (richiesto); qualità e adattabilità dei modelli GAMA non valutate; repository in altre organizzazioni (es. MIT Media Lab, CityScope Hamburg/HCU) non censiti; FindingPlaces non trovato.
