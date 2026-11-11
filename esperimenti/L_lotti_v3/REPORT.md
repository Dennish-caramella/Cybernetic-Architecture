# Report di laboratorio — Base L v3: ambiti di trasformazione prevalenti e terreni comunali confermati

Ticket: [Base L v3](https://github.com/Dennish-caramella/Cybernetic-Architecture/issues/35). Esecutore: agente dati-geo-milano (con urbanista-pgt-milano). Report assemblato dal coordinatore con il testo dell'esecutore (i sub-agenti non possono creare file di report).

## 1. Pre-registrazione
Testo integrale in `esecuzioni/00_preregistrazione.txt` (13:09Z dell'11/11/2026, hash `39e4c160…` in `00_preregistrazione.sha256`, commit `907e0ed` alle 13:18Z), prima di ogni esecuzione. Criteri C1–C8 come in v2, stesse soglie, seme 3511. Conflitto dichiarato prima: gli ambiti di trasformazione (AT) entrano anche se oggi in uso (D1), mentre C5 misura "libero o dismesso oggi".

## 2. Dati e fonti
Fonti di v1 e v2 dalla cache (catasto WFS CC BY 4.0, DBT 2020 CC BY 2.5 IT, DUSAF 8.0, mosaico PGT regionale licenza [L], NIL ds964, ds503, Demanio ds2688/2689, ds677, ds600, ds2813) [V]. Mosaico PGT: 30 AT di cui 6 PCU. `pgt_dism`: CONTAMINAZ sempre "Da verificare"; nessuna fonte aperta dice se una bonifica è risolta [L], quindi la bonifica è segnalata ma non esclude. Ortofoto AGEA 2018–2019 (Regione Lombardia ImageServer), licenza di sola visione [S], immagini non versionate. Corretto un errore ereditato da v2: il campo bonifica PGT è `DBONIFICA`, non `BONIFICA` (in v2 la quota di bonifica PGT era sempre 0).

## 3. Metodo
Regole di v2 più le sole modifiche v3: particelle AT (quota ≥ 0,5 di un AT non PCU) senza filtri DUSAF di uso attuale, salvo acque e filtri di piano; ds677 solo con quota ≥ 0,5 dei codici DUSAF {131, 132, 133, 134, 1412}; ds503 solo se diruto DBT o screening Q1 = D / tetto T2–T3. Filtro "residenza occupata" valido anche negli AT [H]. Screening ds503 cieco su 111 candidati (seme 3513, hash `e92d4f2d…`), confermati 31. Campione C5 cieco (C001–C200, hash `d4211b46…` prima dell'unione); cecità parziale (codificatore = esecutore; 4 lotti già visti nello screening: senza di essi C5a = 0,573). Registro completo in `esecuzioni/registro.txt`.

## 4. Risultati

| Classe | n | ha | FAR 0,5 | FAR 1 | FAR 2 | recupero |
|---|---|---|---|---|---|---|
| lotto edificabile | 245 | 548,8 | 23.888 | 47.898 | 95.913 | — |
| lotto da riusare | 171 | 68,5 | 2.904 | 5.903 | 11.899 | 2.973 |
| area di attivazione | 258 | 182,4 | 0 | 0 | 0 | — |

Edificabili per origine: AT 88 (323 ha), DUSAF 133/134 114, terreno comunale confermato 38, ex AMB_DEG 4, Demanio 1. Riuso: 130 diruti DBT, 26 ds503 confermati, 15 entrambi; scenario principale 134 demolizione e ricostruzione, 37 recupero. Proprietà ignota: 173/245 edificabili, 154/171 da riusare. 72 NIL su 88.

Copertura degli ambiti (ha coperti / totali, `tabelle/copertura_ambiti.csv`): Farini-Lugano 43,6/62,9; Lambrate 6,2/7,1; Rogoredo 1,9/2,1; Greco-Breda 5,7/7,2; San Cristoforo 15,4/17,2; Porta Genova 8,9/10,9; Romana 21,1/21,7; Piazza d'Armi 54,6/61,8; Porto di Mare 26,2/35,9. Totale AT non PCU 0,78 (358,3 ha su 455,9).

| # | Esito | Valore |
|---|---|---|
| C1–C4, C6 | passano | geometrie, attributi, 0 sovrapposizioni, capacità, conteggi |
| C5a ortofoto, 100 lotti | **non passa** | 0,58 [0,482; 0,672], soglia 0,70 |
| C5b differenza con la base | passa | base 0,11 [0,063; 0,186]; differenza 0,47 [0,346; 0,573] |
| C7 controllo di Dennis | in attesa | `controllo_umano/` |
| C8 riproducibilità | passa | hash `4f41a0af…` in tre esecuzioni |

C5 per origine: AT 0,29 (binari, stazioni, capannoni e uffici in uso); DUSAF 13 0,54; terreno comunale confermato 0,83 (v2: 0,11); diruti DBT 0,60; ds503 confermati 3/4. Senza AT: 0,64 [I]. Recuperabilità del riuso [H, screening visivo]: alta 7, media 10, bassa 4.

## 5. Esito
**Cambia.** C5a 0,58 sotto 0,70 (v2: 0,34); C5b passa con ampio margine. La base non si congela; decide Dennis.

## 6. Limiti
Conflitto dichiarato AT/C5; scarto temporale delle fonti (ortofoto 2018–2019, DUSAF 2024, ds503 2014–2017); codificatore = esecutore; regola R3 che trasforma intere particelle ferroviarie in lotti da riusare per un solo edificio diruto (es. R00047, Farini, 9,9 ha); mancano dati aperti su occupazione, proprietà ERP/ALER, stato delle bonifiche, indici reali del PGT, licenza e aderenza del mosaico PGT [L]; resa 0,70 e 80 m²/alloggio [H].

## 7. Revisione indipendente
_Da scrivere: accordo con il secondo codificatore cieco e revisore-metodologico._

## 8. Cosa passa
Nulla come base congelata. Proposte [H] per Dennis: (1) come C5 tratta gli AT — valutarli con lo stato attuativo del piano letto sui documenti, oppure una categoria Q1 "in trasformazione di piano" (nuova pre-registrazione); (2) ortofoto più recente per DUSAF 13; (3) perimetro dei lotti da riusare nelle grandi particelle ferroviarie limitato a un intorno dell'edificio; (4) attendere l'accordo con il secondo codificatore e C7. Riutilizzabili: pipeline, registro, schema di codifica, screening ds503, tabella di copertura.
