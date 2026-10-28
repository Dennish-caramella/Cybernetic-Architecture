# Tool di prova: modelli della tesi

Strumenti interattivi (pagine HTML autonome) per testare e confrontare i modelli emersi nelle analisi.
Regole: ogni pagina separa il dato di fonte dagli esempi e dalle inferenze; nessun parametro è inventato.

## Piano per famiglia (ordine proposto)

1. **Bartlett** (analisi 34–36) — `bartlett/index.html`. Pubblicato come artifact "Laboratorio Bartlett". Moduli: combinatoria delle connessioni (216 vs 303 dichiarati); regole locali stile Langton con 800 agenti; indice di connettività con pesi impostabili e regole di adiacenza.
2. **AADRL** (analisi 28–33) — da fare. Reward esplicita contro reward da VLM; minimax contro Nash su un gioco a due agenti.
3. **MVRDV** (analisi 14, 19–23) — da fare. Spacefighter (regole di crescita), Functionmixer (diversità e rumore come pesi), WEGO, Climatizer.
4. **Modelli matematico-filosofici** (`tesi_out/ricerche_teoriche/`) — da fare. Vicinati di von Neumann e di Moore, automi cellulari, Nash, minimax, Ashby, Bertalanffy.

## Limiti generali

- Le fonti Bartlett danno raramente formule e quasi mai parametri: dove mancano, il tool usa valori di esempio, dichiarati come tali.
- Le definizioni di indice e di grafo nel modulo 3 sono proposte dell'autore del tool (inferenza), non della fonte.
