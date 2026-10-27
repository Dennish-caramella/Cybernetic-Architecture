# 06 - Verifica sui PDF integrali (MIT City Science)

Data: 2026-10-27. Lingua: italiano. Scopo: controllare cifre e affermazioni delle note 01, 02, 04 e del report "MIT City Science ricerca approfondita.md" (basati su riassunti di pagina [V*]) contro il testo dei PDF ora raggiungibili.

Metodo: PDF scaricati con curl -L (proxy preconfigurato, nessun blocco aggirato) in una directory nuova dello scratchpad; testo estratto con pdftotext -layout da un'altra directory e letto per intero con Read; le figure con valori solo grafici (Graph RAG, Fig. 3 e 5) sono state viste come immagini. Legenda: [V] letto nel PDF, con pagina o sezione (le pagine sono quelle del PDF); [I] inferenza; [H] ipotesi. Parafrasi, nessuna citazione lunga. I valori letti dai grafici sono approssimati e marcati come tali.

## 1. Tabella fonti

| Fonte | Stato | Esito |
|---|---|---|
| Noyman, Holtz, Kröger, Noennig, Larson, "FindingPlaces: HCI Platform for Public Participation in Refugees' Accommodation Process", arXiv:1811.10123 (PDF di 10 pagine; intestazione: Procedia Computer Science, KES2017, Marsiglia, 6-8 sett. 2017) | `verificata` (10/10 pagine lette) | Tutte le cifre dell'imbuto, dei workshop e dei limiti delle note 01 e del report sono confermate. Pesi numerici, soglie alta/media, formula di capacità e numero di particelle sono davvero assenti dal PDF (conferma delle lacune). Una inferenza di nota 01 non è sostenuta dal testo (vedi §3). Volume "112" e DOI non compaiono nel PDF: non verificabili da questa fonte. |
| Noyman, Sakai, Larson, "CityScopeAR: Urban Design and Crowdsourced Engagement Platform", arXiv:1907.08586 (PDF di 5 pagine; formato CHI '18 Workshop) | `verificata` (5/5 pagine lette) | Risolve la divergenza di sede del report: è un contributo al workshop "Novel Interaction Techniques for Collaboration in VR", CHI '18 (Montréal, 21-26 aprile 2018), pubblicato su arXiv nel 2019. I deployment elencati dal report sono confermati. |
| Hu, Atchade-Adelomou, Adornetto, Mora-Carrero, Alonso-Pastor, Noyman, Liu, Larson, "Graph RAG as Human Choice Model", arXiv:2508.16172v2 (5 set. 2025; 19 pagine di testo e appendice) | `verificata` per testo e appendice; i valori numerici delle Fig. 3-7 e 13 sono solo grafici e non sono stati estratti puntualmente | Architettura, dati, metriche, KLD 0,814 e 0,621, soglie 50 e 100 campioni, parametri LLM: confermati. Correzioni su "dati sintetici" e su un aspetto della valutazione POI (vedi §3). |
| Noyman 2022, tesi PhD (DSpace, bitstream b8614805-...) | `non verificabile`: HTTP 429 al 1°, 2° e 3° tentativo (intervalli di almeno 25 s); l'intestazione di risposta contiene retry-after: 900 | Non letta; non si è insistito oltre i tre tentativi. |
| Zhang 2017, tesi CityMatrix (DSpace, bitstream 7ed7bb51-...) | `non verificabile`: HTTP 429 ai 3 tentativi, retry-after: 900 | Non letta. |
| Orii, Alonso, Larson 2020, Sustainability 12(22), 9458 (mdpi.com/.../pdf) | `non verificabile`: un solo tentativo, HTTP 403 "Access Denied" (pagina HTML di errore, 408 byte) | Non letta; non ritentata. Nessuna cifra della nota 04 è stata controllata. |

## 2. Cifre confermate (testo del PDF)

### FindingPlaces (arXiv:1811.10123)

- [V] 34 workshop da due ore, maggio-luglio 2016, presso HCU, ciascuno su uno dei sette distretti; quasi 400 partecipanti; fino a 20 invitati per sessione, media 11 per workshop; un solo workshop per distretto a persona (§4.1, p. 7). Confermati nota 01 e report. [I] 34 x 11 = 374 è coerente con "quasi 400".
- [V] Tre stazioni: città (domanda guida sulle particelle comunali adatte; obiettivo 20.000 posti, contatore alla rovescia in tempo reale), distretto (selezione di aree di interesse), quartiere (esame delle particelle); i segnaposto per le proposte indicano tra 40 e 1.500 posti (§4.3, p. 8). Confermati.
- [V] Esito: 161 localizzazioni proposte; soluzioni per quasi 24.000 persone, oltre il target di 20.000; quasi tre quarti giudicati non adatti nella valutazione iniziale, 44 fattibili; 24 escluse dopo esame di dettaglio; 6 con raccomandazione di attuazione e 10 "presi in considerazione" per pianificazione futura; i 6 ospiterebbero circa 750 persone, circa 4% dell'obiettivo iniziale (§4.4, pp. 8-9). Confermati nota 01 e report.
- [V] Il "circa 4%" è riferito al target di 20.000 (la frase del PDF dice "initial target"), non ai posti proposti. [I] 750/20.000 = 3,75%; 750/24.000 = 3,1%. Conferma la correzione già fatta nel report (la nota 05 con "4% dei posti proposti" è imprecisa).
- [V] Strati dichiarati (§3.3, pp. 6-7): proprietà comunale (disponibilità), usi correnti delle particelle, vincoli come riserve naturali; strati "intersecati e pesati" per produrre una valutazione iniziale in tre classi; aerofoto (WMS) e OpenStreetMap (tile) solo per visualizzazione. Confermato.
- [V] Classi (§3.3, p. 7): alta inadeguatezza = aree significativamente toccate da criteri molto restrittivi (tutela naturalistica, cimiteri, forte rumore, "ecc."); media = non toccate in modo significativo da questi, ma da criteri meno restrittivi (parchi, aree ricreative, linee ad alta tensione o simili); bassa o nulla = non toccate dai criteri molto restrittivi e con criteri meno restrittivi su meno del 50% dell'area. Il 50% è l'unica soglia numerica. Confermato.
- [V] Colori in Stazione II (§4.3, p. 8): rosso = alta inadeguatezza, arancione = media, giallo = probabilmente adatto; in Stazione III le classi sono a tratteggio colorato. Dettaglio non presente nelle note.
- [V] Pesi numerici, soglie di alta e media, formula o parametro per la capacità, numero di particelle del dataset: assenti dal PDF. La capacità è solo "calcolata e indicata" (§4.3, p. 8); l'unico numero è l'esempio di un mattoncino da 50 persone (§3.1, p. 5). Le lacune delle note 01 e del report sono confermate come lacune del paper, non solo del riassunto.
- [V] Ruoli (§1.2, §4.2, §4.4): steg ha moderato il coinvolgimento; équipe di 6-8 persone (moderatore, assistente per la documentazione, ricercatore CSL, tecnico, 1-2 rappresentanti dello staff centrale rifugiati e dell'amministrazione di distretto); lo staff centrale (ZKF) ha eseguito il test di fattibilità e ne ha pubblicato esiti e motivazioni online entro due settimane; le particelle ritenute adatte sono state studiate dalle autorità di pianificazione. Confermato.
- [V] Limiti dichiarati (§5, pp. 9-10): tempi stretti (il mandato lasciava tre mesi, §1.2); logistica che vincola i workshop a HCU con bias di selezione; mancanza di dati urbani e difficoltà dei non esperti con mappe e satellite; minacce: manipolazione tramite pre-processing (colori suggestivi), opposizione di stakeholder, comunicazione fuorviante dei risultati, strumentalizzazione politica. Confermati.
- [V] Sospetto di manipolazione dei dati e accuse di partecipazione "finta" (§4.5, p. 9; non §5 come in nota 05, che lo colloca tra i limiti). Confermato nel contenuto, correzione di sezione.
- [V] Nessun dato di valutazione a supporto del giudizio "esperienza positiva per stakeholder e partecipanti" (§5, p. 9): il testo non riporta questionari, campioni né metriche per FindingPlaces. Conferma "valutazione qualitativa e degli autori". I "questionari di uscita" citati (§2.3) riguardano solo i workshop Boston BRT.
- [V] Il paper non menziona referendum, "9 siti", "circa 1.500 persone in costruzione", né "oltre 150" lotti né "40 sedi in revisione accelerata": le cifre di Medium/pagina di progetto citate nel report non trovano riscontro nel PDF. [H] Il numero 1.500 compare nel PDF solo come massimo dei posti per segnaposto (§4.3): possibile confusione a monte, non verificata.
- [V] Il PDF non indica alcun repository di codice né licenza per FindingPlaces; dichiara l'uso di componenti open source (Crossbar, GeoServer, PostGIS, OpenLayers, OpenCV, Python) (§3.3). Coerente con "codice di FindingPlaces non risulta pubblicato" del report (assenza nel PDF, non prova di assenza altrove).

### CityScopeAR (arXiv:1907.08586)

- [V] Boston BRT: due piattaforme CS usate in eventi con oltre 300 partecipanti, avvio inizio 2015 (sez. "Tests and Deployments"). Confermato il dato citato nel report. Nota: il paper FindingPlaces (§2.3) descrive per BRT sei workshop da circa due ore a ottobre 2015; i due testi non sono in contraddizione, ma non si sovrappongono perfettamente [I].
- [V] AnodrrAR (Andorra): sviluppo metà 2015; esposto alla conferenza Smart Cities di Barcellona (1° trim. 2016) e in permanenza a Caldea, Andorra (1° trim. 2017); a Barcellona quasi 200 commenti registrati ogni giorno; versioni simili a HCU Amburgo (2016), sito Volpe a Cambridge (2017), Tongji a Shanghai (2017). Confermati i deployment elencati dal report.
- [V] Gli autori scrivono che allargare il pubblico può far crescere i costi di deliberazione "in modo esponenziale" (sez. "Discussion"). Il report parla di costi crescenti: corretto, ma il testo dice "esponenzialmente" come rischio, senza misurarlo.
- [V] cityIO: sistema client-server HTTP (NodeJS) dal 2015, dopo un tentativo UDP; AR su Tango (inizio 2016), poi ARcore/ARkit (dal tardo 2017).

### Graph RAG (arXiv:2508.16172v2)

- [V] Grafo BDI pesato e diretto G = (V, E, ω); nodi Agent, Person, Desire, Intention; archi relative_of, similar_to, want_to, choose_to; pesi in [0, 1] (§3.1, pp. 3-5). Confermato nota 02.
- [V] Embedding mxbai-embed-large, similarità coseno, poi ricerca depth-first con profondità 3 (§3.2, p. 5). Confermato.
- [V] Peso del cammino = prodotto dei pesi degli archi (cammini semplici con lunghezza k <= K); punteggio S(a,i) = somma dei pesi dei cammini; P(i|a) = S(a,i) normalizzato (eq. 1-4, p. 5). Confermato. Nessun addestramento (p. 6, p. 12).
- [V] L'LLM tratta le probabilità come prior e le ricalibra con condizioni in linguaggio naturale come meteo, orario, città (§3.4, p. 6). Confermato.
- [V] Parametri LLM: Qwen3-8B senza modalità thinking; top-k 20, temperatura 0,6, top-p 0,95, repeat penalty 1 (Tab. 2, p. 17; §4.2, p. 6). Confermato.
- [V] Dati Replica: giovedì tipico, primavera 2024, Cambridge (MA) e San Francisco; campioni di riferimento da 10 a 1.000; 1.000 campioni di validazione; esperimenti principali con 50 campioni di riferimento esclusi dalla validazione (§4.1, p. 6; §4.4, p. 7). Output: 7 modalità e durata in sei classi da 10 minuti (0-10 ... 50-60) (Tab. 1, p. 15). Confermato.
- [V] Metriche KLD e MAE (eq. 5-6, pp. 6-7); baseline LLM, RF, MLP (scikit-learn) e XGBoost con grid search (Tab. 2, p. 17); deep learning escluso dichiaratamente (§4.2, p. 6). Confermato. Il paper scrive "Mean Average Error".
- [V] KLD: con meno di 100 campioni il Preference Chain batte gli altri metodi; oltre 100 l'MLP lo supera. MAE: il Preference Chain migliora fino a 50 campioni, poi oscilla; l'MLP lo supera dopo 50; 50-100 campioni indicato come equilibrio costo-prestazioni (§4.4, p. 8). Confermato. [V, Fig. 5, lettura grafica approssimata] KLD del baseline LLM circa 1,2-1,3; Preference Chain circa 0,5-0,7 per 10-100 campioni; MAE baseline LLM circa 0,18, Preference Chain circa 0,07-0,09 da 50 campioni.
- [V] Trasferimento tra città (Cambridge con dati SF e viceversa, 1.000 validazione, 50 riferimento): migliora l'LLM ma resta inferiore ai dati locali (§4.4, p. 8). Confermato.
- [V] Simulazione di 1.000 persone per 24 ore a Cambridge: KLD del flusso totale di traffico 0,814 (LLM Agent) contro 0,621 (Mobility Agent, 50 campioni di riferimento) (§5.2, p. 9). Confermato. Sui POI i due agenti hanno KLD simili (§5.3, p. 10). Confermato.
- [V] Limiti dichiarati (§4.4 p. 7; §5.2 p. 10; §6.1 p. 12): inferenza lenta; allucinazioni non eliminate, metodo non adatto ad applicazioni critiche; modello discreto; ignora opzioni rare (on-demand, altre modalità) e durate oltre 40 minuti (in Fig. 3 le barre del Preference Chain per queste classi sono praticamente nulle); nessun traffico esterno a Cambridge. Confermati; l'omissione delle durate oltre 40 minuti è un'aggiunta alla nota 02.
- [V] Il paper non include ablazione dei componenti (es. solo link prediction contro prior più LLM). Il confronto tra LLM diversi (Qwen3:8b, Gemma3:12b, Llama3.1:8b, Fig. 13, p. 18) è l'unico confronto aggiuntivo. Conferma "nessuna ablazione formale" di nota 02; nuovo dettaglio: Llama3.1:8b è più allineato senza dati di riferimento, Qwen3:8b è il migliore con il Preference Chain (Appendice, p. 17).
- [V] Il PDF non indica sede di pubblicazione; riporta solo "arXiv:2508.16172v2 [cs.AI] 5 Sep 2025". Lo stato "preprint" è coerente; "non peer-reviewed" non è verificabile dal PDF [I].

## 3. Cifre e affermazioni corrette o con divergenza

1. [V] Nota 01, inferenza "il filtro GIS lascia passare molto che il vaglio amministrativo scarta": non sostenuta dal PDF. La "valutazione iniziale" che boccia circa tre quarti dei 161 lotti (§4.4, p. 8) è lo screening di fattibilità dello staff centrale (ZKF) e delle autorità, non la classificazione GIS delle tre classi; il PDF non dice quante proposte ricadessero nelle classi rossa, arancione o gialla. Il rapporto tra classi GIS ed esito amministrativo resta ignoto. Da riformulare in nota 01 e nel report ("imbuto" amministrativo, non "filtro GIS").
2. [V] Nota 02 (e report): Replica descritto come "sintetico/anonimizzato con ML". Il PDF dice solo che i dati sono stati anonimizzati con tecniche di ML per proteggere la privacy (§4.1, p. 6); non li definisce sintetici. L'inferenza "il confronto è tra un LLM e un modello di popolazione, non il comportamento osservato" resta [I] non verificabile dal PDF. Il report la marca già come "[I, da verificare sul PDF]": l'esito è "non confermata né smentita".
3. [V] Nota 02, "sui POI simili": corretto, ma il riferimento per i POI è SafeGraph (luglio 2023) (§5.3, p. 10), un dataset diverso da Replica, usato per il flusso di traffico. Il PDF contiene un refuso ("Figure 6-14 (d)"). Il KLD dei POI non è riportato nel testo, solo nei grafici (Fig. 9).
4. [V] Report, CityScopeAR: "sede CHI 2018 (lista MIT) contro arXiv 2019" è risolto: entrambe sono vere (workshop CHI '18, aprile 2018; deposito arXiv nel luglio 2019, ID 1907 e data di creazione del PDF 19 luglio 2019). In nota 01 la citazione "(2019)" va sostituita con "CHI '18 Workshop, arXiv 2019".
5. [V] Nota 01, registro fonti: "Procedia Computer Science 112" e DOI 10.1016/j.procs.2017.08.180 non sono nel PDF (intestazione: "Procedia Computer Science 00 (2017)"). Restano non verificabili da questa fonte; il DOI è già marcato come dedotto.
6. [V] Nota 05 (non oggetto del compito, segnalato per coerenza): collocava il sospetto di manipolazione e la "partecipazione finta" tra i limiti dichiarati; nel PDF stanno in §4.5 (osservazioni sul processo), mentre i limiti formali sono in §5.
7. [V] Nota 01 omette una quadratura: 44 fattibili, 24 escluse dopo esame di dettaglio, 6 raccomandate + 10 per pianificazione futura = 16; il PDF non spiega le 4 particelle restanti (44 - 24 = 20). [I] possibile categoria non menzionata (da non interpretare).
8. [V] Informazioni del PDF assenti nelle note e utili per l'imbuto: più della metà delle particelle proposte erano parchi, aree verdi, paesaggio o agricole soggette a tutela; un altro 15% campi sportivi o parchi giochi; più di un terzo respinto per indisponibilità dovuta ad altri usi; un altro terzo per conflitti d'uso (§4.4, pp. 8-9). Obiettivo dichiarato: 20.000 posti fino a fine 2016 su una previsione di circa 79.000 rifugiati (§1.2, §4.3).

Nessuna cifra della nota 02 su Graph RAG risulta errata; nessuna cifra di nota 01 e del report sull'imbuto risulta errata.

## 4. Elenco finale

### Cifre confermate
- FindingPlaces: 34 workshop; due ore; maggio-luglio 2016; sette distretti; quasi 400 partecipanti; fino a 20 invitati, media 11; 40-1.500 posti per segnaposto; obiettivo 20.000; 161 localizzazioni; quasi 24.000 posti; 44 fattibili; 24 escluse; 6 raccomandate; 10 per il futuro; circa 750 posti (circa 4% del target); soglia 50% della classe bassa; tre classi; strati proprietà/uso/vincoli; assenza di pesi, soglie alta/media, formula di capacità e dimensione del dataset; limiti di §5.
- CityScopeAR: oltre 300 partecipanti BRT; Barcellona circa 200 commenti al giorno; deployment HCU 2016, Volpe 2017, Tongji 2017; costi di deliberazione.
- Graph RAG: struttura del grafo, profondità 3, mxbai-embed-large, Qwen3:8b con i parametri di Tab. 2, 7 modalità, sei classi di durata, 10-1.000 campioni di riferimento, 1.000 di validazione, 50 nel caso principale, soglie 50 e 100, KLD 0,814 contro 0,621, limiti dichiarati.

### Cifre corrette
- "Filtro GIS lascia passare molto" (nota 01): da riformulare (punto 1).
- "Replica sintetico" (note 02/report): non è nel PDF (punto 2).
- Sede/anno CityScopeAR: CHI '18 workshop, arXiv 2019 (punto 4).
- Percentuale 4%: riferita al target, non ai proposti (conferma del report, correzione di nota 05).
- Cifre di Medium/pagina di progetto (9 siti, circa 1.500 persone, referendum, oltre 150 lotti, 40 sedi): non presenti nel PDF; il report le tratta già come non usate come fatti.
- Durate oltre 40 minuti ignorate dal Preference Chain: da aggiungere ai limiti di nota 02.

### Ancora non verificabili
- Tesi Noyman 2022: casi, validazione dei modelli, metodo di pesatura (429; retry-after 900 s; ritentare dopo almeno 15 minuti).
- Tesi Zhang 2017 (CityMatrix): architettura, R², validazione dell'ABM (429).
- Orii et al. 2020 (nota 04: formule, pesi uguali, Numbeo 143/67, 69 città, 100% contro 70%, ParkScore): 403; tutta la nota 04 resta [V*].
- Zhang et al. 2018 AAMAS (CNN, R² 0,86, 19x19x2, 10.000 configurazioni): non rientrava tra i PDF assegnati, non scaricato.
- Non scaricati in questo compito (non assegnati): Bruno et al. 2024 (arXiv:2408.03794; 1,6% per Milano), Zádor et al. 2026, MoCho, Grignard ICCS 2018, Deep Image of the City, OECD OPSI, Medium.
- Valori puntuali di KLD e MAE per modalità e durata (Fig. 3-7): solo grafici; il codice è indicato nel PDF (https://github.com/kekehurry/mobility_agent, p. 12), non consultato.
- Stato peer-review del preprint Graph RAG; volume e DOI Procedia di FindingPlaces.
