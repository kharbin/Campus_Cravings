import unittest
from datetime import datetime
from discounts import calculate_discounted_total, apply_discount, is_discount_valid

class TestDiscountApplication(unittest.TestCase):

    def setUp(self):
        self.today = datetime(2025, 4, 30)

    def test_discount_applied_correctly(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "alice")
        self.assertEqual(new_total, 10.00)

    def test_discount_does_not_go_negative(self):
        total = 8.00  # Less than discount
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "alice")
        self.assertEqual(new_total, 0.00)  # Should never go below 0

    def test_discount_not_applied_to_ineligible_user(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", self.today, "bob")  # Bob is faculty
        self.assertEqual(new_total, 20.00)

    def test_invalid_discount_code_does_nothing(self):
        total = 20.00
        new_total = calculate_discounted_total(total, "FAKECODE", self.today, "alice")
        self.assertEqual(new_total, 20.00)

    def test_expired_discount_not_applied(self):
        expired_date = datetime(2026, 1, 1)
        total = 20.00
        new_total = calculate_discounted_total(total, "STUDENT10", expired_date, "alice")
        self.assertEqual(new_total, 20.00)

if __name__ == "__main__":
    unittest.main()
