# District data dictionary

`districts.csv` and `districts.json` contain the same **13,305 geographic school districts** in the 50 states and the District of Columbia. Each row represents one geographic district, identified by a seven-character Census district GEOID. The JSON file contains a `metadata` object and a `districts` array. Both downloads use UTF-8.

Import `district_id` and `state_fips` as **text** when opening the CSV in a spreadsheet. Automatic numeric conversion can remove leading zeros. Numeric columns contain unformatted values. An empty CSV field or JSON `null` means unavailable; a numeric zero remains zero. CSV `matched` values are `true` or `false`, and JSON uses native booleans.

## Fields

| Field | Type / unit | Meaning |
| --- | --- | --- |
| `district_id` | Text, 7 digits | Census district GEOID, consisting of state FIPS plus the five-digit district identifier. Used for an exact join to the finance file's `NCESID`. Some geographic districts have no matching finance agency. Pseudo-district geography and agency IDs can differ. |
| `state_fips` | Text, 2 digits | First two characters of `district_id`. |
| `state` | Text | State name or District of Columbia. |
| `state_abbr` | Text, 2 letters | Postal abbreviation. |
| `district` | Text | Geographic school district name from the Census boundary data. |
| `district_type` | Text | `unified`, `elementary`, or `secondary`, based on geographic district type. This is not a charter-school classification. |
| `median_household_income` | USD in 2024 inflation-adjusted dollars | ACS 2020–2024 five-year estimate from table B19013. Covers all households residing inside the district, including households without children in public school. For a bounded estimate, this field contains the displayed bound; read `income_bound` with it. |
| `income_moe_90` | USD | Published 90% margin of error for the income estimate. It is not a standard error or a percentage. Null when unavailable, including open-ended income bounds. |
| `income_bound` | Text or null | `+` means **$250,000 or more**; `-` means **$2,500 or less**. Null means an ordinary estimate or unavailable income. Census sentinels 250001 and 2499 were mapped to display bounds 250000 and 2500. Do not treat these bounds as exact observations in correlations. |
| `spending_per_student` | USD per student | FY2024 published current elementary-secondary spending per pupil, Census field `PPCSTOT`. Includes spending financed from federal, state, and local sources. The map snapshot contains this value only for an exact-matched regular school system with positive enrollment and positive published spending. Otherwise it is null. The published value is used directly and is already in dollars. |
| `enrollment` | Students | FY2024 finance file's fall 2023 membership (`ENROLL` / `V33`), subject to Census adjustments. A value may be present even when the row is not included in the spending comparison. This snapshot does not include the separate source flag matrix; consult the official source for detailed reporting status. |
| `local_revenue_per_student` | USD per student, rounded to whole dollars | Derived as local-source revenue (`TLOCREV`, converted from thousands of dollars to dollars) divided by positive enrollment. The approved map snapshot rounds this ratio to the nearest dollar. Local revenue includes taxes, parent-government contributions, fees, interdistrict receipts, and other local sources. It is a revenue measure, not a spending figure or tax rate. |
| `local_revenue_share_pct` | Percent, 0–100 | Published `PCTLTOT`: local-source revenue as a share of total revenue. For example, 36.1 means 36.1%, not 0.361%. |
| `matched` | Boolean | True when the map snapshot has positive income, spending per student, and enrollment. Bounded income estimates are included. False otherwise. This is eligibility for the plotted comparison, not a claim that every source field is independently reported or error-free. |

## Coverage and filters

The snapshot has **12,960 matched districts**, including **44 with bounded income**. The default map and scatterplot use unified and elementary districts, giving **12,577 matched districts**. Switching to unified and secondary districts changes grade coverage. Elementary and secondary boundaries can overlap, so adding both layers together would double-cover some places.

| Geographic district type | All rows | Matched rows |
| --- | ---: | ---: |
| Unified | 10,872 | 10,692 |
| Elementary | 1,952 | 1,885 |
| Secondary | 481 | 383 |
| **Total** | **13,305** | **12,960** |

Seventy-seven geographic rows have no usable household-income value. That includes 76 missing income values in the ACS district extract and one geometry without a B19013 district row: Wyandanch Union Free School District, New York (`3631800`). Missing districts remain in the downloads and appear hatched on the map when included in the active layer.

## Benchmarks and interpretation

The national income benchmark is **$80,734**, the published ACS 2020–2024 U.S. median household income. The spending benchmark is **$17,619**, the published FY2024 U.S. current spending per pupil. The map uses these same thresholds in every state. They are national published values, not averages of the district rows in these files. A value equal to a threshold is classified on the higher side.

Current spending excludes capital outlay, debt service, and non-elementary-secondary programs under the Census definition. Geographic costs, student needs, and grade coverage are not adjusted. The income estimate pools five years, while finance represents one fiscal year. The data describe school resources and resident household income; they do not establish a causal relationship or measure school quality or household tax effort.

The snapshot preserves unusual published spending values, including values below $1,000 per student and very high values in small districts. The interactive display calls attention to spending below $1,000. Refer to the source records and technical notes when investigating an outlier; this download is the map's analysis snapshot, not a replacement for the full Census files and flags.

## Sources and reproducibility

- [Census Annual Survey of School System Finances, FY2024](https://www.census.gov/data/tables/2024/econ/school-finances/secondary-education-finance.html), especially `elsec24t.xlsx` and the [technical documentation](https://www2.census.gov/programs-surveys/school-finances/technical-documentation/complete-technical-documentation/2024/school24doc.docx).
- [ACS 2020–2024 table B19013](https://data.census.gov/table/ACSDT5Y2024.B19013), from the [table-based summary file](https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b19013.dat).
- [Census 2024 cartographic boundary files](https://www.census.gov/geographies/mapping-files/2024/geo/carto-boundary-file.html), school district layers at 1:500,000, with [NCES district-boundary guidance](https://nces.ed.gov/programs/edge/Geographic/DistrictBoundaries).
- [Source provenance](source-provenance.json) records source URLs, retrieval dates, raw-file sizes, SHA-256 hashes, and preparation notes. [Metadata](metadata.json) records counts, benchmarks, and exported-file hashes. [SHA256SUMS](SHA256SUMS) includes checksums for the published data files and the approved input snapshot.

From the repository root, run `python3 scripts/export-data.py` to recreate the downloads from `src/education-values.json`. Run `python3 scripts/export-data.py --check` to verify that the checked-in exports still match that snapshot. The script uses Python 3.9 or newer and the standard library. It does not redownload Census data, redo source joins, or regenerate the map's geometry.
