# Report di laboratorio — Base P v1: popolazione sintetica dei nuclei abitativi (ticket #18)

Stato: **cambia** (P1 e P3 falliscono). Regola di arresto: non congelata; v2 con pre-registrazione nuova. Report assemblato dal coordinatore dalla consegna dell'agente `demografo-popolazioni-sintetiche`.

## 1. Ipotesi e soglia
`esecuzioni/00_preregistrazione.txt` (SHA-256 `fa0ec4f8…`, commit 07f3bf3, prima di ogni esecuzione). Scelte D1–D10 accettate provvisoriamente dal coordinatore, non da Dennis (`tesi/DECISIONI.md`, 22/11). Criteri P1 (errore sui margini), P2 (invarianti), P3 (riproducibilità e robustezza sui semi), P4 (margini tenuti fuori), P5 (generatori delle preferenze), P6 (sensibilità).

## 2. Dati e fonti
26 file grezzi scaricati il 22/11 (cache, 27 MB) con URL, licenza, data e SHA-256 in `dati_metadati.csv`; aggiunti i confini comunali ISTAT 2024 (correzione di acquisizione, a registro). ds234 è CC BY-NC. Controllo d'ingresso: tutti i margini ricalcolati dai dati grezzi coincidono con i CSV delle note (scarto 0). Margine per CAP non usabile [L] (i civici non hanno il CAP).

## 3. Metodo
IPF in 3 dimensioni (NIL × tipologia × età) e arrotondamento a resti maggiori; componenti con IPF e zeri strutturali; minori calibrati sul totale; titolo di godimento indipendente da età e tipologia dentro il NIL; reddito dalle classi MEF con coda di Pareto, netto e proxy ISEE; residenza su civico; canone dalla zona OMI; ancore di lavoro dalla matrice origine-destinazione 2011, scuola e cura al servizio più vicino, università sulla sede. Due errori di codice corretti (codice di sezione letto come stringa; flag "fuori Milano"), a registro. Uno zero strutturale aggiunto (niente minori con capofamiglia ≥ 80 anni), a registro.

## 4. Risultati
- **P1 fallisce**: M4 componenti TAE/N 3,64% (soglia 0,5%); M5a nuclei con minori per NIL 1,49% con celle fino al 97%; M5b monogenitori celle fino al 64,5%. Gli altri margini passano (totale residenti 780.935 esatto). Cause [V]: gli zeri strutturali pre-registrati sono smentiti dal dato (tutte le 14.191 famiglie "in convivenza" hanno 1 componente; 2.218 coppie sposate senza figli hanno ≥ 3 componenti); le quote dei minori per NIL del 2021 non reggono dove il NIL è cambiato (NIL 73: 20 famiglie nel 2021, 912 nel 2025).
- **P2 passa** (17 invarianti). **P3 fallisce**: stesso seme → stesso hash, ma P1 fallisce su tutti i 10 semi e il coefficiente di variazione delle giovani coppie è 2,27% (soglia 2%). **P4 non valutato** di proposito: la pre-registrazione dice di fermarsi se P1 fallisce, e aprirlo toglierebbe alla v2 la validazione cieca. **P5 passa** (G1 τ = 1,00; G2 75,7% con τ ≤ 0,80, ma la minoranza "polarizzata" resta additiva; G3 parametri sigillati).
- **P6**: la regola del fattore 2 scatta solo per S5 (giovani coppie ×3,69), variante incoerente col dato; S3 (canoni d'annuncio) porta la fascia grigia fra i richiedenti da circa 9% a 35–41%; S1 (titolo per età) sposta molto anziani soli (×0,58) e giovani (×1,5).
- **Conteggi** (seme 20261122): 881.980 nuclei, 343.108 richiedenti (253.063 affittuari residenti, 31.045 nuovi arrivati, 59.000 studenti); in fascia grigia 29.024 (8,5%); fascia ISEE 14–16k 11.313. Giovani coppie quasi vuote (2.959 nuclei): il dato non distingue le coppie non sposate.

## 5. Esito
**Cambia.** P1 e P3 falliscono per cause di metodo e di dati; P4 resta chiuso per la v2.

## 6. Limiti
Quelli della pre-registrazione (§10); proxy ISEE senza patrimonio; fascia grigia bassa con i canoni OMI (alta con quelli d'annuncio); giovani coppie non misurabili; formula del netto e coefficienti ISEE oltre 4 componenti [L]; riproducibilità senza cache non verificata; sedi universitarie ds94 al 2011.

## 7. Revisione indipendente
Non eseguita per la v1: la prova non passa per i suoi stessi criteri e le correzioni sono già indicate; la revisione si fa sulla v2 [decisione del coordinatore, per risparmiare risorse].

## 8. Cosa passa alla prova successiva
Nessuna base congelata. Per la v2: tabella congiunta vera di ds1441 (NIL × età × componenti × tipologia) al posto dell'IPF a margini, togliendo gli zeri strutturali inventati (l'IPF sbagliava del 6–10% sulle tabelle vere); quote dei minori dalla stessa fonte; verifica dell'incrocio ISTAT titolo × occupanti; P4 tenuto chiuso; forma non additiva per la minoranza polarizzata. Si riusano download, controllo dei margini, ancore e generatori.
