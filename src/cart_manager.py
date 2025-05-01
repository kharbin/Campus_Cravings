class CartManager:
    def __init__(self):
        self.cart = []
        self.orders = []

    def add_to_cart(self, item, restaurant, selections, price):
        self.cart.append({
            "item": item["item"],
            "restaurant": restaurant,
            "selections": selections,
            "price": price,
            "meal_exchange": item["meal_exchange"]
        })

    def get_total(self):
        return sum(item["price"] for item in self.cart)

    def checkout(self):
        order = {
            "order_id": len(self.orders) + 1,
            "restaurant": self.cart[0]["restaurant"] if self.cart else "",
            "items": self.cart,
            "status": "Pending",
            "payment_method": "Meal Swipe"
        }
        self.orders.append(order)
        self.cart = []
