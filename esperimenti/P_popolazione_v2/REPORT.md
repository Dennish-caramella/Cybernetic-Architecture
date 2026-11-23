# Report di laboratorio — Base P v2 (ticket #18)

Stato: **cambia** (P1 fallisce su due celle di M8; ne segue P3). Report assemblato dal coordinatore dalla consegna dell'agente `demografo-popolazioni-sintetiche`.

## 1. Ipotesi e soglia
`esecuzioni/00_preregistrazione.txt` (SHA-256 `1bf8df2a…`, commit eeaeca1, prima di ogni esecuzione). Scelte N1–N6 provvisorie del coordinatore (`tesi/DECISIONI.md`, 23/11); D1–D10 invariate. Non cieca su P1–P3 della v1 (dichiarato). Soglie come la v1.

## 2. Dati e fonti
Cache v1 riusata (26 file, SHA-256 verificati). Tabella congiunta ds1441 2025 (NIL × età × tipologia × componenti; 13.920 celle, 780.935 famiglie): sommata restituisce M1–M4 con scarto 0. Incrocio ISTAT titolo × occupanti per Milano: non esiste via API (lacuna L1).

## 3. Metodo
Scheletro = copia esatta della congiunta; minori da quote condizionate ds139 2021 (molte celle in ripiego); titolo con arrotondamento a resti maggiori per cella (N3); nuovi arrivati con arrotondamento controllato; minoranza polarizzata a punto ideale. Seme 20261122. Nessuna correzione di codice.

## 4. Risultati
- **P1 fallisce** solo per M8 (titolo di godimento per NIL), soglia di cella: NIL 66 "altro titolo" 99 contro 105 (5,7%), NIL 41 120 contro 127 (5,5%), soglia 5%. Tutti gli altri margini passano, M0–M4 con errore 0; M5a 0,32% e M5b 0,66% massimi (nella v1 97% e 64,5%). Causa [I]: l'arrotondamento per celle piccole sottostima la modalità rara (in città −286 "altro", +302 proprietari).
- **P2 passa** (18 invarianti). **P3 fallisce** solo perché P1 fallisce su tutti i 12 run; la variabilità fra semi crolla (CV massimo 0,27%, giovani coppie 0%, contro 2,27% della v1). **P4 non aperto**, ancora cieco. **P5 passa** (G2 95,6%, polarizzate 100% contro 0% della v1).
- **P6**: come v1 (S5 giovani coppie ×3,68; S3 fascia grigia fra i richiedenti 33–41% con i canoni d'annuncio contro 9–15% con OMI; S1 sposta anziani soli e giovani).
- **Conteggi**: 881.980 nuclei; 343.094 richiedenti (253.049 affittuari, 31.045 nuovi arrivati, 59.000 studenti); famiglie con minorenni 121.779 (richiedenti 40.161), anziani soli 127.837 (41.585), giovani coppie 2.955 (1.320), giovani soli e nuovi arrivati 128.447 (60.770); fascia grigia 29.091; ISEE 14–16k 11.100.

## 5. Esito
**Cambia**, per due celle di un margine. Regola di arresto: nessuna regolazione, P4 chiuso.

## 6. Limiti
Quelli della v1 e della pre-registrazione v2; quota di famiglie con minori 15,4% (18,3% nel 2021) dipende dalla stabilità delle quote 2021 e dai ripieghi; titolo per età assunto; non cieca su P1–P3.

## 7. Revisione indipendente
Non eseguita per la v2 (non passa per i suoi criteri; correzione indicata); si fa sulla v3 [coordinatore].

## 8. Cosa passa alla prova successiva
v3 con una sola correzione: arrotondamento controllato a due vincoli (totali di cella e totali NIL × titolo). Il resto della v2 regge e si riusa; P4 ancora cieco.
