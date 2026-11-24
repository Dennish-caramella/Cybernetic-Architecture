# Report di laboratorio — Base P v4 (ticket #18)
Esito: **CAMBIA**. P1, P2, P3 e P5 passano. P4 fallisce su P4c e sul nuovo P4e: il reddito netto mediano dei nuclei è ancora troppo basso. Non c'è `VERSIONE.md`. Testo preparato dall'istanza esecutrice (`demografo-popolazioni-sintetiche`) e scritto nel file dal coordinatore. La §7 è riservata al revisore.

## 1. Ipotesi e soglia
- Testo pre-registrato: `esecuzioni/00_preregistrazione.txt`, SHA-256 `87392129…`, commit `25a31fcb` (2026-11-23T21:41:42Z), riga 1 del registro.
- Unica modifica rispetto alla v3: il modello del reddito per nucleo.
  - (b) percettore principale e percettori secondari, con punteggio s·rango + (1 − s)·U e s = 0,5 [H-R].
  - (c) trasferimenti non IRPEF: c2 (assegno sociale) e c3 (altri redditi).
- Soglie P1–P6 invariate. P4 richiede P4a, P4b, P4c e il nuovo P4e (cieco); P4f è informativo.
- La v4 non è cieca su P4c: era noto il valore della v3, 26.540 €.
- Scelte: la strada (b)+(c) è provvisoria del coordinatore (`tesi/DECISIONI.md`, 23/11); le scelte D, N e H-N3 le ha confermate Dennis il 23/11.

## 2. Dati e fonti
Come la v3 (cache della v1, 26 SHA-256 coincidenti, `controlla` con scarto 0). Novità:
- **c2, assegno sociale: lacuna [L], non applicato.**
  - La circolare INPS n. 1 del 2/1/2024 (lette due copie; testo in `_cache/P_popolazione_v4/inps/`) rinvia all'Allegato n. 2 per importi e limiti, e fissa l'età a 67 anni [V].
  - L'Allegato n. 2 non è in nessuna copia trovata; le cifre di stampa sono [S] e non concordano fra loro.
  - Per questo S11 (senza c2) coincide con la base.
- **c3** (redditi da capitale, cedolare secca, ADI): lacuna [L]. Il file MEF comunale non ha queste colonne [V].
- **P4e e P4f:** ISTAT EU-SILC, flussi `32_292_DF_DCCV_REDNETFAMFONTERED_9` e `_1`.
  - Scaricati solo durante l'esecuzione di P4, in `_cache/P_popolazione_v4/p4/` (SHA-256 `60e6eb9f…` e `c438297a…`).
  - V5 = 33.536 € (comuni centro di area metropolitana, Italia, 2024, esclusi fitti imputati) [V].

## 3. Metodo
Come la v3, tranne il blocco del reddito:
- Il percettore principale è il capofamiglia; gli altri sono secondari (173.810, stesso numero di prima).
- Per ogni percettore j si calcola il punteggio s·rango(u_j) + (1 − s)·v_j, con v_j ~ U(0,1).
- Gli n_sec percettori con il punteggio più basso cedono i loro valori u ai secondari. Dentro ciascun ruolo i valori si riassegnano conservando l'ordine dei ranghi originali.
- Restano identici alla v3: l'insieme degli u, quindi M9; il numero di percettori, quindi le ancore di lavoro.

## 4. Risultati (seme 20261122; hash di contenuto `61373daf2922511d50d78c91e378b9ba61890cd440ea519461d25c42c539d11f`)

**Criteri P1, P2, P3, P5**
- **P1 passa:** M0–M4 errore 0; M8 errore relativo massimo 0,44%; M9 TAE/N 0,18%.
- **P2 passa:** 18 invarianti su 18.
- **P3 passa:** stesso hash con lo stesso seme; P1 e P2 passano su tutti i 10 semi; variazione massima dei richiedenti fra semi 0,34%.
- **P5 passa:** G2 95,6%.

**P4, valutato una sola volta**

| Prova | Valore | Soglia | Esito |
|---|---|---|---|
| P4a: anziani soli 80+ per NIL | Spearman 0,9992; SRMSE 0,029 | ≥ 0,80; ≤ 0,30 | passa |
| P4b: minori per NIL | Spearman 0,9985; SRMSE 0,031 | ≥ 0,85; ≤ 0,25 | passa |
| P4c: reddito netto mediano | 28.302 € | 33.188–55.313 € | **fallisce** |
| P4c: capofamiglia ≥65 | 27.257 € | 22.074–41.390 € | dentro |
| P4e (cieco), V5 = 33.536 € | 28.302 € | 30.182–50.304 € | **fallisce** |
| Appendice: quote di minori per residente | Spearman 0,946; SRMSE 0,087 | — | — |

**P4f, informativo:** reddito mediano simulato e del Nord-ovest, per numero di componenti.

| Componenti | Simulato | Nord-ovest | Rapporto |
|---|---|---|---|
| 1 | 25.750 € | 22.697 € | 1,13 |
| 2 | 29.867 € | 40.631 € | 0,74 |
| 3 | 32.092 € | 52.852 € | 0,61 |
| 4 | 35.144 € | 58.799 € | 0,60 |
| 5 o più | 36.674 € | 55.968 € | 0,66 |

**P6: sensibilità S1–S11** (18 scenari, `tabelle/P6_sensibilita.csv`)
- Il fattore 2 scatta solo con S5: giovani coppie ×3,66, 4.854 nuclei.
- Fascia grigia fra i richiedenti, nella base: **34.656 nuclei con i canoni OMI e 117.608 con quelli d'annuncio** (v3: 29.113 e 103.139).

| Scenario | Fascia grigia OMI | Fascia grigia annunci |
|---|---|---|
| s = 0 | 29.112 | 103.096 |
| s = 1 | 36.155 | 115.801 |
| S6 (inquilini di case popolari esclusi) | 26.959 | 91.855 |

- Budget mediano dei richiedenti, base contro v3: anziani soli 627 € (era 508 €); famiglie con minori 858 € (era 910 €); giovani soli e nuovi arrivati 656 € (era 554 €).

**Conteggi per categoria (base)**

| Categoria | Nuclei | Richiedenti | Fascia grigia OMI | Fascia grigia annunci |
|---|---|---|---|---|
| studenti fuori sede | 70.000 | 59.000 | 0 | 0 |
| famiglie con figli minorenni | 121.779 | 40.144 | 4.333 | 12.751 |
| anziani soli | 127.837 | 41.576 | 7.077 | 20.011 |
| giovani coppie | 2.955 | 1.327 | 142 | 550 |
| giovani soli e nuovi arrivati | 128.447 | 60.766 | 6.287 | 25.552 |
| nessuna categoria | 430.962 | 140.295 | 16.817 | 58.744 |
| **Totale** | **881.980** | **343.108** | **34.656** | **117.608** |

Fascia ISEE 14–16 mila: 12.829 richiedenti.

## 5. Esito
**CAMBIA.** P4c e P4e falliscono: mediana di 28.302 € contro soglie minime di 33.188 € e 30.182 €. Non ci sono errori di codice.

La correzione dei ruoli (b) recupera circa 1.760 € rispetto alla v3, ma non basta. Secondo P4f il difetto si è spostato [I]:
- le persone sole ora stanno sopra il Nord-ovest (rapporto 1,13);
- i nuclei con due o più componenti restano al 60–74%.

Cause possibili:
- un solo percettore nel 78% dei nuclei;
- secondo percettore nelle coppie con probabilità 0,7 [H];
- assegno sociale (c2) e redditi non IRPEF (c3) mancanti;
- famiglia anagrafica contro famiglia di fatto.

**Sensibilità e banda (informativo, P4 non riaperto).** Mediana netta dei nuclei residenti:

| Scenario | Mediana |
|---|---|
| base, s = 0,5 | 28.302 € |
| s = 0 | 26.528 € (circa la v3) |
| s = 1 | 27.353 € |
| S11 | uguale alla base |

La variante più vicina alla banda è la base, a −1.880 € dalla soglia di P4e e a −4.886 € da quella di P4c. Con s = 1 le persone sole salgono a 25.752 €, ma i nuclei con più componenti scendono a 27.705–33.534 €. Nessun valore di s raggiunge le soglie.

## 6. Limiti
- Valgono quelli di v1–v3.
- P4c non è cieco; P4e è cieco ma riguarda l'Italia (comuni centro di area metropolitana), non Milano.
- s non ha fonte.
- c2 e c3 sono lacune.
- La probabilità 0,7 del secondo percettore nelle coppie è un'ipotesi [H]: confermata come scelta, non misurata.
- P4f usa il Nord-ovest, quindi è solo un controllo.
- Non verificato: che la combinazione "centro area metropolitana" 2024 sia confrontabile con le famiglie anagrafiche (famiglia di fatto contro famiglia anagrafica).

## 7. Revisione indipendente
(da scrivere a cura del `revisore-metodologico`)

## 8. Cosa passa alla prova successiva
- **Nessun congelamento.** Restano valide e riprodotte le parti che non dipendono dal reddito: scheletro, minori, titolo, ancore, generatori; P1, P2, P3, P5.
- **Per una v5** (nuovo ticket, nuova pre-registrazione, non cieca né su P4c né su P4e), le leve indicate dai dati, in ordine:
  1. il numero di percettori nei nuclei con più componenti, da una fonte: EU-SILC per numero di percettori o per tipologia, oppure dati sulle famiglie con più occupati;
  2. la fonte primaria INPS per l'assegno sociale (Allegato 2);
  3. i redditi non IRPEF, dove esista una fonte.
  - s non è la leva: nessun suo valore raggiunge la banda.
- **Validazione esterna.** Dopo la v4 non resta una validazione esterna cieca del reddito con fonti aperte: va dichiarato, oppure va trovata una fonte nuova.
- **In alternativa, decisione di Dennis:** usare la base con il reddito dichiarato "non validato". La fascia grigia si riporta sempre come forbice (OMI contro annunci), e i risultati a valle che dipendono dal reddito vanno dati con le sensibilità S9 e S10.
