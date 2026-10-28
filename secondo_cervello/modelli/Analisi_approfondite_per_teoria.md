# Modelli per teoria: schede brevi

Data: 2026-10-20. Complementa `Cronistoria_e_correlazioni_modelli.md`, che contiene storia, fonti e correlazioni. Qui una voce breve per modello: definizione, fonte verificata, collegamento essenziale. Nessuna analisi estesa.

**Legenda di affidabilità** (stessa della cronistoria).

- **[V]** verificato nelle due passate di ricerca.
- **[S]** formalismo standard che conosco ma non ho riletto sul testo primario. Da controllare prima di citare.
- **[I]** interpretazione mia.
- **[L]** lacuna: non verificato.

---

## Bertalanffy: teoria generale dei sistemi

- **Sistema aperto.** Stato X(t) con ingressi U(t): dX/dt = f(X, U, t). Stato stazionario quando f(X*, U*) = 0 con scambi continui. [S, Bertalanffy 1950, *Science* 111]
- **Crescita.** dL/dt = k (L∞ − L), con soluzione L(t) = L∞ (1 − e^(−k(t − t₀))). [S, Bertalanffy 1957, *Human Biology*]
- **Equifinalità.** Stesso stato finale da condizioni iniziali diverse. [S, Bertalanffy 1950]
- **Collegamento essenziale.** Isomorfismo tra discipline: il programma dichiara strutture comuni, senza dimostrarle. [V, cronistoria]

## Ashby: legge della varietà richiesta

- **Varietà.** V(S) = |S| oppure log₂|S| in bit. [V, Ashby 1956, pp. 125–126]
- **Legge.** La varietà degli esiti è almeno quella delle perturbazioni meno quella del regolatore: V(O) ≥ V(D) − V(R). [S, Ashby 1956, cap. 11]
- **Gioco a due giocatori.** Tabella: il disturbo sceglie la riga, il regolatore la colonna, la cella è l'esito. [V, Ashby 1956, p. 202]
- **Limite.** Necessaria, non sufficiente. Dice quanta varietà serve, non come ottenerla. [V]
- **Collegamento essenziale.** Con i vicinati: la varietà locale di un automa è limitata dal suo vicinato. [I]

## Good regulator (Conant e Ashby, 1970)

- **Enunciato.** Un regolatore buono è isomorfo a un modello del sistema regolato. [S, Conant e Ashby 1970, *Int. J. Systems Science*]
- **Nota.** L'attribuzione alla fonte arXiv 2008.04071 è scartata dalla verifica. [V]
- **Collegamento essenziale.** Il regolatore come modello interno del sistema. [I]

## Vicinato di von Neumann

- **Definizione.** N = {(0,0), (±1,0), (0,±1)}: cinque celle con il centro, quattro senza. [V, convenzione dichiarata nelle fonti]
- **Collegamento essenziale.** Interazione solo ortogonale a distanza 1. [I]

## Vicinato di Moore

- **Definizione.** N = {(i,j): |i| ≤ 1, |j| ≤ 1}: nove celle con il centro, otto senza. Contiene il vicinato di von Neumann più le diagonali. [V, convenzione]
- **Regole totalistiche.** Il Game of Life è la regola B3/S23 sul vicinato di Moore. [S]
- **Collegamento essenziale.** Il numero di regole possibili cresce come 2^(2^|N|): 2^32 per von Neumann, 2^512 per Moore, con due stati. [S]

## Automa autoriproducente di von Neumann

- **Definizione.** 29 stati per cella, costruttore universale più nastro di descrizione. [V, due fonti secondarie concordi; architettura S, von Neumann e Burks 1966]
- **Semplificazioni.** Codd (1968) con 8 stati [L, da verificare]; Langton (1984) con un loop minimo. [V, abstract di Langton 1984]
- **Collegamento essenziale.** La costruzione è sufficiente ma non necessaria per l'autoriproduzione (Langton). [V]

## Teorema di Moore-Myhill (Giardino dell'Eden)

- **Enunciato.** Per un automa su Z^d con alfabeto finito: suriettivo se e solo se pre-iniettivo. Moore 1962, Myhill 1963. [S]
- **Nota.** La formulazione "localmente iniettivo se e solo se suriettivo" è scartata dalla verifica. [V]
- **Collegamento essenziale.** Un Giardino dell'Eden è una configurazione senza predecessori. [S]

## Equilibrio di Nash

- **Definizione.** Un profilo σ* è equilibrio se nessun giocatore migliora cambiando da solo: u_i(σ*_i, σ*_−i) ≥ u_i(σ_i, σ*_−i). [V, definizione con voto 3-0]
- **Esistenza.** Ogni gioco finito ha almeno un equilibrio in strategie miste. Dimostrazione del 1950 con Kakutani, del 1951 con Brouwer. [V, Nash 1951, Theorem 1]
- **Collegamento essenziale.** Stabilità, non ottimalità: l'equilibrio può essere peggiore di un esito cooperativo possibile. [S, dilemma del prigioniero]

## Minimax di von Neumann (1928)

- **Enunciato.** Per giochi a somma zero a due giocatori: max_σ min_τ u = min_τ max_σ u. [S]
- **Collegamento essenziale.** Caso speciale in cui l'equilibrio di Nash coincide con il valore minimax. [S]

## Unit operations di Bogost (2006)

- **Natura.** Metodo di analisi dei media, non un modello matematico. [V, tesi generale]
- **Nota.** La definizione "sistema configurativo di unità di significato discrete e interconnesse" è scartata dalla verifica. Non usarla come definizione. [V, 0-3]
- **Collegamento essenziale.** Unità discrete con operazioni: vicino alla cella di un automa. [I]

## Husserl: dipendenza e mereologia (ricostruzione di Smith e Mulligan, 1983)

- **Tre relazioni.** Parte-tutto, dipendenza (fondazione), confine e contatto. [V, tripartizione, voto 3-0]
- **Dipendenza.** x dipende da y se x non può esistere senza un y di un certo tipo. [S, *Ricerche logiche* III]
- **Mereologia formale.** Riflessività, antisimmetria, transitività. [S, Leśniewski, Tarski]
- **Nota.** La formulazione "momenti come relazione oltre la parte-tutto" è scartata nella verifica. Le *Ricerche logiche* non sono state lette. [V]
- **Collegamento essenziale.** La dipendenza è più forte della prossimità del vicinato. [I]

---

## Lacune

- Nessun collegamento tra queste teorie è verificato su fonte primaria. Sono interpretazioni [I].
- I testi primari non sono stati riletti: vanno letti prima della citazione.
- La discrepanza bibliografica su Smith e Mulligan (*Topoi* 3 o 2(1)) è da risolvere. [V]
