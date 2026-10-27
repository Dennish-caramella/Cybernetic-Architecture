# Sanchez, J. — *Combinatorial Design* — Arricchimento visivo

> **Stato:** arricchimento visivo. Il riassunto completo esistente non è accessibile da questa sessione (sta sul computer dell'autore). Questo file va agganciato alle sue sezioni.
> **Fonte:** `TESI/01_Ricerche Teoriche/03_Jose Sanchez_Combinatual Design.pdf` — 10 pagine PDF, circa 3.800 parole, testo integrale letto.
> **Riferimento:** José Sanchez (University of Southern California), "Combinatorial design: non-parametric computational design strategies". **Sede di pubblicazione e anno non indicati nel PDF.** Stato: `da verificare`. Il testo cita Schumacher 2011, Terzidis 2014, Bogost 2006, Sanchez 2014 (ACADIA), Rifkin 2014: anche questi da verificare prima di entrare in bibliografia.
> **Nota sulle figure:** le immagini sono estratte dalle pagine PDF. Le didascalie nel testo sono numerate a margine (1–11) e le immagini non portano lo stesso numero: l'associazione immagine–didascalia qui sotto è per pagina e **non è certa**.

## Figure e schemi estratti

Cartella: `figure/` (13 immagini, nomi per pagina PDF). Non ci sono diagrammi vettoriali o grafici numerici: le immagini sono fotografie di modelli e render di progetti dello studio Polyomino.

| File | Pagina PDF | Cosa mostra (osservazione diretta) | Didascalia nel testo (probabile) |
|---|---|---|---|
| `p01_a_aggregazione_legno.png` | 1 | Aggregazione di molte unità in legno, in una massa a superficie articolata | "Design – Year 3 – Pattern of one unit in two scales. Developed by combinatorial design within a game engine" |
| `p02_a_unita_grigie_patterned.png` | 2 | Unità grigie accoppiate in un pattern, render con sfondo scuro | "Project's game simulation developed in Unity3D" |
| `p02_b_superficie_ondulata.png` | 2 | Superficie ondulata composta da unità bianche, fotografia del modello | Progetto Plethora (Figura 2–3 nei crediti) |
| `p03_diagrammi_orientamento_unita.png` | 3 | Diagrammi in pianta e assonometria: orientamenti dell'unità e crescita geometrica | "Diagrams – Year 2 – Diagrams of unit orientations and geometric growth" (p. 4 del testo) |
| `p04_a_prototipo_grigio.png` | 4 | Pannello con unità grigio-verdi in pattern simmetrico, render | "Pavilion design – Year 1 – Aggregation printed out a pattern developed within the game simulation" |
| `p05_a_struttura_legno_ricostruita.png` | 5 | Struttura in listelli di legno, vista dal basso | "Design – Year 2 – Larger pattern design using combinatorial catalog" |
| `p06_a_modello_legno_pattern.png` | 6 | Modello fisico in legno, pattern di un'unità identica | "Design – Year 3 – Combinatorial patterning of one identical unit" |
| `p07_a_sezione_pattern_colorato.png` | 7 | Sezione o prospetto di un'aggregazione con unità rosse e turchesi | "Model – Year 3 – Material patterning of one identical unit" |
| `p07_b_massa_colorata.png` | 7 | Massa aggregata con unità colorate, vista a grande scala | (non indicata: stesso gruppo di pagina) |
| `p07_c_sezione_con_figure.png` | 7 | Sezione con figure umane per la scala | (non indicata) |
| `p08_a_modello_legno_angolare.png` | 8 | Elemento in legno con connessioni a scorrimento, forma a L | "Detail – Year 3 – Assembly of wooden members with sliding connection" (probabile) |
| `p09_a_unita_gradiente_colori.png` | 9 | Unità stampate 3D con gradiente di colore, dal giallo al blu e al rosa | Prototipi della stampa Polyomino con Stratasys (p. 9–10 del testo) |
| `p10_a_assemblaggio_blu.png` | 10 | Assemblaggio di unità blu-verdi con legenda di colore | Stampa Polyomino, analogia con i legami atomici (p. 10 del testo) |

**Nota sulle fotografie:** sono documentazione di progetti studenteschi (la lista dei crediti attribuisce le immagini a team specifici). Per la tesi vanno citate con il credito corretto, e il permesso d'uso va chiesto al team o al docente.

## Schema 1 — parametrico contro combinatorio (testo, p. 1–2)

```
                 PARAMETRICO                       COMBINATORIO
  insiemi         continui (NURBS, intervalli)     finiti e discreti (unità, regole)
  operazioni      variazione di rapporti,          permutazione, combinazione,
                  intensità, gradienti             accoppiamento di unità
  linguaggio      flussi, gradienti che            pattern, disposizioni
                  passano l'uno nell'altro
  ottimo          possibile (ricerca numerica)     non possibile: lo spazio
                                                   cresce in modo esponenziale
  riferimento     Schumacher 2011                  Bogost 2006 ("unit operations")
                                                   Terzidis 2014 (permutation design, criticato)
```

**Lettura (mia inferenza):** la distinzione non è tra forme "buone" e "cattive", ma tra due modi di definire lo spazio delle soluzioni. Il punto contro Terzidis è che, con spazi esponenziali, la ricerca esaustiva non è praticabile, e quindi l'ottimo è sostituito da una soluzione "ad hoc" scelta da un progettista o da una folla.

## Schema 2 — il ciclo del progetto Polyomino (testo, p. 3–9)

```
   definizione delle unità (parti con relazioni)
        |
        v
   catalogo di permutazioni ("vocabolario" di disposizioni)
        |
        v
   ambiente di gioco (game engine, VR)  <-- feedback in tempo reale --> decisione umana
        |                                                                  (criteri: porosità,
        v                                                                   struttura, luce)
   stampa 3D / costruzione fisica (materiali, prototipi)
        |
        v
   nuova iterazione (3 anni, 2013-)
```

Il testo descrive il passaggio "from gaming to making": il gioco è la simulazione guidata dalle decisioni del giocatore, che diventa la forma dell'edificio. È un'affermazione del progetto, non un risultato valutato.

## Schema 3 — evoluzione dello studio in tre iterazioni (testo, p. 3–7)

| Iterazione | Idea principale | Esito descritto nel testo |
|---|---|---|
| 1 (anno 1) | troncato ottaedro con simmetrie rotte; unità molto dettagliata | base per la serie Polyomino con Stratasys (2016) |
| 2 (anno 2) | impacchettamento perfetto abbandonato in un progetto; più vicini e rotazioni | crescita dello spazio combinatorio; più differenziazione con meno complessità per unità |
| 3 (anno 3) | tre progetti critici: "sistemi ed eccezioni" (20% di unità su misura), connessioni analogiche, unità singola con molte permutazioni | le eccezioni come tessuto connettivo; la connessione a scorrimento come punto di ibridazione con il parametrico |

## Passaggi citabili con pagina (per la scheda)

- Definizione: combinatorial design come "non-parametric design strategies that focus on the permutation, combination and patterning of discrete units" (p. 1, abstract). Citazione breve, da parafrasare in tesi.
- Ruolo umano: il progetto "has been designed to allow for a human-machine symbiosis" (p. 7). Questo è il punto più vicino alla tesi sulla partecipazione.
- Crowd: il testo parla di "crowd-sourced design" e di "prosumers" (Rifkin 2014) come motore di nuovi progettisti (p. 6–7). L'affermazione non è dimostrata nel testo con dati su utenti reali.

## Limiti, assunzioni e bias

- **Conflitto di interessi dichiarato:** il lavoro è sponsorizzato da Stratasys ("sponsored and tested by the company Stratasys", abstract). Il testo presenta la stampa come sbocco del progetto. Va letto come documento di ricerca con un committente industriale.
- **Nessuna valutazione:** il testo non misura né confronta i risultati (tempi di progetto, qualità, soddisfazione degli utenti). Le affermazioni sul potenziale di crowd-sourcing e sulla democratizzazione sono aspettative dell'autore, non risultati.
- **Assenza di dati sui partecipanti:** gli studenti sono progettisti esperti (Master in Advanced Architectural Studies). Non c'è nessun test con utenti non esperti, che è il punto della tesi.
- **Vaghezza terminologica:** "parametric" è definito in modo restrittivo (continuità, rapporti, intensità). Chi legge da un'altra tradizione (es. parametrico come programmazione visuale o come generazione algoritmica) potrebbe non riconoscere la distinzione. È un rischio da segnalare in tesi.
- **Dichiarazione di Bogost:** l'idea di "unit operations" è ripresa da Bogost (2006) con una citazione lunga; in tesi va parafrasata e riferita.

## Collegamenti per la sintesi

- Con Sanchez, *We have always been parametric* (stesso autore, altro saggio): il combinatorio è posto in contrasto con il parametrico, che il secondo testo tratta come storia.
- Con Pask (1969): la "cybernetic" di Pask è un sistema di controllo e regole; il combinatorio qui è un sistema di unità e regole di accoppiamento: stessa struttura generale, senza il riferimento all'ambiente reattivo.
- Con Alexander, *Systems Generating Systems* (1968): il kit di parti e le regole di combinazione. Sanchez non cita Alexander in questo testo: il collegamento è mia inferenza.
