# FindingPlaces (Amburgo) e casi partecipativi MIT City Science / CityScope

AVVISO DI METODO (leggere prima). I PDF non hanno potuto essere scaricati con curl: il proxy di sessione risponde 403 al CONNECT per arxiv.org, export.arxiv.org, dspace.mit.edu, www.media.mit.edu, doi.org (verificato con curl e con /__agentproxy/status; non aggirato). L'unico accesso è stato WebFetch, che restituisce un riassunto di modello e non il testo. Quindi NESSUNA fonte qui è `verificata` (PDF intero letto). Tutte sono `parziale`. Le cifre sotto sono riportate dal riassunto WebFetch del PDF arXiv con riferimenti di sezione; vanno ricontrollate sul PDF. Tag: [V*] = letto in riassunto WebFetch con sezione indicata, NON nel PDF integrale; [I] inferenza; [H] ipotesi.

## Fonti (registro)
| Fonte | Stato |
|---|---|
| Noyman, Holtz, Kröger, Noennig, Larson (arXiv 2018, v. originale 2017), "Finding Places: HCI Platform for Public Participation in Refugees' Accommodation Process", Procedia Computer Science 112, DOI 10.1016/j.procs.2017.08.180 (DOI dedotto dal riassunto della pagina arXiv). https://arxiv.org/abs/1811.10123 (PDF: /pdf/1811.10123) | parziale (abstract + riassunto del PDF via WebFetch) |
| Noyman, Sakai, Larson (2019), "CityScopeAR: Urban Design and Crowdsourced Engagement Platform", arXiv:1907.08586. https://arxiv.org/abs/1907.08586 | parziale (solo abstract) |
| Noyman (2022), "CityScope: An Urban modeling and Simulation Platform", PhD, MIT Media Arts and Sciences, rel. K. Larson. https://dspace.mit.edu/handle/1721.1/145128 ; PDF indicato dalla pagina: https://dspace.mit.edu/bitstreams/b8614805-bbd5-4683-8a65-9f807e3d9dc9/download | parziale (solo abstract; PDF non scaricabile, 403) |
| Alonso, Zhang, Grignard, Noyman, Sakai, ElKatsha, Larson et al. (2018), "CityScope: A Data-Driven Interactive Simulation Tool for Urban Design. Use Case Volpe", International Conference on Complex Systems, Springer, pp. 253-261. https://www.media.mit.edu/publications/cityscope-a-data-driven-interactive-simulation-tool-for-urban-design-use-case-volpe | parziale (pagina publicazione; l'elenco autori è troncato "et al."; DOI Springer non verificato) |

## 1. Come funziona la selezione dei lotti ad Amburgo

### Takeaway
Il processo è un filtro GIS a tre classi di inadeguatezza, usato come base visiva per 34 workshop con cittadini; i partecipanti propongono, l'amministrazione vaglia. I pesi numerici non sono dichiarati nell'articolo, per quanto riportato dal riassunto.

### Cited Findings
- Strati: proprietà comunale (disponibilità), uso attuale della particella, vincoli (es. riserve naturali); aerofoto e OpenStreetMap solo per visualizzazione [V*, §3.3] — [arXiv](https://arxiv.org/pdf/1811.10123)
- Criteri molto restrittivi (inadeguatezza alta): tutela naturalistica, cimiteri, forte rumore. Criteri meno restrittivi (media): parchi, aree ricreative, vicinanza a linee ad alta tensione [V*, §3.3] — stessa fonte
- Le classi: alta = aree significativamente toccate da criteri molto restrittivi; media = non significativamente toccate da questi ma significativamente da criteri meno restrittivi; bassa/nulla = non toccate da criteri molto restrittivi e con criteri meno restrittivi su meno del 50% dell'area. Il 50% è l'unica soglia numerica riportata; le soglie di alta e media non sono definite [V*, §3.3] — stessa fonte
- Pesi: gli strati sono "intersected and weighted", nessun peso numerico dichiarato [V*, §3.3] — stessa fonte
- Capacità: nessun metodo (es. mq/persona) in §3; la capacità potenziale è "computed and indicated" (§4.3) senza spiegazione; esempio illustrativo di "data brick" da 50 persone [V*] — stessa fonte
- Numero di particelle del dataset iniziale: non riportato [V*] — stessa fonte
- Workshop: 34 da due ore, maggio-luglio 2016, presso HCU, sette distretti; quasi 400 partecipanti; fino a 20 invitati, media 11; un solo workshop per distretto per persona [V*, §4.1] — stessa fonte
- Tre stazioni: I città (domanda guida: quali particelle comunali sono adatte; obiettivo 20.000 posti); II distretto (scelta di aree di interesse su mappa colorata per classe); III quartiere (esame particelle, segnaposto, proposte tra 40 e 1.500 posti) [V*, §4.3] — stessa fonte
- Esito: 161 localizzazioni proposte, quasi 24.000 posti (oltre l'obiettivo); circa tre quarti giudicati inadatti in prima valutazione, 44 fattibili; 24 escluse dopo esame di dettaglio; 6 con raccomandazione di attuazione e 10 per pianificazione futura; i 6 ospiterebbero circa 750 persone, ~4% dell'obiettivo [V*, §4.4] — stessa fonte

### Inferences
- [I] Il rapporto 24.000 proposti vs ~750 realizzabili (~3%) mostra che il filtro GIS lascia passare molto che il vaglio amministrativo scarta: la partecipazione produce molte proposte, ma il collo di bottiglia è la fattibilità.
- [I] Nessun "algoritmo di selezione" decide: la parte computazionale è una classificazione di vincoli che orienta lo sguardo.

### Gaps
- Pesi numerici, soglie alta/media, formula di capacità, dimensione del dataset: non ottenibili senza il PDF integrale (o dal sito/GitHub di CityScope). Da verificare.
- Le cifre sopra provengono da un riassunto automatico: proprio il limite della prima passata. Rilettura integrale necessaria.

## 2. Chi ha deciso cosa; limiti dichiarati e non dichiarati

### Takeaway
Cittadini: proponevano e discutevano; moderatori: guidavano; Central Refugees Coordination Staff: screening di fattibilità; autorità di pianificazione: studio dei lotti superstiti. La decisione finale resta amministrativa.

### Cited Findings
- Ruoli come sopra [V*, §4] — [arXiv](https://arxiv.org/pdf/1811.10123)
- Limiti dichiarati: tempi stretti; workshop solo presso HCU (probabile bias di selezione); dati urbani limitati; difficoltà dei non esperti con i contenuti di pianificazione e l'orientamento sulla mappa; rischio che il preprocessing dei dati manipoli gli esiti (es. codifica colore suggestiva) e di strumentalizzazione politica [V*, §5] — stessa fonte
- Gli autori non affermano un effetto dimostrato sulle decisioni finali: parlano di accettazione costruita e feedback di qualità ("built up acceptance... triggered high-quality feedback") [V*] — stessa fonte
- Noyman 2022 conclude che CityScope ha supportato e talvolta sostituito il processo decisionale convenzionale; casi: alloggi per rifugiati in Germania, mappatura sicurezza a Guadalajara, co-creazione trasporto a Boston [V*, abstract] — [DSpace](https://dspace.mit.edu/handle/1721.1/145128)

### Inferences
- [I] Limiti non dichiarati plausibili: la mappa di inadeguatezza pre-colora la scelta (effetto di framing, in parte ammesso); campione auto-selezionato e urbano-istruito; assenza di valutazione indipendente; criteri di scarto amministrativi opachi. [H] Gli abitanti dei quartieri effettivamente interessati potrebbero essere sotto-rappresentati.

### Gaps
- Nessuna valutazione indipendente o follow-up sugli insediamenti realizzati trovata (non cercata a fondo: ricerca bloccata).

## 3. Altri casi del gruppo ed evidenza di efficacia

### Takeaway
Esistono Volpe (Kendall Square), Guadalajara, Boston, ecc., ma con le fonti accessibili non emerge alcuna valutazione indipendente.

### Cited Findings
- CityScope Volpe: piattaforma data-driven con interfaccia tangibile applicata al sito Volpe, Cambridge MA; la pagina non riporta valutazioni o test con utenti [V*] — [MIT Media Lab](https://www.media.mit.edu/publications/cityscope-a-data-driven-interactive-simulation-tool-for-urban-design-use-case-volpe)
- CityScopeAR: tabletop fisico + realtà mista, rete distribuita, test e deployment reali dichiarati nell'abstract [V*, abstract] — [arXiv](https://arxiv.org/abs/1907.08586)
- Andorra, Taipei, Helsinki: non verificati in questa sessione. Da verificare.

### Inferences
- [I] L'evidenza è prevalentemente autoreferenziale (articoli dei membri del gruppo).

### Gaps
- Letteratura indipendente di valutazione: non trovata/non accessibile. Andorra, Taipei, Helsinki, Boston: nessuna fonte aperta.

## 4. Cosa cambia per il social housing a Milano

### Takeaway
[H] FindingPlaces è trasferibile come metodo di preselezione dei lotti (vincoli, proprietà pubblica), non come strumento di decisione.

### Cited Findings
- Nessun fatto citato: la sezione è interpretativa.

### Inferences
- [I] Differenze: Amburgo era un'emergenza con obiettivo numerico (20.000 posti) e proprietà comunale; il social housing milanese ha vincoli di mix, ERP/ERS, oneri e comparti già pianificati.
- [H] Utile: layer pubblici (patrimonio comunale/MM/Aler), classi di inadeguatezza esplicite e pubblicamente discusse, tracciabilità dei pesi (colmando la lacuna di opacità di Amburgo), valutazione di fattibilità amministrativa a valle.

### Gaps
- Dati milanesi e normativa non esaminati in questo compito.

## Prossimo passo raccomandato
Eseguire la lettura integrale da un ambiente con accesso a arxiv.org e dspace.mit.edu (scaricare i tre PDF indicati e usare pdftotext), poi verificare pesi, soglie e capacità e promuovere le fonti a `verificata`.
