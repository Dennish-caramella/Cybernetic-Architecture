# §7 Revisione indipendente — Base P v4 (ticket #18)

`revisore-metodologico`, 24/11/2026. Non ho eseguito la prova. Sono un'altra istanza dello stesso sistema, quindi questa non è una verifica umana. Marche: [V] verificato in questa sessione, [I] inferenza, [H] ipotesi, [L] lacuna.

## Esito proposto: **CAMBIA** (confermato), con arresto e decisione di Dennis

La regola pre-registrata è applicata correttamente: P4c e P4e falliscono, quindi P4 fallisce e la prova non si congela. Non ho trovato errori di codice né violazioni della pre-registrazione.

La diagnosi del REPORT (§5 e §8) però regge solo a metà:
- È vero che **s non è la leva**.
- Non regge che **la leva sia il numero di percettori**. Questa leva è limitata dal conteggio MEF e da sola non basta (vedi G1).

Raccomando quindi di **non** aprire una v5 che rincorra P4c o P4e (vedi la Raccomandazione).

## 7.1 Riproduzione

**Fatto [V]:**
- **Pre-registrazione:**
  - `sha256sum esecuzioni/00_preregistrazione.txt` dà `87392129…6038723`.
  - La versione nel commit `25a31fcb` (2026-11-23 21:41:42Z) ha lo stesso hash.
  - Quel commit contiene solo la pre-registrazione e il suo `.sha256`.
- **Hash di contenuto.** Ho rieseguito da capo `python3 -I run.py esegui` (seme 20261122, senza `--scrivi`, quindi nessun file della prova è stato toccato). Risultato:
  - hash `61373daf2922511d50d78c91e378b9ba61890cd440ea519461d25c42c539d11f`, identico;
  - P1 passa;
  - M9 con TAE/N 0,18%;
  - `n_secondari` = 173.810.
- **P4c, P4e e P4f** ricalcolati da `_cache/P_popolazione_v4/out/nuclei_base_20261122.csv.gz` e dai due CSV ISTAT in `_cache/P_popolazione_v4/p4/`. Gli SHA-256 coincidono col registro: `60e6eb9f…` e `c438297a…`.
  - Mediana netta dei 780.935 nuclei residenti: **28.301,5 €**.
  - Con capofamiglia ≥ 65: 27.256,66 €.
  - V5 = **33.536 €**, con banda 30.182,4–50.304 → fallisce.
  - P4f: rapporti 1,13 / 0,74 / 0,61 / 0,60 / 0,66 per 1, 2, 3, 4 e 5+ componenti. Tutti i valori coincidono con `tabelle/P4_esito.json`.
- **Codici ISTAT**, letti nella codelist in `meta/rednet9_struct.xml`:
  - REF_AREA "2" = "centro area metropolitana";
  - IMPUTED_RENTS "2" = "esclusi fitti imputati";
  - FAM_MAIN_INCOME_SOURCE "9" = "totale";
  - NUMBER_HOUSEHOLD_COMP "7" = "cinque o più";
  - ITC = Nord-ovest.

  Il file `rednet_9` contiene una sola serie (2003–2024), quindi il filtro non può prendere la riga sbagliata.
- **Test:** `test_popolazione.py` sulla popolazione in cache dà 18/18, con uscita 0.
- **Blocco dei ruoli.** Ho estratto il blocco alla lettera e l'ho provato su dati sintetici (N = 200.000, 17,6% di secondari):
  - l'insieme degli u è identico per s = 0, 0,5 e 1;
  - l'ordine dentro ciascun ruolo è conservato;
  - con s = 1 i secondari prendono esattamente i valori più bassi.
- **Scenari rieseguiti** (script mio in scratchpad, che chiama `run.genera`):
  - **S10_s1:** mediana 27.353 €; per componenti 25.752 / 27.705 / 29.530 / 31.982 / 33.534 €. Coincide con il registro (01:46:23Z).
  - **S9_q09** (q2 = 0,9), mai riportato dal REPORT: mediana **29.556 €**, che fallisce sia P4e sia P4c. Percettori 1.024.918; lordo totale 44,66 miliardi di €.

**Non fatto:** S10_s0 (26.528 €, preso dal registro [I]), `robustezza` (P3), `sensibilita` (P6), una riproduzione senza cache [L]. Non ho riscaricato i dati ISTAT: ho usato i file in cache, che hanno gli hash del registro.

## 7.2 Pre-registrazione e ordine delle operazioni [V]

- **Ordine dei commit.**
  - Pre-registrazione: `25a31fc`, 21:41:42Z.
  - Copia del codice: `b36c99e`, 21:43:22Z.
  - Codice modificato: `4bc5377`, 21:48:06Z.

  Dopo `4bc5377` né `run.py` né `valida_p4.py` sono cambiati (`git log` per file). Quindi la prova a vuoto (22:31Z) e P4 (22:32Z) hanno girato su codice già committato.
- **Diff con la v3:**
  - `run.py` cambia solo in docstring, `OUT`, `BASE` (`s_ruolo`, `c2`), `SCENARI` (S10, S11) e nel blocco 4.3 (7 righe).
  - `valida_p4.py` cambia solo per P4e e P4f.
  - `appendice_minori.py`, `test_popolazione.py`, `scarica.py`, `dati_metadati.csv` e `requirements.txt` sono identici byte per byte.

  La modifica è quindi limitata a quanto pre-registrato.
- **Il blocco nuovo corrisponde al testo pre-registrato §1(b):**
  - punteggio `s·rango + (1 − s)·v`, con `v` dal flusso R[3];
  - i `ns` punteggi più bassi vanno ai secondari;
  - dentro ciascun ruolo i valori si riassegnano in ordine di u originale.
- **Prova a vuoto senza valori di riferimento.** Nel ramo `--prova`, V5 e P4f sono finti e non c'è nessun download. Le due colonne di ds205 non vengono caricate (`usecols`).
- **V5 non era nel repo prima di P4.** `git grep` su `a8007a8` trova solo il CSV della Lombardia (ITC4) usato da P4c.
- **c2 non applicato:** è il ramo previsto dalla pre-registrazione quando l'Allegato 2 non si legge. È a registro.
- **Regola di esito:** P4 = P4a ∧ P4b ∧ P4c ∧ P4e (riga 57 di `valida_p4.py`), come pre-registrato. Esito "cambia" corretto.

## 7.3 Difetti gravi

**G1 — La diagnosi e la leva proposte per la v5 non reggono. Le bande di P4c e P4e sono probabilmente irraggiungibili restando coerenti con MEF e anagrafe [V sui numeri, I sulla conclusione].**

Questo difetto non tocca l'esito della v4. Tocca la decisione su cosa fare dopo.

Prove:
1. **Il livello del reddito è già quello del MEF.**
   - Percettori simulati: 985.790. Le frequenze MEF delle classi M9 sono 1.013.387 e i contribuenti dichiarati 1.052.520 (file `mef_comunale_2024`, anno d'imposta 2024).
   - Lordo simulato totale: 42,95 miliardi di €, contro 42,44 miliardi di reddito complessivo MEF.
   - Il netto medio dei nuclei residenti è 36.669 €: sopra V5 e quasi pari a V3.

   Il problema non è il livello ma la distribuzione fra nuclei.
2. **Il margine di "più percettori" è piccolo e non basta.**
   - Restano al massimo circa 27.600 percettori contro M9, o circa 67.000 contro i contribuenti, a fronte di 173.810 secondari.
   - Lo scenario pre-registrato S9_q09 aggiunge 39.128 percettori. Supera già il conteggio M9 e il lordo MEF (+5,2%). Eppure la mediana arriva solo a 29.556 €, sotto entrambe le soglie.
3. **La composizione dei nuclei basta da sola a spiegare gran parte dello scarto.**
   - I nuclei di una persona sono il 57,5% dei residenti simulati. Il dato è esatto per costruzione: M4 viene da ds1441.
   - Il 78% di nuclei con un solo percettore citato nel REPORT discende in gran parte da qui.
   - Controfattuale grezzo [I]: porto i redditi di ogni classe di ampiezza alla mediana del Nord-ovest, conservando la forma interna. Con il mix di Milano la mediana complessiva sarebbe **29.827 €**, ancora sotto P4e, e servirebbe il 17,5% di netto in più rispetto al totale coerente col MEF.
   - Lasciando le persone sole come sono e portando al Nord-ovest solo i nuclei con più componenti: **32.629 €**, ancora sotto P4c, con +23,8% di netto.
   - Con il 40% di persone sole e i livelli del Nord-ovest la mediana sarebbe 34.603 €.

   Quindi P4c e P4e confrontano mediane di popolazioni con composizioni diverse: Lombardia e centri metropolitani italiani da una parte, famiglie anagrafiche di Milano dall'altra. Una parte del fallimento è un effetto di composizione del criterio, non del modello. La quota di persone sole in V3 e V5 è [L].

Conseguenza: una v5 costruita sul punto 1 del §8 dovrebbe gonfiare percettori o reddito oltre il MEF per inseguire una soglia che non è più cieca. È adattamento ai dati di validazione. P1 non se ne accorgerebbe (vedi D1).

Correzione:
- Riscrivere §5 e §8 del REPORT: "il reddito totale è coerente col MEF; lo scarto viene dalla distribuzione fra nuclei e dalla composizione (57,5% di persone sole); la leva 'più percettori' è limitata dal conteggio MEF e S9_q09 non basta".
- Nessuna v5 che usi P4c o P4e come obiettivo.

## 7.4 Difetti da correggere

- **D1 — M9 in P1 controlla solo le proporzioni.**
  - Prova: alla riga 443 di `run.py` l'obiettivo è `D["M9"] * sim.sum() / D["M9"].sum()`. Né il numero di percettori né il reddito totale sono vincolati al MEF.
  - Correzione: riportare nel REPORT, come informazione, percettori simulati contro frequenze M9 e contribuenti, e lordo totale contro MEF. In una v5 eventuale, P1 deve avere un controllo sui conteggi e sul totale.
- **D2 — Le mediane di sensibilità non sono riproducibili dal repo.**
  - Prova: il registro (01:42Z e 01:46Z) cita un "calcolo informativo" di S10. Non c'è script né log nella cartella, e in cache c'è solo la popolazione di base.
  - Le cifre di S10_s1 le ho riprodotte [V], quindi i numeri reggono. Il passaggio però non è riproducibile.
  - Correzione: committare lo script (dieci righe su `run.genera`) e il suo output in `esecuzioni/log/`.
- **D3 — S9 (q2) non è riportato.** Era il test diretto della leva proposta.
  - Correzione: aggiungere la mediana di S9_q05 e di S9_q09 (S9_q09 = 29.556 €, [V] qui).
- **D4 — "Nessun valore di s raggiunge le soglie" è un'estrapolazione da tre punti.**
  - L'affermazione è plausibile. Nella mia prova sintetica la mediana degli u dei principali è già 0,587 con s = 0,5 e resta 0,587 con s = 1: per i principali la leva è esaurita a metà dell'intervallo. Questo spiega perché le persone sole restano quasi ferme (25.750 contro 25.752 €) e perché la mediana non è monotona in s.
  - Correzione: marcare la frase [I] e aggiungere questa spiegazione.
- **D5 — Anno di riferimento di EU-SILC [L].**
  - Non ho verificato se TIME_PERIOD 2024 indica l'anno dell'indagine o l'anno del reddito, che va allineato all'anno d'imposta MEF 2024.
  - L'esito non cambia: con il V5 del 2023 (31.773 €) la soglia è 28.595,7 € e 28.301,5 € fallisce comunque [V].
  - Correzione: scriverlo nei Limiti.
- **D6 — s è una leva importante a valle.**
  - La fascia grigia OMI va da 29.112 (s = 0) a 36.155 (s = 1), con 34.656 nella base. Il budget mediano degli anziani soli passa da 508 a 627 €.
  - Correzione: S10 obbligatorio a valle, accanto a S9 e alle due definizioni di fascia grigia (il §8 lo dice già per S9 e S10: va mantenuto).

## 7.5 Difetti minori

- **M1** `tabelle/G3_veri_astratti.sha256` indica come percorso `_cache/P_popolazione/out`. Il file sta in `_cache/P_popolazione_v4/out`; l'hash `60ad875d…` coincide [V].
- **M2** Il commit `ac27f53` mescola file della v4 e del Banco: tracciabilità debole, già segnalata nella v3.
- **M3** La riga di P4 nel registro (22:32:30Z) è entrata in git solo alle 01:41Z (`1b87545`). Che P4 sia stato eseguito una sola volta resta auto-dichiarato. Le date di modifica dei file (`P4_esito.json` e `rednet_*.csv` alle 22:32) sono coerenti [I].
- **M4** Il pilota (21:45:26Z) ha girato su codice committato solo alle 21:48:06Z. Il codice non è cambiato dopo, quindi non incide.
- **M5** Mancano test sul blocco nuovo (insieme degli u invariato, ordine conservato nel ruolo). L'unica protezione indiretta è M9 identico alla v3; il mio test esterno passa.
- **M6** `c2` è un parametro senza effetto nel codice e S11 coincide con la base: è inutile calcolarlo. Va detto, o tolto in una versione futura.
- **M7** P4c-65 confronta i nuclei con capofamiglia ≥ 65 con la fonte "pensione". È un disallineamento ereditato dalla v1, non nuovo.

## 7.6 Cosa non ho verificato

- S10_s0, P3 (12 esecuzioni) e P6 completo non sono stati rieseguiti.
- Nessuna riproduzione senza cache, nessun nuovo download da ISTAT.
- Il testo della circolare INPS e l'assenza dell'Allegato 2 non li ho controllati.
- La quota di persone sole nelle popolazioni di V3 e V5 è [L]: il controfattuale di G1 è un'inferenza su scala grezza, non un test.
- Non ho verificato che l'unicità dell'esecuzione di P4 si possa dimostrare oltre le date dei file.

## 7.7 Raccomandazione (decide Dennis)

1. **Esito: cambia** per il reddito. Vale la regola di arresto: ticket di revisione e decisione con Dennis.
2. **Fra le due strade raccomando la seconda:** congelare la struttura (scheletro, minori, titolo, ancore, generatori; P1, P2, P3 e P5 riprodotti) e dichiarare il reddito **"non validato"**.
   - Usare il reddito della v4 (s = 0,5), con S10 (s = 0 e s = 1) e S9 obbligatori a valle e con entrambe le fasce grigie.
   - Questa è una **deviazione** dalla pre-registrazione, che lega `VERSIONE.md` al superamento di P4. Va registrata come tale in `tesi/DECISIONI.md`, non presentata come "passa".
3. **Una v5 del reddito ha senso solo se, prima di eseguirla, si pre-registra:**
   - un criterio esterno corretto per la composizione, per esempio le mediane per numero di componenti, o V5 riponderato sul mix di Milano;
   - i vincoli MEF su numero di percettori e reddito totale (D1);
   - una fonte nuova e cieca.

   Senza questi tre elementi una v5 rischia solo di adattarsi a P4c e P4e, che non sono più ciechi.
