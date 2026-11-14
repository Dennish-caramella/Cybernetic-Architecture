# Bartlett RC10: LinX, Civic Matrix, Urban Sutures (letti il 14/11/2026)

> Note di ricerca, non testo di tesi. Sono progetti di studenti (B-Pro, UCL Bartlett), non ricerche sottoposte a revisione tra pari: servono come ispirazione e come confronto, non come prova. I numeri sociali ed economici sono dichiarazioni nei video, **senza fonte mostrata** [S]. Marche: [V] visto o letto direttamente; [S] dichiarato nel materiale, non verificato; [I] inferenza mia; [L] lacuna.

## Cosa ho letto, e con che limiti
- **Pagine**: testo integrale delle tre pagine [V] (autumn2026 … /linx, autumn2025 … /rc10-project-3-team-civic-matrix, autumn2026 … /urban-sutures).
- **Video**: scaricati dagli embed Vimeo, tenuti solo nello scratchpad (non nel repo: diritti di terzi).
  - *Civic Matrix* (11 min 24 s): nessuna trascrizione disponibile, audio non trascritto. Ho guardato tutti i 69 fotogrammi estratti ogni 10 s e 5 a piena risoluzione. Le diapositive sono comprensibili da sole, ma una diapositiva più breve di 10 s può essermi sfuggita.
  - *LinX* (8 min 20 s) e *Urban Sutures* (8 min 58 s): ho letto le trascrizioni automatiche di Vimeo, con possibili errori di trascrizione, e 7 fotogrammi a piena risoluzione. **Non ho guardato tutti i fotogrammi** di questi due.
- "Frame by frame" in senso letterale (15.000 fotogrammi a video) non era realistico: campionamento ogni 10 s.

## 1. Civic Matrix (RC10, Year 1; Xiao Li, Khedkar, Mai, Xu) [V]
**Tesi del progetto**: più metri quadri non significano più comfort; una struttura fissa ospita moduli mobili (pareti, arredi robotici) riassegnati in tempo reale secondo l'uso.
**Parte sociale ed economica** (diapositive "Core problem 01–03"):
- Londra cresce e si comprime: popolazione 1801–2024 (etichetta del grafico: 10,1 milioni nel 2024) e nuove abitazioni per municipio 2006–2016, con Tower Hamlets al massimo (+22.000) [V come diapositiva; origine dei dati non mostrata, S].
- Comfort sacrificato alla densità: casi di confronto (Alexandra Road, edilizia pubblica a Hong Kong) e una tabella di spazio pro capite per paese [V; valori non leggibili al campionamento, L].
- Bisogni che cambiano: tabella 2015–2024 del lavoro da remoto e ibrido (da 13,9% nel 2015 a 46,6% nel 2020, poi 30,0, 16,0, 13,0, 13,0% remoto e 28% ibrido dal 2021) e dei lavoratori della gig economy (da 1,5 milioni e 4,5% nel 2015 a 10,7 milioni e 32,4% nel 2024) [S]. Non ho potuto verificare i dati. Il valore 2024 per la gig economy mi sembra alto: lo tratterei come non attendibile finché non si trova la fonte [I].
**Meccanismo partecipativo** (utile per noi):
- Un'app raccoglie il profilo (età, numero di persone, durata d'uso, **prezzo atteso al giorno**) e le funzioni desiderate con le superfici; poi un "AI-manager" (LLM) in chat estrae i bisogni (lavoro, vita, svago) in una nuvola di parole; il sistema genera le soluzioni di spazio [V].
- Algoritmo genetico con tre criteri di fitness (massimizzare celle-giardino, il loro rapporto, minimizzare il rapporto corridoio) su un reticolo di celle 3×3×3 m [V].
- Calendario degli orari per gli spostamenti dei robot [V].
- Nessun modello economico visibile oltre al prezzo atteso inserito dall'utente [L].

## 2. LinX (RC10, 2026; Amandari, Costa, Jamalzadeh, Ubonchan) [V pagina e trascrizione; S per i numeri]
**Co-living a Londra con legno di recupero**, per tre gruppi: lavoratori essenziali, studenti, giovani professionisti.
- **Affermazioni sociali ed economiche** (nel video, senza fonte) [S]:
  - la spesa di manutenzione per l'edilizia sociale è scesa dal 32% al 24% della produzione dal 1997, presentata come "deliberata mancanza di investimenti";
  - lavoratori essenziali fino all'80% del reddito in affitto;
  - studenti con contratti poco trasparenti o che abbandonano gli studi per i costi.
- **Un grafico** mostra per professione quanti municipi londinesi sono accessibili a un monolocale: scende da circa 25 (insegnante di scuola superiore) a 0 per quasi tutte le altre professioni [V come fotogramma; valori letti a occhio, I].
- **Meccanismi utili**:
  - quattro tipi di utente (studente, professionista, famiglia, ibrido), ciascuno con regole di occupazione e di comunità (zone cuscinetto, adiacenze, piani); quattro schemi di massa (mat, corti, "grotta", "gruviera");
  - piattaforma "London Scan" che legge i vuoti con OpenStreetMap;
  - assegnazione travi-recuperate/progetto con l'algoritmo ungherese (assegnazione ottima) e legno nuovo di riserva [V];
  - cooperazione designer-algoritmo: "il designer cura, l'algoritmo costruisce".
- **Critica per la nostra tesi**: la zonizzazione per tipo di utente rischia l'omogeneità che abbiamo escluso (niente ghetti di interessi uguali) [I]. Non c'è un modello economico (costi, canoni, chi finanzia) [L].

## 3. Urban Sutures (RC10, 2026; Koo, Kim, Leon Cardenas, Yamout, Vitolo) [V pagina e trascrizione; S per i numeri]
**Infill in Londra per "cucire" la città**, con facciate fuse dal contesto e blocchi prefabbricati in calcestruzzo.
- **Dato sociale**: Londra ha bisogno di 88.000 case all'anno e ne consegna circa 5.000, "94% di fallimento" [S]. Il fotogramma mostra i due valori, ma non la fonte; i due numeri non coincidono con le stime che ricordo [I]: da verificare prima di citarli.
- **Rilevante per la Base L**: una piattaforma di scansione dei vuoti (LiDAR del governo britannico, OpenStreetMap, dati ambientali) che individua i siti di infill (tra edifici, muri ciechi, strutture abbandonate, brownfield) con quattro criteri: superficie edificabile, accesso solare, esposizione acustica, accessibilità [V come testo].
- Nessuna validazione su verità di terreno e nessun dato economico o sociale oltre al numero iniziale [L].

## Cosa ne ricaviamo per la tesi [I]
1. **Domanda e budget**: Civic Matrix raccoglie il *prezzo atteso* come dato dell'utente. Per noi è l'ancora che manca per la domanda reale (vedi la domanda di Dennis del 14/11): la domanda si dichiara, non si deduce dai registri. Aggancio con il vettore dei desideri (budget, ancore, pesi).
2. **Estrazione dei bisogni con un LLM** (chat → parole chiave → soluzioni): schema simile al nostro "teach-back"; da citare come esempio di interfaccia, non come validazione.
3. **Assegnazione**: l'algoritmo ungherese di LinX è un caso di ottimizzazione (B2) usato per i materiali; ricorda che la scelta dell'algoritmo cambia chi vince.
4. **Vuoti urbani**: i criteri di Urban Sutures (area edificabile, sole, rumore, accessibilità) confermano la direzione della Base L e suggeriscono attributi per l'analisi A2 (accessibilità) e un'analisi di rumore, che oggi non abbiamo [I].
5. **Diversità sociale**: LinX raggruppa per tipo di utente. Va contrapposto alla nostra scelta di mix per età e condizione.
6. **Mancanze comuni ai tre progetti**: nessun modello economico dei costi o dei canoni, nessuna validazione con persone reali, dati sociali senza fonte. Sono i punti su cui la nostra tesi può differenziarsi [I].

## Da fare
- Cercare le fonti dei numeri se vogliamo citarli (GLA, ONS, Shelter) e verificare gli 88.000/5.000 e la quota gig economy.
- Guardare tutti i fotogrammi di LinX e Urban Sutures se servono dettagli tecnici.
