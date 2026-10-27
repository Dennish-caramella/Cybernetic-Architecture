# Veloso, P.; Rhee, J.; Krishnamurti, R. — *Multi-agent Space Planning. A literature review (2008–2017)* — Arricchimento visivo

> **Stato:** arricchimento visivo. Il riassunto completo esistente non è accessibile da questa sessione. Questo file va agganciato alle sue sezioni.
> **Fonte:** `TESI/01_Ricerche Teoriche/06_Multi-agent Space Planning.pdf` — 23 pagine, circa 7.000 parole, testo letto integralmente (sezioni 1–6 e bibliografia).
> **Riferimento come riportato nel PDF:** Pedro Veloso, Jinmo Rhee, Ramesh Krishnamurti (Carnegie Mellon University), "Multi-agent Space Planning. A literature review (2008–2017)". **Sede di pubblicazione e anno del volume non indicati nel PDF.** Stato: `da verificare`.
> **Nota:** è una **rassegna**, non un prototipo. Le sedici tecniche e i due precedenti sono descritti e confrontati, non sviluppati. Gli esempi delle sezioni 2–4 sono tratti dai rispettivi articoli originali (citati nel testo), che non sono in cartella.

## Figure e schemi estratti

Il PDF ha 19 figure numerate e 6 tabelle. Ho estratto **21 immagini** (con la pagina PDF nel nome). Le figure sono riproduzioni di altri autori, con riferimento al loro articolo: per la tesi vanno citate con la fonte originale e il permesso.

| File (cartella `figure/`) | Pagina PDF | Figura nel testo | Contenuto (dal testo) |
|---|---|---|---|
| `p03_immagine_000.png` | 3 | Fig. 1 — IMAGE (Weinzapfel, 1971) | Volumi di cuboidi con vincoli di posizione relativa, visione, circolazione; grafo dei vincoli |
| `p04_immagine_001.png`, `p04_immagine_002.png` | 4 | Fig. 2 — Fuzzy Layout Planner | Bolle che adattano le dimensioni per conservare l'area, forze di repulsione, impacchettamento |
| `p05_immagine_003.png` | 5 | Fig. 3 — Sniffing Space I | Zone di associazione spaziale; espansione con bordi rettangolari |
| `p06_immagine_004.png`, `p06_immagine_005.png` | 6 | Fig. 4 — Actants | Un Actant con i suoi componenti; scala di consolidamento; associazioni |
| `p07_immagine_006.png` | 7 | Fig. 5 — Floating Bubbles | Tre fasi del sistema base; processo generativo con quadrati |
| `p08_immagine_007.png` | 8 | Fig. 6 — Space-planning with real-time physics | Diagramma astratto; simulazione fisica a sfere e molle |
| `p09_immagine_008.png`, `p09_immagine_009.png` | 9 | Fig. 7 — Interactive bubbles | Simulazione con temperatura variabile; area di contenimento |
| `p10_immagine_010.png` | 10 | Fig. 8 — Narrative landscape | Corpi morbidi e classi di molle; due layout |
| `p11_immagine_011.png`, `p11_immagine_012.png` | 11 | Fig. 9 — Multi-agent + Evolutionary | Agenti sferici e a capsula, operazione di swap, griglia e ottimizzazione |
| `p12_immagine_013.png` | 12 | Fig. 10 — Sniffing Space II | Routing tra destinazioni; clustering del carico (aeroporto) |
| `p13_immagine_014.png` | 13 | Fig. 11 — SSAS | Griglia e pheromone; templates di influenza esterna e node masking; una soluzione |
| `p14_immagine_015.png`, `p14_immagine_016.png` | 14 | Fig. 12 — Collective construction | Risultati degli esperimenti con agenti in squadre |
| `p15_immagine_017.png` | 15 | Fig. 13 — Artificial Life Space Planning | Griglia, diagramma a bolle e integrazione dei due |
| `p18_immagine_018.png` | 18 | Fig. 16–17 — Dwelling Agglomerator / Responsive Algorithms | Regole di flocking; circle packing, diagramma di Voronoi |
| `p19_immagine_019.png`, `p19_immagine_020.png` | 19 | Fig. 18–19 — tassonomia e grafici radar | Confronto delle tecniche; occorrenze per tipo (radar) |

**Nota:** l'associazione tra file e numero di figura è per pagina e va verificata sul PDF prima dell'uso. Le tabelle 1–6 (tipo, rappresentazione, obiettivi, controllo, correlazioni) non sono estratte come immagini: sono descritte qui sotto.

## Schema 1 — la tassonomia dei tre tipi (testo, p. 2–3, tabella 1)

```
  TIPO 1 — agenti come unità spaziali mobili
     (ciascun agente ha una propria rappresentazione dello spazio)
     IMG, FLP, SS1, ACT, FB, RTF, IB, NL, MAE
            |
  TIPO 2 — agenti che occupano uno spazio discreto (griglia)
     SS2, SSAS, CC, ALSP (ibrido)
            |
  TIPO 3 — agenti che partizionano lo spazio
     YONA, ASN, DA, RA, (EF)
```

**Lettura (inferenza mia):** la tassonomia è utile per la tesi perché distingue *dove* stanno gli agenti (su una forma, su una griglia, o nel partizionare il territorio). Per la partecipazione, nessuno dei tre tipi prevede un agente "utente".

## Schema 2 — il ciclo della rassegna (testo, sezione 5)

```
  16 prototipi + 2 precedenti (2008–2017, soprattutto CumInCAD)
        |
        v
  descrizione per tipo: rappresentazione, algoritmo, obiettivi
        |
        v
  occorrenze di caratteristiche: rappresentazione, obiettivi, controllo
        |
        v
  correlazioni tra caratteristiche e tipi (tabelle 5–6, radar fig. 19)
        |
        v
  lacune: validazione formale, condivisione del codice, conflitti spaziali, conoscenza architettonica
```

## Passaggi citabili con pagina (per la scheda)

- Definizione: MASP come metodi "based on online mobile agents that map local perceptions to actions in the environment, generating spatial representation" (abstract, p. 1). Parafrasi.
- Gap della letteratura: "MASP still has a secondary role in the literature" (p. 1–2). Affermazione degli autori, basata sulla loro ricerca.
- Limite delle tecniche attuali: "we point to the limits of current systems to solve spatial conflicts and to incorporate architectural knowledge" (abstract). Citazione breve.
- Proposta: "behavioral learning offers a promising path for robust and autonomous MASP systems in the architectural domain" (abstract, p. 1, e p. 17). Ipotesi, non risultato.

## Limiti, assunzioni e bias

- **Campione:** la rassegna copre un periodo di dieci anni e fa riferimento soprattutto a CumInCAD (archivio di conferenze CAAD). Possono mancare lavori in altre riviste o in lingue diverse. Gli autori lo dichiarano.
- **Criteri di confronto:** le tabelle contano le occorrenze di caratteristiche: un conteggio, non una valutazione di qualità o di prestazioni.
- **Ipotesi di correlazione:** le correlazioni (tab. 5–6) sono calcolate su sedici prototipi; con questo campione, i valori sono indicativi.
- **Assenza di utenti:** nessun prototipo include l'utente come agente. Gli autori includono la figura dell'utente come "omniscient agent" solo nel quadro generale dell'ABM (p. 2). È un punto da riprendere per la tesi sulla partecipazione.
- **Conclusione:** la proposta del deep reinforcement learning (p. 17) è un'ipotesi della rassegna; non c'è un prototipo che la testi. Va trattata come direzione, non come risultato.

## Collegamenti per la sintesi

- Con Meyboom e Reeves (*Stigmergic Space*, 2013): la SSAS è la sezione 3.2 di questa rassegna. Il PDF di Meyboom è una fonte primaria per il tipo 2.
- Con Erioli (*Assembler*, eCAADe 41): Erioli cita questa area di ricerca come precedente per la combinatoria; Assembler non è un MASP ma è vicino alla categoria "partizionamento".
- Con Alexander (*A City is not a Tree*): gli agenti che si sovrappongono (IMG, SS1, ACT) mostrano in forma computazionale la struttura a semi-reticolo.
- Con Pask (1969): la regolazione continua degli agenti è la versione computazionale del ciclo di feedback di Pask.
- Con la tesi: il punto da riprendere è la conclusione sul "behavioral learning" e sulla mancanza di agenti-utente. È il varco più diretto verso la partecipazione.
