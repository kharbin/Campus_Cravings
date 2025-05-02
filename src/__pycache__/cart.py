import unittest

class Cart:
    
    #makes cart for specific user and doesn't allow for non-empty string 
    def __init__(self, user_id):
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string.")
        self.user_id = user_id
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

    #checks whether cart is empty or not
    def is_empty(self):
        return len(self.items) == 0

    #checkout process; returns checkout complete if purchase is valid and and cart is empty. add items before checkout if cart is empty
    def checkout(self):
        if self.is_empty():
            return "Cart is empty. You can not checkout."
        self.items = []
        return "Checkout complete."

# ------------------------------- Unit Tests for Cart -------------------------------

class TestCart(unittest.TestCase):

    #sets up a new cart before each test
    def setUp(self):
        self.cart = Cart("user1")

    #tests if you can add valid item in cart
    def test_add_item(self):
        result = self.cart.add_item("Burger")
        self.assertTrue(result)
        self.assertIn("Burger", self.cart.view_cart())

    #tests if you can remove an item in the cart
    def test_remove_item(self):
        self.cart.add_item("Burger")
        result = self.cart.remove_item("Burger")
        self.assertTrue(result)
        self.assertNotIn("Burger", self.cart.view_cart())

    #tests if checkout process works with all the items
    def test_cart_checkout(self):
        self.cart.add_item("Burger")
        message = self.cart.checkout()
        self.assertIn("Checkout complete", message)
        self.assertTrue(self.cart.is_empty())

    #tests checkout process when cart is empty 
    def test_checkout_empty_cart(self):
        message = self.cart.checkout()
        self.assertEqual(message, "Cart is empty. You can not checkout.")
        
    #tests that cart can't be created by invalid user
    def test_invalid_user_id(self):
        with self.assertRaises(ValueError):
            Cart("  ")

# ------------------------------- Running the Tests -------------------------------
if __name__ == "__main__":
    unittest.main()
