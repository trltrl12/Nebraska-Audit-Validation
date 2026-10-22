import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nebraska_audit_validation.quality import _semantic_duplicate_candidates


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


if __name__ == "__main__":
    unittest.main()
