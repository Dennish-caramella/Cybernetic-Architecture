# Report di laboratorio — Base E v2 (ticket #19)

Stato: **candidata; revisione: passa con correzioni al REPORT** (fatte qui, V1–V5). E1–E4 passano, E5 non applicabile (errore di taratura non misurato), E6: 110 celle robuste su 135, E7 applicato. Scelte H1–H19 provvisorie del coordinatore: congelamento = decisione di Dennis dopo la revisione (§7). Report assemblato dal coordinatore dalla consegna dell'agente `economista-abitativo`.

## 1. Ipotesi e soglia
`esecuzioni/00_preregistrazione.txt` (SHA-256 `01d50363…`, commit 34c09dc, prima di ogni esecuzione), in risposta alla revisione della v1 (`../E_economia/REVISIONE.md`). Non cieca sui risultati della v1 (dichiarato nella §0). Formulazioni F-a…F-f del REPORT fissate prima.

## 2. Dati e fonti
Come v1 (OMI 2025/2, Base L v7, hash verificati); in più aspettative d'inflazione BCE (SPF), tassi MIR Italia, listino CCIAA Como-Lecco [V]. **Esiti dei bandi DG 365 [S, stampa]**: tre compendi senza offerte a giugno e agosto 2026 (Il Foglio, 05/09/2026); due offerte a ottobre, nessuna aggiudicazione né corrispettivo (Il Giorno, 28/10/2026). K1 resta vincolo di segno; si riporta accanto la regione compatibile con i bandi deserti.

## 3. Metodo
Motore v1 con modifiche [v2]: lato cooperativa e operatore Piano Casa in termini reali (inflazione 2%), vincolo r ≥ 0,5 punti con quattro strati, premio del nuovo nel cubo (0–40%), tre scenari di valore finale, imposte sul suolo in acquisto, due letture di K1, bonifica al valore atteso. E6 per cella (3 classi × 3 durate × 5 canoni × 3 regimi). Analisi in sospeso della v1 eseguite (PRCC, quantili, tornado, proprietà, variante senza ERS, bonifiche, flusso di cassa del developer). Seme 4519, 20.000 punti.

## 4. Risultati
- **Taratura**: 18.982 punti con r ≥ 0,5; regione tarata 10.912; regione dei bandi deserti 9.419.
- **Canone di pareggio con suolo gratuito a 60 anni** (mediana, 5–95%, €/m²/anno), tre regioni con lo stesso peso (regola 1.12):
  | Regione | c* a 60 anni |
  |---|---|
  | tarata (K1) | 130 (97–162) |
  | cubo non tarato | 148 (102–212) |
  | compatibile con i bandi deserti [S] (lettura prudente) | 172 (140–226) |
  Nella regione tarata: 198 (153–243) a 30 anni, 108 (78–137) a 90 anni; con IVA 10% 138 a 60 anni; con η = 0,70 154. **In nessuna regione 90 €/m²/anno bastano.**
- **Canone di pareggio con suolo a mercato** (60 anni, VF0 / VF suolo / VF edificio): B 305/226/230; C 204/171/157; D 154/144/120; E 132/131/104.
- **Valore residuo del developer** (FAR 1, €/m² di SL): B 4.235, C 1.810, D 601, E −212; il flusso di cassa scontato conferma l'ordine di grandezza.
- **Cooperativa a 90 €/m²/anno**:
  - acquisto, 60 anni (B/C/D): quota ≈ 0 (≤ 0,005);
  - cessione, 60 anni: 0,02;
  - cessione, 90 anni: 0,17 nella regione tarata; per strato di r da 0,79 (r − g più basso) a 0,11; **0 nella regione dei bandi deserti**; con bonifica 200 €/m² 0,11.
- **Lotti da riusare**: recupero in cessione a 90 anni 0,46; per classi di ρ a 60 anni 0,51 (ρ < 0,8) e 0,01 (ρ > 1,0), a 90 anni 0,86 / 0,40 / 0,12: **quota del recupero non robusta**; demolizione 0,13–0,16.
- **Sensibilità** (PRCC sulla cessione): costo di costruzione 0,94, manutenzione δ 0,86, η −0,82, tassi 0,71–0,72.

## 5. Esito
E1 (hash `024ac9ea…` in 4 ripetizioni), E2 (T1–T12), E3 (tautologico, dichiarato), E4 passano; E5 non applicabile; E6 110/135 celle robuste (le 25 non robuste a canone ≥ 110 o a 90 anni); E7: acquisto in fascia E "non informativo". **Formulazioni ammesse**:
- **F-a** (fasce B, C, D; con VF nullo e VF del suolo; vincolo r ≥ 0,5): a 90 €/m²/anno e 60 anni la cooperativa non paga il suolo di mercato in oltre il 99% della regione tarata. Vera ma quasi vuota: la cooperativa non regge **nemmeno con suolo gratuito** nel 98% della regione tarata (V4).
- **F-b non ammessa**: la cessione a 90 anni non è robusta (η ne rovescia il segno); si può riportare solo "quota 0,17, dipende da η (0,07–0,24 per terzi di η); da 0,79 a 0,11 per strato di r". Lo 0 nella regione dei bandi deserti segue quasi per costruzione dal modello: è un'implicazione, non un'evidenza (V5).
- **F-c**: canone di pareggio con suolo gratuito e sue forbici.
- **F-d**: il Piano Casa sta in pari in parte per costruzione; i bandi deserti [S] indicano che nemmeno l'operatore misto è in pari con sicurezza.
- **F-e, F-f**: le quote sono quote della regione dei parametri, non probabilità; errore di taratura non misurato; la Base E non è un vincolo di fattibilità in B0–B6.

### Aggiunte richieste dalla revisione (condizioni 2–3, registro voci 12–13; hash di contenuto invariato)
- `tabelle/c_star_per_regione.csv`: c* (€/m²/anno, mediana e 5–95%) per tre regioni. Nuovo: 30 anni 198 / 223 / 255; 60 anni 130 / 148 / 172; 90 anni 108 / 124 / 147 (tarata / cubo / bandi deserti). Recupero: 60 anni 111 / 128 / 152; 90 anni 93 / 108 / 130. Solo per il nuovo a 90 anni nella regione tarata il 5% inferiore scende sotto 90.
- `tabelle/E6_fuori_elenco.csv` (informativa): 102 celle su 135 robuste anche fuori dall'elenco (costo di costruzione, ρ, posizione del prezzo nell'intervallo OMI). Le celle di F-a restano robuste; F-b resta non robusta.

## 6. Limiti
K1 è un vincolo di segno contraddetto in parte dai bandi deserti [S]; ramo developer non tarato su compravendite; π_new, η e il vincolo su r scelti conoscendo la v1; lato cooperativa senza geografia; oneri [S]; un solo listino per ρ e costi; tassi CDP/BEI non trovati.

## 7. Revisione indipendente
Testo completo in `REVISIONE.md`. **Esito proposto: passa**, con correzioni al REPORT (fatte: V1 tre regioni per c*, V3 durate del recupero, V4 F-a quasi vuota, V5 bandi deserti come implicazione). Motore riprodotto (hash `024ac9ea…` identico; E00173 e E00182 ricalcolati a mano; controllo indipendente delle quote e di c*).
- Da correggere ancora (non fatali): V2 E7 passa solo grazie al premio del nuovo, scelto conoscendo la v1 (senza premio il rapporto con l'asta è 0,20); V6 η decide e non ha fonte; V7 manca la variante opposta per η, i_E e premio; V8 E6 robusto solo rispetto all'elenco: costo di costruzione e ρ, fuori elenco, ribaltano celle "robuste".
- Condizioni per congelare: c* per regione prodotto dallo script; colonna E6 "robusta anche fuori elenco"; conferma di Dennis su H1–H19 (decidono gli esiti H11 tassi, H14 premio, H15 η, H17 lettura di K1); `VERSIONE.md`.
- Raccomandazioni: congelare la v2 dopo le correzioni (v3 solo se cambiano H11, H14 o H15); riportare le tre regioni con quella dei bandi deserti come lettura prudente; non usare la Base E come vincolo per lotto in B0–B6; rifare K1 quando ci sarà un'aggiudicazione con corrispettivo da fonte istituzionale.

## 8. Cosa passa alla prova successiva
Canone di pareggio per durata e scenario di valore finale, con forbici; acquisto solo per le fasce B, C, D; cessione solo come quota con strati di r e regione dei bandi deserti; nessun conteggio di lotti; nessun uso come vincolo in B0–B6.

Lettura per la tesi [I]: con i costi di Milano un canone di 90 €/m²/anno non copre i costi di una cooperativa a costo nemmeno con suolo gratuito su 60 anni: il canone di pareggio è tra circa 130 (regione tarata) e 172 €/m²/anno (lettura prudente, bandi deserti), mai sotto 90. Il divario si chiude solo con durate molto lunghe, costi di costruzione o manutenzione bassi, o contributi esterni; il valore preciso dipende da η, senza fonte.
