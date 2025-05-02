import unittest
from cart import Cart

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

if __name__ == "__main__":
    unittest.main()
