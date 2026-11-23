# Revisione indipendente: banco di laboratorio (ticket #17)

Revisore: `revisore-metodologico`. Non ho costruito il banco e non ne difendo i risultati. Data: 2026-11-23. Questo testo è la §7 di `REPORT.md`.

Letti: `PROTOCOLLO_LABORATORIO.md`, `CONTEXT.md`, `tesi/DECISIONI.md` (09/11 e 23/11), `banco/` (REPORT, PIANO, README, build.py, lotti.js, banco.css, test_banco.cjs), `L_lotti_v7/VERSIONE.md` e `REPORT.md`, `E_economia_v2/VERSIONE.md`, `REPORT.md` e `run.py` (funzione `compute`), `secondo_cervello/ricerche/06_riesame_spatial_milano_lab.md`.

## 7.1 Riproduzione
- [V] `build.py` rieseguito in una copia nello scratchpad (copiate `banco/`, `L_lotti_v7/`, `E_economia_v2/` e la cartella del Lab). Gli otto SHA-256 d'ingresso coincidono; i tre del Lab coincidono anche con `INVENTARIO_SCRATCH.txt` (righe 109, 110, 112). `banco.html` rifatto: 1.607.920 byte, SHA-256 `bfa8ad964610a64dd3bd3a7e055ab00bba7d6e2903678fb12d5dfe37768b2c8d`, identico a quello nel repo.
- [V] `test_banco.cjs` (Playwright, Chrome di sistema): nessun FALLISCE, tutte le righe PASSA, a 1280 e 400 px, nei due temi e a rete bloccata. Il conteggio di 97 controlli torna con la struttura del test [I].
- [V] Nessuna immagine AGEA o Sentinel: 0 tag `<img>`, 0 `data:image` in `banco.html`; "AGEA" compare solo nel testo "Nessuna immagine AGEA". In `archivio/` ci sono solo due icone di Leaflet (26 e 52 px, grigie).
- [V] Cartella 2,7 MB; pagina 1,6 MB (B7 rispettato).

## 7.2 Fedeltà ai dati: 10 lotti a campione
Campione estratto con seme 17 (3 E, 3 R, 2 A, 2 G) [H]: E00349, E00191, E00326, R00127, R00062, R00093, A00505, A00487, G00672, G00683. Ho confrontato i dati incorporati in `banco.html` (oggetto `BL`) con `lotti_v7.gpkg` su 11 campi (classe, superficie, cap_far05/1/2, cap_recupero, cap_scen_far1, ambito, gruppo, stato, proprietà, NIL) e con `delta_L_lotti.csv.gz` per la Base E (acquisto, 60 anni, c0 = 90, VF = 0, FAR 1 o R1).
- [V] 0 differenze sui campi della Base L. Superficie arrotondata al m² = area della geometria in EPSG:32632 (scarto massimo 0,05 m² su tutti i 701). Formule di capacità verificate: E00349 ⌊0,70·14.489/80⌋ = 126; recupero = ⌊0,70·volume/3,2/80⌋ come in `L_lotti_v7/run.py` r. 589.
- [V] Base E: canone di pareggio con suolo a mercato (5% / mediana / 95%) identico in tutti i 9 casi E/R del campione; le quantili sono calcolate sulla regione tarata (`w = masks["cal"]`, `E_economia_v2/run.py` r. 205, 231), come dice la scheda. Unica differenza: quota 0,0005 mostrata come 0,001 (arrotondamento di Python contro numpy); irrilevante.
- [V] Le GFU del campione non hanno Base E per lotto (corretto: E7 e decisione di non mostrare la Base E per GFU); le aree di attivazione non hanno capacità.
- [V] Totali: 216 / 167 / 268 / 50; edificabili 16.389 / 32.885 / 65.885; da riusare 672 / 1.429 / 2.938, recupero 2.898; scenari GFU (ii) e (iii) uguali a `scenari_capacita.csv` e marcati "base + GFU". Canone di pareggio e quote di cessione (0,173; S0 0,786 → S3 0,106; bandi deserti 0) coincidono con `c_star_per_regione.csv` e con REPORT E v2 §4–5.
- [V] Avvertenze: le quattro sono presenti, chiare e fedeli alle fonti (fascia C5 0,65–0,75 e 0,737: PREREG del controllo umano r. 20–22; "quote non probabilità", η senza fonte, non vincolo: VERSIONE E v2).

## 7.3 Esclusioni (decisione del 09/11)
- [V] Dashboard `city`, `lab`, `pp` rimosse da `D`; scenari della demo e nomi delle fasi ridotti a 10 (ultima: "Base L v7: lotti"); strumenti della chat `show_buildings`, `get_lab_audit`, `get_portfolio`, `get_site` filtrati. Nella chat in demo, "portafogli e SMAA" porta ai lotti, "potere d'acquisto" a Stipendi e affitti.
- [V] Ma il codice del Lab resta nella pagina (definizioni `pp_*`, `d_tau`, `d_dec`, `d_ist`, `MLAB`, `renderLab`, `fetch("data/lab.json")`), e gli indicatori del modello di domanda restano raggiungibili dalla chat con Claude: vedi difetto D1.

## 7.4 Difetti

### Gravi
Nessuno. Nessun difetto falsa i dati delle basi mostrati nel pannello dei lotti, nessuna risorsa esterna oltre Google Fonts, build riproducibile. La regola di arresto non scatta.

### Da correggere (prima di usarlo per mostrare le analisi)
**D1. Il modello di domanda escluso è raggiungibile dalla chat con Claude e restituisce un falso zero.** Prova [V]: `rules()` elenca ai modelli `pp_resb`, `pp_res`, `pp_neg`, `pp_rti`, `d_tau`, `d_dec`, `d_ist` con dashboard `[undefined]`; `get_ranking({indicator:"d_tau"})` restituisce `city_value: 0` con la descrizione del modello ("media di 20 scenari bootstrap"). Una risposta "Domanda D_tau a Milano: 0 famiglie" sarebbe un numero inventato da un modello escluso. Vale solo se la capacità `sample` è disponibile (REPORT §6: oggi risponde in demo) [I]. Correzione: in `build.py` cancellare da `M` le chiavi del gruppo `pp` (come già si fa per `D`), e aggiungere al test un controllo che `IND_LIST` non contenga "undefined" e che `get_ranking` rifiuti quegli id.

**D2. "701 lotti" conta come lotti le aree di attivazione e le GFU.** Prova [V]: KPI "lotti visibili su 701", testo per la chat "701 lotti in quattro classi", REPORT §4. `CONTEXT.md`: l'area di attivazione non va chiamata lotto; il lotto GFU "sta fuori dai totali dei lotti". Correzione: "383 lotti (216 edificabili, 167 da riusare) + 268 aree di attivazione + 50 lotti GFU non verificati"; KPI "elementi visibili su 701" o separato per classe.

**D3. Stato attuativo errato per 11 lotti in ambito.** Prova [V]: 11 poligoni con `gruppo_ambito` (ADP 4, PA 6, GFU 1) e `stato_riferimento` vuoto; la scheda scrive "non censito (fuori dagli ambiti)", in contraddizione con la riga "Ambito PGT 2030" della stessa scheda (es. E00205, Ronchetto GFU). Correzione: "non censito" senza la causa, oppure "in ambito, non censito" quando `gruppo_ambito` è presente.

**D4. Marca e fonte della superficie sbagliate.** Prova [V]: la scheda scrive "Superficie … [V] catasto" per ogni lotto; l'area è quella della geometria della base (`Lt.area`, `L_lotti_v7/run.py` r. 481), dopo unioni e ritagli con DUSAF, DBT, PGT; per E00205 l'origine è DUSAF13. Anche "Origine … [V] <fonti>" ripete per tutti la stessa lista di 11 fonti (527 lotti identici), che non è la fonte del singolo lotto. Correzione: "[V] Base L v7, area della geometria (EPSG:32632)"; elenco delle fonti come "fonti della base", non come verifica del lotto. La legenda ridefinisce [V] ("letto da file"), diverso dal protocollo ("verificato in questa sessione"): dirlo esplicitamente.

**D5. Mancano in pagina due limiti della Base L che toccano i numeri mostrati.** Prova [V]: VERSIONE L v7 indica validazione debole per AdP (0,49) e riuso (0,55–0,59) e nessuna maschera dei corpi idrici; la scheda di E00170 mostra 203 / 407 / 814 alloggi senza nota, mentre il REPORT L v7 r. 60 dice "lago su oltre metà". Correzione: una quinta avvertenza sull'affidabilità per classe (riuso e AdP deboli); nota nella scheda dei lotti con problemi noti (almeno E00170).

**D6. Indicatori del Lab ereditati con un artefatto noto, senza avvertenza.** Prova [V]: la dashboard "Stipendi e affitti" mostra redditi MEF per CAP riportati ai NIL; il valore 40,57% di contribuenti sotto 15 mila compare 5 volte nei dati dei NIL, ed è il caso Stephenson (172 abitanti) che `06_riesame_spatial_milano_lab.md` §3.5 chiama "artefatto di dato (CAP imputato)". "Affitto / stipendio" usa un solo reddito (dichiarato nella fonte). Non sono basi congelate ma stanno accanto ad esse. Correzione: avvertenza nella dashboard ("valori per CAP, non per NIL; NIL piccoli copiano il CAP") o soglia di popolazione dichiarata; non usarli per A1–A4.

**D7. Accessibilità minima non raggiunta nel tema chiaro.** Prova [V, calcolo WCAG]: contrasto dei colori di classe sul fondo chiaro `#eef1f3`/`#f3f4f6` 1,9–2,7:1 (soglia 3:1 per oggetti grafici, 1.4.11); il testo dell'etichetta di classe nella scheda (colore di classe su `#e3e7eb`) 1,7–2,4:1 (soglia 4,5:1, 1.4.3). Tema scuro: 5,7–10:1, regge. I poligoni dei lotti non sono raggiungibili da tastiera (0 `tabindex`, nessun `role`): l'unica via è "Cerca id", che richiede di conoscere l'id; nessuna regione `aria-live` per la scheda. Buono: `lang="it"`, tutti i pulsanti e i campi hanno un nome, `aria-pressed` sui filtri, `prefers-reduced-motion` del Lab. Correzione: colori di classe più scuri nel tema chiaro (o etichetta in testo neutro con pallino colorato); elenco dei lotti filtrati navigabile da tastiera; `aria-live="polite"` su `#lsch`.

### Minori
- M1. "In nessuna regione 90 €/m²/anno bastano con suolo gratuito a 60 anni": vero per le mediane e per il 5° percentile del nuovo (96,8 / 102,0 / 140,4), ma F-a dice "nel 98% della regione tarata"; e per il recupero R1 il 5° percentile tarato è 72,8. Aggiungere "(nuovo; nel 98% della regione tarata)".
- M2. Quote con tre decimali (0,173; 0,786; 0,001) suggeriscono una precisione che le basi non hanno; il REPORT E usa due decimali. Usare due decimali o "≈ 0".
- M3. Due annate OMI nella stessa pagina: Lab OMI 2024/2 su zone 2021, Base E OMI 2025/2. Dirlo nel riquadro delle fonti.
- M4. Licenze: per lotto la stringa è identica per tutti (unione di CC BY 4.0, 2.5 IT, 3.0 IT, CC0, "PGT regionale [L]"); nel riquadro "Fonti" mancano le licenze di DUSAF, PGT, OMI, DBT e il nome ODbL per OSM (attribuzione "© OpenStreetMap contributors" presente). Non ho verificato le licenze sui siti dei titolari [L]. Aggiungere un elenco fonte → licenza.
- M5. Google Fonts caricati da server esterni: trasmettono l'IP del visitatore [I]; per un uso pubblico incorporare i font o usare quelli di sistema.
- M6. "[L] [L] censimento" (marca ripetuta perché il valore contiene già "[L]"); "censimento, fonte V / ufficiale" poco leggibile; la scheda mostra "A" senza "attuazione avviata".
- M7. Il test non controlla la fedeltà per lotto (solo conteggi e totali) né gli strumenti della chat: aggiungere un confronto di 10 lotti con il gpkg (come in 7.2) e il controllo di D1.
- M8. Procedura: il banco è stato pubblicato come artifact (versione 5) prima della revisione; il REPORT §2 non porta le marche richieste dal protocollo.

## 7.5 Esito proposto
**Passa, con correzioni.** Il banco riproduce in modo deterministico le basi L v7 ed E v2, senza difetti gravi e senza numeri delle basi più forti delle basi stesse nel pannello dei lotti (capacità sempre come forbice, GFU fuori dai totali e "non verificato", quote come quote della regione dei parametri). Prima di usarlo per mostrare le analisi A1–A4 e B0–B6 vanno corretti D1–D7; M1–M8 quando si tocca il codice.

Non verificato: apertura nel visualizzatore degli artifact e chat con Claude reale (provata solo la funzione degli strumenti); lettore di schermo; licenze sui siti dei titolari; lotti oltre il campione, E00205 ed E00170.
