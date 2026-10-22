# Audit progress

## Phase 1 — Discovery and baseline

Status: completed and refreshed for source commit `d3fa659a9a62f6ba11fd35154f168f466e70b683`.

Completed:

- Inspected the source pipeline, GitHub Actions workflows, extraction schema, classification rules, workbook, CSV outputs, JSON/verifier population, and retained PDFs.
- Added a reproducible, read-only baseline audit command.
- Added regression tests for filename normalization and duplicate-detection semantics.
- Generated machine-readable metrics and a human-readable baseline report.
- Preserved both source and validation roles: no source artifacts were overwritten.
- Assessed the October 22 source update and documented the Sargent re-trim separately from changes caused by rebuilding previously stale generated projections.

## Phase 2 — Validation architecture

Status: completed for the initial architecture and approved SID policy decisions.

Completed:

- Defined immutable source observations, standardized facts, verification assessments, human decisions, and correction logs.
- Defined independent status dimensions and enforceable record-level publication gates.
- Defined aggregate compatibility rules for accounting basis, scope, period, value type, interfund activity, and duplicates.
- Recorded accounting comparability rules and resolved three SID policy questions without changing source data.
- Stored the approved SID treatments as versioned, machine-readable classification rules.

Next:

- Phase 3: run and refine independent checks against raw/retained evidence and semantic double-count controls.
- Phase 4: prioritize the nine current flagged entities, twenty failed roll-forwards, twelve thousand page-presence review items, and material classification risks.

## Phase 4 — Initial financial audit

Status: in progress.

Completed:

- Independently inspected cited statement-page evidence for fourteen Tier 1 entities.
- Confirmed seventeen internal source-report discrepancies across governmental, business-type, proprietary cash-flow, and balance-sheet checks.
- Confirmed one incomplete retained-source case (Hickman) and four validator false positives: one Municipal Energy Agency classification and three Sargent Public Schools account-name matches.
- Recorded publication treatment without changing or forcing any financial value.
- Refreshed the baseline and quality scan to source commit `d3fa659a9a62f6ba11fd35154f168f466e70b683`.
- Removed four evidence-confirmed validator false positives from active failure and review queues through exact finding resolutions; retained their completed investigation evidence.

Next:

- Investigate the remaining Tier 1 entities, separating source-report defects from extraction, classification, and completeness defects.
- Continue investigating unresolved Tier 1 flags and classification risks.
