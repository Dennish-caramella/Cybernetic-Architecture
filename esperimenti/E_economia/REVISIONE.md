# §7 Revisione indipendente — Base E v1 (ticket #19)

Revisore metodologico, 22/11/2026. Non ho eseguito la prova. Sono un'altra istanza dello stesso sistema dell'esecutore: **non è una verifica fatta da persone** [I]. Ho rieseguito `run.py` e i test in una copia nello scratchpad della sessione, con la cache e la Base L del repo collegate in sola lettura. Gli script di controllo sono fuori dal repo; l'appendice riporta le formule usate perché i controlli si possano rifare. Nel repo non ho modificato nulla oltre a questo file.

**Esito proposto: RIPETI** (pre-registrazione v2, stesso motore). Il motore è corretto e riproducibile, e per la regola pre-registrata E1–E4 passano. Però tre difetti gravi (G1–G3) rendono non sostenuti, così come sono scritti, i risultati che il REPORT passa alla tesi, cioè le quote della cooperativa a 90 anni, i conteggi dei lotti e l'acquisto per fascia. Per il protocollo un difetto grave comporta l'arresto: si apre un ticket e si decide con Dennis.

## 7.1 Riproduzione e cronologia [V]
- SHA-256 di `esecuzioni/00_preregistrazione.txt` = `ce059fd6…c065`. Coincide con il file `.sha256`, con la costante in `run.py` e con il commit b3b0df6. Il file non è cambiato da b3b0df6 a HEAD (`git diff --quiet`).
- Cronologia: b3b0df6 alle 21:19:35Z (pre-registrazione); poi be00262 (solo Base P); poi 0ce868d alle 21:36:21Z, il primo commit che contiene `run.py`, i test e le tabelle. I file OMI nella cache hanno data di modifica dalle 21:20:04Z in poi, cioè dopo il commit della pre-registrazione. Nessun indizio di esecuzioni precedenti. Le date di modifica sono una prova debole e l'ordine interno del registro (punto 8 scritto "prima" del punto 10) non si può verificare, perché tutto sta in un solo commit [L].
- **E1 si riproduce**: la terza esecuzione, la mia, dà l'hash di contenuto `11e200fb…767e`, identico al registro. Θ_cal = 5.671; T1 433/433; E3 vero. Anche `fig/mappe_2d.png` è identica byte per byte.
- **E2**: `test_economia.py --reali` passa per intero (T4, T5, T6, T7, T8, ann, reali).
- `esito_criteri.json` nel repo **non è l'uscita dello script**: contiene campi aggiunti a mano (`E1_hash_contenuto`, `E2`, `E5`, `E6_eleggibili`, `E6_scatta`) che `run.py` non scrive. I valori calcolati coincidono (diff vuoto sul resto). Vedi m1.
- L'hash del PDF della DG 365 (copia Assolombarda) è `51ee24ae…`, identico a F1. Il testo estratto conferma le cifre usate: 90 €/m²/anno come canone medio massimo; vincolo minimo 30 anni con ISTAT, poi canone di mercato ridotto di almeno il 20%; diritto di superficie di 90 anni a 1 €/m²; ST 18.120 / 7.200 / 1.838 m²; ERSC 10.872 / 4.320 / 1.103; SAP 1.812; funzioni libere al massimo 7.248 / 2.880 / 735; bonifiche 3,8–8,6 M€ e 0,75–1,5 M€ con alea divisa al 50% e tetti 6,2 e 1,6 M€; demolizione fino a 3,15 M€. La relazione dice che la sostenibilità è stata "preliminarmente valutata" con un PEF non pubblicato, con supporto metodologico della Bocconi, anche per "individuare le eventuali misure … finalizzate all'eventuale riequilibrio del PEF" [V].

## 7.2 Ricalcolo a mano di un lotto [V/I]
Lotto E00173 (rappresentativo della fascia E, zona E5): area 5.308,3 m², FAR 1, SL 5.308,3 m² (sotto 10.000, quindi s_ERS = 0), p_mid 3.350 €/m². Punto centrale pre-registrato.
- Costi per m² di SL. Oneri O = 100·3 + 0,075·484,78 = 336,36. Costo totale C_tot = 2.000·1,12 + 336,36 = 2.576,36.
- Developer. GDV = 0,85·3.350 = 2.847,5. Interessi F = 0,06·0,6·2.576,36·3/2 = 139,12. Residuo R = 2.847,5·(1 − 0,03 − 0,15) − 2.576,36 − 139,12 = −380,53. Fattore K = 1,09·1,06³ = 1,29821. **VRA = −293,1 €/m²**, quindi L_mkt = 0.
- Cooperativa (c₀ = 90, T = 60). Tasso r = 0,7·4% + 0,3·1,5% = 3,25%; g = 2%. NOI₁ = 0,85·90·(0,96 − 0,20) − 0,008·2.000 = 42,14. Annualità Σ = (1 − (1,02/1,0325)⁶⁰)/(0,0125) = 41,48. Valore attuale VA = 42,14·41,48/1,0325³ = 1.588,0. Costo C_tot·(1 + 0,0325·1,5) = 2.702,0. **L\* = −1.114 €/m²**.
- **ΔL^(acq) = ΔL^(ces) = 1.114 €/m² di lotto** (5,91 M€). Canone di pareggio con suolo gratuito: c\* = 3.304,9/24,344 = **135,8 €/m²/anno** a 60 anni; con lo stesso calcolo, **111,2** a 90 anni.
- Con le funzioni del motore al punto centrale ottengo L\* −1.113,95, c\* 135,76 e 111,19. Le formule di §4.2–4.4 sono implementate come pre-registrate: RICS con margine sul ricavo, T5 verificato; DCF con annualità crescente, corretta in forma chiusa anche per r ≠ g; ΔL = L^(k) − L\*. La mediana su Θ_cal riportata in tabella (ΔL^(ces) 635, c\* 111,41 e 86,62) è coerente con lo spostamento della taratura verso parametri favorevoli.
- **Costi e oneri condivisi**: sì. Una sola funzione `costs()` serve i due regimi, con gli stessi oneri e nessuna esenzione per la convenzionata, come pre-registrato. Due asimmetrie non dichiarate, entrambe minori (m6): in acquisto la cooperativa non paga τ sul suolo, mentre il developer lo sconta nel VRA; il finanziamento è diverso per costruzione (i_c e λ_c contro r), e questo è legittimo.

## 7.3 Rispetto della pre-registrazione
- Intervalli, centrali, soglie, seme, N e criteri sono uguali alla pre-registrazione [V, `P` in `run.py` contro §5].
- **Deviazione di processo**: §13.1 chiedeva a Dennis di confermare H1–H9 *prima* dell'esecuzione. Le ha accettate il coordinatore, "provvisoriamente" (DECISIONI 22/11). È dichiarato, ma resta un passo saltato, come già nella Base L v7 e nella Base P.
- **Scelte del registro 8** (silenzi della pre-registrazione). Tre hanno peso sull'esito.
  - (8a) Nell'operatore K1 le funzioni libere sono senza margine π_R: rende K1 più facile.
  - (8a) Bonifica a carico dell'operatore = 0,5·(max − min), cioè il caso peggiore e non l'atteso: rende K1 più difficile.
  - (8e) Definizione operativa di "vincolato dalla taratura" (KS > 0,10) e classificazione "con ancora" di i_c, i_D, i_E, ω. La pre-registrazione marca questi parametri [H], con il BTP solo come pavimento. Questa regola decide chi entra in E6 (vedi G2).
- **Analisi pre-registrate non eseguite e non dichiarate come omesse** (C5): PRCC (§7c); quantili 5–95% di VRA, L\* e c\* (§7b, c'è solo la mediana); tornado sui tre lotti rappresentativi (§7a, fatto solo sull'insieme); sintesi per proprietà (§7f); ΔL nella variante D1 (c'è solo VRA_D1); scenari di bonifica 200 e 500 €/m² (§5); DCF del developer come verifica di robustezza (§4.2).

## 7.4 Difetti gravi

**G1 — La regione tarata vive dove r ≈ g, e la lettura "a 90 anni regge" dipende da lì.**
Prova [V, ricalcolo su Θ con seme 4519]:
- Nel cubo r ≤ g solo nell'8,9% dei punti; in Θ_cal nel **27,8%**.
- In Θ_cal la mediana di r − g è **0,39 punti percentuali**, e il 57% dei punti ha r − g < 0,5 punti.
- Il punto base del tornado (mediana delle marginali di Θ_cal) ha r = 2,54% e g = 2,41%: r − g = 0,13 punti.
- Il motivo è nel K1. Al punto centrale la voce più grande del VAN dell'operatore è il canone di mercato degli anni 31–90: Ex Palasharp 24,7 M€, contro 14,1 M€ per gli anni 1–30 e 20,9 M€ per le funzioni libere. K1 si soddisfa quindi soprattutto rendendo quasi nullo lo sconto reale su un orizzonte di 90 anni. Se dopo i 30 anni il canone restasse a 90 indicizzato, Θ_cal scenderebbe da 5.671 a 2.518 punti.

Conseguenza: la quota della cooperativa in cessione (c₀ = 90, T = 90) è 0,589 su Θ_cal; 0,492 escludendo r ≤ g; 0,362 con r − g ≥ 0,5 punti. Poiché il lato cooperativa non dipende dalla zona, la quota è **identica per tutti i 216 lotti**, e il conteggio del REPORT ("216 su 216 lotti in cessione a 90 anni") passa da **216 a 0** appena la quota scende sotto 0,5. Non è un'informazione per lotto: è un solo numero sul filo della soglia.
Il motore ammette r < g per 90 anni (perpetuità divergente, tassi nominali fissi per 90 anni). È un difetto di specificazione, non di codice.
Correzione: nella v2, (a) riportare tutte le quote stratificate per r − g (≤ 0; 0–0,5; 0,5–1; > 1 punto); (b) dichiarare come regola v2 un vincolo minimo su r − g, con fonte su tassi reali di lungo periodo, oppure esprimere il modello in termini reali. È una correzione decisa dopo aver visto i dati e va registrata come tale; (c) togliere i conteggi di lotti per il lato cooperativa in cessione, dove sono degeneri.

**G2 — E6 è verificato solo nel punto in cui non può scattare.**
Il tornado di E6 è calcolato a c₀ = 90 e T = 60, dove al punto base 0 lotti su 216 reggono in acquisto: il punto base è lontano dal confine e i segni cambiano poco (massimo eleggibile 0,389). La pre-registrazione non fissa né c₀ né T. Ho rifatto lo stesso tornado [V] negli altri punti della griglia.

| T | c₀ | parametri sopra 0,90 | eleggibili (D, q) | g, δ |
|---|---|---|---|---|
| 90 | 90 | g e i_D 0,94; δ e i_E 0,93; c_new 0,91 | D 0,495; q 0,449 (appena sotto 0,50) | 0,94 e 0,93 |
| 60 | 110 | g e i_D 0,91 | — | g 0,91 |

g e δ sono "senza fonte" anche per l'elenco del registro 8e, e restano fuori da E6 solo per la regola KS > 0,10, scritta dopo la pre-registrazione. A T = 60 e c₀ = 90 la regola KS non cambia l'esito (g 0,426 < 0,5). Nel punto su cui il REPORT fonda la lettura per la tesi (90 anni), invece, la regione non è robusta: un parametro [H] senza fonte rovescia il segno nel 94% dei lotti.
Un vincolo di segno che sposta la marginale (KS 0,24) restringe g, ma non lo identifica.
Correzione: nella v2, E6 su tutta la griglia c₀ × T che il REPORT usa, con l'elenco dei parametri senza fonte preso dalle marche della pre-registrazione e non dal KS. Se E6 scatta a T = 90, l'esito è "cambia" per quella parte (servono dati su g e δ).

**G3 — Nel ramo developer il suolo in periferia vale zero, contro l'unico prezzo osservato; l'acquisto in fascia D/E è un artefatto.**
Prova [V]:
- VRA mediano per fascia (FAR 1, €/m² di SL): B 3.220, C 1.260, **D 198, E −467**; VRA ≤ 0 nel 39% dei lotti.
- In fascia E quindi L_mkt = 0, e "acquisto" coincide con "cessione". Per E00173, a T = 60, la quota è 0,108 in acquisto e 0,114 in cessione. Le cifre del REPORT "acquisto E 0,11" e "acquisto E 0,58 a 90 anni" misurano la cessione.
- L'asta comunale del 2023 (678 €/m² di SL, [S], Il Giorno) riguarda, secondo `casi_taratura.csv`, diritti che "atterrano in aree di rigenerazione della fascia esterna": proprio dove il modello dà suolo a valore zero o negativo.
- Basta un premio del nuovo del **20% su p_z** per portare il VRA mediano D/E da 189 a **634 €/m²** (con il 40%: 1.079) [V]. La spiegazione più semplice [I] è che il "punto medio OTTIMO" di OMI (stock usato) sottostimi il prezzo del nuovo. Questo tocca solo il developer, quindi ΔL^(acq) è sottostimato e la cessione non cambia.
- Un dato dice che i costi condivisi non sono la causa principale: il costo per alloggio del modello (circa 192 k€ senza oneri) è dell'ordine del piano Legacoop (230 k€, [V] secondo `casi_taratura.csv`). Però K2(b) dà un rapporto modello/SACC di 1,59–1,69: non si può escludere che una parte dello scarto venga dai costi, che pesano anche sulla cooperativa [I].
- Con un suolo a 678 €/m² di SL la cooperativa regge (c₀ = 90, T = 90) solo nel 25% di Θ_cal, e nel 4% con r − g ≥ 0,5 punti [V].

Correzione: nella v2, il prezzo del nuovo con un premio dichiarato e un intervallo, cercando una fonte (prezzi del nuovo per zona OMI, annunci o rogiti). In alternativa, nella v1, marcare l'acquisto nelle fasce D/E come "non informativo: L_mkt = 0 per costruzione".

## 7.5 Da correggere (non fatali)
- **C1. VF = 0 in acquisto decide il confronto tra regimi.** Al punto base, con VF = NOI_{T+1}/y_exit, l'acquisto regge in **149 lotti su 216** a T = 60, contro 0 [V, `informativi.varianti_punto_base`]. VF = 0 è conservativo e pre-registrato, ma ignora che in acquisto il suolo resta alla cooperativa. "Regge solo con suolo ceduto" vale quindi *con VF = 0*. Riportare almeno uno scenario con il valore finale del solo suolo.
- **C2. La durata T non è un parametro ma una decisione, e il suo "dominio" è in parte meccanico.** Con VF = 0 un orizzonte di 30 anni obbliga ad ammortizzare tutto l'edificio in 30 anni: "a 30 anni circa 0" segue dalla costruzione. L'89% di lotti che cambiano segno tra 30 e 90 anni va letto così. Riportare c\* per T e regime come risultato principale, che è più robusto della quota.
- **C3. La taratura K1 è un'asserzione del proponente.** K1 si basa su una dichiarazione del Comune sul proprio PEF, non pubblicato e "da riequilibrare". Il primo giro del Piano Casa ha avuto un solo progetto conforme su 24 [S, Il Sole 24 Ore]. Il segno del vincolo potrebbe essere sbagliato, e va in una direzione nota: sposta Θ verso costi e tassi bassi, cioè verso la cooperativa. Ricalcolare K1 come misura appena escono gli esiti dei bandi (pre-registrazione 6.1); se i bandi vanno deserti, il vincolo si rovescia.
- **C4. Il lato cooperativa non dipende dalla posizione.** c₀ è uguale ovunque e non c'è un canone legato al luogo, quindi cessione e diritto di superficie danno la stessa quota per ogni lotto edificabile. Va scritto in testa alle tabelle, perché i conteggi per fascia non vanno letti come geografia.
- **C5. Analisi pre-registrate mancanti** (elenco in 7.3): eseguirle oppure dichiararle omesse nel REPORT §6.
- **C6. η.** La scelta è dichiarata nella pre-registrazione (§0) e committata prima dell'esecuzione. Non è quindi post hoc rispetto ai risultati del motore, ma è stata presa conoscendo l'ordine di grandezza degli input [V]. Conta soprattutto l'intervallo 0,75–0,95, perché il Monte Carlo campiona su tutto l'intervallo. Effetti:
  - η alto favorisce la cooperativa: nel tornado ΔL mediano va da 670 (η = 0,75) a 479 (η = 0,95).
  - Con η = 0,70, Θ_cal scende a 1.995 e la cessione a T = 60 a 0,039.
  - Il confronto con lo 0,70 della Base L è improprio: quello è il rapporto tra superficie utile e SL per contare gli alloggi, non la superficie commerciale [I]. La coerenza va comunque dichiarata: ogni alloggio da 80 m² della Base L corrisponde a 0,85/0,70·80 ≈ 97 m² commerciali, cioè 729 €/mese a 90 €/m²/anno. Il confronto con c_sost (50–85 m² per nucleo) deve usare la stessa superficie.
  - η richiede una fonte: la definizione di SL nel PGT 2030 contro il DPR 138/1998.
- **C7. Lotti da riusare.** "Con il recupero la cooperativa regge nel 64% della regione" dipende quasi solo da ρ, che è [H] senza fonte, KS 0,01 e fuori da E6, che copre solo i lotti edificabili: la quota è 0,99 per ρ < 0,70 e 0,26 per ρ > 0,85 [V]. Estendere E6 ai lotti da riusare, oppure dichiarare la quota non robusta.

## 7.6 Minori
- **m1.** `esito_criteri.json` è stato completato a mano: spostare E1, E2, E5 ed E6_eleggibili nello script, perché il file sia un'uscita riproducibile.
- **m2.** E3 è una tautologia: l'intervallo di p_z è costruito dai valori OMI. T7 controlla la struttura del codice (stessa funzione), non uguaglianze tra i due regimi.
- **m3.** In `informativi` la variante VF, etichettata "solo acquisto", è applicata anche alla cessione (216/216): nella cessione e nel diritto di superficie VF deve valere 0.
- **m4.** K1 tratta la "superficie convenzionale" della DG come SL e la moltiplica per η. Se la superficie convenzionale coincide già con quella locabile, i ricavi ERSC sono sottostimati del 15% e K1 diventa più severo del dovuto [L].
- **m5.** Bonifica dell'operatore K1 al caso peggiore 0,5·(max − min) invece dell'atteso; funzioni libere senza margine. Le due scelte vanno in direzioni opposte e nessuna delle due ha una sensibilità.
- **m6.** In acquisto la cooperativa non paga τ sul suolo. Effetto nullo sui conteggi a T = 90 e c₀ = 90 (85 contro 85) [V]; va comunque corretto per coerenza con il "stessi costi".
- **m7.** Il ticket chiede "entro quale errore" il motore riproduce i casi reali. La risposta, da scrivere esplicitamente, è: **errore non misurato** (E5 non applicabile).

## 7.7 Le conclusioni sono sostenute?
- *"A 90 €/m²/anno e 60 anni la cooperativa non paga il suolo di mercato"*: **sostenuta nella direzione**. Vale anche in una regione già spostata a favore della cooperativa, e la sottostima del suolo (G3) la rafforza. Condizione: VF = 0 (C1).
- *"Regge con suolo ceduto e 90 anni"*: **non sostenuta così**. È circa metà della regione (0,59), sul filo della soglia, e dipende da r − g ≈ 0 (G1) e da parametri senza fonte che a T = 90 rovesciano il segno (G2). Formulazione difendibile [I]: "a 90 anni e con suolo ceduto il canone a costo di 90 €/m² regge in circa metà della regione tarata, solo se il costo del capitale supera di poco l'indicizzazione dei canoni".
- *Il canone di pareggio con suolo gratuito* (mediane 111 a 60 anni e 87 a 90 anni; 136 e 111 al punto centrale non tarato) è l'uscita più informativa e meno fragile, e va portata avanti con la sua forbice.
- *"O con sussidi incrociati come nel Piano Casa"*: è vera in parte per costruzione, perché la regione è tarata proprio perché l'operazione con funzioni libere e canoni di mercato dopo 30 anni stia in pari. Non è una scoperta indipendente.

## 7.8 Rischi per le prove successive
- **A3 fattibilità.** Se usa `quota_cal ≥ 0,5`, eredita tre problemi: indicatori di cessione identici per tutti i lotti (nessuna discriminazione), acquisto in fascia E uguale alla cessione, esiti decisi da T e VF. Deve lavorare per c\* e ΔL con la forbice, stratificati per r − g, non per conteggi.
- **B0–B6.** Usare un indicatore di fattibilità della Base E come vincolo o come costo del lotto **spinge verso la periferia**: il suolo vale zero proprio dove G3 dice che è sottostimato. È uguale per tutti i metodi, quindi non falsa il confronto tra metodi, ma falsa ogni affermazione assoluta su dove "regge". Raccomando che B0–B6 non usino la Base E v1 come vincolo.
- **Sintesi.** La frase del §8 non va usata senza le condizioni di 7.7. Le quote sono quote del cubo e non probabilità, e la base non ha un errore di taratura misurato.

## 7.9 Condizioni per congelare (v2 o v1 con riserva)
1. Quote e c\* stratificati per r − g, ed eventuale vincolo su r − g dichiarato come correzione post hoc in una pre-registrazione v2 con hash, committata prima di rieseguire (G1).
2. E6 su tutta la griglia c₀ × T usata nel REPORT e sui lotti da riusare, con l'elenco dei parametri senza fonte preso dalle marche [H] della pre-registrazione (G2, C7).
3. Premio del nuovo su p_z con fonte, oppure acquisto D/E marcato "non informativo" in tutte le tabelle (G3).
4. Uno scenario con VF del suolo in acquisto (C1); analisi mancanti eseguite o dichiarate (C5); JSON prodotto dallo script (m1).
5. Conferma di Dennis su H1–H9 (e su η con fonte), registrata in `tesi/DECISIONI.md`.
6. REPORT §4, §6 e §8 riscritti con le formulazioni di 7.7; "errore non misurato" scritto in §5.

## 7.10 Cosa deve decidere Dennis
- **(a) Ripetere (v2) o congelare la v1 con riserva.** Raccomando la **v2**: stesso motore, poche ore di lavoro (punti 1–4 di 7.9). Congelare la v1 passerebbe ad A3 e alla sintesi una quota a 90 anni che dipende da r ≈ g e un acquisto in periferia a suolo gratuito. Se Dennis preferisce congelare la v1, deve farlo come "motore e tabelle, tarata debolmente, nessuna lettura per la tesi", con le avvertenze G1–G3 in VERSIONE.md.
- **(b) Il vincolo su r − g.** Serve una regola su r − g: un minimo con fonte, oppure tassi reali. Raccomando i tassi reali con un intervallo per lo spread reale da fonte (BTP€i o tassi CDP), perché sui 90 anni la grandezza economica che conta è lo spread reale e non i tassi nominali.
- **(c) Uso di K1.** Tenere K1 come vincolo di segno, ma con la regola scritta ora: se i bandi DG 365 vanno deserti o si aggiudicano con condizioni diverse, la taratura si rifà. Raccomando di sì.
- **(d) Uso della Base E nelle prove B0–B6.** Raccomando che non sia un vincolo di fattibilità per lotto finché G3 non è risolto.

---
**Appendice — controlli rifatti** (formule di `run.py` invariate; seme 4519, N = 20.000). Θ_cal = punti del cubo con VAN_K1 ≥ −0,05·C_tot nei tre compendi. r = D·i_D + (1 − D)·i_E. Quote "cessione regge" = mean(L\*(c₀, T) ≥ 0) su Θ_cal, poi ristretta a r > g e a r − g ≥ 0,005. Tornado di E6 come la funzione `tornado()` di `run.py`, ripetuto per T ∈ {60, 90} e c₀ ∈ {90, 110, 130}. Premio del nuovo: p_z × {1; 1,2; 1,4} nel VRA mediano dei lotti delle fasce D/E. Recupero: L\*(rec = True, c₀ = 90, T = 60) per classi di ρ. Non verificato: riesecuzione senza cache; fonti [S] (asta 2023, Il Sole 24 Ore, oneri); ordine interno del registro.
