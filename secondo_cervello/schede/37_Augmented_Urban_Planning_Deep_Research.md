# Deep research: Augmented Urban Planning, digital twin urbani, IA e partecipazione

Data: 2026-10-25. Companion della scheda 37. Metodo: tre ricerche parallele; le note grezze (in inglese, con etichette [V] aperta / [U] solo in risultati di ricerca) sono in `37_note_ricerca_grezze/`. **Quasi tutto è verificato a livello di abstract o di pagina riassunta, non di testo integrale.** Cifre da ricontrollare sui PDF prima di ogni uso in tesi. Etichette: `[S]` fonte, `[I]` inferenza, `[H]` ipotesi, `[L]` lacuna.

## 1. Che cosa è la fonte

La pagina indicata è il record di una tesi di dottorato, non di un articolo: Azadi (TU/e, 2026), embargo del testo fino al 23-09-2027. Dettagli nella scheda 37. Gli articoli collegati (Smart Cities 2025; Environment and Planning B 2026; CUPUM 2025; SSRN da verificare) sono i punti d'accesso leggibili. Il PDF dell'articolo su Environment and Planning B è dichiarato ad accesso aperto (CC BY-NC) sul record TU/e: **è la prima lettura da fare** (non apribile da questa sessione).

## 2. Il campo: perché gli UDT non reggono la pianificazione (tutti verificati a livello di abstract)

- Nessuna definizione condivisa di digital twin urbano: Ketzler et al. 2020, Built Environment 46(4), DOI 10.2148/benv.46.4.547 `[S]`.
- Stato sperimentale e aspettative irrealistiche da investimenti pubblico-privati: Caprari et al. 2022, Sustainability 14(10) `[S]`.
- Partecipazione limitata dal design dello strumento: De Jaeger e Swerts 2026, Cities 168:106498, DOI 10.1016/j.cities.2025.106498 (Rotterdam, «limits-by-design») `[S]`. Il riferimento a Lefebvre non risulta nella fonte `[L]`.
- «Technocentric», pochi input degli stakeholder, tabella di marcia partecipativa: Altındaş et al. 2026, Urban Planning, DOI 10.17645/up.12635 `[S]`. Co-autore del TU/e: vicinanza al gruppo di Azadi è `[I]`.
- Prototipo VR a Herrenberg con 39 rispondenti, campione non rappresentativo, nessuna prova su un intero processo: Dembski et al. 2020, Sustainability 12:2307 `[S]`.
- Strumenti di pianificazione statici e poco partecipati; usi a Zurigo spesso pilota e auto-dichiarati: Schrotter e Hürzeler 2020, PFG 88:99 `[S]`.
- Quadro dei modelli, da aggregati ad agent-based: Batty 2024, Nature Computational Science 4:192, DOI 10.1038/s43588-024-00606-7 (solo abstract) `[S]`.
- Grafi/ontologie: CityGML 3.0 tradotto in ontologie OWL (Vinasco-Alvarez et al. 2024, ISPRS Annals, DOI 10.5194/isprs-annals-X-4-W4-2024-231-2024) `[S]`.
- Gap tra PSS di ricerca e di pratica: Luque Martin e Pfeffer 2020 (Handbook of Planning Support Science, cap. 18) `[S]`.
- Strumenti di personalizzazione abitativa costruiti senza input degli utenti futuri: Raposo e Eloy 2022 (abstract IAPS) `[S]`.

`[I]` Lettura trasversale: tre forme dello scarto: definizione vaga, status sperimentale, partecipazione limitata dal design e dalla governance. Nessuno degli articoli aperti tratta la localizzazione di social housing `[L]` (campione piccolo).

**Non verificato** (non cercato o non aperto): canone di teoria della pianificazione (Lindblom, Schmidt, Healey, Forester, Innes e Booher, Arnstein, Sanoff); Deng, White, Weil, Shahat; Batty 2018; Klosterman, Pelzer, Brömmelstroet; ontologie per valori e stakeholder; SOLID; Maptionnaire.

## 3. IA e deliberazione

- *Habermas Machine* (Tessler et al., Science 2024): 5.734 partecipanti più un'assemblea virtuale rappresentativa di 200; dichiarazioni dell'IA preferite a quelle dei mediatori umani circa il 56% delle volte; accordo in aumento di circa 6–9 punti; vedere le opinioni altrui senza mediazione IA non cambia nulla. Letta tramite mirror PDF; **DOI non confermato** (10.1126/science.adq2852 dedotto dall'URL) `[S]/[L]`. Critica di Sætra (blog CACM): «deliberazione» è un termine improprio, fiducia ed empatia non misurate, rischio di illusione del consenso `[S]`.
- Zhou et al., arXiv 2402.17161: pianificatore GPT-4V e circa 1.000 agenti-residenti per regione discutono un piano d'uso del suolo, testato su due regioni di Pechino; i bisogni sono generati dagli stessi agenti LLM, quindi non riflettono residenti reali; omette costo del suolo e proprietà `[S]`. `[I]` È il precedente più vicino all'idea di «modello che sostituisce i bisogni delle persone» e mostra il punto debole che i dati reali di preferenza colmerebbero.
- Flechtner, arXiv 2608.10186 (preprint, non peer reviewed): su 1.980 esecuzioni LLM, i gruppi di LLM partono da circa un terzo della diversità di prospettive umane; i guadagni su temi controversi sono negativi `[S]`.
- Roy, Lessig, Tang, arXiv 2503.11714: position paper su Polis e vTaiwan, non valutazione di esiti `[S]`.
- Zali et al., ISPRS 2026: piattaforma di partecipazione con chatbot LLM, prototipo senza valutazione quantitativa `[S]`.
- Safransky 2020, IJURR, DOI 10.1111/1468-2427.12833: gli strumenti algoritmici nascondono scelte politiche; caso di una valutazione proprietaria dei valori di mercato in città USA, rischio di nuovo *redlining* `[S]`. `[I]` Analogo diretto dell'uso del costo del suolo come criterio di localizzazione.
- Zhai et al., arXiv 2406.13724: rete neurale su grafi eterogenei per inferire l'uso del suolo da dati di trasporto a Londra; non è un modello di localizzazione abitativa `[S]`.

## 4. Strumenti esistenti (solo documentazione pubblica)

UrbanSim: microsimulazione open source (Python) di famiglie, imprese, developer; limiti documentati: norme vincolanti, comportamento stabile `[S]`. Envision Tomorrow: richiede ArcGIS 10.4.1; licenza indicata CC0 4.0 da una pagina aggregatrice, da verificare `[S]/[L]`. Autodesk Forma: solo dichiarazioni del fornitore (massing, sole, vento, rumore); nulla su accessibilità economica o partecipazione `[S]`. MIT CityScope: pagina di alto livello, senza meccanica `[S]`. TestFit, Urban Analytics Lab: non aperti `[L]`.

## 5. Contesto italiano (parziale)

Dati OMI (valori immobiliari): min/max €/m² semestrali per zona, dal 2016 nel repository consultato; scaricamento tramite Fisconline o Entratel; termini non da licenza aperta; circa il 10% dei record con valori zero; una sentenza del 2018, come citata dal repository, li dice indicazioni di massima. Fonte secondaria (repo ondata) `[S]`. **Non verificati**: L.R. Lombardia 18/2019 e geoportale delle aree di rigenerazione, struttura del PGT e indici (IF/IT), norme sull'edilizia residenziale sociale, dati ISTAT, OSM e open data comunali, GIS-MCDA per brownfield, città dei 15 minuti, Decidim `[L]`.

## 6. Che cosa significa per il progetto di dottorato proposto (inferenze e ipotesi)

1. `[I]` Niente di quanto verificato mostra un sistema in cui le scelte dei residenti tra lotti candidati riaddestrano il modello di localizzazione: lì c'è spazio di contributo. Resta `[H]`: va controllato con una rassegna sistematica.
2. `[H]` Rendere i pesi dei criteri (costo, indice, accessibilità) oggetto di partecipazione è una risposta al problema «chi scrive la funzione obiettivo». Non è un risultato pubblicato. Si collega alla tensione già aperta nel corpus (Bhooshan contro Team Robotic, in `stato_avanzamento.md`).
3. `[I]` L'AUP supplisce il lato procedurale (ontologia, grafo, valutazione sulle tre dimensioni) ma tratta stakeholder esperti: la differenza con «le persone al ventre della gaussiana» è sostanziale e va dichiarata.
4. `[I]` Rischi da tenere in primo piano: costo del suolo come criterio che riproduce il mercato (Safransky); consenso illusorio prodotto dalla mediazione IA (Sætra); agenti sintetici al posto di persone (Zhou, Flechtner).
5. `[H]` UrbanSim può fare da baseline per il comportamento dei developer; da verificare sul codice e sulla licenza.
6. Un confronto con Pask/Alexander sul tema «funzione obiettivo» non è stato trovato in letteratura `[L]`: sarebbe una lettura originale dell'autore, da non presentare come stato dell'arte.

## 7. Prossimi passi di verifica

1. Leggere il PDF CC BY-NC dell'articolo su Environment and Planning B e il PDF CUPUM (OSF).
2. Aprire la pagina SSRN (DOI 10.2139/ssrn.6571117) e cercare repository del toolbox.
3. Controllare DOI e numeri di Tessler et al.
4. Coprire le lacune del contesto italiano con fonti primarie (norme regionali, PGT, OMI, ISTAT).
