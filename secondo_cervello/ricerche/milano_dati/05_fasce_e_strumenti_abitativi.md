# 05 — Fasce di reddito e strumenti abitativi a Milano: soglie, domanda pubblica, ipotesi

Data: 2026-11-10. Stato: **nota di lavoro**, non capitolo di tesi. Figura e script in `fasce/`.
Marche: **[V]** = fonte ufficiale (o copia integrale di atto ufficiale) aperta in questa sessione, URL e data 10/11/2026; **[S]** = fonte secondaria (stampa, sindacati, aggregatori); **[I]** = inferenza/calcolo mio; **[H]** = ipotesi; **[L]** = noto da letteratura/memoria, non verificato qui.
Segue `02_mercato_e_accessibilita.md` e `03_pancia_della_gaussiana.md`; ne riusa le conversioni ISEE → reddito lordo (persona sola, dipendente, in affitto, patrimonio nullo: lordo ≈ ISEE + 10.000 sopra i 15k) [I].

---

## 0. Sintesi

- [V] Lo **svantaggio di priorità** della fascia "eleggibile ma non prioritaria" è scritto nel regolamento: nell'ISBAR la condizione economica vale **al massimo 6 punti** (formula `[(16.000 − ISEE)/16.000 × 4] + 2`, II adeguamento RR 4/2017), mentre singole condizioni familiari o abitative valgono 8-13 punti; il **20% degli alloggi va prima agli indigenti**; il punteggio per la residenza nel comune scatta solo se c'è almeno una condizione familiare o abitativa. Nel testo consultato **non esiste una condizione di "affitto oneroso"**: chi paga un canone di mercato insostenibile ma vive in un alloggio idoneo non prende punti per questo [V, ricerca nel testo; I].
- [S] Domanda contro offerta a Milano: **76.373 domande negli ultimi cinque bandi, 2.567 assegnazioni** (≈ 3,4%, [I]); **~16.000 nuclei in graduatoria per ~500 alloggi disponibili**; stock ALER + Comune sceso da **65.986 (2019) a 62.457** (L'Espresso, 29/7/2025, che cita SICET e SUNIA). [V] Il Comune di Milano possiede **26.010 alloggi SAP**; nella Città metropolitana di Milano le assegnazioni SAP 2022-2026 sono state **6.011** (Regione Lombardia, 25/6/2026).
- [V] La Regione definisce la **"fascia grigia"** (DGR XII/5248/2025) senza un tetto ISEE; il tetto compare negli strumenti: **housing sociale ISEE 14.000-40.000 €** (DGR XII/6209 del 25/5/2026), **valorizzazioni ALER/Comuni ISEE 12.000-40.000 €**. Il **Piano Casa Milano** (DG 365/2026) prende come riferimento i nuclei con **reddito netto di 1.500-2.500 €/mese** e fissa un **canone medio massimo di 90 €/m²/anno**, con vincolo ≥ 30 anni. Non fissa però una soglia ISEE: i requisiti sono rinviati ai bandi gestiti dall'operatore privato.
- [I] **Sovrapposizione formale SAP ∩ housing sociale: ISEE 14.000-16.000** (12.000-16.000 con le valorizzazioni). È la banda in cui un'offerta a costo/cooperativa potrebbe assorbire domanda ERP "senza speranza". Sotto ~ISEE 10-12k (povertà assoluta, ADI, indigenza) il canone di 90 €/m²/anno non è sostenibile (vedi §3): quella fascia la proposta non la serve.
- [H] Due ipotesi falsificabili in §4: **H1 decompressione** e **H2 creaming**.

---

## 1. Soglie (verificate sul testo dove indicato)

### 1.1 Povertà assoluta ISTAT
| Voce | Valore | Fonte |
|---|---|---|
| Soglia di povertà assoluta, adulto 30-59 anni che vive solo, **comune centro di area metropolitana della Lombardia**, 2025 | **1.256,37 €/mese** (spesa per consumi, non reddito) | ISTAT, *La povertà in Italia – Anno 2025*, Nota metodologica [V] https://www.istat.it/wp-content/uploads/2026/10/La-poverta-in-Italia-2025.pdf |
| Incidenza della povertà assoluta familiare, comuni centro di area metropolitana del Nord | **5,0% (2025)** contro **8,2% (2024)**; Nord-Ovest 4,2% contro 7,9% (variazione statisticamente significativa, Prospetto 1) | stesso documento [V] |
| Italia 2025 | 8,0% delle famiglie (2,1 mln), 9,3% delle persone | stesso documento e comunicato stampa [V] https://www.istat.it/comunicato-stampa/la-poverta-in-italia-anno-2025/ |
| Soglie per altri tipi di famiglia (coppia, coppia + figli, anziani) | **non estratte**: il calcolatore ISTAT (https://www.istat.it/dati/calcolatori/soglia-di-poverta/) è interattivo e non ha restituito dati in modo automatico | [L] lacuna |

- [S] Il valore 1.175,15 €/mese della nota 02 era di un anno precedente: la nota 02 va aggiornata a 1.256,37 (2025).
- [I] 1.256,37 × 12 = 15.076 €/anno di **spesa**; per un dipendente solo corrisponde a circa **17.800 € lordi** (`fasce.py`, netto approssimato). È solo un ordine di grandezza: la soglia è di consumo e contiene già una componente abitativa.

### 1.2 SAP/ERP in Lombardia (L.R. 16/2016, R.R. 4/2017 con il I e II adeguamento del 2025)
Fonte: Regione Lombardia, *Modifiche testo RR 4-2017, I-II adeguamento* (DGR XII/3974 del 3/3/2025; RR 2/2025) [V] https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/01-abitare-in-lombardia/red-normativa-in-materia-di-servizi-abitativi-pubblici/allegati/Modifiche%20testo%20RR%204-2017-I%20-%20II%20adeguamento.pdf

| Requisito | Testo vigente | Marca |
|---|---|---|
| Cittadinanza | cittadini UE, oppure stranieri titolari di permesso di lungo periodo (o equiparati dalla norma statale) | [V] art. 7 c. 1 lett. a |
| Residenza/lavoro | **residenza anagrafica o attività lavorativa in Lombardia**, senza durata minima (il requisito dei 5 anni della L.R. 16/2016 art. 22 c. 1 lett. b è stato dichiarato illegittimo da C. cost. 44/2020) | [V] art. 7 c. 1 lett. b; sentenza [S] (non riaperta) |
| ISEE | **≤ 16.000 €** | [V] art. 7 c. 1 lett. c |
| Patrimonio | 1 persona **22.000 €**; 2 o più persone: **16.000 + 5.000 × parametro della scala di equivalenza** (es. 2 persone, PSE 1,57 → 23.850 €) | [V] art. 7 c. 1 lett. c, punti 1-2 [I per l'esempio] |
| Proprietà | nessun alloggio adeguato | [V] art. 7 (estratto) |
| Esclusioni | decadenza o occupazione abusiva negli ultimi 5 anni | [V] art. 7 |
| Permanenza (decadenza) | ISEE fino a **35.000 €** | [V] art. 25 |
| Riserva indigenti | **20%** delle unità disponibili ai nuclei indigenti, assegnate per prime (art. 15 c. 1); il piano annuale può alzare la quota (art. 4 c. 3 lett. c) | [V] |
| Soglia di indigenza | ISEE ≤ **3.000 €** (la FAQ regionale lo cita a proposito degli alloggi "nello stato di fatto"); la definizione formale (L.R. 16/2016 art. 23 c. 3 / RR art. 13) non è stata riletta | [V parziale] FAQ https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/01-abitare-in-lombardia/red-normativa-in-materia-di-servizi-abitativi-pubblici/allegati/FAQ.pdf ; [S] definizione |
| Altre riserve | fino a un ulteriore **20%** per le categorie dell'art. 14 (anziani, disabili, forze di polizia, ecc.); nessuna gerarchia tra le riserve | [V] art. 4 c. 3 lett. c bis; art. 15 c. 1 ter |

**Come funziona l'ISBAR (indicatore della situazione di bisogno abitativo), Allegato 1** [V]:
- **Condizioni familiari**: es. anziani (punti 9-12), disabilità (fino a 13), famiglie di nuova formazione o monogenitoriali (8-10), genitore separato (8).
- **Condizioni abitative**: rilascio dell'alloggio per sfratto o provvedimento (8), abitazione impropria (4-8), alloggio antigienico o privo di servizi (3), barriere architettoniche, sovraffollamento e coabitazione (0,5-1,5). Sovraffollamento e coabitazione contano solo insieme ad almeno un'altra condizione.
- **Condizione economica**: `[(16.000 − ISEE)/16.000 × 4] + 2` → da **2 punti (ISEE 16.000) a 6 (ISEE 0)**; prima del II adeguamento era 0-4.
- **Residenza**: in regione 0,5 punti per anno fino a 6; nel comune 0,5 per anno fino a 6 (il prospetto è su due colonne, verificare i massimi sul testo coordinato), ma **quella comunale solo se c'è almeno una condizione familiare o abitativa** (escluse sovraffollamento e coabitazione).
- **A parità di punteggio**: prima la condizione familiare, poi quella abitativa, poi quella economica, infine la residenza.

[I] Conseguenza: un nucleo adulto con ISEE 12.000, in affitto sul mercato con un'incidenza del canone del 50%, senza sfratto, disabilità né anzianità, totalizza ~3 punti economici più al massimo 6 di residenza regionale. Un nucleo sfrattato con un anziano supera i 25. Con un rapporto domande/assegnazioni del 3-4% [S/I], **i primi restano strutturalmente fuori**: è la popolazione "eleggibile a bassa priorità" dell'ipotesi della tesi.

### 1.3 Servizi abitativi sociali / housing sociale ("fascia grigia")
| Strumento | Soglia | Fonte |
|---|---|---|
| Definizione "fascia grigia" | nuclei con capacità economica che "non consente né di sostenere un canone di locazione o un mutuo sul mercato abitativo privato né di accedere ad un servizio abitativo pubblico". **Nessun tetto ISEE nella DGR** | DGR XII/5248 del 3/11/2025, all., Linea 2, pp. 5-6 [V] https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/10-housing-sociale/red-housing-sociale/allegati/All_Delibera%205248%20del%2003_11_2025.pdf |
| DGR 5248, Linea 1 (offerta pubblica e privata) | canoni "riferiti ai valori minimi del canone concordato" (L. 431/98); 18 M€. Linea 2 (ALER): 7,5 M€. Linea 3 (privato sociale): 7 M€ | stesso [V] |
| **DGR XII/6209 del 25/5/2026** (criteri housing sociale, 96 M€ FESR/FSC) | destinatari **ISEE da 14.000 a 40.000 €**, con deroga solo per progetti rivolti a soggetti svantaggiati; vincolo ≥ 20 anni; contributo 700-900 €/m²; canone "calmierato o inferiore al mercato", ad esempio concordato: "Milano città, 60 m² da 650 € contro 1.200 € sul mercato" | Regione Lombardia, presentazione dell'Assessore Franco, 25/6/2026 [V, presentazione ufficiale su sito regionale; testo della DGR non letto] https://www.lombardianotizie.online/wp-content/uploads/2026/06/Presentazione-finale-Tour-con-dati-Milano-def.pdf |
| Valorizzazioni SAP → housing sociale | **ISEE 12.000-40.000 €** più categorie (anziani, disabili, vittime di violenza, sfrattati, studenti, forze dell'ordine, personale sociosanitario) | Regione, *Missione Lombardia – Stato di attuazione 2025* [V] https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/01-abitare-in-lombardia/red-normativa-in-materia-di-servizi-abitativi-pubblici/allegati/RL_MissioneLombardia_Opuscolo_Stato%20di%20attuazione_%202025.pdf |
| Stessa misura, nella presentazione 2026 | "ISEE < 40.000 €" | presentazione 25/6/2026 [V] |
| Bandi ALER "fascia grigia" Milano | ISEE 14.000-40.000; avviso comunale per 65 alloggi con ISEE max 40.000 | [S] (Affaritaliani, Milanofree; bandi originali non scaricati) |

**Disaccordo da segnalare**: il limite inferiore è 12.000 € (valorizzazioni, 2022-25) oppure 14.000 € (DGR 6209/2026). Si riportano entrambi.

### 1.4 Piano Casa Milano (Piano straordinario Casa Accessibile, ERSC)
Fonte: Comune di Milano, Direzione Casa, *Relazione tecnica* allegata alla proposta di DG n. 365 del 26/03/2026, copia conforme all'albo pretorio, firmata il 25/03/2026 [V, copia ripubblicata da Assolombarda] https://www.assolombarda.it/servizi/immobili-urbanistica-e-territorio/documenti/delg-365-2026_all1
- Bersaglio: "fascia di popolazione che ha redditi superiori rispetto ai limiti per l'accesso ai SAP, ma comunque non sufficienti per sostenere un canone in locazione nell'attuale mercato privato"; nuclei con **reddito netto di 1.500-2.500 €/mese** [V].
- **Canone medio massimo degli alloggi ERSC: 90 €/m²/anno** (era 80 nelle linee di indirizzo del 2024 [S]); vincolo ≥ **30 anni** con rivalutazione ISTAT; poi canone di mercato ridotto di almeno il 20%; diritto di superficie per 90 anni; compendi Ex Palasharp, San Romanello, Bovisasca [V].
- **Bando inquilini e graduatoria gestiti dall'operatore privato**, con requisiti soggettivi "dettagliati nei singoli bandi" [V]. → [I] **nessuna soglia ISEE né regola di priorità fissata a monte**: è il punto in cui il creaming (H2) può entrare.
- Delibere richiamate: DG 1299 del 24/10/2024 e DG 1236 del 9/10/2025 [V, citate]. Programma distinto "Casa ai lavoratori": DG 359 del 26/03/2026 [S, non letto].
- [I] 90 €/m²/anno × 50 m² = 375 €/mese; × 65 m² = 488 €/mese. Al 30% del netto servono 15.000-19.500 € netti/anno (1.250-1.625 €/mese): coerente con il limite inferiore di 1.500 €/mese.

### 1.5 Canone concordato (accordo territoriale di Milano)
- [S] Nel 2023 il Comune ha promosso un **nuovo accordo** con 5 zone omogenee al posto delle microzone, che convive con l'accordo precedente. SICET, Unione Inquilini e ASIA **non l'hanno firmato**: secondo loro il concordato aumenta "dal 36% al 148%" (comunicato SICET-UI-ASIA, 27/7/2023, https://cislmilano.it/… [S]). Fasce riportate da Idealista per il nuovo accordo (€/m²/anno): zona 1 100-310; zona 2 70-180; zona 3 60-170; zona 4 55-160; zona 5 50-130 [S, da verificare sul testo dell'accordo].
- [V] Esempio regionale: concordato a Milano, 60 m² ≈ 650 €/mese contro 1.200 € a mercato (presentazione 25/6/2026), cioè ≈ 130 €/m²/anno.
- [I] Il concordato **non ha requisiti di reddito**: è un'agevolazione fiscale al proprietario, non uno strumento mirato. 130 €/m²/anno è circa il 45% sopra il tetto del Piano Casa.
- Testo dell'accordo e tabelle: **non scaricati** (sito del Comune bloccato) → [L] lacuna.

### 1.6 Sostegno all'affitto e morosità incolpevole
- [V] **Sostegno al mantenimento dell'alloggio in locazione sul libero mercato, DGR 5855/2026**, avviso dell'Ambito di Lodi (stessa misura regionale, attuata dagli Ambiti): **ISEE ≤ 15.000 €**; morosità incolpevole iniziale, pensionati, giovani lavoratori ≤ 36 anni, mutuatari all'asta; nessuna procedura di rilascio in corso; residenza nell'alloggio da ≥ 6 mesi; contributo indicativo fino a **1.200 €** https://valera-fratta-api.municipiumapp.it/s3/7586/allegati/avviso-pubblico-dgr-5855_2026.pdf (copia comunale dell'avviso). L'avviso dell'Ambito di Milano non è stato letto: la soglia per Milano va confermata [L].
- [V] Uso a Milano 2022-2026: **9.844 inquilini del mercato privato** aiutati nella Città metropolitana (19,1 M€); contributo di solidarietà a **65.591 inquilini SAP** (72,7 M€) (presentazione 25/6/2026).
- [L] **Fondo nazionale per la morosità incolpevole** (DM 30/3/2016): ISEE ≤ 26.000 € o reddito ISE ≤ 35.000 €. Non verificato in sessione; una ricerca non ha trovato conferme recenti per la Lombardia.
- [L] Assegno di inclusione (D.L. 48/2023): ISEE ≤ 10.140 €. Non verificato.

### 1.7 Edilizia convenzionata (Milano)
- **Non verificato**: prezzi massimi di cessione e canoni della convenzionata a Milano (atti comunali; il sito del Comune è bloccato) → [L] lacuna, come nella nota 02. [S] Il "Piano Casa 2026" nazionale cita alloggi convenzionati per lavoratori (pmi.it, open.online): non letto.

### 1.8 DSU (studenti universitari, Lombardia)
- [V] **a.a. 2026/27** (DGR XII/6298/2026, all. A): **ISEE universitario ≤ 26.887,93 €**, **ISPE ≤ 58.452,06 €**; fasce 0-13.443,97 / 13.443,98-17.925,29 / 17.925,30-26.887,93 (limiti del D.D. MUR 176 del 10/2/2026) https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/03-istruzione-formazione-e-lavoro/06-universita-e-formazione-accademica/red-borse-di-studio-universitarie/allegati/DGR%206298%20Criteri%20e%20linee%20di%20finanziamento%20borse%20di%20studio%202026%202027.pdf
- [V] **a.a. 2025/26** (bando Milano-Bicocca): ISEE ≤ 26.516,70 €, ISPE ≤ 57.645,03 € https://www.unimib.it/sites/default/files/2025-07/bando-DSU-2025-26%20%281%29_0.pdf
- [I] L'ISEE è quello del **nucleo d'origine**: lo studente fuori sede è una popolazione distinta dalla fascia grigia residente, anche se si sovrappone sulla figura.

---

## 2. La domanda sulla casa pubblica a Milano

| Grandezza | Valore | Fonte |
|---|---|---|
| Alloggi SAP di proprietà del **Comune di Milano** (gestione MM) | **26.010** | presentazione Regione 25/6/2026 [V] |
| Alloggi SAP ALER nella **Città metropolitana** | 53.137 (95.677 in Lombardia); più 2.823 alloggi comunali gestiti da ALER nella CM | stessa [V] |
| ALER + Comune **nel Comune di Milano** | **62.457** (65.986 nel 2019) → ALER in città ≈ 36.400 [I = 62.457 − 26.010] | L'Espresso 29/7/2025 [S] |
| ALER Milano, patrimonio complessivo | ~70.000 alloggi (città e provincia) | Il Sole 24 Ore [S] |
| Sfitti | ERP vuoti a Milano: **11%** (9% nel 2014, 4% nel 2019) | L'Espresso, citando i sindacati [S] |
| Domande e assegnazioni | **76.373 domande negli ultimi 5 bandi contro 2.567 assegnazioni** (≈ 3,4%) | SICET, in L'Espresso [S]; rapporto [I] |
| Graduatoria | **~16.000 persone in graduatoria per ~500 alloggi** | SUNIA, in L'Espresso [S] |
| Offerta programmata 2026 (Comune + ALER) | **2.321 unità** nel Piano annuale dell'offerta | Affaritaliani [S] (atto non letto) |
| Programmato contro assegnato (2023, Comune) | 136 alloggi messi a bando su 480 previsti dal piano annuale | comunicato SICET-UI-ASIA 27/7/2023 [S] |
| Ultimo avviso letto | Avviso 13542: **118 alloggi "nello stato di fatto"** (Comune + ALER), 2/7-16/9/2026, ISEE ≤ 16.000 | Affaritaliani 6/7/2026 [S] |
| Assegnazioni SAP, CM Milano | **6.011 nel 2022-2026** (≈ 1.300/anno [I]) | presentazione 25/6/2026 [V] |
| Assegnazioni SAP, Lombardia | 2021: 1.563; 2022: 3.519; 2023: 3.208; 2024: 3.421; 2025 (al 31/10): 2.763 | opuscolo *Stato di attuazione 2025* [V] |
| Housing sociale messo a disposizione | 2.030 alloggi in Lombardia (ISEE < 40.000), di cui **1.112 ALER Milano e 372 Comune di Milano** | presentazione 25/6/2026 [V] |
| Interruzione | 21/2-1/4/2025: avvisi SAP sospesi per l'esecuzione della sentenza 1481/2025 | opuscolo 2025 [V] |
| Composizione delle domande per fascia ISEE | **non trovata** | lacuna: richiesta di accesso civico a Regione (piattaforma SAP) e Comune (cfr. nota 04) |

[I] Ordini di grandezza: stock ~62.000 alloggi; flusso di assegnazioni nel solo Comune nell'ordine di **qualche centinaio fino a ~1.000-1.500 l'anno** (stima incerta, fonti non omogenee); domande per avviso nell'ordine di **~15.000** (76.373/5). Turnover ≈ 2% dello stock l'anno.

---

## 3. Mappa delle categorie (Milano)

Soglie in reddito lordo per **persona sola in affitto** (`fasce.py`); per nuclei più grandi le soglie salgono (es. 3 persone con due redditi: soglia ERP ≈ 45.600 € lordi complessivi, nota 03) [I]. Le quote sono di **contribuenti**, non di famiglie (limite principale, nota 03 §5).

| # | Fascia | ISEE / reddito | Strumento | Chi gestisce | Ordine di grandezza (Milano) | La proposta della tesi? |
|---|---|---|---|---|---|---|
| A | Povertà assoluta, marginalità | spesa < 1.256 €/mese (single) [V]; ISEE ≤ 3.000 (indigenza); ADI ≤ 10.140 [L] | SAP con riserva del 20% agli indigenti, servizi abitativi transitori, ADI, servizi sociali | Comune/MM, ALER, Regione, INPS | **~39.000-64.000 famiglie** [I: incidenza 5,0-8,2% dei comuni centro AM del Nord × 780.935 famiglie, nota 02] | **No**: 90 €/m²/anno = 375-490 €/mese per 50-65 m², oltre il 30% di un reddito alla soglia di povertà; servono canone sociale e accompagnamento [I] |
| B | ERP ad alta priorità | ISEE ≤ 16.000 con condizioni familiari o abitative (sfratto, disabilità, anziani) | SAP (assegnazione) | ALER Milano, MM Casa | quota delle ~1.000-1.500 assegnazioni/anno [I/S] | No (vanno serviti dal SAP) |
| C | **ERP eleggibile a bassa priorità** | ISEE ~8.000-16.000, nucleo adulto senza condizioni ISBAR, spesso in affitto oneroso | formalmente SAP; di fatto mercato, sostegno affitto (ISEE ≤ 15.000), concordato | Regione/Ambiti; proprietari privati | **~10.000-15.000 nuclei** [I/H: chi resta in graduatoria (16.000 [S]) meno chi ha condizioni di priorità; da verificare con microdati SAP] | **Sì, parzialmente**: sopra ~ISEE 10-12k un canone a costo di 90 €/m²/anno è sostenibile al 30% per nuclei di 1-2 persone [I, nota 02 §3.5: Piano Casa sostenibile dal P24-P44 a seconda del nucleo] |
| D | **Sovrapposizione formale** | ISEE 14.000-16.000 (12.000-16.000 per le valorizzazioni) | SAP **e** housing sociale DGR 6209 | ALER, cooperative, privati | sottoinsieme di C | **Bersaglio della decompressione (H1)** |
| E | Fascia grigia / pancia | ISEE 16.000-40.000; netto 1.500-2.500 €/mese | housing sociale (SAS), Piano Casa ERSC, valorizzazioni, concordato; permanenza ERP fino a ISEE 35.000 per chi è già dentro | ALER, Comune/MM, operatori privati, cooperative | 27-40% dei contribuenti (245-410 mila persone, nota 03); offerta dedicata: ~1.500 alloggi (ALER + Comune, 2022-26) [V] + Piano Casa 10.000 in 10 anni [S] | **Sì, è il bersaglio dichiarato**; è anche il luogo del creaming (H2) |
| F | Studenti | ISEE del nucleo d'origine ≤ 26.888 (2026/27) | DSU: borse e posti letto | università, ISU | non stimato | Possibile, ma è un'altra popolazione (temporanea) |
| G | Mercato | lordo > ~48k (30% del lordo) o > ~81k (30% del netto) | mercato libero, acquisto | privati | 10-23% dei contribuenti | No |

Figura: `fasce/fig_fasce_strumenti.png|.svg`. Il pannello superiore mostra la distribuzione Dagum dei redditi MEF 2024 su scala logaritmica, divisa in zone. Quello inferiore riporta le barre degli strumenti sull'asse del reddito, con la banda di sovrapposizione ISEE 14-16k evidenziata. Avvertenza in figura: il 35% sotto ~18k lordi sono **redditi individuali** (part-time, secondi percettori, pensioni), **non famiglie povere**.

---

## 4. Due ipotesi falsificabili

**H1, decompressione.** *Un'offerta stabile a costo/cooperativa con canone ≤ 90 €/m²/anno, aperta alla banda ISEE ~10-16k (inclusa la sovrapposizione 14-16k), riduce la domanda SAP effettiva senza ridurre l'accesso dei più poveri.*
- Metriche: (a) quota degli assegnatari della proposta che erano **in graduatoria SAP** al momento dell'ingresso (dal registro della piattaforma regionale, con consenso); (b) **uscite dalla graduatoria** per rinuncia o sistemazione alternativa, confrontate con comuni o ambiti di controllo (difference-in-differences); (c) variazione del **rapporto domande/alloggi** nei bandi successivi; (d) tempo di attesa mediano dei nuclei nelle fasce A-B.
- Falsificata se: (a) < 20% [H, soglia da pre-registrare], oppure nessuna differenza in (b) e (c) rispetto al controllo, oppure peggiora (d).
- Rischio di confondimento: l'offerta di alloggi può generare domanda nuova (induced demand), cioè nuclei che prima non facevano domanda.

**H2, creaming.** *Se l'operatore seleziona gli inquilini (come prevede la DG 365/2026), la popolazione servita si concentra sul limite alto (ISEE 30-40k, netto vicino a 2.500 €/mese, contratti stabili). La banda C resta scoperta e il SAP concentra i casi più difficili.*
- Metriche: (a) **distribuzione ISEE degli ingressi** contro la distribuzione dei candidati e contro la banda eleggibile (indice di dissimilarità; quota sotto ISEE 16k); (b) quota di contratti di lavoro precari o monoreddito tra gli ingressi; (c) **tasso di rifiuto** per fascia ISEE; (d) nel SAP: quota degli assegnatari con ISEE ≤ 3.000 e dei nuclei con fragilità, prima e dopo.
- Falsificata se gli ingressi sotto ISEE 16k sono ≥ la loro quota tra i candidati e il tasso di rifiuto non cresce al diminuire dell'ISEE.
- Contromisura da testare nel modello di allocazione della tesi (DECISIONI 2026-11-10: accettazione differita con **riserve di capacità per categoria**): riserva minima per la banda C/D, che diventa un parametro del confronto B0-B6.

---

## 5. Limiti e lacune
1. **Contribuente ≠ famiglia**, lordo ≠ disponibile, patrimonio ignorato (nota 03 §5). Le conversioni ISEE → lordo valgono solo per la persona sola in affitto.
2. **Composizione delle graduatorie SAP di Milano per fascia ISEE: non disponibile.** È il dato decisivo per H1: chiederlo con accesso civico alla Regione (piattaforma SAP) e al Comune/MM (vedi nota 04).
3. Numeri su stock, sfitti e domande del Comune di Milano: solo [S] (sindacati via stampa). Servono il Piano annuale 2026, la relazione MM Casa e il bilancio ALER 2025.
4. Non letti: testo integrale della DGR 6209/2026 (solo la presentazione), accordo territoriale del concordato, avviso di Milano per il sostegno affitto, atti sulla convenzionata, soglie ISTAT per altri tipi di famiglia, DM sulla morosità incolpevole, ADI.
5. Il calo dell'incidenza della povertà nei comuni centro AM del Nord (8,2% → 5,0%) è una stima campionaria con intervalli ampi: per Milano usare l'intervallo, non il punto.

## Fonti aperte in questa sessione (10/11/2026)
- RR 4/2017, I-II adeguamento (Regione Lombardia) [V]; FAQ SAP Regione [V]
- DGR XII/5248/2025 all. [V]; opuscolo *Missione Lombardia – Stato di attuazione 2025* [V]; presentazione *Affordable housing*, Ass. Franco, 25/6/2026 (lombardianotizie.online) [V]
- Comune di Milano, relazione tecnica allegata alla DG 365/2026 (copia Assolombarda) [V]
- ISTAT, *La povertà in Italia – Anno 2025* (PDF e comunicato) [V]
- DGR XII/6298/2026 (DSU 2026/27) [V]; bando DSU Milano-Bicocca 2025/26 [V]
- Avviso DGR 5855/2026, Ambito di Lodi [V, copia comunale]
- L'Espresso 29/7/2025; Affaritaliani 6/7/2026 e guida bando 2026; comunicato SICET-UI-ASIA 27/7/2023; Idealista (concordato); Il Sole 24 Ore (ALER) [S]
- Non raggiunti: comune.milano.it (blocca le richieste automatiche, non aggirato); normelombardia (richiesta respinta).
