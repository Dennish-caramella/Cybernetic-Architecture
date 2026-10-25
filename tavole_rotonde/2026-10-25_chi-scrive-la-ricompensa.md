# Tavola rotonda di prova: chi scrive la ricompensa e i pesi?

Data: 2026-10-25. Stato: **solo round 1** (posizioni indipendenti di dieci voci). Round 2 (confronto) e revisione del `revisore-integrita` non eseguiti; i rilievi di integrità qui sotto sono di chi ha redatto la sintesi, non del revisore. Tutte le voci simulano un punto di vista costruito dalle schede, non gli autori reali. Le schede sono riassunti: ogni `[S:NN]` va verificato sul testo primario.

## Nodo

Nel sistema partecipativo agentico del Report fondativo, chi scrive la funzione di ricompensa e i pesi? Se gli attori scelgono tra soluzioni ma non riscrivono i criteri, il processo è partecipativo (H2)? Il progettista di regole è un autore nascosto?

## Posizioni (sintesi)

| Voce | Posizione | Argomento portante |
|---|---|---|
| Alexander | Oggi li scrive il progettista; autore nascosto salvo visibilità e contestabilità | Le regole servono a escludere configurazioni [S:01]; le 141 variabili di Bawains sono catalogate dall'analista [S:26]. Proposta [I]: ricompensa come "Strategy" sostituibile [S:27] |
| Pask | Senza potere sulle regole è "controllo a senso unico con un menu" | Distinzione linguaggio oggetto / metalinguaggio [S:02]; obiettivo sottospecificato nello stadio 1 [S:03] |
| Negroponte-Steenson | H2 necessaria, non sufficiente | In URBAN5 i criteri erano riscrivibili, ma da un esperto [S:05]; l'agente-maggiordomo sposta i criteri dove non si vedono [S:06] |
| De Carlo-Mari | È consultazione, non potere sulle regole | Rifiuto del "demiurgo" e della chiarezza imposta [S:24]; autoprogettazione adottata dalle élite [S:15] |
| De Graaf-Murphy | Condizione necessaria, non sufficiente | "L'ultima scatola è disegnata in Excel" [S:10]: i pesi sono il nuovo foglio Excel [I] |
| Carpo-Sanchez | Il potere è prima nell'alfabeto delle parti | Euristiche, Handles e iWeights sono criteri incorporati [S:17]; il giocatore non riscrive il gioco [I] |
| MVRDV | Scelta del consumatore, non partecipazione forte | Slider Diversity 0,8→0,2 cambia la configurazione [S:22]; residenti come dati passivi [S:22]; un mouse in Climatizer [S:23] |
| AADRL-Bartlett | La reward la scrive il team; nessun caso in cui la scrivano gli attori | Day 1-2, Oikos, Meta London [S:29-32]; Team Robotic delega a un VLM ma resta il prompt di ruolo [S:33] |
| Agenti-stigmergia | Emergenza dinamica, ma il campo è del progettista | Target feromonici e "feromone della regina" fissi [S:12]; Nash presuppone payoff già scritti |
| Ingegnere edile | Servono vincoli duri non negoziabili separati dai pesi | Luce, accessi, struttura come regole del software [S:19]; giunti, antincendio, catasto aperti [S:19, S:20] |

## Convergenze

1. **H2 è condizione necessaria, non sufficiente** (dieci voci su dieci). Il Report la formula come presenza/assenza del potere di modificare i criteri.
2. **Esistono almeno tre livelli di potere**, che H2 e il Report non distinguono: scegliere tra soluzioni; ritoccare i pesi; aggiungere, togliere o riscrivere i criteri (e l'alfabeto delle parti). Lo dicono con parole diverse Alexander, Pask, De Carlo-Mari, Carpo-Sanchez, MVRDV, Stigmergia. Proposta [I]: estendere SQ2 e la prova P3 a questi tre livelli.
3. **Esporre non basta**: servono canali di modifica, registro delle modifiche e responsabilità di chi scrive le regole di modifica (Pask, Negroponte, Stigmergia, Ingegnere).
4. **Manca una regola di aggregazione dei pesi in conflitto**: teoria della scelta sociale assente dal corpus (lacuna 14 del Report), segnalata da sei voci.

## Contraddizioni e tensioni

- **Vincoli duri contro potere sui criteri.** L'ingegnere chiede di sottrarre alcuni vincoli alla negoziazione; De Carlo-Mari chiede chi decide quali vincoli sono "fisici" e quali politici. Il confine è esso stesso una scelta politica. Tensione aperta, da trattare in tesi.
- **Mediazione tecnica contro assemblea.** De Carlo-Mari riconosce che un sistema leggibile potrebbe dare voce a chi in assemblea non parla [H], ma teme la cooptazione; De Graaf-Murphy teme che chi ha tempo e capitale domini anche con pesi aperti.
- **Reward esplicita contro reward evitata** (AADRL-Bartlett): Team Robotic delega a un VLM, ma la regola resta umana [S:33]. Non risolve il nodo, lo sposta.
- **Emergenza contro legittimità** (Stigmergia): una dinamica robusta non è pluralismo.

## Lacune

- Scelta sociale / aggregazione delle preferenze, scienze sociali della partecipazione [L].
- Chi paga dati e modello dei prezzi (strato 4) [L].
- Nessuna scheda mostra un sistema RL o di gioco in cui gli attori scrivano la ricompensa [L, voce AADRL].
- Norme e valori tecnici: assenti dal corpus; non vanno inventati [L].
- Indicatore operativo di "conversazione" (Pask) [L].

## Avvertenze di integrità (di chi redige, non del revisore)

1. **Convergenza sospetta.** Le dieci voci hanno risposto allo stesso nodo, formulato dentro il quadro del Report e di H2, e leggono in parte le stesse schede e il Report stesso. L'accordo unanime può essere un effetto del prompt, non una prova. Prossimo giro: nodo formulato in modo neutro e almeno una voce con il compito esplicito di difendere la posizione opposta (per esempio, che la mediazione tecnica sia preferibile all'assemblea).
2. Le posizioni sul nodo sono quasi tutte `[I]`: le schede non trattano RL, ricompense né scelta sociale (dichiarato da più voci).
3. Voci che contengono dati segnalati non verificati: percentuali di (w)Ego (75/72%), schede 24 (appunti dell'autore, fonte non in cartella), 12 e 13 (avvisi aperti in `stato_avanzamento.md`).
4. Una voce (Stigmergia) cita il Catalogo come "S:22 via Catalogo, riga 77": riferimento indiretto, da riverificare.

## Decisioni che spettano a Dennis

1. Adottare o no i tre livelli di potere (scegliere / pesi / criteri) come riformulazione di H2 e SQ2.
2. Come trattare i vincoli ingegneristici duri: fuori dalla negoziazione, o negoziabili entro una soglia dichiarata.
3. Se aprire il corpus alla scelta sociale e alla letteratura di scienze sociali sulla partecipazione (nuove fonti, da verificare prima di usarle).
