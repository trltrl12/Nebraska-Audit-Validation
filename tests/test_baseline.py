import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nebraska_audit_validation.baseline import (
    _duplicate_keys,
    _duplicate_rows,
    _stem,
    render_markdown,
)


class BaselineHelpersTest(unittest.TestCase):
    def test_stem_normalizes_pdf_and_json_names(self):
        self.assertEqual(_stem("Example_FY2025.pdf"), "Example_FY2025")
        self.assertEqual(_stem("Example_FY2025.json"), "Example_FY2025")

    def test_exact_duplicate_rows_require_all_fields_to_match(self):
        rows = [
            {"entity": "A", "amount": "10", "page": "1"},
            {"entity": "A", "amount": "10", "page": "1"},
            {"entity": "A", "amount": "10", "page": "2"},
        ]
        self.assertEqual(_duplicate_rows(rows), {"groups": 1, "extra_rows": 1})

    def test_duplicate_business_key_is_separate_from_exact_duplicate(self):
        rows = [
            {"entity": "A", "year": "2025", "basis": "cash", "amount": "10"},
            {"entity": "A", "year": "2025", "basis": "cash", "amount": "20"},
        ]
        self.assertEqual(
            _duplicate_keys(rows, ["entity", "year", "basis"]),
            {"groups": 1, "extra_rows": 1},
        )
        self.assertEqual(_duplicate_rows(rows), {"groups": 0, "extra_rows": 0})

    def test_markdown_states_verification_limit(self):
        data = {
            "generated_at": "2026-10-22T00:00:00+00:00",
            "scope": {"source_commit": "abc"},
            "inventory": {
                "summary_rows": 1,
                "file_list_rows": 1,
                "manifest_rows": 1,
                "trimmed_pdfs": 1,
                "json_reports": 1,
                "verifier_reports": 1,
                "long_rows": 1,
                "detail_rows": 1,
                "review_rows": 0,
                "needs_decision_rows": 0,
                "flagged_rows": 0,
            },
            "workflow_status": {"done": 1, "flagged": 0},
            "reconciliation": {
                name: {"yes": 1, "no": 0, "": 0}
                for name in (
                    "governmental_rollforward",
                    "proprietary_cashflow",
                    "business_type_rollforward",
                    "balance_sheet",
                )
            },
            "source_coverage": {
                "summary_missing_source_url": 0,
                "detail_missing_source_url": 0,
                "detail_missing_source_page": 0,
                "json_without_trimmed_pdf": [],
                "trimmed_pdf_without_json": [],
                "json_without_verifier": [],
                "listed_without_manifest": [],
                "manifest_without_trimmed_pdf": [],
            },
            "integrity": {"amount_not_found_review_items": 0},
            "known_exceptions": {
                "failed_governmental_reconciliations": 0,
                "missing_governmental_reconciliation_result": 0,
                "flagged": [],
            },
        }
        report = render_markdown(data)
        self.assertIn("not comprehensive verification against every PDF", report)
        self.assertIn("not publication-ready", report)


if __name__ == "__main__":
    unittest.main()
