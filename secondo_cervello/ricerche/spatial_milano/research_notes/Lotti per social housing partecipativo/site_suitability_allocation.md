# Spatial methods to identify, rank and allocate parcels for affordable/social housing (Milan)

Verification legend: items marked [VERIFIED-WEB] were confirmed against a search result or fetched page in this session (Oct 2026). Items marked [CANONICAL, NOT FETCHED] are standard textbook references whose bibliographic details are well established, but they were not re-checked online in this session. Items marked [UNVERIFIED] come from search snippets, secondary sources or practitioner blogs only.

## GIS-MCDA methods: WLC, AHP, OWA, TOPSIS, PROMETHEE, ELECTRE, fuzzy MCDA, and sensitivity/uncertainty analysis

### Takeaway
GIS-MCDA is a mature field (300+ refereed articles by 2004 alone). The practical core for a parcel platform is: standardise criteria, weight them (pairwise AHP or direct rating), aggregate (WLC as baseline, OWA to expose risk attitude, TOPSIS/PROMETHEE for ranking a shortlist), then run Monte Carlo weight perturbation plus variance-based global sensitivity analysis so users see rank stability, not one "true" map.

### Cited Findings
- Malczewski's survey of GIS-MCDA classifies the 1990–2004 literature and found 300+ refereed articles. Citation: Malczewski, J. (2006) "GIS-based multicriteria decision analysis: a survey of the literature", IJGIS 20(7):703–726, DOI 10.1080/13658810600661508. [VERIFIED-WEB] — [scilit record](https://www.scilit.net/publications/15ccd98a8bc617546e533cd487ced0e2); companion bibliography: [Malczewski 1990–2004 list](https://publish.uwo.ca/~jmalczew/list.htm)
- Reference textbook: Malczewski, J. & Rinner, C. (2015) *Multicriteria Decision Analysis in Geographic Information Science*, Springer, Advances in GIScience series, DOI 10.1007/978-3-540-74757-4, ISBN 978-3-540-74757-4 (ebook) / 978-3-540-74756-7 (print). Aimed at postgraduates and GIS/planning practitioners; covers theory, methods, tools and applications. [VERIFIED-WEB] — [MPDL catalogue](https://ebooks.mpdl.mpg.de/ebooks/Record/EB000945436); [UAM catalogue](https://biblioteca.izt.uam.mx/vufind/Record/978-3-540-74757-4/Description)
- OWA in GIS: Malczewski (2006) "Ordered weighted averaging with fuzzy quantifiers: GIS-based multicriteria evaluation for land-use suitability analysis", Int. J. Applied Earth Observation and Geoinformation 8(4):270–277, DOI 10.1016/j.jag.2006.01.003. Linguistic quantifiers ("at least a few", "most", "all") set the OWA order weights; changing them generates a continuum of decision strategies. Case study in Mexico. [VERIFIED-WEB, abstract level] — [science.gov topic page](https://www.science.gov/topicpages/f/fuzzy+linguistic+quantifiers)
- OWA generalises Boolean overlay (AND/OR) and WLC, letting decision makers choose between pessimistic (AND-like, no trade-off) and optimistic (OR-like) strategies; applied by Malczewski & Rinner to residential quality evaluation. [VERIFIED-WEB, record only] — [Toronto Metropolitan Univ. repository](https://rshare.library.torontomu.ca/articles/journal_contribution/Exploring_Multicriteria_Decision_Strategies_in_GIS_with_Linguistic_Quantifiers_A_Case_Study_of_Residential_Quality_Evaluation/14639916)
- AHP + quantifier-guided OWA integrated in ArcGIS (Boroushaki & Malczewski 2008); OWA plus fuzzy-majority for group decisions (Boroushaki & Malczewski 2010). [UNVERIFIED, index records only] — [science.gov](https://www.science.gov/topicpages/f/fuzzy+linguistic+quantifiers); [zhenzhi record](https://data.zhenzhi.com/details/1/907106974)
- Foundational method references [CANONICAL, NOT FETCHED]: Saaty, T.L. (1980) *The Analytic Hierarchy Process*, McGraw-Hill (pairwise comparisons, principal eigenvector weights, consistency ratio CR < 0.10); Yager, R.R. (1988) "On ordered weighted averaging aggregation operators in multicriteria decisionmaking", IEEE Trans. SMC 18(1):183–190; Hwang, C.L. & Yoon, K. (1981) *Multiple Attribute Decision Making*, Springer (TOPSIS: closeness to ideal and distance from anti-ideal); Brans, J.P. & Vincke, Ph. (1985) "A preference ranking organisation method", Management Science 31(6):647–656 (PROMETHEE outranking via pairwise preference functions and net flows); Roy, B. (1968/1991) ELECTRE family (concordance/discordance, veto thresholds); Jankowski, P. (1995) "Integrating GIS and MCDM methods", IJGIS 9(3):251–273.
- TOPSIS is the most-used distance-based MCDM method in social-housing evaluation; distance-based methods are about 21% of usage in that literature. [VERIFIED-WEB, abstract] — [J. Civil Eng. & Management review](https://journals.vilniustech.lt/index.php/JCEM/article/view/24425)
- PROMETHEE IV coupled with GIS was built into a multicriteria spatial DSS for emergency-station location (IJGIS 29(7), 2015). The method transfers to siting housing. [VERIFIED-WEB, abstract] — [Taylor & Francis](https://www.tandfonline.com/doi/abs/10.1080/13658816.2015.1025790)
- PROMETHEE applied to urban regeneration scenarios in Collegno (Turin, Italy), with social, environmental, mobility and economic criteria. [VERIFIED-WEB, record] — [ResearchGate](https://www.researchgate.net/publication/328963552_Multicriteria_Evaluation_of_Urban_Regeneration_Processes_An_Application_of_PROMETHEE_Method_in_Northern_Italy)
- Uncertainty/sensitivity: Feizizadeh & Blaschke (2014, IJGIS) compared AHP, WLC and OWA with Monte Carlo simulation (MCS) of weights treated as probability distributions, plus Dempster–Shafer theory. AHP was more accurate, but OWA maps had lower uncertainty. [VERIFIED-WEB, abstract] — [Bohrium/arXiv record](https://bohrium.dp.tech/paper/arxiv/813166248786395140)
- Feizizadeh, Omrani & Babaei Aghdam (GI_Forum 2015) paired fuzzy-AHP weights with MCS and variance-based global sensitivity analysis (GSA). The approach improved GIS-MCDA accuracy. [VERIFIED-WEB, abstract] — [GI_Forum DOI 10.1553/giscience2015s72](https://dx.doi.org/10.1553/giscience2015s72)
- Feizizadeh & Kienberger (2017), J. Environmental Planning & Management 60(11):2013–2035: spatially explicit variance-based GSA shows how much each criterion weight drives results, both per cell and overall. [VERIFIED-WEB] — [IDEAS/RePEc](https://ideas.repec.org/a/taf/jenpmg/v60y2017i11p2013-2035.html)
- Scalability critique: a 2026 arXiv preprint argues AHP/TOPSIS/overlay work for small problems but scale poorly to metro-level optimisation over thousands of parcels, and proposes multi-objective reinforcement learning instead. [UNVERIFIED, preprint, not peer-reviewed] — [arXiv 2602.03940](https://arxiv.org/pdf/2602.03940)

### Inferences
- Strengths/weaknesses by method (synthesis from the sources above plus canonical texts):
  - WLC is transparent and fast, and runs as one SQL expression per parcel. But it is fully compensatory: a great transit score can hide high heat risk. It also needs commensurate (standardised) scales.
  - AHP gives a structured way to elicit weights from stakeholders and a consistency check. But it suffers rank reversal and needs n(n−1)/2 judgements, which hurts beyond about 7–9 criteria. Weights also depend on criterion ranges, which AHP judgements often ignore.
  - OWA adds a single "risk attitude / trade-off" knob (orness). This suits a participatory web UI well: a slider from "all criteria must be good" to "any strong criterion is enough".
  - TOPSIS needs only weights and normalisation and ranks large sets fast. But its result is sensitive to the normalisation chosen, and adding or removing alternatives can reverse ranks.
  - PROMETHEE/ELECTRE handle non-compensation, indifference/preference thresholds and veto (e.g. "no site above heat-risk X"). But they are pairwise, O(n²) per criterion. That cost argues for applying them only to a shortlist (e.g. the top 200 parcels after WLC screening).
  - Fuzzy MCDA (fuzzy AHP, fuzzy membership standardisation) models vague thresholds like "near a station". It adds parameters that users must understand.
- A sound platform pipeline: (1) Boolean constraints (zoning excludes, protected areas, flood zones); (2) fuzzy/linear standardisation to 0–1; (3) weights from AHP or a participatory rating; (4) WLC/OWA score; (5) TOPSIS or PROMETHEE II on a shortlist; (6) Monte Carlo weight perturbation (e.g. Dirichlet sampling around elicited weights, 1,000+ runs) reporting each parcel's mean rank, rank interquartile range and probability of being in the top-k; (7) Sobol/variance GSA to show which weights matter.
- Monte Carlo weight perturbation is cheap on parcel tables (parcels × criteria matrix times a weights matrix), so it is feasible in-browser or server-side for tens of thousands of Milan parcels.

### Gaps
- Original full texts of Saaty, Yager, Hwang & Yoon, Brans, Roy were not fetched in this session. Their citations are from established knowledge, not re-checked online.
- I found no GIS-ELECTRE housing-siting application in this session.
- I found no peer-reviewed comparison of rank-reversal behaviour across methods on parcel-scale urban housing data.

## Peer-reviewed applications: affordable/social housing site selection and brownfield prioritisation

### Takeaway
Most housing-siting studies follow a GIS + AHP template: expert pairwise weights over accessibility, land cost, physical/environmental and social criteria, sometimes with TOPSIS ranking. Peer-reviewed Italian/Spanish GIS studies specifically on social-housing *site selection* were not found. The closest Italian work is PROMETHEE for regeneration and accessibility indices in Milan. Brownfield prioritisation uses web MCDA tools (EU Timbre) and participatory MCDA.

### Cited Findings
- Al-Shalabi, Mansor, Ahmed & Shiriff (FIG 2006): GIS + AHP housing-site suitability for Sana'a, Yemen. It frames site selection as balancing physical, economic, social, environmental and political criteria. Widely cited. [VERIFIED-WEB] — [FIG proceedings PDF](https://www.fig.net/resources/Proceedings//fig_proceedings/fig2006/papers/ts72/ts72_05_alshalabi_etal%20_0702.pdf)
- China: Fang, Y., Yuan, Y., Yin, M., Zhou, S., Xu, J. & Liu, K. (2022) "Site Selection of Affordable Housing in Direct Management Area under Jiangbei's New District in Nanjing", *Land* 11(9):1403. AHP + GIS. Site scores ranged 2.7792–3.8572. The authors frame the aims as jobs–housing balance and protecting low-income groups. The criteria list was not visible in the abstract. [VERIFIED-WEB, abstract] — [IDEAS/RePEc](https://ideas.repec.org/a/gam/jlands/v11y2022i9p1403-d898443.html); full text: [MDPI](https://www.mdpi.com/2073-445X/11/9/1403/)
- China (urban development land, not housing specifically): Zhang et al. (2013), Hefei. AHP weights, a composite index and an integrated overlay rule. [UNVERIFIED, secondary mention] — [SHS Conferences 2016](https://www.shs-conferences.org/articles/shsconf/pdf/2016/01/shsconf_psu2016_02001.pdf)
- Iran: low-income housing in Babolsar (Environment, Development and Sustainability, 2023, with a published correction). AHP weights socio-economic, physical, green-space and inclusiveness criteria. GIS overlays the layers, and TOPSIS ranks four candidate areas. [VERIFIED-WEB, abstract/record; authorship not confirmed] — [ResearchGate](https://www.researchgate.net/publication/355661170_Low-income_housing_location_based_on_affordable_criteria_Using_AHP_Model_and_GIS_Technique_Case_Study_Babolsar_City); [AMiner correction](https://aminer.org/pub/62bc2c095aee126c0fa82a97/correction-low-income-housing-location-based-on-affordable-criteria-using-ahp-model)
- Nepal (2026 preprint): civil servants' apartments in Kathmandu Valley. It combines AHP + QGIS with accessibility, land affordability, vacant land, planning constraints and environmental restrictions. Pareto frontier analysis finds accessibility–cost trade-offs, then TOPSIS ranks the sites. [UNVERIFIED, preprint] — [engrXiv 7773](https://engrxiv.org/preprint/view/7773)
- Fuzzy-AHP for affordable-housing "physical resilience" criteria (building condition, access to employment, green space), using Expert Choice software. [UNVERIFIED, book chapter] — [IntechOpen](https://www.intechopen.com/chapters/1122015)
- Malaysia: GIS-MCE for urban development sites (Yaakup & Abu Bakar 2004; Abdullah et al. 2004), cited secondarily. I found no Malaysian public-housing (PPR) GIS-MCDA paper in this session. [UNVERIFIED] — [SHS Conferences 2016](https://www.shs-conferences.org/articles/shsconf/pdf/2016/01/shsconf_psu2016_02001.pdf)
- Spain: GIS + multicriteria socio-spatial analysis of 34 medium-sized inland Spanish cities (Land 12(6):1115, 2023). It identifies vulnerable areas rather than housing sites. [VERIFIED-WEB, abstract] — [MDPI Land](https://www.mdpi.com/2073-445X/12/6/1115)
- Brownfields: the EU FP7 Timbre Brownfield Prioritization Tool is a web-based MCDA tool. It ranks a portfolio of sites by likelihood of successful, sustainable regeneration or by user-defined objectives. It was tested in 5 cases across Germany, the Czech Republic and Romania (J. Environmental Management 166, 2015). [VERIFIED-WEB, record only; full text 403] — [Cardiff ORCA](https://orca.cardiff.ac.uk/110272); [Ca' Foscari IRIS](https://iris.unive.it/handle/10278/3687677)
- Brownfields, UK: a prototype WebGIS DSS for city-region brownfield planning. It has three modules: land-use potential, contamination/geotechnical risk, and economic viability. [VERIFIED-WEB, record] — [Cranfield CERES](https://dspace.lib.cranfield.ac.uk/handle/1826/20548)
- Brownfields, Czech Republic (2025): an MCDA of regional regeneration potential. The number of sites, former land use and public ownership correlated most with regeneration potential, and infrastructure distance less so. The paper cites Škrabal & Vybíral, *Land Use Policy* 72:13–24, on participatory MCDA for brownfield redevelopment. [VERIFIED-WEB] — [Acta academica karviniensia 2025](https://aak.slu.cz/artkey/aak-202501-0006_regional-potential-for-brownfield-regeneration-in-the-czech-republic-using-multi-criteria-decision-analysis.php)
- A recent brownfield/land-reuse MCDA paper (J. Environmental Management, 2023, NERC repository). [UNVERIFIED, content not read] — [NORA PDF](https://nora.nerc.ac.uk/id/eprint/536389/1/1-s2.0-S0301479723022545-main.pdf)
- Milan policy context: PGT Milano 2030 summary. It earmarks 9 areas for social/public housing (about 1,300 dwellings), on top of about 6,200 dwellings in the rail-yard (scali) regeneration and other approved plans. Milan has about 63,000 public housing units: 35,000 ALER (Region) and 28,000 MM (Comune), much of it run down. [VERIFIED-WEB, search snippet of official PDF; check against the current approved PGT] — [Comune di Milano, Sintesi PGT Milano 2030](https://pgt-test.ecaas.comune.milano.it/sites/default/files/allegati%20home/SintesiPGT_Milano2030.pdf)
- Milan rail-yard accord (2017): 7 disused yards, about 1,250,000 m², with at least 30% of volume for social and agreed-price housing. [UNVERIFIED, secondary] — [ASPESI 2021 slides](https://www.aspesi-associazione.it/public/files/2021/Evento%20PGT/SINTESI%20INTERVENTI%20E%20SLIDES.pdf)
- Social-housing share in Italy is only about 2–3% of households. [VERIFIED-WEB, snippet] — [OECD 2023, Housing in Italy](https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/10/housing-in-italy-through-the-telescope-and-the-microphone_111d5b6d/42295a0d-en.pdf)

### Inferences
- Recurring criteria across these studies:
  - accessibility (transit, jobs, schools, health);
  - land cost / affordability;
  - availability (vacant or underused land);
  - planning constraints;
  - environmental hazards (flood, slope, pollution);
  - green space;
  - socio-economic context (deprivation, social mix).
- For Milan, the user's layers map onto these directly: transit stations, services, green index, heat risk, rents, PGT regeneration areas, brownfields.
- Weighting is almost always expert AHP. Few studies use resident or participatory weights. A participatory platform could stand out by collecting stakeholder weights, then showing consensus and dispersion (OWA/fuzzy-majority group aggregation, as in Boroushaki & Malczewski 2010).
- Rents serve as a double-edged criterion. High rents mean higher need and better social mix in wealthy areas, but they also mean costlier land. Model them explicitly as two separate criteria, or as a constraint plus a criterion.

### Gaps
- I found no peer-reviewed GIS-MCDA paper on social-housing *site selection* in Italy or Spain. Next searches to try: "edilizia residenziale sociale" + "analisi multicriteri" + GIS, and "vivienda social" + "localización" + SIG.
- I did not find a UK or US peer-reviewed affordable-housing site-selection GIS-MCDA paper in this session. UK/US practice appears mostly in planning documents (see the next sections).
- The Sharghi et al. (2023) AHP-TOPSIS-GIS affordable-housing paper is cited in the JCEM review, but I could not locate the original.
- The Fang et al. (2022) criteria and weights need the MDPI full text.

## Accessibility measures for housing suitability: 2SFCA/E2SFCA, gravity, cumulative opportunities, 15-minute city, job access by transit

### Takeaway
Use cumulative-opportunity counts (by walk/transit isochrone) for interpretability, and E2SFCA where supply competition matters (school places, GP capacity, childcare). For Milan, two ready proximity indices already exist: IAPI, tested in Crescenzago, and the OSM-based NEXI covering all of Italy. They can benchmark or seed a 15-minute indicator.

### Cited Findings
- E2SFCA: Luo, W. & Qi, Y. (2009) "An enhanced two-step floating catchment area (E2SFCA) method for measuring spatial accessibility to primary care physicians", *Health & Place* 15(4):1100–1107, DOI 10.1016/j.healthplace.2009.06.002. It adds distance-decay weights by travel-time zone inside the catchment. It is a special case of the gravity model and is easy to implement in GIS. It builds on Luo & Wang (2003) and Radke & Mu (2000). [VERIFIED-WEB] — [Wikipedia 2SFCA](https://en.wikipedia.org/wiki/Two-step_floating_catchment_area_method); [peeref record](https://peeref.com/works/16427815)
- 2SFCA mechanics: step 1 computes each supply point's supply-to-demand ratio within its catchment. Step 2 sums, for each demand location, the ratios of the supplies reachable within its catchment. [VERIFIED-WEB] — [Wikipedia 2SFCA](https://en.wikipedia.org/wiki/Two-step_floating_catchment_area_method)
- IAPI (Inclusive Accessibility by Proximity Index): Pucci, Carboni & Lanza (2022), FrancoAngeli journal (in Italian). It is based on "basic accessibility" to essential daily services at neighbourhood scale and was tested in the Crescenzago district of Milan. [VERIFIED-WEB, record] — [FrancoAngeli](https://www.francoangeli.it/riviste/articolo/71632)
- NEXI (NExt proXimity Index): Olivari & Cipriani, *Journal of Urban Mobility* (Dec 2023). It measures walking proximity to services on a hexagonal grid from OpenStreetMap, is available for all of Italy, and was tested in Ferrara and Bologna. [VERIFIED-WEB, abstract] — [DOAJ](https://doaj.org/article/3656e977d5b243fa853496caa29cd898)
- Enel X 15 Minute City Index: a commercial interactive map built with scientific support from the University of Florence. It covers 13 service categories for Italian city micro-districts. [VERIFIED-WEB, press release] — [Enel X press release](https://corporate.enelx.com/es/media/press-releases/2021/12/enel-x-launches-the-15-minute-city-index)
- A 2025 study (journal *Computers*) used a customised 15-min City Score Toolkit to compare day vs night service access in Milan. [UNVERIFIED, snippet] — [search result list](https://www.moreno-web.net/?p=16061)
- Accessibility method references [CANONICAL, NOT FETCHED]:
  - Hansen, W.G. (1959) "How accessibility shapes land use", J. American Institute of Planners 25(2):73–76 (gravity accessibility A_i = Σ_j O_j f(c_ij)).
  - Luo, W. & Wang, F. (2003) Environment and Planning B 30(6):865–884 (2SFCA).
  - Geurs, K.T. & van Wee, B. (2004) "Accessibility evaluation of land-use and transport strategies", J. Transport Geography 12(2):127–140 (taxonomy: infrastructure-, location-, person- and utility-based; cumulative opportunities vs gravity).
  - Moreno, C. et al. (2021) "Introducing the 15-minute city", Smart Cities 4(1):93–111.
- Methods tools [CANONICAL, NOT FETCHED]: transit job accessibility is typically computed with GTFS-based travel-time matrices (e.g. the r5r / R5 routing engine from Conveyal; OpenTripPlanner) over a departure-time window. ATM Milano publishes GTFS. Check the current licence before use.

### Inferences
- Recommended indicators per parcel (or per H3 hexagon, then joined to parcels):
  - cumulative jobs reachable within 30/45 min by transit (median over the 7–9 am window);
  - count of essential-service categories within 15 min walk;
  - E2SFCA for capacity-constrained services (schools, nurseries, GPs);
  - network distance to the nearest metro/rail station.
- Cumulative measures are easiest to explain to participants. Gravity/E2SFCA are more defensible but need decay parameters, which should be included in the sensitivity analysis.
- New housing changes demand in E2SFCA. A two-way model is possible: recompute accessibility after allocating units, to avoid overloading local services. This links directly to the allocation optimisation below.

### Gaps
- No Milan-specific transit job-accessibility study was retrieved. Workplace data would come from ISTAT (census of enterprises/local units). Availability at a fine scale was not checked.
- The IAPI and NEXI formulas were not read in full.

## Development capacity, soft-site analysis, and ownership constraints

### Takeaway
California housing-element practice offers the most codified parcel-level method. Capacity = parcel area × allowed FAR (or density) × a realistic-yield factor. "Soft" = existing built floor area at or below about 30% of allowed. Then apply filters (minimum size, excluded uses, public/critical infrastructure, historic) and model lot consolidation. Raw soft-site counts overstate real supply.

### Cited Findings
- San Francisco *Affordable Housing Sites Analysis and Strategies* (Dec 2025) [VERIFIED-WEB via search summary only; PDF text could not be extracted in this session]:
  - parcels built to ≤30% of allowable floor area are "soft";
  - about 3,410 viable sites with capacity for about 247,000 affordable units;
  - stand-alone sites are non-residential parcels ≥8,000 sq ft (1,204 sites, 60% of capacity);
  - groups of adjacent parcels that become viable only when combined are also counted.
  — [SF Planning AHSAS final report](https://sfplanning.org/sites/default/files/documents/citywide/AHSAS-final-report-2025.pdf)
- San Francisco's housing-element sites appendix excludes public schools, parks and critical public infrastructure, unless the agency has identified housing opportunities there. [VERIFIED-WEB, snippet] — [SF Housing Element Appendix B](https://sfplanning.s3.amazonaws.com/archives/sfhousingelement.org/files/AppendixB.pdf)
- Mill Valley assumes a 70% average realistic yield on zoned capacity, and places parcels with ≥10-unit capacity in the moderate-income category. [VERIFIED-WEB, snippet] — [Mill Valley Appendix C](https://cityofmillvalley.gov/DocumentCenter/View/3256/Appendix-C-Sites-Capacity-Analysis-and-Inventory?bidId=)
- Contra Costa County counts a site as adequate for lower-income housing when zoned ≥30 units/acre and able to fit ≥20 units. Its inventory flagged 980 sites as questionable after checking real development potential. [VERIFIED-WEB, snippet] — [Contra Costa Land Inventory](https://www.contracosta.ca.gov/DocumentView.asp?DID=3224)
- California HCD guidance asks for more on non-vacant/underutilised sites. Jurisdictions must describe existing uses and evaluate how far those uses impede redevelopment. Evidence includes developer interest, lot consolidation potential and lot splits. [VERIFIED-WEB, snippet] — [HCD Analysis of Sites and Zoning](https://www.hcd.ca.gov/planning-and-community-development/housing-elements/building-blocks/analysis-of-sites-and-zoning)
- Milan PGT 2030 removed limits on converting productive (industrial) functions to other urban uses. This is relevant to soft-site eligibility of disused productive buildings. [UNVERIFIED, practitioner comment] — [ASPESI 2021](https://www.aspesi-associazione.it/public/files/2021/Evento%20PGT/SINTESI%20INTERVENTI%20E%20SLIDES.pdf)
- Public ownership is among the strongest correlates of brownfield regeneration potential (Czech 2025 study). [VERIFIED-WEB] — [AAK 2025](https://aak.slu.cz/artkey/aak-202501-0006_regional-potential-for-brownfield-regeneration-in-the-czech-republic-using-multi-criteria-decision-analysis.php)

### Inferences
- Parcel formulas for Milan:
  - existing GFA ≈ footprint area × floors, where floors = height / about 3.0–3.3 m;
  - existing FAR = existing GFA / parcel area;
  - allowed GFA = parcel area × index from PGT. The base index (IT) is 0.35 m²/m², rising to about 1 m²/m² with transfers/ERS, and higher near transit nodes. Exact values were not verified here; extract them from the PGT Piano delle Regole.
  - utilisation = existing / allowed. Soft if ≤0.3, adapted from SF.
  - potential units = (allowed − existing GFA) × yield (about 0.7) / average unit GFA (about 65–75 m²).
- Height-derived GFA is noisy (mixed floor heights, roofs, basements). Treat it as uncertain and include it in the Monte Carlo runs.
- Ownership (public: Comune/MM, ALER, Demanio, FS-Sistemi Urbani; private) should act as a hard filter or a strong criterion, because acquisition cost dominates social-housing feasibility. The Agenzia del Demanio and the Comune's real-estate lists are candidate data sources (not checked).
- Lot consolidation: cluster adjacent soft parcels (shared boundaries, same block) and evaluate them jointly. The SF report shows this adds meaningful capacity.

### Gaps
- The PGT Milano 2030 indices (IT, ERS bonuses, transit-node densification rules) were not verified in this session. They need primary extraction from the PGT Piano delle Regole / NTA.
- No peer-reviewed (as opposed to planning-document) validation of soft-site thresholds was found, i.e. what share of flagged soft sites actually redevelop.
- Cadastral ownership data access in Italy (Agenzia delle Entrate catasto) for public use was not checked.

## Optimisation and location-allocation: integer programming and multi-objective (NSGA-II) alternatives

### Takeaway
Allocating units of different household profiles to sites is a capacitated assignment/transportation problem, solvable exactly as a MILP for city-scale instances (hundreds of sites × a handful of profiles). NSGA-II and similar evolutionary methods are established for spatial land-use allocation and can produce a Pareto set of alternative plans for participatory comparison. I found no published social-mix housing-allocation MILP.

### Cited Findings
- A recent paper builds synthetic populations with IPF and integer programming, then assigns households to residences via a MILP. The MILP balances allocation volume, housing-quality fit and census-tract targets. [VERIFIED-WEB, abstract; Optimization Online, Aug 2026] — [Optimization Online](https://optimization-online.org/2026/08/synthetic-population-generation-and-georeferenced-household-allocation-via-iterative-proportional-fitting-and-integer-programming/)
- A joint synthetic housing–household inventory uses a hierarchical multi-objective MILP: building-capacity feasibility first, then marginal consistency, then match quality. It oversamples the candidate pool to meet group targets. [UNVERIFIED, arXiv preprint] — [arXiv 2605.17031](https://arxiv.org/pdf/2605.17031)
- Practitioner case: a MILP for resettling 1,200+ families into 1,500 units, using an admissibility matrix to prune invalid household–unit pairs. [UNVERIFIED, vendor blog] — [DigitalSense blog](https://www.digitalsense.ai/blog/housing-allocation-with-mixed-integer-optimization)
- Fairness in house allocation (AAAI): algorithmic group-fairness formulations. [VERIFIED-WEB, record] — [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/38753/42715); [arXiv 2511.07022](https://arxiv.org/html/2511.07022)
- NSGA-II land-use allocation: "Spatial multi-objective land use optimization: extensions to the non-dominated sorting genetic algorithm-II" (Cao et al., IJGIS 2011; Tongzhou New Town, Beijing). Objectives: conversion cost, accessibility and land-use compatibility. It searched tens of thousands of candidate plans for Pareto-optimal trade-offs. [VERIFIED-WEB, record; author/year from canonical knowledge] — [SMU InK](https://ink.library.smu.edu.sg/sis_research/5411)
- NSGA-II for district land use in Tabriz (Iran). Eight land-use types, including housing classes; objectives FAR, economic profit, compatibility and compactness. Reported gains of about 13% FAR and 21% profit. [VERIFIED-WEB, abstract, in Persian] — [GAIJ](https://gaij.usb.ac.ir/article_5581.html)
- Further NSGA-II land-use allocation studies: Sheffield Hallam (Shura) and Córdoba (Helvia, sub-regional sustainable allocation), and a Geo-spatial Information Science 2018 article. [VERIFIED-WEB, records] — [SHU](https://shura.shu.ac.uk/34897/); [UCO Helvia](https://helvia.uco.es/handle/10396/14893); [DOAJ GSIS 2018](https://doaj.org/article/08d8377d434041b5bae40d3080f84743)
- A genetic algorithm hybridised with PROMETHEE for multicriteria localisation. [VERIFIED-WEB, record] — [arXiv 2002.04068](https://arxiv.org/pdf/2002.04068)
- Kathmandu preprint: uses a Pareto frontier (accessibility vs cost) before TOPSIS ranking. [UNVERIFIED, preprint] — [engrXiv 7773](https://engrxiv.org/preprint/view/7773)
- Canonical references [CANONICAL, NOT FETCHED]:
  - Deb, K., Pratap, A., Agarwal, S. & Meyarivan, T. (2002) "A fast and elitist multiobjective genetic algorithm: NSGA-II", IEEE Trans. Evolutionary Computation 6(2):182–197.
  - Church, R. & ReVelle, C. (1974) "The maximal covering location problem", Papers of the Regional Science Association 32:101–118.
  - Church, R.L. & Murray, A.T. (2009) *Business Site Selection, Location Analysis and GIS*, Wiley.
  - Haimes et al. ε-constraint method for multi-objective programming.

### Inferences
Proposed MILP for the Milan platform:
- Variables: x_{s,p} ∈ ℤ≥0 are the units of household profile p on site s. y_s ∈ {0,1} means site s is activated.
- Constraints:
  - capacity: Σ_p a_p x_{s,p} ≤ Cap_s y_s, where a_p is the GFA per unit;
  - budget: Σ_s (FixedCost_s y_s + Σ_p c_{s,p} x_{s,p}) ≤ B, where cost includes acquisition (zero for public land) plus construction;
  - demand: Σ_s x_{s,p} ≥ D_p (or ≤);
  - social mix per site: L_p Σ_q x_{s,q} ≤ x_{s,p} ≤ U_p Σ_q x_{s,q}, which is linear;
  - district caps to avoid concentration: Σ_{s∈d} Σ_p x_{s,p} ≤ K_d;
  - minimum viable project size: x_s ≥ m y_s;
  - service load: new demand ≤ residual capacity of schools/nurseries in the catchment, which links to the E2SFCA layer.
- Objective: maximise Σ suitability_s × units (from the MCDA score), or a profile-specific suitability (e.g. families weight schools and green space, elderly weight health and ground-floor access). Alternatively, minimise cost subject to minimum suitability.
- Pareto alternatives: the ε-constraint method over the MILP (e.g. maximise suitability for cost budgets B1…Bk) gives an exact, explainable Pareto front for 2–3 objectives. NSGA-II is better when objectives are non-linear (compactness, post-allocation accessibility recomputation, segregation indices) or with more than 3 objectives.
- Solvers: open-source CBC/HiGHS (via PuLP, OR-Tools or Pyomo) should handle about 10³ sites × 5 profiles in seconds. NSGA-II is available in pymoo (Python). These are tool facts from canonical knowledge, not fetched here.
- Presentation: show 4–6 representative Pareto solutions (e.g. knee point plus extremes) on maps, so participants compare plans instead of receiving one optimum. This matches the participatory aim of the project.

### Gaps
- I found no peer-reviewed social-mix MILP for social-housing allocation across sites. The formulation above is a synthesis, not a cited model.
- I found no NSGA-II study specifically for housing-unit allocation across parcels with social-mix constraints.
- The arXiv 2602.03940 RL claim of scalability advantages is from a non-peer-reviewed preprint.
