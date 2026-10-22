import sqlite3
import sys
import unittest
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nebraska_audit_validation.publication import (
    PublicationCandidate,
    VerificationDimension,
    VerificationStatus,
    evaluate_aggregate,
    evaluate_publication,
)


def verified_candidate(**changes):
    candidate = PublicationCandidate(
        fact_id="fact-1",
        measure_definition_id="revenue",
        entity_id="entity-1",
        reporting_period_end="2025-06-30",
        accounting_basis="cash",
        reporting_scope="governmental_funds",
        value_type="AUDITED_ACTUAL",
        amount=Decimal("0.00"),
        source_document_id="document-1",
        source_page=3,
        publication_role="primary",
        transaction_scope="external",
        statuses={dimension: VerificationStatus.VERIFIED for dimension in VerificationDimension},
    )
    return replace(candidate, **changes)


class PublicationGateTest(unittest.TestCase):
    def test_source_supported_zero_is_publishable(self):
        result = evaluate_publication(verified_candidate())
        self.assertTrue(result.eligible)
        self.assertEqual(result.reasons, ())

    def test_missing_amount_is_not_treated_as_zero(self):
        result = evaluate_publication(verified_candidate(amount=None))
        self.assertFalse(result.eligible)
        self.assertIn("amount is missing", result.reasons[0])

    def test_under_review_dimension_blocks_publication(self):
        statuses = {dimension: VerificationStatus.VERIFIED for dimension in VerificationDimension}
        statuses[VerificationDimension.CLASSIFICATION] = VerificationStatus.UNDER_REVIEW
        result = evaluate_publication(verified_candidate(statuses=statuses))
        self.assertFalse(result.eligible)
        self.assertIn("classification status is UNDER_REVIEW", result.reasons)

    def test_not_applicable_dimension_passes(self):
        statuses = {dimension: VerificationStatus.VERIFIED for dimension in VerificationDimension}
        statuses[VerificationDimension.RECONCILIATION] = VerificationStatus.NOT_APPLICABLE
        self.assertTrue(evaluate_publication(verified_candidate(statuses=statuses)).eligible)

    def test_not_applicable_extraction_does_not_pass(self):
        statuses = {dimension: VerificationStatus.VERIFIED for dimension in VerificationDimension}
        statuses[VerificationDimension.EXTRACTION] = VerificationStatus.NOT_APPLICABLE
        result = evaluate_publication(verified_candidate(statuses=statuses))
        self.assertFalse(result.eligible)
        self.assertIn("extraction status is NOT_APPLICABLE", result.reasons)

    def test_mixed_basis_aggregate_is_blocked(self):
        facts = [verified_candidate(), verified_candidate(fact_id="fact-2", accounting_basis="GAAP")]
        result = evaluate_aggregate(facts)
        self.assertFalse(result.eligible)
        self.assertTrue(any(reason.startswith("mixed accounting basis") for reason in result.reasons))

    def test_interfund_revenue_is_blocked_from_operating_aggregate(self):
        facts = [verified_candidate(transaction_scope="interfund")]
        result = evaluate_aggregate(facts)
        self.assertFalse(result.eligible)
        self.assertTrue(any("nonexternal" in reason for reason in result.reasons))


class DatabaseConstraintTest(unittest.TestCase):
    def test_schema_rejects_unknown_verification_status(self):
        schema = (Path(__file__).resolve().parents[1] / "schema" / "validation.sql").read_text()
        connection = sqlite3.connect(":memory:")
        connection.executescript(schema)
        with self.assertRaises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO source_document (
                    document_id, content_sha256, filename, entity_id, reporting_period_end,
                    accounting_basis, filing_type, source_completeness_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("doc", "a" * 64, "a.pdf", "entity", "2025-06-30", "cash", "Audit", "MAYBE", "now"),
            )


if __name__ == "__main__":
    unittest.main()
