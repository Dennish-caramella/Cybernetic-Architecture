# §7 Revisione indipendente — Base L v6 (ticket #39)

Revisore metodologico, 14/11/2026. Testo trascritto dal coordinatore dalla consegna del revisore (che non può creare file); condensato nelle parti descrittive, completo negli esiti. Il revisore non ha eseguito la prova e non ha aperto le immagini. È un'altra istanza dello stesso sistema dell'esecutore e dei codificatori: **non è una verifica fatta da persone** [I].

## 7.1 Riproduzione e cronologia [V]
- SHA-256 della pre-registrazione `0d83dda3…` uguale al file `.sha256`. Il commit `f4b8f44` (19:58:10Z) precede pilota, esecuzioni e pacchetti: in v5 non era così. L'ora è quella di git, auto-dichiarata; il commento sul ticket con l'hash non è nel repo [L].
- `test_lotti.py` passa (649 lotti). C5 ricalcolato dai fogli grezzi e dalla chiave riproduce i valori: S2 47/84 = 0,560 e 43/84 = 0,512; C5a = 0,6819 e 0,6902, media 0,686; GFU 6/23, ADP 19 e 17 su 35, PA/AS 22 e 20 su 26.
- Non rieseguito `run.py` per intero; fonti non riscaricate; fonti dei cantieri non aperte [L].

## 7.2 Pre-registrazione e arresto
- Soglie non spostate; soglia implicita su S2 (0,6439) e potenza a registro prima delle codifiche. Regola di arresto applicata. Il cambio di regole dopo v5 è dichiarato e trattato come prova nuova: ammissibile. Debolezza: la pre-registrazione è stata scritta conoscendo C5a di v5 (0,7083).
- La regola cantiere è stata scritta senza conoscere il numero di poligoni (6, mentre si prevedeva "pochi o nessuno") e applicata senza cambiarla.
- Mancano modello, versione e temperatura dei codificatori (richiesti da 2.1) [L].

## 7.3 Scarto della prima consegna
Ammissibile e documentato, con riserve. Il revisore ha ricalcolato C5 con la consegna scartata (da `1330ea1`): S2 48/84 per entrambi, C5a = 0,691, **sotto 0,70 comunque**: lo scarto non ha deciso l'esito [V]. Riserve: motivo basato su dichiarazione dei codificatori non verificabile; seconda consegna con circa 1–1,5 minuti per 21 immagini [L]; il foglio non dice quale istanza ha scritto quale riga [L]. Test–retest tra le due consegne: la quota binaria cambia su 7 lotti per codificatore; rumore su C5a circa ±0,011, dello stesso ordine dello scarto dalla soglia (0,014) [I].

## 7.4 Post-stratificato C5
- Disegno corretto. S1 (565, codifiche di v5) pesa l'87% della stima e non è nuova evidenza. Fatto nuovo: i lotti in ambito (44% della capacità edificabile, 16.160 di 36.744 alloggi a FAR 1) non erano mai stati guardati: il "passa" di v5 non li copriva.
- Il pooled non è distinguibile da 0,70 (IC di Wilson [0,614; 0,743] e [0,623; 0,750]): si può dire "la regola pre-registrata non è soddisfatta", non "la quota vera è < 0,70". Il difetto sta in S2 (censimento): 47 e 43 successi contro i 55 necessari.
- Oltre "non passa" [I]: in ambito 0,51–0,56 contro 0,70–0,72 fuori; per classe in S2 edificabili 0,489, riuso 0,577, attivazione 0,604; PA/AS 0,81 regge, ADP 0,51, GFU 0,26; le 17 GFU edificabili hanno 5 successi (0,29); per stato B (istruttoria) 0,27 su 11, A 0,51, C 0,75 su 8. Descrittivo: contando V come non edificato, le GFU salgono a 9/23 (0,39), ancora molto sotto. Non rifare C5 con un'altra definizione di successo sugli stessi dati.

## 7.5 Codificatori LLM
Kappa binario su tutti i casi 0,934 (accordo 0,967); su S2 da solo 0,904 (4 disaccordi: C325, C336, C376, C379). Note identiche: 2 su 84 (21 su 220 in v5). I conteggi di s2 sono identici per i due (75 N / 8 S / 1 M). Nessun indizio di errore sistematico trovato, ma non escludibile senza guardare le immagini: in v5 un "passa" fragile poggiava su codificatori non indipendenti, ora un "non passa" che porterebbe a cambiare la base poggia sulla stessa fonte. Verifica minima raccomandata: Dennis guarda (licenza di visione) i 17 lotti GFU edificabili.

## 7.6 GFU e CONTEXT.md
17 lotti GFU edificabili, 7.723 alloggi a FAR 1 (21% della capacità edificabile), 5 su 17 liberi o dismessi. `CONTEXT.md` definisce il lotto edificabile come area libera o dismessa; la regola lo definisce per designazione di piano, e C5 lo misura per stato fisico: finché coesistono, il criterio verifica ciò che la regola scarta. Regresso rispetto a v5 (la revisione v5 chiedeva di separare la destinazione ignota dall'attivazione).

## 7.7 Regola cantiere e Bovisa
I sei poligoni con cantiere = sì (ADP_25, ADP_29, GFU_5267, MA_6, MA_15, MA_17) vengono tutti dalla sola codifica 2, con fonti secondarie per il cantiere. MA_17 è in categoria B (nessun atto approvato). ADP_29 e Bovisa: il cantiere riguarda solo una parte, ma la regola toglie il poligono intero (Bovisa: 27 lotti, 63,8 ha, 58,1 ha edificabili, circa 5.100 alloggi a FAR 1). Tessuto consolidato: 52 lotti, 112,8 ha, 9.121 alloggi, mai visti in foto. La capacità edificabile a FAR 1 è una forbice 29.000–45.700 (+57%).

## 7.8 `potenziale_vuoto`
Errore del report: i lotti marcati 1 sono **127 su 649** (96 E, 30 A, 1 R), tutti fuori ambito, non "1 su 127"; vale 0 su tutti gli 84 lotti in ambito. L'accordo con Q1 promesso da 1.6 non è riportato; controllo indicativo: 78% dei marcati L/C/D (18/23) contro 66% dei non marcati (52/79) [I].

## 7.9 Rischi per le prove successive
Banco: non mostrare le GFU come edificabili validate. Base P/E e A1–A4: usare più scenari (29k–46k alloggi a FAR 1). A3/A4: `disponibile_da` non calcolato, 30 stati "non determinato". B0–B6: l'indipendenza dei metodi non va confusa con quella dei codificatori (stesso modello).

## 7.10 Difetti
**Gravi**
- **G1.** C5 è falso (0,686 < 0,70), localizzato in S2; confermato dalla consegna scartata (0,691). Regola di arresto scattata: nuova versione, non ripetizione identica.
- **G2.** Le GFU come lotti edificabili contraddicono `CONTEXT.md` e la misura C5. Correzione: classe o attributo separato "edificabile per destinazione, non verificato".
- **G3.** Il fallimento poggia, come il "passa" di v5, solo su codificatori LLM. Correzione minima: Dennis guarda i 17 lotti GFU.

**Da correggere**: C1 `potenziale_vuoto` nel REPORT (127/649); C2 le due cifre di kappa nel REPORT sono kappa e accordo tra i due codificatori, non uno per codificatore; C3 regola cantiere: fonte, qualità e parte coinvolta per ognuno dei sei poligoni (MA_17 non è stato avanzato); C4 REPORT §8 proponeva una "candidata con riserva" che il protocollo non prevede; C5 registro: ora di avvio della run sui fogli scartati, istanza per riga, modello e versione; C6 definizione dello scenario "senza Bovisa".
**Minori**: M1 etichette obsolete in `cascata.csv`; M2 dire quale delle tre definizioni di Bovisa è usata ogni volta; M3 riproducibilità da zero non verificata; M4 conteggi di s2 identici.

## 7.11 Esito proposto: **cambia**
Non passa per la regola pre-registrata; ripetere la prova identica darebbe lo stesso risultato. Cambiare: GFU (G2), regola cantiere (C3), controllo minimo del fallimento (G3). Resta: geometria e pipeline (hash identico, test verde) e il censimento in ambito. Una v7 cambia solo questi punti, con nuova pre-registrazione committata prima.

## 7.12 Cosa deve decidere Dennis (raccomandazioni del revisore)
1. **GFU**: classe o attributo separato, fuori dal totale e riportato come scenario; in alternativa ridefinire in `CONTEXT.md` "lotto edificabile" come "libera, dismessa o designata", ma allora C5 deve misurare altro, pre-registrato prima di guardare altri dati.
2. **Cantiere e Bovisa**: la regola vale solo con fonte ufficiale o con cantiere confermato da due codifiche; Bovisa "da verificare" finché non si conosce la parte interessata; MA_17 non tessuto consolidato senza atto approvato.
3. **Verifica dei 17 lotti GFU** da parte sua, prima di cambiare la base.
4. **Ticket**: non congelare; aprire la v7 con nuova pre-registrazione; non usare lo stato "candidata con riserva".
5. **Capacità**: dichiarare nelle prove successive la forbice 29.000–45.700 alloggi a FAR 1.

Non verificato dal revisore: riesecuzione completa di `run.py`, immagini, fonti online dei cantieri.
