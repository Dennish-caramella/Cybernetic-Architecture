# Housing need and affordability: metrics, models, and the Milan context (for the 88 NIL of Milan)

Research date: October 2026. Tool budget: about 17 calls. Items marked **[UNVERIFIED]** come from background knowledge of the literature. No URL was fetched for them this session, so the report writer must flag them or drop them.

## Q1. Affordability metrics: which are academically defensible?

### Takeaway
The 30% rent-to-income rule is a descriptive convention with no normative basis. Its strength is that the data are easy to get and comparable. The residual income approach (Stone's "shelter poverty") is the more defensible normative measure, but it needs a basic-needs budget for each household type. Eurostat's overburden rate (more than 40% of disposable income) is the standard EU comparative indicator. Best practice: report a ratio and a residual measure together, by household type, and compute an "affordability gap" in euros (rent minus affordable rent).

### Cited Findings
- **Critique of the 30% rule.** Stone argues that a normative affordability standard needs an independent logical basis. The 30% figure instead came from observed spending patterns. — [Shelterforce, "30 percent standard's blinders" (2017)](https://shelterforce.org/2017/04/25/30-percent-standards-blinders/)
- **Ratio errors run both ways.** The ratio flags high-income households that spend more than 30% by choice. It misses low-income households that spend under 30% but still have too little left for non-housing needs. It also ignores location costs such as transport. — [City Observatory, "Residual income: a better way of measuring affordability"](https://cityobservatory.org/residual-income-a-better-way-of-measuring-affordability/); [Sightline](https://sightline.org/?p=1468)
- **Residual income method.** Subtract a normative non-housing budget, which varies with household size and composition, from income. The remainder is the maximum affordable housing cost. Stone's "shelter poverty" = households that cannot meet non-housing basic needs after paying for housing. — [City Observatory](https://cityobservatory.org/residual-income-a-better-way-of-measuring-affordability/); [Planetizen summary of Harvard JCHS work](https://planetizen.com/node/100982)
- **Herbert & McCue (Harvard JCHS) comparison.** The affordable housing share varies by household size, composition, and income. In high-cost markets, the 30% standard tends to overstate problems for higher-income and small households. Aggregate burden levels came out similar under both methods. — [Planetizen](https://planetizen.com/node/100982)
- **Practical drawbacks of residual income.** It needs much more household data. The poverty and basic-needs thresholds are contestable. The US Department of Veterans Affairs uses a version of it for mortgage underwriting. — [City Observatory](https://cityobservatory.org/?p=1256)
- **Eurostat housing cost overburden rate.** The share of the population living in households whose total housing costs exceed 40% of disposable income, both "net" of housing allowances. The detailed guidance says tenant rent is counted before housing benefits, so the page is internally inconsistent on allowances. Mortgage interest is counted net of tax relief. — [Eurostat Glossary: Housing cost overburden rate](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Housing_cost_overburden_rate)
- **Italy overburden by tenure, EU-SILC 2024** (Eurostat via mirror). Market-rent tenants 19.4% (series peak 34.6% in 2011). Reduced-rent or free tenants 4.8%. Owners with mortgage 1.7%. Owners without mortgage 2.2%. Single-person households 15.6%. Market renters are therefore the burden concentration. — [Trading Economics / Eurostat, market-rent tenants](https://tradingeconomics.com/italy/housing-cost-overburden-rate-tenant-rent-at-market-price-eurostat-data.html); [single person](https://tradingeconomics.com/italy/housing-cost-overburden-rate-single-person-eurostat-data.html); [reduced rent](https://tradingeconomics.com/italy/housing-cost-overburden-rate-tenant-rent-at-reduced-price-or-free-eurostat-data.html). Eurostat source tables: [tespm140](https://db.nomics.world/Eurostat/tespm140), [ilc_lvho07e](https://db.nomics.world/Eurostat/ilc_lvho07e?offset=10). The Italy all-household total for 2024 was not retrieved (gap).
- **Price-to-income for Milan.** A Financial Times analysis, cited by Tgcom24, puts Milan at 12.5 times average annual income, above London. The underlying metric (average vs median, gross vs net) is not specified. — [Tgcom24 (Feb 2026)](https://www.tgcom24.mediaset.it/tgcomlab/focus/milano-stipendio-non-basta-caro-casa-trasporti_111302150-202602k.shtml)
- **Literature beyond the fetched sources [UNVERIFIED, no URL fetched]:**
  - Hulchanski (1995, *Housing Studies*) separates six uses of the expenditure-to-income ratio: description, analysis, administration, definition, prediction, and selection criteria. He argues the ratio is valid only for description and administration.
  - Stone (2006, *Housing Policy Debate*, "What is housing affordability? The case for the residual income approach") is the canonical normative statement.
  - Haffner & Heylen (2011, *Housing Studies*) compare ratio and residual measures on Dutch and Flemish data.
  - The OECD Affordable Housing Database reports indicator HC1.2: the share of households in the bottom income quintile spending over 40% of disposable income on rent and mortgage.
  - The UK English Housing Survey, and Bramley's work, apply an affordability test of 25-35% of gross income for local need assessment.

### Inferences
- For a NIL-level model, the most defensible set of metrics is:
  1. Rent-to-income ratio, at 30% and at the Eurostat 40%, applied to *net* income.
  2. A residual income test by household archetype, using the Istat absolute poverty line for Milan (metropolitan North) as the non-housing basic-needs budget. This gives a transparent, published normative basket. [Istat line values not retrieved; gap]
  3. An affordability gap in €/month and €/year = OMI rent for an adequate dwelling minus the affordable rent (min of 30% of net income and the residual), aggregated over households.
- IRPEF income by CAP is *gross taxable income per taxpayer*, not household net income. A conversion step is needed: tax-unit to household (Istat household size by NIL), gross to net (IRPEF brackets and addizionali). Without it, ratios will understate burden.

### Gaps
- The Italy 2024 total overburden rate and Milan- or Lombardy-specific EU-SILC figures were not retrieved.
- Primary journal pages for Stone 2006, Hulchanski 1995, and Haffner & Heylen were not fetched. The citations above are from memory.
- The OECD HC1.2 values for Italy were not retrieved.

## Q2. Housing need estimation methods (projection, stock-flow, missing middle, archetypes)

### Takeaway
The UK literature (Bramley; Holmans) is the most developed. Need = backlog (existing households in unsuitable or unaffordable housing) + newly arising need (household formation × share unable to afford market) − supply of affordable relets and new completions. Projects of this kind apply it with an affordability test calibrated to local entry-level market rents. For Milan, the "missing middle" is the band between the ERP/SAP income ceiling and the income needed to rent at OMI market levels. This band is quantifiable from IRPEF distributions.

### Cited Findings
- **Bramley's taxonomy (2010 DCLG report "Estimating housing need").** He groups methods into four families: (1) the Holmans demographic "net stock" model, (2) a second family the search did not identify, (3) affordability-based needs models, and (4) a fourth family the search did not identify. He separates *backlog* need from *newly arising* need, with methodological implications. — [White Rose eprints 72850, Estimating Housing Need (DCLG 2010)](https://eprints.whiterose.ac.uk/72850/1/estimatinghousingneed.pdf)
- **Crisis/NHF 2018 (Bramley).** Backlog of 4.75 million households across Great Britain (4 million in England). The study combined three methods: two demographic frameworks augmented by affordability, plus a dynamic sub-regional housing market simulation model. — [Crisis, Housing supply requirements across Great Britain (2018)](https://www.crisis.org.uk/ending-homelessness/homelessness-knowledge-hub/housing-models-and-access/housing-supply-requirements-across-great-britain-2018/)
- **Bramley & Karley (2005, *Housing Studies*).** Modelled affordability-based need estimates at regional and local levels in England, usable to compare areas and track change over time. — [Crisis/ISER pages citing it](https://www.iser.essex.ac.uk/research/publications/publication-525831) (indirect; the paper itself was not fetched)
- **Local application (Nottingham SHMA 2012, spreadsheet "Bramley model").** About 45% of emerging households are unlikely to be able to access entry-level market housing. This is the "share of new households priced out" parameter. — [Nottingham SHMA update 2012](https://www.nottinghamcity.gov.uk/media/jp0fwzjg/bdhou32-nottingham_shma_update2012_final.pdf)
- **Contestation.** A council report (Elmbridge 2024) argues that Bramley's national figure of 300,000 homes a year would be closer to 210,000 a year under different assumptions. The estimates are highly sensitive to the affordability threshold and the backlog clearance period. This is a policy-motivated source. — [Elmbridge Supplementary Housing Affordability Report (Mar 2024)](https://elmbridge.gov.uk/sites/default/files/2024-03/Supplementary%20Housing%20Affordability%20Report%20-%20Mar%202024.pdf)
- **Milan "missing middle" size.** Lombardy regional studies, cited in reporting on the Milan 2026 calls, put the group "not eligible for ERP but unable to pay market rent" at 37-38% of employees. — [ANSA, 26 Mar 2026](https://www.ansa.it/lombardia/notizie/2026/03/26/a-milano-bandi-per-case-a-canone-calmierato-affitti-da-375-euro-al-mese_66ef3480-1bc0-4430-aacd-a1b546ad8bf5.html)
- **Milan Piano Casa target band.** Households earning €1,500-2,500 net per month. A 2025 commentary argues that about €48,000 per year net is needed to cover average costs at the lower end of the Milan market, above the band ceiling. — [QuiFinanza](https://quifinanza.it/mercato-immobiliare/piano-casa-milano-case-canone-calmierato/859762/); [Diego Valazza substack, "Il piano casa"](https://diegovalazza.substack.com/p/capitolo-2-il-piano-casa) (opinion source)
- **Long-term rental supply is shrinking.** Long-term leases' share of Milan rentals fell from 66% to 51% between 2020 and 2024, with temporary or short lets rising. The source is reported via Tgcom24 and is not named precisely. — [Tgcom24 (2026)](https://www.tgcom24.mediaset.it/tgcomlab/focus/milano-stipendio-non-basta-caro-casa-trasporti_111302150-202602k.shtml)
- **Methods literature [UNVERIFIED, no URL fetched]:**
  - Household projection by the *headship-rate* method: projected population by age × sex × headship rate = households. Used by ONS/MHCLG and by Istat's "previsioni delle famiglie" (base 2021/2022, to 2041/2043), which are available at regional or provincial level, not NIL.
  - Stock-flow model: Δstock = completions + conversions − demolitions − change of use. Need gap = projected households × (1 + vacancy allowance, typically 2-4% frictional) − effective stock.
  - Archetype or microsimulation segmentation: households cross-classified as size × income band × age of reference person, each cell weighted by frequency. Examples are UK SHMA "housing market segmentation" and Dutch WoON-based models.

### Inferences
- **Recommended NIL pipeline** (open data only):
  1. Households by NIL and size: Comune di Milano open data (anagrafe by NIL), plus Istat Census 2021 tables by section aggregated to NIL.
  2. Income distribution: MEF IRPEF by CAP, giving taxpayer counts per income bracket (0-10k, 10-15k, 15-26k, 26-55k, 55-75k, 75-120k, >120k). Map CAP to NIL by areal or population-weighted overlay.
  3. Build archetypes as size (1, 2, 3, 4+) × income band (ISEE-ERP, ERS/missing middle, market) × age (<35, 35-64, 65+). Weight each cell by its NIL frequency. Without microdata, use iterative proportional fitting or raking of the marginals.
  4. Rents: OMI semester rent range (€/m²/month, min-max, "abitazioni civili" normal state) by OMI zone, intersected with NIL.
  5. For each archetype × NIL: required size (DM 2008 standard, about rooms ≥ persons; or around 28 m² for 1 person and 14-15 m² per extra person [UNVERIFIED norm]) × OMI rent gives the market cost. Affordable rent = min(30% net income, residual income). Then compute gap and headcount.
  6. Need = backlog (current burdened households) + flow (new households from projections × priced-out share) − pipeline (Piano Casa units, ERP vacancies brought back into use).
- The single most influential parameter is the income threshold applied to IRPEF brackets. Run a sensitivity analysis at 25%, 30%, 35%, and 40%.

### Gaps
- Bramley's four model families were not fully enumerated in the fetched snippet. The second and fourth names are missing.
- No Italian peer-reviewed NIL-level need model was found. The Politecnico DAStU / OCA (Osservatorio Casa Abbordabile) methodology was not fetched. Tgcom24 cites an OCA estimate that housing and transport together take up to 60% of income in Milan, but the primary report URL was not retrieved.
- Nomisma fabbisogno abitativo estimates for Milan were not retrieved.

## Q3. Italian social housing framework and Milan crisis data

### Takeaway
Italy has two tiers.
- ERP/SAP: public, very low income, canone sociale, governed in Lombardy by L.R. 16/2016 and R.R. 4/2017.
- ERS/housing sociale: public-private, middle incomes, rents capped at or below canone concordato. Defined nationally by DM 22 aprile 2008.

Milan's 2024-2026 Piano Casa targets €1,500-2,500 per month households with rent caps of €80-90/m²/year. Meanwhile market rents absorb roughly 73-76% of a single net wage. About 17,000 households wait for ERP while 10,000-17,700 public dwellings stand vacant.

### Cited Findings

**National definition (DM 22 aprile 2008, GU 24/06/2008 n.146):** — [Text via ANCE](https://ance.it/wp-content/uploads/archive/784-DM%2022-04-2008%20definizione%20di%20alloggio%20sociale.pdf); [Camera dei Deputati summary](https://www.camera.it/temiap/t/news/post-OCD15-10142)
- Art. 1 c.2: an "alloggio sociale" is a residential unit in *permanent* rental. It serves the general interest of reducing housing hardship for disadvantaged households unable to access the free market.
- Art. 1 c.3: the definition also covers units built or recovered by public or private operators with public contributions or incentives (tax exemptions, land, guarantee funds, planning incentives). These may be for temporary rental of *at least 8 years* and also for ownership.
- Art. 1 c.5: social housing is a service of general economic interest. It constitutes an *additional urban planning standard*, secured by free transfer of land or dwellings under regional rules.
- Art. 2 c.2: regions, with regional ANCI, set rents by economic capacity, household composition, and dwelling characteristics. Rents must cover tax, management, and ordinary maintenance costs.
- Art. 2 c.3: the rent of ERS units (art. 1 c.3) **cannot exceed the canone concordato** under the local agreements of L. 431/1998 art. 2 c.3.
- Art. 2 c.4: operator compensation (rent plus subsidies) cannot exceed the cost of the public-service obligations plus a "reasonable profit". This is the SGEI / EU state-aid logic.
- Art. 2 c.7: the dwelling is "adequate" if the number of habitable rooms is about at least the number of household members, capped at 5, plus bathroom and kitchen. Energy and sustainability principles apply.
- Commentators call the decree generic, and qualitative with no competition rules. — [Regione Emilia-Romagna, Petrone seminar](https://territorio.regione.emilia-romagna.it/osservatorio-delle-politiche-abitative/i-seminari-di-orsa/quadro-normativo-nazionale-e-regionale-dellers-iole-petrone.pdf/@@download/file/Quadro%20normativo%20nazionale%20e%20regionale%20dell'ERS%20(Iole%20Petrone).pdf); [Il Sole 24 Ore NT+](https://ntplusdiritto.ilsole24ore.com/art/esenzione-imu-ed-alloggi-sociali-requisiti-e-finalita-sas-e-sap-ADtGPxVB)

**Lombardy (L.R. 16/2016):**
- SAP (public housing services) are governed by L.R. 16/2016 and R.R. 4/2017. L.R. 7/2025 (30 May 2025) amended art. 22 c.1 lett. d) on beneficiary requirements. — [Regione Lombardia, SAP page](https://www.regione.lombardia.it/politiche-sociali-e-abitative/abitare-in-lombardia/servizi-abitativi-pubblici--l-r--16-2016-e-r-r--4-2017)
- Decree 18698 of 17/12/2025 updates the ISEE-ERP classes and the canone sociale for 2026 by CPI. The threshold figures were not extracted. — [Regione Lombardia, Aggiornamento 2026 classi ISEE ERP (PDF)](https://www.regione.lombardia.it/content/dam/rl/canali-tematici-servizi/08-politiche-sociali/01-abitare-in-lombardia/red-abitare-in-un-alloggio-pubblico/allegati/Aggiornamento%20anno%202026%20classi%20ISEE_ERP.pdf)
- Art. 25 provides a temporary "contributo regionale di solidarietà" for indigent SAP tenants. — same Regione page
- **[UNVERIFIED]** The SAP access ceiling is commonly reported as ISEE ≤ €16,000. An Il Giorno piece notes regional rules envisaging income bands of €16-40k for some ALER calls. — [Il Giorno](https://www.ilgiorno.it/milano/cronaca/redditi-proprieta-domande-consegnate-a-mano-rozza-contro-gli-strani-requisiti-di-4-bandi-aler-5dc97dd8) (dated; must check against DD 18698/2025)

**Canone concordato Milan:**
- Two territorial agreements are in force. The historic one sets zones with €/m²/month min-max ranges by unit size band. The new July 2023 agreement adds corrective factors, and the owner chooses which to apply. The 2023 proposal described replacing about 60 microzones with 5 bands. — [DokiCasa (commercial)](https://dokicasa.it/servizi/accordi-canone-concordato-milano); [Sky TG24, 25 May 2023](https://tg24.sky.it/economia/2023/05/25/milano-caro-affitti-studenti); [Milano Finanza](https://www.milanofinanza.it/news/l-affitto-cambia-passo-2614232)
- Actual €/m² values were not retrieved (gap). They are needed because they cap ERS rents under DM 2008 art. 2 c.3.

**Piano Casa Milano / Milano Abitare / Società della Casa:**
- Announced 24 Oct 2024. Targets 10,000 units at canone calmierato over about 10 years, roughly 6,500 in Milan and 3,500 outside. Target households earn €1,500-2,500 per month. The rent cap was announced as max €80/m²/year. — [MilanoToday](https://www.milanotoday.it/politica/case-affitti-bassi.html); [Radio Lombardia](https://www.radiolombardia.it/2024/10/24/milano-il-comune-presenta-il-piano-casa-10-mila-case-contro-il-caro-affitti/); [QuiFinanza](https://quifinanza.it/mercato-immobiliare/piano-casa-milano-case-canone-calmierato/859762/)
- More than 300,000 m² of unused or underused public land, granted in 90-year diritto di superficie for free or a symbolic fee. — [FHS repost of mitomorrow (Jun 2025)](https://www.fhs.it/2025/06/05/milano-in-arrivo-10-000-nuovi-alloggi-a-canone-calmierato/?lang=en)
- **Calls of March 2026** (ex Palasharp, San Romanello, Bovisasca), from [ANSA, 26 Mar 2026](https://www.ansa.it/lombardia/notizie/2026/03/26/a-milano-bandi-per-case-a-canone-calmierato-affitti-da-375-euro-al-mese_66ef3480-1bc0-4430-aacd-a1b546ad8bf5.html):
  - Average maximum rent €90/m²/year.
  - Example rents: 50 m² €375, 70 m² €525, 90 m² €675 per month.
  - More than 27,000 m² of land at a symbolic €1/m², 90-year surface right.
  - Rents fixed for at least 30 years. Lower rents or longer restrictions earn extra points.
  - About €11M for remediation and Palasharp demolition.
  - Bocconi supported the economic-financial analysis.
- A municipal "Società della Casa" will acquire, regenerate, and manage up to about 1,000 units for the middle class. — [Affaritaliani](https://www.affaritaliani.it/milano/milano-nasce-la-societa-della-casa-fino-a-mille-alloggi-per-il-ceto-medio.html)
- Date conflict: one source says the plan was formally approved in October 2025, another implies October 2024. Verify with Comune di Milano deliberations. — [QuiFinanza](https://quifinanza.it/mercato-immobiliare/piano-casa-milano-case-canone-calmierato/859762/) vs [Radio Lombardia](https://www.radiolombardia.it/2024/10/24/milano-il-comune-presenta-il-piano-casa-10-mila-case-contro-il-caro-affitti/)

**Rents vs wages (Milan, 2019-2026):**
- CNA report (June 2026, OMI rents and net wages 2019-2025): Milan rents rose 49% (joint highest with Florence), while net wages grew 7-15% nationally. The average rent for a standard flat (over €1,800 per month) takes 73% of the average net monthly wage. — [AGI, 6 Jun 2026](https://www.agi.it/economia/news/2026-06-06/casa-caro-affitti-milano-37410756/); [Money.it](https://www.money.it/affitti-dal-2019-cresciuti-5-volte-piu-degli-stipendi-a-milano-si-mangiano-il-73-del-reddito); [PMI.it](https://www.pmi.it/economia/lavoro/495555/affitti-salari-divario-capoluoghi.html)
- CDP data (rents 2024, wages 2023): a 60 m² flat costs 76% of the net wage in Milan, against a national average of 35%. — [PMI.it (Dec 2025)](https://www.pmi.it/economia/mercati/484035/affitti-il-conto-sale-a-milano-fino-al-76-dello-stipendio-ecco-la-mappa-nazionale.html)
- Caveat: these are single-earner, average-rent ratios. They are not household-level and not distributional, so they are not comparable with Eurostat overburden.

**ERP waiting lists and vacancies:**
- June 2026: about 17,000 households waiting for ERP and almost 10,000 vacant public dwellings (Unione Inquilini). More than 1,500 evictions validated in 2025. 400 emergency-housing applications accepted but not housed. — [Il Fatto Quotidiano, 10 Jun 2026](https://www.ilfattoquotidiano.it/2026/06/10/emergenza-abitativa-milano-alloggi-sfitti-notizie/8414696/)
- Conflicting vacancy counts:
  - 16,423 vacant (ALER 10,364; MM/Comune 6,059). — [Immobiliare.it news](https://www.immobiliare.it/news/vivere-a/milano/case-popolari-vuote-a-milano-sono-oltre-16mila-50mila-in-tutta-la-lombardia-221005/) and [Mi-Tomorrow](https://www.mitomorrow.it/online/primo-piano/case-popolari-piu-di-16-000/). Search snippet only; the page returned 403.
  - 17,675 vacant (ALER 11,584).
  - 8,155 ALER vacancies per the 2024 ALER board of auditors. — search-summary figures from [MilanoToday](https://www.milanotoday.it/economia/aler-conti-rosso-abusivi-morosi.html) / [MilanoToday 2025](https://www.milanotoday.it/politica/ristrutturazione-manutenzione-case-popolari-situazione-2025.html). **UNVERIFIED which article holds which figure.**
  - Differences likely reflect "sfitto" definitions (needing works, not assignable, in sale plans) and dates.
- Unions report that about 9,440 assignments were planned for 2021-2025 but only 4,320 were made. — [MilanoToday](https://www.milanotoday.it/politica/case-popolari-non-assegnate.html) (search snippet; **UNVERIFIED**)
- One small call drew 551 candidates for 31 homes. — [Il Giorno](https://www.ilgiorno.it/milano/cronaca/per-31-case-popolari-551-f11eb404)
- ALER Milano manages the regional stock. MM S.p.A. manages the municipal ERP stock. — [MilanoFree](https://www.milanofree.it/milano/cronaca/case-popolari-a-milano-come-funzionano-aler-e-mm-assegnazioni-e-occupazioni.html)

### Inferences
- The Piano Casa example rent of €375 for 50 m², with income of €1,500-2,500 per month, gives a rent-to-income ratio of 15-25%. For a single €1,500 earner in 70 m² (€525), it is 35%. The cap is affordable for the stated band only when unit size matches household size.
- At €90/m²/year (€7.5/m²/month), the cap is roughly 35-45% below typical Milan OMI rents for semi-central zones. This rests on an unverified assumption of €13-20/m²/month in OMI semester ranges; check against OMI.
- The ERP vacancy stock (about 10-17k) is the same order of magnitude as the waiting list (about 17k). Bringing vacancies back into use is therefore a supply lever comparable to the whole 10-year Piano Casa target.

### Gaps
- The 2026 ISEE-ERP thresholds and canone sociale values (DD 18698/2025) were not extracted.
- Milan canone concordato €/m² values by zone were not retrieved.
- The Fondazione Housing Sociale / CDP Sistema Integrato Fondi (FIA, FIA2) model and typical ERS rents (often cited around €60-90/m²/year in Milan FHS projects) were not verified this session **[UNVERIFIED]**.
- No official Comune di Milano statistic on the ERP waiting list (graduatoria) by NIL was found.

## Q4. Construction/land cost and feasibility models

### Takeaway
Feasibility for capped-rent social housing comes from discounted cash flow or residual land value. Capitalised net rent must cover construction, fees, and finance. Land is the value that makes it work, which is why Milan gives land at €1/m² for 90 years. Milan's official "costo di costruzione base" (for fees) is €494.96/m² for 2026, far below actual hard costs. Real-cost benchmarks for Milan were not found in primary sources.

### Cited Findings
- **Milan base construction cost (for computing the contribution on building permits).** €494.96/m² for 2026, revalued from €484.78/m² in 2025 (DD 10249 of 13/11/2025). This is a fee parameter, not a market build cost. — [Comune di Milano, DD 10249/2025 (PDF)](https://www.comune.milano.it/documents/20118/722122/Aggiornamento+costo+costruzione+-+Annualit%C3%A0+2026.pdf/bb0e4eea-9242-c574-b8b3-7aa15e5b831a?version=2.1&t=1763638252974&download=true)
- **Porto di Mare canone calmierato district.** Estimated works cost €98.18M net of VAT. The floor area was not given, so no €/m² can be derived. — search summary of [professioneArchitetto](https://www.professionearchitetto.it/concorsi/notizie/34300/milano-social-housing-a-porto-di-mare) (**figure unverified on the page**)
- **Land subsidy in the Milan calls.** Land at €1/m², a 90-year surface right, and a 30-year rent lock. Bocconi did the financial analysis. — [ANSA 2026](https://www.ansa.it/lombardia/notizie/2026/03/26/a-milano-bandi-per-case-a-canone-calmierato-affitti-da-375-euro-al-mese_66ef3480-1bc0-4430-aacd-a1b546ad8bf5.html)
- **Regulatory profit cap.** Under DM 2008 art. 2 c.4, compensation (rent plus subsidies) ≤ cost of the service obligations + "reasonable profit" (EU SGEI decision 2005/842/EC). This frames any viability model as cost-plus-reasonable-return. — [DM 22/04/2008 via ANCE](https://ance.it/wp-content/uploads/archive/784-DM%2022-04-2008%20definizione%20di%20alloggio%20sociale.pdf)
- **Rents must cover tax, management, and ordinary maintenance** (DM 2008 art. 2 c.2). This sets a floor on viable rents. — same source
- **Invimit SGR student and social project.** Beds at about €454/month, framed as balancing economic sustainability and social impact. — [Milano Finanza, Jan 2026](https://www.milanofinanza.it/news/milano-invimit-sgr-lancia-un-progetto-di-social-housing-con-posti-letto-a-canone-calmierato-202601221548283897)
- **Regional co-funding example.** A 21-unit LUM project cost €1,084,813, of which €609,973 was regional grant (56%). Floor area is unknown. — [Lombardia Notizie](https://www.lombardianotizie.online/housing-sociale-sopralluogo/)

### Inferences
- **Simple viability check per NIL lot** (to parameterise; values marked [UNVERIFIED] are typical-order assumptions, not sourced):
  - Net rent = cap (€80-90/m²/yr on net lettable area) × (1 − vacancy and arrears 3-5%) − opex (management, maintenance, IMU-exempt per DM 2008: around 20-30% of gross rent [UNVERIFIED]).
  - Capital value = net rent / yield. FIA social funds typically target a 2-4% real yield [UNVERIFIED].
  - Residual land value = capital value − (hard cost €/m² GFA × GFA + soft costs 12-18% + finance + developer margin).
  - Example: at €90/m² rent, about €65/m² net and a 3% yield, capital value is about €2,170/m². With hard costs in Milan for new residential often reported around €1,800-2,500/m² [UNVERIFIED], the residual land value is about zero or negative. That is consistent with the city granting land at €1/m².
- **Land value from OMI.** OMI gives market *prices* (€/m² of saleable area) by zone. Market residual land value ≈ OMI price × saleable m² − build cost − margin. The gap between market residual land value and social-use residual land value (about 0) gives the *implicit public subsidy* per lot. That is a defensible metric for ranking NIL sites.

### Gaps
- No primary source found for actual construction costs per m² of Milan social housing for 2024-2026, for example from the Collegio Ingegneri e Architetti Milano price lists, Politecnico, or FHS project data.
- No Nomisma or Scenari Immobiliari feasibility benchmarks were retrieved.
- Yields and discount rates used by the CDP FIA / FHS funds were not verified.
