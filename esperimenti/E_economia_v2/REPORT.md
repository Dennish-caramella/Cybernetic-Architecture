# Report di laboratorio — Base E v2 (ticket #19)

Stato: **candidata**. E1–E4 passano, E5 non applicabile (errore di taratura non misurato), E6: 110 celle robuste su 135, E7 applicato. Scelte H1–H19 provvisorie del coordinatore: congelamento = decisione di Dennis dopo la revisione (§7). Report assemblato dal coordinatore dalla consegna dell'agente `economista-abitativo`.

## 1. Ipotesi e soglia
`esecuzioni/00_preregistrazione.txt` (SHA-256 `01d50363…`, commit 34c09dc, prima di ogni esecuzione), in risposta alla revisione della v1 (`../E_economia/REVISIONE.md`). Non cieca sui risultati della v1 (dichiarato nella §0). Formulazioni F-a…F-f del REPORT fissate prima.

## 2. Dati e fonti
Come v1 (OMI 2025/2, Base L v7, hash verificati); in più aspettative d'inflazione BCE (SPF), tassi MIR Italia, listino CCIAA Como-Lecco [V]. **Esiti dei bandi DG 365 [S, stampa]**: tre compendi senza offerte a giugno e agosto 2026 (Il Foglio, 05/09/2026); due offerte a ottobre, nessuna aggiudicazione né corrispettivo (Il Giorno, 28/10/2026). K1 resta vincolo di segno; si riporta accanto la regione compatibile con i bandi deserti.

## 3. Metodo
Motore v1 con modifiche [v2]: lato cooperativa e operatore Piano Casa in termini reali (inflazione 2%), vincolo r ≥ 0,5 punti con quattro strati, premio del nuovo nel cubo (0–40%), tre scenari di valore finale, imposte sul suolo in acquisto, due letture di K1, bonifica al valore atteso. E6 per cella (3 classi × 3 durate × 5 canoni × 3 regimi). Analisi in sospeso della v1 eseguite (PRCC, quantili, tornado, proprietà, variante senza ERS, bonifiche, flusso di cassa del developer). Seme 4519, 20.000 punti.

## 4. Risultati
- **Taratura**: 18.982 punti con r ≥ 0,5; regione tarata 10.912; regione dei bandi deserti 9.419.
- **Canone di pareggio con suolo gratuito** (mediana, 5–95%): 198 (153–243) €/m²/anno a 30 anni; **130 (97–162) a 60 anni**; 108 (78–137) a 90 anni. Con IVA 10%: 138 a 60 anni; con η = 0,70: 154.
- **Canone di pareggio con suolo a mercato** (60 anni, VF0 / VF suolo / VF edificio): B 305/226/230; C 204/171/157; D 154/144/120; E 132/131/104.
- **Valore residuo del developer** (FAR 1, €/m² di SL): B 4.235, C 1.810, D 601, E −212; il flusso di cassa scontato conferma l'ordine di grandezza.
- **Cooperativa a 90 €/m²/anno**:
  - acquisto, 60 anni (B/C/D): quota ≈ 0 (≤ 0,005);
  - cessione, 60 anni: 0,02;
  - cessione, 90 anni: 0,17 nella regione tarata; per strato di r da 0,79 (r − g più basso) a 0,11; **0 nella regione dei bandi deserti**; con bonifica 200 €/m² 0,11.
- **Lotti da riusare**: recupero in cessione a 90 anni 0,46; con ρ < 0,8 circa 0,51, con ρ > 1,0 circa 0,01; demolizione 0,13–0,16.
- **Sensibilità** (PRCC sulla cessione): costo di costruzione 0,94, manutenzione δ 0,86, η −0,82, tassi 0,71–0,72.

## 5. Esito
E1 (hash `024ac9ea…` in 4 ripetizioni), E2 (T1–T12), E3 (tautologico, dichiarato), E4 passano; E5 non applicabile; E6 110/135 celle robuste (le 25 non robuste a canone ≥ 110 o a 90 anni); E7: acquisto in fascia E "non informativo". **Formulazioni ammesse**:
- **F-a** (fasce B, C, D): a 90 €/m²/anno e 60 anni la cooperativa non paga il suolo di mercato in oltre il 99% della regione tarata.
- **F-b non ammessa**: la cessione a 90 anni non è robusta (η ne rovescia il segno); si può riportare solo "quota 0,17, dipende da η; da 0,79 a 0,11 per strato di r; 0 nella regione dei bandi deserti".
- **F-c**: canone di pareggio con suolo gratuito e sue forbici.
- **F-d**: il Piano Casa sta in pari in parte per costruzione; i bandi deserti [S] indicano che nemmeno l'operatore misto è in pari con sicurezza.
- **F-e, F-f**: le quote sono quote della regione dei parametri, non probabilità; errore di taratura non misurato; la Base E non è un vincolo di fattibilità in B0–B6.

## 6. Limiti
K1 è un vincolo di segno contraddetto in parte dai bandi deserti [S]; ramo developer non tarato su compravendite; π_new, η e il vincolo su r scelti conoscendo la v1; lato cooperativa senza geografia; oneri [S]; un solo listino per ρ e costi; tassi CDP/BEI non trovati.

## 7. Revisione indipendente
(da scrivere dal `revisore-metodologico`)

## 8. Cosa passa alla prova successiva
Canone di pareggio per durata e scenario di valore finale, con forbici; acquisto solo per le fasce B, C, D; cessione solo come quota con strati di r e regione dei bandi deserti; nessun conteggio di lotti; nessun uso come vincolo in B0–B6.

Lettura per la tesi [I]: con i costi di Milano, un canone di 90 €/m²/anno non copre i costi di una cooperativa a costo nemmeno con suolo gratuito su 60 anni (pareggio ≈ 130); il divario si chiude solo con durate molto lunghe, costi o manutenzione bassi, o sussidi esterni.
