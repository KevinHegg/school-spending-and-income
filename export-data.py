#!/usr/bin/env python3
"""Export the approved map snapshot as transparent CSV, JSON, and metadata.

Run from any directory with Python 3.9 or newer. Only the Python standard
library is required. This script reproduces the published downloads from the
checked-in snapshot; it does not download or rejoin the original Census files.
"""

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "education-values.json"
PROVENANCE = ROOT / "data" / "source-provenance.json"
DICTIONARY = ROOT / "data" / "data-dictionary.md"
TYPES = {"u": "unified", "e": "elementary", "s": "secondary"}
FIELDS = [
    "district_id",
    "state_fips",
    "state",
    "state_abbr",
    "district",
    "district_type",
    "median_household_income",
    "income_moe_90",
    "income_bound",
    "spending_per_student",
    "enrollment",
    "local_revenue_per_student",
    "local_revenue_share_pct",
    "matched",
]


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def positive(value):
    return value is not None and value > 0


def transform(source):
    records = []
    ids = set()
    for row in source["rows"]:
        if len(row) != 10:
            raise ValueError("Every source row must have exactly 10 fields.")
        key, name, kind, income, moe, bound, spending, enrollment, local, share = row
        if not isinstance(key, str) or len(key) != 7 or not key.isdigit() or key in ids:
            raise ValueError(f"District ID is invalid or duplicated: {key!r}")
        ids.add(key)
        if key[:2] not in source["states"] or kind not in TYPES:
            raise ValueError(f"District has an unknown state or type: {key}")
        if not isinstance(name, str) or not name:
            raise ValueError(f"District is missing its name: {key}")
        for value in (income, moe, spending, enrollment, local, share):
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(f"District has an invalid numeric value: {key}")
        if share is not None and share > 100:
            raise ValueError(f"Local revenue share is outside 0–100: {key}")
        if bound not in (None, "+", "-"):
            raise ValueError(f"Unrecognized income bound: {key}")
        if bound == "+" and income != 250000:
            raise ValueError(f"Upper income bound must be stored as 250000: {key}")
        if bound == "-" and income != 2500:
            raise ValueError(f"Lower income bound must be stored as 2500: {key}")
        state = source["states"][key[:2]]
        records.append(dict(zip(FIELDS, [
            key, key[:2], state["name"], state["abbr"], name, TYPES[kind],
            income, moe, bound, spending, enrollment, local, share,
            positive(income) and positive(spending) and positive(enrollment),
        ])))
    return sorted(records, key=lambda record: record["district_id"])


def summarize(records):
    matched = [record for record in records if record["matched"]]
    by_type = {}
    for kind in TYPES.values():
        subset = [record for record in records if record["district_type"] == kind]
        by_type[kind] = {
            "districts": len(subset),
            "matched": sum(record["matched"] for record in subset),
        }
    return {
        "geographic_districts": len(records),
        "states_and_dc": len({record["state_fips"] for record in records}),
        "matched_districts": len(matched),
        "unmatched_or_incomplete_districts": len(records) - len(matched),
        "default_view_matched_districts": sum(
            record["district_type"] in ("unified", "elementary") for record in matched
        ),
        "districts_with_income": sum(record["median_household_income"] is not None for record in records),
        "districts_without_income": sum(record["median_household_income"] is None for record in records),
        "matched_with_exact_income_estimate": sum(record["income_bound"] is None for record in matched),
        "matched_with_bounded_income": sum(record["income_bound"] is not None for record in matched),
        "upper_bounded_income": sum(record["income_bound"] == "+" for record in records),
        "lower_bounded_income": sum(record["income_bound"] == "-" for record in records),
        "by_type": by_type,
    }


def prepare_outputs():
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    provenance_bytes = PROVENANCE.read_bytes()
    provenance = json.loads(provenance_bytes)
    records = transform(source)
    counts = summarize(records)
    benchmarks = {
        "median_household_income": {
            "value": source["benchmarks"]["income"],
            "unit": "2024 inflation-adjusted USD per household",
            "period": "ACS 2020–2024 five-year estimate",
            "scope": "Published national median for all households; not an average of district medians",
        },
        "spending_per_student": {
            "value": source["benchmarks"]["spending"],
            "unit": "USD per enrolled student",
            "period": "Fiscal year 2024",
            "scope": "Published national current elementary-secondary spending per pupil",
        },
    }
    table_metadata = {
        "title": "School spending and household income by district",
        "schema_version": "1.0",
        "snapshot_date": provenance["snapshot_date"],
        "geography": "50 U.S. states and the District of Columbia; 2024 school district boundaries",
        "counts": counts,
        "benchmarks": benchmarks,
        "data_dictionary": "data-dictionary.md",
        "source_provenance": "source-provenance.json",
        "source_urls": [
            provenance["finance"]["source_page"],
            provenance["income"]["table_url"],
            provenance["geometry"]["source_page"],
        ],
        "missing_values": "JSON null; empty CSV fields. Numeric zero is retained as zero.",
        "income_bounds": "+ means $250,000 or more; - means $2,500 or less. These are bounds, not exact medians.",
    }

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow({**record, "matched": "true" if record["matched"] else "false"})
    csv_content = stream.getvalue().encode("utf-8")

    # One named record per line keeps the JSON readable and its diffs compact.
    prefix = json.dumps({"metadata": table_metadata}, ensure_ascii=False, indent=2, allow_nan=False)[:-2]
    record_lines = [
        "    " + json.dumps(record, ensure_ascii=False, separators=(", ", ": "), allow_nan=False)
        for record in records
    ]
    json_content = (prefix + ',\n  "districts": [\n' + ",\n".join(record_lines) + "\n  ]\n}\n").encode("utf-8")

    outputs = {
        "data/districts.csv": csv_content,
        "data/districts.json": json_content,
    }
    metadata = {
        **table_metadata,
        "record_fields": FIELDS,
        "identifier_note": "district_id is the seven-character Census district GEOID used for an exact match to finance NCESID. An unmatched geography is not evidence of an agency-ID match.",
        "reproduction": {
            "command": "python3 scripts/export-data.py",
            "check_command": "python3 scripts/export-data.py --check",
            "requirements": "Python 3.9 or newer; standard library only",
            "scope": "Reproduce downloads from the approved checked-in map snapshot. Original Census ingestion and the geometry simplification are not rerun by this command.",
            "input": {"path": "src/education-values.json", "bytes": len(source_bytes), "sha256": sha256(source_bytes)},
        },
        "file_checksums": [
            {"path": path, "bytes": len(content), "sha256": sha256(content)}
            for path, content in outputs.items()
        ] + [
            {"path": "data/source-provenance.json", "bytes": len(provenance_bytes), "sha256": sha256(provenance_bytes)},
            {"path": "data/data-dictionary.md", "bytes": DICTIONARY.stat().st_size, "sha256": sha256(DICTIONARY.read_bytes())},
        ],
        "display_notes": [
            "The default layer contains unified and elementary districts. The alternative contains unified and secondary districts. Elementary and secondary geographies can overlap.",
            "The map uses the same national income and spending benchmarks in every state. The scatterplot uses a linear income axis and a logarithmic spending axis; each district is one unweighted point.",
            "Income describes all resident households. Spending is current elementary-secondary expenditure from federal, state and local funds per pupil, not the locality's own spending or a household tax rate.",
            "Local revenue per student is rounded to whole dollars in this map snapshot. Local share is the source's published percentage on a 0–100 scale.",
            "The snapshot retains unusually low and high published spending values. Consult source documentation and flags when investigating a district.",
            "Dollar values are not adjusted for geographic costs. The five-year income estimate and one-year finance measure describe different time windows.",
        ],
    }
    outputs["data/metadata.json"] = json_bytes(metadata)
    hash_inputs = {
        **outputs,
        "data/data-dictionary.md": DICTIONARY.read_bytes(),
        "data/source-provenance.json": provenance_bytes,
        "src/education-values.json": source_bytes,
    }
    outputs["data/SHA256SUMS"] = "".join(
        f"{sha256(content)}  {path}\n" for path, content in sorted(hash_inputs.items())
    ).encode("utf-8")
    # Reparse both formats before writing, so a malformed download is never emitted.
    if json.loads(json_content)["districts"] != records:
        raise ValueError("JSON export failed its lossless round-trip check.")
    csv_rows = list(csv.DictReader(io.StringIO(csv_content.decode("utf-8"))))
    if len(csv_rows) != len(records) or any(
        csv_row[field] != ("" if record[field] is None else str(record[field]).lower() if isinstance(record[field], bool) else str(record[field]))
        for csv_row, record in zip(csv_rows, records) for field in FIELDS
    ):
        raise ValueError("CSV export failed its field-by-field round-trip check.")
    return outputs, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify checked-in exports without rewriting them")
    args = parser.parse_args()
    outputs, counts = prepare_outputs()
    different = []
    for relative, content in outputs.items():
        destination = ROOT / relative
        if args.check:
            if not destination.exists() or destination.read_bytes() != content:
                different.append(relative)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    if different:
        parser.exit(1, "Exports differ from their inputs: " + ", ".join(different) + "\n")
    print(json.dumps({"status": "verified" if args.check else "exported", "counts": counts, "files": list(outputs)}, indent=2))


if __name__ == "__main__":
    main()
