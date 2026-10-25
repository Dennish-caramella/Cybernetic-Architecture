---
name: tavola-rotonda
description: Orchestra il team di voci-esperte della tesi (agenti in .claude/agents/) su un nodo di ricerca, in due round, e produce una sintesi con convergenze, contraddizioni e lacune. Usare quando Dennis chiede di far discutere gli esperti, di sovrapporre le posizioni critiche o di mettere alla prova una tesi o un'ipotesi.
---

# Tavola rotonda

Il team simula le competenze dei testi analizzati, non gli autori reali. Le voci sono definite in `.claude/agents/`:
`alexander-sistemi`, `pask-cibernetica`, `negroponte-steenson`, `decarlo-mari-partecipazione`, `degraaf-murphy-potere`, `carpo-sanchez-discreto`, `mvrdv-negoziazione`, `aadrl-bartlett-agenti`, `agenti-stigmergia`, `azadi-pianificazione-aumentata`, `ingegnere-edile`, `revisore-integrita`.

## Procedura

1. **Nodo.** Formula il nodo in una domanda sola, legata al Report fondativo (domanda, SQ1-5, H1-H4, assi). Se Dennis non l'ha dato, proponilo e parti.
2. **Selezione.** Scegli le voci pertinenti (di solito 5-8), sempre `ingegnere-edile` e `decarlo-mari-partecipazione` come contrappesi. Il `revisore-integrita` interviene alla fine.
3. **Round 1, posizioni.** Lancia le voci in parallelo (tipo agente = nome della voce; se non è registrato, usa un agente generico che legga il file `.claude/agents/<nome>.md` e ne assuma il ruolo). Ogni voce riceve solo il nodo, non le posizioni altrui.
4. **Round 2, confronto.** Dai a ogni voce le posizioni sintetizzate delle altre e chiedi: dove cambia idea, dove resta in disaccordo, quale prova risolverebbe il disaccordo.
5. **Revisione.** Il `revisore-integrita` controlla etichette `[S]`/`[I]`/`[H]`/`[L]`, circolarità e affermazioni che le schede non reggono.
6. **Sintesi.** Scrivi un file `tavole_rotonde/AAAA-MM-GG_<nodo>.md` con: nodo; posizioni per voce; convergenze; contraddizioni; lacune; prove proposte (con criterio di fallimento); correzioni del revisore; stato di verifica. Non riscrivere la tesi.

## Regole

- Italiano. Nessuna citazione inventata. Ogni affermazione porta lo statuto: fonte (scheda), inferenza, ipotesi, lacuna.
- Il consenso non è una prova: la sintesi deve dire dove le voci concordano per le stesse ragioni sbagliate (stesse schede, stesse fonti).
- Le idee e la scrittura finale restano di Dennis; la sintesi si chiude con 2-3 decisioni che spettano a lui.
