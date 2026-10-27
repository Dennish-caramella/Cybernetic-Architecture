> **Superata** da `2026-10-27_critica-spatial-milano-lab-sui-testi.md`, fatta dopo aver letto paper e review. Questa versione si basava solo su riassunti.

# Tavola rotonda: critica a "Spatial Milano Lab" e come portarlo a livello PhD

Data: 2026-10-27. Sintesi di Claude su round 1 di sei voci e revisione di integrità. **Stato: provvisorio.**
Etichette: [S] dai dati esportati dell'artifact; [R] dai riassunti della sessione originale (seconda mano); [I] inferenza; [H] ipotesi da verificare; [L] lacuna.

## 0. Limiti di questa tavola (leggere prima)
- **Non letti**: `paper.md`, `review1.md`, `review2.md`, codice del modello, dati di base. Le voci hanno letto solo il briefing (`lab.json` più riassunti [R]) e le proprie schede. [L]
- **Le voci non sono sei verifiche indipendenti.** Tutte partono dallo stesso briefing: i numeri ricorrenti (38 CAP contro 88 NIL, rho 0,987, 7,5 NIL effettivi, 11 su 20) sono una fonte sola, in parte [R]. La frequenza con cui una critica ricorre non ne prova la validità. La convergenza sulla cooptazione è indotta: il briefing chiude citando quel rischio dal Report fondativo, e le voci hanno lenti partecipative. [I]
- **Round 2 non eseguito**, quindi nessuna voce ha risposto alle altre. Manca la voce di statistica spaziale che più voci hanno chiesto. [L]
- Alcune critiche [R] potrebbero essere già assorbite: il null per blocchi di NIL e la correzione di calibrazione sono stati aggiunti dopo le review. "Quasi un lancio di moneta" (11 su 20) potrebbe riguardare una versione precedente. Discrepanza da non confondere: +43% (review 2, [R]) contro +48% (`lab.json`, [S]) sono versioni diverse del confronto persone/PGT.

## 1. Limiti del laboratorio, per ordine di gravità
1. **Il segnale empirico principale è fragile.** [S] AT "risk" non è significativo col null per blocchi di NIL (dep_resid p = 0,067; conc_q5 p = 0,092; dDI p = 0,103); 58 siti in 12 NIL (7,5 effettivi); stabilità nella griglia di sensibilità 0,14; effetto dDI +0,00033 (0,4% del DI di base). Con 7,5 unità effettive la potenza è bassa: una non significatività non prova l'assenza di segregazione. [I] Gli indicatori di segregazione derivano dalla stessa fonte di reddito per CAP, quindi sono un solo segnale. [R]
2. **Risoluzione dei dati inferiore alla precisione dichiarata.** [S] Reddito noto per 38 CAP, affitto per 88 NIL. Differenze di pochi euro al mese (−92 contro −22/−38) su dati imputati richiedono propagazione dell'incertezza. [I] Il rho 0,987 tra tasso target e affitto [R] indica che la domanda è in parte un riflesso della mappa degli affitti. [I]
3. **Pre-registrazione indebolita.** [S] La regola è datata 2026-10-27 (autodichiarata, senza timestamp esterno [I]) e il file elenca sei modifiche dopo i risultati (conc_q5, soglia 500 famiglie, pool del null, famiglia BH da 3 a 4 insiemi, p unilaterali, null per blocchi). [R] Un test dei falsi positivi è stato rilanciato dopo un FAIL. Le modifiche sono dichiarate, ma l'osservatore è intervenuto sullo strumento di misura. [I]
4. **Chi scrive le regole.** [I] Il briefing dice che i pesi degli archetipi sono sintetici e che tau 0,3, moltiplicatore 1,5, FAR, costi sono assunzioni [S]. Che criteri, soglie e catalogo siano "scritti dall'autore" e che "Il tuo voto" sposti solo i pesi è inferenza dalle descrizioni, non documentata nel briefing. Nessuna persona reale ha usato lo strumento in un processo. [L] È il rischio di cooptazione già indicato dal Report fondativo.
5. **Costi e fattibilità assunti.** [S] FAR 1,0, resa 0,7, 80 m² per alloggio, 2000 €/m², budget 1 miliardo come costanti. L'etichetta ERP "potential" vale solo con suolo a 1 €/m² (proprietà non verificata); a prezzo di mercato 1,32 famiglie per M€ contro mediane 1,58/1,39, e 1.729 famiglie servite contro 2.254. Nessuna analisi di sensibilità sul costo dichiarata nel briefing. [L] Il filtro di fattibilità è urbanistico, non tecnico (contaminazione, vincoli idraulici, frammentazione proprietaria non risultano). [L]
6. **Pluralità dei portafogli forse apparente.** [S] P1-P6 servono 1.781-1.795 famiglie. L'uguaglianza riguarda le famiglie servite, non necessariamente i siti: la sovrapposizione dei siti non è nel briefing. [H] Se i pesi non muovono i portafogli, la scelta tra portafogli è apparente; se invece i siti cambiano, è un risultato robusto. Da misurare (§2, punto 4).
7. **Proprietà, finanziamento e governance fuori dal modello.** [L] Chi possiede il suolo e chi attua un portafoglio non risulta tra gli oggetti d'analisi.

## 2. Come portarlo a livello PhD: sei interventi
Per ognuno: prova, esito atteso e criterio di fallimento da fissare **prima**. Le soglie numeriche indicate sono proposte da discutere. [H]

1. **Congelare e rendere replicabile il verdetto.** Pubblicare hash del codice, parametri e famiglia di test prima di rieseguire; timestamp esterno (registro di pre-registrazione). Replica con specificazione alternativa scritta da altri. *Fallimento*: l'etichetta di AT, ERP o RIG cambia segno con la specificazione alternativa. Nota: la replica a codice congelato verifica la riproducibilità, non la validità.
2. **Rompere la dipendenza dal reddito per CAP.** Reddito a scala più fine o un indicatore indipendente (per esempio affitto o catasto a livello NIL), con propagazione dell'incertezza (ricampionamento) e **effetto minimo rilevabile dichiarato in anticipo**. *Fallimento*: meno di una quota prefissata di esiti stabili; in caso di nullo, concludere "non rilevabile con questa potenza", non "assente". Con 7,5 NIL effettivi va dichiarato quale effetto è rilevabile.
3. **Validazione a blocchi spaziali anche per il verdetto.** Nel briefing il PR-AUC 0,33 contro 0,93 [R] riguarda il rilevatore ML di lotti, non l'audit: non estenderlo. Per l'audit: stabilità del verdetto sotto nuovi semi e ricampionamento di NIL interi. *Fallimento*: il verdetto cambia in più di una quota prefissata di ripetizioni (proposta 20%).
4. **Testare se i pesi muovono i portafogli.** Pesi agli estremi del simplesso (non solo dagli archetipi), matrice di correlazione dei 9 criteri, sovrapposizione dei siti (Jaccard) tra pesi estremi. *Fallimento (proposta)*: Jaccard mediano sopra 0,9 e meno di 3 dimensioni effettive dei criteri; in tal caso dichiarare che l'ipotesi sulla scelta tra portafogli non è testabile con questo modello.
5. **Sensibilità su costo, resa, FAR e regime del suolo.** Tre regimi (suolo gratuito, ERP, mercato) e costo per tipologia di area, con registro di proprietà dove ottenibile. *Fallimento*: se il solo cambio di regime ribalta il confronto tra portafogli o tra insiemi, i valori "per euro" non si riportano.
6. **Passare dagli archetipi sintetici alle persone, con numerosità e misure dichiarate.** Elicitazione di criteri e soglie (non solo pesi) con un campione reale e variegato; confronto con i nove criteri attuali e con i pesi degli archetipi. Servono numerosità, esito misurato e soglia: "2-3 sessioni" è aneddotico. *Fallimento (proposta)*: i pesi osservati cadono fuori dalla regione che contiene il 90% dei pesi simulati, oppure i criteri proposti coincidono con i nove attuali e i portafogli non cambiano oltre la variabilità tra ripetizioni. Se coincidono, la partecipazione è decorativa; se divergono molto, il modello attuale era cooptato. Test di decisione con due gruppi (trasparenza completa contro sola mappa) è un'estensione.
7. **Revisione tecnica cieca di un campione di siti** (fattibilità e vincoli). Il contenuto di H4 non era nel briefing: collegare al Report prima di usarlo come test. *Fallimento*: quota di scarti sistematici oltre una soglia fissata a priori.

## 3. Cosa regge, con riserva
- [S] Il portafoglio come pluralità invece del "lotto migliore", la dichiarazione degli esiti non significativi e delle modifiche, il rifiuto di forzare un verdetto su AMB_DEG (5 siti) e su ERP a prezzo di mercato.
- [S] RIG (855 siti, 53 NIL, 26,6 effettivi; reddito residuo −68 contro −16 €/mese) è il segnale di collocazione più forte, ma è dichiarato "contesto, non verdetto", usa lo stesso reddito per CAP e non è stato verificato col null per blocchi: qualificarlo come più forte tra i deboli, non come robusto. [I]
- La pre-registrazione ha valore soprattutto come disciplina; il suo valore probatorio è ridotto dalle modifiche e dall'assenza di timestamp esterno. [I]

## 4. Lacune del team
- **Statistica spaziale** (dipendenza spaziale, problema dell'unità modificabile 38 CAP contro 88 NIL, potenza, test per blocchi): la più urgente.
- Economia abitativa e mercato immobiliare; diritto urbanistico e PGT (il contesto italiano non è coperto dalle schede); voce di red team/riproducibilità; abitanti e operatori locali (le schede riportano workshop con esperti, non residenti [S: scheda 37, via voce AZ]).

## 5. Punti ciechi delle voci (dichiarati)
DC svaluta la mediazione tecnica; MV è indulgente sulla validità statistica; PK rischia di lasciare "conversazione" come metafora; DG smonta senza meccanismo; IE tratta la fattibilità come precondizione; AZ: nessuna misura di partecipazione di residenti nelle sue fonti.

## 6. Decisioni che spettano a Dennis
1. Procurare `paper.md` e le review, così da rifare questa tavola sui testi (e una voce di statistica spaziale, da definire).
2. Scegliere quali tre degli interventi del §2 diventano la prossima fase sperimentale, con soglie fissate da te.
3. Decidere se il laboratorio resta un dispositivo esplorativo (e allora dichiarare i limiti come parte del risultato) o aspira a un risultato inferenziale su segregazione (e allora servono gli interventi 1-3).
