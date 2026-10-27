# 08 - Modelli matematici e di IA del MIT City Science Group: studio tecnico

Data: 2026-10-27. Lingua: italiano. Scopo: capire cosa hanno fatto il gruppo di Kent Larson e i collaboratori con matematica e IA, cosa ha funzionato e cosa no, e che cosa se ne ricava per un dottorato sulla definizione partecipativa di lotti di social housing a Milano, solo con persone e senza developer ([I]).

**Legenda.** [V] = letto nel PDF con testo estratto (sezione o pagina indicata); [V*] = da riassunto di pagina web prodotto da un modello, non dal testo; [I] = inferenza mia; [H] = ipotesi da verificare; [B] = spiegazione didattica di sfondo, da conoscenza generale e non da una fonte del gruppo (la uso per spiegare logit, CNN, GAN, KLD, ABM e va controllata su un manuale). Parafrasi, nessuna citazione lunga. Dove una formula non è pubblicata lo scrivo.

**Che cosa è stato letto davvero.**
- Letti per intero o nelle sezioni tecniche: Hu et al., Graph RAG (arXiv:2508.16172v2, 19 pagine, riscaricato oggi); Zhang et al., AAMAS 2018 (3 pagine, scaricato da ifaamas.csc.liv.ac.uk); Yurrita et al. (arXiv:2106.14572); Noyman, Hu, Larson, TravelAgent (arXiv:2412.18985, sezioni 1-6 e limiti); Sakai et al., Propagational Proxy Voting (arXiv:2504.13641, sezioni di modello, utilità, caso e discussione); Li et al., HugAgent (arXiv:2510.15144v4, corpo principale e limiti); abstract e struttura di Li et al., GenMinds/RECAP (arXiv:2506.06958) e di Taillandier et al. (arXiv:2507.19364).
- Solo pagina o abstract [V*]: tesi Zhang 2017 (DSpace: 429 a tre tentativi con pause di 65 s, il PDF non è stato letto), MoCho, Deep Image of the City, Reversed Urbanism, Grignard et al. ICCS 2018, CityScope Andorra, tesi Noyman 2022, Adornetto et al. IEEE TAI 2025.
- Bloccati o non raggiungibili: Semantic Scholar (403 dal proxy), doi.org, GitHub, alcune pagine media.mit.edu (robots_disallowed per WebFetch). Non aggirati. L'API di arXiv funziona solo via HTTPS su export.arxiv.org.

---

## 0. Mappa: che cosa è modello e che cosa è IA

Il corpus non è una famiglia unica. Distinguo quattro tipi di oggetto matematico, perché hanno criteri di validità diversi.

| Tipo | Lavori | Oggetto matematico | Che cosa si deve validare |
|---|---|---|---|
| Simulatore meccanicistico | ABM in GAMA (Grignard 2018; Yurrita 2021) | regole di decisione + stato spaziale | calibrazione e validazione su dati osservati |
| Surrogato statistico del simulatore | CityMatrix (Zhang 2018) | funzione appresa da griglia a mappa di traffico | fedeltà al simulatore, poi fedeltà del simulatore al reale |
| Modello di scelta | MoCho (Doorley 2019), Preference Chain (Hu 2025) | distribuzione di probabilità sulle alternative | calibrazione/verosimiglianza, divergenza dai dati osservati |
| Regressione/analisi di dati osservati | Reversed Urbanism (Noyman 2019) | regressione lineare su cluster di permanenza | spiegazione, non previsione |
| Generativo | Deep Image of the City (DCGAN), TravelAgent (LLM + diffusione) | campionatore da una distribuzione appresa | plausibilità, bias, utilità per la deliberazione |
| Aggregazione di preferenze | Propagational Proxy Voting (Sakai 2025) | catena di Markov assorbente | proprietà formali, uso reale |
| Valutazione di LLM sul ragionamento | HugAgent, GenMinds (Li 2025) | benchmark e formalismo di credenze | accordo con il test-retest umano |

[I] Il filo comune è il "ciclo CityScope": una configurazione urbana modificata da persone (tavolo tangibile, AR, web) viene valutata in tempo reale da un modello, e il risultato torna alle persone. Cambia ciò che sta nella scatola del modello: prima ABM e logit, poi reti neurali come surrogati, poi LLM.

---

## 1. CityMatrix: CNN come surrogato di un ABM di traffico (Zhang 2017; Zhang et al. AAMAS 2018)

### 1.1 Problema
Rendere l'urbanistica esplorabile da non esperti in un evento pubblico. Gli strumenti tradizionali richiedono anni di formazione, e i simulatori ad agenti sono lenti. [V, AAMAS p. 2171] Nel sistema CityMatrix ogni cella della griglia può diventare uno di sei tipi (edifici, strade, cortili), con Lego marcati otticamente; slider per la densità; un grafico radar con cinque prestazioni (densità, diversità, energia, traffico, solare) e mappe di calore. L'ABM del traffico è l'unico simulatore costoso. Un ciclo a quattro strati: input utente, valutazione, suggerimento, visualizzazione [V, p. 2171-2172].

### 1.2 Modello matematico
**Simulatore (ground truth).** ABM in GAMA: 24 ore a passi di 1 minuto; tutti gli spostamenti sono eseguiti da una flotta di veicoli autonomi condivisi molto efficiente; esce un volume di traffico per ogni cella stradale e un tempo di attesa [V, p. 2172]. Le regole di decisione degli agenti, la domanda e il routing non sono descritti nell'abstract esteso.

**Surrogato.** Si cerca una funzione appresa f_theta che mappi la configurazione x in {tipi di cella}^(19x19) (tensore 19x19x2) alla mappa y dei volumi di traffico per cella, minimizzando un errore tra f_theta(x) e il risultato del simulatore S(x):

theta* = argmin_theta (1/N) sum_n L( f_theta(x_n), S(x_n) ).

La funzione di perdita L, l'ottimizzatore, il learning rate, le epoche, la dimensione dei filtri, il pooling e le attivazioni non sono pubblicati nell'estratto [V, p. 2172: "solo tre strati convoluzionali", TensorFlow e Keras]. [H] L è probabilmente un errore quadratico medio, perché la metrica riportata è R^2; non è scritto.

**Che cosa è una CNN [B].** Un livello convoluzionale applica a ogni posizione della griglia lo stesso piccolo filtro w (ad esempio 3x3), sommando i valori vicini pesati e passando il risultato per una non linearità: h(i,j) = sigma( sum_{a,b} w(a,b) x(i+a, j+b) + b ). Condividere i pesi fa due cose: impone che la stessa regola locale valga ovunque (invarianza per traslazione) e riduce i parametri. Per il traffico, è plausibile (non verificato) che il volume su una strada dipenda dagli usi del suolo nel vicinato: la convoluzione codifica proprio questo. Tre livelli danno un campo recettivo ampio, ma un'interazione a lunga distanza (percorsi attraverso tutto il distretto) è rappresentata solo se il campo recettivo la copre [I].

**Metrica.** R^2 = 1 - SS_res / SS_tot, dove SS_res = somma degli errori quadratici tra previsione e simulazione e SS_tot = varianza totale delle celle intorno alla loro media. R^2 = 1 vuol dire accordo perfetto; R^2 = 0 vuol dire non fare meglio della media. Il paper non dice se R^2 sia calcolato cella per cella su tutte le configurazioni di test o per configurazione [V, p. 2172 non lo specifica].

**Ottimizzazione dei suggerimenti.** A ogni mossa il server fa una ricerca casuale sulle mosse possibili da quello stato e propone la migliore secondo gli obiettivi dell'utente; le posizioni degli slider diventano pesi sugli aspetti della prestazione [V, p. 2172]. In formule (ricostruzione mia, [I]): data una funzione di punteggio scalare J(c) = sum_k w_k * P_k(c) sulle cinque prestazioni P_k della configurazione c, si campionano M mosse m dall'insieme delle mosse ammissibili e si propone m* = argmax_m J(c ∘ m). La scalarizzazione con pesi scelti dall'utente è l'ipotesi più semplice di compromesso tra obiettivi; il testo non dice se le prestazioni diverse dal traffico siano calcolate da formule analitiche o da altri surrogati. **L'apprendimento per rinforzo non compare nell'extended abstract**, e nemmeno nell'abstract della tesi letto su DSpace [V*]: l'ipotesi "ricerca casuale e/o RL" è sostenuta solo per la ricerca casuale. Il testo integrale della tesi non è stato letto.

### 1.3 Dati e addestramento
10.000 configurazioni di città generate e simulate in GAMA; 7.000 per l'addestramento, 3.000 per il test; ogni simulazione richiede circa 1 minuto su un thread da 2,8 GHz e 8 GB; distribuite su otto computer, 18 ore in tutto [V, p. 2172]. Sono stati provati più algoritmi, parametri e combinazioni di feature "senza sovra-adattamento" al training set; l'obiettivo dichiarato era R^2 = 0,8. [I] Con 7.000 esempi e un input di 722 valori, la CNN regge perché l'input è piccolo; il paper stesso lo dice (p. 2172). Nel riferimento [6] cita Niepert et al. 2016 sulle CNN per grafi, ma non usa un grafo; la connessione è poco chiara.

### 1.4 In uso
Il test pilota è su cinque gruppi da quattro, 20 utenti in tutto, professionisti e non; log del software e questionario [V, p. 2172]. La CNN risponde in meno di 10 ms contro circa 1 minuto dell'ABM [V]. La tesi parla di tavolo tangibile, feedback in tempo reale e suggerimenti [V*].

### 1.5 Cosa ha funzionato
- R^2 = 0,86 per la CNN contro 0,571 per la regressione lineare [V, p. 2172]: la differenza dice che la relazione è fortemente non lineare nello spazio dei tipi di cella.
- Accelerazione di circa 6.000 volte (60 s / 10 ms) [I, calcolo mio da cifre V].
- Nel log, i suggerimenti hanno "stabilizzato e migliorato" il punteggio collettivo nel tempo; 85% dei 20 utenti li ha giudicati utili [V, p. 2172]. Nella tesi, un confronto tra volontari con e senza suggerimenti ha dato risultati "positivi" [V*].

### 1.6 Cosa non ha funzionato o non è dimostrato
1. **Validazione circolare per costruzione.** La verità di riferimento è l'uscita di GAMA. Un R^2 di 0,86 dice che il surrogato imita l'ABM, non che l'ABM descriva il traffico reale; nell'extended abstract non c'è alcuna calibrazione dell'ABM su dati osservati [V]. [I] È un surrogato di un modello non validato empiricamente.
2. **Ipotesi di mobilità autonoma condivisa.** Il traffico che si predice non esiste oggi [V, p. 2172]: nessun dato reale potrebbe validarlo.
3. **Generalizzazione.** Il test viene dalla stessa distribuzione dei dati di addestramento (griglia 19x19, stesse regole); i "quattro esempi" in Fig. 3 sono confronti visivi. Nessuna prova fuori distribuzione, nessuna analisi dei residui, nessuna cross-validazione [V, assenze].
4. **R^2 medio e errori locali.** Un R^2 alto può nascondere errori nelle celle di congestione, che sono quelle decisive [H].
5. **Valutazione utente piccola.** 20 persone, cinque sessioni, tutti pilota; il 85% di "utile" è un'autovalutazione, e non si dice se il punteggio migliorato sia misurato dal modello stesso (nuova circolarità: l'ottimizzatore migliora J, J è calcolato dal surrogato) [I].

### 1.7 Lezioni per il dottorato [I]
- Il disegno "simulatore lento -> surrogato rapido -> interfaccia fisica" è trasferibile ai lotti. Ma servirebbe un simulatore di Milano **calibrato**, e prima di ogni uso in sessione un test della CNN fuori distribuzione (lotti irregolari, non griglia).
- La ricerca casuale con pesi scelti da slider è trasparente; un'ottimizzazione che "suggerisce" in un processo con persone è anche una forma di potere sul risultato. Nel dottorato conviene mostrare i pesi e lasciarli ai partecipanti, oppure non suggerire.
- Tenere separati nel disegno di ricerca tre domande: il surrogato imita il simulatore? il simulatore imita Milano? la persona decide meglio?

---

## 2. Modelli ad agenti in GAMA (Grignard et al.; Yurrita et al.)

### 2.1 Problema
Esplorare scenari di mobilità e di residenza dove molti fattori interagiscono (veicoli elettrici, autonomi, condivisione) e comunicare le conseguenze [V*, pagina ICCS 2018]. La pagina di Grignard et al. descrive un modello generico che costruisce un "micro-mondo artificiale", con modalità di trasporto, profili di persone, congestione e traffico, applicato a Cambridge; non riporta regole, dati né validazione [V*]. Il documento dettagliato che ho potuto leggere è il successivo modello di Yurrita et al. (2021), che riusa e cita Grignard 2018 per i criteri di scelta modale.

### 2.2 Che cos'è un ABM [B]
Un modello ad agenti è un sistema dinamico fatto di entità autonome con stato s_i(t) e regole di decisione d_i; il comportamento aggregato emerge dall'iterazione: s_i(t+1) = d_i( s_i(t), osservazione locale, ambiente(t) ). Si usa quando l'aggregato non si ottiene sommando i singoli (interazioni, segregazione, congestione). Il modello di Schelling sulla segregazione ne è l'esempio canonico; Yurrita lo cita come ispirazione. La difficoltà tipica non è scrivere il modello ma calibrarlo e validarlo: più parametri e più regole ci sono, più è facile far tornare un dato a caso.

### 2.3 Modello matematico di Yurrita et al. (Kendall Square) [V]
Entità: gruppi di isolati censuari (con posti vacanti, affitti medi da web scraping, popolazione per fascia di reddito, presenza di stazione T e bus), edifici (finestra fine), strade, e agenti "persone" che lavorano nell'area e cercano casa e modo di trasporto (sez. 3.1).

**Scelta del modo (iterazione 0).** Ogni modo di trasporto m riceve un punteggio come combinazione lineare delle caratteristiche ponderate dall'importanza che ciascun profilo di reddito attribuisce a prezzo, tempo, difficoltà d'uso e "schema sociale"; si sceglie il massimo:

S_m = w_prezzo * prezzo_m + w_tempo * tempo_m + w_diff * difficoltà_m + w_schema * schema_m,  m* = argmax_m S_m.

I pesi sono sintetici: ad esempio per la fascia 45-60 mila dollari prezzo -0,8, tempo -0,8, difficoltà -0,7, schema 0,7 (Tab. 1); modi con prezzo/km e velocità media tratti da MBTA (Tab. 2) [V, sez. 3.2].

**Scelta della casa (iterazioni successive).** A ogni iterazione ad ogni agente viene proposta a caso un'abitazione alternativa; l'agente si sposta se il punteggio dell'alternativa supera quello dell'attuale; il punteggio comprende prezzo, tempo di pendolarismo con il miglior modo, preferenza di zona e accettazione della diversità, calcolata con la formula di Shannon-Weaver sui profili di reddito dell'edificio o dell'isolato. Si itera finché il numero di chi si sposta tende a zero [V, sez. 3.2; Tab. 3].

Nota formale: la regola è un argmax deterministico di una funzione lineare, **senza termine di errore casuale**. È diverso da un logit, in cui l'incertezza dell'analista entra nella probabilità (vedi §3).

### 2.4 Dati e calibrazione
Dati geografici (shapefile di isolati, disponibilità di appartamenti, edifici, trasporto pubblico, rete stradale) e file con profili di reddito, pesi e modi [V, sez. 3.3]. Calibrazione: otto fattori (prezzo casa, accettazione diversità, zona preferita, peso zona; prezzo trasporto, importanza del tempo, difficoltà, schema) per otto profili di reddito, cioè 64 variabili, ottimizzate con un algoritmo di arrampicata (hill climbing) in esperimenti batch per minimizzare la somma di due errori: errore sulla distribuzione dei profili per isolato (RMSE rispetto alla quota stimata da dati di trasporto/censimento) ed errore sulla ripartizione modale (RMSE rispetto ai dati PTDM della città di Cambridge): RMSE = sqrt( (1/n) sum_i (Y_i - Yhat_i)^2 ) [V, sez. 4, eq. 1]. Risultato: errore medio 3,87% sulla casa e 2,30% sulla mobilità (Fig. 3) [V].

### 2.5 In uso
Nel paper non è in tempo reale: gli autori dichiarano che la complessità e la scala metropolitana rendono difficile ricalcolare l'impatto in tempo reale, e che la conversione in strumento in tempo reale è lavoro in corso [V, sez. 5-6]. Cioè, in questo modello **manca esattamente il surrogato** di CityMatrix.

### 2.6 Cosa ha funzionato
Il modello riproduce con errore basso le due distribuzioni usate per calibrarlo [V]. Ha il pregio, per il tema abitativo, di mettere insieme casa e mobilità e di rendere esplicito un parametro di accettazione della diversità per fascia di reddito.

### 2.7 Cosa non ha funzionato o non è dimostrato
1. **Calibrazione = validazione.** Il testo parla di "calibrazione e validazione", ma la procedura descritta minimizza l'errore sugli stessi dati con cui si valuta; nessun campione tenuto fuori [V, sez. 4]. Con 64 parametri liberi e due distribuzioni da riprodurre, un errore basso non prova che i meccanismi siano giusti [I].
2. **Pesi iniziali sintetici** (Tab. 1-3) e hill climbing dipendente dal punto di partenza, ammesso dagli autori [V, sez. 5].
3. **Verità di riferimento approssimata**: il reddito dei lavoratori è approssimato con il reddito medio dell'isolato censuario [V, sez. 4]: errore ecologico.
4. **Un solo caso** (Kendall Square, ricco e tecnologico) e dati USA; nessuna analisi di sensibilità o di identificabilità dei parametri.
5. **L'agente sceglie tra poche alternative casuali**: nessun mercato, nessun vincolo di accesso (graduatorie, ISEE), nessun rifiuto da parte del locatore [I].

### 2.8 Lezioni per il dottorato [I]
- La scelta del lotto da parte di famiglie con reddito diverso può essere modellata come qui, ma in social housing l'accesso è assegnato, non scelto sul mercato: l'agente non "cerca" ma "aspetta". Il modello di Yurrita serve da griglia concettuale, non da motore.
- Il parametro di tolleranza alla diversità per fascia è lo stesso che il dottorato dovrebbe misurare con le persone, non assumere.
- Regola metodologica: dividere i dati in calibrazione e validazione, riportare identificabilità.

---

## 3. MoCho: scelta modale con modelli a scelta discreta (Doorley, Noyman, Sakai, Larson, UrbComp 2019)

### 3.1 Problema
Prevedere in tempo reale come le persone scelgono il modo di trasporto nell'area metropolitana al variare del progetto urbano, su un tavolo CityScope, con interfaccia web [V*]. Istanza 2018 per l'area di Boston, con sito di 14 acri a Kendall Square [V*].

### 3.2 Modello matematico
**Che cosa si sa.** La pagina dice solo "discrete choice models" calibrati su dati di indagine, con associazioni significative con tempi di viaggio, densità residenziale e occupazionale, età, genere, istruzione e proprietà della casa; non nomina la forma (logit multinomiale o annidato), il metodo di stima, il numero di rispondenti né alcuna metrica numerica oltre "well fitted" [V*]. **La specificazione non è pubblicata sulla pagina**; il codice è su github.com/CityScope/CS_choiceModels (non raggiungibile da qui).

**Spiegazione didattica del logit multinomiale [B].** Teoria dell'utilità casuale: la persona n sceglie, tra le alternative j in un insieme C_n (a piedi, bici, bus, auto...), quella con utilità più alta. L'analista non osserva tutto, quindi U_nj = V_nj + eps_nj, dove V_nj = beta' x_nj è la parte osservabile (tempo, costo, caratteristiche della persona interagite con l'alternativa) ed eps_nj è un errore. Se gli eps sono indipendenti e distribuiti Gumbel (valore estremo di tipo I) con la stessa scala, la probabilità di scelta ha forma chiusa:

P_n(j) = exp(V_nj) / sum_{k in C_n} exp(V_nk).

I coefficienti beta si stimano per massima verosimiglianza sui dati di indagine: LL(beta) = sum_n sum_j y_nj * log P_n(j), con y_nj = 1 se n ha scelto j. Interpretazione: beta_tempo negativo significa che ogni minuto in più riduce l'utilità; il rapporto beta_tempo/beta_costo è il valore del tempo. Limiti noti: la proprietà IIA (il rapporto tra le probabilità di due alternative non dipende dalle altre; il bus rosso/bus blu), che si allenta con il logit annidato; l'omogeneità dei gusti, che si allenta con il logit a coefficienti casuali. Bontà di adattamento: rho^2 di McFadden = 1 - LL(beta)/LL(0), e accuratezza di classificazione fuori campione; **MoCho non riporta nessuna delle due nella pagina** [V*].

### 3.3 Dati e addestramento
Survey di mobilità (numero e anno non dichiarati [V*]). "Addestramento" qui significa stima per massima verosimiglianza di pochi coefficienti, non apprendimento di rete.

### 3.4 In uso
L'utente modifica uso del suolo, densità o prossimità sul tavolo CityScope; un sistema distribuito invia i dati al modello, che restituisce probabilità per persona; la web UI mostra le variazioni [V*]. Il calcolo del logit è istantaneo: è il motivo per cui MoCho non ha bisogno di un surrogato.

### 3.5 Cosa ha funzionato
Dichiarato: "well fitted" e interattività in tempo reale [V*]. Il vantaggio strutturale è l'interpretabilità: ogni coefficiente ha un segno e un'unità, discutibile con i partecipanti [I].

### 3.6 Cosa non è dimostrato
Nessuna metrica; nessun test fuori campione; nessuna validazione sul nuovo progetto, cioè sull'effetto causale di un cambiamento di densità (il logit stima associazioni nei dati attuali; usarlo per un'alterazione del progetto assume stabilità dei coefficienti: [I]); popolazione e parametri di Boston.

### 3.7 Lezioni [I]
Per i lotti, il logit è lo strumento onesto per la scelta di accessibilità: pochi parametri, interpretabile, stimabile con una survey locale a Milano. Si può usare anche per la scelta tra tipologie di alloggio (logit su attributi di alloggio) con esperimenti di scelta (stated choice), dove le persone scelgono tra profili ipotetici: i dati nascono dalla partecipazione.

---

## 4. Graph RAG come modello di scelta: Preference Chain (Hu et al., arXiv:2508.16172v2)

Letto per intero (19 pagine) e riscaricato oggi. Sede: preprint arXiv cs.AI, 5 set 2025 [V]. Codice: github.com/kekehurry/mobility_agent (non consultato) [V, p. 12].

### 4.1 Problema
Prevedere scelta modale e durata dello spostamento per persone con profilo dato in aree con pochi dati. Gli ABM classici hanno regole fisse; ML/DL richiedono grandi dataset; gli LLM da soli producono comportamenti poco coerenti e senza conoscenza locale [V, §1-2].

### 4.2 Modello matematico (notazione dell'articolo, spiegata)
**Grafo BDI.** G = (V, E, omega): nodi Agent, Person (individui simili), Desire, Intention; archi relative_of, similar_to, want_to, choose_to; pesi omega(e) in [0,1] con significato per tipo: vicinanza familiare (omega_rel), similarità di attributi (omega_sim), similarità di desideri (omega_want), vicinanza temporale delle scelte (omega_choice) [V, §3.1, pp. 3-5].

**Ricerca di similarità.** I profili testuali sono trasformati in vettori con il modello mxbai-embed-large; si trovano le persone più vicine all'agente per similarità del coseno, cos(u,v) = u·v / (|u||v|); poi una ricerca in profondità (profondità 3) raccoglie i nodi desiderio e intenzione collegati, formando un sottografo [V, §3.2, p. 5]. Quante persone vengono recuperate (k) non è dichiarato nel testo [V, assenza].

**Probabilità di scelta (eq. 1-4).** Per un agente a e una intenzione i, sia P_{a->i}^(K) l'insieme dei cammini semplici da a a i di lunghezza k <= K, con p = (e_1,...,e_k):

- peso del cammino: W(p) = prodotto_{j=1..k} omega(e_j)  (eq. 1);
- esempio con quattro archi: W(p') = omega_rel * omega_sim * omega_want * omega_choice  (eq. 2);
- punteggio grezzo: S(a,i) = somma_{p in P_{a->i}^(K)} W(p)  (eq. 3);
- probabilità: P(i|a) = S(a,i) / somma_{j in I} S(a,j), con I l'insieme delle intenzioni candidate  (eq. 4) [V, p. 5].

Lettura [I]: poiché i pesi stanno in [0,1], un cammino lungo "costa" (il prodotto diminuisce), come un fattore di sconto sulla distanza nel grafo; sommare i cammini è un conteggio pesato di "testimoni" che sostengono l'intenzione i. Per un cammino agente -> persona simile -> desiderio -> intenzione, l'espressione si riduce a una stima a nuclei (kernel) o k-vicini pesati: la distribuzione sulle scelte è la media delle scelte di persone simili, pesate dalla loro similarità. **Non c'è nessun parametro addestrato**: il modello è un estimatore non parametrico a memoria. Non è però una regressione: non c'è nessuna funzione di verosimiglianza.

**Ricalibrazione con LLM (§3.4, p. 6).** Le probabilità sono trattate come distribuzione a priori e l'LLM le aggiusta in base a condizioni descritte in linguaggio naturale (meteo, ora, città). Il passaggio non ha una formula: è un prompt (Fig. 12, in appendice, solo come figura). Quindi la parte "bayesiana" è una metafora; la regola con cui il testo trasforma il prior in posterior non è pubblicata come equazione [V]. Parametri: Qwen3-8B senza modalità di ragionamento; top-k 20, temperatura 0,6, top-p 0,95, repeat penalty 1 (Tab. 2, p. 17) [V].

**Metriche (eq. 5-6, pp. 6-7).**
- KLD = somma_i somma_j P(i,j) log( P(i,j) / Q(i,j) ), con P la distribuzione congiunta vera tra gruppi di popolazione i e scelte j, e Q la predetta. Spiegazione [B]: la divergenza di Kullback-Leibler misura quanta informazione si perde se si usa Q per descrivere dati che hanno distribuzione P; vale 0 solo se P = Q, non è simmetrica, e **diverge se Q(i,j) = 0 dove P(i,j) > 0**. Il paper non dice se applichi una regolarizzazione: dato che ammette che il Preference Chain "ignora" le opzioni rare e le durate oltre 40 minuti (§4.4, p. 7), il valore di KLD dipende molto da come si trattano gli zeri [I].
- MAE = (1/N) somma_i somma_j |P(i,j) - Q(i,j)| (il paper la chiama "Mean Average Error") [V].

### 4.3 Dati e addestramento
Replica, giovedì tipico di primavera 2024, Cambridge (MA) e San Francisco; campioni di riferimento da 10 a 1.000, più 1.000 campioni di validazione; esperimenti principali con 50 riferimento esclusi dalla validazione. Input: età, reddito, occupazione, dimensione del nucleo, veicoli, istruzione, scopo, ora; output: 7 modi e durata in sei classi da 10 minuti. Variabili continue categorizzate. I dati sono anonimizzati con tecniche ML per la privacy; il PDF non li chiama sintetici [V, §4.1, Tab. 1]. Baseline: LLM puro, Random Forest, MLP, XGBoost con ricerca a griglia (Tab. 2); deep learning escluso per la scarsità di dati [V, §4.2].

### 4.4 In uso (Mobility Agent, §5)
Un ABM costruito attorno a un agente LLM con tre strumenti (generatore di profilo, di agenda, ricerca di POI): 1) profili da dati demografici; 2) agenda giornaliera; 3) modo e durata con il Preference Chain; 4) ricerca di POI per codice NAICS, modo e durata; 5) l'LLM sceglie il POI; 6) si ripete fino a fine giornata. 1.000 persone a Cambridge per 24 ore [V, §5.1-5.2, p. 9]. L'inferenza è lenta: non è un modello da tavolo in tempo reale [V, §6.1].

### 4.5 Cosa ha funzionato
- Con riferimento di 50 campioni il Preference Chain avvicina le distribuzioni al reale più dell'LLM da solo, in tutti i gruppi demografici (Fig. 3-4) [V]. Lettura grafica approssimata di Fig. 5: KLD dell'LLM circa 1,2-1,3 contro circa 0,5-0,7 per il Preference Chain tra 10 e 100 campioni [V, lettura approssimata].
- Confronto con ML: con meno di 100 campioni il Preference Chain ha KLD più basso di RF, MLP e XGBoost; oltre 100 l'MLP lo supera. Sul MAE il miglioramento arriva fino a 50 campioni, poi oscilla; l'MLP lo supera dopo 50 (§4.4, p. 8) [V].
- Trasferimento tra città: usare i dati di San Francisco per Cambridge e viceversa migliora l'LLM ma resta inferiore ai dati locali (Fig. 6-7) [V].
- Flusso di traffico totale a Cambridge: KLD 0,814 per l'agente LLM contro 0,621 per il Mobility Agent con 50 riferimenti; individua Massachusetts Avenue come asse principale, mentre l'LLM puro indica Cambridge Street (§5.2) [V].
- Tra LLM: Llama3.1:8b è più allineato senza riferimenti, Qwen3:8b migliore con il Preference Chain (Fig. 13) [V].

### 4.6 Cosa non ha funzionato o non è dimostrato
1. **Il punto debole dichiarato.** L'accordo con il reale è il confronto con un modello di popolazione (Replica), non con comportamento osservato direttamente; il testo non discute questa distinzione [I, non confermata né smentita dal PDF].
2. **Opzioni rare ignorate.** Il metodo trascura servizi on demand, "altri modi" e durate oltre 40 minuti (§4.4) [V]: sono spesso proprio le scelte delle fasce più fragili.
3. **Sopra circa 100 campioni un MLP fa meglio**; con molti dati il metodo non serve. Il vantaggio vale solo nel regime di scarsità [V].
4. **Nessuna ablazione**: non si separa il contributo del recupero a grafo, del prior e dell'LLM [V]. Non si sa se un k-vicini pesato senza LLM farebbe uguale [I].
5. **Sui POI il vantaggio non si vede**: KLD simili; l'ipotesi degli autori è l'assenza di informazione di preferenza diretta; il riferimento POI è SafeGraph (luglio 2023) (§5.3) [V].
6. **Allucinazioni e lentezza** ammesse, "non adatto ad applicazioni critiche"; modello discreto (§6.1) [V]; nessun traffico esterno a Cambridge.
7. **Una sola famiglia di test** (mobilità statunitense), un solo LLM piccolo; ripetibilità del campionamento LLM non quantificata (le barre d'errore sono nelle figure, non in tabella) [I].
8. **Preprint**: la peer review non è verificabile dal PDF.

### 4.7 Lezioni [I]
- L'idea più riutilizzabile non è l'LLM, ma il **recupero di persone simili con pesi su un grafo**: un modello a memoria interpretabile, utilizzabile con poche decine di risposte. Per il dottorato: con 50 interviste a famiglie milanesi si può stimare una distribuzione di preferenze condizionata al profilo senza assumere una forma funzionale.
- Se si usa un LLM, va confrontato con la versione senza LLM (ablazione) e con un logit semplice, e va testato sul ricordo delle scelte rare.
- KLD e MAE vanno accompagnati da un test sulle code della distribuzione.

---

## 5. Deep Image of the City (Noyman, DCGAN su Cityscapes)

### 5.1 Problema
La visualizzazione urbana è lenta e costosa; nei primi stadi della progettazione (zonizzazione, schema) i dettagli non esistono. Si propone una visualizzazione generativa in tempo reale accoppiata al tavolo CityScope, per discutere massa e programma, ispirata a "The Image of the City" di Lynch [V*].

### 5.2 Modello
DCGAN [V*] addestrata su Cityscapes [V*]. **Non sono pubblicate nella pagina né la funzione di perdita né l'architettura né il condizionamento sul progetto.**

**Spiegazione [B].** Una GAN mette in gara due reti: un generatore G(z) trasforma un rumore z in un'immagine; un discriminatore D(x) stima la probabilità che x sia reale. Il gioco è

min_G max_D E_{x~p_dati}[ log D(x) ] + E_{z~p_z}[ log(1 - D(G(z))) ].

All'ottimo, la distribuzione generata coincide con quella dei dati. "Deep convolutional" significa che entrambe le reti sono convoluzionali (convoluzioni trasposte nel generatore, norma di batch, nessun livello completamente connesso). Una DCGAN base è **non condizionata**: da sola non permette di "mostrare" un progetto specifico. Come il design sul tavolo diventi un'immagine (condizionamento, selezione del punto di vista, mappa semantica) non è descritto [V*]. Cityscapes, per quanto ricordo, è un insieme di scene stradali di città prevalentemente tedesche con annotazione semantica [B, da controllare]. Il dato di data/sede è in conflitto: la pagina MIT dà Noyman, giugno 2019; l'elenco del gruppo dà Noyman e Larson, 2020 [V*].

### 5.3 Come funziona, cosa ha funzionato
Dopo ogni modifica del tavolo un rendering "street-view" in tempo reale, con front-end web leggero [V*]. La pagina non riporta metriche, test, né studio utente [V*].

### 5.4 Cosa non è dimostrato [I]
Nessuna metrica di qualità (nemmeno FID), nessuna valutazione della coerenza con il progetto, nessun test su persone; **il bias del dataset** (città tedesche, tipologie, ricchezza) viene incorporato come "immagine della città" normale; un'immagine realistica ma inventata può persuadere più di un grafico (rischio di manipolazione; FindingPlaces stesso cita la manipolazione tramite pre-processing come minaccia, nota 06).

### 5.5 Evoluzione
In TravelAgent (2024) Noyman e Hu sostituiscono la GAN con un modello di diffusione (SDXL-Turbo) guidato da classi o da bordi (canny) dal modello 3D semanticamente segmentato [V, §3.1, Fig. 3 di arXiv:2412.18985]: il condizionamento che nel 2019 mancava.

### 5.6 Lezioni [I]
Per i lotti milanesi, mostrare immagini generate a persone che discutono è rischioso: preferire visualizzazioni schematiche o da dati locali, e dichiarare cosa è generato. Se si usa un generatore condizionato, validarlo con un test di accordo tra persone ("questa immagine rappresenta questo progetto?").

---

## 6. Reversed Urbanism (Noyman, Doorley, Xiong, Alonso, Grignard, Larson; Environment and Planning B 46(8), 1480-1498, 2019)

Riassunto di pagina [V*]; DOI 10.1177/2399808319840668 da RePEc (IDEAS) [V*]; testo non letto.

### 6.1 Problema
Misurare, su un'intera città, quali spazi pubblici "funzionano", senza osservazione manuale sporadica.

### 6.2 Modello
Dati telecom anonimizzati e georeferenziati di Andorra. 1) **Stay-point**: punto in cui un dispositivo resta entro una distanza di roaming per un tempo minimo; 2) **cluster di attività** descritti da dimensione, persistenza, diversità; 3) **regressione lineare multivariata** a risoluzione 25-50 m tra le caratteristiche del cluster e le variabili urbane (morfologia, uso del suolo, servizi e svago, istruzione, parchi, acqua, centralità di intermediazione della rete stradale) [V*]. In forma [B]: y_c = beta_0 + sum_k beta_k * x_{c,k} + eps_c, con y_c una misura del cluster nella cella c e x le variabili urbane; i beta sono stimati con i minimi quadrati. Le specifiche esatte (trasformazioni, selezione delle variabili, R^2, errori standard, numero di celle) non compaiono nel riassunto [V*].

### 6.3 Cosa ha funzionato
Associazioni stabili: servizi e svago, acqua e centralità stradale sono associati a cluster più grandi, diversi e duraturi; istruzione e parchi hanno associazione negativa [V*]. Lo studio propone l'inversione "comportamento osservato -> giudizio di progetto" (da cui il nome) [V*].

### 6.4 Cosa non è dimostrato [I]
- Correlazione, non causalità: la centralità attrae dwell, ma il dwell può causare servizi.
- "Prestazione" = permanenza di dispositivi: misura il tempo passato, non il benessere né l'inclusività. Un parco con risultato negativo non è un parco "fallito".
- Rappresentatività dei dati telecom (copertura, turisti in transito in Andorra; Andorra è un contesto non generalizzabile).
- Nessuna metrica in pagina; limiti non letti.
- Lavoro collegato: RevUrb, modellazione con processi puntuali sugli stessi dati (Doorley et al. 2019): solo titolo [V*]; il metodo non è stato letto.

### 6.5 Lezioni [I]
Per i lotti, questa logica vale per la fase di valutazione post-occupazione: usare dati comportamentali (con consenso) per giudicare spazi esistenti di edilizia popolare. Non per decidere dove costruire.

---

## 7. Lavori 2018-2026 con ML/IA trovati (arXiv e pagine del gruppo)

### 7.1 TravelAgent (Noyman, Hu, Larson; arXiv:2412.18985, 25 dic 2024, preprint)
**Problema.** Valutare come le persone si orientano e vivono lo spazio (a scala dal progetto di quartiere alla stanza) prima che esista, superando osservazioni manuali e ABM a regole semplici [V, §1].
**Modello.** Non c'è un modello matematico nuovo: è un'architettura di agente generativo. A ogni passo l'agente riceve ingressi sensoriali (immagine in prima persona generata da un modello 3D semplice con SDXL-Turbo, segmentazione, raggi per profondità e collisioni, mappa di scoperta, bussola opzionale, memoria spaziale testuale), elabora con catena di pensiero in tre fasi (osservazione, pianificazione, azione), esegue un'azione chiave-valore con lunghezza (per esempio "avanti 1 metro") e aggiorna la memoria [V, §3.1-3.2, Fig. 1]. Nessuna funzione di utilità né perdita.
**Dati.** 100 simulazioni, 1.898 passi, scenari della "stazione della metropolitana" con combinazioni di stagione, ora, persona (anche "utente in sedia a rotelle") [V, §4.2].
**In uso.** Piattaforma web: si cambiano scenario, profilo, compito modificando un breve testo [V, Fig. 2].
**Cosa ha funzionato.** Completamento del compito 76% (nel testo introduttivo "circa 75%": piccola incoerenza interna); i fallimenti si concentrano nello scenario notturno; analisi spaziali, linguistiche e di sentimento dei registri di pensiero distinguono percorsi riusciti e falliti [V, §5.2]. L'idea: i luoghi dove gli agenti si perdono segnalano scarsa leggibilità del progetto.
**Cosa non è dimostrato.** Gli autori ammettono: serve validazione contro studi con persone, osservazioni reali e ABM tradizionali; bias, allucinazioni e generalizzazione degli LLM; le decisioni dipendono dalle condizioni iniziali; le immagini generate non sono coerenti tra i passi [V, §6.2]. Nei primi esperimenti il percorso era determinato dalle scelte iniziali (comportamento quasi deterministico) [V, §5.1]. Gli agenti conoscono già l'ambiente e ricevono indicazioni di direzione nel prompt (§4.2.2): il 76% misura quanto un LLM segue indicazioni da immagini, non quanto sia difficile orientarsi per una persona [I].
**Lezione [I].** Utile come strumento di esplorazione "dove potrebbe esserci confusione", mai come sostituto di camminate con residenti.

### 7.2 Propagational Proxy Voting (Sakai, Atchade-Adelomou, Jiang, Alonso, Larson, Suzuki; arXiv:2504.13641, apr 2025, preprint)
Questo è il lavoro matematicamente più vicino alla "definizione partecipativa".
**Problema.** Il voto semplifica la volontà dei partecipanti; la democrazia liquida (delega) ha deleghe binarie e catene incontrollate [V, §1-2].
**Modello.** Ogni votante distribuisce voti **frazionari** tra proposte, altri partecipanti e insiemi intermedi (gruppi, categorie). La matrice di voto V è una matrice di transizione di una catena di Markov assorbente (proposte = stati assorbenti, con 1 sulla diagonale; i votanti sono stati transitori, con zero sulla propria diagonale: nessun auto-voto) [V, §IV.B, eq. 5-7]. Il voto finale è il limite W = lim V^x, calcolabile per elevamenti al quadrato ripetuti W = lim V^(2^x) (eq. 8-9) [V]. Con intermediari X (votanti), Y (intermediari), Z (proposte) la matrice è a blocchi 3x3 (eq. 10-11) [V]. **Influenza** o "Net Proxy Vote": p_i = somma_j somma_t W_ij(t) / somma_t W_ii(t) (eq. 12), cioè il voto totale che i riceve diviso la quota che ritorna a i attraverso cicli, e si dimostra con un aggiornamento di rango uno che il suo vettore è parallelo a f (I - V)^(-1) (Lemma IV.5) [V]; minimo 1,0 se nessuno delega a i.
**Utilità.** Il votante j ha un'utilità di delega che combina allineamento di preferenze (F_{i,j} = -theta ||F_i - F_j||), competenza e_{i,j}, un costo di perdita di controllo gamma * lunghezza della catena, e un termine logaritmico di influenza (rendimenti decrescenti); la forma CES (Constant Elasticity of Substitution) è usata per distribuire il voto; con più periodi le preferenze si aggiornano in base agli esiti [V, §V]. [B] La CES è la funzione di utilità micro-economica U = (sum a_i y_i^rho)^(1/rho): rho misura quanto sono sostituibili i destinatari della delega.
**Dati.** Caso: Cambridge Participatory Budgeting 2023, 20 proposte in quattro categorie, 69 partecipanti in 10 tavoli; discussione di 5 minuti per tavolo, valutazione con cursori su un'app web; i tavoli e le categorie sono intermediari con distribuzione uguale del voto [V, §VI].
**Risultati.** La categoria Ambiente ha raccolto la maggiore delega frazionaria; le categorie dominano la metrica di influenza; il confronto con la democrazia liquida (stessi input, tolti gli intermediari, un voto intero all'elemento preferito) dà una deviazione standard dei voti di 0,64 per PPV contro 4,20 per LD: il PPV produce punteggi più sfumati, meno "il vincitore prende tutto" [V, Tab. III].
**Cosa non è dimostrato.** Costo computazionale elevato su larga scala [V, §VII.C]; il modello di utilità è normativo: non si stimano gamma, theta, rho da comportamenti [I]; 69 studenti (dal testo: "69 students" nell'abstract) non sono cittadini; "più sfumato" non è "più giusto"; non c'è confronto con altri metodi di voto frazionario (quadratic voting, approval) [I].
**Lezione [I].** Il formalismo è un candidato per aggregare, in un laboratorio per i lotti, preferenze su alternative di progetto con delega a facilitatori o gruppi di inquilini, ma andrebbe usato come strumento di lettura, con dichiarazione dei pesi e prova di sensibilità: l'elemento "influenza" può anche far emergere i mediatori informali. Rischio: la matematica sembra neutrale e nasconde scelte (uguale ripartizione agli intermediari).

### 7.3 HugAgent e GenMinds/RECAP (Li et al., MIT Media Lab con Alonso e Larson; arXiv:2510.15144 e 2506.06958)
**Problema.** Gli LLM simulano la risposta media; si vuole prevedere il ragionamento di una persona e come cambia con una nuova informazione [V].
**Modello.** Formalismo: lo stato di credenza b_i = P(s | C_i), con contesto C_i; sotto un intervento I_t, b^{t+1} = U(b^t, I_t); variazione Delta b = E_{b^{t+1}}[s] - E_{b^t}[s]. Ancore normative: aggiornamento bayesiano b'(s) proporzionale a b(s) p(I|s) e modelli causali strutturali con do(I) [V, §2]. In pratica, credenza = (s, w) con s in {1..10} e pesi di K ragioni [V, §3.2]. Due compiti: inferenza dello stato (Belief State Inference) e aggiornamento (Belief Dynamics Update) [V].
**Dati.** Dominio sanità, sorveglianza e **zonizzazione**; da oltre 120 partecipanti (Prolific) ne restano 54; 356 item di inferenza e 1.386 di aggiornamento (Tab. 1); interviste semi-strutturate con chatbot "TraceYourThinking" [V, §3.3-3.4].
**Risultati.** Test-retest umano a 14 giorni: accuratezza 84,84% sull'inferenza dello stato e 85,66% sull'aggiornamento, ma solo 13 persone conservate dopo i controlli [V, §3.5]. I migliori LLM sono 7-9 punti sotto l'umano nell'inferenza e con errori maggiori nella direzione degli aggiornamenti; per GPT-4o il passaggio ad un altro dominio fa scendere l'inferenza da 74,66% a 58,56% e l'aggiornamento da 63,11% a 44,64%; più contesto non migliora l'aggiornamento (entro 1 punto) [V, §4.2, §5].
**Limiti dichiarati.** Pochi partecipanti, solo tre domini di politica, auto-segnalazione come proxy, sensibilità a prompt e versione del modello [V, Limitations].
**Lezione [I].** È la prova più diretta, nel corpus, che un LLM non può sostituire il parere di una persona su una questione come lo zoning. Per il dottorato giustifica il disegno "solo con persone".

### 7.4 Altri lavori trovati (non letti o solo pagina)
- Yurrita et al. è già in §2. Coretti-Sanchez et al., "Urban mobility swarms" (ITSC 2023) e Genua Cerviño et al. (arXiv:2402.19233, flotte condivise di veicoli autonomi leggeri per consegne, ABM a Cambridge con piattaforma interattiva): ABM di mobilità, fuori dal tema abitativo; letto solo l'abstract [V].
- Azcarate Urrutia et al., scelta modale con machine learning in Gipuzkoa (ITSC 2024) e Bilbao Pavón et al., scelta di mobilità in America Latina (2025): titoli da elenco del gruppo, pagina non raggiungibile; non letti [V*].
- Adornetto et al., "Generative agents in agent-based modeling: overview, validation, and emerging challenges", IEEE Transactions on Artificial Intelligence 2025 (DOI 10.1109/TAI.2025.3566362): rassegna, propone modelli ibridi ABM-GABM e validazione sistematica [V*, solo pagina]. Atchade-Adelomou et al., "Humanized Agent-based Models: A Framework" (citato in arXiv:2508.16172, ref. 20): non letto.
- Fan, Su, Sun, Noyman, Zhang, Pentland, Moro (arXiv:2209.07041, 2022): "Experienced Social Mixing" di strade da dati mobili di 0,5 milioni di utenti in tre aree USA; la concentrazione di visitatori spiega il 26% del mixing, servizi adiacenti, diversità residenziale e reddito il 44%; la frequenza dei negozi di cibo aumenta il mixing 2016-2018 [V, solo abstract]. Rilevante per il tema "mescolanza sociale" nei quartieri con social housing. Noyman è coautore, non primo autore.
- Noyman, "Gridnberg" (arXiv:2607.22523, 24 lug 2026): dataset di instradamento pedonale con quota per New York, 313.184 segmenti su 315.577 (99,24%), costi di percorso distanza/pendenza di comfort/pendenza per accessibilità [V, solo abstract]. Non è IA: è infrastruttura di dati; segnalo perché il gruppo si sposta su dati aperti riproducibili.
- Taillandier, Zucker, Grignard, Gaudou et al., "From the Fluency Fallacy to the Micro-to-Macro Validity Gap" (arXiv:2507.19364, v4 ott 2026; inviato a Frontiers in AI): critica metodologica sull'uso di LLM nelle simulazioni sociali. Grignard (afferenza UMMISCO/IRD, ex City Science) è coautore, ma il lavoro non è del gruppo del MIT. Sostiene che gli LLM hanno valore operativo in giochi seri e ambienti partecipativi ed esplorazione, non in ricerca confermativa o previsione sociale precisa; propone architetture ibride con ABM esplicito e introduce il rischio di "physics washing" (la rigore fisico del simulatore che copre decisioni LLM non validate) [V, abstract e struttura].
- Tesi Noyman 2022 "CityScope: An Urban Modeling and Simulation Platform": quattro temi (insight, transformation, prediction, consensus), casi: allocazione di alloggi per rifugiati in Germania, mappatura della sicurezza a Guadalajara, co-creazione del trasporto di massa a Boston [V*, solo abstract]; l'abstract non menziona ML.
- Non trovato su arXiv per autori richiesti: nessun lavoro 2023-2026 di Doorley, Sakai (oltre PPV e un lavoro del 2026 su aggregazione di LLM: arXiv:2606.08098, solo titolo [V*]) né Winder, Zhang Y. oltre a quelli già citati. Il motore Semantic Scholar è bloccato dal proxy, quindi l'elenco è incompleto.

---

## 8. Sintesi trasversale

### 8.1 Cosa ha funzionato nel complesso
1. **Surrogati di simulatori con input piccolo** (CNN 19x19): grande accelerazione con buona fedeltà al simulatore [V].
2. **Modelli interpretabili a pochi parametri** (logit, regressione lineare, punteggi lineari) sono compatibili con la discussione in sala, anche se non validati in pagina.
3. **Modelli a memoria con pochi dati** (Preference Chain) battono il ML nel regime sotto circa 100 campioni [V].
4. **Strumenti che rendono visibile la struttura** (influenza in PPV, mappa di scoperta in TravelAgent) sono utili come lettura, non come verdetto.

### 8.2 Cosa non ha funzionato o non è mai stato mostrato
1. **Validazione circolare.** Il surrogato è valutato sul simulatore (Zhang); il modello ad agenti è valutato sugli stessi dati di calibrazione (Yurrita); l'agente LLM sul modello di popolazione (Hu). Nessuno dei lavori letti valida una previsione rispetto a **un cambiamento reale di progetto**.
2. **Generalizzazione.** Tutto è testato su Cambridge/Boston/San Francisco (e Andorra per i dati telecom); il solo lavoro con una prova esplicita di trasferimento (Hu) mostra che il dato locale batte il dato di un'altra città [V].
3. **Bias.** L'LLM trascura le scelte rare [V]; la GAN eredita il dataset; gli agenti "sedia a rotelle" non sono mai confrontati con persone reali [V].
4. **Valutazione con persone sempre piccola e autoriferita**: 20 utenti (CityMatrix), 69 studenti (PPV), 13 persone di test-retest (HugAgent).
5. **Uso in tempo reale solo dove il modello è semplice** (logit, CNN piccola): ABM e LLM non girano in sessione [V].

### 8.3 Per il dottorato su lotti di social housing a Milano, solo persone, senza developer [I]
- **Architettura minima difendibile**: un modello a pochi parametri leggibile (logit su alloggio/servizi stimato con scelte dichiarate di residenti), un simulatore semplice calibrato sul territorio, un surrogato solo se serve la velocità, tutto con dati di validazione tenuti fuori.
- **Cosa non importare**: i coefficienti di MoCho, la CNN di CityMatrix, l'immagine generata da Cityscapes; sono Boston/Germania.
- **Regola sull'LLM**: usarlo, se mai, per esplorare scenari e sintetizzare, non per rappresentare i residenti (HugAgent mostra che non regge sull'individuo e sul cambio di dominio [V]). Proteggere dalla "fallacia della fluidità" [V, Taillandier].
- **Aggregazione**: PPV è un candidato sperimentale; richiede un pre-test su un gruppo reale e il confronto con un metodo semplice (voto di approvazione) prima di sostenerne la superiorità.
- **Aperte**: come misurare la fiducia dei partecipanti nel modello; come rendere visibili i pesi; se la scelta in social housing, assegnata e non di mercato, richieda un modello di allocazione (matching) invece che di scelta, che nel corpus non compare.

---

## 9. Tabella delle fonti e stato

| Fonte | Stato |
|---|---|
| Hu et al., arXiv:2508.16172v2 (PDF scaricato oggi) | [V] testo e appendice; figure solo approssimate |
| Zhang et al., AAMAS 2018, pp. 2171-2173 (ifaamas.csc.liv.ac.uk/Proceedings/aamas2018/pdfs/p2171.pdf) | [V] 3 pagine |
| Zhang 2017, tesi (DSpace 1721.1/114059) | [V*] solo abstract; PDF: 429 a tre tentativi |
| Yurrita et al., arXiv:2106.14572 | [V] corpo e riferimenti |
| Noyman, Hu, Larson, arXiv:2412.18985 | [V] sezioni 1-6 e limiti; appendici non lette |
| Sakai et al., arXiv:2504.13641 | [V] modello, utilità, caso, discussione (estrazione parziale di alcune equazioni) |
| Li et al., arXiv:2510.15144 | [V] corpo principale e limiti; appendici non lette |
| Li et al., arXiv:2506.06958; Taillandier et al., arXiv:2507.19364; Fan et al., arXiv:2209.07041; Genua Cerviño et al., arXiv:2402.19233; Noyman, arXiv:2607.22523 | abstract e struttura |
| MoCho; Deep Image of the City; Reversed Urbanism; Grignard ICCS 2018; CityScope Andorra; tesi Noyman 2022; Adornetto IEEE TAI 2025 | [V*] pagine web |
| Elenchi pubblicazioni media.mit.edu (Noyman, Larson/CityScope, Alonso) | [V*] riassunti di elenco |

Non inventato nulla: se un valore (perdita, iperparametri, R^2 di Reversed Urbanism, specificazione di MoCho, k nel Preference Chain) manca, è indicato come non pubblicato o non letto.
