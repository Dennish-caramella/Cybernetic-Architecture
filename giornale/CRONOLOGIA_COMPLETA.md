# Stato di avanzamento della tesi

Aggiornato: 2026-10-19. Questo file è il registro dello stato. Va aggiornato ad ogni sessione di lavoro: una voce datata per ogni cambiamento, senza cancellare le voci precedenti.

## Fase attuale

**Ricerca e sintesi** (come da istruzioni di progetto). La scrittura della tesi è rimandata. Il Report fondativo (basi teoriche e tecniche) non esiste ancora: va redatto.

## Stato del corpus

| Voce | Stato | Note |
|---|---|---|
| Analisi approfondite 01–24 (`03_Analisi Approfondite/`) | 24 presenti, corpo letto integralmente il 2026-10-10 | Tutte con chiusura "Se dovessi condensare". Avvisi di verifica in tabella sotto. |
| Indice 00 (`03_Analisi Approfondite/00_Indice_Generale_e_Guida_delle_Analisi.md`) | Presente, coerente con i file | 24 link relativi a percorsi assoluti `file:///C:/...` (funzionano solo su questo PC) |
| Linee guida di analisi (`00_Istruzioni Progetto/00_Linee_Guida_…`) | Presenti, complete | Metodo di riferimento per ogni nuova analisi |
| Bibliografia (`01_Ricerche Teoriche/bibliografia consigliatra.md`) | Presente | Circa dieci opere senza PDF in cartella |
| PDF teorici (`01_Ricerche Teoriche/`) | 18 PDF corrispondono alle analisi 01–18 | Non aperti: il collegamento è per titolo e autore |
| Materiali MVRDV (`02_MVRDV Research/`) | 368 file, circa 900 MB, in gran parte TIF/EPS | Non letti: binari. Le fonti PDF/PPTX per le analisi 19–23 non sono state aperte |
| `01_Prime considerazioni.md` | Letto integralmente | È una chat, non una fonte. Trattare come ipotesi di progetto |
| Second brain (`00_Schemi e Mappe/Second_Brain_Analisi_Approfondite/`) | Rigenerato il 2026-10-10 | Vedi `00_LEGGIMI_come_aggiornare.md` |

## Avvisi di verifica aperti

1. **Analisi 12 (Meyboom e Reeves, *Stigmergic Space*)**: il `CLAUDE.md` di root dice che le "schede 11–14 (Stigmergic Spaces, Bartlett)" sono state verificate il 2026-10-07 e non corrette, con report in `01_schede/00_verifica/`. La cartella non esiste. Non risulta quale analisi corrisponda alle vecchie schede 11–14. Finché non si recupera il report, i contenuti di 11–14 non vanno usati come fatti.
2. **"Bartlett"**: nel corpus compare come sede accademica (analisi 08 su Carpo, analisi 18 su Koehler con il gruppo RC17). I progetti Horizon, InterX, Civic Canvas e Meta-CLT citati nel `CLAUDE.md` non compaiono in nessun file.
3. **Analisi 24 (De Carlo)**: la fonte non è in cartella (la bibliografia dice che non è disponibile in digitale). Dati bibliografici e cifre del Villaggio Matteotti da verificare.
4. **Dati numerici non verificati nei testi**: percentuali e cifre citate nelle analisi (es. 08: "40% delle emissioni"; 14: quote di reddito e di solitudine; 20: punteggi di soddisfazione 75/72/65/53%; 23: cifre del modello climatico). Da verificare sulle fonti prima di citarli.
5. **Incoerenza interna analisi 13**: la sezione 2 dice "sedici prototipi", le conclusioni "18 prototipi" (il conteggio dei tre tipi dà 18).
6. **Residui di estrazione PDF**: l'analisi 10 contiene in più punti la riga "04_De Graaf, R. _ Four Walls an…". Da ripulire.
7. **Datazione da verificare**: analisi 17 cita *Space is the Machine* di Hillier nel 1989; la bibliografia cita l'edizione 2015.

## Cronologia

- **2026-10-10**: rilettura integrale del corpo delle 24 analisi e dei file di istruzione (sola lettura). Creata questa cartella. Rigenerato il second brain. Aggiornato `CLAUDE.md`.
- **2026-10-10 (precedente)**: audit della struttura, creazione del second brain in prima versione (basato su indici e chiusure, non sul corpo).

## Prossimi passi

1. Recuperare o ricostruire il report di verifica delle "schede 11–14", oppure confermare che non esiste e chiudere l'avviso.
2. Reperire la fonte di De Carlo (analisi 24) o segnalarla come non verificabile in tesi.
3. Verificare le cifre elencate negli avvisi 3–4 sulle fonti PDF.
4. Redigere il Report fondativo in `02_sintesi/` (cartella da creare) a partire dal second brain.
5. Decidere se costruire il grafo (skill graphify) sul second brain: costo di token alto, da autorizzare.

## 2026-10-19 — Arricchimento visivo delle letture (sessione Project thread)

- Prodotti arricchimenti visivi in `tesi_out/arricchimenti/` (vedi `README.md` lì): Alexander SGS, Pask Architectural Relevance, Alexander City, Sanchez Combinatorial Design, Sanchez (intro Commons), Meyboom e Reeves Stigmergic Space, Erioli Assembler. Ogni cartella ha `arricchimento_visivo.md` e `figure/` con le immagini estratte dai PDF e didascalie per pagina.
- Limite: i riassunti completi esistenti stanno sul computer dell'autore, non accessibili dalla sessione. Gli arricchimenti non sostituiscono i riassunti: vanno agganciati alle loro sezioni.
- Non ancora fatti: Koehler, Multi-agent Space Planning, Pask (An Approach to Cybernetics, 68 p.), Mari (Autoprogettazione, 66 p.).
- Avviso aperto: lo Stigmergic Space è attribuito dal PDF alla University of British Columbia, mentre il registro lo indicava come "Bartlett". Da chiarire prima di citare l'affiliazione.
- Diritti: le figure di terzi (Gehry Partners, RBTA, Alexander, Architectural Forum, progetti studenteschi) richiedono credito o permesso prima dell'uso in tesi.

## 2026-10-19 — Ricerca su progetti e pubblicazioni (sessione Project thread)

- Prodotti cinque file `ricerca.md` in `tesi_out/ricerche_progetti/` (vedi `README.md` lì): MIT City Science, AADRL, Shajay Bhooshan, Bartlett RC3/RC10 (Architecture Design), Bartlett RC11/RC14 (Urban Design). Struttura come `arricchimento_visivo.md`, con focus su coefficienti, modelli matematici e di IA.
- Esito: il focus matematico e di IA è documentato solo per MIT City Science (CNN, ABM, regressione lineare di riferimento). Per gli altri quattro argomenti le fonti aperte descrivono i metodi a parole; nessuna formula, peso o soglia verificata.
- Avvisi: il nome corretto è "Bhooshan", non "Booshan" (ZHA CODE: Vishu Bhooshan è un'altra persona). Il nome dell'RC10 Bartlett cambia tra cluster page (Ecocentrism) e show 2026 (AI Tectonics). I titoli RC11/RC14 sono noti solo per 2020/21 e 2024/25.
- Gap aperti: pubblicazioni peer-reviewed di Shajay Bhooshan; articoli AADRL su ACADIA/eCAADe; pubblicazioni 2025–2026; pagine dei singoli progetti Bartlett.
- Aggiornamento 2026-10-19: su richiesta dell'autore, i due file Bartlett sono stati uniti in un unico `03_Bartlett_Autumn_Show/ricerca.md` (Parte A: RC3/RC10; Parte B: RC11/RC14). Restano tre file: MIT City Science, AADRL, Bartlett.

## 2026-10-19 — Cinque artifact Claude Docs salvati e analizzati (sessione Project thread, richiesta di Dennis)

- Salvati in `tesi_out/da_artifact/` cinque file `.md`, con contenuto invariato rispetto agli artifact (letti con il connettore Claude Docs, non con la lettura pagina):
  - `01_AA_DRL_Phase_II_Day1_Bhooshan.md` (UpBridge City, VertiCity)
  - `02_AA_DRL_Phase_II_Day2_Bhooshan_Make_No_Little_Plans.md`
  - `03_AADRL_Oikos_Bhooshan_Studio.md`
  - `04_AADRL_Meta_London_Bhooshan_Studio.md` (contiene un frammento corrotto nell'artifact, segnalato nel file)
  - `05_Team_Robotic_Agentic_Participator.md` (studio Spyropoulos)
- Stato di verifica: tutti e cinque i file sono `da verificare`. Le fonti primarie sono video (trascrizioni lette dall'autore dell'artifact) e il libro Oikos su Issuu, non riaperti in questa sessione. Le formule sono ricostruzioni standard dell'autore dell'artifact: **inferenza**, da controllare sulle fonti prima di citarle.
- Aggiornati: `01_INDICE_BREVE.md` (sezione in fondo, senza rinumerare le analisi 01–24), `02_MAPPA_CONCETTI.md` (sezione datata con convergenze e tensioni).
- Rapporto con `tesi_out/ricerche_progetti/02_AADRL/ricerca.md`: i cinque file sono analisi di singoli progetti; la ricerca AADRL resta la scheda del laboratorio. Le due fonti si completano. Avviso: il file `ricerca.md` indica Spyropoulos come "programme head" (da snippet, `da verificare`), mentre il file Team Robotic lo definisce "direttore del DRL" (dalla trascrizione). Da chiarire prima di scrivere il ruolo in tesi.

### Convergenze e tensioni emerse (inferenza, salvo dove indicato)

- **Il gioco come linea di lavoro (dichiarato dalle fonti):** Oikos (2017–19, giocato da persone) → Meta London (2023–24, regole a mano) → Day 1 e Day 2 (2026, RL e Nash). UpBridge cita Meta London come antecedente.
- **Riduzione degli attori umani (tensione per la tesi):** Oikos ha 80 partite reali; Meta London 4 sviluppatori più un pubblico; i progetti 2026 hanno due agenti. La partecipazione diminuisce man mano che il sistema si fa più ottimizzato.
- **Reward: chi le scrive (tensione di metodo):** Bhooshan chiede reward esplicite (giuria, Day 1 e Day 2); il Team Robotic usa un VLM per evitare reward scritte a mano ("la regola di premi e punizioni è sempre umana", dichiarato). Sono posizioni opposte sullo stesso problema.
- **Ottimizzazione contro apertura (dichiarato):** Team Robotic "non ottimizzare: provare nuove configurazioni"; Bhooshan cerca equilibri win-win. Il confronto è utile per la tesi perché mette in gioco il ruolo dell'architetto come designer di sistemi.
- **Incoerenza interna del Day 2 (rilevata dall'artifact):** il gioco è dichiarato a somma zero (minimax) ma l'esito è "win-win" (Nash a somma non nulla). L'artifact stesso chiede un termine di creazione di valore. Da verificare sul video.
- **Pask come antecedente (dichiarato dal Team Robotic):** Pask è citato come riferimento della "conversazione" come forma di intelligenza. Il corpus ha già `tesi_out/arricchimenti/00_Pask_...`: punto di aggancio, non verificato qui sulla fonte.
- **Auto-organizzazione e stigmergia (inferenza):** la reazione-diffusione del Team Robotic e il sistema di particelle si possono confrontare con la stigmergia di Meyboom e Reeves (analisi 12). Il Team Robotic non cita la stigmergia; il confronto è costruito qui.
- **Parti discrete (inferenza):** gli ottaedri troncati di Oikos e le celle poliedriche del Day 2 si collegano all'asse "Discreto e mereologia" (analisi 08, 09, 17, 18). Il collegamento non è dichiarato dai testi.

### Avvisi e lacune aperte

1. Nessuna delle fonti video è stata riaperta: tutti i minuti citati sono da verificare sul video.
2. Oikos: il testo del libro non è estraibile; le citazioni sono parafrasi delle pagine viste (pp. 9–212 per indice e pagine campione).
3. Meta London: trascrizione di 330 segmenti più descrizione ufficiale, non la trascrizione completa; la tabella sui minuti è incompleta.
4. Biografia di Bhooshan (PhD ETH, insegnamento al DRL dal 2006): dalla pagina ZHA citata, non verificata.
5. Riferimenti nominati e non verificati: Tero et al. (Physarum), Jones (versione ad agenti), Gray-Scott, Cedric Price (Fun Palace), riferimento Stanford sugli agenti generativi, Pask (macchina per insegnare a scrivere). Da reperire prima di ogni citazione in bibliografia.

### Prossimi passi (aggiunti)

1. Riaprire almeno i minuti chiave (6:40 Day 1; 4:43 e 5:13 Day 2; 6:08:30 Team Robotic) per verificare le reward e la somma zero.
2. Decidere quale costellazione assegnare alle nuove analisi (proposta: Oikos in F con G; Meta London in G; Day 1 e Day 2 in E e G; Team Robotic in E). Non assegnata: è una decisione dell'autore.
3. Inserire nel Report fondativo la tensione "riduzione degli attori umani" e "reward: chi le scrive" come domande aperte.

### 2026-10-19 — Second brain e mappa di sovrapposizione (aggiornamento successivo)

- Creato `04_MAPPA_SOVRAPPOSIZIONE.md` nella root: matrice tra le cinque analisi da artifact e il corpus 01–24, con legame (D dichiarato, I inferenza, T tensione) e forza. Gruppi per asse e cinque tensioni per il Report fondativo.
- Aggiornato `00_LEGGIMI_come_aggiornare.md` con il nuovo file e la nota sulle analisi da artifact.
- Tensione più rilevante emersa dalla mappa: Koehler (18, "dalla partizione alla partecipazione") contro il Day 2, che divide la lastra top-down per densità. Da verificare prima di usarla come critica.

### 2026-10-19 — Riallineamento con la cartella TESI e archivio Bartlett

- Dalla cartella TESI sul computer (collegata per la lettura) risultano più recenti del materiale in project-files: `00_Avanzamento/stato_avanzamento.md` (aggiornato al 2026-10-18), analisi 26 (Alexander, *Notes on the Synthesis of Form*) e 27 (Gamma et al., *Design Patterns*), più la analisi 25 (Witt) già presente. Il grafo `graphify` sulle analisi risulta costruito il 2026-10-18 (`00_Schemi e Mappe/Second_Brain_Analisi_Approfondite/graphify-out/`).
- Aggiunte in `01_INDICE_BREVE.md` le righe 25, 26, 27 con costellazione **proposta** (C, A, D), da confermare. Aggiunta in `02_MAPPA_CONCETTI.md` una sezione datata per le tre analisi.
- **Bartlett:** nella cartella TESI del computer non risulta un file separato di analisi o riflessioni Bartlett (la cartella di primo livello contiene `01_Ricerche Teoriche`, `03_Analisi Approfondite`, `00_Avanzamento`, `00_Schemi e Mappe`, `02_MVRDV Research`). I file Bartlett disponibili sono `tesi_out/ricerche_progetti/03_Bartlett_Autumn_Show/ricerca.md` e la prima versione combinata. In attesa di indicazione dell'autore su dove si trovino le "riflessioni" Bartlett.
- **Archivio:** la prima versione combinata MIT/AADRL/Bartlett (`ricerche/mit_aadrl_bartlett/`) è stata spostata in `tesi_out/ricerche_progetti/_archivio_2026-10-19/`, con README. Non eliminata. La cartella `ricerche/` di primo livello non esiste più.
- **Da chiarire:** `tesi_out/ricerche_progetti/` contiene anche `03_Shajay_Bhooshan/`, non citata nel README della cartella (che parla di tre file). Da decidere se è una quarta ricerca o un duplicato.

### 2026-10-19 — Ricerche Bartlett RC10 e RC14 salvate e indicizzate

- Salvati in `tesi_out/ricerche_progetti/03_Bartlett_Autumn_Show/` due file di lettura, testo verbatim della versione incollata da Dennis nel project chat:
  - `RC10_AI_Tectonics_modelli_AI_e_matematici.md` (RC10, 2021–2026, 20 progetti, circa 120 tavole). Ricerca di lettura, non fonte primaria.
  - `RC14_Urban_Design_modelli_AI_e_matematici.md` (RC14, 2020–2026, 32 progetti letti su 34).
- Il messaggio RC10 e il messaggio RC14 sono stati letti per intero dalla chat prima di salvarli.
- Aggiornati `01_INDICE_BREVE.md` (sezione "Ricerche Bartlett"), `02_MAPPA_CONCETTI.md` (sezione datata ter) e `04_MAPPA_SOVRAPPOSIZIONE.md` (sezione 5, due tensioni nuove).
- Tensioni nuove per il Report fondativo: "dati o giocatori" (RC14 contro Oikos) e "leggere o generare" (RC14 contro RC10). Tutte inferenze, da verificare sulle pagine di progetto.
- Restano da incollare nel project chat i testi RC3 e RC11 della ricerca Bartlett. RC14 è ora salvato come file separato; la sua versione dentro `ricerca.md` (Parte B) non è stata toccata.
- Restano aperti i punti del 2026-10-19 sulla cartella TESI: `03_Shajay_Bhooshan/` (quarta ricerca o duplicato) e il ruolo di Spyropoulos.

### 2026-10-19 — Copia completa delle analisi dal computer (richiesta di Dennis)

- Copiati nel progetto tutti i 28 file `.md` di `TESI/03_Analisi Approfondite/` in `/mnt/project-files/03_Analisi Approfondite/`: l'indice `00_Indice_Generale_e_Guida_delle_Analisi.md` e le analisi `01`–`27`. Lettura solo dal computer, nessun file del computer modificato.
- La cartella del computer contiene anche `graphify-out/`, non copiata perché non è un file `.md` di analisi.
- Costellazione della 27 (Gamma et al.) corretta da D a **A**, come nell'indice 00 del computer. La 26 è in A, la 25 in C (già così).
- `00_LEGGIMI_come_aggiornare.md` ora dice che la cartella contiene 01–27 più l'indice.
- Da decidere: `tesi_out/25_Witt_Architecture_Automata_and_Artificial_Memory_Riassunto_Dettagliato_Completo.md` è una copia precedente della 25 (33.300 byte), più vecchia di quella del computer (33.086 byte). Non l'ho eliminata. Va tenuta o rimossa dopo conferma.
- Le analisi 01–24 nella cartella del progetto ora sono quelle del computer del 2026-10-19. Non ho confrontato il contenuto con le versioni del 2026-10-10 usate per gli indici; se cambiano, va riaggiornato `01_INDICE_BREVE.md`.

### 2026-10-19 — File AADRL e Bartlett aggiunti alla cartella delle analisi (richiesta di Dennis)

- Aggiunti a `03_Analisi Approfondite/` nel progetto e nel computer (`TESI\03_Analisi Approfondite\`), come copie nuove senza sovrascritture: 9 file.
  - AADRL: `AADRL_ricerca_modelli_matematici.md` (da `ricerche_progetti/02_AADRL/ricerca.md`); cinque analisi da artifact `AADRL_DRL_Phase_II_Day1_Bhooshan.md`, `AADRL_DRL_Phase_II_Day2_Make_No_Little_Plans.md`, `AADRL_Oikos_Bhooshan_Studio.md`, `AADRL_Meta_London_Bhooshan_Studio.md`, `AADRL_Team_Robotic_Agentic_Participator.md`.
  - Bartlett: `Bartlett_ricerca_RC3_RC10_RC11_RC14.md` (ricerca combinata), `Bartlett_RC10_AI_Tectonics_modelli_AI_e_matematici.md`, `Bartlett_RC14_Urban_Design_modelli_AI_e_matematici.md`.
- Le versioni originali restano in `tesi_out/`; le copie nella cartella delle analisi sono copie, non spostamenti.
- Nel computer la cartella `03_Analisi Approfondite` contiene già i 28 file `.md` della serie 00–27; il progetto li mostrava già dal 2026-10-19 e non era la stessa vista. Se Dennis non li vede, il problema è nella vista, non nei file.

### 2026-10-19 — Nomenclatura delle aggiunte AADRL e Bartlett (richiesta di Dennis)

- I nove file aggiunti sono numerati 28–36 e seguono lo schema `NN_Autore_Titolo_Riassunto_Dettagliato_Completo.md`, come i file 00–27. Lo stesso nome è nel progetto e nel computer.
  - 28 AADRL ricerca; 29–33 AADRL analisi da artifact; 34 Bartlett ricerca combinata; 35 RC10; 36 RC14.
- Sul computer restano i nove file con il nome provvisorio `AADRL_*` e `Bartlett_*`, copiati prima. Non posso cancellarli con gli strumenti disponibili. Vanno eliminati a mano, sono copie.
- Il contenuto non è stato modificato, solo i nomi. Le versioni originali restano in `tesi_out/`.

### 2026-10-20 — Cronistoria e correlazioni tra modelli teorici (richiesta di Dennis)

- Nuovo file `tesi_out/ricerche_teoriche/Cronistoria_e_correlazioni_modelli.md`: otto capitoli su Bertalanffy, Ashby, vicinato di von Neumann e di Moore, Nash, Bogost, Husserl (Smith e Mulligan), correlazioni trasversali, lacune.
- Base: due passate di ricerca verificata (`wcvx37469` del 2026-10-19, `w2ewgvgos` del 2026-10-20). Affermazioni marcate C, C-s, I, L, R, D secondo la verifica.
- Il rapporto tra von Neumann e Moore, e tra Nash e gli automi cellulari, non è documentato da fonti verificate: resta lacuna.
- Da fare: leggere i testi primari elencati nel file; risolvere la discrepanza bibliografica su Smith e Mulligan (Topoi vol. 3 o 2(1)); verificare il legame tra Unit Operations di Sanchez (analisi 09) e Bogost.

## 2026-10-20 — Primo tool di prova: Bartlett (sessione Project thread)

- Richiesta di Dennis: tool interattivi per testare e confrontare i modelli delle analisi. Piano proposto in `tesi_out/tool_prova/README.md` con quattro famiglie in ordine: Bartlett, AADRL, MVRDV, modelli matematico-filosofici.
- Prototipo Bartlett in `tesi_out/tool_prova/bartlett/index.html` (pubblicato come artifact "Laboratorio Bartlett"). Tre moduli:
  1. Combinatoria: 9 × 24 = 216 contro 303 dichiarate in TetrAgora. Lo scarto non è spiegato nella fonte.
  2. Regole locali: agenti con regola R/L stile Langton, 800 agenti come dato di fonte, regola e griglia di esempio.
  3. Pesi e grafo: due piante di esempio, regole di adiacenza ✓/✗ e indice con pesi impostabili. Definizioni di grado, articolazione e piano terra sono inferenze del tool.
- Esito atteso dal modulo 3: con β = 0 le due piante pareggiano; con β alto vince B. È una dipendenza dai pesi, non un risultato sperimentale.
- Avvisi: le formule Bartlett riportate in analisi 34 (CSI, Σρ·V) non hanno parametri reperiti; il tool non le implementa. Le regole di Langton non sono quelle di TetrAgora, che non le riporta.
- Non fatto: AADRL, MVRDV, modelli matematico-filosofici. `tesi_out/ricerche_teoriche/` non è in questa cartella di progetto: va verificata la presenza prima di lavorarci.

## 2026-10-20 — Tool Assembler (richiesta di Dennis)

- Dennis ha chiesto di abbandonare gli esempi Bartlett e di replicare un tool come [co-de-iT Assembler](https://www.co-de-it.com/assembler.html), aggiornandolo con metodi nuovi.
- Fonti lette: pagina co-de-iT (blog, 15.06.2022) e README del repository GitHub Co-de-iT/Assembler (licenza GPL-3.0). Né l'una né l'altra descrive l'algoritmo, le strategie, le formule o i parametri. Il Notion di documentazione non è leggibile dal sistema. Il repository non è stato letto a livello di codice.
- Quindi la replica è una implementazione nostra dei concetti dichiarati (parti, regole di connessione, criteri di crescita, metriche locali e globali). Le strategie e le metriche sono proposte, da marcare come tali in tesi.
- Tool in `tesi_out/tool_prova/assemblatore/index.html` (artifact "Assemblatore di tessere"). Cinque strategie: casuale, attrattore, campo scalare, minima entropia, partecipativa con pesi di tre portatori. Confronto su più semi con copertura, compattezza, diversità e celle bloccate.
- Verifiche fatte: sintassi dello script; test della sola logica in Node (20 semi per strategia): nessuna adiacenza con porte incompatibili. Non verificata l'interfaccia in browser.
- Il prototipo Bartlett in `tesi_out/tool_prova/bartlett/` è superato e resta solo come archivio.
- Da fare: leggere il codice del repository Assembler (licenza GPL-3.0, da considerare prima di riutilizzare codice) e definire le strategie nuove con il materiale delle analisi.

## 2026-10-20 — Catalogo unico dei modelli (richiesta di Dennis)

- File: `tesi_out/ricerche_teoriche/Catalogo_modelli.md`. Raccoglie i modelli matematici, filosofici, economici e di IA di tutte le analisi 00-36 e dei quattro file di `ricerche_teoriche/`. Sono organizzati per famiglia, con formula o coefficienti dove la fonte li riporta, il file in cui compaiono, la fonte originale e lo stato [V]/[S]/[I]/[L]. In fondo ci sono un indice incrociato per fonte e una sezione di lacune.
- Per il catalogo non ho riaperto PDF né video: lo stato di ogni voce è quello dei file di analisi.
- Discrepanze trovate tra i file (sezione 6 del catalogo):
  1. Le pagine di Ashby (pp. 125-126 e 202) sono [V] nello Studio ma risultano non lette nelle Verifiche. Nel catalogo sono [S].
  2. "Only variety can destroy variety" va ancora controllata sul testo.
  3. La definizione di unit operation che l'analisi 09 attribuisce a Bogost tramite Sanchez coincide quasi con la formulazione scartata nella Cronistoria.
  4. Le formule delle analisi 29-33 sono ricostruzioni, non formule dei team.
- Prossimo passo utile: leggere `TESI/02_MVRDV Research/4 FUNCTIONMIXER/1 technology OptiMixer2_14/OptiMixer2_14.pdf`, che può dare i pesi e i parametri di OptiMixer, e le pp. 121-125 e 202-213 di Ashby 1956.

## 2026-10-20 — Cartella 04_Fondamenta Matematiche (richiesta di Dennis)

- Creata su `C:\Users\Caredda Dennis\Desktop\TESI\04_Fondamenta Matematiche\` con 7 file: `Atlante_Critico_Modelli.md` (testo incollato da Dennis, senza modifiche di contenuto; decodificate solo le entità HTML del passaggio), `README.md` (elenco file e lista di controllo), e le cinque analisi già prodotte (`Catalogo_modelli.md`, `Studio_modelli_con_esempi.md`, `Cronistoria_e_correlazioni_modelli.md`, `Analisi_approfondite_per_teoria.md`, `Verifiche_testi_primari.md`).
- Copie verificate sul disco: dimensioni e presenza confermate con un elenco della cartella.
- Nota: la copia di riferimento delle analisi è in `tesi_out/ricerche_teoriche/`; la cartella sul disco è una copia.
- Nel README sono elencate come da verificare le attribuzioni dell'Atlante, in particolare Nash 1950/1951 (Kakutani/Brouwer), Bertalanffy (equifinalità), Ashby (pagine), Alexander (min-cut e formula), Tero et al., le percentuali (w)Ego e gli URL della sezione 8, che non sono stati aperti.
- Il testo dell'Atlante non è stato corretto: le correzioni vanno in un file separato.
- Non fatto: verifica degli URL; lettura di Ashby pp. 121–126 e 202–213; lettura di Nash 1950.
- Nota sul device: la cartella `00_Avanzamento\stato_avanzamento.md` sul disco di Dennis non è stata aggiornata; questa modifica è solo nel file di progetto.

### 2026-10-25 — Augmented Urban Planning (Azadi, TU/e): scheda 37, deep research, nuova voce (richiesta di Dennis)

- La pagina indicata è il record di una **tesi di dottorato** (S. Azadi, TU/e, conferita il 23-09-2026), non di un articolo. Testo integrale sotto embargo fino al 23-09-2027: nessuna lettura del testo completo.
- Prodotti in `03_Analisi Approfondite/`: `37_Azadi_Augmented_Urban_Planning_Riassunto_Dettagliato_Completo.md` (scheda, livello abstract e articoli collegati), `37_Augmented_Urban_Planning_Deep_Research.md` (UDT, IA e deliberazione, strumenti, contesto italiano) e `37_note_ricerca_grezze/` (tre note in inglese con etichette [V]/[U]).
- Nel repository: voce `azadi-pianificazione-aumentata` in `.claude/agents/` (PR sul ramo della PR #2), aggiunta all'elenco della skill `tavola-rotonda`.
- Da fare: leggere i PDF ad accesso aperto degli articoli (Environment and Planning B; CUPUM su OSF); SSRN; verificare DOI e cifre di Tessler et al.; contesto italiano (L.R. 18/2019, PGT, OMI, ISTAT) con fonti primarie; canone di teoria della pianificazione non verificato.
- Non aggiornati `01_INDICE_BREVE.md` e `02_MAPPA_CONCETTI.md` (la costellazione della 37 è decisione di Dennis).

---

## Appendice: voci presenti solo in altre copie del registro (non erano nella copia da 25 KB)

Fonti: `archivio_tecnico/stato_avanzamento_copie/`. Riportate senza modifiche.

- **2026-10-22 (pipeline Milano su dati reali, tesi su partecipazione e IA: prova tecnica, non parte del Report fondativo)**: eseguita la pipeline `05_Urbanistica/pipeline_milano` su dati reali del Comune di Milano e OpenStreetMap, senza LLM. Scaricate e registrate (URL, data, licenza CC-BY 4.0, sha256 in `data_raw/originali/MANIFEST.csv`): NIL PGT 2030, famiglie e popolazione per NIL (ds1440, ds27, 2025), zone e quotazioni OMI 2024/2 (ds1996, ds2938), DBT 2020 SHP (unità volumetriche con altezza). Risultati: 1.911 celle H3 res 9; K = 4 (silhouette 0,450), varianza PC1–PC3 82,5%, stabilità bootstrap ARI media 0,952; 370 lotti candidati; sensibilità Spearman 0,932 (res 8) e 0,988 (res 10). Limiti dichiarati: vincolo protetto derivato da OSM (esclude 587 celle), nessun PGT né vincolo idraulico ufficiale, nessun reddito per NIL, lotto da 1,9 km² probabilmente ferroviario, canone obiettivo 8,0 €/m²/mese ancora non giustificato. Modello 3D: 348 tile glb in OGC 3D Tiles 1.0 e viewer CesiumJS in `viewer/cesium/`, verificato solo numericamente (il render nel browser di sessione non è stato controllato). Dettagli in `05_Urbanistica/pipeline_milano/RAPPORTO_ESECUZIONE.md`. Non toccati `00_Schemi e Mappe` né i file del grafo.

- **2026-10-21 (pipeline Milano, senza LLM)**: scritta e collaudata la pipeline in `05_Urbanistica/pipeline_milano/` (griglia H3, interpolazione areale, accessibilità pedonale su grafo, PCA e K-Means con validazione, idoneità multicriterio con pesi e sensibilità, lotti candidati, viewer 2D/3D). 6 test di calcolo passano; esecuzione completa su dati SINTETICI in pochi secondi. **Mai eseguita su dati reali**: la sessione non raggiungeva i portali dei dati. Da fare sul computer dell'autore: scaricare le fonti, compilare le colonne in `config/sources.yaml`, eseguire. Lettura critica dei documenti Orchestratore, Pipeline e Modelli ZHA/MIT in `00_Avanzamento/02_sintesi/LETTURA_CRITICA_FASE_1_MILANO.md` (se presente) con i punti da correggere: risultati scritti prima dell'analisi, agenti LLM che muovono i pesi, T1 attribuito ad Alexander, fonti non verificabili.
