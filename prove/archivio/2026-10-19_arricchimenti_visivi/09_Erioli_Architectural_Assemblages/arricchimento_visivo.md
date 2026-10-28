# Erioli, A. — *Architectural Assemblages as Computational Medium* — Arricchimento visivo

> **Stato:** arricchimento visivo. Il riassunto completo esistente non è accessibile da questa sessione. Questo file va agganciato alle sue sezioni.
> **Fonte:** `TESI/01_Ricerche Teoriche/09_Alessio Erioli_Architectural Assemblages as Computational Medium.pdf` — 10 pagine (eCAADe 41, Volume 1, pp. 589–598). Testo letto integralmente.
> **Riferimento come riportato nel PDF:** Alessio Erioli, Università di Bologna / Co-de-iT, "Architectural Assemblages as Computational Medium. Introducing Assembler, a tool for the design and study of architectural assemblages", eCAADe 41 (*Digital Design Reconsidered*), vol. 1. Anno e sede da verificare sugli atti.
> **Nota:** il PDF include figure di progetti (RBTA, *The City in the Space*, con credito "used with permission"; progetti di Bologna e IaaC). Per la tesi serve il permesso, o la citazione nei termini del credito.

## Figure e schemi estratti

Il PDF ha 9 figure numerate. Non tutte sono estraibili come immagini intere: alcune (fig. 1, 2, 4, 6, 7, 8) sono vettoriali e il testo le indica solo per titolo. Qui sotto quelle che ho potuto estrarre.

| File (cartella `figure/`) | Pagina PDF | Cosa mostra (osservazione diretta) | Didascalia / riferimento |
|---|---|---|---|
| `p04_a_RBTA_city_in_the_space_circolazione_1.png` | 4 | Disegno in pianta di un tessuto modulare con assi di circolazione (frecce) e corpi in tratteggio: la circolazione è incorporata nella crescita modulare. | "Figure 3: RBTA – The City in The Space" (testo) |
| `p04_b_RBTA_city_in_the_space_circolazione_2.png` | 4 | Stesso tipo di tessuto, con una variante dei percorsi e dei volumi in tratteggio incrociato. | "Figure 3" (variante) |
| `p04_c_RBTA_situacion_jardines_patios_nucleo_circolazione.png` | 4 | Titolo in spagnolo sul disegno: "Situación de los jardines o patios en un núcleo de circulación alrededor del eje vertical". Giardini e cortili disposti intorno a un nucleo di circolazione. | "Figure 3" (didascalia in originale) |
| `p08_composito_progetti_Bologna_IaaC.png` | 8 | Composito di quattro riquadri: vista aerea di un tessuto denso, piante e sezione di un edificio residenziale, diagrammi di densità locale, tipo di AO e orientamento su una forma a volta, un interno in legno a celle. | Fig. 9 (progetti di Bologna) e fig. 5 (IaaC, "Urban Eurhythmics") (probabile) |

## Schema 1 — il ciclo di Assembler (testo, p. 5–6)

```
  PARTI (AssemblyObject, AO)           CAMPO (Field, voxel 3D)
  collision volume + piano + handles   dati esogeni: scalari, vettori, iWeights
          |                                      |
          v                                      v
  MOTORE: ciclo a tre fasi
    1. scegli un ricevente tra gli AO già posati
    2. scegli un mittente (tipo di AO) coerente geometricamente
    3. aggiorna l'assemblaggio
          |
          v
  EURISTICHE: regole generate per permutazione degli handles; criteri di scelta (preset o C#)
          |
          v
  AMBIENTE: mesh chiuse, solide (collisione) o vuoti (inclusione)
          |
          v
  POST-PROCESSING: connettività, grafo di circolazione, dati per ogni oggetto
```

**Lettura (inferenza mia):** la domanda che guida il tool è "dove metto il prossimo oggetto?" (p. 5). Ogni scelta di luogo e orientamento è una decisione, e il progettista controlla le *parti*, i *collegamenti* e le *euristiche*, non la forma finale. È un'implementazione concreta del "designer di generating systems" di Alexander (1968), con l'aggiunta del campo di dati.

## Schema 2 — dove il testo si colloca (testo, p. 2–4)

| Asse | Riferimento nel testo | Posizione |
|---|---|---|
| Assemblage theory | DeLanda 2006, 2016; Deleuze e Guattari 1987; Dovey 2013 | parti e relazioni generano qualità emergenti |
| Semi-reticolo | Alexander 2015 | sovrapposizioni invece di gerarchia ad albero |
| Combinatoria | Sanchez 2016; Stiny 1980 (shape grammar) | variazione da un insieme limitato di parti |
| Partecipazione | Friedman 1971 (Flatwriter); Negroponte; Price | algoritmi con autonomia decisionale |

## Passaggi citabili con pagina (per la scheda)

- Definizione: Assembler "interweaves mereology, combinatorial design, and automated decision at scale" (p. 2, introduzione). Parafrasi.
- Ruolo del progettista: "the user has control over the design of parts, connections, and heuristics of the system, and the tool enacts those decisions in space and time" (abstract). Citazione breve.
- Il tool non è neutro: "The only coherence it enforces is a geometrical one; its bias are structural, not conceptual" (p. 9–10). Utile come contro-argomento alla tesi di neutralità.
- Limite: "a steep learning curve … students show confidence after week 5" (p. 11, limiti). Dato da corso, non misurato.

## Limiti, assunzioni e bias

- **Autore-sviluppatore:** il tool è sviluppato dall'autore; la valutazione (corsi IaaC e Bologna) è autoreferenziale. Non ci sono confronti con altri utenti o con misure di qualità.
- **Utente esperto:** il testo presuppone competenza in Rhino–Grasshopper e in C#. Per la tesi sulla democratizzazione è un limite forte: l'accesso è per progettisti esperti.
- **Euristiche deterministiche:** la scelta è dichiarata deterministica "to ensure a reliable response for the designer" (p. 10). Non c'è discussione dell'apprendimento o dell'adattamento dei criteri dal feedback degli utenti. Il testo lo indica come sviluppo futuro (rete neurale, apprendimento per rinforzo).
- **Dato della "IA":** il titolo parla di "computational medium", non di IA. Le parole "intelligence" e "neural network" compaiono solo nell'ultima sezione come lavoro futuro.
- **Riferimenti:** Alexander 2011 (ristampa in *AD Reader*) e Alexander 2015 (50° anniversario) vanno controllati: il testo cita entrambi per lo stesso saggio. Da verificare.

## Collegamenti per la sintesi

- Con Alexander, *A City is not a Tree* (1965) e *Systems Generating Systems* (1968): il semi-reticolo e i kit di parti con regole sono le due basi teoriche esplicite del tool.
- Con Sanchez, *Combinatorial Design*: stesso vocabolario delle unità combinatorie; Erioli cita Sanchez 2016 come punto di riferimento.
- Con Meyboom e Reeves (*Stigmergic Space*, 2013): stessa idea di decisioni locali che producono un esito globale, con un campo di dati (feromoni vs campo voxel).
- Con la tesi: il tool mostra come l'architetto diventi progettista di euristiche. Per la partecipazione va chiarito chi definisce le euristiche e chi le modifica.
