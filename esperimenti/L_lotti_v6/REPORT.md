# Report di laboratorio — Base L v6: regole di Dennis del 14/11 (ticket #39)

Stato: **non passa** (C5 falso). Report assemblato dal coordinatore. Revisione indipendente: vedi §7.

## 1. Ipotesi e soglia
Testo completo in `esecuzioni/00_preregistrazione.txt` (SHA-256 `0d83dda3…`, commit f4b8f44 del 14/11, **prima di ogni esecuzione**). Regole nuove rispetto a v5 (decisioni di Dennis, `tesi/DECISIONI.md`): lo stato di attuazione non esclude lotti (C9 eliminato, resta come attributo); nessun controllo umano; GFU e ambiti a destinazione non verificata come lotti edificabili; riuso senza estensioni, con un attributo informativo `potenziale_vuoto`; progetti con cantiere = sì in codifica 1 o 2 come tessuto consolidato.
Criteri: C1–C4, C6, C8 come v5; C5 con post-stratificazione (S1 = lotti identici a v5, codifiche v5 riusate; S2 = lotti nuovi o cambiati, censimento di 84 lotti); C5a ≥ 0,70, kappa binario ≥ 0,60, C5b limite inferiore Newcombe ≥ 0,25. Soglia implicita su S2: 0,6439; potenza dichiarata prima delle codifiche: 0,51 con q = 0,65, 0,85 con q = 0,70.

## 2. Dati e fonti
Come v5 (cache e fonti non riscaricate). Ambiti 2030 dallo strato 11 del mosaico regionale, AdP Scali ferroviari, GFU con perimetro 2012 sostitutivo [H]. Censimento di v5 (codifiche 1 e 2) usato solo per l'attributo di stato e per la regola cantiere. Immagini AGEA 2018–2019 (sola visione) e Sentinel-2 2025 EOX (CC BY-NC-SA 4.0).

## 3. Metodo
Come v5 con modifiche minime in `run.py`. Tre esecuzioni complete con hash identico `b0db2c5a…`. Verifica degli SHA-256 dei file di v5 riusati: superata.
**Incidente di codifica** (registro): la prima consegna dei codificatori è stata scartata prima di leggere qualsiasi risultato, perché le immagini già viste erano state rimosse dal contesto. È stata rifatta con otto istanze nuove (quattro per codificatore, 21 immagini ciascuna). Ogni istanza ha dichiarato di aver visto le immagini; i tempi sono molto brevi (circa 1,5 minuti per 21 immagini) [L]. I codificatori sono LLM della stessa famiglia; Dennis ha deciso di non fare un controllo umano.

## 4. Risultati
- **Conteggi**: 220 lotti edificabili, 160 da riusare, 269 aree di attivazione, 52 lotti nel tessuto consolidato (112,8 ha). Capacità degli edificabili a FAR 0,5 / 1 / 2: 18.318 / 36.744 / 73.605 alloggi. Per scenario, a FAR 1: 29.021 (GFU come in v5), 37.799 (senza Bovisa), 45.683 (senza regola cantiere). I lotti non in ambito sono identici a v5.
- **Dato Bovisa di v5 non riproducibile** (56,5 ha): verificati 64,1 ha (lotti nell'ambito) e 63,8 ha (intersezione), su un poligono di 85,6 ha; in v6 Bovisa è tessuto consolidato.
- **C1–C4, C6, C8**: veri.
- **C5**: kappa binario 0,934 (cod. 1) e 0,967 (cod. 2). C5a = 0,686 (soglia 0,70): **falso**. Quota di lotti liberi o dismessi:
  - S1 (identici a v5): 0,700 e 0,717;
  - S2 (nuovi o cambiati, n = 84): 0,560 e 0,512, contro la soglia implicita 0,644.
  - Particelle a caso (base): 0,16 per entrambi. C5b passa (limite inferiore 0,522 e 0,530).
  - Dentro S2: aree di attivazione 0,604 (n = 24), riuso 0,577 (13), edificabili **0,489** (47).
  - Per gruppo di ambito: **GFU 0,261 (n = 23)**, AdP 0,514 (35), PA/AS 0,808 (26).
- **Lettura** [I]: le GFU, che per decisione di Dennis diventano lotti edificabili, risultano libere o dismesse solo in circa un quarto dei casi (perimetro 2012 sostitutivo, con edifici in uso). I PA/AS sono invece ben confermati.

## 5. Esito
**Non passa (C5 falso: 0,686 < 0,70).** La regola di arresto è scattata: decide Dennis. La soglia non si modifica dopo l'esito.

## 6. Limiti
- I codificatori sono LLM della stessa famiglia, con kappa molto alto [I]; l'ipotesi di indipendenza non regge.
- Prima consegna scartata; seconda consegna con tempi di codifica molto brevi [L].
- Perimetri e destinazioni delle GFU mancano [L]; si usa il perimetro 2012 [H].
- `potenziale_vuoto` è una regola calcolata dagli strati, senza verità a terra; 1 solo lotto su 127 è marcato "1" (vedi `tabelle/lotti_attributi.csv`).
- I "cantiere = sì" (6 poligoni) vengono dalla sola codifica 2, con fonti spesso secondarie; non ho incrociato la fonte ufficiale.
- Etichette obsolete in `cascata.csv` (cosmetiche).
- Non verificata la riproducibilità da zero senza la cache copiata.

## 7. Revisione indipendente
(da scrivere dal `revisore-metodologico`)

## 8. Cosa passa alla prova successiva
Niente: la base non è congelata. Opzioni per Dennis nel messaggio di consegna (ripetere con le GFU in una classe separata "da verificare", oppure accettare le GFU come ipotesi dichiarata e andare avanti con la base come "candidata con riserva").
