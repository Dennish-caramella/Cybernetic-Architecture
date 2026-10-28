# Indicatori urbani, accessibilità e abitare nei lavori del MIT City Science Group

**Avvertenza di metodo (leggere prima).** In questa sessione `curl` è bloccato dal proxy per tutti gli host utili (mdpi.com, arxiv.org, dspace.mit.edu, media.mit.edu, doi.org, crossref, ecc.: CONNECT 403; verificato con `/__agentproxy/status`, che elenca questi host tra i `connect_rejected`). Non è stato quindi possibile scaricare nessun PDF né leggerlo con Read/pdftotext. Tutto quanto segue viene da WebFetch, cioè da riassunti prodotti da un modello sulla pagina HTML o PDF. **Nessuna fonte può essere marcata `verificata` secondo il criterio richiesto (PDF intero letto).** Marcatura usata: `parziale` = riassunto di modello su testo integrale della fonte (più affidabile di un abstract, ma di seconda mano); `da verificare` = solo titolo/citazione. [V*] = riportato dal riassunto di WebFetch, con sezione/equazione indicata dal riassunto ma non controllata sul PDF. [I] inferenza, [H] ipotesi. Cifre ed equazioni vanno ricontrollate sul PDF prima di citarle in tesi. Non ho trovato né letto nulla su CityHome/Compact Living/Andorra/Boston/Taipei da fonti scientifiche primarie (vedi Gap).

## Fonti

| # | Autori, anno | Titolo | Sede | DOI/URL | Stato |
|---|---|---|---|---|---|
| A | Orii L., Alonso L., Larson K., 2020 | Methodology for Establishing Well-Being Urban Indicators at the District Level to be Used on the CityScope Platform | Sustainability 12(22), 9458 | DOI 10.3390/su12229458; https://www.mdpi.com/2071-1050/12/22/9458 | `parziale` (due riassunti WebFetch dell'HTML integrale; PDF non scaricabile) |
| B | Noyman A., Doorley R., Xiong Z., Alonso L., Grignard A., Larson K., 2019 | Reversed urbanism: Inferring urban performance through behavioral patterns in temporal telecom data | Environment and Planning B 46(8), 1480-1498 | DOI 10.1177/2399808319840668; https://ideas.repec.org/a/sae/envirb/v46y2019i8p1480-1498.html | `parziale` (solo scheda bibliografica con abstract) |
| C | Elenco pubblicazioni Noyman (MIT Media Lab), s.d. | Elenco: Andorra mobility/COVID (2021), RevUrb (2019), MoCho (2019), CityScope Andorra (AAMAS 2018), CityScopeAR, Roadmap for Autonomous Cities (2017) ecc. | https://www.media.mit.edu/people/noyman/publications/ | come indicato | `parziale` (solo indice; contenuti non letti) |
| D | MIT Media Lab, pagina di progetto | Understanding the 15 Minute City (persone, collaborazione NTT DATA) | https://www.media.mit.edu/projects/understanding-the-15-minute-city/people/ | | `parziale` (pagina senza descrizione né pubblicazioni) |
| E | BD+C (Building Design+Construction), 30 maggio 2014 | How can you make a 200-sf micro apartment feel and function like a typical studio unit? (CityHome) | Stampa di settore, non scientifica | https://www.bdcnetwork.com/mit-researchers-create-home-box-transformable-wall-system-micro-apartments?page=9 | `parziale`, fonte secondaria |
| F | Bruno M., Melo H.P.M., Campanelli B., Loreto V., 2024 | A universal framework for inclusive 15-minute cities | Preprint arXiv:2408.03794 (Sony CSL Roma ecc.) | https://arxiv.org/pdf/2408.03794 | `parziale`. **Non è un lavoro MIT**: serve solo come riferimento esterno su Milano |
| G | Zádor Z. et al., 2026 | Public transport in the 15-minute city | Preprint arXiv:2604.00699v1 | https://arxiv.org/html/2604.00699v1 | `parziale`. **Non è un lavoro MIT**; letti solo i primi 100.000 caratteri su 148.000 |

Non aperte (host bloccato o robots): pagina media.mit.edu del paper Volpe (robots_disallowed), articolo ACM/IGI "CityScope Platform for Real-Time Analysis and Decision-Support in Urban Design Competitions" (IJEPR 2021, DOI 10.4018/IJEPR.20211001.oa8, comparso in ricerca: `da verificare`, contenuto non letto), articolo Urban Land (ULI) su MIT City Science (errore). Elenco noto in `08_mit_city_science.md` per le fonti già lette (FindingPlaces, CNN, ecc.).

---

## Orii, Alonso, Larson 2020: formule, variabili, pesi, normalizzazione, fonti, validazione; usabilità a Milano

### Takeaway
L'indice è una media pesata, con pesi uguali, di cinque indicatori (Community Connectedness, Safety & Security, Physical Health, Mental Health, Diversity) costruiti da attributi urbani alimentati da dati USA a scala di città; è dichiaratamente non validato. Per Milano si può riusare la struttura (formule di copertura/accessibilità/Simpson e composito), non i valori né diversi attributi (Numbeo, ParkScore, uso della forza); la ricalibrazione richiede nuovi dati di quartiere (NIL), pesi giustificati e validazione. Tutto da ricontrollare sul PDF.

### Cited Findings
- Cinque indicatori e relativi attributi: Community Connectedness (Perceived Safety, Park Coverage, Park Accessibility, Walkability, Community Gardens); Safety & Security (Perceived Safety, Park Coverage, Use of Force Policies); Physical Health (Perceived Safety, Community Gardens, Park Coverage, Park Accessibility); Mental Health (Perceived Safety, Park Accessibility, Social Interaction, Community Gardens); Diversity (sei attributi). [V*, sez. 3] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Formule [V*, sez. 4]: Park Coverage = area parchi / area urbana × 100 (eq. 1); Park Accessibility = somma delle capacità dei punti di interesse raggiungibili a piedi in 10 minuti, poi media (eq. 2), normalizzata 0-100 con ParkScore; Park Quality = media dei rapporti amenità/capacità su sei amenità (eq. 3), descritta ma non assegnata a nessun indicatore; Community Gardens = orti ogni 1.000 abitanti (eq. 4), poi percentile di rango tra 69 città USA; Use of Force Policies = somma delle riduzioni percentuali delle uccisioni associate alle policy adottate / somma di tutte le policy possibili × 100 (eq. 5); Diversity D = 1 − Σp² (eq. 6); composito Score = Σ(w_i·x_i) (eq. 7). — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Walkability = Walk Score 0-100 (nessuna formula); Perceived Safety = Numbeo Safety Index di città da sondaggi (143 utenti Boston, settembre 2020; 67 Kansas City); Social Interaction coincide con il composito di Community Connectedness. [V*, sez. 4.1, 4.5, 4.8] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Sei dimensioni di diversità: razza/etnia, reddito, età, lingua parlata, istruzione, regione di nascita; il reddito ha tre fasce (sotto 35.000 $, 35.000-100.000 $, sopra 100.000 $); categorie da U.S. Census Bureau, formula da BPDA. [V*, sez. 3.5, 4.9] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Pesi: uguali (w = 1) per indicatori e attributi, per mancanza di evidenza empirica a favore di altri; l'unico peso derivato dai dati è quello delle singole policy sull'uso della forza (impatto percentuale sulle uccisioni). [V*, sez. 5] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Normalizzazione: lineare 0-100 con minimo e massimo possibili (non osservati), arrotondata al centesimo; composito normalizzato 0-100; proposta futura di min-max sulla distribuzione reale (Yigitcanlar e Lönnqvist). [V*, sez. 6] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Fonti dati: Numbeo; The Trust for Public Land ParkScore (confini censuari 2010, stime ESRI 2018, orti 2019); Walk Score; Police Use of Force Project e Mapping Police Violence (2013-2019); U.S. Census Bureau; BPDA. [V*, sez. 4] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Risultati: Boston supera Kansas City in tutti e cinque gli indicatori e in tutti gli attributi tranne l'età (Diversity: Age); 100% dei residenti di Boston a 10 minuti a piedi da un parco contro 70% a Kansas City; Boston 9ª e Kansas City 32ª per ParkScore. I punteggi numerici delle tabelle non sono stati restituiti dal riassunto. [V*, sez. 7] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Validazione e limiti dichiarati: dati a scala di città con rischio di generalizzazione; campioni Numbeo piccoli; sicurezza percepita soggettiva; normalizzazione lineare; pesi uguali non supportati; mancano interviste e lavoro sul campo; governance e politiche non incluse; solo due città, con "speculazioni" dichiarate. [V*, sez. 8.4] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Incoerenza interna: Community Connectedness ha cinque attributi in sez. 3.1 e sei in sez. 7. [V*] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Uso in CityScope: l'indice combina indicatori soggettivi e oggettivi per una valutazione rapida di politiche urbane nella City Science Network. [V*, sez. 8.1] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)

### Inferences
- [I] Struttura riusabile: Park Coverage, accessibilità a 10 minuti a piedi, Simpson (1 − Σp²) e composito lineare sono formule generiche. Per Milano gli equivalenti sarebbero copertura di verde per NIL, accessibilità ai servizi con soglia a piedi, diversità sociale per sezione di censimento. L'accessibilità del paper è una somma di capacità raggiungibili: un'impostazione affine a E2SFCA ma senza competizione per la domanda (nel riassunto non compare un rapporto offerta/popolazione) [H: da controllare sul testo che eq. 2 non includa pesi di decadimento].
- [I] Attributi non trasferibili: Numbeo (sondaggio su pochi utenti, non per quartiere), ParkScore (solo USA), Use of Force Policies (contesto statunitense). Il resto richiede dati italiani: ISTAT per sezioni di censimento, Geoportale/DUSAF per verde, GTFS ATM, OpenStreetMap.
- [I] Ricalibrazione per Milano: (1) scala NIL o sezione di censimento, non città; (2) pesi non uguali ma giustificati (consultazione di esperti o abitanti, analisi di sensibilità), perché gli stessi autori dichiarano la mancanza di base per i pesi; (3) normalizzazione sulla distribuzione osservata o su soglie normative, con test di robustezza; (4) validazione con indicatori esterni (salute, sondaggi) e coinvolgimento locale; (5) aggiunta di un attributo di accessibilità economica, assente.
- [H] Per la tesi l'indice può servire più come esempio negativo di governance dell'indicatore (pesi uguali, nessuna partecipazione nella costruzione) che come strumento da adottare.

### Gaps
- PDF non scaricato: formule e pesi vanno verificati sul testo; eq. 2 e eq. 5 in particolare. Punteggi delle Tabelle 3-4 non ottenuti.
- Non è stato verificato in alcuna fonte se e come l'indice sia stato effettivamente implementato in CityScope (sez. 8.1 solo dichiarativa).

---

## Altri lavori del gruppo: accessibilità, prossimità, mixed-use, densità, mobilità; housing (CityHome, Compact Living, robotica modulare, Andorra, Boston, Taipei)

### Takeaway
Non ho trovato, né letto, un articolo scientifico del gruppo di Larson dedicato all'accessibilità/15-minute city con metodo esplicito: la pagina progetto "Understanding the 15 Minute City" non contiene descrizione né pubblicazioni, e i risultati di ricerca sulla città dei 15 minuti sono di gruppi esterni. Sull'abitare, l'unica fonte aperta è un articolo di stampa del 2014 su CityHome (micro-appartamento di circa 18,6 m² con parete trasformabile), senza dati di test né costi. Evidenza scientifica primaria sull'abitare: assente nel materiale raggiunto.

### Cited Findings
- La pagina del progetto "Understanding the 15 Minute City" non ha descrizione né pubblicazioni; indica Kent Larson, Luis Alberto Alonso Pastor, Markus Elkatsha, Margaret Church come membri attuali, ex membri (tra cui Ronan Doorley) e un team NTT DATA come collaboratore. — [MIT Media Lab](https://www.media.mit.edu/projects/understanding-the-15-minute-city/people/)
- L'elenco pubblicazioni di Noyman contiene, nell'area mobilità/Andorra: "Mobility and COVID-19 in Andorra" (IEEE JBHI 26(1), 183-193, 2021), RevUrb (Smart Cities Symposium Prague 2019, DOI 10.1109/SCSP.2019.8805683), MoCho (UrbComp SIGKDD 2019), CityScope Andorra (AAMAS 2018, pp. 1939-1940). Nessuna voce su Taipei o su housing oltre a FindingPlaces. — [Elenco Noyman](https://www.media.mit.edu/people/noyman/publications/)
- Reversed urbanism (Noyman, Doorley, Xiong, Alonso, Grignard, Larson 2019): dati telecom anonimizzati di Andorra, stay-point raggruppati in cluster valutati per dimensione, persistenza e diversità; regressioni lineari multivariate con morfologia e uso del suolo a risoluzione 25-50 m. Servizi e intrattenimento, corsi d'acqua e betweenness centrality della rete stradale sono associati a cluster grandi, diversi e duraturi; amenità educative e parchi hanno effetto negativo. Il modello è associativo; i limiti non sono elencati nella scheda. — [IDEAS/RePEc](https://ideas.repec.org/a/sae/envirb/v46y2019i8p1480-1498.html)
- CityHome (BD+C, 30 maggio 2014): obiettivo di un micro-appartamento di 200 sf (circa 18,6 m²); parete trasformabile con mobili, contenitori, attrezzi per l'esercizio, illuminazione, postazioni di lavoro e intrattenimento, sensori e motori; letto e tavolo estraibili con gesto o voce; scenari d'uso presentati come "potenziali" (palestra, sala per 14 persone, uffici). Costi, test con utenti e dati tecnici non indicati; Kent Larson e Hasier Larrea sono nominati nei riferimenti. — [BD+C](https://www.bdcnetwork.com/mit-researchers-create-home-box-transformable-wall-system-micro-apartments?page=9)
- Riferimento esterno su Milano (non MIT): nel framework di Bruno et al. 2024 Milano risulta già ben ottimizzata per la prossimità, con necessità minima di rilocalizzazione dei POI (Fig. 2B) e un incremento dell'1,6% di popolazione entro 15 minuti nella tabella D (da controllare nella figura). Il modello usa PT medio ai 20 POI più vicini per categoria, soglia 15 minuti, dati OSM e WorldPop; non considera reddito né costo abitativo, e ammette pesi uguali tra categorie e assenza di qualità dei servizi. — [Bruno et al. 2024](https://arxiv.org/pdf/2408.03794)
- Riferimento esterno (non MIT): Zádor et al. 2026 integrano il trasporto pubblico (GTFS, isocrone Valhalla, 10 min di bus + 5 a piedi) nella città dei 15 minuti a Helsinki, Madrid e Budapest, e misurano la mescolanza socio-economica con Gini; usano reddito per sezione o prezzi €/m² come proxy dello status. — [Zádor et al. 2026](https://arxiv.org/html/2604.00699v1)

### Inferences
- [I] Per prossimità/accessibilità il lavoro MIT utile qui è l'indice di benessere (parchi a 10 minuti a piedi) più i risultati su Andorra (Reversed urbanism, relazioni tra uso del suolo e attività). Un gap rispetto a E2SFCA: nessuna fonte letta usa decadimento o competizione per la capacità dei servizi.
- [I] Reversed urbanism è un metodo di associazione tra forma urbana e comportamento con dati telecom; trasferirlo a Milano richiede dati telecom che non risultano disponibili pubblicamente, e la causalità non è dimostrata.
- [I] CityHome è un concetto di progetto di prodotto e non ha evidenza di costo né di sostenibilità economica: il collegamento con il social housing è tramite il kit of parts (componenti trasformabili) ma solo come analogia [H].

### Gaps
- Nessun accesso a: pubblicazioni scientifiche su CityHome/Compact Living/abitazioni robotiche modulari; progetti Boston (se non BRT), Taipei; documentazione CityScope Andorra oltre al titolo; lavori recenti su mixed-use e densità. Non è provata l'assenza: mancano accessi (host bloccati) e il limite di 15 chiamate.
- Il paper Volpe, "Data-driven, evidence-based simulation of urban dynamics" e l'articolo IJEPR 2021 su concorsi di progettazione urbana (che potrebbe riportare indicatori di densità/mixed-use) non sono stati letti.
- Dato non verificato: se esista un articolo MIT sul framework 15-minute city di NTT DATA.

---

## Costo dell'abitare e distribuzione tra gruppi di reddito: come è trattato e lacune

### Takeaway
Nelle fonti raggiunte il costo dell'abitare non è un attributo: l'indice di benessere non misura affordability; il reddito entra solo come dimensione di diversità (3 fasce) e nel commento sull'accesso ai parchi per reddito a Kansas City. CityHome è presentato per la compattezza, senza costi. L'equità distributiva è quindi la lacuna principale rispetto agli obiettivi della tesi.

### Cited Findings
- L'indice di benessere non include costo dell'abitare né affordability; housing compare solo come risorsa materiale nell'introduzione (sez. 1.2, elenco OECD in 1.3); il reddito è presente come "Diversity: Income" in tre fasce e criticato come indicatore econometrico tradizionale (sez. 1.4: "income per household"). [V*] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Equità parziale: nella sez. 7 l'accessibilità ai parchi è riportata per età, reddito e razza; a Kansas City "accessibility varies greatly, depending on age, income, and race", a Boston è 100% per tutte le categorie. [V*] — [Orii et al. 2020](https://www.mdpi.com/2071-1050/12/22/9458)
- Il framework di Bruno et al. 2024 non tratta reddito né costo abitativo e rimanda come sviluppo futuro a fattori socioeconomici; Zádor et al. 2026 trattano la distribuzione per status (basso/alto) con risultati diversi tra città. — [Bruno et al. 2024](https://arxiv.org/pdf/2408.03794); [Zádor et al. 2026](https://arxiv.org/html/2604.00699v1)
- CityHome: costi non indicati nell'articolo di stampa. — [BD+C](https://www.bdcnetwork.com/mit-researchers-create-home-box-transformable-wall-system-micro-apartments?page=9)

### Inferences
- [I] Per il Lab: servirebbe affiancare ad accessibilità e diversità un'ipotesi di reddito residuo (dopo affitto/spesa abitativa) e una disaggregazione per fasce, cosa che l'indice di Orii et al. suggerisce solo in parte con la disaggregazione dei parchi per reddito.
- [H] La diversità di Simpson sul reddito misura mescolanza, non accessibilità economica: un quartiere può essere "diverso" ed essere escludente per i redditi bassi.

### Gaps
- Nessuna fonte MIT letta sul rapporto tra costo dell'abitare e localizzazione dei servizi, né su social housing o politiche di affordability (Boston/Andorra/Taipei non coperti).
- PDF non letti: le affermazioni sopra sono sul riassunto di WebFetch.
