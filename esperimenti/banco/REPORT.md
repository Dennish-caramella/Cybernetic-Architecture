# Report di laboratorio — Banco di laboratorio (ticket #17)

Stato: **pubblicato come artifact privato** (https://claude.ai/artifact/3wjxMbZiHpkLvCsBMfHRAs, versione 5); revisione indipendente: §7. Report assemblato dal coordinatore.

## 1. Ipotesi e soglia
Il banco non è una prova con ipotesi: è lo strumento che mostra le basi. Criteri di accettazione scritti in `PIANO.md` prima del codice (B0–B9): hash e totali coerenti con le basi congelate; nessuna risorsa esterna bloccata dal visualizzatore; 701 lotti per classe; NIL e strati del Lab presenti; dashboard dei modelli di analisi escluse; zero errori JS, 400 px, tema chiaro e scuro; nessuna capacità per attivazione e GFU; pagina < 5 MB; avvertenze in pagina; zoom (B9).

## 2. Dati e fonti
Pagina dello Spatial Milano Lab (`prove/in_evidenza/2026-10-25_spatial_milano_lab/lab_completo/prototype/site/spatial-milano-lab.html`, DUSAF e PGT, hash contro `INVENTARIO_SCRATCH.txt`); Base L v7 (`lotti_v7.gpkg`, `scenari_capacita.csv`, SHA-256 contro `VERSIONE.md`); Base E v2 congelata (tre tabelle, SHA-256 contro `VERSIONE.md`). Nessuna immagine AGEA.

## 3. Metodo
`build.py` prende la pagina del Lab e fa sostituzioni puntuali (si ferma se una non è univoca o un hash non coincide); `lotti.js` aggiunge lo strato dei lotti, le schede, i filtri, la Base E v2, le avvertenze e lo zoom (sul meccanismo di viewBox del Lab); geometrie semplificate a 1 m nel sistema di coordinate del Lab. Prima versione con Leaflet e OpenStreetMap scartata (contro la decisione del 09/11 e bloccata dal visualizzatore): in `archivio/`.

## 4. Risultati
`test_banco.cjs` (Playwright): 97 controlli su 97 a 1280 e 400 px, tema chiaro e scuro, e con rete bloccata; 701 lotti (216 / 167 / 268 / 50); 88 NIL; totali edificabili 16.389 / 32.885 / 65.885; pagina 1,6 MB; build deterministica (SHA-256 `bfa8ad96…`). Riusati dal Lab: mappa dei NIL, globo, fasi, chat (in modalità dimostrativa), dashboard di popolazione, densità, stipendi e affitti, verde e calore, metro, edificato DBT per NIL, DUSAF, PGT. Esclusi: modelli di analisi (siti candidati, SMAA, portafogli, potere d'acquisto e domanda) per la decisione del 09/11; edifici 3D per quartiere (tasselli DBT solo sul PC [L]).

## 5. Esito
Criteri B0–B9 soddisfatti nel test automatico. Da confermare con la revisione e con l'uso di Dennis.

## 6. Limiti
Apertura nel visualizzatore simulata a rete bloccata, non provata dal vero; pinch provato solo con eventi simulati; a 400 px il pannello copre gran parte della mappa; la chat del Lab chiede la capacità `sample` (interrogare Claude), non dichiarata: risponde in demo; hash di contenuto della Base L non riproducibile dal gpkg (vale lo SHA-256 del file); limiti ereditati dalla Base L (schegge geometriche, nessuna maschera dei corpi idrici) e dalla Base E (non vincolo).

## 7. Revisione indipendente
(da scrivere dal `revisore-metodologico`)

## 8. Cosa passa alla prova successiva
Il banco è lo strumento su cui mostrare i risultati di A1–A4 e B0–B6: ogni analisi aggiunge uno strato o una dashboard con lo stesso meccanismo (`build.py` + `lotti.js`), con hash dei file d'ingresso controllati.
