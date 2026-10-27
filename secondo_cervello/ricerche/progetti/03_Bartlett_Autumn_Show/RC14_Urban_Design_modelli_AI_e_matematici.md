# Analisi dei progetti RC14 – The Bartlett (Urban Design MArch)

**Fonte:** [The Bartlett Show Index – Project Index](https://shows.bartlettarchucl.com/project-index), filtro *RC14 – All Years*
**Data dell'analisi:** 19 ottobre 2026
**Progetti nel periodo:** 34 (2020–2026), di cui **32 letti**. Le pagine di *Tonal Walks* e *Agro-Matrix* (2022) restituiscono un errore del server (500) e non si aprono.

---

## 1. Il metodo che quasi tutti seguono

Quasi ogni progetto del cluster passa per gli stessi cinque passaggi:

1. **Raccolta dei dati.** Si sovrappongono a griglia molti strati di dati aperti su Londra: deprivazione (IMD), densità, verde, rumore, inquinamento, GPS, social media (Instagram, Twitter), Google Street View, OpenStreetMap.
2. **Riduzione delle dimensioni (statistica).** PCA (Principal Component Analysis), matrici e heatmap di correlazione, t-SNE.
3. **Clustering (apprendimento non supervisionato).** K-Means, DBSCAN e Self-Organising Map (SOM) per dividere la città in "tipi" di luogo.
4. **Analisi dello spazio (geometria e teoria dei grafi).**
   - Space Syntax: analisi angolare dei segmenti, angular step depth, integrazione e scelta (Depthmap)
   - Visibility Graph Analysis (VGA)
   - isovist e ray-casting
5. **Generazione e ottimizzazione:**
   - reti generative: Pix2Pix/GAN, 3D GAN, Stable Diffusion
   - algoritmi evolutivi multi-obiettivo e genetici (Wallacei)
   - simulazioni ad agenti (pedoni, flussi)
   - sistemi procedurali e bio-ispirati: automi cellulari, physarum, shape grammar, Voronoi, aggregazione con Wasp, Woolly

---

## 2. Scheda dei progetti

### 2026 – *Stacked Urbanities*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [The Uneven City](https://autumn2026.bartlettarchucl.com/rc14-stacked-urbanities-2026/the-uneven-city) | Namar Nazer, Xizhe Li, Shawaiz Shaukat, Ruixuan Zhu | PCA, clustering, Pix2Pix (campi spaziali), analisi di rete e angular step depth, Wallacei (ottimizzazione evolutiva) |
| [Shadow Zone: The Glitch City](https://autumn2026.bartlettarchucl.com/rc14-stacked-urbanities-2026/shadow-zone-the-glitch-city) | Tzuping Shih, Qiran Lin, Deqiong Zou, Yixuan Jiang | Pix2Pix, deep learning, SOM, clustering, VGA, keypoint di posa, Gaussian splatting / point cloud, outlier spaziali Low-High |
| [Atmo-Grad](https://autumn2026.bartlettarchucl.com/rc14-stacked-urbanities-2026/atmo-grad) | Shrey Boda, Tanya Vasudeva, Madhuri Manasali Koteshwar Guptha | La pagina dice poco: classificazione di forme di nuvole, mappatura di sovrapposizioni, analisi di visibilità e soleggiamento |
| [From Driven to Drift](https://autumn2026.bartlettarchucl.com/rc14-stacked-urbanities-2026/from-driven-to-drift) | Xiya Mu, Lu (Lydia) Yang, Yuchen Liu | SOM su dipinti, Pix2Pix, algoritmo genetico su griglie, isovist ray-casting, simulazione di 500 pedoni, Voronoi, box plot |
| [Lost in Battersea Maze](https://autumn2026.bartlettarchucl.com/rc14-stacked-urbanities-2026/lost-in-battersea-maze) | Keming Zhang | Clustering e predizione spaziale, aggregazione casuale e con Wasp, dati di profondità e colore estratti da dipinti |

### 2025 – *Sensoria Urbanism*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [MotioGlyph](https://autumn2025.bartlettarchucl.com/ud-rc14-sensoria-urbanism/A25-RC14-project-1) | Sneha Nour Abdul Salam, Vania Arlene, Varssni Karthick | Rete neurale di pose detection, GAN e 3D GAN, t-SNE, clustering non supervisionato, algoritmo evolutivo multi-obiettivo, shape grammar generativa, isovist, Space Syntax |
| [Eco Stack](https://autumn2025.bartlettarchucl.com/ud-rc14-sensoria-urbanism/A25-RC14-project-2) | Isabella Peiling Bai, Kamilya Kelbuganova, Minghao Wang | Simulazione physarum (pathfinding), algoritmo evolutivo multi-obiettivo, SOM sulle morfologie edilizie di Londra |
| [Urban Resonance](https://autumn2025.bartlettarchucl.com/ud-rc14-sensoria-urbanism/A25-RC14-project-3) | Chongyang Cai, Nishna Gaddam, Aditya Bhavesh Shroff, Shufan Yao | Simulazione ad agenti, analisi di spettrogrammi audio (feature di pitch), MIDI tradotto in forme 3D, modello generativo, analisi di rete |
| [Beyond Boundary](https://autumn2025.bartlettarchucl.com/ud-rc14-sensoria-urbanism/A25-RC14-project-4) | Minyue Li, Qi Wan, Jiahang Yang, Haozhe (Eric) Zuo | GAN, PCA, DBSCAN, heatmap di correlazione, spatial join, algoritmo Woolly |
| [MoodLens](https://autumn2025.bartlettarchucl.com/ud-rc14-sensoria-urbanism/moodlens) | Jun Hao, Qizhen He, Hanjie Pan | Pix2Pix (mappa delle emozioni di Londra), VGA, simulazione ad agenti, analisi dei segmenti, composito pesato |

### 2024 – *Sensoria Urbanism*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [Ebb & Evolve](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/ebb-and-evolve) | Ananya Pandey, Sharima Achmad, Shiyun Yang | ML supervisionato e non supervisionato, GAN, clustering, simulazioni di alluvione a scala micro e meso |
| [Sensory Balance](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/sensory-balance) | Jie Liu, Yuan Ping, Huiye Wang, Yu Wu | Stable Diffusion, clustering, correlazione, Street View, simulazione |
| [Playbourhood (Child Haven)](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/child-haven) | Yaohui Zhang, Lina Wu | Machine learning (generico), Stable Diffusion, correlazione |
| [Foggy Dragon City](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/foggy-dragon-city) | Jin (Jennie) Yan, Kexin Zhu, Jiangxing Yu | Deep learning, GAN, Stable Diffusion, point cloud, correlazione |
| [Verdecity](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/green-infrastructure-strategies-for-mitigating-pollution-in-urban) | Nagarjun Chakkaravarthi | Angular segment analysis, mappe di integrazione, dati su inquinamento, salute, alberi e criminalità, immagini dai social |
| [MiniMinds Metropolis](https://autumn2024.bartlettarchucl.com/rc14-sensoria-urbanism/miniminds-metropolis) | Abdullah Ammar A Hababi, Praphulla Thaliyakkattil | Angular segment analysis, step depth, isovist, point cloud, correlazione |

### 2023 – *Machine Learning Urbanism*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [Accent Fusion](https://bpro2023.bartlettarchucl.com/rc14-machine-learning-urbanism-23/accent-fusion) | Xuming Cai, Muskaan Mardia, Yiwen Qian, Yiheng Xu | K-Means, modello ML addestrato su GPS, VGA, Space Syntax, Stable Diffusion personalizzato, Touch Designer |
| [Attenomy City](https://bpro2023.bartlettarchucl.com/rc14-machine-learning-urbanism-23/attenomy-city) | Qiutong Huang, Manan Kinjal Hingoo, Flip Meijaard, Jiahui Xu | K-Means, Pix2Pix, ottimizzazione multi-obiettivo, isovist |
| [Equiticity](https://bpro2023.bartlettarchucl.com/rc14-machine-learning-urbanism-23/equiticity) | Tejaswini Bharat Deshmukh, Shriyansh Jain, Aalok Joshi | Pix2Pix/GAN, clustering non supervisionato, sentiment analysis, VGA, Space Syntax, OpenStreetMap, Google Street View |
| [ND²](https://bpro2023.bartlettarchucl.com/rc14-machine-learning-urbanism-23/nd-squared) | Yiran Luo, Yi Yue, Xiru Zhang | Correlazione dei dati, ML per predire l'idoneità del suolo, "plantable index", "food desert index", VR |
| [Food-Topia](https://bpro2023.bartlettarchucl.com/rc14-machine-learning-urbanism-23/food-topia) | Yanjie Lu, Gracia Muljono, Qiuyi Zhang, Yawei Zhang | PCA, K-Means, reti neurali, algoritmo evolutivo, angular segment analysis, correlazione |

### 2022 – *Machine Thinking Urbanism*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [Mood-ulated Subtopia](https://bpro2022.bartlettarchucl.com/rc14-machine-thinking-urbanism/mood-ulated-subtopia) | Jiwen Bian, Rajita Jain, Trishla Chadha, Zhaoyi Wang | Deep learning e rete neurale con segmentazione semantica di Google Street View, QGIS, simulazione |
| [IsoChronic City](https://bpro2022.bartlettarchucl.com/rc14-machine-thinking-urbanism/isochronic-city) | Shuyao Li, Prakriti Srimal, Sonali Bordia, Siyang Zheng | PCA, K-Means, CNN, ottimizzazione multi-obiettivo (steady-state island GA), automi cellulari, angular step depth, isovist |
| Tonal Walks | — | *Non letto: la pagina dà errore 500* |
| Agro-Matrix | — | *Non letto: la pagina dà errore 500* |

### 2021 – *Cities Beyond Cognition*

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [NutriNet](https://bpro2021.bartlettarchucl.com/rc14-cities-beyond-cognition/nutrinet) | Alankrita Amarnath, Ioannis Bousios, Margarita Chaskopoulou, Junqiao Li | PCA, K-Means, deep learning, Unity |
| [Shadow-Shaped City](https://bpro2021.bartlettarchucl.com/rc14-cities-beyond-cognition/shadow-shaped-city) | Yanni Ren, Flora Mistica Selvaraj, Veleria Volkova, Ruilu Yu | PCA, simulazione ad agenti, point cloud |
| [Inter-Pelagos](https://bpro2021.bartlettarchucl.com/rc14-cities-beyond-cognition/inter-pelagos) | Licheng Yao, Qingrui Jiang, Xuan Zhou, Mengyue Han, Miao Zeng | PCA, K-Means, VGA, simulazioni |
| [Upon Iso-individuals](https://bpro2021.bartlettarchucl.com/rc14-cities-beyond-cognition/upon-iso-individuals) | Qiyuan Hong, Yuhan Shen, Shiqi Wang, Jiang Chang | La pagina dice poco: solo simulazione |
| [(De)stressed City](https://bpro2021.bartlettarchucl.com/rc14-cities-beyond-cognition/de-stressed-city) | Weiheng Qin, Yue Xu, Xiao Peng, Hongying Zhu, Jinyu Wang | PCA, isovist, ottimizzazione, simulazione |

### 2020

| Progetto | Studenti | Modelli di AI e matematici |
|---|---|---|
| [In\|Between](https://bproautumn2020.bartlettarchucl.com/rc14/in-or-between) | Chia Hsun Chiang, Krishan Sharma, Eirini Tsouknida, Xinzhuo Zhao | Rete neurale ricorrente (RNN) su 52 layer con dati GPS e Instagram, word2vec, analisi del colore, PCA, K-Means, simulazione ad agenti |
| [Re-Surge](https://bproautumn2020.bartlettarchucl.com/rc14/re-surge) | Abdimajid Hassan Aden, Yubin Liao, Mohammed Saifiz P. A. Hameed, Keyu Su, Nanxi Zhou | Kernel density, correlazioni, ML per assegnare le destinazioni d'uso, analisi di rumore e visibilità |
| [IIG: Intelligent Intergrowth](https://bproautumn2020.bartlettarchucl.com/rc14/iig-intelligent-intergrowth) | Jie Chen, Huiyu Fan, Xueqing Wang, Jialu Yu | PCA, K-Means su griglia di 10 m × 10 m, analisi dei segmenti con Depthmap, simulazione del rumore |
| [City De-Generate](https://bproautumn2020.bartlettarchucl.com/rc14/city-de-generate) | Hongshuo Dai, Yifei Song, Jingzhe Xu, Ning Zhao | Big data, calcolo dei percorsi minimi, auto-organizzazione |

---

## 3. Quante volte compare ogni metodo (sui 32 progetti letti)

| Famiglia | Metodi | Progetti (circa) |
|---|---|---|
| Statistica e riduzione delle dimensioni | PCA, correlazione, t-SNE, kernel density | ~20 |
| Clustering | K-Means, DBSCAN, SOM, clustering generico | ~20 |
| Space Syntax e geometria della visibilità | angular segment / step depth, VGA, isovist | ~16 |
| Modelli generativi di immagini | Pix2Pix, GAN, 3D GAN, Stable Diffusion | ~15 |
| Simulazione | ad agenti, pedoni, alluvioni, rumore | ~13 |
| Ottimizzazione evolutiva | GA, multi-obiettivo, Wallacei | ~8 |
| Visione artificiale | CNN, segmentazione semantica, pose detection | ~4 |
| Procedurali e bio-ispirati | physarum, automi cellulari, Voronoi, shape grammar, Wasp, Woolly | ~7 |
| Linguaggio e social | RNN, word2vec, sentiment analysis | ~3 |

*I valori sono indicativi: un progetto può rientrare in più famiglie.*

---

## 4. Come cambiano gli strumenti negli anni

- **2020–2021:** soprattutto statistica classica (PCA + K-Means), con RNN e word2vec sui dati social e simulazioni ad agenti.
- **2022:** compaiono la visione artificiale (CNN, segmentazione di Street View), gli algoritmi genetici e gli automi cellulari.
- **2023–2024:** prevalgono i modelli generativi di immagini (Pix2Pix, Stable Diffusion), accanto a Space Syntax.
- **2025–2026:** strumenti più vari:
  - pose detection, 3D GAN, t-SNE
  - SOM su dipinti e morfologie
  - Gaussian splatting
  - sistemi bio-ispirati (physarum)
  - ottimizzazione evolutiva e aggregazione procedurale (Wasp)

**Sintesi:** Pix2Pix, K-Means/PCA e Space Syntax sono i tre strumenti più ricorrenti nel cluster.

---

## 5. Limiti e note sul metodo

- **Pagine non lette:** *Tonal Walks* e *Agro-Matrix* (2022) danno errore 500.
- **Come sono stati raccolti i metodi:**
  - per alcuni progetti (soprattutto 2021, 2022 e 2024 e alcuni del 2020) i metodi sono stati estratti cercando parole chiave nel testo della pagina;
  - lì l'elenco è affidabile per dire *quali* metodi sono citati, meno per descrivere *come* vengono usati.
- **Software:** le pagine li nominano di rado; gli unici citati sono Wasp, Woolly, Depthmap, Touch Designer, QGIS, Unity e Wallacei. È probabile che molti progetti usino anche Grasshopper o Rhino e Python senza dichiararlo.
- **Contenuti nelle immagini:** quello che compare solo nelle tavole e non nel testo della pagina non è stato rilevato.
