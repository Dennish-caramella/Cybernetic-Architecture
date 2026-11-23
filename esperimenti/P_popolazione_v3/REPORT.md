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
- **P1 passa** nel senso che il codice costruisce ciò che dichiara: dopo v2 e v3, M0–M4 sono copiati dalla congiunta di ds1441, M5 è calcolato su un obiettivo interno (quote condizionate di ds139) e M8 sui totali arrotondati. La popolazione è **costruita dai dati, non validata**: l'unica validazione esterna è P4, ancora chiuso e comunque debole (REVISIONE §7.5). Valori: M0–M4 errore 0; M8 TAE/N 0,008%, errore relativo massimo 0,44% (celle ≥ 100; soglia 5%), assoluto massimo 0,56 (celle < 100; soglia 10); M5a 0,32%, M5b 0,66%.
- **P2 passa** (18 invarianti). **P3 passa**: stesso hash con lo stesso seme (`7ec73ec8…`); P1 e P2 passano su tutti i 10 semi; CV massimo 0,34%. **P5 passa** (G1 τ 1,00, tautologico: G1 è additivo per costruzione, solo controllo di sanità; G2 95,6%). Il tipo chiamato "omofile" nel codice non è omofilia (quota s_ℓ uguale per tutti i nuclei): prima di B0–B6 va rinominato o reso dipendente dalla categoria, con nuova pre-registrazione dei generatori. **P4 non aperto.**
- **P6**: la regola del fattore 2 scatta solo per S5 (giovani coppie ×3,66): al congelamento la base va consegnata con **due popolazioni** (base e S5). S3: fascia grigia fra i richiedenti 9–15% (OMI) contro 33–41% (canoni d'annuncio).
- **Conteggi**: 881.980 nuclei; 343.108 richiedenti; famiglie con minorenni 121.779 (richiedenti 40.144), anziani soli 127.837 (41.576), giovani coppie 2.955 (1.327), giovani soli e nuovi arrivati 128.447 (60.766), studenti 70.000 (59.000).

- **Prodotti per G1 della revisione** (registro): ogni nucleo ha `fascia_grigia_omi` e `fascia_grigia_annunci` (richiedenti 29.113 contro 103.139; residenti 136.859 contro 343.050), fuori dall'hash di contenuto, che resta `7ec73ec8…`. Popolazione S5 (coppie conviventi) in `tabelle/categoria_S5_conviventi.csv.gz`, hash di contenuto `c3a82da0…`: differisce dalla base solo nella categoria di 7.859 nuclei; giovani coppie 10.814 nuclei, 4.854 richiedenti.
- **Preparativi di P4** (P4 non aperto): prova a vuoto di `valida_p4.py` su ds205 con rumore: 87 NIL su 87 abbinati (il NIL 8 di ds205 non ha famiglie in ds1441 2025 ed è escluso: dettaglio non pre-registrato); appendice informativa `appendice_minori.py` (quote di minori per residente, senza soglia). Il ramo con P4c non è mai stato eseguito.

## 5. Esito
Sospeso: i criteri valutati passano; l'esito finale dipende da (a) come trattare l'attesa non realizzata e (b) P4, valutabile una sola volta.

## 6. Limiti
Quelli di v1 e v2; inferenza sbagliata nella pre-registrazione (registrata); `valida_p4.py` mai eseguito (un suo errore emergerebbe solo all'unica esecuzione); confini NIL 2021–2025 non verificati; riproduzione da zero non fatta.

Ripieghi delle quote dei minori pesati sui nuclei con figli (212.733): 98,19% in celle dirette, 1,51% NIL × età, 0,31% età × componenti (monogenitori 96,47 / 3,03 / 0,50%); i conteggi 475 / 673 / 244 sono celle, non nuclei. La docstring di `run.py` diceva che le colonne tenute fuori di ds205 non vengono lette: `carica()` legge tutto ds205 ma usa solo il totale cittadino dei minori (M6); corretta il 23/11, solo testo. I valori 2024 di V1 e V2 sono nel repo dal 10/11 (nota 06): la cecità di P4 vale per dichiarazione [L].

## 7. Revisione indipendente
Testo in `REVISIONE.md`. **Esito proposto: passa** per P1–P3 e P5 (riprodotti); attesa M8 = inferenza sbagliata; dopo v2 e v3 P1 non è una validazione esterna ("costruita dai dati"), l'unica validazione esterna è P4. Difetti gravi per l'uso a valle: **G1** fascia grigia ×3,5 secondo la fonte dei canoni (consegnare entrambe le definizioni); **G2** giovani coppie della base smentite dal dato (S5 come riferimento). Raccomanda di aprire P4 adesso, dopo prova a vuoto e appendice.

## 8. Cosa passa alla prova successiva
Se Dennis tratta l'attesa come inferenza sbagliata e non come criterio: P4 una volta con `valida_p4.py`, esito a registro, poi congelamento con `VERSIONE.md` e due popolazioni (base e S5).
