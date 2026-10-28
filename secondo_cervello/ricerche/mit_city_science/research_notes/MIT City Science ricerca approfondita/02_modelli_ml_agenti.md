# Modelli ML, ad agenti e di scelta del MIT City Science Group

Data: 2026-10-27. Lingua: italiano.

**AVVERTENZA CRITICA SUL METODO.** Nessun PDF e' stato scaricato. Tutti gli host primari (arxiv.org, ifaamas.csc.liv.ac.uk, dspace.mit.edu, media.mit.edu, mdpi.com) rispondono 403 al CONNECT del proxy di policy (verificato con curl e con /__agentproxy/status; non aggirato). Le uniche letture possibili sono state via WebFetch, che restituisce un riassunto prodotto da un modello, non il testo. Quindi **nessuna fonte ha stato `verificata` (PDF intero letto)**. Stati usati: `parziale` = riassunto WebFetch del documento (o della pagina) ottenuto in questa sessione; `da verificare` = non aperto. Le cifre riportate sotto sono quelle del riassunto e vanno ricontrollate sul PDF prima di citarle in tesi. Legenda: [V*] = presente nel riassunto WebFetch del documento (non letto direttamente); [I] inferenza; [H] ipotesi.

## Fonti

| # | Autori, anno | Titolo | Sede | URL / DOI | Stato |
|---|---|---|---|---|---|
| A | Zhang Y., Grignard A., Lyons K., Aubuchon A., Larson K., 2018 | Real-time Machine Learning Prediction of an Agent-Based Model for Urban Decision-making (extended abstract) | AAMAS 2018, pp. 2171-2173 | https://ifaamas.csc.liv.ac.uk/Proceedings/aamas2018/pdfs/p2171.pdf (DOI non trovato) | parziale (riassunto del testo, PDF non scaricabile) |
| B | Zhang Y., 2017 | CityMatrix: an urban decision support system augmented by artificial intelligence | Tesi S.M., MIT Media Arts and Sciences (rel. K. Larson) | https://dspace.mit.edu/handle/1721.1/114059 ; PDF indicato dalla pagina: https://dspace.mit.edu/bitstreams/7ed7bb51-c235-415e-a29a-2590026c1870/download | parziale (solo abstract; PDF non recuperato: errore del fetch) |
| C | Hu K. et al., 2025 | Graph RAG as Human Choice Model: Building a Data-Driven Mobility Agent with Preference Chain | arXiv:2508.16172 (preprint) | https://arxiv.org/pdf/2508.16172 | parziale (riassunto del testo integrale; non peer-reviewed) |
| D | Doorley R., Noyman A., Sakai Y., Larson K., 2019 | What's your MoCho? Real-time Mode Choice Prediction Using Discrete Choice Models and a HCI Platform | UrbComp, SIGKDD 2019 | https://www-prod.media.mit.edu/publications/mocho-paper/ (nessun DOI/PDF sulla pagina); codice https://github.com/CityScope/CS_choiceModels | parziale (solo pagina/abstract) |
| E | Noyman A. (Larson K.), 2019 (data pagina 1 giu 2019) | Deep Image of the City: A Generative Approach to Urban-Design Visualization | pagina pubblicazione MIT Media Lab; la citazione "Noyman e Larson 2020, Symposium on Simulation for Architecture and Urban Design" e' dal riassunto precedente, NON confermata qui | https://www.media.mit.edu/publications/deep-image-of-the-city-a-generative-approach-to-urban-design-visualization/ | parziale (solo pagina); autori/sede/anno **in conflitto** tra pagina (solo Noyman, 2019) e citazione del corpus |
| F | Grignard A., Alonso L., Taillandier P., Gaudou B., Nguyen-Huu T., Gruel W., Larson K., 2018 | The Impact of New Mobility Modes on a City: A Generic Approach Using ABM | ICCS 2018, Springer, pp. 272-280 | https://www.media.mit.edu/publications/the-impact-of-new-mobility-modes-on-a-city-a-generic-approach-using-abm/ (DOI non trovato) | parziale (solo abstract/pagina) |
| G | GAMA platform docs; altre pubblicazioni GAMA di Grignard | - | - | non consultate | da verificare |

## 1. CNN come surrogato di un ABM (Zhang et al. 2018; tesi Zhang 2017)

### Takeaway
Nell'extended abstract una CNN a tre strati convoluzionali, addestrata su 10.000 configurazioni simulate in GAMA (7.000 train / 3.000 test), riproduce il traffico per cella con R^2 0,86 (regressione lineare 0,571) in meno di 10 ms contro circa 1 minuto della simulazione. La validazione e' interamente rispetto al simulatore stesso: nessun confronto con dati reali emerge dal riassunto, quindi si tratta di un surrogato di un modello non validato empiricamente (per quanto letto).

### Cited Findings
- Architettura: CNN con "soli tre strati convoluzionali", TensorFlow/Keras; non indicati filtri, kernel, pooling, strati densi, attivazioni [V*] — fonte A.
- Input 19x19x2 (configurazione urbana su griglia); output: volume di traffico per cella stradale, mostrato come heatmap [V*] — A.
- Dati: 10.000 configurazioni simulate con GAMA (ABM del traffico), 7.000 training e 3.000 test; generazione in 18 ore su otto computer [V*] — A.
- Metriche: R^2 migliore della CNN 0,86; regressione lineare 0,571; obiettivo dichiarato R^2 0,8; confronto visivo ABM vs predizione per quattro città (Fig. 3) [V*] — A. Il riassunto non chiarisce se R^2 sia su test o su train.
- Iperparametri (learning rate, ottimizzatore, loss, batch, epoche) non riportati; si dice solo che piu' modelli e combinazioni di feature sono stati provati "senza overfitting" [V*] — A.
- Validazione: ground truth = output GAMA, confronto numerico (R^2) e visivo; nessuna cross-validation menzionata [V*] — A.
- Prestazioni: inferenza < 10 ms vs ~1 minuto per simulazione ABM [V*] — A.
- Assunzione del simulatore: tutti gli spostamenti avvengono con un sistema di mobilita' condivisa con veicoli autonomi, ipotesi che limita la generalizzazione [V*] — A.
- Valutazione utente: cinque test pilota con 20 utenti in totale; ottimizzazione dei suggerimenti con ricerca casuale sulle mosse [V*] — A.
- Tesi: CityMatrix e' un sistema di supporto alle decisioni con interfaccia tangibile, feedback in tempo reale su piu' obiettivi, suggerimenti AI; ML per predire le simulazioni, algoritmi di ricerca per ottimizzare; pilot con volontari con/senza suggerimenti AI "giudicati positivi" [V*, solo abstract] — B. Il testo integrale (architettura, dati, R^2 della tesi) NON e' stato letto.

### Inferenze
- [I] La risposta alla domanda "e' un surrogato di un modello non validato?": per quanto riportato in A, si', la fedelta' e' misurata solo contro GAMA; la validita' del surrogato non implica quella del modello di traffico. Va verificato nella tesi B se l'ABM e' calibrato su dati reali.
- [I] Generalizzazione: il test set proviene dalla stessa distribuzione di configurazioni (griglia 19x19, stesse regole); l'assenza di test fuori distribuzione e la dimensione contenuta del dataset suggeriscono prudenza. La distinzione "quattro citta'" in Fig. 3 non chiarisce se siano configurazioni fuori training.
- [H] Un R^2 di 0,86 puo' nascondere errori locali rilevanti (es. su celle di congestione); il riassunto non discute i residui.

### Gaps
- PDF di A e B non scaricabili (403 / errore fetch): architettura dettagliata, iperparametri, split, uso di R^2, tesi completa non verificati.
- Non noto se l'ABM di Zhang sia validato su dati reali.

## 2. Modelli ad agenti in GAMA, MoCho, Graph RAG, Deep Image of the City

### Takeaway
Quattro filoni eterogenei: ABM generico di mobilita' in GAMA (Cambridge), modelli a scelta discreta calibrati su survey (MoCho), agente LLM + Graph RAG come modello di scelta modale a pochi dati (preprint, valutato su dati Replica), e una DCGAN per rendering di street-view (non un modello di scelta). Dei quattro, solo C ha dettagli metodologici ricavati dal testo integrale (via riassunto).

### Cited Findings
- F: modello ABM generico su GAMA con piu' modalita' di trasporto, profili di persone, congestione e pattern di traffico; applicato a Cambridge. La pagina non riporta dati di input ne' procedura di validazione [V*] — F.
- D (MoCho): modelli a scelta discreta per la scelta modale, calibrati con dati di indagine; input caratteristiche individuali e attributi delle alternative; interfaccia CityScope tangibile con ricalcolo in tempo reale; istanza 2018 per l'area di Boston, sito di ~14 acri a Kendall Square, Cambridge (MA). Il modello e' detto "ben adattato" e i parametri significativi per tempi di viaggio, densita' residenziali e occupazionali, eta', genere, istruzione, proprieta' abitativa; nessuna metrica quantitativa, survey e numero di rispondenti non specificati [V*, solo pagina] — D.
- C (Graph RAG, Preference Chain), da riassunto del testo: grafo BDI diretto pesato con nodi Agent, Person, Desire, Intention e archi relative_of, similar_to, want_to, choose_to; embedding mxbai-embed-large, similarita' coseno, ricerca in profondita' 3; probabilita' P(i|a) come somma dei pesi dei cammini semplici, senza training; l'LLM (Qwen3:8b, top-k 20, temperatura 0,6, top-p 0,95) corregge i prior in base a condizioni testuali (meteo, orario, citta') [V*] — C.
- C, dati: Replica, Cambridge (MA) e San Francisco, giovedi' tipico primavera 2024; riferimento 10-1000 campioni (esperimenti principali: 50), 1000 di validazione; input eta', reddito, occupazione, nucleo, veicoli, istruzione, scopo, orario; output modalita' (7 categorie) e durata a intervalli di 10 minuti fino a 60; dati sintetici/anonimizzati con ML [V*] — C.
- C, metriche e baseline: KLD e MAE; baseline LLM standalone, Random Forest, MLP, XGBoost con grid search; deep learning escluso; i valori numerici di KLD/MAE per modalita' e durata sono solo nei grafici (Fig. 3-7) [V*] — C.
- C, risultati: con meno di 100 campioni il KLD supera i metodi ML, oltre 100 l'MLP lo supera; per il MAE miglioramento fino a 50 campioni; il trasferimento da un'altra citta' migliora l'LLM ma resta inferiore ai dati locali; simulazione di 1000 persone per 24 ore a Cambridge: KLD del flusso di traffico 0,814 (LLM agent) vs 0,621 (Mobility Agent); sui POI simili [V*] — C. Nessuna ablazione formale dei componenti.
- C, limiti dichiarati: inferenza lenta, allucinazioni non eliminate, modello discreto, traffico esterno a Cambridge ignorato, preferenze dirette assenti nella simulazione POI; il metodo tende a ignorare opzioni rare (on-demand, altre modalita') [V*] — C.
- E: DCGAN addestrata su Cityscapes, accoppiata a CityScope per generare un rendering street-view dopo ogni modifica di design; per supportare la discussione senza design dettagliato. Nessuna metrica, validazione o sede sulla pagina [V*] — E.

### Inferenze
- [I] MoCho e C sono modelli di scelta (descrittivi/predittivi di comportamento individuale); F e' un simulatore; E e' un'immagine generativa: non vanno trattati come famiglia unica nel capitolo.
- [I] C e' l'unico a dichiarare dove il metodo perde (oltre ~100 campioni vince l'MLP): pertinente per contesti a pochi dati, ma il risultato dipende da dati Replica, essi stessi sintetici, cioe' si valuta un LLM contro un modello di popolazione e non contro comportamento osservato [I, da verificare nel PDF].
- [I] E con dataset Cityscapes (citta' europee, prevalentemente tedesche) produce immagini che incorporano i bias visivi del training: un rischio se mostrate in un processo partecipativo a Milano [H].

### Gaps
- Nessun PDF di D, E, F letto; calibrazione, dati e validazione di F e D ignoti.
- Documentazione GAMA (G) non consultata.
- Discrepanza E: pagina MIT (Noyman, 2019) vs corpus (Noyman e Larson 2020, SimAUD): sede/anno non confermati.

## 3. Trasferibilita' a lotti di social housing a Milano

### Takeaway
Trasferibili come impianto metodologico: surrogato veloce di un simulatore per feedback in workshop, scelta discreta con survey locale, agente a pochi dati come esplorazione. Non trasferibili: i parametri e i dati (Boston/Cambridge/USA, traffico AV condiviso), e senza validazione locale nessun output e' difendibile.

### Cited Findings
- Il surrogato di A e' addestrato su una griglia 19x19 con ipotesi AV condiviso [V*] — A; la tesi nomina feedback in tempo reale e suggerimenti AI per non esperti [V*] — B.
- MoCho e' calibrato su dati survey di Boston, sito Kendall Square [V*] — D.
- Il Preference Chain e' valutato su Cambridge e San Francisco; il trasferimento tra citta' e' inferiore ai dati locali [V*] — C.

### Inferenze
- [I] Trasferibile: (1) logica surrogato+ABM per esplorare molte configurazioni di lotti in tempo reale, a condizione di ri-simulare e riaddestrare su Milano; (2) logit/discrete choice per accessibilita' ai servizi con survey o dati ATM/Comune; (3) uso della distribuzione (KLD) per confrontare agenti con dati osservati.
- [I] Non trasferibile: pesi e coefficienti MoCho; modello traffico AV; rendering DCGAN su Cityscapes per rappresentare quartieri di edilizia sociale milanesi.
- [I] Rischi: validazione circolare (surrogato valutato contro un ABM non validato); dati (assenza di dati Replica equivalenti per Milano; sintetici); bias (LLM tende a ignorare opzioni minoritarie e popolazioni a basso reddito, rilevanti per social housing); spiegabilita' e partecipazione (output di LLM lenti e con allucinazioni difficilmente giustificabili davanti agli abitanti).
- [H] Un test di sensibilita' del surrogato fuori distribuzione (configurazioni di lotti irregolari invece di griglia) sarebbe il controllo minimo prima di usarlo nel Lab.

### Gaps
- Nessuna fonte letta sul contesto milanese o su esiti di applicazioni a social housing; la valutazione sopra e' inferenza.
- Per citazioni in tesi: scaricare i PDF da rete non filtrata e ricontrollare ogni cifra.
