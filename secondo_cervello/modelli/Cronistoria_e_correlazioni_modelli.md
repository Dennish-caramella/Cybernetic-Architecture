# Cronistoria e correlazioni tra modelli matematici, filosofici e teorici

Data: 2026-10-20. Base: due passate di ricerca web con verifica avversaria (run `wcvx37469` del 2026-10-19 e `w2ewgvgos` del 2026-10-20), più i riscontri nel corpus `03_Analisi Approfondite/`.

**Stato di questo file.** È una ricerca di lavoro, non un capitolo di tesi. Le affermazioni sono classificate così:

- **[C]** confermata dalla verifica (voto di almeno due verificatori su tre), su fonte primaria o secondaria dichiarata.
- **[C-s]** confermata solo su fonte secondaria (Wikipedia, enciclopedie, blog, profili d'autore). Da controllare sul testo primario.
- **[I]** interpretazione mia o della ricerca, non attribuibile a una fonte.
- **[L]** lacuna: nessuna affermazione verificata. Va cercata una fonte primaria.
- **[R]** affermazione scartata dalla verifica. Non usare la formulazione indicata.
- **[D]** da verificare: attribuzione o dato riportato da una fonte, non confermato.

Le fonti primarie citate (von Neumann 1966, Moore 1962, Ashby 1956, Nash 1950/1951, Langton 1984) **non sono state lette per intero**, tranne l'abstract di Langton e il testo di Nash nella versione OCR. Le citazioni tra virgolette vanno ricontrollate sul libro o sull'articolo.

---

## Capitolo 1. Teoria dei sistemi di Ludwig von Bertalanffy

**Cronistoria.**

- Bertalanffy (1901–1972) è generalmente riconosciuto come il fondatore della *General Systems Theory* (GST) [C-s, voto 1-2 sulla formulazione "padre della GST"; fonte Systems Thinking Alliance].
- La GST è rappresentata come fondamento di tutte le scienze dei sistemi [R, voto 0-3]: l'affermazione è scartata. Va presentata come programma, non come fondamento riconosciuto.
- Il rapporto con la cibernetica cambia nel tempo. Secondo Drack e Pouvreau (2015, *International Journal of General Systems* 44(5): 523–571, PMC4610108), la cibernetica è una parte della GST nel 1951, un "sottoclasse ristretta" nel 1969, e non una teoria generale dei sistemi nel 1967 [C-s, voto 2-1 sull'ambivalenza].
- Ashby è presentato come mediatore tra GST e cibernetica [C-s, voto 3-0; fonte unica: Drack e Pouvreau, sezione 4.4].
- Un confronto tra Bertalanffy e von Neumann (Wiener e Ashby più vicini alla GST di von Neumann) è scartato [R, voto 0-3].

**Lacune.** I testi primari di Bertalanffy (1951, 1967, 1969) non sono stati letti. Non c'è nessuna fonte verificata che colleghi Bertalanffy agli automi cellulari o all'autoriproduzione [L].

---

## Capitolo 2. Legge della varietà richiesta di W. Ross Ashby (1956)

**Definizione e formulazione.**

- La varietà è il numero di elementi distinguibili di un insieme, oppure il suo logaritmo binario, in bit [C-s, voto 3-0; Wikipedia cita Ashby 1956, pp. 125–126].
- La legge è una condizione **necessaria ma non sufficiente** per il controllo [C-s, voto 3-0; Wikipedia cita Ashby 1956, pp. 130, 207–208]. Un regolatore richiede almeno tanta varietà quanto le perturbazioni da contrastare.
- La formula "solo la varietà distrugge la varietà" (*only variety can destroy variety*) è attribuita al libro del 1956 [D]. Nella verifica il testo di Wikipedia la riporta in forma incompleta, e l'attribuzione alla pagina di Ashby è stata scartata [R, voto 0-3]. Va controllata sul testo primario prima di essere citata.
- La formulazione "un regolatore deve avere almeno tanta varietà quanto il sistema controllato", attribuita a Glanville, è scartata [R, voto 0-3].

**Correlazione matematica con Shannon.** Ashby collega la sua legge al teorema di Shannon sulla rimozione del rumore da un canale di correzione (Shannon e Weaver 1949) [C-s, voto 2-1]. La varietà è il ponte tra cibernetica e teoria dell'informazione.

**Gioco a due giocatori.** Nel capitolo 11 del libro del 1956 (p. 202) la regolazione è analizzata come gioco a due giocatori: una parte sceglie le perturbazioni, l'altra la risposta [C-s, voto 2-1]. La struttura è tabellare e combinatoria, non una teoria dei giochi con payoff e minimax [C-s, confidenza bassa]. **Ashby non applica la teoria dei giochi di von Neumann e Morgenstern** [I].

**Teorema del buon regolatore** (Conant e Ashby, 1970). L'attribuzione alla formulazione "ogni regolatore massimamente efficace e semplice è isomorfo al sistema regolato" è scartata come finding della fonte arXiv 2008.04071 [R, voto 0-3]. Il teorema è citato nelle fonti come risultato di Conant e Ashby; non l'ho verificato sul testo [D].

**Estensione di Aulin.** La legge della conoscenza richiesta (*requisite knowledge*) è scartata [R, voto 0-3].

**Lacune.** Il libro del 1956 non è stato letto. Non c'è nessuna fonte verificata che colleghi la legge della varietà ai vicinati degli automi cellulari [L].

---

## Capitolo 3. Vicinato di von Neumann e vicinato di Moore

Il tuo riferimento è agli automi cellulari. Qui le definizioni, la cronistoria e i rapporti con Moore e con l'autoriproduzione.

**Definizioni.**

- **Vicinato di von Neumann**: le quattro celle ortogonalmente adiacenti (distanza di Manhattan 1) [C-s, voto 3-0; Wikipedia e Esolangs]. Il centro è escluso nella definizione standard, ma molte convenzioni lo includono nella regola di aggiornamento: la distinzione va dichiarata caso per caso [I, da una formulazione scartata].
- **Vicinato di Moore**: le otto celle della griglia 3×3 intorno alla cella centrale (distanza di Chebyshev 1). Contiene il vicinato di von Neumann più le quattro celle diagonali [C-s, voto 3-0].
- Un vicinato di Moore di "nove celle" con il centro incluso è una convenzione possibile, non la definizione standard [R, voto 0-3 sulla formulazione che la presenta come definizione].
- Il vicinato di 5 celle (centro più quattro) è usato nell'automa di von Neumann e nei modelli evoloop di Sayama (9 stati, 5 vicini) [C-s, voto 3-0, arXiv 2402.03961v2]. L'identificazione di questo vicinato con quello di von Neumann è un'inferenza dal numero di celle [I].

**Attribuzione del nome.** Il vicinato di Moore porta il nome di Edward F. Moore [C-s, voto 2-1, con fonti deboli]. La pagina di Moore non dice che abbia coniato il nome [I].

**Cronistoria.**

- **Anni Quaranta–Cinquanta.** Von Neumann tiene lezioni nel 1949 sull'automa autoriproducente e lavora al progetto intorno al 1952–53 [C-s, voto 3-0].
- **Il costruttore universale.** Von Neumann chiama la sua macchina ipotetica *Universal Constructor* [C-s, voto 2-1; Spektrum 2012]. L'automa è a 29 stati per cella, su griglia bidimensionale [C-s, voto 3-0]. Il testo di riferimento è von Neumann e Burks (1966), *Theory of Self-Reproducing Automata*, pubblicato postumo [C-s; testo primario non letto].
- **La semplificazione di Codd (1968)** riduce il numero di stati a 8 [D, dato di fonte secondaria non verificato].
- **Moore (1962).** *Machine models of self-reproduction*, *Proceedings of Symposia in Applied Mathematics* 14, pp. 17–33, American Mathematical Society [C, voto 3-0; con un estratto della Wellcome Collection]. Il testo primario non è stato letto.
- **Langton (1984).** *Self-Reproduction in Cellular Automata*, *Physica D* 10, pp. 135–144. Un loop autoriproducente più semplice del costruttore di von Neumann. L'abstract dice: la capacità di costruzione universale è condizione **sufficiente ma non necessaria** per l'autoriproduzione [C, voto 2-1; fonte primaria, abstract]. La citazione condensata nella ricerca è inesatta: usare l'abstract originale.

**Teorema del Giardino dell'Eden.** L'attribuzione a Moore (1962) e Myhill (1963) è nella forma "un automa cellulare in spazio euclideo è localmente iniettivo se e solo se è suriettivo". La formulazione è scartata [R, voto 0-3]. La pagina di Moore dice che è accreditato del teorema con Myhill [C-s, dato secondario].

**Il rapporto tra Moore e von Neumann.** È il punto più importante per la tua tesi, e non è documentato. La letteratura cita spesso i due insieme, ma la pagina di Moore non menziona von Neumann né i suoi automi autoriproducenti [C-s, voto 3-0, ma verifica su riassunto]. Se il lavoro del 1962 discuta esplicitamente von Neumann, va verificato sul volume AMS 14 [L].

**Correlazione.** Il vicinato definisce che cosa vuol dire "locale" in un automa. Von Neumann (4 celle) e Moore (8 celle) danno due nozioni di località con diversa connettività.

- Dal punto di vista teorico: la scelta del vicinato decide che cosa un elemento può "sentire". È lo stesso problema che il corpus incontra nella stigmergia (analisi 12, Meyboom e Reeves: le funzioni "sentono l'odore" delle altre attraverso il feromone) [I].
- Dal punto di vista filosofico: il vicinato è una scelta di che cosa conta come vicino, cioè una definizione di relazione. Questo collega il vicinato alla mereologia di Husserl (capitolo 6), dove la relazione di dipendenza tra parti è una relazione diversa dalla relazione parte-tutto [I, nessuna fonte verificata].

---

## Capitolo 4. Teoria dei giochi di John Nash

**Formulazione.**

- **Equilibrio di Nash**: in un gioco non cooperativo n-persona, una n-upla di strategie miste in cui la strategia di ciascun giocatore massimizza il suo payoff, tenendo fisse le strategie degli altri [C, voto 3-0; fonte primaria Nash 1951, *Annals of Mathematics* 54(2): 286–295].
- **Teorema di esistenza**: ogni gioco finito ha almeno un punto di equilibrio [C, voto 3-0; Nash 1951, Theorem 1]. La dimostrazione del 1950 (*PNAS*) usa il teorema di Kakutani; quella del 1951 il teorema di Brouwer [C, confidenza alta].
- Il testo del 1951 è stato ricevuto l'11 ottobre 1950 [C].

**Rapporto con von Neumann e Morgenstern (1944).** Nessuna affermazione verificata [L]. Va letto il testo del 1944 (*Theory of Games and Economic Behavior*). Un punto da chiarire: il gioco a somma zero di von Neumann e Morgenstern non è il gioco non cooperativo di Nash [I].

**Uso in architettura e pianificazione urbana.** Nessuna affermazione verificata [L]. Il corpus però ha esempi concreti: SpaceFighter (analisi 21) cita Nash, Maynard Smith e Schelling per la città come matrice di payoff; il Day 2 (analisi 30) dichiara un equilibrio di Nash in un gioco che è a somma zero [dal corpus, da verificare sul video].

**Legame con gli automi cellulari.** Nessuna fonte verificata [L].

---

## Capitolo 5. Unit operations di Ian Bogost (2006)

**Verificato.**

- La tesi generale: principi simili sottostanno alla teoria letteraria e all'informatica, e il libro propone un'analisi teorico-tecnica dei videogiochi [C, voto 3-0; pagina dell'autore, MIT Press, ISBN 9780262025997 e 9780262524872].
- La recensione del 2006 conferma l'esistenza del dibattito, senza contraddire la tesi [C-s].

**Scartato.**

- La definizione di *unit operation* come "sistema configurativo di unità di significato discrete e interconnesse" è scartata [R, voto 0-3]. Non usarla come definizione.

**Nel corpus.** La voce 09 dell'indice (Sanchez, *Combinatorial Design*) cita le *Unit Operations* come strumento di progetto insieme alle piattaforme di gioco [dal corpus, indice 00, riga 65]. Non è chiaro se Sanchez riprenda il concetto di Bogost o un altro: va verificato sul testo di Sanchez (analisi 09).

**Lacune.** Nessuna fonte verificata sul rapporto tra unit operations e mereologia di Husserl [L].

---

## Capitolo 6. Mereologia fenomenologica di Husserl (ricostruzione di Smith e Mulligan, 1983)

**Verificato.**

- Smith e Mulligan (1983), *A Framework for Formal Ontology*, *Topoi*. L'ontologia formale si distingue dalla logica formale per l'oggetto: la logica formale riguarda le strutture di significato, l'ontologia formale le strutture tra oggetti e le loro parti [C, voto 2-1; fonte primaria, Buffalo].
- Gli strumenti dell'ontologia formale sono tre gruppi: teoria del tutto e delle parti (mereologia), teoria della dipendenza, teoria del confine, continuità e contatto. Gli autori dichiarano esplicitamente di seguire Husserl [C, voto 3-0; abstract PhilArchive; **da controllare sul PDF prima di citare**].
- La mereologia di Leśniewski (estensionale) è estesa a relazioni tra oggetti concreti e pezzi-oggetto, e poi alle parti dipendenti (momenti) [C, voto 3-0].
- La struttura tripartita corrisponde alla lettura standard delle *Ricerche logiche* III di Husserl [C, voto 3-0].

**Scartato.**

- "Dependent parts or moments" come relazione ulteriore oltre la parte-tutto è scartato [R, voto 0-3].

**Discrepanze bibliografiche.** Smith e Mulligan 1983 è indicato come *Topoi* vol. 3, pp. 73–85 (pagina dell'autore), e come *Topoi* 2(1): 73–85 (PhilArchive). Va risolta prima di citare [D].

**Lacune.** Non sono stati letti né le *Ricerche logiche* III né i *Prolegomeni* di Husserl. L'attribuzione a Husserl viene dal testo di Smith e Mulligan, non dal testo di Husserl [L].

---

## Capitolo 7. Correlazioni trasversali

Questa tabella riassume i collegamenti tra i capitoli. La colonna "Stato" dice quanto sono documentati.

| Collegamento | Lato matematico | Lato filosofico | Stato |
|---|---|---|---|
| Varietà (Ashby) ↔ vicinati (von Neumann, Moore) | Conteggio di stati distinguibili; vicinato come insieme di celle | Che cosa conta come "sentire" un elemento | [I] Nessuna fonte verificata |
| Equilibrio di Nash ↔ gioco a due giocatori di Ashby | Strategie miste contro tabella di risposte | Regolazione come gioco contro le perturbazioni | [C-s] Ashby non applica Nash; differenza documentata come interpretazione |
| Bertalanffy ↔ Ashby | GST come quadro generale | Ashby come mediatore con la cibernetica | [C-s] Fonte unica |
| Von Neumann (automa) ↔ Moore | Vicinati e costruzione universale | Attribuzione del nome e del lavoro | [L] Il legame non è documentato |
| Moore ↔ Myhill (Giardino dell'Eden) | Iniettività e suriettività di automi | Teorema, non attribuzione | [R] Formulazione scartata |
| Langton ↔ von Neumann | Costruzione universale come condizione sufficiente | Autoriproduzione come proprietà | [C] Langton 1984 (abstract primario) |
| Bogost ↔ Husserl/Smith-Mulligan | Unit operations come unità discrete | Parti e tutto, dipendenza | [L] Nessun collegamento verificato |
| Sanchez (analisi 09) ↔ Bogost | Unit operations nell'indice del corpus | Piattaforme di gioco | [D] Da verificare sul testo di Sanchez |
| Von Neumann-Morgenstern ↔ Nash | Gioco a somma zero ↔ equilibrio non cooperativo | Teoria del gioco come modello della decisione | [L] Nessuna affermazione verificata |
| Vicinati ↔ stigmergia (analisi 12) | Località e propagazione del feromone | Relazione tra agenti | [I] Interpretazione mia |

---

## Capitolo 8. Lacune e prossimi passi

**Domande aperte** (dalla verifica):

1. Moore (1962) discute esplicitamente von Neumann? Va letto il volume AMS 14.
2. Quali fonti primarie collegano Nash agli automi cellulari, al vicinato di von Neumann o alla pianificazione urbana? Come si collega il gioco a somma zero di von Neumann e Morgenstern (1944) all'equilibrio non cooperativo?
3. Ashby (1956) e Bertalanffy: quali testi primari documentano un collegamento con gli automi cellulari o con l'autoriproduzione?
4. Bogost (2006) e Smith-Mulligan (1983): quale rapporto formale c'è tra unit operations e mereologia fenomenologica? Le fonti sono accessibili per una citazione diretta?

**Passi suggeriti.**

- Leggere i testi primari elencati: von Neumann e Burks (1966); Moore (1962); Langton (1984, testo completo); Nash (1950, 1951); von Neumann e Morgenstern (1944); Ashby (1956, cap. 11); Bertalanffy (1968, *General System Theory*); Husserl, *Ricerche logiche* III; Smith e Mulligan (1983); Bogost (2006).
- Risolvere la discrepanza bibliografica di Smith e Mulligan (Topoi 2(1) o vol. 3).
- Verificare il rapporto tra le *Unit Operations* di Sanchez (analisi 09) e quelle di Bogost.
- Decidere se il capitolo sugli automi cellulari deve tenere la convenzione del centro incluso o escluso, e dichiararla.

**Nota di metodo.** Le due passate di ricerca hanno coperto solo parte dei punti richiesti: i capitoli su Ashby, Bertalanffy, Husserl e Bogost hanno affermazioni confermate, ma spesso su fonti secondarie. I capitoli su von Neumann-Moore e su Nash hanno affermazioni confermate per le definizioni e per il teorema di esistenza di Nash, ma **non** per il rapporto tra le teorie.
