# Decisioni di impianto

Registro delle decisioni di direzione. Ogni voce: data, decisione, perché. Le decisioni nuove si aggiungono in fondo; quelle superate si barrano, non si cancellano.

## 2026-11-09 — Ripartenza (intervista di impianto con Claude)

### Natura e livello
- **Tesi magistrale con rigore da dottorato.** Era stata dichiarata "dottorato, un anno" il 27/10; corretto: è una tesi magistrale, ma condotta con metodo di ricerca di livello PhD, sperimentando il più possibile con l'IA.
- **Obiettivo oltre la tesi:** progetto concreto di vita e pubblicazioni scientifiche sulle scoperte e sul metodo. Pubblicare durante o dopo la tesi è indifferente.
- **Laurea entro i primi mesi del 2028.** Mezzi e policy di ateneo: nessun vincolo segnalato.

### Visione (parole di Dennis, riassunte)
La crisi abitativa di Milano. Sulla curva gaussiana, agli estremi stanno i poveri (compito primario della politica) e i ricchi (i clienti degli architetti, che hanno perso il contatto con la realtà dell'architettura, cioè le persone). La tesi guarda alla "pancia": persone comuni. Obiettivo: un nuovo modello di vivere comune che superi le politiche economiche dei developer, usando IA (LLM, RL, agenti) per ridurre il divario tra le persone. Riferimenti: Sanchez, Koehler, Philippe Morel; la cibernetica e l'utopia sociale degli anni '70; il vivere comune del villaggio verticale (MVRDV) e della città di Jane Jacobs; edifici che crescono come città medievali.

### Domanda di ricerca (bozza di base, da raffinare)
Vedi `tesi/DOMANDA_DI_RICERCA.md`. Formula: scelta (c) — **il metodo è il contributo scientifico, il progetto su un caso reale ne è la prova.**

### Struttura
- **Due scale in sequenza, un caso continuo:** (1) scala urbana: il sistema produce una serie di lotti; le persone, in base alle loro esigenze, scelgono tra i lotti; (2) scala edificio: sui lotti trovati si sviluppa un esempio di edificio.
- **Individui → gruppi → lotti.** Il vivere comune richiede gruppi; i gruppi **non** devono essere omogenei (niente ghetti di interessi uguali): mix di età e di condizioni. Come rendere operativa la diversità: si decide quando si lavora concretamente (rinviato).
- **Prima agenti, poi test reale.** Il sistema deve prima funzionare con agenti simulati; il test con persone reali ("la grande prova") viene dopo. Scelta del partner: rinviata a quando il sistema funziona.
- **Modello economico:** il più vicino possibile alla realtà e all'uso.

### Basi da tenere
- **Scala urbana:** artifact *Spatial Milano Lab* (https://claude.ai/artifact/LHHSCseATyEEmS4g7SoTW5) come infrastruttura di dati e mappa (NIL, strati, shapefile, metadati, lotti candidati), **senza** il pannello "Cooperativa ed edificio" (anticipava la scala edificio).
- **Scala edificio:** artifact *Villaggio Verticale Milano* (https://claude.ai/artifact/C6XKorgUEPVhNLztQWnhCR) resta base, da affrontare a suo tempo.
- **Modelli di analisi del Lab** (domanda, audit PGT, portafogli, SMAA, PU): non entrano come risultati. Prima una mappa critica: cosa sono, cosa dimostrano, e quali alternative consolidate o di frontiera esistono.

### Conoscenza
- Tutto ciò che è stato analizzato (schede, artifact di analisi) entra nel secondo cervello come conoscenza condivisa, **tranne l'artifact "Albero Conflitti"**.
- Nuove letture da verificare e schedare: Philippe Morel, Yona Friedman, Cybersyn (Beer/Medina), Jane Jacobs, i link di `bibliografia_consigliata.md` (pagine Notion e Box).

### Gestione dei file
- Cinque categorie (vedi `tesi/GESTIONE_FILE.md`). Ogni scelta su cosa tenere o archiviare va **comunicata a Dennis prima di essere eseguita**; prima si chiarisce a cosa serve ogni file.
- Il riordino riguarda repo e cartelle del PC (`Desktop\TESI`, `Desktop\PROVA PROGETTO`). Accesso al PC: via Remote Control dell'app Claude desktop (da aggiornare).

### Calcolo
- In cloud. Rete dell'ambiente sbloccata il 2026-11-09 per i portali dati (Comune di Milano, Regione Lombardia, ISTAT, Agenzia Entrate, MEF, Overpass) e per Notion e Box.

## 2026-11-10 — Allocazione: raccomandazione spiegabile + matching con scelta (sostituisce "individui → gruppi → lotti")

- **Decisione:** individui → lotti → comunità sul lotto. Ogni famiglia ha un vettore dei desideri (ancore di lavoro, scuola e cura; pesi sui criteri; budget). Il sistema propone i lotti migliori spiegando il perché; la famiglia sceglie; l'assegnazione usa l'accettazione differita con riserve di capacità per categoria; il feedback aggiorna solo i pesi della famiglia, le regole comuni cambiano solo per decisione collettiva.
- **Niente veto di ingresso** tra persone (scartata la stabilità individuale come regola d'ingresso): rischio di esclusione e discriminazione, e nessuna stabilità garantita con più di due tipi di famiglia. Dopo l'assegnazione: fase di conoscenza e uscita libera senza penalità.
- **Diversità** senza imposizione tra persone: raggruppamento per esigenze di luogo (non per somiglianza personale) e riserve di capacità sul lotto.
- **Perché, e confronto con gli approcci esistenti:** `tesi/CONFRONTO_APPROCCI_ALLOCAZIONE.md`. La scelta va dimostrata empiricamente con un confronto pre-registrato tra sette approcci (B0–B6) su popolazioni simulate, poi con un contrasto su persone reali in F2.
- **Chiarito:** il confronto economico cooperativa/developer va tarato su casi reali e riportato come gap fondiario ΔL (regione di parametri), non come stima puntuale.

## 2026-11-14 — Regole della Base L v6 (decisioni di Dennis sui punti del revisore, ticket #38)

- **Stato di attuazione degli ambiti (C9) non esclude nessun lotto.** Tutti i lotti restano disponibili, qualunque sia la fase (A, B, C, D, N). La fase di ogni lotto si registra come attributo, per l'analisi successiva. Per noi oggi un lotto disponibile conta come libero. Motivo: la tesi può essere attuata dopo, e così non si perdono lotti rispetto ad altre fonti.
- **Nessun controllo umano sulla dipendenza dei codificatori.** Non è richiesto.
- **Aree designate dal PGT come riuso o simili (GFU, ambiti di trasformazione) sono lotti edificabili.** Non sono più area di attivazione né "destinazione ignota".
- **Lotti da riusare: non si va oltre le informazioni disponibili.** Vuoti urbani con recinzioni o muri di confine e, all'interno, sterbaglia o terreno abbandonato, si riconoscono anche da immagini satellitari e si segnalano come **possibile area con potenziale** (attributo, non nuova classe).
- **Progetti in stato avanzato o in costruzione** diventano **tessuto urbano consolidato**: contesto su cui basare le analisi, non lotti disponibili.

Nota di metodo [I]: queste regole cambiano i criteri dopo aver visto l'esito di C9 e della revisione. Il protocollo (§6) vieta modifiche dopo l'esecuzione. Quindi la v6 va come nuova prova: nuova pre-registrazione su git prima di qualsiasi esecuzione, con la motivazione e il riferimento a v5 e alla revisione. v5 resta come prova documentata con esito "cambia".
