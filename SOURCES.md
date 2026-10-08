# Sources

The visualization uses U.S. Census Bureau data and boundaries. NCES documentation supplies context for school district geography and membership. Source files were retrieved **October 8, 2026**. The machine-readable [source-provenance file](data/source-provenance.json) records source vintages, URLs, original file sizes, and SHA-256 hashes; [metadata](data/metadata.json) describes this project's coverage and exports.

## School finances: fiscal year 2024

**Agency and program:** U.S. Census Bureau, Annual Survey of School System Finances (F-33). The [FY2024 release](https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html), published May 7, 2026, reports national current spending of **$17,619 per student**, the map's spending benchmark.

| Source | Use in this project |
| --- | --- |
| [2024 education finance landing page](https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html) | Official release and download entry point |
| [Individual-unit tables: XLSX](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24t.xlsx) · [TXT](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24t.txt) | Published per-student current spending (`PPCSTOT`), membership, local revenue, and revenue shares; values checked across formats |
| [All data items: XLSX](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24.xlsx) · [TXT](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24.txt) | Supporting totals, definitions, and source checks |
| [Data-item flags: TXT](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24f.txt) | Review of reported, estimated, adjusted, missing, and not-applicable source items |
| [FY2024 technical documentation: DOCX](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx) | Survey scope, units, fiscal periods, per-pupil calculations, membership, state notes, and comparability limitations |
| [Finance file archive](https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/) | Alternate formats and original files |

The main spending statistic includes current resources funded by federal, state, and local sources. It does not represent only spending financed by local households. The [methodology](METHODOLOGY.md#spending-and-local-revenue) distinguishes spending, local revenue, and tax effort.

## Household income: ACS 2020–2024

**Agency and program:** U.S. Census Bureau, American Community Survey five-year estimates. Table **B19013** provides median household income in 2024 inflation-adjusted dollars. The district estimates describe all resident households. The national estimate, **$80,734**, supplies the map's income benchmark.

| Source | Use in this project |
| --- | --- |
| [B19013 on data.census.gov](https://data.census.gov/table/ACSDT5Y2024.B19013) | Published table and national comparison value |
| [B19013 summary-file data](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b19013.dat) | Exact district, state, and national estimates and margins of error used to assemble the snapshot |
| [B19013 variable definitions](https://api.census.gov/data/2024/acs/acs5/groups/B19013.html) | `B19013_001E` estimate and `B19013_001M` margin of error |
| [ACS summary-file documentation](https://www.census.gov/programs-surveys/acs/data/summary-file.html) | File structure, geography, and statistical conventions |
| [Estimate and annotation value notes](https://www.census.gov/data/developers/data-sets/acs-1year/notes-on-acs-estimate-and-annotation-values.html) | Interpretation of unavailable and bounded values |

The project retains missing values and the distinction between exact estimates and published bounds. [Income uncertainty](METHODOLOGY.md#household-income-and-uncertainty) explains the margins of error and the use of triangles for bounded medians.

## District boundaries

**Source:** Census Bureau [2024 Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/2024/geo/carto-boundary-file.html), 1:500,000 scale, school district geography for school year 2023–2024.

| Boundary type | Original download |
| --- | --- |
| Unified school districts | [cb_2024_us_unsd_500k.zip](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_unsd_500k.zip) |
| Elementary school districts | [cb_2024_us_elsd_500k.zip](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_elsd_500k.zip) |
| Secondary school districts | [cb_2024_us_scsd_500k.zip](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_scsd_500k.zip) |

[NCES district boundary documentation](https://nces.ed.gov/programs/edge/Geographic/DistrictBoundaries) explains the school district geography program. The [NCES composite boundary file documentation](https://nces.ed.gov/programs/edge/docs/EDGE_SDBOUNDARIES_COMPOSITE_FILEDOC.pdf) explains identifier issues, including pseudo-districts. The project uses exact identifier joins and leaves unmatched records unmatched.

The website's geometry has been further simplified for display. Download the original Census boundaries for spatial analysis; see [display geometry](METHODOLOGY.md#display-geometry) for the limits of this visualization's shapes.

## Project outputs and software

The [district CSV](data/districts.csv), [district JSON](data/districts.json), coverage counts, visual classifications, and local revenue per-student calculation are project outputs derived from the sources above. They are not new Census statistical releases. Their fields and derivations are documented in the [data dictionary](data/data-dictionary.md) and [methodology](METHODOLOGY.md).

Rendering uses D3 and TopoJSON Client. Their upstream projects and license notices are listed separately in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Data attribution and software licensing are distinct; this independent visualization does not imply endorsement by Census or NCES.

