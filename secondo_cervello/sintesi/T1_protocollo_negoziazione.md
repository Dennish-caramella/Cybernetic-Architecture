# Protocollo T1: negoziazione con pesi espliciti

**Stato:** protocollo di progetto, non un risultato. Nessun dato di Milano è ancora verificato.
**Data:** 2026-10-20
**Riferimento:** `REPORT_FONDATIVO.md`, ipotesi H1 e H2, asse 4.

## 1. Scopo

Verificare se un sistema che espone criteri e pesi, e li lascia modificare agli attori, produce compromessi leggibili e discutibili. Il test non cerca la soluzione ottima. Cerca se i compromessi cambiano quando cambiano i pesi, e chi li cambia.

Il test è la baseline per il confronto con l'apprendimento per rinforzo, da fare dopo.

## 2. Oggetto

- **Insieme di lotti candidati.** Da definire dopo l'analisi socio-economica. Per il test possono bastare 10–20 lotti ipotetici, purché dichiarati come tali.
- **Per ogni lotto:** superficie, destinazione urbanistica, accessibilità, costo stimato del suolo, servizi. I valori vanno da fonti verificate. Per il test iniziale si usano valori di scenario, marcati come tali.
- **Tipologie di intervento:** due o tre, con unità abitative e percentuale di edilizia accessibile. Le tipologie sono dati di input, non soluzioni proposte dal sistema.

## 3. Attori e pesi

Gli attori sono profili di scenario, non persone reali. Il test non è una prova di partecipazione: serve a verificare il meccanismo di negoziazione. I profili vanno dichiarati come finti in ogni output (rischio 2 del report).

| Attore | Obiettivo dichiarato | Vincolo |
|---|---|---|
| Residente in cerca di casa | canone accessibile, vicinanza al lavoro | superficie minima |
| Sviluppatore | margine economico | costo massimo di costruzione |
| Comune | quota di edilizia accessibile, servizi | normativa urbanistica |
| Finanziatore o gestore | rendimento, rischio | tempi di realizzazione |

Ogni attore dichiara un vettore di pesi sui criteri, la cui somma è 1. I pesi sono l'oggetto della negoziazione.

## 4. Procedura

1. **Baseline manuale (P1 del report).** Stesso scenario con tabelle e confronto a voce. Si registrano tempo alla scelta, criteri esplicitati e alternative considerate.
2. **Calcolo delle soluzioni.** Per ogni combinazione lotto–tipologia si calcolano i valori dei criteri.
3. **Frontiera di Pareto.** Si calcola l'insieme delle soluzioni non dominate rispetto ai criteri degli attori.
4. **Round di negoziazione.** Ogni attore modifica i propri pesi (e, in una variante, i vincoli). Si ricalcola la frontiera.
5. **Registrazione.** Per ogni round: pesi proposti, soluzioni non dominate, soluzioni che entrano o escono dalla frontiera.

## 5. Metriche

- **M1.** Quota di soluzioni non dominate che cambia tra due round consecutivi.
- **M2.** Numero di round in cui almeno un attore cambia un criterio, e non solo il peso.
- **M3.** Tempo alla scelta, in confronto con la baseline P1.
- **M4.** Quante soluzioni sono scartate per vincoli violati, e da quale attore.

## 6. Ipotesi e condizioni di falsificazione

- **H1 (mediazione visibile).** Falsificata se M1 resta vicina a zero per tutti i round, cioè i pesi non cambiano il fronte.
- **H2 (potere sui criteri).** Falsificata se M2 è zero in tutti i round, cioè nessuno propone modifiche ai criteri e il sistema resta un selettore di soluzioni.
- **H3 (costo dell'esplorazione).** Falsificata se M3 non è inferiore alla baseline P1.

Le soglie numeriche per "vicina a zero" e per "cambia" si fissano prima del test, non dopo.

## 7. Limiti noti

- Attori di scenario, non reali: il risultato dice qualcosa sul meccanismo, non sul comportamento delle persone.
- Pesi e vincoli scelti dal progettista nella prima versione: va dichiarato in ogni output.
- Nessun modello di prezzo immobiliare verificato: il criterio di costo è uno scenario.
- Un solo caso: non generalizza.

## 8. Cosa serve prima di iniziare

1. Lista dei lotti candidati, o scelta della procedura per generarla dall'analisi socio-economica.
2. Fonti verificate per i criteri di costo e domanda abitativa (ISTAT, Comune di Milano, osservatori), con data e granularità.
3. Conferma dei quattro profili di attore e dei pesi di partenza.
