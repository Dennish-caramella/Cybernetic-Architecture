# Riformulazione come progetto di dottorato: dal tool di screening all'architetto come designer di sistemi

**Stato:** bozza di impianto scientifico, non un capitolo di tesi. Idee e scrittura finale restano di Dennis.
**Data:** 2026-10-25
**Autore del documento:** il modello orchestratore, nel ruolo di dottorando esterno. Le posizioni delle "voci" sono simulazioni di competenze costruite dalle schede del corpus, non gli autori reali.
**Base:** `REPORT_FONDATIVO.md` (H1-H4, assi 1-6), `T1_protocollo_negoziazione.md`, `LETTURA_CRITICA_FASE_1_MILANO.md`, `pipeline_milano/` (README e config), `stato_avanzamento.md`, e una tavola rotonda di otto voci del team (vedi §9).

**Marche** (come nel Report): **[S]** riportato da una scheda del corpus (le schede sono riassunti, non fonti primarie); **[I]** inferenza mia; **[H]** ipotesi da verificare; **[L]** lacuna. Nessuna fonte esterna al corpus è stata aperta per questo documento (la scheda 37 su Azadi è parte del corpus ma si basa su abstract): tutto ciò che non sta nelle schede è [I] o [L].

**Integrazione AUP (aggiunta il 2026-10-25, dopo la tavola rotonda):** la scheda 37 (Azadi, *Augmented Urban Planning*, tesi PhD TU/e 2026) è stata letta solo a livello di scheda, non il testo integrale (sotto embargo fino al 23-09-2027). Le voci della tavola rotonda **non** l'hanno vista. Vedi §11.

---

## 0. In breve

1. **L'idea di partenza è difendibile, ma non nella forma in cui è formulata.** La frase "un ente terzo che estrae le esigenze reali" è il punto su cui le voci attaccano con più forza (tutte e otto le risposte, in `tavole_rotonde/2026-10-25_riformulazione-phd.md`, lo toccano, con accenti diversi; l'accordo è anche effetto delle stesse schede, vedi §8.7). Un'esigenza non si estrae: si costruisce attraverso un modello di osservazione, un catalogo di variabili e dei pesi, e chi li scrive decide prima delle persone. Le schede 02 (l'osservatore è partecipante), 22 (la soggettività passa a monte, nella formula) e 26 (il catalogo di 141 variabili è costruito dall'esperto) lo sostengono in parte; il passaggio all'"esigenza" del tool è [I].
2. **Proposta di riformulazione.** Il contributo del dottorato non è "scoprire i bisogni veri", ma **rendere la funzione di valutazione dei lotti pubblica, riscrivibile dagli abitanti e verificabile**, e misurare quanto e come cambiano le graduatorie quando cambia chi scrive i criteri. L'apprendimento dalle scelte diventa un secondo livello, con audit dei bias, non la promessa centrale. [I]
3. **Fase 1 è il nucleo del dottorato. Fase 2 è un secondo progetto.** Sette voci su otto, in forma più o meno forte, dubitano che la Fase 2 discenda dalla Fase 1 (Carpo-Sanchez ritiene che reggerebbe con un ponte, vedi §8.4): la Fase 1 sceglie *dove*, la Fase 2 riguarda *come* si compone e *chi* costruisce. Resta un solo ponte plausibile (un campo di vincoli per lotto che alimenta un sistema di parti) ed è da trattare come esperimento esplorativo, non come conseguenza. [I; voci]
4. **Oggi non esiste nessuna evidenza.** La pipeline di Milano non è mai stata eseguita su dati reali e il costo del suolo e il FAR non sono modellati [S: pipeline_milano/README, config]. Il primo passo non è la teoria: è far girare lo screening su un quartiere reale e farlo verificare da un tecnico.
5. **Un dottorato, non una tesi magistrale.** Per una magistrale basterebbe la Fase 1 ridotta (screening + T1). Il dottorato ha senso solo se include dati reali, persone reali, un disegno di studio e un'etica della ricerca. Questo è anche il rischio maggiore: il progetto richiede competenze (urbanistica, scienze sociali, data science, scelta sociale) che il corpus non contiene [L].

---

## 1. Che cosa cambia rispetto al Report fondativo

Il Report (2026-10-20) chiede: *in che misura un sistema multi-attore può rendere visibili e discutibili i compromessi, senza che il modello diventi il decisore nascosto?* Quella domanda resta valida. La riformulazione ne restringe l'oggetto e ne amplia il contesto:

| Aspetto | Report fondativo | Riformulazione dottorato |
|---|---|---|
| Oggetto | sistema partecipativo agentico, scala urbana come caso | tool di screening e valutazione di lotti per social housing, con elicitazione e apprendimento dalle scelte |
| Caso | quartiere ipotetico o reale, da scegliere | comune reale (Milano come caso già avviato) |
| Attori nelle prove | profili di scenario (T1) | scenario in T1, poi persone reali con approvazione etica |
| Ruolo del modello | mediatore con pesi esposti | mediatore con pesi esposti **e** aggiornato dalle scelte, con audit |
| Fase costruttiva | assi 3 e 6 (discreto, ingegneria) | Fase 2 separata, con un solo ponte sperimentale |
| Tesi | l'architetto come progettista di regole negoziabili | invariata, ma spostata da "regole" a "chi può riscrivere i criteri" |

Le quattro ipotesi H1-H4 restano e diventano il **banco di prova di base** (§5). Le nuove ipotesi H5-H8 coprono ciò che la riformulazione aggiunge: catalogo di variabili, apprendimento dalle scelte, bias di campione, verificabilità dei lotti.

---

## 2. Il problema, in due livelli

**Livello politico-abitativo (la motivazione).** Dennis parte dall'emergenza abitativa delle persone nella "pancia" della curva gaussiana, lasciata a politiche abitative guidate dal profitto dei developer. Nel corpus, la "belly" e i Commons come terzo settore accanto a pubblico e privato sono in Sanchez [S: scheda 11]. Lo stesso testo lega i Commons a infrastrutture precise (copyleft, registri distribuiti) e al ruolo dei cittadini come co-produttori [S:11].

**Livello metodologico (il problema di ricerca).** Un tool che propone lotti e impara dalle scelte solleva tre problemi che il corpus conosce bene e la formulazione di partenza non risolve:

- *Chi definisce le esigenze?* Alexander: scegliere le variabili è già la decisione di progetto [S:26]. De Carlo: chi decide cosa è "superfluo" e cosa "necessario"? Il rischio è un "Uomo Tipo" statistico [S:24]. Pask: l'osservatore è un partecipante, non una telecamera neutra [S:02].
- *Chi scrive i pesi?* MVRDV: la soggettività del progettista passa a monte, nella formula [S:22]. Un "ente terzo" è chi scrive i λ [I].
- *Chi si approprierà del risultato?* De Graaf: la figura dell'architetto è economicamente reattiva, e il "carisma" è sapere in assenza di sapere [S:10]. Una mappa dei lotti fa risparmiare ricerca soprattutto a chi ha già capitale [I].

Una nota sul termine **"ente terzo"**. Suggerisco di abbandonarlo. Nei termini di Pask non esiste un osservatore esterno neutro [S:02], e nei termini del Report un "terzo" che decide è il rischio 1 (mediazione che diventa decisione nascosta). Proposta: **"modello di mediazione con osservatore dichiarato"**, cioè un sistema che dice chi lo ha scritto, con quali dati e con quali variabili. [I]

---

## 3. Domanda di ricerca e sottodomande

### 3.1 Domanda principale (proposta)

> In che misura un sistema di screening e valutazione di lotti per social housing, con catalogo di criteri, pesi e vincoli pubblici e riscrivibili da chi abita, produce esiti diversi da quelli ottenuti con criteri fissati da un esperto, e a quali condizioni la differenza riflette esigenze degli abitanti anziché bias di selezione e di rappresentazione?

Perché questa e non "il modello impara le esigenze reali": la formulazione di partenza afferma un risultato che non si può provare (il bisogno non è osservabile direttamente), mentre quella proposta si misura: la sensibilità degli esiti a chi scrive i criteri, e la qualità dell'apprendimento rispetto a una linea di base. [I]

### 3.2 Sottodomande

- **SQ-A (esigenze).** Come si distinguono bisogno dichiarato, rivelato, osservato e adattato in una scelta tra lotti, e quale dato osservato (non dichiarato) misura la domanda abitativa a scala comunale? [I; lacuna delle scienze sociali: §8]
- **SQ-B (catalogo).** Quanto cambiano i lotti selezionati quando il catalogo di variabili è scritto da gruppi diversi (tecnici, residenti, amministrazione)? [I, da Alexander: scheda 26]
- **SQ-C (apprendimento).** Un modello aggiornato sulle scelte motivate prevede le scelte di persone non viste meglio di una linea di base (pesi uniformi o pesi dell'esperto)? [H]
- **SQ-D (bias).** In che modo un campione auto-selezionato o parziale sposta i pesi appresi, e chi manca dal tavolo? [I, da De Carlo: scheda 24; Report §6]
- **SQ-E (verificabilità).** Quanti dei lotti proposti sopravvivono a una verifica tecnica indipendente (FAR, vincoli, proprietà, bonifica) e con quale livello di approssimazione dichiarato? [I, da Report asse 6]
- **SQ-F (ponte, esplorativa).** Un campo di vincoli per lotto può alimentare un sistema di parti ricombinabili, e gli abitanti producono configurazioni distinte e non equivalenti? [I, da Sanchez ed Erioli: schede 09 e 17]

---

## 4. Definizioni operative (da fissare prima di ogni prova)

Il Report segnala la lacuna L1 (definizione di partecipazione). Per il dottorato servono almeno queste definizioni, da scrivere in un glossario unico (`second_brain_v3/01_GLOSSARIO.md` non è stato letto qui [L]).

**Esigenza abitativa.** Nessuna delle voci ha trovato nelle schede un modo di misurarla. Proposta di quattro livelli, da raccogliere separatamente e non mescolare:

| Livello | Che cosa è | Esempio di dato | Rischio |
|---|---|---|---|
| Dichiarata | quello che la persona dice di volere | questionario, motivazione testuale | desiderabilità sociale, aspirazione |
| Rivelata | quello che la persona sceglie tra opzioni date | scelta tra lotti proposti | eredita il filtro di chi ha scelto le opzioni |
| Osservata | quello che i dati mostrano senza chiedere | affitti, sfratti, liste d'attesa, redditi, tempi di spostamento | dati assenti per chi è fuori dai registri |
| Adattata | quello che la persona accetta perché non ha alternative | non osservabile direttamente | confonde accettazione e preferenza |

Il bisogno "reale" non coincide con nessuno dei quattro. È un costrutto, e va dichiarato come tale. Mari mostra che chi ha bisogno può rifiutare ciò che non riconosce come proprio [S:15]; De Carlo, che l'abitante può preferire la "villetta convenzionale" e che a Terni servì un processo faticoso di educazione reciproca [S:24]. [I]

**Partecipazione.** Livello minimo di potere: sulle scelte (selezione tra lotti), sui criteri (pesi e vincoli) o sul catalogo (aggiungere o togliere una variabile). Il dottorato assume che la partecipazione sia reale solo dal secondo livello in su (H2 del Report). [I]

**Funzione di aggregazione.** Come si combinano le scelte di più persone in un'unica graduatoria è una scelta politica, non solo tecnica. Il corpus non contiene teoria della scelta sociale [L] e la lettura critica di Fase 1 lo segnala già. Va colmata prima di qualunque modello di apprendimento.

**Lotto.** Una cella H3 di livello 9 (circa 10 ettari) non è un lotto [S: pipeline_milano/README]. Il lotto è un poligono con proprietà, vincoli e indice. Le celle descrivono il contorno.

---

## 5. Ipotesi falsificabili

H1-H4 sono quelle del Report (§3.2) e restano identiche. H5-H9 sono nuove. Tutte le soglie numeriche vanno fissate **prima** della prova, come richiede T1.

| # | Ipotesi | Falsificata se | Scheda o voce di origine dell'idea |
|---|---|---|---|
| H1 | Esporre i pesi e renderli modificabili cambia il fronte non dominato | il fronte resta invariato o cambia solo per caso | MVRDV, T1 |
| H2 | Il processo è partecipativo solo se gli attori modificano i criteri, non solo scelgono | nessuno propone modifiche ai criteri | De Carlo, MVRDV, Pask |
| H3 | Il sistema riduce il costo di esplorazione dei compromessi rispetto al processo manuale | tempo o qualità non migliorano rispetto a P1 | Report |
| H4 | Un modello con vincoli dichiarati e verificati non produce scarti sistematici alla revisione tecnica | i vincoli mancanti producono scarti sistematici | Ingegnere |
| **H5** (catalogo) | Cataloghi di variabili scritti da gruppi diversi selezionano lotti sensibilmente diversi | i lotti top-N coincidono oltre una soglia fissata ex ante | Alexander |
| **H6** (apprendimento) | Un modello aggiornato sulle scelte motivate prevede scelte di persone non viste meglio della linea di base | su un campione di controllo non supera pesi uniformi e pesi esperto | AADRL-Bartlett, Pask |
| **H7** (bias) | I pesi appresi da un campione auto-selezionato differiscono da quelli di un campione stratificato | non emerge alcuna differenza misurabile (esito informativo, da riportare) | De Carlo, AADRL-Bartlett |
| **H8** (screening) | Una quota rilevante dei top-N lotti sopravvive alla verifica tecnica indipendente | la quota sotto una soglia fissata ex ante cade per vincoli assenti nel modello | Ingegnere, De Graaf |
| **H9** (ponte, esplorativa) | Un alfabeto di parti per un lotto reale produce, con abitanti reali, configurazioni distinte e non equivalenti | le configurazioni risultano equivalenti, e Fase 2 cade | Carpo-Sanchez |

Nota del revisore: le formulazioni qui sopra sono ancora **non operative** (soglie, metriche, numerosità, relazione di equivalenza per H9 non definite; H5 è quasi tautologica senza una misura del rumore entro il gruppo; H7 non ha un'ipotesi nulla falsificabile; H2 non ha controllo). Vanno riscritte in F0 con una soglia calibrata ex ante e un test dichiarato. Le formulazioni migliorate proposte: H5 falsificata se l'indice di Jaccard dei top-N tra gruppi supera una soglia calibrata sulla variabilità test-retest dentro il gruppo; H6 con metrica (log-loss o accuratezza sulle scelte), margine minimo e numerosità; H7 con distanza minima tra pesi e test statistico; H8 separando tasso di sopravvivenza sotto soglia e causa identificata; H9 con una relazione di equivalenza operativa tra configurazioni (es. distanza o isomorfismo di grafo). [H]

Criterio di lettura: H5 e H8 **non dipendono** dal fatto che i dati dei bisogni siano buoni. Sono prove sul sistema e sul processo, non sulla verità dei bisogni. È per questo che sono il nucleo del dottorato. [I]

---

## 6. Metodo e fasi

Le fasi seguono l'ordine che Dennis aveva già indicato (verificare il cuore, poi ingegnerizzare) e corrette dalla lettura critica di Fase 1. Le durate non sono stimate: dipendono dalla disponibilità dei dati e dell'approvazione etica. [L]

**F0. Chiusura delle definizioni e delle fonti.**
Glossario unico (PAI, rent gap, velocità, K, lotto); fonti dei numeri datate e verificate; definizione dei quattro livelli di esigenza; revisione di scelta sociale e di scienze sociali sulla partecipazione. Output: un documento che chiude gli avvisi aperti del Report (§7, tabella delle lacune) e un registro fonti `verificata` / `da verificare`.

**F1a. Screening su dati reali.**
Eseguire `pipeline_milano` su un quartiere o su Milano intera con dati verificati. Compilare `sources.yaml` aprendo i file reali e non indovinando i nomi delle colonne. Far verificare a mano a un tecnico un campione di lotti (FAR, vincoli, proprietà, bonifica); la numerosità è [L] e va giustificata, per esempio con un intervallo di confidenza sul tasso di sopravvivenza (la prima stima di lavoro di 5-10 lotti è un ordine di grandezza senza giustificazione statistica). Output: tasso di sopravvivenza dei lotti (H8) e test di sensibilità alla risoluzione e ai pesi. Se il tasso è basso, la Fase 1 si riscrive prima di andare avanti.

**F1b. Protocollo di negoziazione (T1) con scenari.**
Eseguire T1 con profili di scenario dichiarati finti (residente, sviluppatore, comune, gestore). Misurare M1-M4. Verifica di H1, H2, H3. Output: baseline per il confronto con l'apprendimento.

**F1c. Elicitazione con persone reali.**
Con approvazione etica e trattamento dati conforme alla normativa sulla protezione dei dati (richiesto dall'ateneo; i dettagli vanno verificati con l'ufficio competente [L]). Le persone vedono i lotti con criteri e pesi visibili e **possono modificarli**; le motivazioni testuali sono raccolte come discorso e codificate da persone, non usate come etichette di addestramento. Campione stratificato contro campione auto-selezionato (H7). Output: dati per H2, H5, H6, H7.

**F1d. Apprendimento con audit.**
Modello di aggiornamento dei pesi dalle scelte, con tutte le versioni dei pesi tracciate e visibili. Linea di base: pesi uniformi e pesi dell'esperto. Validazione su persone non viste (H6). Il modello **non decide**: propone aggiornamenti che le persone possono accettare o rifiutare. Se l'apprendimento rende i pesi meno visibili, contraddice H2 (obiezione dell'MVRDV): quindi pesi appresi ammessi solo come proposta. [I]

**F2 (esplorativa, opzionale).**
Un solo lotto reale o ipotetico, un solo alfabeto di parti, un solo dettaglio costruttivo con calcolo dichiarato (giunto o partizione acustica). Il campo di vincoli per lotto (FAR, costo, esposizione) viene dalla Fase 1. Obiettivo: H9, non un progetto completo. Gli strumenti candidati (grafi come nel Bartlett RC10, mereologia) restano da sperimentare passo passo, come dice Dennis.

### 6.1 Su `pipeline_milano` come base

Giudizio: **buono come scheletro, nullo come evidenza.** [I]

| Elemento | Giudizio |
|---|---|
| Griglia H3, interpolazione areale, accessibilità, WLC con pesi esposti, sensibilità (Dirichlet), Pareto, esportazione, test sintetici | riutilizzabili; allineati con H1 |
| Mai eseguita su dati reali; `col: null` in tutte le fonti | nessun risultato esiste [S: README] |
| Costo del suolo = prezzo OMI di zona (proxy), nessun bilancio, FAR `null` | il vincolo "costo, FAR, coefficienti" della proposta di Dennis oggi non è modellato [S: README, pipeline.yaml] |
| Lotti da OSM (`landuse` dismessi/ferroviari) | includono aree attive; nessun controllo di proprietà, bonifica, indice [S: README] |
| PCA + K-Means | utile come esplorazione, **non** come criterio di scelta; K deciso dai dati; già segnalato il doppio conteggio con la WLC [S: LETTURA_CRITICA, punti 1-2] |
| Quattro criteri e quattro pesi di partenza | decisi dall'autore; vanno resi contestabili (H2) |
| Mancano | dati di proprietà (catastali), modello di domanda abitativa, modello di costo di costruzione, traccia delle versioni dei pesi, aggregazione di più persone |

---

## 7. Rischi e lacune

| Rischio | Descrizione | Mitigazione |
|---|---|---|
| R1. Mediazione che diventa decisione | il modello fissa catalogo e pesi, le persone scelgono tra opzioni già filtrate | H2, H5; catalogo e pesi riscrivibili; tracciabilità |
| R2. Apprendimento che nasconde i pesi | pesi appresi meno visibili dei pesi dichiarati | pesi appresi solo come proposta; audit |
| R3. Media che nasconde le minoranze | "la pancia" è la maggioranza; chi non lascia tracce non c'è | H7; campione stratificato; aggregazione che protegga le minoranze (da studiare) |
| R4. Partecipazione di facciata | consultazione su opzioni già formulate (cooptazione) | misurare chi cambia i criteri, non chi sceglie |
| R5. Lavoro non pagato | le persone alimentano il modello con lavoro di elicitazione | compensazione, uso e proprietà dei dati e del modello dichiarati (commons) |
| R6. Dati assenti | nessun dato verificato; reddito alla scala NIL forse non esiste | F1a prima di tutto; segnalare ogni dato mancante |
| R7. Ambito eccessivo | due fasi, quattro discipline, persone reali | Fase 2 esplorativa; scheda dei limiti |
| R8. Credibilità ingegneristica | Fase 2 peggiora giunti, acustica, antincendio, costi [S: schede 19, 20] | un solo dettaglio costruttivo con calcolo; altrimenti rinviare |
| R9. Appropriazione | una mappa dei lotti serve prima a chi ha capitale | licenza aperta e commons by design; soggetto istituzionale (§10) |

**Lacune strutturali** [L]: scienze sociali sulla partecipazione e sull'elicitazione; teoria della scelta sociale; urbanistica italiana (PGT, oneri, edilizia convenzionata e sociale); modelli di prezzo e costo; strumenti validati per misurare soddisfazione e partecipazione; dati di proprietà dei lotti; etica della ricerca con persone.

---

## 8. Critica severa delle voci

Le citazioni sono parafrasi dalle risposte delle voci; ogni voce ha un punto cieco dichiarato. Le obiezioni sono ordinate per la forza con cui si ripetono, non per gravità.

### 8.1 Chi definisce le "esigenze reali" (voci riportate: Pask, Alexander, De Carlo, MVRDV)

- **Pask.** Un ente terzo che estrae le esigenze è l'osservatore esterno distaccato che la scheda dà come superato; le esigenze sono costruite dal modello di osservazione [S:02; I].
- **Alexander.** Il catalogo delle variabili è già la forma; nell'esempio del villaggio le 141 variabili sono catalogate dall'esperto. Alexander mette in guardia dalle astrazioni facili che modellano solo il misurabile [S:01]; che gli indici *need/access/transform/feasib* della pipeline siano un caso di questo è [I].
- **De Carlo.** Un modello che estrae esigenze da dati aggregati è un Uomo Tipo 2.0 [S:24; I].
- **MVRDV.** Il bisogno non si estrae, si negozia con criteri e pesi dichiarati. [S:22] riporta che spostare il peso di *Diversity* cambia l'esito; il resto è [I].

### 8.2 Bias dell'apprendimento dalle preferenze

- Chi sceglie tra lotti già filtrati eredita il filtro: chi scrive il filtro decide prima delle persone [I; AADRL-Bartlett, Carpo-Sanchez].
- Un apprendimento che segue le scelte medie codifica conformismo (la "villetta convenzionale") [S:24, fonte di De Carlo non disponibile: avviso 3 dello stato; I].
- Le preferenze dichiarate e rivelate incorporano aspirazione e adattamento. [S:15] riporta il rifiuto, da parte di un pubblico operaio, di oggetti "ben disegnati" che non riconosce come propri; estendere il punto a chi cerca casa è [I].
- Il carisma retorico: in (w)Ego, nel *Trading Game* vince chi ha più carisma; "scegliere e dire perché" può riprodurre il vantaggio retorico [S:20; I].
- I satisfaction score di (w)Ego (75/72/65/53%) vengono da studenti in ruolo e non sono verificati: non sono dati di preferenza utilizzabili [S:20; avviso 4 dello stato].
- [S:20] documenta omogeneità nelle immagini prodotte dagli utenti; che le piattaforme producano desideri omogenei è [I].

### 8.3 Dati

- Non esiste alcun risultato reale: la pipeline è collaudata solo su sintetici [S: README].
- Le schede non contengono dati abitativi, catastali, di prezzo o di PGT italiano [L; Ingegnere, AADRL-Bartlett, MVRDV, Alexander].
- Il reddito alla scala di sezione potrebbe non esistere; OMI sono intervalli stimati, non transazioni [S: README].

### 8.4 Rapporto Fase 1 – Fase 2

Convergenza di otto voci su otto: **la Fase 2 non segue dalla Fase 1.**

- *Alexander*: la Fase 2 è un kit di parti con regole; la scelta di un lotto no. Il ponte è assente [I; L].
- *Pask*: la Fase 1 restringe l'obiettivo a monte, la Fase 2 lo lascia sottospecificato; la seconda contraddice la prima [S:03; I].
- *De Carlo*: sono due regimi di potere distinti; Terni fu deliberazione lunga con tempi assembleari in conflitto con l'urgenza [S:24, da verificare sul libro].
- *Ingegnere*: salto da pianificazione a progettazione costruttiva senza ponte tecnico [I].
- *De Graaf-Murphy*: manca un soggetto istituzionale (ente pubblico, cooperativa) che passi dal tool alla costruzione [I].
- *Carpo-Sanchez*: reggerebbe se la Fase 1 restituisse per ogni lotto un campo di vincoli leggibile da un sistema combinatorio [I; ispirato a Erioli, il cui campo (Field) come vincolo è in S:17, ma Erioli non tratta lotti].
- *AADRL-Bartlett*: per UpBridge e VertiCity il flusso gioco→forma è lineare [S:29]; la successione Oikos → Meta London → UpBridge è cronologia [S:31]; che la costruzione non retroagisca sul gioco in generale è [I].
- *MVRDV*: HouseMaker/VillageMaker è scelta del consumatore, non governance [S:19].

### 8.5 Fattibilità e scopo

- Per un dottorato regge la Fase 1; la Fase 2 è un secondo progetto [AADRL-Bartlett, Ingegnere, MVRDV].
- Secondo Bhooshan, per VertiCity un ciclo gioco→dati→forma richiedeva in passato un anno con tre persone per scala [S:29]; estenderlo ad altri contesti è [I].
- La Fase 2 autocostruita peggiora giunti sismici, antincendio, impianti, acustica e costo/m² [S:19, 20; I].
- Mancano finanziatore, proprietario e garante pubblico [De Graaf-Murphy; I].

### 8.6 Dove le voci non sono d'accordo

- *Cosa salvare della Fase 1.* MVRDV: strumento di negoziazione con pesi in vista, non estrattore di bisogni. AADRL-Bartlett: un gioco con reward pubblica e contestabile, non un oracolo. Alexander: un sistema generativo di parti e regole, non un ottimizzatore di lotti. Sono tre ricostruzioni diverse dello stesso nucleo; la scelta spetta a Dennis (§12).
- *Ottimizzare o no.* Il ranking WLC/Pareto "che indica i migliori" ricade nel mito tecnocratico (Carpo-Sanchez, schede 09 e 11); il Report e MVRDV lo tengono come strumento se i pesi sono visibili. [I]
- *Se l'apprendimento serve.* Pask: oggi è feedback unilaterale, non conversazione. AADRL-Bartlett: apprendere preferenze rivelate in un gioco è legittimo se dichiarato. Alexander: dentro un catalogo chiuso la macchina non scopre bisogni nuovi. [I]

### 8.7 Cautela sul consenso

Le otto voci hanno letto in larga parte le stesse schede e lo stesso Report. La convergenza è in buona parte una convergenza di fonti, non un'indipendenza di prove: va letta come indicazione dei punti dove la tesi è più esposta, non come verifica. Il revisore (§9) riprende il punto.

---

## 9. Procedura e revisione di integrità

**Tavola rotonda.** Otto voci del team (PR #2, `.claude/agents/`): `decarlo-mari-partecipazione`, `degraaf-murphy-potere`, `ingegnere-edile`, `mvrdv-negoziazione`, `aadrl-bartlett-agenti`, `carpo-sanchez-discreto`, `pask-cibernetica`, `alexander-sistemi`. Un solo round: ogni voce ha ricevuto solo il nodo (formulato in questo documento al §3), non le posizioni delle altre. **Non è stato fatto il round 2 di confronto.** Le domande che le voci si sono poste a vicenda (§12) restano senza risposta. Non hanno partecipato `negroponte-steenson` e `agenti-stigmergia`, e non c'è nessuna voce di scienze sociali, di urbanistica, di dati o di scelta sociale: lo hanno detto più voci (lacuna del team, non solo del corpus).

**Revisione di integrità.** Vedi §13. Le risposte integrali delle voci sono in `tavole_rotonde/2026-10-25_riformulazione-phd.md`.

---

## 10. Il ruolo dell'architetto come designer di sistemi

Questo documento non scrive la tesi, ma la riformulazione deve dire dove sta l'architetto. Due posizioni delle voci, in tensione:

- **L'architetto è l'autore del catalogo e dei criteri minimi di qualità** (sole, aria, soglie tecniche). De Carlo chiede: *chi fissa il criterio di qualità? È soglia minima o gatekeeping?* [S:24; I]. Per Pask, il designer è il "controllo del controllo" in un obiettivo sottospecificato [S:03].
- **L'architetto non può essere il demiurgo travestito.** Il rischio è che il designer di sistemi sia l'autore nascosto di tutto (De Graaf: carisma; De Carlo: architetto-demiurgo) [S:10, 24; I].

Proposta di lavoro [H]: separare tre livelli di scrittura delle regole, con tre responsabilità diverse: (1) *soglie minime di qualità* (tecniche, non negoziabili, dichiarate dal designer e verificate dall'ingegnere); (2) *criteri e pesi* (riscrivibili dagli abitanti, H2); (3) *catalogo di variabili* (apribile a proposte delle persone e dell'amministrazione, H5). Così il designer di sistemi risponde di (1) e rende contestabili (2) e (3).

Un soggetto istituzionale (ente pubblico, cooperativa, fondazione) che porti il progetto oltre il tool è un requisito per la Fase 2, e il corpus non lo discute [L].

---

## 11. Integrazioni in arrivo e punti aperti

1. **Azadi, *Augmented Urban Planning* (scheda 37 e file di deep research).** Fonte: tesi di dottorato di S. Azadi, TU/e, 2026. Il testo integrale è sotto embargo fino al 23-09-2027: la scheda si basa sull'abstract del record TU/e e su abstract di articoli collegati; la corrispondenza articolo-capitolo è inferenza [S: scheda 37, avviso di integrità]. Che cosa ne ricavo per la riformulazione:
   - **Vocabolario e griglia di valutazione.** Le tre dimensioni dell'AUP (*Interdisciplinary Integration*, *Consensual Contextualization*, *Procedural Operationalization*) offrono una griglia per rendere verificabile lo strumento, senza fornire un metodo di selezione dei lotti [S:37; I]. Possono diventare criteri di valutazione di processo accanto a H1-H9 (es. il tool si innesta in un processo decisionale reale? rappresenta punti di vista diversi?). [H]
   - **Contrappeso sul chi partecipa.** Il workshop AUP coinvolge 12 stakeholder esperti su densificazione del centro di Eindhoven, non residenti [S:37, abstract CUPUM]. Questo conferma, dal lato della letteratura, l'obiezione di De Carlo: la domanda "chi entra nel processo" non è risolta dai digital twin.
   - **Possibile spazio di originalità.** Nella letteratura verificata dalla scheda non risulta un sistema in cui le scelte dei residenti tra lotti riaddestrino il modello [S:37, 'Rilevanza']. **Non è una prova di novità**: la ricerca si è limitata a quanto raggiungibile (testo integrale e molti PDF non aperti), e un'assenza di risultati non è assenza dell'oggetto. Prima di rivendicare originalità serve una rassegna sistematica dedicata (preference learning in urbanistica partecipativa, PPGIS, *participatory digital twins*). [L]
   - **Cautela sulla corrispondenza.** L'AUP non dichiara un ciclo di apprendimento; il DKG è una struttura di conoscenza, non un modello predittivo [S:37]. Quindi AUP non è il concorrente diretto dell'apprendimento da scelte, ma è l'antecedente più vicino sul versante processo/partecipazione.
   - **Ruolo nell'impianto.** Suggerisco di usarla come ancoraggio teorico di Fase 1 per il lato "digital twin partecipativo" e di non basare nulla su dettagli del testo integrale finché non è accessibile.
2. **Letture da aggiungere** (oltre all'AUP) (nessuna è nel corpus, nessuna è verificata): scienze sociali sulla partecipazione e metodi di elicitazione; scelta sociale e aggregazione che protegga le minoranze; urbanistica italiana e social housing; modelli di prezzo e costo. Vanno cercate e verificate prima di entrare in bibliografia.
3. **Ashby, pp. 121-126 e 202-213**, e le citazioni di De Carlo: ancora da leggere sui testi primari (avvisi 3 e 4 dello stato).
4. **Glossario unico** (PAI, rent gap, velocità, K, lotto): da scrivere in F0.

---

## 12. Decisioni che spettano a Dennis

1. **Che cosa è il contributo.** (a) la funzione di valutazione pubblica e riscrivibile (MVRDV, scelta più sicura); (b) il gioco con reward contestabile (AADRL-Bartlett); (c) il sistema generativo di parti e regole (Alexander, Carpo-Sanchez). Raccomando (a) come nucleo, perché è l'unico che si prova con i dati che ci sono. [I]
2. **Fase 2: separata o ponte?** Raccomando di separarla come secondo progetto e di tenere solo H9 come esperimento esplorativo. [I]
3. **Persone reali.** Il dottorato regge solo con persone reali e approvazione etica; se non si possono avere, l'ambito torna a una magistrale (screening + T1 + scenari).
4. **Apprendimento.** Tenerlo come pesi *proposti* e visibili (raccomandato), o rinunciare ad "apprendere" come tesi?
5. **Licenza e commons.** Dati, modello e lotti saranno beni comuni nel senso di Sanchez [S:11]? Se sì, serve una licenza aperta e una scelta di governo. Se no, la differenza con un servizio per developer è solo retorica. [I]

Domande che le voci si sono poste a vicenda e che restano aperte: chi può aggiungere o togliere una variabile dal catalogo; se "belly della curva" è un target statistico o un soggetto politico con voce propria; quali lotti hanno proprietari pubblici e quali sono acquistabili a costo sociale; come si protegge una minoranza nell'aggregazione.

---

## 13. Revisione di integrità

Revisione condotta dalla voce `revisore-integrita` (un agente che ha riletto 16 schede, il README di pipeline_milano, il Report, T1, la lettura critica e lo stato). Esito: **il documento non regge ancora come base** senza le correzioni qui indicate; quelle testuali sono state applicate (marche [S] ridotte a ciò che la scheda dice, conteggi corretti, §8.4-8.5 riscritti). Restano aperti:

1. **Round 2 non fatto.** Le voci hanno letto le stesse schede e il nodo era formulato dall'orchestratore: la convergenza è in parte circolare. Chiusura: round 2 con voci diverse (scienze sociali, urbanistica, dati, scelta sociale non esistono nel team) oppure riesame a campione di tutte le [S] riportate dalle voci. Le [S] delle voci sono state ricontrollate dal revisore solo in parte.
2. **Nessuna evidenza a favore.** Sono state sentite voci critiche. Non è stata cercata evidenza che sostenga la proposta, per esempio Oikos [S:31], dove persone reali giocano e i dati alimentano le regole.
3. **Ipotesi H5-H9 non operative** (vedi nota nel §5).
4. **Dati di De Carlo (scheda 24)** da verificare sul libro prima di ogni citazione (avviso 3 dello stato).
5. **Integrazione AUP fatta dopo la tavola rotonda e dopo la revisione:** il §11 punto 1 non è stato visto né dalle voci né dal revisore. Rivendicazione di originalità da non fare senza rassegna dedicata.
