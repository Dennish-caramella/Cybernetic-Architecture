# Mappa critica dei modelli di analisi

Stato: **prima versione, 2026-11-09** (Fase 0). Serve a decidere quali modelli usare, non è una scheda di lettura.
Marche: **[V]** verificato nei file del repo; **[S]** da una scheda del corpus; **[I]** inferenza; **[DV]** riferimento bibliografico noto ma **da verificare** prima di citarlo (autore, anno, sede). Nessun riferimento [DV] entra in bibliografia senza verifica.

Fonti interne: `prove/in_evidenza/2026-10-25_spatial_milano_lab/lab_completo/results/paper.md` (§3 Metodi) [V], riesame `secondo_cervello/ricerche/06_riesame_spatial_milano_lab.md` [V].

---

## Parte 1. Che cosa c'era nel Lab e che cosa dimostra

| # | Modello del Lab | Che cosa fa | Che cosa dimostra oggi (riesame #6) | Tenere? [I] |
|---|---|---|---|---|
| 1 | **Domanda e potere d'acquisto**: distribuzione di Dagum sui redditi IRPEF per CAP, famiglie sintetiche dal Censimento 2021, proxy ISEE per l'ERP, tre strati di domanda (D_tau, D_res_decent, D_res_istat) con il test di reddito residuo (*shelter poverty*, Stone) [V] | stima quante famiglie per NIL non reggono l'affitto di mercato | **artefatto**: la domanda stimata coincide con gli affitti (rho 0,987), il reddito è noto solo a 38 CAP [V] | sì come idea (reddito residuo = buona definizione della "pancia"); da rifare con dati a risoluzione migliore |
| 2 | **Siti candidati**: filtro sulle particelle catastali (≥300 m², non verde, non parchi, non residenziale occupato), accorpamento in siti 1.500–60.000 m², capacità da FAR [V] | da 112.568 particelle a 2.291 siti [V] | regge come procedura; FAR 1,0 e proprietà non verificati [V] | **sì: è la base dei lotti** |
| 3 | **Nove criteri** di sito (metro, lavoro, servizi E2SFCA, verde, calore, famiglie bisognose vicine, peso dell'affitto, capacità, costo) [V] | descrive ogni lotto | descrittivo, non una prova | sì, ma **catalogo riscrivibile** (domanda di ricerca) |
| 4 | **SMAA-2** (Lahdelma e Salminen) [V; DV] | dice quanto un sito vince al variare dei pesi, senza fissarli | "nessun vincitore": risultato onesto [V] | sì: è lo strumento giusto per "criteri negoziabili" |
| 5 | **Apprendimento bayesiano delle preferenze a coppie** con domande attive e *teach-back* [V] | impara i pesi di una persona da scelte tra due siti, e le spiega cosa le farebbe cambiare idea | **solo archetipi sintetici**, nessun dato umano [V] | sì per la prova reale (F2); il *teach-back* è una buona idea di trasparenza |
| 6 | **Portafogli MILP robusti** (HiGHS, media + CVaR, budget 1 mld, tetti per NIL, tagli di diversità) [V] | sceglie un insieme di siti e alloggi | molti portafogli quasi equivalenti; vincolo Gini non vincolante [V] | da rivedere: è un'ottimizzazione "dall'alto", va spostata dopo la scelta dei gruppi |
| 7 | **Audit di segregazione del PGT** (dissimilarità, isolamento, null appaiati, Benjamini-Hochberg) [V] | verifica se le aree del piano concentrano povertà | "rischio" = rumore Monte Carlo; +48% = artefatto [V] | in archivio: è una domanda diversa dalla tesi (critica del PGT) |
| 8 | **Rilevatore PU** (positive-unlabeled) di siti simili a quelli designati [V] | ML spaziale | PR-AUC gonfiata, non usato nel modello [V] | in archivio |

**Lettura d'insieme [I].** Il Lab è forte su *dove* (lotti, criteri, incertezza dei pesi) e debole su *chi* (domanda) e *come insieme* (gruppi). Mancano del tutto i tre pezzi che la nuova domanda di ricerca mette al centro: **formazione di gruppi eterogenei, abbinamento gruppi–lotti, modello economico reale**.

---

## Parte 2. Il processo della tesi e i modelli candidati per ogni passo

Processo deciso il 09/11: *lotti → persone e gruppi → abbinamento gruppi–lotti (con scelta) → economia → edificio*.

### 2.1 Lotti
| Livello | Modelli | Nota |
|---|---|---|
| Già nel Lab | filtro particelle + criteri + SMAA [V] | base |
| Consolidati | GIS-MCDA (Malczewski) [DV]; analisi di sensibilità dei pesi | standard in pianificazione |
| Frontiera | modelli su grafi di particelle (GNN); embedding di immagini satellitari e street view per descrivere i lotti [I] | utili solo se aggiungono informazione verificabile; rischio di opacità |

### 2.2 Persone e domanda
| Livello | Modelli | Nota |
|---|---|---|
| Già nel Lab | reddito residuo, famiglie sintetiche [V] | buona definizione, dati deboli |
| Consolidati | **popolazioni sintetiche** con IPF o ricampionamento da microdati; modelli **agent-based** del mercato abitativo [DV] | permettono di simulare famiglie con età, composizione, reddito: serve per la fase "prima agenti" |
| Frontiera | **agenti generativi con LLM** come residenti simulati (Park et al. 2023, *Generative Agents*) [DV] | affascinanti per simulare negoziazione e motivazioni; rischio forte: l'LLM riproduce stereotipi, non esigenze. Usabili per collaudare il sistema, **mai** come evidenza sui bisogni |

### 2.3 Formazione dei gruppi (il pezzo nuovo)
| Livello | Modelli | Nota |
|---|---|---|
| Consolidati | **giochi edonici / formazione di coalizioni** (ogni persona valuta il proprio gruppo) [DV]; **clustering con vincoli di equità/diversità** (*fair clustering*, Chierichetti et al. 2017) [DV] | il fair clustering impone proporzioni (per esempio di età) in ogni gruppo: è il modo diretto di evitare i ghetti |
| Precedente progettuale | Housing Prime (Morel RC11): cluster per esigenze **simili** [V: scheda 09] | il controesempio da superare |
| Frontiera | RL multi-agente per formare coalizioni; LLM come mediatore che propone composizioni e le spiega [I] | da tenere come esperimento, dopo una linea di base semplice |

### 2.4 Abbinamento gruppi–lotti, con scelta
| Livello | Modelli | Nota |
|---|---|---|
| Consolidati | **matching stabile** (Gale e Shapley 1962); **top trading cycles** e assegnazione della casa (Shapley e Scarf 1974; Abdulkadiroğlu e Sönmez) [DV]; matching con **vincoli distributivi** (Kamada e Kojima) [DV] | è esattamente "le persone scelgono tra i lotti": teoria matura, con proprietà dimostrabili (nessuno ha incentivo a mentire, nessuna coppia gruppo-lotto preferisce deviare). **Candidato forte per il nucleo della scala urbana** [I] |
| Già nel Lab | MILP di portafoglio [V] | ottimizza per il pianificatore, non per chi sceglie |

### 2.5 Negoziazione dei criteri e aggregazione
| Livello | Modelli | Nota |
|---|---|---|
| Già nel Lab | SMAA, preferenze bayesiane, teach-back [V] | base |
| Consolidati | **teoria della scelta sociale** (Borda, approvazione, Arrow) [DV]; **bilancio partecipativo computazionale** [DV]; piattaforme di deliberazione come Polis [DV] | colma la lacuna "funzione di aggregazione" segnalata il 25/10 |
| Frontiera | **deliberazione mediata da LLM** che cerca un terreno comune (lavori recenti tipo "Habermas Machine", 2024) [DV] | è la versione contemporanea del mediatore cibernetico di Pask; va messa alla prova sulla seconda metà della domanda (mediatore trasparente o decisore nascosto?) |

### 2.6 Economia
| Livello | Modelli | Nota |
|---|---|---|
| Consolidati | **valore residuo del suolo / piano economico del developer** (DCF) come scenario di confronto; piano economico di **cooperativa a proprietà indivisa**, **Community Land Trust**, modelli tipo Mietshäuser Syndikat [DV] | serve per misurare "più accessibile" contro lo scenario developer, con parametri reali (costi di costruzione, oneri, mutui) |
| Già nel Lab | costo per alloggio come criterio, budget nel MILP [V] | troppo semplice |

### 2.7 Edificio (F3, da affrontare a suo tempo)
| Livello | Modelli | Nota |
|---|---|---|
| Nel corpus | Assembler (Erioli) [S:17]; multi-agent space planning [S:13]; WFC + RL (Mintrone ed Erioli 2021) [DV] | coerenti con kit of parts e villaggio verticale |
| Consolidati | grammatiche di forma; layout da grafi di adiacenza [DV] | |
| Frontiera | generazione di piante da grafi con reti neurali (famiglia House-GAN, Graph2Plan) [DV] | |

### 2.8 Simulazione e valutazione del tutto
- **Linea di base obbligatoria**: ogni modello "intelligente" va confrontato con una regola semplice (pesi uniformi, assegnazione casuale, Schelling come modello minimo di segregazione [DV]). È la lezione del Lab: senza linea di base non si sa se il modello aggiunge qualcosa [V: riesame].

---

## Parte 3. Proposta di nucleo per F1 (da discutere) [I]
1. Lotti: filtro del Lab + criteri riscrivibili + SMAA.
2. Persone: popolazione sintetica di famiglie milanesi della "pancia" (reddito residuo), poi agenti LLM solo per collaudare l'interazione.
3. Gruppi: fair clustering con diversità dichiarata e negoziabile, confrontato con il clustering per somiglianza (alla Housing Prime).
4. Abbinamento: matching stabile gruppi–lotti, confrontato con il portafoglio MILP dall'alto.
5. Economia: piano economico cooperativa/CLT contro piano developer, per lotto.

Ogni passo ha una linea di base e una metrica fissata prima. Così la domanda di ricerca diventa misurabile: *gruppi eterogenei + scelta dei lotti + economia non speculativa* contro *mercato/developer* e contro *pianificatore che ottimizza dall'alto*.

## Da fare
- Verificare tutti i [DV] sulle fonti primarie prima di citarli.
- Decidere con Dennis il nucleo di F1 (Parte 3).
