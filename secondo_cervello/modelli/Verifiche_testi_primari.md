# Verifiche sui testi primari

Data: 2026-10-20. Esito della lettura dei testi primari disponibili online per i formalismi marcati [S] in `Studio_modelli_con_esempi.md` e `Analisi_approfondite_per_teoria.md`. Dove il testo non è stato raggiunto, la voce resta [S] o [L].

## Verificato sul testo

**Nash (1951), "Non-Cooperative Games", *Annals of Mathematics* 54(2).** Fonte: https://irving.vassar.edu/faculty/gj/FTU/io/literature/Nash51.pdf
- Equilibrio: σ è equilibrio se per ogni giocatore il payoff è il massimo rispetto alle strategie miste unilaterali. È l'equivalente della disuguaglianza usata nello studio. [V, p. 287]
- Esistenza: Teorema 1, "Every finite game has an equilibrium point". La dimostrazione del 1951 usa il teorema del punto fisso di Brouwer. Kakutani è citato come base della dimostrazione del 1950, che il lavoro migliora. [V, p. 288]
- "Non-cooperative": il termine compare nel titolo e nelle intestazioni, non nel corpo dell'introduzione. L'introduzione contrappone la teoria cooperativa di von Neumann e Morgenstern, basata sulle coalizioni, alla propria, basata sull'assenza di coalizioni: "each participant acts independently, without collaboration or communication with any of the others". [V, p. 286]

**von Neumann e Burks (1966), *Theory of Self-Reproducing Automata*, capitoli sull'automa.** Fonte: https://fab.cba.mit.edu/classes/MAS.865/topics/self_replication/Burks.pdf
- 29 stati per cella: "Each cell is capable of 29 different states". [V]
- Vicinato: "a neighborhood composed of a cell and the four cells with which it shares boundaries". È il vicinato di von Neumann con centro, cinque celle. [V]
- Architettura: costruttore universale, nastro di descrizione, copia della descrizione sulla nuova macchina. [V]
- **Correzione.** Il testo non dice che la costruzione sia sufficiente ma non necessaria per l'autoriproduzione. Dice l'opposto come impostazione: "self-reproduction is a special case of construction". La tesi "sufficiente, non necessaria" resta attribuita a Langton (1984) e va citata come sua, non come affermazione di von Neumann. [V, correzione]

**Bertalanffy, recensione in *Nature* (1949), "'Open Systems' in Physics and Biology".** Fonte: https://www.nature.com/articles/163384a0.pdf
- Organismi come sistemi aperti che si mantengono scambiando materia con l'ambiente. "the second law of thermodynamics applies only to closed systems". [V]
- L'equifinalità non compare in questo testo. [V]
- Questo testo è una fonte diversa da quella dello studio: non è l'articolo di *Science* 111 (1950). [V]

## Non verificato (gap)

- **Ashby (1956), *An Introduction to Cybernetics*, cap. 7 e 11.** Il PDF su archive.org è stato raggiunto, ma l'estratto fornito si ferma al cap. 4. Restano da verificare: la definizione di varietà come conteggio o in bit (pp. 125–126), la formulazione della legge della varietà richiesta come necessaria e non sufficiente (p. 206 e segg.), la tabella del gioco a due giocatori (p. 202). Richiede il testo delle pagine 121–125 e 202–213. [L]
- **Bertalanffy (1950), "The Theory of Open Systems in Physics and Biology", *Science* 111.** Non raggiunto. [L] Restano da verificare la dinamica dello stato stazionario e l'equifinalità.
- **Bertalanffy (1957), *Human Biology*, equazione di crescita.** Non raggiunto. [L] Resta [S].
- **Codd (1968), 8 stati.** Non verificato. [L]
- **Husserl, *Ricerche logiche* III, e Smith e Mulligan (1983).** Non raggiunti in questa sessione. [L] Resta aperta la discrepanza bibliografica (*Topoi* 3 o 2(1)).

## Conseguenze per i file di studio

- Nella sezione Nash dell'analisi breve, la frase "dal testo di Nash 1951, 'non-cooperative' dichiarato nell'introduzione" va letta così: il termine è nel titolo, la contrapposizione con le coalizioni è nell'introduzione. Il file breve non usa più quella formulazione.
- Nella sezione von Neumann dello studio, la frase "Langton mostra che… sufficiente… non necessario" resta attribuita a Langton. Il testo di von Neumann e Burks non la sostiene.
