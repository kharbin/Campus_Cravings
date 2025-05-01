# ------------------------------- Component: Cart for Food Delivery App -------------------------------
import unittest

class Cart:
    def __init__(self):
        self.items = []

#add items to cart
    def add_item(self, item):
        if isinstance(item, str) and item:
            self.items.append(item)
            return True
        return False

#removes item from cart
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

#views item in cart by returning a copy of the current items in the cart
    def view_cart(self):
        return self.items.copy()

#clears the entire cart
    def clear_cart(self):
        self.items = []

#checks whether cart is empty or not
    def is_empty(self):
        return len(self.items) == 0

#checkout process
    def checkout(self):
        if self.is_empty():
            return "Cart is empty. Add items before checkout."
        total_items = len(self.items)
        self.clear_cart()
        return f"Checkout complete. {total_items} item(s) purchased."

# ------------------------------- Unit Tests for Cart -------------------------------

class TestCart(unittest.TestCase):

#sets up a new cart before each test
    def setUp(self):
        self.cart = Cart()

#tests if you can add valid item in cart
    def test_add_item(self):
        result = self.cart.add_item("Burger")
        self.assertTrue(result)
        self.assertIn("Burger", self.cart.view_cart())

#tests to see if you can add an invalid item in cart
    def test_add_invalid_item(self):
        result = self.cart.add_item("")  # Invalid: empty string
        self.assertFalse(result)
        self.assertEqual(self.cart.view_cart(), [])

#tests if you can remove an item in the cart
    def test_remove_existing_item(self):
        self.cart.add_item("Sushi")
        result = self.cart.remove_item("Sushi")
        self.assertTrue(result)
        self.assertNotIn("Sushi", self.cart.view_cart())

#tests if you can remove an item not in the cart
    def test_remove_nonexistent_item(self):
        result = self.cart.remove_item("Pizza")
        self.assertFalse(result)

#tests if checkout process works with all the items
    def test_cart_checkout(self):
        self.cart.add_item("Salad")
        message = self.cart.checkout()
        self.assertIn("Checkout complete", message)
        self.assertTrue(self.cart.is_empty())

#tests if you can clear all items in the cart
    def test_checkout_empty_cart(self):
        message = self.cart.checkout()
        self.assertEqual(message, "Cart is empty. Add items before checkout.")

    def test_clear_cart(self):
        self.cart.add_item("Pasta")
        self.cart.clear_cart()
        self.assertTrue(self.cart.is_empty())

# ------------------------------- Run All Tests -------------------------------
if __name__ == "__main__":
    unittest.main()
