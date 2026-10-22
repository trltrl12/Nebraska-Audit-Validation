import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nebraska_audit_validation.quality import _resolution_matches, _semantic_duplicate_candidates


def detail(**changes):
    row = {
        "filename": "Example_FY2025.pdf",
        "entity_name": "Example",
        "source_page": "4",
        "schedule": "Schedule A",
        "fund": "General Fund",
        "department": "",
        "original_label": "Property taxes",
        "amount": "100.00",
        "section": "revenue",
        "category": "property tax",
        "detail_category": "property tax",
    }
    row.update(changes)
    return row


class SemanticDuplicateTest(unittest.TestCase):
    def test_equal_amounts_on_different_pages_are_not_candidates(self):
        rows = [detail(), detail(source_page="5")]
        self.assertEqual(_semantic_duplicate_candidates(rows), [])

    def test_equal_amounts_with_different_labels_are_not_candidates(self):
        rows = [detail(), detail(original_label="Sales taxes")]
        self.assertEqual(_semantic_duplicate_candidates(rows), [])

    def test_same_source_location_is_a_review_candidate(self):
        rows = [detail(), detail(category="other taxes")]
        findings = _semantic_duplicate_candidates(rows)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule_id, "DUP-SOURCE-001")
        self.assertEqual(findings[0].severity, "REVIEW")


class ResolvedFindingTest(unittest.TestCase):
    def setUp(self):
        self.resolutions = [
            {
                "filename": "Example_FY2025",
                "source_page": "4",
                "original_label": "Transfer account (Receipts)",
                "rule_ids": ["CLASS-TRANSFER-001", "SOURCE-FLAG-001"],
            }
        ]

    def test_exact_reviewed_finding_is_resolved(self):
        self.assertTrue(
            _resolution_matches(
                self.resolutions,
                rule_id="CLASS-TRANSFER-001",
                filename="Example_FY2025",
                source_page="4",
                label_or_reason="Transfer account (Receipts)",
            )
        )

    def test_different_page_does_not_clear_finding(self):
        self.assertFalse(
            _resolution_matches(
                self.resolutions,
                rule_id="CLASS-TRANSFER-001",
                filename="Example_FY2025",
                source_page="5",
                label_or_reason="Transfer account (Receipts)",
            )
        )

    def test_substring_does_not_clear_different_label(self):
        self.assertFalse(
            _resolution_matches(
                self.resolutions,
                rule_id="SOURCE-FLAG-001",
                filename="Example_FY2025",
                source_page="4",
                label_or_reason="Transfer account fee (Receipts)",
            )
        )


if __name__ == "__main__":
    unittest.main()
