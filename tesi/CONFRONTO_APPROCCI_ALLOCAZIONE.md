# Come si assegnano persone e lotti: confronto critico degli approcci

Stato: decisione presa il 2026-11-10 (vedi `tesi/DECISIONI.md`), con il protocollo per verificarla empiricamente.
Marche: **[V]** verificato su testo, abstract o record; **[S]** fonte secondaria o snippet; **[I]** inferenza; **[H]** ipotesi da verificare. Le fonti sono quelle delle note in `secondo_cervello/ricerche/research_notes/` (cartelle *Lotti ideali…* e *Frontiere…*): quasi tutte lette solo come abstract, da verificare sul testo prima di citarle in tesi.

---

## 1. La domanda

Dati i lotti candidati di Milano e le famiglie della "pancia", **chi decide quale famiglia va su quale lotto, e con chi abiterà?** Ogni approccio risponde in modo diverso, e la risposta stabilisce dove sta il potere: in alto (piano, developer, algoritmo) o in basso (le famiglie).

## 2. La decisione presa

**Individui → lotti → comunità sul lotto**, al posto di "individui → gruppi → lotti" (9/11).

1. Ogni famiglia descrive le sue esigenze con un **vettore dei desideri**:
   - **ancore**: luoghi di lavoro, scuola e cura;
   - **pesi sui criteri** del lotto;
   - **budget** e composizione della famiglia.
2. Il sistema calcola per ogni lotto un'utilità **spiegabile** [I, forma proposta]:
$$u_{i\ell}=\sum_j w_{ij}\,\tilde x_{\ell j}\;-\;\alpha_i\sum_{a\in A_i}t(a,\ell)\;-\;\lambda_i\max\big(0,\,c_{i\ell}-B_i\big)$$
   e **propone** i K lotti migliori, mostrando il contributo di ogni voce e che cosa cambierebbe la proposta (*teach-back*).
3. **La famiglia sceglie** e ordina i lotti. L'assegnazione la fa l'**accettazione differita con le famiglie che propongono**, con **riserve di capacità** per categoria su ogni lotto (anziani, famiglie con figli, persone sole…).
4. **Il feedback** (accetto, rifiuto, perché) aggiorna solo **i pesi di quella famiglia**:
$$P(\ell\succ\ell'\mid w_i)=\sigma\big(\beta\,w_i\cdot(x_\ell-x_{\ell'})\big).$$
   Le regole comuni (criteri, riserve, formula del costo) cambiano solo per decisione collettiva tra un ciclo e l'altro.
5. **Nessun veto di ingresso.** Chi abita insieme dipende dal lotto scelto. Dopo l'assegnazione c'è una fase di conoscenza; chi vuole lascia senza penalità e rientra nel ciclo successivo.

**Il punto originale [I].** La diversità non è imposta tra persone e non dipende dal consenso degli altri. Nasce in due modi:
- **(a)** famiglie diverse condividono le stesse **esigenze di luogo** (il raggruppamento è per ancore, non per somiglianza personale);
- **(b)** le **riserve di capacità** garantiscono un mix minimo su ogni lotto.

## 3. Gli approcci esistenti, a confronto

| # | Approccio | Dove si usa o è proposto | Chi decide | Pro | Contro |
|---|---|---|---|---|---|
| A | **Mercato / developer** | prassi attuale | prezzo e developer | nessun costo di coordinamento; molta offerta dove conviene | esclude la "pancia" per reddito; segrega per prezzo; la rendita va al developer [I] |
| B | **Graduatoria amministrativa** (ERP, punteggi, liste d'attesa) | case popolari in Italia | ente, con punteggio | trasparente sul punteggio; tutela chi ha più bisogno | toglie la scelta: secondo Waldinger 2021 (AER) costa oltre il 30% del benessere degli inquilini [S]; accettazione di alloggi marginali per non perdere il posto (Arnosti & Shi 2020, Management Science) [V record]; sotto l'AI Act un punteggio sui richiedenti può essere "ad alto rischio" [S] |
| C | **Classifica dei lotti con analisi multicriterio** (GIS-MCDA, AHP, SMAA) | letteratura sulla localizzazione; Spatial Milano Lab | chi scrive criteri e pesi | consolidata; con SMAA mostra la robustezza ai pesi [V: Lab] | dice dove costruire, non chi va dove; i filtri iniziali decidono l'esito (caso londinese nelle note 03) [S]; nessuna scelta delle famiglie |
| D | **Ottimizzazione dall'alto** (programma lineare intero, portafogli) | Spatial Milano Lab (MILP con CVaR) | il pianificatore, tramite la funzione obiettivo | massimizza un obiettivo dichiarato; gestisce budget e vincoli | è top down per definizione; nel Lab molti portafogli equivalenti e vincolo Gini non vincolante [V: riesame 06]; nessuna garanzia che le famiglie preferiscano l'esito |
| E | **Raggruppamento per somiglianza** | Housing Prime, Bartlett RC11 2020 [V] | l'algoritmo (cluster per esigenze uguali) | gruppi coerenti, convivenza più facile a breve | produce gruppi omogenei: il "ghetto di interessi" escluso dalla decisione del 9/11 [I] |
| F | **Gruppi con consenso all'ingresso** (giochi edonici, stabilità individuale) | teoria (Boehmer & Elkind 2020; Bredereck et al. 2019) [V] | ogni membro, con un veto | rispetta l'autonomia del gruppo; stabile con due tipi di famiglia [V] | il veto permette di escludere i diversi; con tre o più tipi una partizione stabile può non esistere [V]; rischio di discriminazione e di dati sensibili (GDPR) [S]; scartato il 10/11 |
| G | **Diversità imposta** (fair clustering, quote rigide) | Chierichetti et al. 2017 [V abstract]; quote etniche per blocco a Singapore (Benabbou et al. 2020) [S] | il progettista, con le soglie | garantisce il mix | paternalismo; le quote rigide danneggiano le minoranze più delle riserve (Hafalir et al. 2013) [S]; con vincoli duri l'assegnazione equa può non esistere (Ehlers et al. 2014) [S] |
| H | **Workshop partecipativo con modello interattivo** | Finding Places, MIT City Science, Amburgo 2016 [V] | cittadini propongono, amministrazione decide | coinvolgimento reale, strumento tangibile | 161 siti proposti, 6 raccomandati, circa il 4% dell'obiettivo [V]; pesi del prefiltro non pubblicati; decisione finale fuori dal processo [V] |
| I | **Lotteria** (unica o per alloggio) | bandi di edilizia convenzionata; NYC Housing Connect [S] | il caso | equità ex ante, semplice | ignora le preferenze; con lotterie separate per alloggio peggiora la corrispondenza tra famiglie e alloggi (Arnosti & Shi 2020) [V record] |
| J | **Matching con scelta e riserve** (accettazione differita) | scuole (Boston, NYC), riserve in India (Sönmez & Yenmez 2022) [S], rifugiati (Bansak et al. 2018; Ahani et al. 2021) [V] | le famiglie, con regole pubbliche | per chi propone, dire la verità conviene sempre; con le riserve protegge le categorie senza quote rigide; prove empiriche solide in altri campi | non ottimizza il benessere totale; non era mai stata applicata a lotti da costruire e comunità abitative [I: nessun lavoro trovato] |
| **K** | **Proposta della tesi**: raccomandazione spiegabile + J + feedback personale | — | le famiglie scelgono; regole comuni scritte collettivamente | unisce la scelta (J) a una proposta personalizzata e motivata; diversità tramite ancore e riserve, senza veto; la macchina impara senza diventare decisore | dipende dalla qualità del vettore dei desideri; la spiegazione può persuadere (la proposta orienta la scelta); la convivenza non è scelta a priori; le riserve sono comunque scritte da qualcuno |

### Perché K e non le alternative più vicine

- **Rispetto a J da solo**: J assume che le famiglie sappiano già ordinare 2.291 lotti, cosa impossibile. La raccomandazione spiegabile restringe la scelta a K lotti motivati, e il feedback corregge la proposta senza togliere la scelta [I].
- **Rispetto a F**: il veto è il punto debole sia etico sia matematico (esclusione; nessuna stabilità garantita con molti tipi). K sposta la diversità dalle persone alla capacità del lotto [I].
- **Rispetto a E**: si raggruppa per **luoghi** di cui c'è bisogno, non per somiglianza personale. È l'ipotesi da verificare (H-K2 sotto).
- **Rispetto a D**: l'ottimizzazione resta come **linea di base** di confronto, non come decisore.

### Rischi di K da tenere aperti (dalle revisioni critiche)

1. **La raccomandazione è un'agenda.** Mostrare 5 lotti invece di altri orienta la scelta. Mitigazione: l'elenco completo resta sempre consultabile; si misura quanto le scelte seguono la proposta rispetto a una proposta casuale (metrica M7 della nota 09, "placebo") [H].
2. **Il feedback può derivare.** Mitigazione: il feedback agisce solo sul livello personale; versioni registrate; confronto prima e dopo [H].
3. **Le riserve sono scritte da qualcuno.** Mitigazione: sono regole di livello 1 della costituzione minima, votate e rese pubbliche con il controfattuale prima del voto [I].
4. **Strategia.** Il matching non è manipolabile per chi propone, ma il feedback potrebbe esserlo, se una famiglia "insegna" alla macchina per ottenere un lotto. Da verificare in simulazione [H].

## 4. Confronto empirico: sì, ed è il cuore scientifico della scala urbana

Confrontare gli approcci sugli stessi dati e con le stesse metriche trasforma una preferenza argomentata in un risultato. È anche il modo di evitare i due difetti fatali segnalati dalla revisione metodologica:
- **circolarità**: gli agenti generati dalle stesse ipotesi del sistema;
- **metrica uguale all'obiettivo**: si misura il sistema con ciò che il sistema stesso ottimizza.

### 4.1 Disegno

**Bracci a confronto**, sullo stesso insieme di lotti reali (30–50 nel prototipo, poi i 2.291 siti) e sulle stesse popolazioni simulate:

| Braccio | Approccio |
|---|---|
| B0 | lotteria unica (riferimento minimo) |
| B1 | graduatoria a punteggio (B) |
| B2 | ottimizzazione dall'alto (D, MILP del Lab) |
| B3 | cluster per somiglianza + assegnazione (E, alla Housing Prime) |
| B4 | gruppi con consenso all'ingresso (F, stabilità individuale) |
| B5 | accettazione differita con riserve, senza raccomandazione (J) |
| **B6** | **proposta K** (raccomandazione spiegabile + J + feedback) |

**Popolazioni simulate**, quattro famiglie di generatori indicate dalla nota 08:
1. **strutturale**: dal censimento e dai redditi;
2. **avversaria**: preferenze diverse da quelle che il sistema assume;
3. **verità nota**: parametri veri fissati, per misurare se il sistema li recupera;
4. **agenti LLM**: solo come prova di stress.

**Regola**: un risultato vale solo se regge sia sulla popolazione strutturale sia su quella avversaria [I, da nota 08].

### 4.2 Metriche

Si misurano su preferenze **vere** delle famiglie simulate, che il meccanismo non vede.

| Metrica | Formula (proposta) | Cosa dice |
|---|---|---|
| Rango medio del lotto ottenuto | $\bar r=\frac1n\sum_i \mathrm{rank}_i(\mu(i))$ | quanto ognuno ottiene ciò che voleva |
| Invidia giustificata | quota di coppie $(i,\ell)$ con $\ell\succ_i\mu(i)$ e $i$ prioritario su $\ell$ rispetto a chi l'ha ottenuto | equità e stabilità |
| Sostenibilità economica | quota di famiglie con $c_{i\mu(i)}\le B_i$ | accessibilità reale |
| Diversità per lotto | indice di Simpson $D_\ell = 1-\sum_k p_{k\ell}^2$ su età e condizione | mix ottenuto |
| Esposizione | correlazione tra reddito di una famiglia e reddito medio dei vicini di lotto | segregazione |
| Guadagno dalla manipolazione | utilità ottenuta mentendo meno utilità dicendo il vero, per famiglia | resistenza alla strategia |
| Esclusi | famiglie senza lotto, per categoria | chi resta fuori |
| Influenza del sistema | quota di scelte che seguono la proposta, contro una proposta casuale (placebo) | decisore nascosto (M7) |
| Stabilità nel tempo | quota di famiglie che lasciano dopo l'assegnazione, simulata | tenuta delle comunità |

### 4.3 Ipotesi da fissare prima

Le soglie si fissano prima di vedere i risultati, insieme.

- **H-K1**: B6 ottiene un rango medio migliore di B2 e B1, con invidia giustificata non superiore a B5.
- **H-K2**: con lo stesso vincolo di riserve, raggruppare per ancore (B6) produce diversità per lotto maggiore di B3 senza peggiorare il rango medio oltre una soglia fissata ex ante.
- **H-K3**: B6 ha meno esclusi per categoria di B4 (dove il veto esclude).
- **H-K4**: l'influenza del sistema su B6 (quota di scelte che seguono la proposta) è significativamente diversa dal placebo, ed è riportata comunque, in ogni caso.

**Falsificazione.** Se B6 non batte B5 (J senza raccomandazione), la raccomandazione non serve e si toglie. Se non batte B2 sul rango medio, l'argomento bottom up va riformulato. Entrambi gli esiti sono pubblicabili.

### 4.4 Dimensione e tempi

- **Simulazione**: circa 197 repliche per cella per rilevare effetti piccoli (d = 0,2) [I, calcolo della nota 08]. Con i lotti del prototipo il costo di calcolo è basso [I, nota 10].
- **Prova con persone (F2)**: un solo contrasto, B6 contro B5, entro soggetto: circa 87 persone per d = 0,3 [I, nota 08].
- **Tempi**: il confronto rientra nella pipeline minima di F1 (gennaio–aprile 2027) come "esperimenti pre-registrati". Se si è in ritardo, si tagliano prima B4 e gli agenti LLM, mai B0, B2 e B5 (le linee di base).

## 5. Che cosa resta da verificare prima di scrivere
- Testi integrali: Waldinger 2021, Arnosti & Shi 2020, Hafalir et al. 2013, Sönmez & Yenmez 2022, Boehmer & Elkind 2020.
- Se esistono applicazioni del matching a cooperative o cohousing (nessuna trovata finora, anche in letteratura tedesca e italiana non cercata).
- Profilo AI Act della proposta K: non dà punteggi alle famiglie (raccomanda lotti alla famiglia stessa), ma va confermato con un giurista.
