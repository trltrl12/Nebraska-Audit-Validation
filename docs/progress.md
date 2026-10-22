# Audit progress

## Phase 1 — Discovery and baseline

Status: completed for source commit `e3487afa0a6953a428bea997359aa257fd97882c`.

Completed:

- Inspected the source pipeline, GitHub Actions workflows, extraction schema, classification rules, workbook, CSV outputs, JSON/verifier population, and retained PDFs.
- Added a reproducible, read-only baseline audit command.
- Added regression tests for filename normalization and duplicate-detection semantics.
- Generated machine-readable metrics and a human-readable baseline report.
- Preserved both source and validation roles: no source artifacts were overwritten.

Next:

- Phase 2: define versioned record-level verification statuses, publication gates, source-of-truth tables, and accounting-scope rules.
- Phase 3: implement independent checks against raw/retained evidence and semantic double-count controls.
- Phase 4: prioritize the nine current flagged entities, twenty failed roll-forwards, twelve thousand page-presence review items, and material classification risks.
