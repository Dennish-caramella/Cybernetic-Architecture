# §7 Revisione indipendente — Base L v5 (ticket #38)

Revisore metodologico, 14/11/2026. Non ho eseguito la prova. Non ho aperto le immagini (AGEA: licenza di sola visione; Sentinel-2: non serve). Sono un'altra istanza dello stesso sistema dell'esecutore e, con ogni probabilità, dei codificatori: questa revisione non è una verifica fatta da persone (`06_riesame_spatial_milano_lab.md` §0) [I].

Script della revisione: `revisione/verifica.py`. Ricalcola C5 dai fogli grezzi e dalla chiave, le analisi informative di questa sezione e C9. Si esegue dalla cartella della prova. Non scrive nulla.

## 7.1 Riproduzione [V]
- **Esecuzione.** Ho rieseguito `run.py --no-fetch` (SHA `3ace4844…`, uguale a `VERSIONE.md` e alle esecuzioni 3–5) su una copia della cartella fuori dal repo, con la cache condivisa in sola lettura. Durata 490 s.
- **Risultati della riesecuzione:**
  - hash del contenuto `440bf046ea72`, identico;
  - conteggi 216 E / 176 R / 309 A;
  - C1–C6 e C8 veri, C9 falso;
  - `esito_criteri.json` identico all'originale salvo la chiave `registro`;
  - le 12 tabelle di `tabelle/` identiche byte per byte. `sensibilita_senza_gfu.json` è copiato, non rigenerato: non ho eseguito `--sens-gfu`.
- **Test.** `test_lotti.py` passa sull'originale e sulla copia (701 lotti). `git status` resta pulito dopo il test. pytest non serve: il test è uno script con `assert`.
- **Hash dei file.** Pre-registrazione `5e2da4ab…`, chiave `d787a547…`, fogli C5 `999bf3e2…` e `7de45185…`, censimento `a3ad9dda…` e `5eef113b…`. Tutti coincidono con i file `.sha256` e con il registro, dove sono riportati.
- **C5 ricalcolato dai fogli grezzi** (unione con la chiave, non dalla tabella di esito). Kappa binario 0,945 (accordo 0,973); kappa Q1 0,876. C5a = 170/240 = 0,7083. Cod. 1: 84/120 [0,613; 0,775]; cod. 2: 86/120 [0,630; 0,790]. Base 16/100 per entrambi. Valori identici a `esito_criteri.json`.
- **Limite.** La riesecuzione parte dalla cache e non riscarica le fonti online: verifica la pipeline, non la disponibilità attuale dei servizi [I].

## 7.2 Pre-registrazione e cronologia
- **SHA-256.** Lo SHA-256 del testo è `5e2da4ab…f4cdb6a39df` e corrisponde al file `.sha256` e alla riga 1 del registro [V].
- **Il commit `0490f98` non precede le esecuzioni [V, `git log`].** È delle 11:15:49Z, mentre il pilota è delle 10:30Z, le esecuzioni complete 1–4 vanno dalle 10:39 alle 11:14Z e la codifica 1 del censimento è delle 11:04Z. Il commit dei risultati (`aad07a3`) arriva un secondo dopo, alle 11:15:50Z. Il commit precede solo la codifica 2 del censimento (inizio dichiarato 11:16:22Z) e le codifiche C5 (commit `3eb8d61`, 15:20Z).
  - `VERSIONE.md` lo dice correttamente ("non committata… la precedenza si regge su registro e mtime [I]").
  - REPORT §1 ("in commit separato") lascia invece intendere una precedenza che git non dimostra.
- **Quanto pesa [V/I].** Le soglie decisive (C5: kappa ≥ 0,60, C5a ≥ 0,70, C5b ≥ 0,25; C9b ≥ ceil(5n/6)) sono quelle di v4, committate il 12/11 in `f287378` [V]. Restano auto-datate solo le regole nuove di v5: l'insieme degli ambiti, D4 sugli ambiti 2030, le GFU sostitutive e il seme 5511. Nel loro contenuto non trovo nulla che richieda di aver visto i conteggi. La correzione del registro delle 10:40Z, che allinea il codice al testo 1.3, è coerente con un testo già esistente [I].
- **Correzioni dopo la prima esecuzione.** Sono due, registrate con motivo, e nessuna soglia è cambiata [V, registro]. Ammissibili: una correzione di codice su 2 lotti, verso la regola scritta, e una cosmetica.
- **Esecuzione 5.** Non ha una riga nel registro: `registro.txt` non è cambiato tra `aad07a3` e `3eb8d61` [V]. Mancano anche consegna, ore e SHA delle codifiche C5. Gli SHA stanno solo nei file `.sha256`, committati insieme ai risultati: l'integrità delle codifiche prima dell'unione è auto-dichiarata [I]. È lo stesso difetto già segnalato in v3, §7.2.

## 7.3 C5: passa di misura
- **Margine.** Servono 168 successi su 240 e ne risultano 170 [V]: due giudizi in meno su 240 portano C5a a 0,700, che passa; tre in meno lo portano sotto soglia.
  - Il codificatore 1 da solo sta esattamente a 0,700.
  - La quota dei lotti su cui entrambi i codificatori dicono "sì" è 0,683 [0,596; 0,760]: è riportata come informativa nella pre-registrazione di v4 e non è un criterio.
- **Lettura corretta.** La regola pre-registrata è sulla stima puntuale e va rispettata: C5 passa [V]. Ma la pre-registrazione di v4 (§2.4) dichiarava già che P(C5a ≥ 0,70) vale 0,146 con p vero = 0,65 e 0,545 con p = 0,70 [V, testo letto]. Il risultato è quindi compatibile con una quota vera tra circa 0,61 e 0,79 [I]. Si può dire "non è sotto 0,61", non "è sopra 0,70".
- **Non pre-registrati, solo informativi [V numeri, I lettura]:**
  - **lotti con capacità abitativa (E + R, n = 68):** 0,618 [0,499; 0,724] e 0,632 [0,514; 0,737]. C5a supera 0,70 grazie alle aree di attivazione (0,817), che hanno capacità 0;
  - **lotti piccoli:** 0,586 sotto 3.000 m² (58 lotti), 0,823 sopra;
  - **scarto temporale:** l'ortofoto è del 2018–2019. In 5 lotti codificati L/C/D da entrambi, il codificatore 2 annota sull'immagine 2025 "nuovo edificio" o "edificato" (C097, C101, C127, C154, C211; forse anche C199). Se fossero insuccessi, C5a scenderebbe a 0,667. Il campo s2 è a 10 m, non è un criterio e viene da un LLM: è un segnale da controllare, non una misura.
- **Conclusione.** Nessuno di questi numeri può cambiare l'esito pre-registrato. Usarli per bocciare sarebbe spostare la soglia dopo i dati, lo stesso errore di `06_riesame` §2 n. 5. Dicono però che il "passa" di C5 è fragile e che riguarda soprattutto la classe senza capacità.

## 7.4 Codificatori LLM: indipendenza
- **Accordo anomalo [V].** Kappa binario 0,945. Sono 6 i disaccordi binari sui 120 lotti e 0 sulle 100 particelle di base. In v3 l'accordo tra codificatori era 0,785.
- **Note identiche [V].** 21 note libere non vuote sono identiche parola per parola tra i due codificatori, per esempio C058 "telaio senza copertura invaso da vegetazione", C093 "incolto e sterrato con resti di fondazioni", C139 "capannone e piazzale con auto". Due persone indipendenti non producono testo libero identico in un caso su dieci. La spiegazione più semplice è lo stesso modello, con lo stesso prompt (`ISTRUZIONI.txt` identico salvo il numero) [I].
- **Cosa misura il kappa [I].** Misura quindi soprattutto la riproducibilità del modello (test–retest), non l'affidabilità tra codificatori. La precondizione kappa ≥ 0,60 non fa il lavoro per cui era stata pensata:
  - un errore sistematico del modello, per esempio "U" su poligoni piccoli o sottili, compare in entrambe le codifiche e non abbassa il kappa;
  - la media di C5a sui due codificatori non aggiunge informazione indipendente.
- **Nessun riferimento umano.** C7 è stato tolto per decisione di Dennis. In v5 nessun giudizio sulle immagini è verificato da una persona [V, pre-registrazione 2.4].
- **Dati mancanti [L].** Modello, versione, temperatura e prompt dei codificatori non sono registrati, contro `08_critica_metodologica.md` §3.3 ("pre-registrare modello, versione, temperatura, prompt"). Mancano anche le ore di inizio e fine, che le istruzioni chiedevano.
- **Note dei codificatori** (riferite dal coordinatore, non verificabili nei file [L]):
  - entrambi interrotti da un limite d'uso;
  - il codificatore A ha perso il contesto delle immagini già viste.
  - Il kappa per metà del campione è 0,926 (C001–C110) e 0,964 (C111–C220) [V]: nessuna deriva evidente. Il punto di ripresa però non è noto.
- **Cecità.** È solo di disciplina [V, codice e git]. `chiavi/campione_chiave.csv` e gli esiti di v3 erano sullo stesso disco prima della codifica. `censimento_AT/codifica_1.csv` stava nella stessa cartella data al codificatore 2 del censimento. Le 18 discordanze di C9 rendono improbabile una copia in quel caso [I]. Per C5 non ho prove né di fuga né di cecità [L].
- **Per il ticket.** Con codificatori LLM "esterni" significa altre sessioni, non altre persone. Dennis deve decidere se questo soddisfa "due codificatori esterni".

## 7.5 Lotti da riusare (0,532)
- **Numeri [V].** 33 successi su 62 giudizi: [0,41; 0,65], intervallo approssimato perché i giudizi sono 31 lotti × 2 codificatori. `dbt_diruto` vale 0,50 su 22 lotti per il cod. 1. Molti insuccessi sono "U" con uso "U?": dall'alto non si vede se un edificio è in uso.
- **Lettura [I].** È anzitutto un limite di costrutto: lo stato d'uso di un edificio non si osserva su un'ortofoto a 20–50 cm. Il valore non dimostra che la classe sia sbagliata, ma la classe R non è validata. Pesa poco sulla capacità: 1.564 alloggi a FAR 1, pari al 4,8 % della capacità degli edificabili (32.885), e 3.029 con il recupero. Pesa molto sulla tesi, se il riuso diventa un argomento.
- **Correzione.** Marcare R come "non validata" nelle prove successive. Validarla con un'altra fonte: data del rilievo DBT "diruto", accesso civico già in bozza (commit `863dccf`), sopralluogo a campione.

## 7.6 D4 sulle GFU con perimetro 2012 sostitutivo [H]
- **Applicazione.** Coerente con il testo 1.3 per i lotti edificabili [V, test e `copertura_ambiti_2030.csv`]. Sono 37 lotti, 146,8 ha, tra le aree di attivazione con capacità 0.
- **Problema di costrutto [I].** `CONTEXT.md` definisce l'area di attivazione come "area dismessa con potenziale strategico **non residenziale**". La regola invece ci mette aree di cui la destinazione **non si conosce**. "Ignoto" diventa così "non residenziale", e 147 ha entrano in una classe che le prove A1/A2 potrebbero trattare come servizio o verde potenziale.
- **Fonti contrarie** (lette da me nei file del censimento, non sulle fonti):
  - Piazza d'Armi: il protocollo Invimit del 23/12/2025 indica residenze, in larga parte a locazione calmierata [V nel registro, fonte ufficiale per l'elenco delle istruzioni];
  - Porto di Mare: concorso del "Piano casa" [S];
  - Bovisa-Goccia: campus del Politecnico [S], ragionevolmente non residenziale.
  - Su 4 GFU, quindi, 2 probabilmente ammettono residenza [I].
- **Perimetri.** Che le GFU 2030 corrispondano ai perimetri AT 2012 non è verificato [L]. Bovisa 2012 misura 85,6 ha e il codificatore 2 annota "solo una parte del perimetro 2012" [S].
- **Asimmetria.** San Siro-Trotto e Rubattino non hanno un poligono sostitutivo e seguono la pipeline non AT [V, pre-registrazione 1.2c].
- **Effetto sui numeri [V].**
  - Senza le GFU sostitutive i lotti edificabili salgono di 6 e la capacità a FAR 1 da 32.885 a 34.051. Le aree di attivazione scendono di 41, perché quelle particelle, fuori dal canale AT, escono quasi tutte dalla base.
  - Se le GFU fossero residenziali per la via AT, varrebbero 12.798 alloggi a FAR 1 [I, `esito_criteri.json`].
  - La capacità degli edificabili è quindi incerta tra circa 32.900 e 45.700 alloggi a FAR 1 (+39 %), a seconda di una sola ipotesi [I].
- **Deviazione testo–codice [V].** 9 lotti da riusare stanno in ambiti con residenza "no" o "non verificata" (5 Bovisa, 2 Porto di Mare, MA_2, MA_15) e conservano la capacità: 135 alloggi a FAR 1, 131 con il recupero. Il testo 1.3 dice "una particella in ambito 2030… va tra le aree di attivazione". Il test D4 controlla solo i lotti edificabili. L'effetto è piccolo, ma è lo stesso tipo di scarto corretto per 2 lotti edificabili dopo l'esecuzione 1.

## 7.7 C9: fallisce. Difetto dello strumento e dell'accesso, non della geometria
**Esito.** C9a [9, 15] su 29; C9b 11 su 29, con soglia 25 [V]. Per la regola 3.5 l'esito è "non passa", non "in attesa di Dennis": C9b manca e il codificatore 2 ha lacune che non sono N [V, codice e testo coerenti]. La riconciliazione con Dennis (`consenso.csv`) non può far passare C9b, che è definito prima della riconciliazione.

Le cause sono quattro, tutte nello strumento [V nei fogli, I nella lettura].
- **Categorie sovrapposte per costruzione.**
  - C significa "la ricerca non trova atti successivi".
  - N significa "le sole fonti utili stanno su siti bloccati **o non ci sono**".
  - "Non ci sono" è la condizione di C. Le 6 discordanze N contro C (MA_2, MA_3, MA_9, MA_13, MA_14, GFU_5264) nascono da qui.
- **Istruzioni del codificatore 2 più larghe della pre-registrazione.** La pre-registrazione 3.3 dice "stampa e operatori privati [S] non decidono". `censimento_AT/ISTRUZIONI.txt` chiede solo di marcare `fonte_ufficiale = no` e non dice che una fonte non ufficiale non può decidere la categoria. Delle 18 discordanze, 12 hanno una fonte non ufficiale nel codificatore 2: MA_5 A da Hines, MA_15 A dalla stampa, GFU_5267 A da un documento MIT, che non è nell'elenco.
- **Accesso.** Entrambi i codificatori indicano come documenti decisivi pagine di `www.comune.milano.it`: 20 per il cod. 1 e 13 `documento_da_aprire` per il cod. 2, tra cui le delibere di approvazione PA7 n. 465/2023 e PA5. Il sito è escluso per decisione di Dennis ("senza materiale utile"). Le due codifiche, indipendentemente, contraddicono quella premessa [I].
- **Ricerca del codificatore 1 non documentata per poligono.** `censimento_c1.py` assegna N per difetto a ogni poligono non trattato a mano. Per 15 poligoni la nota è sempre la stessa ("nessuna fonte ufficiale raggiungibile trovata…") [V].

**Conseguenze per la base [V].** I 136 lotti AT hanno `stato_attuativo` = "in attesa del censimento". I 43 lotti edificabili AT valgono 12.301 alloggi a FAR 1, il 37 % della capacità degli edificabili. Per più di un terzo della capacità `disponibile_da` è quindi ignoto.

## 7.8 Altri controlli [V]
- C1–C4, C6 e C8 passano anche nella mia riesecuzione. C4 verifica la formula, non la plausibilità (già detto nel §6).
- L'allocazione C5 è proporzionale ai lotti non AT (37 / 52 / 31 su 173 / 245 / 147), quindi C5a descrive la popolazione, a differenza di v3. Sono 13 i lotti già visti in v3; senza di loro C5a = 0,71.
- La licenza degli strati regionali non è dichiarata [L]. Una base congelata con una licenza ignota va segnalata nel `VERSIONE.md` finale.

## 7.9 Rischi per le prove successive [I]
- **Banco:** non deve mostrare R e A come validati. Le GFU vanno visualizzate come "destinazione ignota", non come attivazione.
- **Base P / Base E:** la capacità ha una forbice di circa il 39 % per un'unica ipotesi sulle GFU (§7.6), più lo scarto temporale dell'ortofoto. Base E e il rapporto domanda/offerta vanno calcolati almeno sui due scenari (con e senza GFU residenziali), pre-registrati.
- **A1 e A2:** 147 ha di "attivazione" vengono dall'ipotesi GFU. Se le aree di attivazione aumentano il punteggio dei lotti vicini, Piazza d'Armi, Bovisa e Porto di Mare producono un vantaggio artificiale.
- **A3:** il recupero dei lotti da riusare poggia su una classe validata al 53 %.
- **A4 e B0–B6:**
  - senza `disponibile_da` per il 37 % della capacità edificabile, ogni metodo assume che tutto sia disponibile oggi;
  - un confronto B0–B6 sensibile alla capacità può riflettere un artefatto di base, uguale per tutti i metodi: non cambia il loro ordinamento, ma cambia i livelli (quanti nuclei abitativi sono serviti);
  - le metriche sensibili alla capacità vanno riportate per scenario.
- **Precedente metodologico:** usare istanze dello stesso modello come "codificatori indipendenti" non va esteso al confronto cieco né agli agenti di B0–B6. Lì l'indipendenza richiesta dal protocollo è di informazione (non leggere gli altri), ma errori correlati dello stesso modello restano possibili (`08_critica_metodologica` D2).

## 7.10 Difetti

**Gravi** (per la regola di arresto)
- **G1. C9 non passa ed è impossibile da passare con lo strumento attuale.**
  - Prova: §7.7. Categorie N e C sovrapposte; istruzioni del cod. 2 senza la regola "le fonti secondarie non decidono"; fonti decisive sul sito escluso.
  - Conseguenza: il 37 % della capacità edificabile senza stato attuativo.
  - Correzione:
    - (a) ridefinire N come "esiste un documento identificato, con URL, non raggiungibile" e C come "ricerca documentata, con parole e fonti, senza esito";
    - (b) copiare nelle istruzioni la regola 3.3 alla lettera;
    - (c) Dennis apre i documenti di `www.comune.milano.it` da browser, oppure revoca l'esclusione per C9;
    - (d) registrare la ricerca poligono per poligono.
  - Ripetere C9 con queste correzioni, pre-registrate prima.
- **G2. Il "passa" di C5 si regge su due codifiche verosimilmente non indipendenti, a 2 successi dalla soglia.**
  - Prova: §7.3–7.4. 21 note identiche, kappa 0,945 con 0 disaccordi sulla base, nessun riferimento umano, modello e prompt non registrati.
  - Non invalida l'esito pre-registrato, ma non sostiene l'affermazione "validata da due codificatori ciechi esterni".
  - Correzione, la più piccola:
    - un controllo umano pre-registrato su un sottocampione, per esempio 40 lotti stratificati, inclusi i 6 disaccordi e i lotti con s2 = M;
    - regola fissata prima: se l'accordo persona–LLM sul binario è ≥ 0,80 [H], C5 resta;
    - in alternativa, un secondo codificatore di un'altra famiglia di modelli;
    - in ogni caso registrare modello, versione, temperatura e prompt.

**Da correggere**
- **C1. Cronologia.** Correggere REPORT §1: il commit `0490f98` segue le esecuzioni 1–4 (§7.2). Dalla v6 la pre-registrazione va committata, o pubblicata come commento sul ticket, prima del pilota.
- **C2. Registro.** Aggiungere l'esecuzione 5, la consegna delle codifiche C5 con SHA e ore, e le note dei codificatori (interruzioni, perdita di contesto, domini irraggiungibili).
- **C3. D4/GFU.** Separare "destinazione ignota" da "area di attivazione", con un attributo `destinazione_incerta` o una sottoclasse, così che A1/A2 non le contino come servizio. Passare ai successori la forbice di capacità (§7.6). Piazza d'Armi è contraddetta da una fonte ufficiale: la decisione va presa in v6.
- **C4. Deviazione testo–codice su 9 lotti da riusare** (§7.6): dichiarare che D4 vale solo per i lotti edificabili, come in v4, oppure correggere in v6 ed estendere il test.
- **C5. Lotti da riusare** (§7.5): marcarli come "non validati" nella base e nel banco, e pianificare una validazione da altra fonte.
- **C6. Cecità fisica.** Dare ai codificatori una copia con solo il pacchetto, senza `chiavi/`, `codifica_1.csv` o le cartelle delle versioni precedenti.

**Minori**
- **M1.** Il codificatore 2 del censimento ha impiegato 7 minuti per 29 poligoni [V, `orari_codifica_2.txt`]. GFU_5264 è codificato C su una scheda AT del 2012, non su un atto successivo al 2030. Mancano 4 `data_fonte`.
- **M2.** Gli intervalli per classe del §4 o del §5, se riportati, vanno dati per codificatore (n lotti), non su 2n giudizi.
- **M3.** REPORT §4: Bovisa "56,5 ha" diverge dai 64,1 ha di aree di attivazione con `ambito_id` GFU_5267 nel gpkg e dai 58,4 ha per motivo GFU. Probabilmente il §4 si riferisce all'intersezione con il poligono 2012: va precisato [I, non verificato].
- **M4.** `sensibilita_senza_gfu.json` non è stato rigenerato in questa revisione.

## 7.11 Esito proposto: **cambia**
- **Formalmente** la base non passa: C9 = falso secondo la regola pre-registrata 3.5, indipendentemente da questa revisione. Si applica la regola di arresto.
- **Ripetere** la prova identica darebbe di nuovo C9 falso: categorie sovrapposte e sito escluso. Per questo l'esito non è "ripeti".
- **Cosa cambiare:** lo strumento C9 (G1), un controllo umano minimo di C5 (G2) e il trattamento delle GFU (C3).
- **Cosa resta:** la geometria e la pipeline sono riproducibili (hash identico, tabelle identiche) e non vanno rifatte. Una v6 cambia solo questi punti, con una nuova pre-registrazione committata prima.

## 7.12 Cosa deve decidere Dennis
1. **C9.**
   - (a) Aprire lui, da browser, i documenti dei poligoni N (13–20 link, quasi tutti su `www.comune.milano.it`), oppure revocare l'esclusione del sito per il censimento;
   - (b) oppure dichiarare C9 superato per decisione, come C7. Sconsigliato: il 37 % della capacità resterebbe senza `disponibile_da`. Se lo fa, va scritto come decisione, non come misura, e B0–B6 devono trattare la disponibilità come scenario.
2. **C5.** Se codificatori LLM della stessa famiglia contano come "due codificatori esterni" (ticket #38). Se no, serve un controllo umano su circa 40 lotti, con soglia fissata prima.
3. **GFU.**
   - Se in v6 Piazza d'Armi (e Porto di Mare) passano a residenza "si" sulla base delle fonti.
   - Se le GFU senza destinazione nota devono uscire dalla classe area di attivazione.
4. **Lotti da riusare.** Se tenerli come classe piena o "da verificare" finché non arriva l'accesso civico.
5. **Altri AdP e PII** (Cascina Merlata, MIND, Rubattino…). Già aperto nel §8.

Cosa non ho verificato: le fonti online (pagine regionali, Invimit, CDP, FS, stampa); le immagini; la corrispondenza dei perimetri GFU; il punto in cui il codificatore A è stato interrotto; il modello dei codificatori [L].
