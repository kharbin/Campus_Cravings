import unittest
from datetime import datetime
from discount_feature import (
    calculate_discounted_total,
    apply_discount,
    is_discount_valid
)

# ------------------------------- Unit Test Class for Discount Feature -------------------------------
class TestDiscountFeature(unittest.TestCase):

    def setUp(self):
        # Common test date for all scenarios
        self.today = datetime(2025, 4, 30)

    # -------------------- Reliability Test: Discount is applied correctly --------------------
    def test_discount_applied_correctly(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "alice")
        self.assertEqual(new_total, 10.00)

    # -------------------- Edge Case Test: Discount does not go below zero --------------------
    def test_discount_does_not_go_negative(self):
        total = 8.00
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "alice")
        self.assertEqual(new_total, 0.00)

    # -------------------- Security Test: Ineligible user cannot use discount --------------------
    def test_discount_not_applied_to_ineligible_user(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "bob")
        self.assertEqual(new_total, 20.00)

    # -------------------- Reliability Test: Invalid discount code is ignored --------------------
    def test_invalid_discount_code_does_nothing(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "FAKECODE", self.today, "alice")
        self.assertEqual(new_total, 20.00)

    # -------------------- Reliability Test: Expired discount is not applied --------------------
    def test_expired_discount_not_applied(self):
        expired_date = datetime(2026, 1, 1)
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", expired_date, "alice")
        self.assertEqual(new_total, 20.00)

# ------------------------------- Running the Tests -------------------------------
if __name__ == '__main__':
    unittest.main()
