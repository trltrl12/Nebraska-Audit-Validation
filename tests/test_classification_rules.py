import json
import unittest
from pathlib import Path


class ClassificationRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "config" / "classification_rules.json"
        cls.ruleset = json.loads(path.read_text(encoding="utf-8"))
        cls.rules = {rule["rule_id"]: rule for rule in cls.ruleset["rules"]}

    def test_rule_ids_are_unique(self):
        rules = self.ruleset["rules"]
        self.assertEqual(len(rules), len({rule["rule_id"] for rule in rules}))

    def test_every_rule_preserves_original_label(self):
        self.assertTrue(all(rule["preserve_original_label"] for rule in self.ruleset["rules"]))

    def test_warrant_rule_has_no_forced_debt_maturity_default(self):
        rule = self.rules["SID-WARRANT-001"]
        self.assertEqual(rule["fallback"], "UNDER_REVIEW")
        self.assertIn("always current payable", rule["prohibited_defaults"])
        self.assertIn("always long-term debt", rule["prohibited_defaults"])

    def test_actual_basis_comes_from_schedule(self):
        rule = self.rules["SID-ACTUAL-BASIS-001"]
        self.assertIn("printed on the schedule", rule["decision"])
        self.assertEqual(rule["fallback"], "UNDER_REVIEW")

    def test_maintenance_fallback_is_explicitly_recorded(self):
        rule = self.rules["SID-MAINT-001"]
        self.assertEqual(rule["fallback"], "streets/highways")
        self.assertEqual(rule["classification_support"], "HUMAN_DECISION")
        self.assertTrue(rule["fallback_must_be_recorded"])


if __name__ == "__main__":
    unittest.main()
