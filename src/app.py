import pygame
from .screen_manager import ScreenManager
from .restaurant_manager import RestaurantManager
from .cart_manager import CartManager
from .user_manager import UserManager
from .ai_recommendation.meal_recommender import MealRecommender
from .ai_recommendation.user_preference_manager import UserPreferenceManager
from .ai_recommendation.location_manager import LocationManager
from .constants import Constants

class App:
    def __init__(self):
        self.state = {
            "screen": "role_selection",
            "selected_restaurant": None,
            "scroll_offset": 0,
            "option_selection": None,
            "username_input": "",
            "password_input": "",
            "login_error": "",
            "active_input": None,
            "selected_user": None,
            "recommendation": None
        }
        self.running = True

    def setup(self):
        print("Setting up Pygame...")
        pygame.init()
        print("Pygame initialized.")
        pygame.display.set_caption("Campus Cravings")
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
        print("Display mode set.")
        self.screen.fill(Constants.CREAM)
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.restaurant_manager = RestaurantManager()
        self.cart_manager = CartManager()
        self.users = UserManager()
        self.user_preference_manager = UserPreferenceManager()
        self.meal_recommender = MealRecommender(self.restaurant_manager)
        self.location_manager = LocationManager(self.restaurant_manager)
        self.screen_manager = ScreenManager(
            self.screen, self.font, self.restaurant_manager, self.cart_manager,
            self.users, self, self.meal_recommender, self.user_preference_manager
        )
        print("Setup complete.")

    def run(self):
        self.setup()
        print("Starting main loop...")
        while self.running:
            print("Handling events...")
            self.screen_manager.handle_events()
            if not self.running:
                print("Running flag set to False, breaking loop.")
                break
            print("Rendering...")
            self.screen_manager.render()
            self.clock.tick(Constants.FPS)
        print("Main loop exited, quitting Pygame...")
        pygame.quit()
        print("Pygame quit.")
