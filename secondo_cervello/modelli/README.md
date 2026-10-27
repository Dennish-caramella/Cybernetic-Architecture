# 04_Fondamenta Matematiche

Data: 2026-10-20

Questa cartella raccoglie il materiale sui modelli matematici, filosofici, cibernetici, di teoria dei giochi e di IA usato come base delle analisi della tesi.

## File

| File | Contenuto | Stato |
| :--- | :--- | :--- |
| `Atlante_Critico_Modelli.md` | Atlante scritto da Dennis: formalizzazioni in LaTeX, esempi, schemi, sinottico e fonti. Testo riportato senza modifiche, salvo la decodifica delle entità HTML (es. `&#39;` → `'`) dovuta al passaggio del messaggio. | Testo di Dennis, da verificare sulle fonti (vedi sotto) |
| `Catalogo_modelli.md` | Catalogo unico dei modelli di tutte le analisi 00-36, con stato [V]/[S]/[I]/[L]. | Lavoro precedente, 2026-10-20 |
| `Studio_modelli_con_esempi.md` | Studio dei modelli con esempi. | Lavoro precedente, 2026-10-20 |
| `Cronistoria_e_correlazioni_modelli.md` | Cronistoria e correlazioni tra i modelli. | Lavoro precedente, 2026-10-20 |
| `Analisi_approfondite_per_teoria.md` | Analisi approfondite raggruppate per teoria. | Lavoro precedente, 2026-10-20 |
| `Verifiche_testi_primari.md` | Esito delle verifiche sui testi primari raggiungibili online. | Lavoro precedente, 2026-10-20 |

## Stato delle legende

* [V] verificato sul testo primario
* [S] dalla sintesi di analisi, non verificato sul testo
* [I] inferenza
* [L] lettura non raggiunta

## Delimitazione dichiarata nell'Atlante

L'Atlante dichiara che la **Statica Grafica 3D** (diagrammi reciproci di forma e forza, maglie poliedriche, equilibrio di Minkowski) è esclusa. Questa è una scelta metodologica dichiarata nel documento. Non è una verifica di contenuto.

## Lista di controllo: da verificare prima di usare l'Atlante

Nessuna voce qui sotto è stata verificata. Ogni punto richiede il testo primario o la fonte indicata.

### Attribuzioni e citazioni

- [ ] **Langton (1984) e von Neumann.** L'Atlante (sez. 2.2) attribuisce a Langton la tesi "computazione universale condizione sufficiente ma non necessaria". Le Verifiche confermano che il testo di von Neumann e Burks (1966) non la sostiene. Da controllare che nessun altro punto dell'Atlante, o del Catalogo, la attribuisca a von Neumann.
- [ ] **Nash 1950 e 1951.** L'Atlante (sez. 4.1) dice che Nash dimostra l'esistenza con il teorema di Kakutani. Le Verifiche dicono che il 1951 usa Brouwer e che Kakutani è la base del 1950. Da riformulare, dopo aver controllato il testo del 1950 (PNAS), che l'Atlante elenca in bibliografia ma non è stato letto.
- [ ] **Bertalanffy.** L'Atlante (sez. 1.1) attribuisce l'equifinalità e la formula di stato stazionario a Bertalanffy. Le Verifiche dicono che la recensione *Nature* 1949 non contiene l'equifinalità. Il *Science* 1950 non è stato raggiunto. Da controllare la fonte esatta.
- [ ] **Bertalanffy 1957 (crescita).** Equazione di crescita non verificata sul testo. Resta [S].
- [ ] **Ashby 1956, pagine.** L'Atlante (sez. 3.2) dà pp. 121–126 per la varietà, pp. 202–213 per la legge, p. 207 per "Only variety can destroy variety". Le Verifiche dicono che il testo non è stato raggiunto oltre il cap. 4. Da controllare su PDF completo.
- [ ] **Ashby, forma della legge.** La forma $V(O) \ge V(D) - V(R)$ nella tabella finale è una formalizzazione logaritmica. Da confermare sul testo, non è stata verificata.
- [ ] **Codd (1968), 8 stati.** Non verificato.
- [ ] **Husserl e Smith & Mulligan (1983).** Riferimento bibliografico incerto nelle Verifiche (*Topoi* 3 o 2(1)). Non raggiunto.
- [ ] **Bogost.** Nella sez. 2.5 l'Atlante cita *Unit Operations* (2006). Nella bibliografia (sez. 8) cita *The Rhetoric of Video Games*, in *The Ecology of Games* (2008). Da controllare che il riferimento sia corretto, e in quale libro compaia la definizione di unit operation.
- [ ] **Carpo 2023 (*Beyond Digital*).** La scansione in "prima" e "seconda svolta digitale" è una sintesi dell'Atlante. Da confrontare con il testo.
- [ ] **Alexander 1964, min-cut.** L'Atlante (sez. 3.4) dice che Alexander usa un algoritmo di partizionamento min-cut e propone una formula $M(\mathbf{x})$. Né il min-cut né la formula sono stati verificati nel testo. La formula è probabilmente una formalizzazione dell'Atlante, non di Alexander. Da segnare come [I] se non trovata.
- [ ] **Pask, SAKI (1956).** Descrizione di SAKI da controllare sulla fonte primaria.
- [ ] **Schelling 1978, soglia τ = 0,33.** Il valore e il risultato di segregazione sono da controllare su Schelling 1971/1978 e su fonte primaria.
- [ ] **Axelrod, condizione δ ≥ (T−R)/(T−P).** La formula è da confermare sulla fonte (Axelrod 1984 o articolo del 1980).
- [ ] **Nowak & May 1992.** Descrizione dei cluster e del punteggio $8 \times R$: da confrontare con l'articolo *Nature* 359.
- [ ] **Tero et al. (2010), Physarum.** La formula di adattamento $dD/dt$ con $\gamma$ e $\mu$ è una formalizzazione dell'Atlante. Da confrontare con l'articolo originale. Se non confermata, segnare [I].
- [ ] **Gray-Scott, valori (F, k).** I valori indicativi dello spazio dei parametri (es. F≈0.030, k≈0.062) sono da controllare su fonte. Lo schema ASCII è illustrativo.
- [ ] **Gumin 2016 (WFC).** Attribuzione e formula dell'entropia da controllare sul codice o sul repository originale.
- [ ] **PPO, Schulman et al. 2017.** Formula di loss: da confermare sull'articolo. In genere corretta, ma da controllare.
- [ ] **Kirkpatrick et al. 1983.** Criterio di Metropolis e α in [0,85; 1): da controllare sul testo.
- [ ] **Smooth minimum (smin).** Formula standard di letteratura SDF, da confermare sulla fonte di riferimento.
- [ ] **Space Syntax (Hillier & Hanson 1984).** Definizioni di isovist, MD e integrazione: da controllare sul testo. La definizione di "Relative Asymmetry" nella tabella è sintetica.

### Affermazioni dell'Atlante che non sono fonti

- [ ] **Sezione 4.4, percentuali di soddisfazione (75%, 72%, 65%, 53%)** per i quattro motori (w)Ego. Non è chiaro da quale analisi (es. 31-33 o SpaceFighter) provengano. Da trovare la fonte o marcare come non verificato.
- [ ] **Sezione 4.2 (dilemma del prigioniero).** Gli anni di pena (0, 1, 3, 5) sono un esempio di comodo: la matrice è corretta in forma logica. Non è una fonte storica precisa.
- [ ] **Sezione 2.3 e tabelle sinottiche.** Il collegamento tra modelli e progetti (es. "Oikos", "AIRS", "Civic Canvas", "Horizon") è una lettura progettuale. Da segnare come [I].
- [ ] **Sezioni 6.2 e 6.3.** Positional encoding e GAE sono descritti in modo generale. Il collegamento a progetti specifici non è verificato.

### URL delle fonti open access (sezione 8)

- [ ] Nessun URL è stato aperto. Da controllare uno per uno che siano raggiungibili e che il documento sia la fonte citata (Internet Archive, isnature.org, ASHBY PDF, Burks/von Neumann, DOI AMS, PNAS, Nature, MIT Press).
- [ ] Il PDF di Ashby indicato (pcp.vub.ac.be) non è stato verificato.
- [ ] Il link al testo di Burks (fab.cba.mit.edu) nelle Verifiche differisce da quello in sezione 8 dell'Atlante (cba.mit.edu). Da scegliere una sola fonte.

### Incoerenze interne tra Atlante e file del catalogo

- [ ] Nella sezione Nash del catalogo la frase "non-cooperative dichiarato nell'introduzione" è stata corretta: il termine è nel titolo. Controllare che l'Atlante non lo ripeta.
- [ ] Il Catalogo (sez. 6) segnala che la definizione di unit operation attribuita a Bogost tramite Sanchez coincide quasi con una formulazione scartata nella Cronistoria. L'Atlante la usa comunque. Da risolvere.
- [ ] Le formule delle analisi 29-33 sono ricostruzioni, non formule dei team. L'Atlante usa alcune di quelle formule come se fossero dei team. Da segnare.

## Prossimi passi proposti

1. Leggere le pagine di Ashby 1956 (121–126, 202–213) per chiudere le voci [L] più importanti.
2. Leggere Nash 1950 (PNAS) e chiarire Kakutani/Brouwer.
3. Aprire le URL della sezione 8 e segnare quelle non raggiungibili.
4. Decidere con Dennis se l'Atlante resta come testo di riferimento e in quale forma entra nel Report fondativo. Il testo resta suo: le correzioni vanno fatte in un file separato, non dentro l'Atlante.

## Esito della verifica del 2026-10-20

Verifica fatta su fonti raggiunte online. Le fonti non raggiunte sono segnate come tali. Il testo dell'Atlante non è stato modificato.

### Verificato o corretto

- **Nash 1950 (PNAS 36, pp. 48–49, "Equilibrium Points in n-Person Games").** Usa il teorema di Kakutani. L'Atlante lo dice correttamente. [V]
- **Nash 1951 ("Non-Cooperative Games").** Usa il teorema di Brouwer, non Kakutani. **Errore nell'Atlante**: sez. 4.1 dice "Nash (1950, 1951)" con Kakutani, quindi va riformulato. [V]
- **Tero et al. 2010.** Riferimento corretto: *Science* 327, 439 (2010), DOI 10.1126/science.1177894. Le equazioni (Q_ij, Kirchhoff, dD/dt) **non sono state verificate**: il materiale supplementare non le riporta e l'articolo non è stato letto. Resta [I] fino a verifica. [L]
- **Nowak & May 1992 (*Nature* 359, 826–829, "Evolutionary games and spatial chaos").** Riferimento corretto. Il testo della pagina Nature non riporta il punteggio "8 × R" né la descrizione dei cluster così come scritta nell'Atlante. Il risultato descritto nella pagina è la coesistenza persistente di cooperatori e difettori con proporzioni che fluttuano. La frase dell'Atlante sul salvataggio dall'estinzione va riscritta come interpretazione. [L, parziale]
- **Gray-Scott, valori F=0.030, k=0.062.** Non compaiono in Pearson 1993, che è la fonte standard per la mappa dei pattern. Il riferimento è da rimuovere o da sostituire con i valori della fonte. Lo schema ASCII dell'Atlante va trattato come illustrativo. [L]

### Non verificato (fonti non raggiunte)

- Tutti gli URL della sezione 8 dell'Atlante: archive.org, isnature.org, pcp.vub.ac.be, cba.mit.edu, DOI AMS, PNAS (pagina), archive.org DLI, Nature (articoli 163384a0 e 359826a0 in parte), MIT Press. Il proxy di questo ambiente ha bloccato le connessioni dirette (403) e le pagine non sono state lette. Da aprire a mano.
- PNAS 1950 via DOI: non letto (la pagina ha dato errore); letto il PDF di un'altra copia (vedi sopra).
- Bertalanffy 1950 *Science* ed equifinalità: non raggiunto.
- Ashby 1956, pp. 121–126 e 202–213: non raggiunte.
- Schelling, soglia τ = 0,33: ricerca fatta, nessuna fonte primaria letta. Resta [S].
- Axelrod, δ ≥ (T−R)/(T−P): non verificato.
- Percentuali (w)Ego (75/72/65/53%): fonte non trovata.
- Alexander 1964, min-cut e formula M(x): non trovati nel testo.

### Correzioni da fare nell'Atlante (da decidere con Dennis)

1. Sez. 4.1: Nash 1951 usa Brouwer, non Kakutani.
2. Sez. 8: aggiungere la fonte Tero 2010 con il riferimento *Science* 327, 439.
3. Sez. 1.3: togliere o marcare come non verificati i valori F=0.030, k=0.062 e l'elenco dei pattern.
4. Sez. 4.2 (Nowak & May): "8 × R" e la descrizione dei cluster vanno marcati come interpretazione.
