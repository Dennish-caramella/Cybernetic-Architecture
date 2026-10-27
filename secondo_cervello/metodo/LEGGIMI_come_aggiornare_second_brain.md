# Second brain delle analisi approfondite: come aggiornarlo

Questa cartella è costruita sulle analisi in `03_Analisi Approfondite/` (file 01–27 più l'indice 00, copiati dal computer il 2026-10-19). Non modifica nessun file della tesi.

## Contenuto

- `00_LEGGIMI_come_aggiornare.md`: questo file.
- `01_INDICE_BREVE.md`: una riga per analisi, con costellazione, idea e avvisi.
- `02_MAPPA_CONCETTI.md`: assi concettuali e collegamenti trasversali (inferenze segnalate).
- `03_AUDIT_TESI.md`: audit della cartella TESI del 2026-10-10 (problemi aperti).
- `04_MAPPA_SOVRAPPOSIZIONE.md` (2026-10-19): matrice di sovrapposizione tra le cinque analisi in `tesi_out/da_artifact/` e il corpus 01–24, con tipo di legame (dichiarato, inferenza, tensione) e forza.

Le analisi in `tesi_out/da_artifact/` non sono numerate nella serie 01–24: sono in `01_INDICE_BREVE.md`, in una sezione separata con costellazione proposta da confermare.

## Ordine di lettura per risparmiare token

1. `01_INDICE_BREVE.md` per trovare la scheda giusta.
2. `02_MAPPA_CONCETTI.md` per i collegamenti.
3. Solo se serve: l'analisi completa in `03_Analisi Approfondite/`, aprendo la sezione che interessa.

Per citare in tesi vale sempre il testo originale e l'analisi completa, mai l'indice o la mappa.

## Come aggiungere una nuova analisi (`NN_*.md` in `03_Analisi Approfondite/`)

1. Leggi la chiusura "Se dovessi condensare…" e scrivi in `01_INDICE_BREVE.md` una riga nuova, con il numero successivo.
2. Assegna una costellazione (A–G) coerente con `00_Indice_Generale_e_Guida_delle_Analisi.md`, sezione 2. Se non ne esiste una adatta, segnalalo invece di inventarla.
3. In `02_MAPPA_CONCETTI.md` aggiungi il numero all'asse che il testo sostiene. Le connessioni nuove vanno scritte come inferenza, a meno che un testo le citi esplicitamente.
4. Se la fonte (PDF) non è in cartella o l'analisi cita un avviso di verifica, scrivilo nella colonna "Avvisi".

## Cosa non è stato fatto e perché

- Il grafo `graphify` non è stato costruito. Il grafo descritto nel vecchio `CLAUDE.md` (`graphify-out/`) non esiste, e la costruzione richiede di far leggere e processare tutte le 24 analisi a un modello: costo alto. Per attivarlo: eseguire la skill graphify su questa cartella, dopo aver deciso se includere anche l'indice.
- L'indice non è generato da uno script: non esiste `aggiorna_indice.py` nel progetto. Gli aggiornamenti sono manuali.

## Regole fisse

- Italiano.
- Mai inventare fonti, citazioni o dati: ogni riferimento va verificato e separato da inferenza o ipotesi.
- Non modificare le analisi originali né `03_AUDIT_TESI.md` senza motivo: è il registro dei problemi aperti.

Aggiunta del 2026-10-19: i file 28–36 sono le ricerche AADRL e Bartlett e le analisi da artifact, con lo stesso schema di nome dei file 01–27. Le analisi da artifact non sono nella serie di indice 01–24.
