# Verification architecture

## Source-of-truth layers

### Layer 1 — Source observations

This layer preserves the report as presented. Each observation records the original label, amount text, statement, fund, reporting period, basis, page, column, extraction method, and immutable document hash. Corrections never overwrite this layer.

### Layer 2 — Standardized facts

This layer maps a source observation to a defined financial measure and category. It records accounting basis, reporting scope, whether the activity is external or interfund, its role in published aggregates, the classification rule and version, and the type of support for the classification.

### Layer 3 — Published facts

Published data is a filtered result rather than a separately editable copy. A fact is eligible only when it has source provenance and each applicable verification dimension is either `VERIFIED` or `NOT_APPLICABLE`. Published aggregates must additionally contain compatible periods, bases, scopes, value types, and measure definitions.

## Verification dimensions

| Dimension | Question answered |
| --- | --- |
| Extraction | Does the value, sign, label, page, period, fund, and column match the source? |
| Reconciliation | Does the applicable statement relationship reconcile without forced adjustments? |
| Classification | Is the standardized category supported by the label, notes, a versioned rule, or a documented decision? |
| Source completeness | Are the statements and schedules needed for this measure present? |
| Entity identity | Is the report assigned to the correct government, period, entity type, and geographic scope? |

Statuses apply independently to every dimension: `VERIFIED`, `UNDER_REVIEW`, `FAILED_VALIDATION`, `INCOMPLETE_SOURCE`, `NOT_YET_VERIFIED`, and `NOT_APPLICABLE`. For a published financial fact, `NOT_APPLICABLE` is valid only for reconciliation. Extraction, classification, source completeness, and entity identity always require affirmative verification.

## Publication gates

A record is excluded when any of the following is true:

- Its amount is missing. Missing information is never converted to zero.
- Its source document or page is missing.
- Accounting basis, reporting scope, or value type is unknown.
- Any required verification dimension is unresolved, failed, incomplete, or not yet verified.
- It is marked as an elimination or excluded record.
- Its classification lacks a versioned rule or documented human decision.

An aggregate is also excluded when it mixes:

- Reporting periods.
- Accounting bases.
- Government-wide and fund-level scopes.
- Actual, estimated, and budget values.
- Different measure definitions.
- Interfund or unknown-scope activity into external revenue or expenditure totals.
- Duplicate fact identifiers.

## Immutability and corrections

Original observations remain unchanged. A correction creates a new or revised standardized fact, records the prior and corrected values, cites evidence, identifies the code or rule change, and stores the resulting validation outcome. A human decision has its own status and may be superseded without deleting its history.

## Current implementation

- `schema/validation.sql` defines the normalized evidence, classification, assessment, decision, and correction tables.
- `publication.py` implements record and aggregate gates independently of the source workbook.
- Regression tests cover missing values, incomplete verification, accounting-basis mixing, interfund aggregation, and database constraints.

