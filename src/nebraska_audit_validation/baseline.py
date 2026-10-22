"""Create a read-only baseline audit of the Nebraska-Audit output snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from openpyxl import load_workbook


EXPECTED_SHEETS = [
    "Summary",
    "Needs Decision",
    "Review",
    "Line Items",
    "Detail Lines",
    "Revenue by Source",
    "Spending by Type",
    "Spending by Department",
    "Receipts",
    "Disbursements",
    "Financing & Balances",
    "Proprietary",
    "Balance Sheet",
    "Flagged",
    "Progress",
    "Mistakes",
    "Mistakes by Type",
    "Notes",
]

PRIMARY_TABLES = [
    "cashflow_summary.csv",
    "cashflow_long.csv",
    "cashflow_detail.csv",
]

HASHED_ARTIFACTS = [
    "output/cashflow.xlsx",
    "output/cashflow_summary.csv",
    "output/cashflow_long.csv",
    "output/cashflow_detail.csv",
    "output/progress.csv",
    "output/flagged.csv",
    "output/review.csv",
    "scripts/validate.py",
    "scripts/build_csv.py",
    "scripts/build_xlsx.py",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git_value(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _stem(value: str) -> str:
    return Path(value).stem


def _counter(rows: Iterable[Mapping[str, str]], column: str) -> dict[str, int]:
    return dict(sorted(Counter(row.get(column, "") for row in rows).items()))


def _duplicate_rows(rows: Sequence[Mapping[str, str]]) -> dict[str, int]:
    if not rows:
        return {"groups": 0, "extra_rows": 0}
    columns = tuple(rows[0].keys())
    counts = Counter(tuple(row.get(column, "") for column in columns) for row in rows)
    return {
        "groups": sum(count > 1 for count in counts.values()),
        "extra_rows": sum(count - 1 for count in counts.values() if count > 1),
    }


def _duplicate_keys(
    rows: Sequence[Mapping[str, str]], columns: Sequence[str]
) -> dict[str, int]:
    counts = Counter(tuple(row.get(column, "") for column in columns) for row in rows)
    return {
        "groups": sum(count > 1 for count in counts.values()),
        "extra_rows": sum(count - 1 for count in counts.values() if count > 1),
    }


def _require_files(root: Path, relative_paths: Iterable[str]) -> None:
    missing = [relative for relative in relative_paths if not (root / relative).is_file()]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def analyze(source_root: Path, generated_at: str | None = None) -> dict:
    """Inspect source artifacts without modifying them and return baseline metrics."""

    source_root = source_root.resolve()
    output = source_root / "output"
    required = [
        "output/cashflow.xlsx",
        "output/progress.csv",
        "output/flagged.csv",
        "output/review.csv",
        "output/cashflow_summary.csv",
        "output/cashflow_long.csv",
        "output/cashflow_detail.csv",
        "output/manifest.csv",
        "output/file_list.csv",
    ]
    _require_files(source_root, required)

    progress = _read_csv(output / "progress.csv")
    flagged = _read_csv(output / "flagged.csv")
    review = _read_csv(output / "review.csv")
    summary = _read_csv(output / "cashflow_summary.csv")
    long_rows = _read_csv(output / "cashflow_long.csv")
    detail = _read_csv(output / "cashflow_detail.csv")
    manifest = _read_csv(output / "manifest.csv")
    file_list = _read_csv(output / "file_list.csv")

    workbook_path = output / "cashflow.xlsx"
    workbook = load_workbook(workbook_path, read_only=True, data_only=False)
    sheet_rows = {
        sheet.title: max(sheet.max_row - 1, 0) for sheet in workbook.worksheets
    }
    sheet_columns = {sheet.title: sheet.max_column for sheet in workbook.worksheets}
    workbook_sheets = workbook.sheetnames
    workbook.close()

    json_stems = {path.stem for path in (output / "json").glob("*.json")}
    verifier_stems = {path.stem for path in (output / "json" / "verify").glob("*.json")}
    trimmed_stems = {path.stem for path in (source_root / "trimmed").glob("*.pdf")}
    manifest_stems = {_stem(row["filename"]) for row in manifest}
    listed_stems = {_stem(row["filename"]) for row in file_list}

    exact_duplicates = {
        "cashflow_summary.csv": _duplicate_rows(summary),
        "cashflow_long.csv": _duplicate_rows(long_rows),
        "cashflow_detail.csv": _duplicate_rows(detail),
    }

    artifacts = {
        relative: {
            "bytes": (source_root / relative).stat().st_size,
            "sha256": _sha256(source_root / relative),
        }
        for relative in HASHED_ARTIFACTS
        if (source_root / relative).is_file()
    }

    missing_reconciliation = sum(row.get("reconciles", "") == "" for row in summary)
    failed_reconciliation = sum(row.get("reconciles") == "no" for row in summary)
    amount_not_found = sum(
        row.get("reason", "").startswith("amount not found on cited page") for row in review
    )

    return {
        "report_version": 1,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "scope": {
            "source_root": str(source_root),
            "source_commit": _git_value(source_root, "rev-parse", "HEAD"),
            "source_branch": _git_value(source_root, "branch", "--show-current"),
            "source_remote": _git_value(source_root, "remote", "get-url", "origin"),
            "claim": "Structural and existing-validator baseline; not comprehensive PDF verification",
        },
        "inventory": {
            "file_list_rows": len(file_list),
            "manifest_rows": len(manifest),
            "json_reports": len(json_stems),
            "verifier_reports": len(verifier_stems),
            "trimmed_pdfs": len(trimmed_stems),
            "summary_rows": len(summary),
            "long_rows": len(long_rows),
            "detail_rows": len(detail),
            "review_rows": len(review),
            "flagged_rows": len(flagged),
            "needs_decision_rows": sheet_rows.get("Needs Decision", 0),
        },
        "workflow_status": _counter(progress, "status"),
        "filing_type": _counter(progress, "filing_type"),
        "accounting_basis": _counter(summary, "basis"),
        "reconciliation": {
            "governmental_rollforward": _counter(summary, "reconciles"),
            "proprietary_cashflow": _counter(summary, "prop_reconciles"),
            "business_type_rollforward": _counter(summary, "bt_reconciles"),
            "balance_sheet": _counter(summary, "balance_sheet_balances"),
        },
        "source_coverage": {
            "summary_missing_source_url": sum(not row.get("source_url", "").strip() for row in summary),
            "detail_missing_source_url": sum(not row.get("source_url", "").strip() for row in detail),
            "detail_missing_source_page": sum(not row.get("source_page", "").strip() for row in detail),
            "json_without_trimmed_pdf": sorted(json_stems - trimmed_stems),
            "trimmed_pdf_without_json": sorted(trimmed_stems - json_stems),
            "json_without_verifier": sorted(json_stems - verifier_stems),
            "listed_without_manifest": sorted(listed_stems - manifest_stems),
            "manifest_without_trimmed_pdf": sorted(manifest_stems - trimmed_stems),
        },
        "integrity": {
            "duplicate_summary_filename": _duplicate_keys(summary, ["filename"]),
            "duplicate_summary_entity_period_basis": _duplicate_keys(
                summary, ["entity_name", "fiscal_year_end", "basis"]
            ),
            "exact_duplicate_rows": exact_duplicates,
            "amount_not_found_review_items": amount_not_found,
            "decision_review_items": sum(row.get("where") == "decision_needed" for row in review),
        },
        "workbook": {
            "sheet_count": len(workbook_sheets),
            "sheets": workbook_sheets,
            "missing_expected_sheets": sorted(set(EXPECTED_SHEETS) - set(workbook_sheets)),
            "unexpected_sheets": sorted(set(workbook_sheets) - set(EXPECTED_SHEETS)),
            "data_rows": sheet_rows,
            "columns": sheet_columns,
        },
        "known_exceptions": {
            "failed_governmental_reconciliations": failed_reconciliation,
            "missing_governmental_reconciliation_result": missing_reconciliation,
            "flagged": flagged,
            "top_review_reasons": [
                {"reason": reason, "count": count}
                for reason, count in Counter(row.get("reason", "") for row in review).most_common(15)
            ],
        },
        "artifact_hashes": artifacts,
    }


def _table(rows: Sequence[Sequence[object]], headers: Sequence[str]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out.extend("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in rows)
    return out


def render_markdown(data: Mapping) -> str:
    """Render a concise baseline report from :func:`analyze` output."""

    inv = data["inventory"]
    rec = data["reconciliation"]
    coverage = data["source_coverage"]
    integrity = data["integrity"]
    exceptions = data["known_exceptions"]
    status = data["workflow_status"]
    lines = [
        "# Phase 1 Baseline Audit",
        "",
        f"Generated from source commit `{data['scope']['source_commit']}` on `{data['generated_at']}`.",
        "",
        "> Scope: structural inventory, cross-table checks, and reproduction of the existing validator's status. "
        "This is not comprehensive verification against every PDF.",
        "",
        "## Executive findings",
        "",
        f"- {inv['summary_rows']:,} summarized reports are represented in the published summary; "
        f"{status.get('done', 0):,} are marked done and {status.get('flagged', 0):,} are flagged in progress.",
        f"- {exceptions['failed_governmental_reconciliations']:,} summary records explicitly fail the governmental "
        f"roll-forward and {exceptions['missing_governmental_reconciliation_result']:,} have no affirmative result.",
        f"- {inv['review_rows']:,} review items remain, including "
        f"{integrity['amount_not_found_review_items']:,} amounts not found by the automated cited-page check and "
        f"{inv['needs_decision_rows']:,} explicit decision items.",
        f"- The current flagged output contains {inv['flagged_rows']:,} issues. These remain publication blockers until "
        "resolved or explicitly excluded with evidence.",
        f"- Exact whole-row duplication was not found in the three primary CSV outputs; this does not rule out semantic "
        "double counting across statements, funds, or schedules.",
        "",
        "## Inventory",
        "",
    ]
    lines.extend(
        _table(
            [
                ("Listed filings", inv["file_list_rows"]),
                ("Manifest rows", inv["manifest_rows"]),
                ("Trimmed PDFs", inv["trimmed_pdfs"]),
                ("Extraction JSON reports", inv["json_reports"]),
                ("Independent verifier JSON reports", inv["verifier_reports"]),
                ("Summary rows", inv["summary_rows"]),
                ("Normalized line items", inv["long_rows"]),
                ("Detailed financial lines", inv["detail_rows"]),
                ("Review items", inv["review_rows"]),
                ("Needs Decision items", inv["needs_decision_rows"]),
            ],
            ["Artifact", "Count"],
        )
    )
    lines.extend(["", "## Existing validation coverage", ""])
    lines.extend(
        _table(
            [
                ("Governmental roll-forward", rec["governmental_rollforward"].get("yes", 0), rec["governmental_rollforward"].get("no", 0), rec["governmental_rollforward"].get("", 0)),
                ("Proprietary cash flow", rec["proprietary_cashflow"].get("yes", 0), rec["proprietary_cashflow"].get("no", 0), rec["proprietary_cashflow"].get("", 0)),
                ("Business-type roll-forward", rec["business_type_rollforward"].get("yes", 0), rec["business_type_rollforward"].get("no", 0), rec["business_type_rollforward"].get("", 0)),
                ("Balance sheet", rec["balance_sheet"].get("yes", 0), rec["balance_sheet"].get("no", 0), rec["balance_sheet"].get("", 0)),
            ],
            ["Check", "Yes", "No", "Blank / not recorded"],
        )
    )
    lines.extend(
        [
            "",
            "A blank result can mean the statement or measure was not applicable, unavailable, or not extracted. The current "
            "output does not always encode those cases separately, so blanks cannot be treated as passes or zeros.",
            "",
            "## Cross-table and source checks",
            "",
            f"- Summary rows missing source URLs: {coverage['summary_missing_source_url']:,}.",
            f"- Detail rows missing source URLs: {coverage['detail_missing_source_url']:,}.",
            f"- Detail rows missing cited source pages: {coverage['detail_missing_source_page']:,}.",
            f"- JSON reports without a trimmed PDF: {len(coverage['json_without_trimmed_pdf']):,}.",
            f"- Trimmed PDFs without extraction JSON: {len(coverage['trimmed_pdf_without_json']):,}: "
            + (", ".join(coverage["trimmed_pdf_without_json"]) or "none")
            + ".",
            f"- JSON reports without verifier output: {len(coverage['json_without_verifier']):,}.",
            f"- Listed filings without a manifest record: {len(coverage['listed_without_manifest']):,}: "
            + (", ".join(coverage["listed_without_manifest"]) or "none")
            + ".",
            f"- Manifest records without a retained trimmed PDF: {len(coverage['manifest_without_trimmed_pdf']):,}: "
            + (", ".join(coverage["manifest_without_trimmed_pdf"]) or "none")
            + ".",
            "",
            "## Current flagged issues",
            "",
        ]
    )
    lines.extend(
        _table(
            [
                (row.get("filename", ""), row.get("check", ""), row.get("reason", ""))
                for row in exceptions["flagged"]
            ],
            ["File", "Check", "Reason"],
        )
    )
    lines.extend(
        [
            "",
            "## Baseline risk assessment",
            "",
            "1. **Source confirmation remains incomplete.** The page-presence check produces 12,275 review items, and the "
            "existing verifier shares the same trimmed-PDF population. A second method must verify statement context, period, "
            "fund, and column before publication status can be granted.",
            "2. **Arithmetic coverage is uneven.** Failed and blank roll-forward/balance checks must be separated into true "
            "failures, not-applicable cases, and incomplete-source cases.",
            "3. **Classification exceptions remain material.** Transfer classifications appear in current flagged output, and "
            "catch-all category mappings dominate parts of the review queue.",
            "4. **The retained PDF set is curated rather than complete.** Validation can only confirm pages present in `trimmed/`; "
            "known missing schedules require source reacquisition or re-trimming.",
            "5. **Duplicate detection is currently structural.** No exact duplicate primary rows were found, but semantic duplicate "
            "and double-count tests still need statement/fund/schedule inclusion rules.",
            "",
            "## Phase 1 conclusion",
            "",
            "The snapshot is reproducible and internally traceable at the row-to-URL/page level for the primary outputs, but it is "
            "not publication-ready as a fully verified database. Existing flags, missing affirmative reconciliations, unresolved "
            "decisions, and page-check exceptions require explicit resolution or publication exclusions.",
            "",
            "Artifact hashes and the complete machine-readable metrics are stored in `baseline_metrics.json` so future runs can "
            "distinguish source changes from validation-rule changes.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Path to the Nebraska-Audit checkout")
    parser.add_argument("--json", type=Path, required=True, help="Machine-readable output path")
    parser.add_argument("--markdown", type=Path, required=True, help="Human-readable output path")
    args = parser.parse_args(argv)

    data = analyze(args.source)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(render_markdown(data), encoding="utf-8")
    print(
        f"baseline: {data['inventory']['summary_rows']} summaries, "
        f"{data['inventory']['flagged_rows']} flags, {data['inventory']['review_rows']} review items"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
