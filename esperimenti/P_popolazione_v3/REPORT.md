# Report di laboratorio — Base P v3 (ticket #18)

Stato: **P1, P2, P3, P5 passano; P4 non aperto, in attesa di Dennis.** Report assemblato dal coordinatore.

## 1. Ipotesi e soglia
`esecuzioni/00_preregistrazione.txt` (SHA-256 `a2561ce8…`, commit 7eeb306, prima di ogni esecuzione). Una sola novità rispetto alla v2: arrotondamento del titolo di godimento a due vincoli (totali di cella e totali NIL × titolo). Soglie P1–P6 identiche. Non cieca su M8, P1–P3, P5, P6 (dichiarato). Tutte le scelte provvisorie del coordinatore.
**Attesa scritta nella pre-registrazione e non realizzata**: "errore di M8 ≤ 0,5 per cella; se no, regola di arresto". Osservato: 15 celle su 261 sopra 0,5, massimo 0,634. È un'inferenza sbagliata (i resti maggiori garantiscono |errore| < 1, non ≤ 0,5), non un errore di codice; il criterio P1 su M8 è largamente rispettato.

## 2. Dati e fonti
Come la v2 (cache v1, 26 SHA-256 coincidenti; margini e congiunta verificati). Nessun dato nuovo.

## 3. Metodo
Come la v2, salvo il blocco del titolo: (A) totali NIL × titolo con resti maggiori; (B) valori attesi per cella; (C) arrotondamento sistematico sulle somme cumulate, "altro" poi "affitto", "proprietà" residuo; (D) permutazione nella cella.

## 4. Risultati
- **P1 passa**: M0–M4 errore 0; M8 TAE/N 0,008%, errore relativo massimo 0,44% (celle ≥ 100; soglia 5%), assoluto massimo 0,56 (celle < 100; soglia 10); M5a 0,32%, M5b 0,66%.
- **P2 passa** (18 invarianti). **P3 passa**: stesso hash con lo stesso seme (`7ec73ec8…`); P1 e P2 passano su tutti i 10 semi; CV massimo 0,34%. **P5 passa** (G2 95,6%). **P4 non aperto.**
- **P6**: la regola del fattore 2 scatta solo per S5 (giovani coppie ×3,66): al congelamento la base va consegnata con **due popolazioni** (base e S5). S3: fascia grigia fra i richiedenti 9–15% (OMI) contro 33–41% (canoni d'annuncio).
- **Conteggi**: 881.980 nuclei; 343.108 richiedenti; famiglie con minorenni 121.779 (richiedenti 40.144), anziani soli 127.837 (41.576), giovani coppie 2.955 (1.327), giovani soli e nuovi arrivati 128.447 (60.766), studenti 70.000 (59.000).

## 5. Esito
Sospeso: i criteri valutati passano; l'esito finale dipende da (a) come trattare l'attesa non realizzata e (b) P4, valutabile una sola volta.

## 6. Limiti
Quelli di v1 e v2; inferenza sbagliata nella pre-registrazione (registrata); `valida_p4.py` mai eseguito (un suo errore emergerebbe solo all'unica esecuzione); confini NIL 2021–2025 non verificati; riproduzione da zero non fatta.

## 7. Revisione indipendente
Testo in `REVISIONE.md`. **Esito proposto: passa** per P1–P3 e P5 (riprodotti); attesa M8 = inferenza sbagliata; dopo v2 e v3 P1 non è una validazione esterna ("costruita dai dati"), l'unica validazione esterna è P4. Difetti gravi per l'uso a valle: **G1** fascia grigia ×3,5 secondo la fonte dei canoni (consegnare entrambe le definizioni); **G2** giovani coppie della base smentite dal dato (S5 come riferimento). Raccomanda di aprire P4 adesso, dopo prova a vuoto e appendice.

## 8. Cosa passa alla prova successiva
Se Dennis tratta l'attesa come inferenza sbagliata e non come criterio: P4 una volta con `valida_p4.py`, esito a registro, poi congelamento con `VERSIONE.md` e due popolazioni (base e S5).
