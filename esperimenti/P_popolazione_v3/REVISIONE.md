# §7 Revisione indipendente — Base P v1 → v2 → v3 (ticket #18)

`revisore-metodologico`, 23/11/2026; non ha eseguito le prove. Testo trascritto dal coordinatore dalla consegna del revisore (che non può creare file); condensato nelle parti descrittive, completo negli esiti e nelle raccomandazioni. È un'altra istanza dello stesso sistema: non è una verifica umana.

## 7.1 Riproduzione [V]
Cache: 26/26 SHA-256 coincidenti; `controlla` scarto 0. Riesecuzione in copia isolata: stesso hash di contenuto `7ec73ec8…`; tabelle identiche byte per byte; .gz identici nel contenuto decompresso; 18/18 invarianti. NIL 21 ricontrollato a mano sulla congiunta ds1441 con un parser indipendente: 90 celle, 0 differenze, 35.740 famiglie. M8: tutte le 261 celle in {⌊TT⌋, ⌈TT⌉}; 15 con |errore| > 0,5, massimo 0,634. Non rieseguiti `robustezza` e `sensibilita` (presi dalle tabelle [I]); nessuna riproduzione senza cache [L]; `valida_p4.py` non eseguito.

## 7.2 Ordine dei commit
Rispettato in tutte e tre le versioni (pre-registrazione prima di ogni esecuzione). Riserve: la frase "scritta prima di scrivere il codice" nelle pre-registrazioni v2 e v3 non è plausibile (codice committato 98 s e 50 s dopo); file della v2 entrati in commit con messaggi del Banco (tracciabilità debole); tempi del registro auto-dichiarati.

## 7.3 Divieto di cambiare regole dopo aver visto i dati
Formalmente rispettato. Nella sostanza: la v2 ha cambiato il metro di M5 (obiettivo interno invece di quota ds139 2021 × famiglie 2025): col vecchio confronto la v3 avrebbe TAE/N 17,7%, Spearman 0,46 (in parte perché anche il vecchio obiettivo era distorto: universi ds139 e ds1441 diversi). L'arrotondamento controllato toglie significato al criterio di variabilità di P3. **Dopo v2 e v3 nessun margine di P1 è una validazione esterna**: "P1 passa" significa "il codice costruisce ciò che dichiara". L'unica validazione esterna è P4.

## 7.4 Attesa M8 ≤ 0,5
**Inferenza sbagliata, non criterio**: sta tra le "conseguenze attese [I]"; con i resti maggiori l'errore è < 1, non ≤ 0,5; le altre attese si realizzano. Va chiusa come decisione registrata, non come misura; la pre-registrazione v3 non si tocca.

## 7.5 Potenza di P4
P4a è coerenza fra registri; P4b su conteggi è facile da superare (dominato dalla dimensione dei NIL); P4c debole. Un "P4 passa" sarebbe prova debole, un "P4 fallisce" informativo.

## 7.6 Qualità per l'uso a valle
1. Ancore di lavoro da matrice 2011 (700.558, 19,7% fuori Milano): da trattare come [H] a valle, sensibilità in A2 e B6.
2. **Giovani coppie**: base 2.955 nuclei (0,39% dei richiedenti); il dato in cache smentisce D3: ds139 2021 conta 6.065 coppie conviventi senza figli con capofamiglia 18–34, contro 2.956 sposate. La variante S5 (×3,66) è meglio sostenuta della base.
3. **Fascia grigia**: 29.113 richiedenti con canoni OMI contro 103.139 con canoni d'annuncio (×3,54); la regola del fattore 2 guarda solo le categorie e non la vede.
4. Ripieghi dei minori: pesati sui nuclei sono pochi (98,2% in celle dirette): la preoccupazione non è fondata; il problema è livello e distribuzione delle famiglie con minori (15,4% contro 18,3% del 2021).
5. Titolo indipendente dall'età (affitto 32,2–32,6% per classe d'età); la composizione dei richiedenti dipende da D4; T1 sposta anziani soli ×0,58 e giovani ×1,5.
6. La regola delle due popolazioni (base + S5) va rispettata ma da sola non propaga le incertezze grandi.

## 7.7 Difetti
**Gravi (bloccano il congelamento finché Dennis non decide)**
- **G1** L'incertezza sulla fascia grigia non arriva a valle. Correzione: due campi per nucleo, `fascia_grigia_omi` e `fascia_grigia_annunci` (codice già pre-registrato, scenario S3); ogni risultato su B0–B6 e A1–A4 con entrambe le definizioni.
- **G2** Giovani coppie della base smentite dal dato in cache. Correzione: S5 popolazione di riferimento per le giovani coppie, base come limite inferiore; S5 come base solo con una v4.

**Da correggere**: (1) il REPORT non dica "validata" ma "costruita dai dati; validazione esterna solo P4"; (2) appendice informativa sulle quote di minori per NIL committata prima di P4; (3) prova a vuoto di `valida_p4.py` su dati sostituiti con rumore; (4) T1 scenario obbligatorio a valle o rapporti per età da fonte; (5) il tipo "omofile" di G2 non è omofilia (attributo comune del lotto): rinominarlo o renderlo dipendente dalla categoria prima di B0–B6; (6) revisioni di v1 e v2 saltate e H-N3 assente da `DECISIONI.md`: registrare come deviazioni; (7) ancore 2011 come [H] a valle.
**Minori**: frase "prima del codice" non plausibile; commit con messaggi del Banco; docstring su V2; valori 2024 di V1 e V2 già nel repo dal 10/11 (cecità di P4 solo per dichiarazione [L]); P5a tautologico; nidi 2018/19 e scala ISEE fissa oltre 5; ancora "cura" per capofamiglia ≥ 65; ripieghi da riportare pesati sui nuclei.

## 7.8 Esito proposto
**Passa** per P1–P3 e P5 (riprodotti, nessun errore di codice). L'esito finale dipende da P4; G1 e G2 bloccano il congelamento finché Dennis non decide. Diventa "cambia" (v4) se P4 fallisce o se Dennis vuole cambiare D3 o D4 nella base.

## 7.9 Condizioni per congelare
1. Decisione di Dennis sull'attesa M8. 2. Prova a vuoto e appendice committate prima di P4. 3. P4 una sola volta, esito subito a registro. 4. Due popolazioni (base e S5) più i due campi di fascia grigia; hash in `VERSIONE.md`. 5. REPORT corretto. 6. Una eventuale v4 non tocca scheletro, minori e reddito.

## 7.10 Cosa deve decidere Dennis (raccomandazioni del revisore)
1. Attesa M8 come inferenza sbagliata: sì, come decisione. 2. Aprire P4 sulla v3: sì, adesso, dopo prova a vuoto e appendice (le grandezze di P4 non dipendono da D3, D4, D7). 3. D3: S5 come definizione di riferimento delle giovani coppie. 4. D7: consegnare e riportare entrambe le definizioni di fascia grigia. 5. D4: T0 base con T1 scenario obbligatorio; cercare una fonte. 6. Conferma o rifiuto di D1–D10, N1–N6, H-N3.
