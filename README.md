# School spending and district income

An interactive map and scatterplot of public school spending per student and the income of households living within school district boundaries, covering the 50 states and Washington, D.C.

**[Explore the website](https://kevinhegg.github.io/school-spending-and-income/)** · [Methodology](METHODOLOGY.md) · [Sources](SOURCES.md) · [Download CSV](data/districts.csv) · [Data dictionary](data/data-dictionary.md)

The map shows where different combinations of income and spending occur. The linked scatterplot makes their relationship easier to inspect. Select a state and district type, then select a district on either view to see its income estimate, current spending per student, enrollment, and local revenue context.

## What is being compared?

| Measure | Meaning | Period and source |
| --- | --- | --- |
| Current school spending per student | Census's published current elementary-secondary spending per pupil, supported by federal, state, and local funds. It excludes capital outlay and debt service. | Fiscal year 2024; [Census Annual Survey of School System Finances](https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html) |
| Median household income | Income of all households residing within the district boundary, including households without children in public schools. | ACS 2020–2024 five-year estimate, expressed in 2024 dollars; [table B19013](https://data.census.gov/table/ACSDT5Y2024.B19013) |

This is a comparison of school resources and resident household affluence. It does not measure the percentage of household income paid in school taxes. The local revenue figures in district details include multiple revenue sources and should not be read as a tax rate or a measure of residents' willingness to pay. See the [finance definitions and limitations](METHODOLOGY.md#spending-and-local-revenue).

## Reading the views

- **Colors use the same national benchmarks in every state:** $80,734 median household income and $17,619 current spending per student. These are published national values, not averages or medians calculated from the displayed districts. The income benchmark comes from [ACS B19013](https://data.census.gov/table/ACSDT5Y2024.B19013); the spending benchmark comes from the [Census FY2024 release](https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html).
- **The four colors describe combinations:** lower income/lower spending, higher income/lower spending, lower income/higher spending, and higher income/higher spending. “Higher” includes values equal to the benchmark. The categories are descriptive, not school quality ratings or statistical significance tests.
- **One scatterplot mark represents one district.** Districts are unweighted observations; enrollment does not determine mark size. Income uses a linear axis. Spending uses a logarithmic axis, so equal vertical distances represent equal proportional changes.
- **Triangles mark bounded income estimates.** The Census reports these as $250,000 or more or $2,500 or less. Their positions show the published bounds, not exact district medians.
- **Hatching marks unavailable comparisons.** A district remains on the map when it lacks an eligible spending value or a usable income estimate.
- **District types matter.** The default shows unified and elementary districts. Switch to unified and secondary districts to inspect high-school district geography, or to unified districts only. Elementary and secondary districts can overlap, so they are not painted together.

The published dataset contains **13,305 geographic districts**, of which **12,960** have usable income and eligible positive spending and enrollment values. The default unified-plus-elementary view includes **12,577 matched districts**. These are project coverage counts, documented in [data/metadata.json](data/metadata.json); changing the layer changes which districts are visible.

## Interpretation

Dollar amounts are not adjusted for geographic differences in wages or living costs, student needs, or grade spans. School finance rules and accounting practices also differ across states. Income estimates have sampling uncertainty, and the five-year income period does not describe precisely the same time window as FY2024 school finances. A district's position cannot, by itself, establish school quality, fiscal effort, efficiency, or the causal effect of household income on spending. The [methodology](METHODOLOGY.md) explains these limits and the handling of unusual source values.

## Downloads and documentation

- [District data: CSV](data/districts.csv) or [JSON](data/districts.json)
- [Field definitions and missing-value rules](data/data-dictionary.md)
- [Dataset metadata](data/metadata.json) and [source provenance](data/source-provenance.json)
- [High-resolution map and scatterplot image](assets/education-spending-and-income.png)
- [Full methodology](METHODOLOGY.md) and [primary source links](SOURCES.md)

Import district identifiers and state FIPS codes as **text** when opening the CSV in a spreadsheet, so leading zeros remain intact.

## Run locally

This is a static website. From the repository directory, start a local server:

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000/> in a modern browser. No application server, account, API key, or build service is required. The JavaScript dependencies are included in the repository.

To regenerate the public CSV, JSON, and associated metadata from the included approved data snapshot:

```sh
python3 scripts/export-data.py
```

The export script uses Python 3.9 or newer and its standard library. Add `--check` to verify existing exports without rewriting them. It reproduces the downloadable tables from the included snapshot; it is not a complete pipeline for downloading new Census releases, reconciling changed district boundaries, or rebuilding the original source joins. See [reproducibility and updates](METHODOLOGY.md#reproducibility-and-updates).

The site is intended for GitHub Pages publication from the repository's `main` branch and root directory. The `.nojekyll` file marks it as ordinary static content.

## Credits

Data and district boundaries: U.S. Census Bureau, with NCES documentation used to interpret school district geography and enrollment. This is an independent visualization and does not imply agency endorsement. Third-party JavaScript licenses are reproduced in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md); those licenses apply to the named dependencies.

