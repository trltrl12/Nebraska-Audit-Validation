# Phase 4 Incomplete Reconciliation Review

The initial scanner reported 339 blank governmental reconciliation results. Review of the retained source JSON established that 338 are business-only reports with no governmental receipts, disbursements, or fund balances. Their governmental roll-forward is not applicable, so a blank result is not an incomplete validation.

Hickman is the single remaining incomplete governmental reconciliation. Its source JSON contains governmental receipts, disbursements, and ending balance, but the retained PDF lacks the governmental statements needed to establish beginning fund balance. It remains `INCOMPLETE_SOURCE` and is excluded from verified publication for that measure.

The quality scanner now checks whether the source document contains governmental financial facts before creating `REC-GOV-002`. Missing or unreadable JSON remains conservatively in scope so evidence failures cannot silently clear an incomplete finding.
