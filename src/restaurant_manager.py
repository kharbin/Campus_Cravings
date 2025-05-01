from datetime import datetime, time

class RestaurantManager:
    def __init__(self):
        self.restaurants = [
            {
                "name": "Basic Knead",
                "schedule": {"Mon": "1pm-12am", "Tue": "1pm-12am", "Wed": "1pm-12am", "Thu": "1pm-12am", "Fri": "1-10pm", "Sat": "-", "Sun": "4pm-12am"},
                "meal_exchange": "Yes",
                "menu": [
                    {"item": "Build Your Own Pizza", "price": 9.75, "category": "Entree", "dietary": ["Gluten-Friendly"], "meal_exchange": True, "options": {"toppings": ["Pepperoni", "Sausage", "Bacon", "Chicken", "Ground Beef", "Ham", "Olives", "Onions", "Mushrooms", "Bell Peppers", "Tomatoes", "Spinach", "Jalapeños", "Pineapple"], "max_toppings": 3, "sauce": ["BBQ", "Alfredo", "Pizza Sauce"]}},
                    {"item": "Build Your Own Calzone", "price": 9.95, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"toppings": ["Pepperoni", "Sausage", "Bacon", "Chicken", "Ground Beef", "Ham", "Olives", "Onions", "Mushrooms", "Bell Peppers", "Tomatoes", "Spinach", "Jalapeños", "Pineapple"], "max_toppings": 3, "sauce": ["BBQ", "Alfredo", "Pizza Sauce"]}},
                    {"item": "Build Your Own Pasta Bake", "price": 10.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"toppings": ["Pepperoni", "Sausage", "Bacon", "Chicken", "Ground Beef", "Ham", "Olives", "Onions", "Mushrooms", "Bell Peppers", "Tomatoes", "Spinach", "Jalapeños", "Pineapple"], "max_toppings": 3, "pasta": ["Fettuccini", "Penne", "Tri Color Rotini"], "sauce": ["Alfredo", "Marinara"]}},
                    {"item": "Cheese Calzone", "price": 8.25, "category": "Entree", "dietary": ["Vegetarian"], "meal_exchange": True},
                    {"item": "Pepperoni Calzone", "price": 8.75, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Garden Calzone", "price": 9.25, "category": "Entree", "dietary": ["Vegetarian"], "meal_exchange": True},
                    {"item": "Pepperoni and Sausage Calzone", "price": 9.50, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Boneless Wings", "price": 11.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"sauce": ["Buffalo", "BBQ", "Garlic Parmesan"]}},
                    {"item": "Extra Side of Sauce", "price": 1.50, "category": "Side", "dietary": [], "meal_exchange": False}
                ]
            },
            {
                "name": "Cafe 201",
                "schedule": {"Mon": "7:45am-2pm", "Tue": "7:45am-2pm", "Wed": "7:45am-2pm", "Thu": "7:45am-2pm", "Fri": "7:45am-2pm", "Sat": "-", "Sun": "-"},
                "meal_exchange": "Yes",
                "menu": [
                    {"item": "Brewed Coffee", "category": "Drink", "dietary": ["Vegan"], "meal_exchange": True, "options": {"size": {"Small": 2.25, "Medium": 2.65, "Large": 2.95}}},
                    {"item": "Latte", "category": "Drink", "dietary": [], "meal_exchange": True, "options": {"size": {"Small": 3.75, "Medium": 4.45, "Large": 4.95}}},
                    {"item": "Café Mocha", "category": "Drink", "dietary": [], "meal_exchange": True, "options": {"size": {"Small": 4.15, "Medium": 4.65, "Large": 4.95}}},
                    {"item": "Vanilla Latte", "category": "Drink", "dietary": [], "meal_exchange": True, "options": {"size": {"Small": 3.95, "Medium": 4.75, "Large": 5.25}}},
                    {"item": "Hot Chocolate", "category": "Drink", "dietary": [], "meal_exchange": True, "options": {"size": {"Small": 3.25, "Medium": 3.75, "Large": 3.95}}},
                    {"item": "Americana", "category": "Drink", "dietary": ["Vegan"], "meal_exchange": True, "options": {"size": {"Small": 2.95, "Medium": 3.45, "Large": 3.65}}},
                    {"item": "Iced Tea", "price": 2.00, "category": "Drink", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Bottled Soda", "price": 2.00, "category": "Drink", "dietary": [], "meal_exchange": True},
                    {"item": "Bottled Water", "price": 2.00, "category": "Drink", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Bottled Juice", "price": 1.75, "category": "Drink", "dietary": [], "meal_exchange": True},
                    {"item": "Powerade", "price": 2.45, "category": "Drink", "dietary": [], "meal_exchange": True},
                    {"item": "Monster", "price": 3.85, "category": "Drink", "dietary": [], "meal_exchange": True},
                    {"item": "Biscuits & Gravy (1)", "price": 2.75, "category": "Breakfast", "dietary": [], "meal_exchange": True, "available": "7:45am-10:45am"},
                    {"item": "Biscuits & Gravy (2)", "price": 4.50, "category": "Breakfast", "dietary": [], "meal_exchange": True, "available": "7:45am-10:45am"},
                    {"item": "Sausage, Egg & Cheese (Biscuit/English Muffin)", "price": 4.00, "category": "Breakfast", "dietary": [], "meal_exchange": True, "available": "7:45am-10:45am"},
                    {"item": "Sausage, Egg & Cheese (Croissant/Bagel)", "price": 5.25, "category": "Breakfast", "dietary": [], "meal_exchange": True, "available": "7:45am-10:45am"},
                    {"item": "Bagel with Cream Cheese", "price": 3.90, "category": "Breakfast", "dietary": ["Vegetarian"], "meal_exchange": True, "available": "7:45am-10:45am"},
                    {"item": "Grilled Cheese", "price": 4.00, "category": "Entree", "dietary": ["Vegetarian"], "meal_exchange": True},
                    {"item": "Hot Dog", "price": 4.50, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Chili Dog", "price": 5.50, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Flat Bread Pizza", "price": 8.00, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"type": ["Pepperoni", "Sausage", "Sundried Tomato Pesto"]}}
                ]
            },
            {
                "name": "Glow Kitchen",
                "schedule": {"Mon": "1pm-12am", "Tue": "1pm-12am", "Wed": "1pm-12am", "Thu": "1pm-12am", "Fri": "1-10pm", "Sat": "-", "Sun": "-"},
                "meal_exchange": "Yes",
                "menu": [
                    {"item": "Cross Chipotle Chicken Club", "price": 8.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"wrap": ["Naan", "Flour Tortilla"]}},
                    {"item": "Chicken Ranch Baconator", "price": 8.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"wrap": ["Naan", "Flour Tortilla"]}},
                    {"item": "Maui Jerk Chicken", "price": 9.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"wrap": ["Naan", "Flour Tortilla"]}},
                    {"item": "Buffalo Chicken Wrap", "price": 7.00, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"wrap": ["Naan", "Flour Tortilla"]}},
                    {"item": "Coastal Chicken Wrap", "price": 8.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"wrap": ["Naan", "Flour Tortilla"]}},
                    {"item": "The Sunny Day", "price": 6.95, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Cross Punch", "price": 5.75, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Paradise Beach", "price": 5.50, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Mango Tango", "price": 6.50, "category": "Smoothie", "dietary": [], "meal_exchange": True},
                    {"item": "Pink Lime", "price": 7.95, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Blueberry Magic", "price": 6.00, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Peanut Delight", "price": 6.00, "category": "Smoothie", "dietary": [], "meal_exchange": True},
                    {"item": "Piña Colada", "price": 6.50, "category": "Smoothie", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Berry Bowl", "price": 7.95, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Coconut Mango Bowl", "price": 8.25, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Pineapple Bowl", "price": 7.25, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "SunChips", "price": 1.95, "category": "Side", "dietary": [], "meal_exchange": False, "options": {"flavor": ["Cheddar", "Garden Salsa", "Chili Lime"]}},
                    {"item": "Baked Lays", "price": 1.95, "category": "Side", "dietary": [], "meal_exchange": False, "options": {"flavor": ["Original", "BBQ", "Cheddar Sour Cream"]}}
                ]
            },
            {
                "name": "The Crimson Panda",
                "schedule": {"Mon": "10am-6pm", "Tue": "10am-6pm", "Wed": "10am-6pm", "Thu": "10am-6pm", "Fri": "10am-5pm", "Sat": "-", "Sun": "-"},
                "meal_exchange": "2-6pm",
                "menu": [
                    {"item": "Egg Roll", "price": 4.00, "category": "Appetizer", "dietary": [], "meal_exchange": True},
                    {"item": "Veggie Spring Rolls (2)", "price": 3.50, "category": "Appetizer", "dietary": ["Vegetarian"], "meal_exchange": True},
                    {"item": "Pot Stickers (3)", "price": 4.00, "category": "Appetizer", "dietary": [], "meal_exchange": True},
                    {"item": "Jasmine Rice", "price": 4.00, "category": "Side", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Fried Rice", "price": 4.00, "category": "Side", "dietary": [], "meal_exchange": True},
                    {"item": "Lo Mein", "price": 4.00, "category": "Side", "dietary": [], "meal_exchange": True},
                    {"item": "Steamed Greens", "price": 4.00, "category": "Side", "dietary": ["Vegan"], "meal_exchange": True},
                    {"item": "Tangerine Chicken", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "General Tso's Chicken", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Honey Sriracha Chicken", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Mushroom Chicken", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Broccoli Beef", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Pepper Steak", "price": 6.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Plate (1 Entree + 1 Side)", "price": 8.00, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"entree": ["Tangerine Chicken", "General Tso's Chicken", "Honey Sriracha Chicken", "Mushroom Chicken", "Broccoli Beef", "Pepper Steak"], "side": ["Jasmine Rice", "Fried Rice", "Lo Mein", "Steamed Greens"]}},
                    {"item": "Platter (2 Entrees + 1 Side)", "price": 12.00, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"entree": ["Tangerine Chicken", "General Tso's Chicken", "Honey Sriracha Chicken", "Mushroom Chicken", "Broccoli Beef", "Pepper Steak"], "side": ["Jasmine Rice", "Fried Rice", "Lo Mein", "Steamed Greens"], "max_entrees": 2}},
                    {"item": "Soft Drink", "price": 2.00, "category": "Drink", "dietary": [], "meal_exchange": True}
                ]
            },
            {
                "name": "Credo Kitchen",
                "schedule": {"Mon": "1pm-12am", "Tue": "1pm-12am", "Wed": "1pm-12am", "Thu": "1pm-12am", "Fri": "1-10pm", "Sat": "-", "Sun": "4pm-12am"},
                "meal_exchange": "Yes",
                "menu": [
                    {"item": "Ruthie's Classic Cheeseburger", "price": 9.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"cheese": ["Cheddar", "Pepper Jack", "Swiss"], "combo": {"Side": ["French Fries", "Corn"], "Drink": ["Soft Drink"], "price": 3.50}}},
                    {"item": "Hamburger", "price": 8.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"cheese": ["Cheddar", "Pepper Jack", "Swiss"], "combo": {"Side": ["French Fries", "Corn"], "Drink": ["Soft Drink"], "price": 3.50}}},
                    {"item": "Bacon Cheeseburger", "price": 11.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"cheese": ["Cheddar", "Pepper Jack", "Swiss"], "combo": {"Side": ["French Fries", "Corn"], "Drink": ["Soft Drink"], "price": 3.50}}},
                    {"item": "Vegetarian Burger", "price": 8.95, "category": "Entree", "dietary": ["Vegetarian"], "meal_exchange": True, "options": {"combo": {"Side": ["French Fries", "Corn"], "Drink": ["Soft Drink"], "price": 3.50}}},
                    {"item": "Spicy Chicken Sandwich", "price": 9.50, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"combo": {"Side": ["French Fries", "Corn"], "Drink": ["Soft Drink"], "price": 3.50}}},
                    {"item": "Corn Dog Basket", "price": 11.00, "category": "Entree", "dietary": [], "meal_exchange": True},
                    {"item": "Chicken Basket", "price": 12.00, "category": "Entree", "dietary": [], "meal_exchange": True, "options": {"sauce": ["BBQ", "Ranch", "Honey Mustard"]}},
                    {"item": "French Fries", "price": 3.25, "category": "Side", "dietary": [], "meal_exchange": True},
                    {"item": "Corn", "price": 3.25, "category": "Side", "dietary": [], "meal_exchange": True},
                    {"item": "Avocado Spread", "price": 1.75, "category": "Side", "dietary": ["Vegan"], "meal_exchange": False},
                    {"item": "Grilled Red Onions", "price": 2.75, "category": "Side", "dietary": ["Vegan"], "meal_exchange": False},
                    {"item": "Grilled Mushrooms", "price": 1.10, "category": "Side", "dietary": ["Vegan"], "meal_exchange": False},
                    {"item": "Grilled Jalapeños", "price": 1.10, "category": "Side", "dietary": ["Vegan"], "meal_exchange": False},
                    {"item": "Add Egg", "price": 2.00, "category": "Side", "dietary": [], "meal_exchange": False},
                    {"item": "Extra Patty", "price": 4.25, "category": "Side", "dietary": [], "meal_exchange": False},
                    {"item": "Extra Bacon", "price": 2.25, "category": "Side", "dietary": [], "meal_exchange": False},
                    {"item": "Extra Ranch", "price": 1.25, "category": "Side", "dietary": [], "meal_exchange": False},
                    {"item": "Extra BBQ", "price": 1.25, "category": "Side", "dietary": [], "meal_exchange": False},
                    {"item": "Extra Honey Mustard", "price": 1.25, "category": "Side", "dietary": [], "meal_exchange": False}
                ]
            }
        ]

    def is_open(self, schedule, day, current_time):
        hours = schedule.get(day, "-")
        if hours == "-":
            return False
        for period in hours.split(", "):
            try:
                start, end = period.split("-")
                start_time = datetime.strptime(start, "%I:%M%p" if ":" in start else "%I%p").time()
                end_time = datetime.strptime(end, "%I:%M%p" if ":" in end else "%I%p").time()
                if start_time <= current_time <= end_time:
                    return True
            except ValueError:
                continue
        return False

    def is_item_available(self, item, current_time):
        if "available" not in item:
            return True
        try:
            start, end = item["available"].split("-")
            start_time = datetime.strptime(start, "%I:%M%p" if ":" in start else "%I%p").time()
            end_time = datetime.strptime(end, "%I:%M%p" if ":" in end else "%I%p").time()
            return start_time <= current_time <= end_time
        except ValueError:
            return True

    def filter_restaurants(self, meal_exchange_filter):
        if not meal_exchange_filter:
            return self.restaurants
        return [r for r in self.restaurants if r["meal_exchange"] not in ["No", "N/A"]]
