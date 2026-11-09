# Laboratori di ricerca su IA, agenti, RL, giochi e partecipazione computazionale per l'abitare (2015–2026)

> Note di ricerca prodotte il 2026-11-09 da agente. Fonti verificate solo tramite risultati di ricerca web (snippet + metadati); **nessun PDF o pagina primaria è stato aperto per intero**: i domini journal.b-pro.org, bproautumn2020.bartlettarchucl.com, pure.tudelft.nl e schoolofmaterialistresearch.org risultano bloccati dalla rete della sessione. Ogni voce va ricontrollata sul testo originale prima di citarla in tesi (regola CLAUDE.md: per citare vale il testo originale).
> Legenda status: **[PR]** = peer-reviewed (rivista/atti con revisione), **[ED]** = pubblicazione editoriale/monografia/rivista curata (AD, Prospectives, libri), **[ST]** = progetto studentesco/mostra, **[IND]** = progetto professionale/commerciale, **[NV]** = non verificato in questa sessione.

## 1. Quali laboratori/progetti affrontano l'abitare partecipativo con IA/agenti/RL/giochi?

### Takeaway
Il nucleo più denso e coerente con la tesi è a Londra: Bartlett B-Pro (RC11 di Morel con "Housing Prime" 2020; cluster mereologici di Koehler/Navasaityte; lavori RL+WFC legati a Hosmer) e AADRL/ZHA CODE (Bhooshan: configuratore per housing mass-customised, piattaforma "gamificata" di partecipazione urbana). MIT City Science ha la base empirica più solida (piattaforme tangibili usate con cittadini reali, es. FindingPlaces Amburgo 2016). Per ETH, IAAC, ICD Stuttgart, GSD, Politecnici e AiDAPT (TU Delft) **non ho trovato** in questa sessione progetti documentati su housing partecipativo con IA: è un gap di ricerca, non prova di assenza.

### Cited Findings
**Bartlett B-Pro (UCL)**
- Philippe Morel è Course Master del Research Cluster 11 (RC11), Graduate Urban Design (B-Pro), UCL Bartlett, con insegnamento elencato anche per 2023–24 (incluso il corso teorico "Introduction to Urban Design Theory: Architecture and its Future"). [ED/istituzionale] — [UCL profile Morel](https://profiles.ucl.ac.uk/82439-philippe-morel/teaching)
- "Housing Prime" (RC11, B-Pro Autumn Show 2020): progetto per un'applicazione che permette agli utenti di progettare la propria casa, con regole generative per scelta del sito, progetto dell'unità, cluster e layout di comunità. [ST] Studenti/tutor non verificati (pagina non accessibile). — [Housing Prime, B-Pro Autumn 2020](https://bproautumn2020.bartlettarchucl.com/rc11/housing-prime)
- B-Pro Show 2023, programma Architectural Computation: progetto "Modular Housing" che usa un solver a vincoli per aggregare case singole in habitat multilivello. [ST] Non verificato che sia RC11 né che Morel ne sia tutor. — [Modular Housing, B-Pro 2023](https://bpro2023.bartlettarchucl.com/architectural-computation-23/modular-housing)
- Il titolo "AI and the Case of La Défense" per RC11 **non è stato trovato** in nessuna fonte indicizzata in questa sessione. [NV] — (ricerca senza esito)
- Koehler e Navasaityte hanno condotto due cluster con il titolo comune "Large City Architecture": RC8 Architectural Design "Mereologies" (2016–17) e RC17 Urban Design. Nessuna fonte trovata per "RC14" associato a Koehler (il brief menziona RC14: da verificare). — [lab-eds, Large City Architecture at the Bartlett](https://lab-eds.org/work/large-city-architecture-bartlett); [Introduction to Issue 01: Mereologies](https://journal.b-pro.org/article/mereologies/)
- Daniel Koehler è oggi docente alla UT Austin School of Architecture (profilo di facoltà). — [UT Austin, Daniel Koehler](https://soa.utexas.edu/faculty/daniel-koehler)
- Tigas & Hosmer, "Spatial Assembly: Generative Architecture With Reinforcement Learning, Self Play and Tree Search" (arXiv 2101.07579, 2021): la generazione di assemblaggi spaziali è formulata come Markov Decision Process con transizioni definite da Wave Function Collapse; policy appresa con RL e self-play. [preprint, non PR] Tyson Hosmer insegna alla Bartlett (affiliazione e cluster [NV]). — [arXiv 2101.07579](https://arxiv.org/pdf/2101.07579v1.pdf); [DeepAI](https://deepai.org/publication/spatial-assembly-generative-architecture-with-reinforcement-learning-self-play-and-tree-search)
- "Training Spaces" (record su CORE): DRL + WFC per generazione goal-driven di spazi; tre passi: definizione tile e regole di connessione, WFC sceglie dove, RL sceglie quale tile. Autori **non confermati** (possibile legame con Erioli/Co-de-iT: [NV]). — [CORE 142707019](https://core.ac.uk/works/142707019)
- Tesi (Academia.edu) "Deep Reinforcement Learning for Training Intelligent Agents in Cooperative Housing Environments Using Decentralised Agents and a Central-Critic": agenti che assemblano aggregati abitativi mantenendo prossimità al verde. Istituzione/autore non verificati (probabile tesi B-Pro/AC). [ST/NV] — [Academia.edu](https://www.academia.edu/56469349/_Deep_Reinforcement_Learning_for_Training_Intelligent_Agents_in_Cooperative_Housing_Environments_Using_Decentralised_Agents_and_a_Central_Critic_)

**AA DRL / ZHA CODE (Shajay Bhooshan)**
- Louth, Fragachan, V. Bhooshan, S. Bhooshan, "Configurator: A Platform for Multifamily Residential Design and Customisation" (Springer, cap. 2023; ResearchGate indica gen. 2024): configuratore real-time su game engine per esiti abitativi mass-customised, guidati dall'utente/partecipazione. [PR probabile: atti Springer, venue esatto NV] — [Springer 10.1007/978-3-031-36922-3_40](https://link.springer.com/chapter/10.1007/978-3-031-36922-3_40)
- Il configuratore ZHA è stato usato per Próspera (Honduras), accoppiato a microfabbriche per "start-up neighbourhoods". [IND] — [Unreal Engine spotlight](https://www.unrealengine.com/spotlights/personalizing-property-with-zaha-hadid-architects-real-time-configurator?lang=en-US)
- Schumacher & Bhooshan, capitolo su piattaforma online "gamificata" per urban design partecipativo (Routledge Companion to Smart Design Thinking, 2025), che fa risalire l'idea al progetto AADRL 2001 "Negotiate My Boundary". [ED] — [patrikschumacher.com, A Smart Paradigm for Participatory Urban Design](https://patrikschumacher.com/a-smart-paradigm-for-participatory-urban-design/)
- AADRL "Oikos" (studio Nahmad/Bhooshan): rule-set architettonico che permette alle persone di partecipare al progetto della propria casa; architetture prefabbricate mass-customised informate da teoria dei giochi. [ST] — [AADRL Oikos](https://drl.aaschool.ac.uk/oikos)
- AADRL Phase 2 review gen. 2026: studio Bhooshan su "geometric energy landscapes" e "socio-economic game rules", progetti UpBridge City, VertiCity. [ST] — [AADRL archive Jan 2026](https://www.aadrlarchive.co.uk/phase-2-review-jan-2026)

**MIT City Science (Media Lab, Kent Larson)**
- Noyman, Holtz, Kröger, Noennig, Larson, "Finding Places: HCI Platform for Public Participation in Refugees' Accommodation Process", *Procedia Computer Science* 112 (2017), pp. 2463–2472: sistema HCI (CityScope tangibile) usato ad Amburgo nel 2016 per decisioni partecipative sull'allocazione di alloggi per rifugiati. [PR, atti KES] — [record catalogo](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c3060-34ec0a3f390b4a0183105a6dc50c5108f9bf67670d806b9d756ddeeafe7abfcf3)
- Alonso, Noyman, Larson et al., "CityScope: A Data-Driven Interactive Simulation Tool for Urban Design. Use Case Volpe" (Springer, *Unifying Themes in Complex Systems IX*, 2018). [atti; peer review NV] — [MIT Media Lab](https://www.media.mit.edu/publications/cityscope-a-data-driven-interactive-simulation-tool-for-urban-design-use-case-volpe)
- Agent-based model che accoppia scelta modale e scelta abitativa (Kendall Square), con incentivi per housing accessibile entro 20 minuti a piedi dal lavoro (arXiv 2106.14572). [preprint] — [arXiv 2106.14572](https://arxiv.org/pdf/2106.14572)
- Tesi di dottorato di Noyman su CityScope (MIT, 2022): combina decisione data-driven e pianificazione partecipativa. — [DSpace@MIT 1721.1/145128](https://dspace.mit.edu/handle/1721.1/145128)

**TU Delft**
- Paper EC3 2024 (TU Delft): pipeline in cui un modello a grafo genera il layout graph (invece di recuperarlo da database come Graph2Plan), poi un RaGAN vincolato al grafo basato su HouseGAN++ genera la pianta; l'utente valuta, modifica o rigenera il grafo secondo le proprie preferenze. [PR, atti EC3; autori NV] — [EC3 2024 paper 188](https://ec-3.org/wp-content/uploads/2025/10/EC32024_188.pdf)
- TU Delft: ricerca partecipativa design-led sull'abitare collaborativo per anziani (Tanthof-Oost, Delft) e gruppo Co-Lab Research (abitare collaborativo) — senza IA. — [ResearchGate, Together: Towards Collaborative Living](https://www.researchgate.net/publication/374892847_Together_Towards_Collaborative_Living); [Co-Lab Research](https://co-lab-research.net/)
- AiDAPT (TU Delft): **nessun risultato** trovato in questa sessione. [NV]

### Inferences
- [inferenza] La "filiera" Bartlett/AA produce soprattutto lavori [ST] ed [ED]; la validazione con utenti reali è quasi assente. L'unico caso con dispiegamento pubblico documentato e peer-reviewed è FindingPlaces (MIT/HCU, 2017).
- [inferenza] Il configuratore ZHA è l'erede industriale più diretto del Flatwriter di Friedman, ma il suo primo dispiegamento è in una charter city privata (Próspera): utile per la sezione critica (partecipazione come scelta di consumo dentro un sistema chiuso).
- [ipotesi] RL+WFC (Tigas & Hosmer; "Training Spaces") è il ponte tecnico più vicino all'idea di "villaggio verticale che cresce": sistema di regole locali + agenti che apprendono. Manca però la dimensione multi-attore/negoziale.

### Gaps
- Contenuto effettivo di "Housing Prime" (autori, tutor, uso di IA): pagina bloccata.
- RC11 "AI and the Case of La Défense": nessuna fonte; possibile titolo di un anno specifico (verificare sul sito B-Pro show dell'anno).
- ETH (Gramazio Kohler, CAAD/Digital Architectonics, Future Cities Lab), IAAC, Harvard GSD, ICD Stuttgart, PoliMi/PoliTo, MIT Self-Assembly Lab, AiDAPT: nessuna fonte su housing partecipativo con IA trovata (ricerche non esaustive per limite di chiamate).
- Erioli/Co-de-iT "Assembler" e WFC+RL: nessun paper confermato con suo nome.

## 2. Pubblicazioni peer-reviewed: RL multi-agente, layout da grafi, configuratori, architettura discreta

### Takeaway
La letteratura peer-reviewed su RL multi-agente per layout residenziali è esplosa nel 2024–2026, ma viene soprattutto da ingegneria/informatica (Automation in Construction, Advanced Engineering Informatics, Knowledge and Information Systems), non dai laboratori di architettura citati; la "partecipazione" vi compare raramente, e quasi solo come agenti che simulano stakeholder.

### Cited Findings
- Planning comunitario come gioco di Markov; MARL con curriculum learning per generare layout di comunità — *Knowledge and Information Systems* (Springer, 2024). [PR] — [Springer 10.1007/s10115-024-02291-4](https://link.springer.com/10.1007/s10115-024-02291-4?fromPaywallRec=false)
- MARL per composizione spaziale in ristrutturazione edilizia — *Automation in Construction* (2024). [PR] — [ScienceDirect S0926580524004382](https://www.sciencedirect.com/science/article/abs/pii/S0926580524004382)
- Aggregazione di unità abitative e core in piante residenziali alte con algoritmo genetico + multi-agent cooperative DQN — *Automation in Construction* (2025). [PR] — [ScienceDirect S0926580525003693](https://www.sciencedirect.com/science/article/abs/pii/S0926580525003693)
- Layout residenziali controllabili con multi-agent DRL — *Advanced Engineering Informatics* (2025). [PR] — [ScienceDirect S1474034625005956](https://sciencedirect.com/science/article/abs/pii/S1474034625005956)
- Rein2Plan: MARL controllabile per piante residenziali orientate alla salute (2026). [PR, rivista NV] — [ScienceDirect S266616592600092X](https://www.sciencedirect.com/science/article/pii/S266616592600092X)
- "AI Agent as Urban Planner": MARL basato su consenso; agenti come rappresentanti di stakeholder votano usi del suolo; confronto con pianificazione top-down e partecipativa (arXiv 2310.16772). [preprint] — [arXiv 2310.16772](https://arxiv.org/pdf/2310.16772)
- "Design Process is a Reinforcement Learning Problem" (arXiv 2211.03136). [preprint] — [arXiv 2211.03136](https://arxiv.org/pdf/2211.03136)
- Graph2Plan (Hu et al., 2020): piante da layout graph con vincoli utente (numero stanze, connettività). — [nono.ma/graph2plan](https://nono.ma/graph2plan)
- House-GAN++ (Nauata et al., CVPR 2021): GAN relazionale vincolato a grafo funzionale con raffinamento iterativo. [PR] — [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2021/html/Nauata_House-GAN_Generative_Adversarial_Layout_Refinement_Network_towards_Intelligent_Computational_Agent_CVPR_2021_paper.html)
- Mass customisation dell'housing industrializzato, framework per armonizzare esigenze individuali e produzione in fabbrica — *Buildings* 12(7):955 (MDPI, 2022). [PR] — [MDPI](https://www.mdpi.com/2075-5309/12/7/955)
- Koehler et al., "Mereologies – Combinatorial Design and the Description of Urban Form", Proceedings 36th eCAADe (2018; pagine/DOI NV). [PR] — [lab-eds](https://lab-eds.org/work/large-city-architecture-bartlett)
- Koehler, "Mereological Thinking: Figurating Realities within Urban Form", *AD* "Discrete" (2019), pp. 30–37; Koehler, "From Partitioning to Partaking, or why Mereologies matter", *Prospectives* 1 (Bartlett, 2020), pp. 11–33. [ED] — [journal.b-pro.org issue 1](https://journal.b-pro.org/issue/issue1/)
- Koehler, *The Mereological City: A Reading of the Works of Ludwig Hilberseimer*, transcript, Bielefeld 2016 (Architektur 36), DOI 10.1515/9783839434666. [ED] — [De Gruyter](https://www.degruyterbrill.com/document/doi/10.1515/9783839434666-007/machineReadableCitation/BibTeX)
- eCAADe 2025 preprint pertinente al tema layout/grafi (titolo NV). — [ecaade2025_272](https://conf.dap.tuwien.ac.at/preprints/ecaade2025/ecaade2025_272.pdf)

### Inferences
- [inferenza] C'è una frattura disciplinare: i laboratori di architettura producono teoria (mereologia, discreto) e prototipi studenteschi; le prove quantitative su RL/layout stanno in riviste ingegneristiche che ottimizzano piante, non processi sociali. Lo spazio "RL + partecipazione reale + abitare collettivo" sembra poco occupato: possibile contributo originale della tesi.
- [inferenza] Nei paper MARL l'"agente" è un vano o un'unità, non un abitante; solo arXiv 2310.16772 tratta agenti come stakeholder, e lo fa per simulazione, non con persone vere.

### Gaps
- Nessuna ricerca diretta su CUMINCAD è riuscita (non indicizzato dai risultati); servono query manuali su cumincad.architexturez.net per "participatory", "housing", "agent-based", "Flatwriter".
- Discendenti accademici del Flatwriter (Friedman) non trovati in questa sessione.

## 3. Prospettive critiche: capitalismo di piattaforma, automazione, tokenismo

### Takeaway
Le fonti critiche principali sono identificate bibliograficamente (Sanchez 2020, Carpo 2017, Morel 2011–2019), ma il contenuto argomentativo è verificato solo da descrizioni editoriali; va letto sul testo.

### Cited Findings
- Sanchez, *Architecture for the Commons: Participatory Systems in the Age of Platforms*, Routledge 2020, 148 pp., ISBN 978-1-138-36235-2 (hb) / 978-1-138-36236-9; capitoli dall'architettura post-2008 alla "self-provision" e alle "immaterial architectures". — [Routledge](https://www.routledge.co.uk/9781138362369); [Schweitzer](https://www.schweitzer-online.de/en/buch/Sanchez/Architecture-for-Commons/9781138362352/A56032057/)
- Sanchez è autore di Block'hood e Common'hood, piattaforme social/videoludiche per coinvolgere non esperti nel pensiero architettonico ed ecologico; dirige Plethora Project; oggi Associate Professor a Cornell AAP / Cornell Tech (alcune bio lo indicano ancora a Michigan). — [Routledge](https://www.routledge.co.uk/9781138362369); [Cornell AAP](https://aap.cornell.edu/people/jose-sanchez)
- Lecture di Sanchez "Platform Realism" (UT Austin). — [UT Austin SoA](https://soa.utexas.edu/events/lecture-series-jose-sanchez-plethora-project-u-michigan-platform-realism)
- Carpo, *The Second Digital Turn: Design Beyond Intelligence*, MIT Press 2017 (Writing Architecture); include il capitolo "The participatory turn that never was" e "Economies without scale: toward a nonstandard society". — [CCA catalogue](https://www.cca.qc.ca/en/search/details/library/publication/964698464); [TOC](https://biblioteca.izt.uam.mx/vufind/Record/musev2_56304/TOC)
- Il caso Próspera (configuratore ZHA) offre un esempio concreto di "partecipazione" come personalizzazione dentro un modello di sviluppo privato. — [Unreal Engine spotlight](https://www.unrealengine.com/spotlights/personalizing-property-with-zaha-hadid-architects-real-time-configurator?lang=en-US)

### Inferences
- [inferenza] Il titolo stesso del capitolo di Carpo ("la svolta partecipativa che non c'è stata") è un contrappunto diretto all'ipotesi della tesi: va affrontato esplicitamente.
- [ipotesi] Una griglia utile per il tokenismo è la scala di Arnstein (1969), non verificata in questa sessione: configuratori come ZHA/Flatwriter si collocano probabilmente tra "consultation" e "placation" se l'utente sceglie solo entro opzioni predefinite.

### Gaps
- Testo dei capitoli di Sanchez e Carpo sulla partecipazione non letto.
- Nessuna fonte trovata su critiche specifiche alla "gamification" della partecipazione in architettura (oltre ai titoli).

## 4. Philippe Morel: scritti teorici (EZCT, capitalismo computazionale)

### Takeaway
I testi chiave verificabili: "Sense and Sensibilia" (AD 2011, "logica computazionale del tardo capitalismo"), "Computation or Revolution" (AD 2014), "The Communism of Genius" (2014, IA e politica), "The Origins of Discretism" (AD 2019, DOI 10.1002/ad.2407); primi saggi "The Integral Capitalism" (2000–02) ecc. Nessun saggio su *Log* trovato.

### Cited Findings
- "The Origins of Discretism: Thinking Unthinkable Architecture", *Architectural Design* 89(2), marzo 2019 (numero "Discrete", a cura di Retsin), DOI 10.1002/ad.2407: rottura con antropomorfismo e razionalismo verso un'architettura propriamente computazionale. — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/ad.2407); [ResearchGate](https://www.researchgate.net/publication/331468113_The_Origins_of_Discretism_Thinking_Unthinkable_Architecture)
- "Sense and Sensibilia", *Architectural Design*, luglio 2011: esplora la "computational logic of late capitalism"; Morel collega l'idea a ciò che dal 2000 chiama "Integral Capitalism". — [ResearchGate](https://www.researchgate.net/publication/260281397_Sense_and_Sensibilia); [The City as a Project, seminario 2011](http://thecityasaproject.org/2011/10/a-discussion-about-the-computational-logic-of-late-capitalism-a-seminar-with-phillippe-morel/)
- "Computation or Revolution", *Architectural Design*, maggio 2014: radici di computazione e robotica nella Seconda guerra mondiale. — [ResearchGate](https://www.researchgate.net/publication/261702096_Computation_or_Revolution)
- "The Communism of Genius" (2014, in un volume/rivista "Next Generation Building" — venue esatto NV): problemi politici legati all'IA in architettura. — [ResearchGate](https://www.researchgate.net/publication/276527832_The_Communism_of_Genius)
- Primi saggi elencati in bio: "The Integral Capitalism" (2000–2002), "Research On the Biocapitalist Landscape" (2002), "Notes on Computational Architecture" (2004). [ED; venue NV] — [What's the Matter (ENHSA)](http://www.enhsa.net/WhatsTheMatter/philippe-morel/); [School of Materialist Research](https://schoolofmaterialistresearch.org/Philippe-Morel)
- Un "Bartlett tutor" ha pubblicato nel 2023 il libro *Disruptive Technologies* per Springer (autore non verificato: possibile Morel, da controllare). [NV] — [UCL Bartlett news, May 2023](https://www.ucl.ac.uk/bartlett/news/2023/may/bartlett-tutor-publishes-new-book-disruptive-technologies-springer)

### Inferences
- [inferenza] Per la tesi, la linea Morel (automazione integrale, discretismo) fornisce la cornice critica sul lavoro dell'architetto: se il sistema genera, l'architetto progetta le regole — coerente con "architetto come progettista di sistemi", ma Morel lo legge come esito del capitalismo computazionale, non come emancipazione.

### Gaps
- EZCT Architecture & Design Research (fondazione ~2000, soci Morel, Jacob, Ruiz-Geli?): dati [NV], non verificati in questa sessione.
- Bibliografia completa di Morel: da prendere dal suo profilo UCL o ResearchGate ([profilo ResearchGate](https://www.researchgate.net/profile/Philippe-Morel-5)).
- Riferimenti già noti nel brief (Friedman/Flatwriter 1967, Pask, Price, MVRDV Functionmixer/Spacefighter, Block'hood 2017) non riverificati qui.
