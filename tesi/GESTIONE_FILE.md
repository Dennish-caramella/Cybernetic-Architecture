# Gestione dei file

## Le cinque categorie (decise il 2026-11-09)

Ogni file appartiene a una sola categoria. Un file che non serve a nessuna delle prime quattro va in archivio, con il motivo.

| Categoria | A cosa serve | Esempi | Dove vive |
|---|---|---|---|
| **1. Fonti** | gli originali, non si toccano mai | PDF dei libri, dati grezzi scaricati | PC (PDF); cloud per i dati, riscaricabili con gli script |
| **2. Conoscenza** | quello che *sappiamo* (secondo cervello) | schede di lettura, schede di caso studio, glossario, mappe, sintesi | repo |
| **3. Esperimenti** | quello che *proviamo* | Spatial Milano Lab, Villaggio Verticale, test con agenti | repo |
| **4. Decisioni** | quello che *abbiamo deciso* e perché | domanda, metodo, calendario, STATO, giornale | repo `tesi/`, `STATO.md`, `giornale/` |
| **5. Archivio** | ciò che è superato, con il motivo | vecchie prove, doppioni, branch | repo `archivio/` |

Ogni esperimento ha una scheda fissa: **ipotesi → dati → esito → cosa ne teniamo**.

Regola per i doppioni: si propone di tenere la versione più recente e completa (a parità, quella già nel repo), ma **ogni scelta viene mostrata a Dennis prima di essere eseguita**.

## Proposta di riordino del repo (DA APPROVARE, niente è stato spostato)

Base di partenza: branch `claude/project-thread-378fa2` (il più completo). Gli altri 8 branch:

| Branch | Contenuto unico rispetto alla base | Proposta | Motivo |
|---|---|---|---|
| `main` | nessuno (solo configurazione) | sostituire con la nuova struttura dopo l'approvazione | era rimasto indietro |
| `project-thread-1d2sxb` | 4 note di ricerca MIT/AADRL/Bartlett (19/10) | archivio | probabile doppione di `secondo_cervello/ricerche/progetti/_archivio_2026-10-19/` (da confermare con un confronto) |
| `project-thread-ct2o4z` | 12 "voci esperte" (`.claude/agents/`), skill `tavola-rotonda`, tavola "chi scrive la ricompensa" | **conoscenza / strumenti**: portare nella base | contiene tutto 4rfan9 più la voce Azadi; le tavole rotonde sono state usate nella riformulazione |
| `project-thread-4rfan9` | sottoinsieme di ct2o4z | archivio | doppione |
| `project-thread-mq0mt0`, `rzorau`, `yfzjy4`, `qhwnx8` | nessuno | archivio (eliminare il branch dopo l'approvazione) | già contenuti nella base |

Cartelle della base:

| Oggi | Categoria | Proposta | Motivo |
|---|---|---|---|
| `secondo_cervello/schede, mappe, modelli, ricerche, tavole_rotonde, metodo` | 2 Conoscenza | tenere così | è il secondo cervello |
| `secondo_cervello/sintesi/` (Report fondativo, Riformulazione, T1, confronti) | 2 Conoscenza | tenere come storia del ragionamento | la decisione corrente sta in `tesi/` |
| `secondo_cervello/fonti/` | 1 Fonti (elenchi) | tenere | elenco dei non versionati e bibliografia consigliata |
| `prove/in_evidenza/2026-10-25_spatial_milano_lab` | 3 Esperimenti | **base della scala urbana**: separare *dati e mappa* (si tiene) da *modelli di analisi* (in attesa della mappa critica) e dal pannello Cooperativa (archivio) | decisione del 09/11 |
| `prove/in_evidenza/2026-10-21_pipeline_milano` | 3 → 5 | **da decidere**: archivio, oppure tenere solo il codice (griglia H3, accessibilità, sensibilità) | superata dai dati del Lab; i risultati su dati reali del 22/10 sono sul PC e non sono stati ritrovati |
| `prove/archivio/*` (gioco, Assemblatore, Bartlett, Abitare Cinisello, arricchimenti) | 5 Archivio | tenere in archivio | già archiviati il 27/10 |
| `archivio_tecnico/` | 5 Archivio | unire in `archivio/` | una sola cartella di archivio |
| `giornale/`, `STATO.md`, `INDEX.md`, `istruzioni_progetto_tesi.md` | 4 Decisioni | tenere; aggiornare le istruzioni (magistrale con rigore PhD) | — |

Artifact su claude.ai:

| Artifact | Proposta |
|---|---|
| Spatial Milano Lab | base scala urbana (senza pannello Cooperativa) |
| Villaggio Verticale Milano | base scala edificio (da recuperare nel repo) |
| Spatial Milano | archivio (superato dal Lab) |
| Parallodge, Adaptive City, Game AI DRL, Game-based growth AA DRL, Benghazi 2050, LinX, Augmented Urban Planning, agente spaziale (LinkedIn), Spatial agent prototipo, Civic Canvas, HousingPrime (3), Stigmergic Space Lab, Laboratorio Bartlett, Modelli matematici (8), Mappa sovrapposizioni (2), Acqua Point Cloud, Assemblatore di tessere, Regole Comuni | conoscenza: schede di caso studio o già schedati (da verificare uno per uno) |
| Albero Conflitti | escluso (decisione del 09/11) |
| Viaggi, cruciverba, Amsterdam, Dutch Design Week | fuori dalla tesi |

## Cartelle del PC
`Desktop\TESI` e `Desktop\PROVA PROGETTO`: stessa procedura quando saranno accessibili da Remote Control. `PROVA PROGETTO` è un tentativo di riorganizzazione che Dennis giudica troppo carico di bias: va letto per capire cosa salvare, non adottato.
