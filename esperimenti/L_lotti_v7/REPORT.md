# Report di laboratorio — Base L v7: GFU separate e validazione cieca nuova (ticket #40)

Stato: **congelata il 22/11 per decisione di Dennis** (`VERSIONE.md`): C1–C4, C6, C8 passano; C5 dei modelli 0,722 ma dipende dalla deviazione sul codificatore 1 (revisione: ripeti); **controllo umano 0,737 (0,730 con la precisazione di Dennis su H36 e H57): inconcludente** per la fascia pre-registrata 0,65–0,75, dato per passato da Dennis come decisione, non come misura. Report assemblato dal coordinatore.

## 1. Ipotesi e soglia
Testo completo in `esecuzioni/00_preregistrazione.txt` (versione 2, SHA-256 `7f98ab31…`, commit 114bea1 del 16/11 21:07Z, prima di ogni esecuzione). La prima stesura (`9342f700…`, commit e5ca67b) è superata: la regola del cantiere chiedeva una fonte ufficiale "nella riga" e non "riferita al cantiere"; la correzione è stata fatta dopo un conteggio in sola lettura ed è dichiarata.

Regole (lettura del coordinatore delle raccomandazioni della revisione v6, `tesi/DECISIONI.md` 16/11):
- **GFU** (4 perimetri 2012 sostitutivi, Bovisa compresa) in una classe a parte, "edificabile per destinazione, non verificato", fuori dai totali; capacità solo come scenario.
- **Tessuto consolidato** solo con cantiere da fonte ufficiale riferita al cantiere o confermato da entrambe le codifiche del censimento: nessun poligono la soddisfa.
- **C5 con codifiche nuove**: campione nuovo stratificato (seme 7711): 150 lotti fuori ambito per classe, censimento dei lotti in ambito (86), 100 particelle nuove; soglie come v5/v6 (kappa binario ≥ 0,60; C5a ≥ 0,70; C5b limite inferiore Newcombe ≥ 0,25). Potenza dichiarata prima: P(passa) 0,03 con quota vera 0,65, 0,48 con 0,70, 0,98 con 0,75.
- C1–C4, C6, C8 come v6.

## 2. Dati e fonti
Come v6 (cache non riscaricata). Immagini AGEA 2018–2019 (sola visione) e Sentinel-2 cloudless 2025 EOX (CC BY-NC-SA 4.0).

## 3. Metodo
`run.py` v7 = v6 con modifiche marcate `[v7]`. Hash di contenuto `49327c8a…` identico nelle esecuzioni (C8).
**Codifiche**: 336 casi per codificatore, in 16 blocchi da 21 immagini, un'istanza nuova per blocco, riga scritta subito, identificativo d'istanza e ora per riga.
- **Codificatore 2 = Claude Haiku**, come pre-registrato.
- **Codificatore 1 = Claude Opus**: **deviazione dalla pre-registrazione** (prevista Fable). Fable è stato interrotto dai limiti d'uso e poi ha richiesto crediti a pagamento, non attivati. Il codificatore 1 è stato rifatto da capo con Opus, deciso e registrato prima di ogni confronto. Limite: Opus è probabilmente il modello delle codifiche v5 (30 lotti in comune). Le righe parziali di Fable sono in `codifiche_fable_parziali/`, solo informative.
- **Incidenti di esecuzione** (registro): una run senza i fogli uniti (C5 "in attesa"); una run fermata da un errore di codice puro nella scrittura del JSON (chiavi-tupla), corretto senza cambiare calcoli; la cartella di quella run, con JSON troncato, spostata in `esecuzioni/_interrotte/` senza aprirla.
- Anomalie di compilazione dichiarate dalle istanze (campi vuoti, righe riscritte per colonne sfasate, un'ora inventata e corretta) sono a registro; nessuna cambia Q1 salvo quanto indicato lì.

## 4. Risultati
**Conteggi**: 216 lotti edificabili, 167 da riusare, 268 aree di attivazione; **50 lotti nella classe GFU** (Piazza d'Armi 11, Ronchetto 2, Porto di Mare 10, Bovisa 27); tessuto consolidato 0.

| Capacità (alloggi) | FAR 0,5 | FAR 1 | FAR 2 |
|---|---|---|---|
| Lotti edificabili (base) | 16.389 | 32.885 | 65.885 |
| + GFU senza Bovisa (scenario) | 20.247 | 40.608 | 81.338 |
| + GFU con Bovisa (scenario) | 22.783 | 45.683 | 91.497 |

Lotti da riusare: 672 / 1.429 / 2.938 (recupero 2.898). Forbice degli edificabili a FAR 1 negli scenari pre-registrati: circa 29.000–45.700 (`tabelle/scenari_capacita.csv`).

**C5** (`esito_criteri.json`, `tabelle/controllo_ortofoto_esito_C5.csv`):
- Kappa binario 0,78 (accordo 0,89): più basso che in v5/v6 (0,93–0,95), coerente con due modelli diversi.
- Quota stimata di lotti liberi o dismessi: **codificatore 1 (Opus) 0,760** [IC Wilson 0,707; 0,806]; **codificatore 2 (Haiku) 0,684** [0,628; 0,735]. **C5a = 0,722 ≥ 0,70: passa.** Particelle qualsiasi: 0,15 e 0,12. C5b: limiti inferiori 0,512 e 0,468.
- Per strato (media dei due): fuori ambito E 0,78, A 0,82, R 0,55; in ambito E 0,56, R 0,68, A 0,63.
- Per classe: attivazione 0,77, edificabili 0,67, riuso 0,59. Per gruppo di ambito: PA 0,72, AdP 0,49.
- Lotti in comune con v5 (30) e v6 (61): kappa tra 0,59 e 0,90; quote simili a quelle di allora (informativo).

## 5. Esito
Secondo la regola pre-registrata i criteri passano; la revisione propone **ripeti** per C5 (G1: il passaggio dipende dalla sostituzione Fable → Opus; con il codificatore pre-registrato la proiezione è C5a ≈ 0,68 [I]). Controllo umano di Dennis (60 lotti, `controllo_umano/ESITO_umano.txt`): 51 liberi o dismessi, 7 non giudicabili (6 in aree di attivazione fuori ambito), 2 in uso; edificabili e da riusare 38 su 40 (informativo); i modelli sono più severi di Dennis sui 35 lotti in comune (Dennis 0,94, Opus 0,74, Haiku 0,60). Base congelata per decisione di Dennis (§8).

## 6. Limiti
- C5a passa per la media dei due codificatori: **il codificatore 2 da solo (0,684) sarebbe sotto 0,70**. La differenza tra modelli (0,76 contro 0,68) è dello stesso ordine del margine dalla soglia.
- Deviazione sul codificatore 1 (Opus invece di Fable) e possibile correlazione con le codifiche v5.
- I codificatori sono modelli linguistici della stessa azienda, senza riferimento umano (decisione di Dennis del 14/11).
- I lotti in ambito (in particolare gli AdP: 0,49) e i lotti da riusare (0,55–0,59) restano deboli.
- Diverse istanze segnalano contorni multipli, spezzati o autointersecanti (C509, C543, C557, C562, C602, C611, C614, C621, C715): possibile problema di geometria dei lotti. L'acqua non è una categoria dello schema (C627, C761).
- GFU, perimetri 2012 sostitutivi [H] e destinazioni non verificate [L].

## 7. Revisione indipendente
Testo completo in `REVISIONE.md` (`revisore-metodologico`; altra istanza dello stesso sistema, non una verifica umana). **Esito proposto: ripeti (solo C5).**
- Riproduzione [V]: hash, fogli uniti e C5 ricalcolato da zero coincidono (C5a 0,7221; kappa 0,780). La costruzione della base regge.
- **G1**: il "passa" dipende dalla deviazione sul codificatore 1 (Opus invece di Fable). Sui 77 lotti codificati anche da Fable: Fable 0,662 contro Opus 0,740; proiezione con Fable C5a ≈ 0,68 [I]; bootstrap IC di C5a [0,665; 0,777], P(C5a < 0,70) ≈ 0,22 [I]. Disaccordo sistematico tra i due codificatori (27 contro 5).
- **G2**: le regole della v7 (GFU separate, cantiere) non sono state confermate da Dennis: il passo (0) della pre-registrazione è stato saltato dal coordinatore.
- **Errore del coordinatore** segnalato dalla revisione: il JSON troncato della run interrotta contiene **tutto C5** (C5a 0,7221), non "valori parziali" come scritto nel registro, ed è stato committato (af76460) durante la run finale. Il coordinatore non l'ha aperto, ma git non lo dimostra; dopo quel momento nulla è cambiato (run.py, fogli, risultato identico).
- Geometria: nessun poligono non valido (0 su 701); 122 lotti a più parti, 127 con fori, 15 schegge sotto 10 m². Acqua: C627 = E00170 (4,65 ha, lago su oltre metà) codificato L sulla sola parte a terra; contando C627 e C761 come non successo C5a = 0,713.
- Da correggere: `test_lotti.py` fallisce sui file `.sha256` dei blocchi; `potenziale_vuoto` e la sua tabella con Q1 da riportare; maschera dei corpi idrici; schegge geometriche; isolamento delle istanze solo dichiarato; registro (JSON "parziale", ora errata, versione dei modelli); scenari (iv) e (v) mancanti in `scenari_capacita.csv`.
- Raccomandazione per chiudere C5: Dennis codifica alla cieca un sottocampione stratificato nuovo (es. 60 lotti) con soglia 0,70 pre-registrata; in alternativa completare Fable con crediti. Sconsigliato accettare il "passa" così com'è.

## 8. Cosa passa alla prova successiva
Base L v7 congelata per decisione di Dennis il 22/11 (`VERSIONE.md`; limiti nelle sezioni §6 e §7) con le classi edificabile / da riusare / attivazione e la classe GFU separata; capacità dichiarata come forbice di scenari; avvertenze sui lotti in ambito AdP e sul riuso per banco, Base P, Base E, A1–A4.
