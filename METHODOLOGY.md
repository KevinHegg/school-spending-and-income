# Methodology

This project compares current public school spending per student with median household income inside school district boundaries. Its map and scatterplot are descriptive tools for exploring geographic patterns. The data snapshot was assembled from sources retrieved on **October 8, 2026**. Source URLs, vintages, and hashes are recorded in [source provenance](data/source-provenance.json).

## Unit of analysis and coverage

The unit is a **geographic school district**, represented by a seven-character Census district identifier. Coverage includes the 50 states and Washington, D.C. Puerto Rico, other territories, and Census “School District Not Defined” areas are excluded.

District boundaries come from the Census Bureau's [2024 cartographic boundary files at 1:500,000 scale](https://www.census.gov/geographies/mapping-files/2024/geo/carto-boundary-file.html). The school district geography represents school year 2023–2024; [NCES boundary documentation](https://nces.ed.gov/programs/edge/Geographic/DistrictBoundaries) explains the boundary collection and vintages.

The published district data contain the following coverage, calculated from the assembled snapshot:

| Geographic district type | Geographic rows | Rows with an eligible comparison |
| --- | ---: | ---: |
| Unified | 10,872 | 10,692 |
| Elementary | 1,952 | 1,885 |
| Secondary | 481 | 383 |
| **All types** | **13,305** | **12,960** |

An eligible comparison requires a usable positive household-income estimate or bound, positive published spending per student, positive enrollment, and a finance record classified as a regular elementary, secondary, or elementary-secondary school system. Of the 12,960 eligible comparisons, 44 have bounded income estimates rather than exact published medians.

The default map combines unified and elementary districts: 12,824 geographic areas and 12,577 eligible comparisons. The alternative unified-plus-secondary view has 11,353 areas and 11,075 eligible comparisons. Unified districts alone have the counts shown in the table above. These layers help separate potentially overlapping elementary and secondary district geography; they should not be combined to calculate a population total or an average household income.

District type in the display comes from the geographic file. A finance record's grade responsibility can differ from its geographic layer classification. The project does not silently change the boundary classification to match the finance code.

## Spending and local revenue

### Current spending per student

The main spending measure is **`PPCSTOT`**, the published current elementary-secondary spending per pupil in the [FY2024 Census individual-unit finance tables](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24t.xlsx). It is already expressed in **dollars per student**. The project uses this published value directly; it does not multiply it by 1,000 or substitute its own ratio of an expenditure total to enrollment.

The website uses “current operating spending” as a reader-facing description. The precise statistical definition is Census's current elementary-secondary spending measure. It covers instruction, support, and other eligible elementary-secondary activities funded from federal, state, and local sources. Capital outlay, debt service, and nonelementary-secondary programs such as adult education and community services are outside the displayed per-pupil measure. Census also makes exclusions for spending on students outside the fall-membership denominator. State payments made on behalf of districts can be estimated or available only at state level; state-specific treatment is documented by Census. Consult the [FY2024 technical documentation, especially Appendix B and the per-pupil definitions](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx).

FY2024 generally covers July 1, 2023 through June 30, 2024. Alabama and D.C. use October 2023 through September 2024; Nebraska, Texas, and Washington use September 2023 through August 2024. Enrollment is generally fall 2023 membership from the NCES Common Core of Data school-year 2023–2024 provisional agency file, subject to Census adjustments. These timing and membership conventions come from the same [Census technical documentation](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx).

### Local revenue context

District details also show local revenue per student and the local share of total school-system revenue:

| Displayed quantity | Calculation or source | Unit |
| --- | --- | --- |
| Current spending per student | Published `PPCSTOT` | Dollars per student |
| Enrollment | Published `ENROLL` / `V33`, subject to Census adjustments | Students in fall membership |
| Local revenue per student | `TLOCREV × 1,000 ÷ ENROLL`, for positive enrollment; rounded to a whole dollar for display | Dollars of local-source revenue per fall-member student |
| Local share of revenue | Published `PCTLTOT` | Percent, on a 0–100 scale |

`TLOCREV` is an aggregate originally reported in thousands of dollars, hence the multiplication by 1,000. Once an aggregate has been normalized to dollars, it must not be multiplied again. Local revenue per student is a project calculation; the main spending measure is a published Census rate.

Local-source revenue includes local taxes, contributions from parent governments, interdistrict receipts, tuition and fees, and other local-source receipts. The numerator can support activities or recipients outside the displayed enrollment denominator. State funding structures, transfers between school systems, and accounting practices affect these figures. The [Census revenue definitions](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx) are essential for detailed comparisons.

These local revenue measures do not establish how much district residents pay in school taxes or what fraction of their income they contribute. Dividing spending per student by median household income would mix different denominators and would not yield a household tax-burden measure. No such ratio is used for the map's colors.

## Household income and uncertainty

Income is the [ACS 2020–2024 five-year B19013 estimate](https://data.census.gov/table/ACSDT5Y2024.B19013): median household income in the past 12 months, expressed in 2024 inflation-adjusted dollars. Its universe is **all resident households within each school district boundary**, including households without children and households whose children attend other schools. The estimate is `B19013_001E`; the accompanying margin of error is `B19013_001M`. See the [official variable definitions](https://api.census.gov/data/2024/acs/acs5/groups/B19013.html) and [summary-file documentation](https://www.census.gov/programs-surveys/acs/data/summary-file.html).

A five-year ACS estimate pools survey information collected across 2020–2024. It is not a measurement of income solely during FY2024. Although both sources use a 2024 reference, their time windows differ.

Where available, district details show the Census **90% margin of error**. The display identifies when the interval formed by the estimate plus or minus that margin crosses the national income benchmark. Color assignment still uses the published point estimate. This interval note is a prompt to consider uncertainty, not a formal test of a district's difference from the national estimate; the national estimate also has sampling uncertainty.

The national household-income benchmark is **$80,734**, with a published 90% margin of error of **±$166**. It is the national ACS estimate, not a mean or median of district medians.

### Bounded and unavailable estimates

The Census reports some medians only as an upper or lower bound. In this snapshot, 43 districts are reported as **$250,000 or more**, and one as **$2,500 or less**. The data retain the bound indicator. The scatterplot positions these observations at $250,000 or $2,500 and uses triangles to distinguish them from exact estimates. They must not be treated as exact medians in a correlation or regression. See the [Census notes on estimate and annotation values](https://www.census.gov/data/developers/data-sets/acs-1year/notes-on-acs-estimate-and-annotation-values.html).

Unavailable estimates remain missing; they are not replaced with zero. The ACS source contains 13,304 real school district rows after scope exclusions. All have matching district geometry. The geographic file additionally contains Wyandanch Union Free School District, New York (`3631800`), for which this B19013 source has no row. Its income remains unavailable. Other missing estimates and ineligible finance records also remain visible as hatched areas when their layer is selected.

## Joining the sources

Finance records are school systems or agencies; they are not inherently polygons. The project joins finance `NCESID` to the seven-character school district geographic identifier **by exact identifier**, preserving leading zeros. It does not match on names or assign a school system to the polygon of its associated county. Pseudo-district and agency identifiers can differ; [NCES composite district documentation](https://nces.ed.gov/programs/edge/docs/EDGE_SDBOUNDARIES_COMPOSITE_FILEDOC.pdf) explains these cases. An unmatched identifier stays unmatched unless a documented crosswalk is available.

The original finance file has 14,077 school-system records. The current-spending comparison admits regular finance systems with `SCHLEV` codes `01`, `02`, or `03`, together with the positive-value rules above. Service agencies, vocational/special-only systems, and nonoperating systems are outside this comparison. Nongeographic or unmatched finance records are not given invented locations. Geography rows without eligible matched finance remain in the public dataset, with comparison spending unavailable.

Census government-finance scope includes governmental school systems. Nongovernmental charter operators are outside that scope, though payments to them may appear in sponsoring districts' spending. This is not a complete school-level census of all public or charter schools. The release does not supply a charter/non-charter flag for these records, and the project does not infer one from names. See the [Census scope documentation](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx).

## Colors, axes, and selection

Both views use two fixed national reference values:

| Reference | Value | Source |
| --- | ---: | --- |
| National median household income | $80,734 | ACS 2020–2024 B19013 national estimate |
| National current spending per student | $17,619 | [Census FY2024 national release](https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html) |

An income or spending value **at or above** its reference belongs to the “higher” side; a value below it belongs to the “lower” side. Combining those two classifications produces four colors. Benchmarks stay fixed when the user changes states or layers. The spending benchmark is a published national per-student measure, not the median district's spending and not an unweighted average of the plotted districts.

The scatterplot uses a linear income axis and a logarithmic spending axis. Equal vertical distances therefore represent equal proportional changes in spending. The log axis allows very low and very high published positive values to remain visible. Each eligible district is one mark; mark size does not encode enrollment. A dense pattern consequently describes districts, not the number of students experiencing a spending level. Axes can change extent with the selected geography, while the benchmark values and color rules remain the same.

Selecting a district links the map, scatterplot, and district details. A state-level district selector offers another way to inspect small districts. Missing comparisons are hatched on the map and absent from the scatterplot. The project does not fit a regression, compute a causal estimate, or rank schools by these colors.

## Source anomalies and comparability

Published spending values were checked between Census's individual-unit XLSX and TXT files. There were no substantive numeric discrepancies after disregarding insignificant floating-point serialization differences. Agreement between file formats verifies transcription, not the underlying accuracy or comparability of a district's accounting.

Unusually low spending values below **$1,000 per student** are retained and receive a source-review note in district details. This is an analyst screening rule, not an official Census quality flag and not a declaration that a value is erroneous. Very high values are also retained; per-student figures can be sensitive to small enrollment denominators.

The Census [data-item flags](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24f.txt) distinguish reported, alternative-source, adjusted, imputed, missing, and not-applicable items. Some positive published enrollment values carry missing or not-applicable flags. The website's displayed enrollment preserves the numeric source value and does not certify that denominator as confirmed. The full Census flag matrix is not reproduced in the district card; review the original flags and state notes before drawing conclusions from an unusual record. Summary variables such as `PPCSTOT` do not have their own source flags in this release.

Dollar values have **no adjustment for geographic price or labor-cost differences**. The analysis also does not adjust for student poverty, disability, English-learner status, transportation distances, district size, grade spans, capital needs, or accounting differences. These factors can influence spending. The Census describes several interstate comparability issues in its [technical documentation](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx).

The views can identify places worth examining more closely. They cannot independently establish school quality, efficiency, fairness, local tax effort, or the effect of household income on spending.

## Display geometry

The original cartographic files already generalize boundaries. The website further simplifies them for fast national display, retaining topology junctions and protecting very small district shapes. All 13,305 district features are retained. Coastlines, tiny islands, and boundary details are not preserved at source precision. The simplification process reported nine residual segment intersections; this is a display product, not a boundary dataset for spatial analysis or legal use.

The stored display geometry uses compact encoding and coordinate quantization. These operations do not change the published data values or district identifiers. For precise boundaries, use the linked [Census source files](SOURCES.md#district-boundaries), not polygons extracted from the visualization.

## Reproducibility and updates

The repository includes the approved data snapshot in [src/education-values.json](src/education-values.json), human-readable [CSV](data/districts.csv) and [JSON](data/districts.json) downloads, a [data dictionary](data/data-dictionary.md), [metadata](data/metadata.json), and [source provenance](data/source-provenance.json). The provenance records identify original Census files with URLs, retrieval dates, and SHA-256 hashes so the source snapshot can be distinguished from later revisions.

Running `python3 scripts/export-data.py` regenerates the downloadable tables and their associated metadata from the included snapshot. It does not automatically redownload all original Census files, rerun source normalization, construct a new identifier crosswalk, or rebuild generalized geometry. Reproducing or updating the entire analysis requires repeating those source-specific steps and checking changed district identities, source flags, periods, and coverage. Do not replace a new year's finance or income file while leaving the other vintages and labels unchanged.

The interactive display and downloadable data describe this fixed snapshot. They are not a live feed, and no update schedule is implied.

