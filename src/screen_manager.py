import pygame
from datetime import datetime
from .constants import Constants
from .button import Button
from .ai_recommendation.recommendation_interface import RecommendationInterface

class ScreenManager:
    def __init__(self, screen, font, restaurant_manager, cart_manager, users, app, meal_recommender, user_preference_manager):
        self.screen = screen
        self.font = font
        self.restaurant_manager = restaurant_manager
        self.cart_manager = cart_manager
        self.users = users
        self.app = app
        self.state = app.state
        self.meal_recommender = meal_recommender
        self.user_preference_manager = user_preference_manager
        self.filtered_restaurants = []
        self.customer_buttons = []
        self.menu_buttons = []
        self.option_buttons = []
        self.restaurant_buttons = []
        self.window_width = Constants.WIDTH
        self.window_height = Constants.HEIGHT
        button_width = 200
        button_height = 50
        total_button_width = button_width * 3
        spacing = (self.window_width - total_button_width) // 4
        self.role_buttons = [
            Button(spacing, 200, button_width, button_height, "Customer", lambda: self.state.update({"screen": "login_screen"}), self.font),
            Button(spacing * 2 + button_width, 200, button_width, button_height, "Restaurant", lambda: self.state.update({"screen": "restaurant"}), self.font),
            Button(spacing * 3 + button_width * 2, 200, button_width, button_height, "Driver", lambda: self.state.update({"screen": "driver"}), self.font),
        ]
        self.back_button = Button(self.window_width // 4 - 100, self.window_height - 100, 200, 50, "Back", 
                                 lambda: self.state.update({
                                     "screen": "role_selection" if self.state["screen"] in ["customer", "restaurant", "driver", "login_screen", "recommendation"] 
                                     else "customer" if self.state["screen"] == "menu_screen" 
                                     else "menu_screen" if self.state["screen"] == "option_screen" 
                                     else "menu_screen" if self.state["screen"] == "cart_screen" and self.state["selected_restaurant"]
                                     else "customer" if self.state["screen"] == "cart_screen"
                                     else "customer" if self.state["screen"] == "confirmation_screen" and not self.state["selected_restaurant"]
                                     else "menu_screen",
                                     "selected_restaurant": None if self.state["screen"] in ["customer", "restaurant", "driver"] else self.state["selected_restaurant"],
                                     "scroll_offset": 0, "option_selection": None,
                                     "username_input": "", "password_input": "", "login_error": "", "active_input": None,
                                     "recommendation": None
                                 }), self.font)
        self.cart_button = Button(3 * self.window_width // 4 - 100, self.window_height - 100, 200, 50, "View Cart", 
                                 lambda: self.state.update({"screen": "cart_screen"}), self.font)
        self.checkout_button = Button(self.window_width // 2 - 125, self.window_height - 100, 250, 50, "Checkout", 
                                     lambda: self.state.update({"screen": "confirmation_screen"}) or self.cart_manager.checkout() if self.cart_manager.cart else None, self.font)
        self.exit_button = Button(self.window_width // 2 + 25, self.window_height - 100, 200, 50, "Exit App", 
                                 lambda: self.close_app(), self.font)
        self.recommend_button = Button(
            self.window_width // 2 - 100, self.window_height - 150, 200, 50, "Recommend Meal",
            lambda: self.state.update({"screen": "recommendation"}), self.font
        )
        self.restaurant_buttons = [
            Button(50, 50 + i * 60, self.window_width - 100, 50, f"{restaurant['name']} (Link)", 
                   lambda r=restaurant: print(f"Link for {r['name']} clicked"), self.font)
            for i, restaurant in enumerate(self.restaurant_manager.restaurants)
        ]
        self.restaurant_filter_input = ""
        self.restaurant_filter_rect = pygame.Rect(self.window_width // 2 - 100, 120, 200, 40)
        self.restaurant_filter_active = False
        self.restaurant_filter_label = self.font.render("Enter Restaurant Here", True, Constants.CRIMSON)
        self.selected_restaurant_index = None
        self.username_rect = pygame.Rect(self.window_width // 2 - 100, 200, 200, 40)
        self.password_rect = pygame.Rect(self.window_width // 2 - 100, 260, 200, 40)
        self.login_button = Button(self.window_width // 2 - 100, 320, 200, 50, "Login", self.handle_login, self.font)
        self.recommendation_interface = RecommendationInterface(screen, font, meal_recommender, user_preference_manager, app)

    def handle_login(self):
        username = self.state["username_input"]
        password = self.state["password_input"]
        if self.users.validate_login(username, password):
            self.state.update({
                "screen": "customer",
                "username_input": "",
                "password_input": "",
                "login_error": "",
                "active_input": None,
                "selected_user": username
            })
        else:
            self.state["login_error"] = "Invalid username or password"

    def close_app(self):
        print("close_app() called, setting running to False.")
        self.app.running = False

    def handle_events(self):
        current_time = datetime.now().time()
        day = datetime.now().strftime("%a")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("pygame.QUIT event detected, setting running to False.")
                self.app.running = False
                return
            if event.type == pygame.VIDEORESIZE:
                self.window_width, self.window_height = event.w, event.h
                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.back_button.rect = pygame.Rect(self.window_width // 4 - 100, self.window_height - 100, 200, 50)
                self.back_button.text_rect = self.back_button.text.get_rect(center=self.back_button.rect.center)
                self.cart_button.rect = pygame.Rect(3 * self.window_width // 4 - 100, self.window_height - 100, 200, 50)
                self.cart_button.text_rect = self.cart_button.text.get_rect(center=self.cart_button.rect.center)
                self.checkout_button.rect = pygame.Rect(self.window_width // 2 - 125, self.window_height - 100, 250, 50)
                self.checkout_button.text_rect = self.checkout_button.text.get_rect(center=self.checkout_button.rect.center)
                self.exit_button.rect = pygame.Rect(self.window_width // 2 + 25, self.window_height - 100, 200, 50)
                self.exit_button.text_rect = self.exit_button.text.get_rect(center=self.exit_button.rect.center)
                self.recommend_button.rect = pygame.Rect(self.window_width // 2 - 100, self.window_height - 150, 200, 50)
                self.recommend_button.text_rect = self.recommend_button.text.get_rect(center=self.recommend_button.rect.center)
                button_width = 200
                button_height = 50
                total_button_width = button_width * 3
                spacing = max(10, (self.window_width - total_button_width) // 4)
                self.role_buttons = [
                    Button(spacing, 200, button_width, button_height, "Customer", lambda: self.state.update({"screen": "login_screen"}), self.font),
                    Button(spacing * 2 + button_width, 200, button_width, button_height, "Restaurant", lambda: self.state.update({"screen": "restaurant"}), self.font),
                    Button(spacing * 3 + button_width * 2, 200, button_width, button_height, "Driver", lambda: self.state.update({"screen": "driver"}), self.font),
                ]
                self.restaurant_buttons = [
                    Button(50, 50 + i * 60, self.window_width - 100, 50, f"{restaurant['name']} (Link)", 
                           lambda r=restaurant: print(f"Link for {r['name']} clicked"), self.font)
                    for i, restaurant in enumerate(self.restaurant_manager.restaurants)
                ]
                self.restaurant_filter_rect = pygame.Rect(self.window_width // 2 - 100, 120, 200, 40)
                self.username_rect = pygame.Rect(self.window_width // 2 - 100, 200, 200, 40)
                self.password_rect = pygame.Rect(self.window_width // 2 - 100, 260, 200, 40)
                self.login_button.rect = pygame.Rect(self.window_width // 2 - 100, 320, 200, 50)
                self.login_button.text_rect = self.login_button.text.get_rect(center=self.login_button.rect.center)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state["screen"] == "role_selection":
                    for button in self.role_buttons:
                        button.check_click(event.pos)
                elif self.state["screen"] == "login_screen":
                    if event.button == 1:
                        self.login_button.check_click(event.pos)
                        self.back_button.check_click(event.pos)
                        if self.username_rect.collidepoint(event.pos):
                            self.state["active_input"] = "username"
                        elif self.password_rect.collidepoint(event.pos):
                            self.state["active_input"] = "password"
                        else:
                            self.state["active_input"] = None
                elif self.state["screen"] == "customer":
                    if event.button == 1:
                        if self.restaurant_filter_rect.collidepoint(event.pos):
                            self.restaurant_filter_active = True
                        else:
                            self.restaurant_filter_active = False
                        y_start = 180
                        visible_restaurants = self.filtered_restaurants[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + 7]
                        for i, restaurant in enumerate(visible_restaurants):
                            restaurant_rect = pygame.Rect(self.window_width // 2 - 100, y_start + i * 40, 200, 30)
                            if restaurant_rect.collidepoint(event.pos):
                                self.selected_restaurant_index = i + self.state["scroll_offset"]
                                self.state.update({"screen": "menu_screen", "selected_restaurant": restaurant, "scroll_offset": 0})
                                break
                        self.back_button.check_click(event.pos)
                        self.cart_button.check_click(event.pos)
                        self.recommend_button.check_click(event.pos)
                    elif event.button == 4:
                        self.state["scroll_offset"] = max(0, self.state["scroll_offset"] - 1)
                    elif event.button == 5:
                        self.state["scroll_offset"] = min(len(self.filtered_restaurants) - 7, self.state["scroll_offset"] + 1)
                elif self.state["screen"] == "menu_screen":
                    if event.button == 1:
                        visible_buttons = self.menu_buttons[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + 7]
                        for button in visible_buttons:
                            button.check_click(event.pos)
                        self.cart_button.check_click(event.pos)
                        self.back_button.check_click(event.pos)
                    elif event.button == 4:
                        self.state["scroll_offset"] = max(0, self.state["scroll_offset"] - 1)
                    elif event.button == 5:
                        self.state["scroll_offset"] = min(len([i for i in self.state["selected_restaurant"]["menu"] if self.restaurant_manager.is_item_available(i, current_time)]) - 7, self.state["scroll_offset"] + 1)
                elif self.state["screen"] == "option_screen":
                    if event.button == 1:
                        for button in self.option_buttons:
                            button.check_click(event.pos)
                        self.back_button.check_click(event.pos)
                    elif event.button == 4:
                        self.state["scroll_offset"] = max(0, self.state["scroll_offset"] - 1)
                    elif event.button == 5:
                        self.state["scroll_offset"] = min(len(self.option_buttons) - 7, self.state["scroll_offset"] + 1)
                elif self.state["screen"] == "cart_screen":
                    if event.button == 1:
                        self.checkout_button.check_click(event.pos)
                        self.back_button.check_click(event.pos)
                    elif event.button == 4:
                        visible_items = (self.window_height - 200) // 40
                        self.state["scroll_offset"] = max(0, self.state["scroll_offset"] - 1)
                    elif event.button == 5:
                        visible_items = (self.window_height - 200) // 40
                        self.state["scroll_offset"] = min(len(self.cart_manager.cart) - visible_items, self.state["scroll_offset"] + 1)
                elif self.state["screen"] == "recommendation":
                    self.recommendation_interface.handle_events()
                elif self.state["screen"] in ["restaurant", "driver"]:
                    self.back_button.check_click(event.pos)
                elif self.state["screen"] == "confirmation_screen":
                    if event.button == 1:
                        self.back_button.check_click(event.pos)
                        self.exit_button.check_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if self.state["screen"] == "login_screen":
                    if self.state["active_input"] == "username":
                        if event.key == pygame.K_BACKSPACE:
                            self.state["username_input"] = self.state["username_input"][:-1]
                        elif event.key == pygame.K_RETURN:
                            self.state["active_input"] = "password"
                        elif event.unicode.isprintable() and len(self.state["username_input"]) < 20:
                            self.state["username_input"] += event.unicode
                    elif self.state["active_input"] == "password":
                        if event.key == pygame.K_BACKSPACE:
                            self.state["password_input"] = self.state["password_input"][:-1]
                        elif event.key == pygame.K_RETURN:
                            self.handle_login()
                        elif event.unicode.isprintable() and len(self.state["password_input"]) < 20:
                            self.state["password_input"] += event.unicode
                elif self.state["screen"] == "customer" and self.restaurant_filter_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.restaurant_filter_input = self.restaurant_filter_input[:-1]
                    elif event.unicode.isprintable() and len(self.restaurant_filter_input) < 20:
                        self.restaurant_filter_input += event.unicode

    def render(self):
        try:
            current_time = datetime.now().time()
            day = datetime.now().strftime("%a")
            
            self.screen.fill(Constants.CREAM)
            if self.state["screen"] == "role_selection":
                title = self.font.render("Campus Cravings", True, Constants.CRIMSON)
                self.screen.blit(title, (self.window_width // 2 - title.get_width() // 2, 100))
                for button in self.role_buttons:
                    button.draw(self.screen)
            elif self.state["screen"] == "login_screen":
                title = self.font.render("Login", True, Constants.CRIMSON)
                self.screen.blit(title, (self.window_width // 2 - title.get_width() // 2, 100))
                
                username_label = self.font.render("Username:", True, Constants.CRIMSON)
                self.screen.blit(username_label, (self.window_width // 2 - 250, 200))
                pygame.draw.rect(self.screen, Constants.CREAM, self.username_rect)
                pygame.draw.rect(self.screen, Constants.CRIMSON, self.username_rect, 2 if self.state["active_input"] != "username" else 4)
                username_text = self.font.render(self.state["username_input"], True, Constants.CRIMSON)
                self.screen.blit(username_text, (self.username_rect.x + 5, self.username_rect.y + 5))
                
                password_label = self.font.render("Password:", True, Constants.CRIMSON)
                self.screen.blit(password_label, (self.window_width // 2 - 250, 260))
                pygame.draw.rect(self.screen, Constants.CREAM, self.password_rect)
                pygame.draw.rect(self.screen, Constants.CRIMSON, self.password_rect, 2 if self.state["active_input"] != "password" else 4)
                password_text = self.font.render("*" * len(self.state["password_input"]), True, Constants.CRIMSON)
                self.screen.blit(password_text, (self.password_rect.x + 5, self.password_rect.y + 5))
                
                if self.state["login_error"]:
                    error_text = self.font.render(self.state["login_error"], True, Constants.CRIMSON)
                    self.screen.blit(error_text, (self.window_width // 2 - error_text.get_width() // 2, 380))
                
                self.login_button.draw(self.screen)
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "customer":
                header = self.font.render("Campus Cravings", True, Constants.CRIMSON)
                self.screen.blit(header, (self.window_width // 2 - header.get_width() // 2, 20))
                
                selected_user_text = f"Selected User: {self.state['selected_user'] or 'Unknown'}"
                selected_user_label = self.font.render(selected_user_text, True, Constants.CRIMSON)
                self.screen.blit(selected_user_label, (self.window_width // 2 - selected_user_label.get_width() // 2, 60))
                
                self.screen.blit(self.restaurant_filter_label, (self.window_width // 2 - self.restaurant_filter_label.get_width() // 2, 90))
                pygame.draw.rect(self.screen, Constants.CREAM, self.restaurant_filter_rect)
                pygame.draw.rect(self.screen, Constants.CRIMSON, self.restaurant_filter_rect, 2 if not self.restaurant_filter_active else 4)
                filter_text = self.font.render(self.restaurant_filter_input, True, Constants.CRIMSON)
                self.screen.blit(filter_text, (self.restaurant_filter_rect.x + 5, self.restaurant_filter_rect.y + 5))
                
                self.filtered_restaurants = [
                    r for r in self.restaurant_manager.restaurants
                    if self.restaurant_filter_input.lower() in r["name"].lower()
                ]
                
                y_start = 180
                visible_restaurants = self.filtered_restaurants[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + 7]
                for i, restaurant in enumerate(visible_restaurants):
                    restaurant_text = self.font.render(restaurant["name"], True, Constants.CRIMSON)
                    restaurant_rect = pygame.Rect(self.window_width // 2 - 100, y_start + i * 40, 200, 30)
                    if self.selected_restaurant_index == i + self.state["scroll_offset"]:
                        pygame.draw.rect(self.screen, Constants.CRIMSON, restaurant_rect, 2)
                    self.screen.blit(restaurant_text, (self.window_width // 2 - restaurant_text.get_width() // 2, y_start + i * 40))
                
                self.back_button.draw(self.screen, Constants.BEIGE)
                self.cart_button.draw(self.screen, Constants.GOLD)
                self.recommend_button.draw(self.screen, Constants.GOLD)
            elif self.state["screen"] == "menu_screen":
                if self.state["selected_restaurant"] is None:
                    self.state.update({"screen": "customer", "scroll_offset": 0})
                    return
                restaurant = self.state["selected_restaurant"]
                title = self.font.render(f"{restaurant['name']} Menu", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                self.menu_buttons = [
                    Button(50, 70 + i * 60, self.window_width - 100, 50, f"{item['item']} - ${item['price'] if 'price' in item else list(item['options']['size'].values())[0]}{' (Meal Exchange)' if item['meal_exchange'] else ''}", 
                           lambda i=item: self.state.update({"screen": "option_screen", "option_selection": {"item": i, "restaurant": restaurant["name"], "selections": {}}}), self.font)
                    for i, item in enumerate([i for i in restaurant["menu"] if self.restaurant_manager.is_item_available(i, current_time)])
                ]
                visible_buttons = self.menu_buttons[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + 7]
                for button in visible_buttons:
                    button.draw(self.screen)
                self.cart_button.draw(self.screen)
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "option_screen":
                item = self.state["option_selection"]["item"]
                restaurant = self.state["option_selection"]["restaurant"]
                title = self.font.render(f"Customize {item['item']}", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                self.option_buttons = []
                y_offset = 70
                if "options" in item:
                    if "size" in item["options"]:
                        for size, price in item["options"]["size"].items():
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Size: {size} - ${price}", 
                                                             lambda s=size, p=price: self.state["option_selection"]["selections"].update({"size": s, "price": p}), self.font))
                            y_offset += 60
                    if "toppings" in item["options"]:
                        for topping in item["options"]["toppings"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Topping: {topping}", 
                                                             lambda t=topping: self.state["option_selection"]["selections"].setdefault("toppings", []).append(t) if len(self.state["option_selection"]["selections"].get("toppings", [])) < item["options"]["max_toppings"] else None, self.font))
                            y_offset += 60
                    if "sauce" in item["options"]:
                        for sauce in item["options"]["sauce"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Sauce: {sauce}", 
                                                             lambda s=sauce: self.state["option_selection"]["selections"].update({"sauce": s}), self.font))
                            y_offset += 60
                    if "pasta" in item["options"]:
                        for pasta in item["options"]["pasta"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Pasta: {pasta}", 
                                                             lambda p=pasta: self.state["option_selection"]["selections"].update({"pasta": p}), self.font))
                            y_offset += 60
                    if "wrap" in item["options"]:
                        for wrap in item["options"]["wrap"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Wrap: {wrap}", 
                                                             lambda w=wrap: self.state["option_selection"]["selections"].update({"wrap": w}), self.font))
                            y_offset += 60
                    if "type" in item["options"]:
                        for type_option in item["options"]["type"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Type: {type_option}", 
                                                             lambda t=type_option: self.state["option_selection"]["selections"].update({"type": t}), self.font))
                            y_offset += 60
                    if "entree" in item["options"]:
                        for entree in item["options"]["entree"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Entree: {entree}", 
                                                             lambda e=entree: self.state["option_selection"]["selections"].setdefault("entrees", []).append(e) if len(self.state["option_selection"]["selections"].get("entrees", [])) < item["options"].get("max_entrees", 1) else None, self.font))
                            y_offset += 60
                    if "side" in item["options"]:
                        for side in item["options"]["side"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Side: {side}", 
                                                             lambda s=side: self.state["option_selection"]["selections"].update({"side": s}), self.font))
                            y_offset += 60
                    if "cheese" in item["options"]:
                        for cheese in item["options"]["cheese"]:
                            self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Cheese: {cheese}", 
                                                             lambda c=cheese: self.state["option_selection"]["selections"].update({"cheese": c}), self.font))
                            y_offset += 60
                    if "combo" in item["options"]:
                        self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, f"Combo (+${item['options']['combo']['price']})", 
                                                         lambda: self.state["option_selection"]["selections"].update({"combo": {"side": item["options"]["combo"]["Side"][0], "drink": item["options"]["combo"]["Drink"][0], "price": item["options"]["combo"]["price"]}}), self.font))
                        y_offset += 60
                self.option_buttons.append(Button(50, y_offset, self.window_width - 100, 50, "Add to Cart", 
                                                 lambda: self.cart_manager.add_to_cart(item, restaurant, self.state["option_selection"]["selections"], self.state["option_selection"]["selections"].get("price", item.get("price", 0)) + self.state["option_selection"]["selections"].get("combo", {"price": 0})["price"]) or self.state.update({"screen": "menu_screen", "option_selection": None}), self.font))
                visible_buttons = self.option_buttons[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + 7]
                for i, button in enumerate(visible_buttons):
                    button.rect.y = 70 + i * 60
                    button.text_rect = button.text.get_rect(center=button.rect.center)
                    button.draw(self.screen)
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "cart_screen":
                title = self.font.render("Your Cart", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                total = self.cart_manager.get_total()
                visible_items = max(1, (self.window_height - 200) // 40)
                visible_cart = self.cart_manager.cart[max(0, self.state["scroll_offset"]):self.state["scroll_offset"] + visible_items]
                for i, item in enumerate(visible_cart):
                    selections = ", ".join([f"{k}: {v}" for k, v in item["selections"].items() if k != "price" and not isinstance(v, dict)] + [f"Combo: {item['selections']['combo']['side']}, {item['selections']['combo']['drink']}" if "combo" in item["selections"] else ""])
                    text = self.font.render(f"{item['restaurant']}: {item['item']} {f'({selections})' if selections else ''} - ${item['price']:.2f}{' (Meal Exchange)' if item['meal_exchange'] else ''}", True, Constants.CRIMSON)
                    self.screen.blit(text, (50, 70 + i * 40))
                total_text = self.font.render(f"Total: ${total:.2f}", True, Constants.CRIMSON)
                self.screen.blit(total_text, (50, 70 + len(visible_cart) * 40))
                self.checkout_button.draw(self.screen)
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "confirmation_screen":
                title = self.font.render("Order Confirmation", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                confirmation_text = self.font.render("Order placed successfully!", True, Constants.CRIMSON)
                self.screen.blit(confirmation_text, (50, 70))
                self.back_button.draw(self.screen)
                self.exit_button.draw(self.screen)
            elif self.state["screen"] == "restaurant":
                title = self.font.render("Restaurant View", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                for i, restaurant in enumerate(self.restaurant_manager.restaurants):
                    restaurant_text = self.font.render(restaurant["name"], True, Constants.CRIMSON)
                    self.screen.blit(restaurant_text, (50, 70 + i * 40))
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "driver":
                title = self.font.render("Driver View", True, Constants.CRIMSON)
                self.screen.blit(title, (50, 20))
                self.back_button.draw(self.screen)
            elif self.state["screen"] == "recommendation":
                self.recommendation_interface.render()
            
            pygame.display.flip()
        except pygame.error as e:
            print(f"Rendering error: {e}. Skipping render.")
            return
