# Prompt per la sessione Claude sul PC (inventario, senza spostare nulla)

Da incollare in una sessione Claude Code aperta sul PC, nella cartella `Desktop`. Serve finché la sessione cloud non riesce a vedere le cartelle del PC.

---

Lavora in sola lettura. Non spostare, rinominare o cancellare nulla.

Cartelle: `C:\Users\Caredda Dennis\Desktop\TESI` e `C:\Users\Caredda Dennis\Desktop\PROVA PROGETTO`.

1. Per ogni sottocartella di primo e secondo livello: numero di file, dimensione totale, data dell'ultima modifica, tipi di file principali.
2. Trova i doppioni: file con lo stesso hash SHA-256 (indica tutti i percorsi) e file con nome simile ma contenuto diverso (indica date e dimensioni).
3. Classifica ogni cartella in una di queste categorie (vedi `tesi/GESTIONE_FILE.md` nel repo Cybernetic-Architecture, branch `claude/f0-ripartenza`): 1 Fonti (PDF, dati grezzi), 2 Conoscenza (schede, mappe, sintesi), 3 Esperimenti, 4 Decisioni, 5 Archivio. Se non sei sicuro, scrivi "da decidere" e perché.
4. Per `PROVA PROGETTO`: descrivi com'era organizzata la conoscenza e quali criteri usava. Dennis la giudica carica di bias: segnala dove vedi scelte che pesano sugli esiti.
5. Cerca i risultati della pipeline Milano su dati reali del 22/10 (`RAPPORTO_ESECUZIONE.md`, `MANIFEST.csv`, 348 tile glb): se li trovi, scrivi il percorso.
6. Scrivi tutto in `Desktop\TESI\INVENTARIO_PC_<data>.md`, con una tabella per cartella: percorso | categoria proposta | doppione di | motivo.

Alla fine, riassumi in dieci righe cosa terresti e cosa archivieresti, e aspetta l'approvazione di Dennis.
