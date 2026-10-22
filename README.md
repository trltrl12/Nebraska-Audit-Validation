# Nebraska Audit Validation

Independent validation and publication-readiness work for the Nebraska local-government financial database.

The existing extraction pipeline and its generated data remain in the sibling `Nebraska-Audit` repository. This repository reads those artifacts as evidence and stores independent checks, tests, audit reports, classification documentation, correction logs, and publication decisions. It does not overwrite the source workbook, JSON, PDFs, or generated CSV files.

## Current phase

Phase 1 establishes a reproducible baseline from the current source snapshot. Run it from this repository with:

```bash
source /workspace/.venvs/nebraska-audit/bin/activate
python -m nebraska_audit_validation.baseline \
  --source /workspace/Nebraska-Audit \
  --json reports/baseline_metrics.json \
  --markdown reports/phase1_baseline.md
python -m unittest discover -s tests -v
```

The generated report identifies current validation exceptions and coverage gaps. Counts describe the inspected source snapshot; they are not claims that every financial figure has been independently verified.

Phase 2 adds the normalized source-of-truth schema, independent verification dimensions, accounting-scope rules, and enforceable publication gates. See [verification_architecture.md](docs/verification_architecture.md) and [accounting_scope_rules.md](docs/accounting_scope_rules.md).

Run the initial Phase 3 quality and triage scan with:

```bash
python -m nebraska_audit_validation.quality \
  --source /workspace/Nebraska-Audit \
  --json reports/phase3_initial_quality.json \
  --markdown reports/phase3_initial_quality.md \
  --resolved-findings config/resolved_findings.json
```

Evidence-confirmed false positives are removed from active failure and review queues through `config/resolved_findings.json`. Their investigation evidence remains in `records/investigation_log.csv`.

Build the independent validation workbook with:

```bash
python -m nebraska_audit_validation.workbook \
  --repo /workspace/Nebraska-Audit-Validation \
  --output reports/nebraska_audit_validation.xlsx
```

The validation workbook is separate from the read-only source workbook at `/workspace/Nebraska-Audit/output/cashflow.xlsx`.
