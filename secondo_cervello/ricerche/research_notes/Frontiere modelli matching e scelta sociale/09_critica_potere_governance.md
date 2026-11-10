# Critica di potere, legittimità, governance, etica e diritto del "mediatore cibernetico" (nota 09)

Note di ricerca, 2026-11-10. Ruolo: revisore critico (teoria politica, STS, diritto, teoria della pianificazione) di una commissione di dottorato. Oggetto: `tesi/DOMANDA_DI_RICERCA.md`, `tesi/DECISIONI.md`, `secondo_cervello/sintesi/RIFORMULAZIONE_PHD.md` §0–8, `secondo_cervello/ricerche/reports/Lotti ideali partecipazione e digital twin.md`, note 02–07 di questa cartella (in particolare 03, 04, 07).

**Marche.** **[V]** verificato sul testo primario in sessione; **[S]** fonte secondaria, abstract, snippet di ricerca o file interno riassuntivo; **[I]** inferenza mia; **[H]** ipotesi da testare; **[L]** lacuna: riferimento noto "a memoria" o non riaperto, da verificare sull'originale prima di citarlo. Per i file interni il percorso sostituisce l'URL e [V] significa "presente nel file", non "vero".

**Limiti della sessione.** Sei ricerche web, nessun testo normativo letto in originale (né EUR-Lex né Normattiva). Le affermazioni giuridiche sono **letture di lavoro da far verificare a un giurista**, non pareri. Arnstein, Lukes, Bachrach–Baratz, Winner, Morozov, Elster, Scholz, la giurisprudenza del Consiglio di Stato e gli articoli del GDPR sono citati **a memoria** [L]. Nessun numero di pagina è dato.

---

## 0. Giudizio in breve

1. La seconda metà della domanda ("a quali condizioni la mediazione resta trasparente e non diventa un nuovo decisore nascosto?") è la parte **più originale e più difendibile** del progetto, ma oggi è trattata come requisito di design ("criteri e pesi pubblici e riscrivibili"), non come **oggetto di misura** con una linea di base. Senza metriche di influenza del mediatore e un confronto con mediatore umano e con nessun mediatore, la tesi non può dire se il mediatore è nascosto o no [I].
2. "Pubblico e riscrivibile" non basta. Il potere sta anche (a) nella scelta di **quali opzioni** arrivano al voto (filtri di ammissibilità, catalogo, lotti candidati), (b) nella **regola** che aggrega le riscritture, (c) in chi ha **autorità giuridica** di attuare l'esito. Su (a) e (c) l'impianto è quasi muto [I].
3. Il rischio maggiore non è tecnico ma istituzionale: **senza un soggetto che si impegni prima a rispettare l'esito**, il sistema è consultazione (Arnstein, gradini intermedi [L]); e una mappa pubblica di lotti "ideali" è un'informazione che il capitale usa meglio delle famiglie (R9 della riformulazione, mai trattato oltre una riga) [I].
4. La classificazione giuridica **dipende dall'architettura**: un abbinatore di gruppi che hanno scelto sta probabilmente fuori dall'Allegato III dell'AI Act; un sistema che, per conto di un ente pubblico, valuta l'idoneità o la priorità di singole famiglie per alloggi sociali ci sta dentro [S, sotto]. La tesi può trasformare questo confine in un risultato, invece di subirlo [I].

---

## 1. Difetti più gravi (11), in ordine di gravità

Formato: **che cosa** · **perché conta** · **evidenza** · **correzione**.

### D1. Il potere di agenda è fuori dal perimetro del "riscrivibile"

- **Che cosa.** La tesi rende riscrivibili criteri, pesi e catalogo (tre livelli, `RIFORMULAZIONE_PHD.md` §4, §10) [V nel file]. Restano scritti dal progettista: l'insieme dei lotti candidati (estratti da OSM `landuse`, poi da filtri di idoneità), i filtri "prima dei pesi" (report, §"Idoneità dei lotti") [V nel file], la definizione di "pancia" e di "famiglia", il formato del voto, l'ordine dei passi (lotti → persone → gruppi → abbinamento → economia).
- **Perché.** Nella teoria del potere la "seconda faccia" è decidere che cosa non arriva mai in decisione (Bachrach e Baratz 1962; Lukes 1974, terza dimensione) [L]. Chi sceglie tra lotti già filtrati eredita il filtro: la tesi lo dice già (§8.2) [V nel file], ma non lo misura.
- **Evidenza.** In Polis il convener decide enunciati iniziali, moderazione e invitati; lo sviluppatore fissa $K\in[2,\min(5,2+\lfloor n/12\rfloor)]$ (nota 04 §1, da Gelauff 2026) [V nella nota]. Nei lavori RL "la ricompensa è la politica" (nota 07 §3) [V nella nota].
- **Correzione.** (i) Ogni filtro di ammissibilità diventa un **criterio esplicito** nel registro versionato, con autore e motivazione; (ii) misurare il **rimpianto da esclusione** (§3, metrica $E_{\text{agenda}}$); (iii) un canale con cui un partecipante può reintrodurre un lotto escluso pagando un costo di giustificazione, non un veto del sistema; (iv) distinguere nei vincoli *legali* (non negoziabili, con fonte normativa) da *scelte di progetto* travestite da vincoli tecnici [I].

### D2. Le impossibilità risalgono di un livello: manca una "costituzione" non riscrivibile nel processo

- **Che cosa.** Se i residenti possono riscrivere criteri e anche la regola di aggregazione, la scelta della regola è a sua volta una scelta sociale, con le stesse impossibilità (Arrow, Gibbard–Satterthwaite) e lo stesso rischio di manipolazione (nota 03 §5, "meta-livello") [V nella nota]. In più, con giudizi logicamente collegati (criterio rilevante → soglia rispettata → lotto ammissibile) l'aggregazione proposizione per proposizione può dare insiemi incoerenti (paradosso dottrinale, List–Pettit 2002) [L, già segnalato nella nota 03].
- **Perché.** Senza un punto fisso, chi controlla il momento in cui si cambia la regola controlla l'esito. Il mediatore IA, che "propone" la regola o ne riassume le opzioni, diventa l'arbitro di fatto [I].
- **Evidenza.** Nota 03: strategyproofness + proporzionalità sui pesi esistono solo nel formato "distribuisci 100 punti" (moving phantoms, Independent Markets, Freeman et al. 2021) [V abstract nella nota]; MES dà proporzionalità ma non strategyproofness [L nella nota]. Habermas Machine: cambiare Schulze con Borda cambia spesso il vincitore [S nella nota 04].
- **Correzione.** Costituzione minima a tre livelli con regola di emendamento **esterna** al processo (§2). È la versione operativa del precommitment (Elster, *Ulysses and the Sirens*) [L] e del principio 3 di Ostrom (chi è toccato dalle regole partecipa a cambiarle) dentro un livello superiore annidato (principio 8) [S: elenco da fonti secondarie; numerazione da verificare su Ostrom 1990].

### D3. Il mediatore LLM è un persuasore efficace, e la tesi non ha un controllo

- **Che cosa.** L'LLM è previsto per "teach-back e sintesi, auditato" (report, passo 6) [V nel file], ma ogni sintesi è un aggregatore implicito (nota 03 §4, Conitzer et al.: il RLHF aggrega in modo "intransparent", vicino al Borda) [V nella nota].
- **Perché.** Il rischio non è la propaganda, ma lo spostamento silenzioso delle preferenze dichiarate prima che vengano aggregate: la regola resta pubblica, gli input sono già stati cambiati [I].
- **Evidenza.** Salvi et al. 2025: con personalizzazione GPT-4 dà +81,7% di odds di accordo con l'avversario [S nella nota 04]. Hackenburg et al. 2025 (*Science*): dove cresce la persuasività cala l'accuratezza [S nella nota 04]. Benchmark su 18 LLM: sotto-rappresentazione delle minoranze nei riassunti e dipendenza dall'ordine dell'input [S nella nota 04]. La Habermas Machine, al contrario, dopo la critica *sovra-pesa* le minoranze [S]: il mediatore sposta il peso in qualunque direzione, quindi è un decisore (nota 04 §3) [I nella nota].
- **Correzione.** Disegno a tre bracci (LLM, facilitatore umano, nessuna sintesi) già proposto in nota 04 §4 [V nella nota], più le metriche di §3 qui sotto con soglie preregistrate. Regola costituzionale: l'LLM non produce mai testi che siano *input* del voto senza che l'autore umano li approvi riga per riga; i testi del mediatore sono marcati come tali [H].

### D4. L'apprendimento (RL, aggiornamento dei pesi) è un decisore che deriva nel tempo

- **Che cosa.** La domanda nomina "apprendimento per rinforzo" come parte del mediatore [V: `DOMANDA_DI_RICERCA.md`]. La riformulazione ammette i pesi appresi "solo come proposta" (F1d) [V nel file], ma non dice chi scrive la ricompensa dell'RL, né come si impedisce che la proposta di default diventi la decisione (effetto di default, status quo bias [L]).
- **Perché.** Una ricompensa scritta dagli autori è la politica (Zheng et al. 2023: "batte gli esperti" sulle metriche che ottimizza) [S nella nota 07]. L'AI Economist mostra *tax gaming*: gli agenti sfruttano qualsiasi ricompensa [V abstract nella nota 07]. Famiglie o loro agenti LLM faranno lo stesso con le dichiarazioni (Goodhart) [I].
- **Correzione.** (i) La ricompensa è un file pubblico versionato del livello 1 della costituzione (§2), non un iperparametro; (ii) l'RL resta in simulazione (nota 07 §4, ordine prudente) [V nella nota]; (iii) ogni proposta di aggiornamento dei pesi va mostrata con il **controfattuale** ("con i pesi attuali vincerebbe X, con quelli proposti Y") e richiede ratifica attiva, mai silenzio-assenso; (iv) misurare il tasso di accettazione delle proposte del sistema contro un placebo (proposta casuale di pari entità): se si accetta tutto, il sistema decide [H].

### D5. Tokenismo strutturale: nessuno si impegna prima a rispettare l'esito

- **Che cosa.** "Scelta del partner: rinviata a quando il sistema funziona" (`DECISIONI.md`) [V nel file]. Il report riconosce che senza impegno istituzionale preventivo "anche il miglior meccanismo resta consultazione" [V nel file].
- **Perché.** In Italia le decisioni sull'uso del suolo stanno nel PGT approvato dal consiglio comunale (L.R. Lombardia 12/2005) e la partecipazione formale è per osservazioni [L, da verificare]; l'assegnazione di alloggi ERP/ERS segue bandi e graduatorie dell'ente [L]. Il sistema non ha alcuna autorità propria: i suoi esiti sono raccomandazioni. Cardullo e Kitchin trovano iniziative "citizen-centric" fondate su paternalismo civico e cittadinanza da consumatore [S nel report]. HouseMaker/VillageMaker è "scelta del consumatore, non governance" [S nella riformulazione §8.4].
- **Evidenza storica.** Cybersyn: secondo recensioni del libro di Medina (2011), la partecipazione operaia dovette essere conciliata con sindacati e con gli schemi degli "interventores", e il disegno rifletteva una visione ristretta di chi avrebbe tenuto potere decisionale [S, recensioni; testo non letto]. Lezione per la tesi: un sistema cibernetico eredita la struttura di potere del committente [I].
- **Correzione.** Rendere il partner istituzionale una **variabile del disegno**, non un dettaglio rinviato: dichiarare per ogni esperimento il gradino di potere effettivo (Arnstein [L]; o il "democracy cube" di Fung [L]) e, per la "grande prova", cercare un atto che leghi l'ente prima del voto (bando di una cooperativa, convenzione urbanistica, accordo ex art. 11 L. 241/1990 [L, da verificare con un amministrativista]). Se non c'è, dichiarare la prova come **consultiva** e non trarne conclusioni sulla democratizzazione [I].

### D6. Esclusione digitale e auto-selezione: la "pancia" non è chi partecipa

- **Che cosa.** La popolazione-obiettivo è definita dal reddito ("pancia della curva"); la popolazione che partecipa sarà definita da competenze digitali, tempo libero, lingua, fiducia nelle istituzioni [I].
- **Perché.** Chi non lascia tracce non c'è (R3 della riformulazione) [V nel file]; i pesi appresi da un campione auto-selezionato sono la H7 [V nel file]. Gli LLM che simulano famiglie falliscono proprio sulla varianza e sui gruppi meno rappresentati (nota 05) [S nella nota], quindi la fase "prima agenti" rischia di calibrare il sistema sulle famiglie medie e poi di misurarle [I].
- **Correzione.** (i) Panel sorteggiato con quote e probabilità esplicite (LEXIMIN o Goldilocks, nota 03 §3) [V/S nella nota] accanto al canale aperto; (ii) canale assistito non digitale (sportello, facilitatore umano che inserisce per conto, con log); (iii) compenso per il tempo (R5) [V nel file]; (iv) metrica di rappresentatività per strato (§3, $\rho_s$) con soglia minima che blocca la ratifica se violata [H].

### D7. Appropriazione da parte del capitale e delle piattaforme

- **Che cosa.** R9 ("una mappa dei lotti serve prima a chi ha capitale") ha come mitigazione "licenza aperta e commons by design" [V nel file]. Ma una licenza aperta *favorisce* chi ha capitale per usare l'informazione: rivelare dove la domanda delle famiglie si concentra è un segnale di rendita (rent gap) [I].
- **Perché.** Sadowski descrive l'urbanizzazione del capitale tecnologico in fasi che prendono controllo di supervisione del governo, gestione dei servizi e proprietà dello spazio [S, abstract *Urban Studies* 2021]. Una piattaforma di matching che funziona diventa un'infrastruttura appetibile per un operatore privato o per un fondo che la "white-label" (platform urbanism) [I]. Morozov sul "soluzionismo" [L].
- **Correzione.** (i) Pubblicazione **differita e aggregata** delle preferenze geolocalizzate (pubblici i criteri, non le mappe di domanda per lotto fino all'impegno sul terreno); (ii) aggancio della governance al **regime del suolo**: il sistema produce valore per le famiglie solo se il lotto passa in diritto di superficie, CLT o proprietà indivisa (nota 06, report §"catena terreno–vincolo–canone") [V nel file]; (iii) proprietà del software e dei dati in capo a un soggetto senza scopo di lucro con le famiglie nella governance (cooperativismo di piattaforma, Scholz [L]); (iv) metrica di cattura (§3, $K_{\text{dev}}$) [H].

### D8. Classificazione giuridica non risolta (AI Act, GDPR, diritto amministrativo italiano)

- **AI Act, Allegato III, punto 5(a).** Copre i sistemi usati da o per conto di autorità pubbliche per valutare l'idoneità a prestazioni e servizi di assistenza pubblica essenziali, e per concederli, ridurli, revocarli o recuperarli [S: sintesi McCann FitzGerald e AI Act Service Desk]. Il Service Desk della Commissione dà come esempio *in scope* un sistema che attribuisce punteggi ai richiedenti di alloggi sociali, e come *fuori ambito* uno strumento che abbina persone ai servizi di supporto più adatti ai loro bisogni senza valutare domande [S: [Service Desk](https://ai-act-service-desk.ec.europa.eu/en/essential-services)]. Un chatbot le cui risposte influenzano materialmente la decisione dell'operatore è *in scope* [S, idem]. **Conseguenza [I]:** il confine passa tra "abbinare chi ha scelto" (probabilmente fuori) e "dire chi ha titolo o priorità" (dentro). Il mediatore che *filtra* le famiglie per la "pancia" o ordina famiglie per un lotto scarso scivola verso il punto 5(a) se c'è un ente pubblico dietro.
- **Altri punti da verificare [L].** Allegato III 5(b) (merito creditizio di persone fisiche) se il modello economico valuta la solvibilità delle famiglie per quote cooperative o mutui; art. 5 (pratiche vietate: tecniche manipolative, social scoring) per un mediatore persuasivo che usa profili; art. 50 (obbligo di dichiarare l'interazione con un sistema di IA); esenzione per ricerca scientifica (art. 2), che copre la fase simulata ma non un uso con un ente.
- **Tempi.** Il Digital Omnibus sull'IA (Reg. (UE) 2026/1744) risulta pubblicato in GU il 24/07/2026 e sposta gli obblighi dell'Allegato III al 2/12/2027 [S: più studi legali concordi; GU non letta]. La "grande prova" della tesi cadrebbe a ridosso o dopo quella data: va progettata già conforme [I]. Questo aggiorna la riga "pubblicazione in Gazzetta non verificata" del report (da verificare su EUR-Lex prima di chiudere l'avviso).
- **GDPR [L, articoli a memoria].** Art. 22 (decisioni basate unicamente su trattamento automatizzato, compresa la profilazione, con effetti significativi): la ratifica umana deve essere effettiva, non una firma. Art. 9: gli attributi di diversità (età va bene; disabilità, salute, origine, orientamento no) sono categorie particolari; usarli per comporre gruppi richiede base giuridica esplicita. Art. 35: valutazione d'impatto (DPIA) quasi certamente necessaria. Trasferimenti extra-UE se l'LLM è servito da un fornitore statunitense.
- **Diritto italiano.** L. 132/2025, art. 14: nella PA l'IA è supporto strumentale all'attività provvedimentale, nel rispetto dell'autonomia e del potere decisionale della persona responsabile [S: Sole 24 Ore NT+, Agenda Digitale]; un commento a una sentenza del TAR Marche richiede controllo effettivo sulla decisione finale [S: diritto.it]. Giurisprudenza del Consiglio di Stato del 2019 sull'algoritmo nel procedimento (conoscibilità, non esclusività, non discriminazione) [L, sentenze da identificare].
- **Correzione.** Un capitolo di metodo, non di diritto: una **matrice architettura × norma** che dice, per ogni configurazione (simulata; cooperativa privata; ente pubblico), quali obblighi scattano. Farla validare da un giurista (lacuna di competenza già dichiarata [L]) [H].

### D9. Il confine della "pancia" è un atto di gatekeeping

- **Che cosa.** Chi rientra nella "pancia" (reddito, composizione familiare, residenza) è il primo principio di Ostrom (confini chiari) [S] ma anche il punto più politico: è l'idoneità, cioè proprio l'oggetto del punto 5(a) se c'è un ente pubblico [I].
- **Perché.** La categoria è attribuita a Sanchez ma "non trovata nei testi accessibili" (report, tabella verifiche) [V nel file]: oggi è una metafora senza definizione operativa, e una metafora non è contestabile [I].
- **Correzione.** Definire la soglia con fonte (es. ISEE o reddito equivalente rispetto alla mediana metropolitana, da ISTAT) [L], dichiararla livello 0 o 1 della costituzione, misurare quante famiglie stanno appena fuori e che cosa perdono (sensibilità alla soglia) [H].

### D10. La diversità imposta dal progettista è paternalismo con buone intenzioni

- **Che cosa.** "I gruppi non devono essere omogenei" è una decisione di Dennis (`DECISIONI.md`) [V nel file], non dei gruppi.
- **Perché.** Il caso empirico più vicino, Singapore, è diversità imposta dall'alto con quote etniche (nota 02 §2) [V nella nota]. Con tre o più tipi la stabilità individuale può non esistere e deciderla è NP-completo (nota 07 §1) [V nella nota]: il sistema dovrà forzare gruppi che qualcuno vorrebbe lasciare. Gli attributi auto-dichiarati sono un canale di manipolazione (LEXIMIN, nota 03 §3) [V nella nota].
- **Correzione.** La diversità come **parametro votato** con il suo prezzo mostrato (price of diversity, nota 02) [V nella nota]; soft bounds o riserve invece di quote rigide; diritto di uscita garantito a livello 0 (Hirschman, *exit/voice* [L]) [I].

### D11. Responsabilità diffusa: nessuno risponde dell'esito

- **Che cosa.** Il designer di sistemi è "controllo del controllo" (Pask, riformulazione §10) [V nel file], le famiglie scelgono, l'LLM sintetizza, l'ente (se c'è) firma. Se un gruppo si forma male o un lotto si rivela inedificabile, chi ne risponde?
- **Perché.** È il "problema delle molte mani" [L] e, nel diritto italiano, l'imputabilità del provvedimento al funzionario anche quando l'IA ha inciso (L. 132/2025) [S]. Una ratifica umana "di firma" lascia la responsabilità formale e il potere reale in luoghi diversi [I].
- **Correzione.** Ogni decisione ha un **titolare nominato** nel registro (§2), una via di ricorso a costo basso (principio 6 di Ostrom [S]) e una spiegazione controfattuale leggibile [H].

### D12 (metodologico). Le prove con agenti simulati possono chiudere il disegno prima che arrivino le persone

- **Che cosa.** "Prima agenti, poi test reale" [V: `DECISIONI.md`]. Gli agenti LLM riproducono medie, non varianze né minoranze (nota 05) [S].
- **Perché.** Un sistema ottimizzato per mesi su agenti sintetici arriva alla "grande prova" con criteri, soglie e regole già stabilizzati: le persone reali diventano un test di accettazione, non co-autrici. È la critica di Carpo della "svolta partecipativa che non c'è stata" [S nel report] riprodotta nel metodo [I].
- **Correzione.** Una prova umana **piccola e precoce** (una sessione con 10–15 persone reali sul catalogo dei criteri) prima di fissare le regole; dichiarare nel registro quali parametri sono stati calibrati su agenti e renderli rivedibili al primo contatto umano [H].

---

## 2. Proposta: "costituzione minima" del sistema

Principio guida [I]: **il mediatore non può mai scrivere, né proporre in silenzio, una regola del livello in cui opera.** Le regole sono scritte da attori umani nominati, ogni modifica lascia una traccia verificabile, e chi è toccato dalle regole ha un canale per cambiarle a un livello superiore (Ostrom, principi 3 e 8 [S]).

### 2.1 Tre livelli di regole

| Livello | Contenuto | Chi può modificarlo | Come | Mai modificabile da |
|---|---|---|---|---|
| **0. Carta** (fissa nel ciclo) | diritti (uscita, accesso ai propri dati, ricorso, spiegazione); il mediatore non decide; ratifica umana attiva; formato del voto sui pesi (bilancio a 100 punti); insieme ammesso di regole di aggregazione con gli assiomi garantiti; soglie minime di qualità tecnica e vincoli legali con fonte; obbligo di registro; metriche di §3 e loro soglie di blocco | solo fuori dal processo: ente garante + assemblea sorteggiata, maggioranza qualificata (es. 2/3), periodo di raffreddamento, effetto solo dal ciclo successivo | emendamento motivato, pubblicato prima, con analisi d'impatto su casi simulati | mediatore, progettista da solo, partecipanti dentro il ciclo |
| **1. Regole** (riscrivibili tra un ciclo e l'altro) | catalogo dei criteri; filtri di ammissibilità non legali; soglie di diversità (soft bounds/riserve); scelta della regola di aggregazione *dentro* l'insieme ammesso; ricompensa dell'RL; soglia della "pancia" se non fissata dall'ente | assemblea dei partecipanti con panel sorteggiato; maggioranza qualificata; le minoranze coese ottengono garanzia proporzionale (Independent Markets sui pesi, nota 03) | proposta → controfattuale mostrato → voto → entrata in vigore al ciclo seguente | mediatore (può solo segnalare incoerenze, es. paradosso dottrinale) |
| **2. Preferenze** (riscrivibili sempre) | pesi individuali, scelte di lotti, scelte di gruppo, motivazioni | ogni partecipante, per sé | interfaccia diretta; i testi suggeriti dall'LLM sono marcati e richiedono approvazione | nessun altro |

Per evitare il regresso (chi decide le regole per cambiare il livello 0?) la tesi deve **dichiarare** che il livello 0 non è legittimato dal processo ma da un atto esterno (ente, statuto della cooperativa, approvazione etica) e lo deve sottoporre a critica esplicita. È una scelta, non una soluzione: il regresso si ferma per convenzione dichiarata, come la "regola di riconoscimento" in Hart [L] [I].

### 2.2 Traccia di audit

- **Registro append-only con hash concatenati** (ogni voce contiene l'hash della precedente; un repository git firmato basta per la tesi): versione di catalogo, pesi aggregati, regola, ricompensa, prompt di sistema e modello dell'LLM (nome, versione, temperatura), seme casuale, input, output, chi ha ratificato [H].
- **Model card del mediatore** pubblicata a ogni ciclo: funzione obiettivo, vincoli, iperparametri "politici" (nella nota 04: $\lambda$, soglie, $K$, metodo di voto) [V nella nota], assiomi garantiti e violati.
- **Riproducibilità come requisito di livello 0**: dagli input pubblici e dal seme si deve ricalcolare l'esito. Polis mostra che oggi spesso non si può (K ricalcolato coincide in 70 conversazioni su 112) [V nella nota 04].
- **Revisore indipendente** (non il progettista) che riesegue a campione e firma.

### 2.3 Metriche per rilevare un decisore nascosto

Notazione. $N$ partecipanti, preferenze dichiarate prima della mediazione $p_i^{0}$, dopo $p_i^{1}$. Regola costituzionale dichiarata $R$ (livello 0/1). Bracci: $A$ (mediatore IA), $H$ (facilitatore umano), $\varnothing$ (nessuna sintesi: voto diretto con $R$). Esito $o^{a}$ nel braccio $a$; $d(\cdot,\cdot)$ distanza sugli esiti (es. $1-$Jaccard sui lotti assegnati, o distanza di Kendall sulle graduatorie). Tutte le metriche sono **proposte mie** [H], costruite sulle fonti della nota 04; nessuna è uno standard.

**M1. Influenza eccedente sull'esito.** Quanto l'esito si allontana da ciò che la regola dichiarata darebbe sulle preferenze iniziali, rispetto al mediatore umano:
$$\Delta_{A} \;=\; \mathbb{E}\big[d\big(o^{A},\,R(p^{0})\big)\big]\;-\;\mathbb{E}\big[d\big(o^{H},\,R(p^{0})\big)\big].$$
$\Delta_A>\delta$ (soglia preregistrata) segnala che il mediatore IA sposta gli esiti più di un umano. Il confronto con $\varnothing$ ($\mathbb{E}[d(o^{\varnothing},R(p^0))]$, che misura la sola deliberazione tra pari) separa l'effetto "deliberazione" dall'effetto "mediatore".

**M2. Deriva direzionale verso il mediatore.** Sia $m$ la posizione che il mediatore assume se interrogato da solo (es. pesi che propone senza input). Quota dello spostamento delle preferenze allineata a $m$:
$$\alpha_{a} \;=\; \frac{1}{N}\sum_{i}\frac{\langle p_i^{1}-p_i^{0},\; m-p_i^{0}\rangle}{\lVert m-p_i^{0}\rVert^{2}},\qquad \text{test: } \alpha_{A}-\alpha_{H}>0 .$$
Variante con $m$ = posizione maggioritaria iniziale per misurare la deriva verso la maggioranza (nota 04 §3, metrica 1) [V nella nota].

**M3. Potere di voto del mediatore (indice alla Banzhaf).** Trattare ogni iperparametro politico $\theta$ (prompt, ordine dell'input, regola tra quelle ammesse, $K$, soglie) come un "votante". Su perturbazioni ammissibili $\theta'\sim\Theta$:
$$\beta_{M} = \Pr_{\theta'\sim\Theta}\big[o(\theta')\neq o(\theta)\big],\qquad \beta_{i}=\Pr\big[o(p_{-i},\,p_i')\neq o(p)\big],$$
con $p_i'$ estratto dalla distribuzione delle preferenze altrui. Il mediatore è un **decisore nascosto** se $\beta_M>\max_i\beta_i$, cioè se un cambio "tecnico" pesa più del voto di qualunque partecipante [H].

**M4. Potere di agenda (rimpianto da esclusione).** $F$ insieme dei lotti fattibili per legge; $S\subseteq F$ quelli mostrati. Per ciascuno, il miglior lotto escluso rispetto a quello assegnato:
$$E_{\text{agenda}}=\frac{1}{N}\sum_i \mathbf 1\Big[\max_{\ell\in F\setminus S}u_i(\ell)>u_i\big(o_i\big)\Big],$$
stimato su un campione di lotti esclusi mostrati a posteriori. Valori alti: il filtro decide.

**M5. Copertura proporzionale delle minoranze nella sintesi.** Per un cluster $g$ di dimensione $n_g$ e quota $s_g$ dei suoi argomenti nella sintesi finale:
$$c_g = \frac{s_g}{n_g/N},\qquad \text{blocco se } \min_g c_g<\underline c .$$

**M6. Rappresentatività per strato.** Per lo strato $s$ (reddito, età, competenza digitale, cittadinanza):
$$\rho_s=\frac{n_s/n}{N_s/N_{\text{pop}}},$$
con $N_s$ dalla popolazione-obiettivo (ISTAT, se il dato esiste alla scala utile [L]). La ratifica di livello 1 è bloccata se $\min_s\rho_s<\underline\rho$.

**M7. Accettazione delle proposte contro placebo.** $a_{\text{sys}}$ quota di proposte del sistema accettate, $a_{\text{plac}}$ quota di proposte casuali di pari entità accettate. Se $a_{\text{sys}}\approx a_{\text{plac}}\approx 1$, la ratifica è formale (effetto default) e il sistema decide [H].

**M8. Cattura da parte del capitale.** Per ogni lotto scelto, $V^{\text{dev}}_\ell$ valore residuo nel regime developer e $V^{\text{coop}}_\ell$ nel regime cooperativo/CLT (DCF della nota 06 e del report) [V nel file]. Indice:
$$K_{\text{dev}}=\operatorname{corr}\big(\mathbf 1[\ell\text{ scelto}],\,V^{\text{dev}}_\ell\big)-\operatorname{corr}\big(\mathbf 1[\ell\text{ scelto}],\,V^{\text{coop}}_\ell\big).$$
$K_{\text{dev}}>0$ dice che il sistema sceglie i lotti che rendono di più a un developer: il mediatore sta lavorando per il mercato. Più una misura *ex post*: quanti lotti segnalati sono stati acquistati da operatori privati entro $T$ mesi dalla pubblicazione [H].

**M9. Riproducibilità.** $\mathrm{Rep}=1$ se l'esito si ricalcola esattamente dal registro pubblico, $0$ altrimenti. Livello 0: $\mathrm{Rep}=1$ obbligatorio.

Tutte le soglie ($\delta,\underline c,\underline\rho$) vanno preregistrate prima delle prove, coerentemente con `RIFORMULAZIONE_PHD.md` §5 [V nel file]. Unità di analisi: il gruppo, non l'individuo; serve un calcolo di potenza su ICC che oggi manca (nota 04 §4) [L].

---

## 3. Cinque opportunità di contributo originale, in ordine

1. **Una misura dell'influenza del mediatore (M1–M4) con disegno a tre bracci, applicata a una decisione spaziale con esiti materiali.** La nota 04 non trova metriche standard per il decisore nascosto né studi su esiti materiali (allocazioni, costi) della mediazione IA [V nella nota]; il report non trova mediazione IA in urbanistica o housing [V nel file]. È il contributo più netto, pubblicabile anche fuori dall'architettura (FAccT, CSCW, *Environment and Planning B*) e già annunciato dalla seconda metà della domanda [I]. Rischio: serve un campione di gruppi umani adeguato.
2. **Costituzione a livelli per le assunzioni del modello, con emendamento esterno e registro verificabile.** I quadri sui twin regolano i dati, non le assunzioni (report) [V nel file]; la nota 03 indica il meta-livello come problema aperto [V nella nota]. Tradurre Ostrom (principi 3, 4, 6, 8 [S]) in regole computabili per un "commons di criteri" è originale nella forma, se non nel principio [I/H]. Verifica di novità da fare (letteratura su *algorithmic governance*, *data trusts*, *constitutional AI* collettiva).
3. **Matrice architettura × norma (AI Act, GDPR, L. 132/2025, PGT/ERS) come strumento di progetto.** Mostrare che scelte di architettura (abbinare chi sceglie vs ordinare chi ha titolo; ente pubblico vs cooperativa) spostano il sistema dentro o fuori l'Allegato III, e che il mediatore "sotto soglia" può essere più democratico o solo meno controllato. Contributo utile a pianificatori e comuni; richiede un coautore giurista [I].
4. **Governance anti-cattura legata al regime del suolo, misurata ($K_{\text{dev}}$).** Unisce la critica della platform urbanism [S] al confronto DCF developer/cooperativa già previsto (report, terzo contributo) [V nel file]: non "piattaforma aperta = commons", ma "valore del matching trattenuto dalle famiglie solo se il suolo è vincolato". Originalità [H], da verificare sulla letteratura CLT e platform cooperativism.
5. **Rilettura di Cybersyn come caso di studio di governance, non di estetica.** La tesi cita Beer e Medina come ispirazione [V: `DECISIONI.md`]; una lettura critica (chi aveva voce, chi scriveva i modelli, come la struttura del committente entrava nel sistema [S, recensioni]) darebbe al progetto una genealogia onesta e una lezione verificabile. Contributo storico-critico minore ma a basso costo; richiede la lettura del libro di Medina [L].

---

## 4. Cosa fare subito (proposte per Dennis, non decisioni)

- Aggiungere alla domanda di ricerca una sottodomanda misurabile sulla seconda metà: "di quanto il mediatore IA sposta gli esiti rispetto a un facilitatore umano e a nessun mediatore, su una regola dichiarata?" (M1) [H].
- Fissare per iscritto il livello 0 prima di ogni prova con agenti, e registrare quali parametri sono calibrati su agenti.
- Chiedere a un giurista la verifica di D8 prima della scelta del partner.
- Leggere in originale: Arnstein 1969; Ostrom 1990 (cap. sui principi); Medina 2011; Cardullo e Kitchin; Sadowski 2021; testo consolidato AI Act Allegato III e Reg. (UE) 2026/1744 su EUR-Lex; L. 132/2025 art. 14 su Normattiva.

## 5. Gaps di questa nota

- Nessun testo normativo letto in originale; numeri di articolo GDPR e AI Act diversi da Allegato III 5(a) sono a memoria [L].
- Giurisprudenza amministrativa italiana sugli algoritmi non identificata [L].
- Numerazione e formulazione dei principi di Ostrom solo da fonti secondarie [S].
- Le "cinque lezioni" di Medina su Jacobin non lette [L].
- Nessuna ricerca su letteratura di *algorithmic auditing* (es. audit esterni, *contestability by design*) che potrebbe già contenere metriche simili a M3–M4: da fare prima di rivendicare novità [L].

## Fonti consultate in questa sessione (web)

- AI Act Service Desk, essential services: https://ai-act-service-desk.ec.europa.eu/en/essential-services [S]
- McCann FitzGerald, draft guidelines high-risk classification: https://www.mccannfitzgerald.com/knowledge/technology-and-innovation/essential-services-spotlight-eu-ai-act-draft-guidelines-on-high-risk-ai-classification [S]
- Digital Omnibus on AI (Reg. (UE) 2026/1744): https://www.mondaq.com/uk/new-technology/1825722/eu-digital-omnibus-on-ai-enters-into-force ; https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines/ ; https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/ [S]
- L. 132/2025 art. 14: https://ntplusdiritto.ilsole24ore.com/art/responsabilita-senza-potere-pa-firma-funzionario-non-basta-provare-controllo-umano-sull-ia-AJD0HcWB ; https://www.agendadigitale.eu/cittadinanza-digitale/pubblica-amministrazione-e-ai-le-parole-chiave-della-legge-italiana/ ; https://www.diritto.it/ai-decisioni-pubbliche-limiti-responsabilita-umana/ [S]
- Medina, *Cybernetic Revolutionaries* (recensioni): https://muse.jhu.edu/article/522475/pdf ; https://wiki.p2pfoundation.net/Cybernetic_Revolutionaries [S]
- Ostrom, principi (secondarie): https://wiki.p2pfoundation.net/Elinor_Ostrom’s_Eight_Commons_Governance_Design_Principles [S]
- Sadowski, "Who owns the future city?", *Urban Studies* 58(8), 2021: https://ideas.repec.org/a/sae/urbstu/v58y2021i8p1732-1744.html [S]
