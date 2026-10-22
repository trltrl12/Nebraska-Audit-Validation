"""Independent structural quality checks and entity triage for source outputs."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence


TRANSFER_RE = re.compile(r"\btransfers?\b(?! station)", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    filename: str
    entity_name: str
    message: str
    evidence: str = ""


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _stem(value: str) -> str:
    return Path(value).stem


def _read_resolutions(path: Path | None) -> list[dict]:
    if path is None or not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("resolutions", []))


def _resolution_matches(
    resolutions: Sequence[Mapping],
    *,
    rule_id: str,
    filename: str,
    source_page: str,
    label_or_reason: str,
) -> bool:
    """Return true only for an exact, evidence-reviewed finding resolution."""

    for resolution in resolutions:
        if rule_id not in resolution.get("rule_ids", []):
            continue
        if filename != resolution.get("filename"):
            continue
        if source_page != str(resolution.get("source_page", "")):
            continue
        label = str(resolution.get("original_label", ""))
        if label and label in label_or_reason:
            return True
    return False


def _semantic_duplicate_candidates(rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    """Find repeated source-located records; equal amounts alone are never enough."""

    groups: dict[tuple[str, ...], list[Mapping[str, str]]] = defaultdict(list)
    location_fields = (
        "filename",
        "source_page",
        "schedule",
        "fund",
        "department",
        "original_label",
        "amount",
    )
    for row in rows:
        key = tuple(row.get(field, "").strip() for field in location_fields)
        if key[0] and key[1] and key[5]:
            groups[key].append(row)

    findings = []
    for key, matches in groups.items():
        if len(matches) < 2:
            continue
        classifications = {
            (row.get("section", ""), row.get("category", ""), row.get("detail_category", ""))
            for row in matches
        }
        findings.append(
            Finding(
                rule_id="DUP-SOURCE-001",
                severity="REVIEW",
                filename=_stem(key[0]),
                entity_name=matches[0].get("entity_name", ""),
                message=(
                    f"{len(matches)} detail records share the same source location, label, and amount; "
                    "confirm they represent distinct facts"
                ),
                evidence=(
                    f"page={key[1]}; schedule={key[2]}; fund={key[3]}; department={key[4]}; "
                    f"label={key[5]!r}; amount={key[6]}; classifications={sorted(classifications)!r}"
                ),
            )
        )
    return findings


def analyze(
    source_root: Path,
    generated_at: str | None = None,
    resolved_findings: Path | None = Path("config/resolved_findings.json"),
) -> dict:
    source_root = source_root.resolve()
    output = source_root / "output"
    summary = _read_csv(output / "cashflow_summary.csv")
    detail = _read_csv(output / "cashflow_detail.csv")
    review = _read_csv(output / "review.csv")
    flagged = _read_csv(output / "flagged.csv")
    progress = _read_csv(output / "progress.csv")
    resolutions = _read_resolutions(resolved_findings)

    findings: list[Finding] = []
    entity_by_file = {_stem(row["filename"]): row.get("entity_name", "") for row in summary}

    for row in summary:
        filename = _stem(row["filename"])
        entity = row.get("entity_name", "")
        checks = (
            ("reconciles", "REC-GOV-001", "governmental roll-forward"),
            ("prop_reconciles", "REC-PROP-001", "proprietary cash-flow reconciliation"),
            ("bt_reconciles", "REC-BT-001", "business-type roll-forward"),
            ("balance_sheet_balances", "REC-BAL-001", "balance-sheet equation"),
        )
        for column, rule_id, label in checks:
            value = row.get(column, "")
            if value == "no":
                findings.append(Finding(rule_id, "FAIL", filename, entity, f"{label} failed"))
            elif column == "reconciles" and not value:
                findings.append(
                    Finding(
                        rule_id="REC-GOV-002",
                        severity="INCOMPLETE",
                        filename=filename,
                        entity_name=entity,
                        message="governmental roll-forward has no affirmative result",
                    )
                )
        if not row.get("source_url", "").strip():
            findings.append(Finding("SRC-URL-001", "FAIL", filename, entity, "summary source URL is missing"))

    for row in detail:
        filename = _stem(row["filename"])
        entity = row.get("entity_name", "")
        if not row.get("source_url", "").strip():
            findings.append(Finding("SRC-URL-002", "FAIL", filename, entity, "detail source URL is missing"))
        if not row.get("source_page", "").strip():
            findings.append(Finding("SRC-PAGE-001", "FAIL", filename, entity, "detail source page is missing"))
        label = row.get("original_label", "")
        if (
            TRANSFER_RE.search(label)
            and row.get("section") != "other financing"
            and not _resolution_matches(
                resolutions,
                rule_id="CLASS-TRANSFER-001",
                filename=filename,
                source_page=row.get("source_page", ""),
                label_or_reason=label,
            )
        ):
            findings.append(
                Finding(
                    rule_id="CLASS-TRANSFER-001",
                    severity="REVIEW",
                    filename=filename,
                    entity_name=entity,
                    message="a transfer-labeled detail record is outside other financing",
                    evidence=(
                        f"page={row.get('source_page', '')}; section={row.get('section', '')}; "
                        f"label={label!r}; amount={row.get('amount', '')}"
                    ),
                )
            )

    findings.extend(_semantic_duplicate_candidates(detail))

    for row in flagged:
        filename = _stem(row["filename"])
        if _resolution_matches(
            resolutions,
            rule_id="SOURCE-FLAG-001",
            filename=filename,
            source_page=row.get("pages", ""),
            label_or_reason=row.get("reason", ""),
        ):
            continue
        findings.append(
            Finding(
                rule_id="SOURCE-FLAG-001",
                severity="FAIL",
                filename=filename,
                entity_name=entity_by_file.get(filename, ""),
                message=f"existing validator flag ({row.get('check', '')}): {row.get('reason', '')}",
                evidence=f"pages={row.get('pages', '')}",
            )
        )

    summary_files = set(entity_by_file)
    progress_files = {_stem(row["filename"]) for row in progress}
    for filename in sorted(summary_files - progress_files):
        findings.append(
            Finding(
                "XREF-PROGRESS-001",
                "FAIL",
                filename,
                entity_by_file.get(filename, ""),
                "summary record has no progress record",
            )
        )

    review_counts = Counter(_stem(row["filename"]) for row in review)
    decision_counts = Counter(_stem(row["filename"]) for row in review if row.get("where") == "decision_needed")
    page_check_counts = Counter(
        _stem(row["filename"])
        for row in review
        if row.get("reason", "").startswith("amount not found on cited page")
    )

    findings_by_file: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        findings_by_file[finding.filename].append(finding)

    priority = []
    for filename in sorted(set(entity_by_file) | set(findings_by_file)):
        current = findings_by_file.get(filename, [])
        severity_counts = Counter(finding.severity for finding in current)
        if severity_counts["FAIL"]:
            tier = 1
        elif severity_counts["INCOMPLETE"]:
            tier = 2
        elif current or decision_counts[filename] or page_check_counts[filename]:
            tier = 3
        else:
            tier = 4
        priority.append(
            {
                "tier": tier,
                "filename": filename,
                "entity_name": entity_by_file.get(filename, ""),
                "failures": severity_counts["FAIL"],
                "incomplete": severity_counts["INCOMPLETE"],
                "review_findings": severity_counts["REVIEW"],
                "existing_review_items": review_counts[filename],
                "page_check_items": page_check_counts[filename],
                "decision_items": decision_counts[filename],
                "rule_ids": sorted({finding.rule_id for finding in current}),
            }
        )
    priority.sort(
        key=lambda row: (
            row["tier"],
            -row["failures"],
            -row["incomplete"],
            -row["decision_items"],
            -row["page_check_items"],
            -row["existing_review_items"],
            row["filename"],
        )
    )

    return {
        "report_version": 1,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "source_root": str(source_root),
        "finding_counts": dict(sorted(Counter(finding.rule_id for finding in findings).items())),
        "severity_counts": dict(sorted(Counter(finding.severity for finding in findings).items())),
        "findings": [asdict(finding) for finding in findings],
        "priority_queue": priority,
    }


def render_markdown(data: Mapping) -> str:
    counts = data["finding_counts"]
    severity = data["severity_counts"]
    priority = data["priority_queue"]
    lines = [
        "# Phase 3 Initial Quality Scan",
        "",
        f"Generated `{data['generated_at']}` from read-only source outputs.",
        "",
        "> These are automated findings and review candidates. A candidate is not a confirmed financial error until source evidence establishes it.",
        "",
        "## Findings",
        "",
        f"- Failures: {severity.get('FAIL', 0):,}",
        f"- Incomplete checks: {severity.get('INCOMPLETE', 0):,}",
        f"- Review candidates: {severity.get('REVIEW', 0):,}",
        "",
        "| Rule | Count |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {rule} | {count:,} |" for rule, count in sorted(counts.items()))
    lines.extend(
        [
            "",
            "## Highest-priority entities",
            "",
            "Tier 1 has an explicit failure, Tier 2 has an incomplete governmental roll-forward, Tier 3 has review-only findings, and Tier 4 has no finding from this scanner.",
            "",
            "| Tier | File | Entity | Failures | Incomplete | Scanner reviews | Existing reviews | Page checks | Decisions |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in priority[:50]:
        lines.append(
            f"| {row['tier']} | {row['filename']} | {row['entity_name']} | {row['failures']} | "
            f"{row['incomplete']} | {row['review_findings']} | {row['existing_review_items']} | "
            f"{row['page_check_items']} | {row['decision_items']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- Matching amounts alone are never treated as duplicates. Duplicate candidates require the same source file, page, schedule, fund, department, original label, and amount.",
            "- Transfer-word findings require context review; labels such as transfer fees may describe external revenue rather than interfund activity.",
            "- Blank reconciliation results remain incomplete until applicability and source completeness are established.",
            "- The queue prioritizes investigation; it does not assign publication eligibility by itself.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument(
        "--resolved-findings",
        type=Path,
        default=Path("config/resolved_findings.json"),
        help="Evidence-reviewed findings to remove from active queues",
    )
    args = parser.parse_args(argv)
    data = analyze(args.source, resolved_findings=args.resolved_findings)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    args.markdown.write_text(render_markdown(data), encoding="utf-8")
    print(
        f"quality: {data['severity_counts'].get('FAIL', 0)} failures, "
        f"{data['severity_counts'].get('INCOMPLETE', 0)} incomplete, "
        f"{data['severity_counts'].get('REVIEW', 0)} review candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
