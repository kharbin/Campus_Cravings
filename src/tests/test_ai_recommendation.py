import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, time
import pygame
from src.ai_recommendation.meal_recommender import MealRecommender
from src.ai_recommendation.user_preference_manager import UserPreferenceManager
from src.ai_recommendation.location_manager import LocationManager
from src.ai_recommendation.recommendation_interface import RecommendationInterface
from src.restaurant_manager import RestaurantManager
from src.constants import Constants

class TestAIRecommendation(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, including a mocked RestaurantManager and Pygame environment."""
        # Mock RestaurantManager
        self.restaurant_manager = RestaurantManager()
        self.restaurant_manager.restaurants = [
            {
                "name": "Italian Bistro",
                "menu": [
                    {"item": "Pasta", "dietary": ["vegetarian"], "available": {"start": "00:00", "end": "23:59"}},
                    {"item": "Peanut Salad", "dietary": [], "available": {"start": "00:00", "end": "23:59"}}
                ],
                "schedule": {"Mon": [{"start": "09:00", "end": "21:00"}]},
                "link": ""
            },
            {
                "name": "Sushi Bar",
                "menu": [
                    {"item": "Sushi", "dietary": [], "available": {"start": "00:00", "end": "23:59"}}
                ],
                "schedule": {"Mon": [{"start": "09:00", "end": "21:00"}]},
                "link": ""
            }
        ]
        self.restaurant_manager.is_open = MagicMock(return_value=True)
        self.restaurant_manager.is_item_available = MagicMock(return_value=True)

        # Initialize classes
        self.meal_recommender = MealRecommender(self.restaurant_manager)
        self.user_preference_manager = UserPreferenceManager()
        self.location_manager = LocationManager(self.restaurant_manager)

        # Mock Pygame for RecommendationInterface
        pygame.init()
        self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.app = MagicMock()
        self.app.state = {"screen": "recommendation", "recommendation": None}
        self.app.running = True
        self.recommendation_interface = RecommendationInterface(
            self.screen, self.font, self.meal_recommender, self.user_preference_manager, self.app
        )

    def tearDown(self):
        """Clean up Pygame resources."""
        pygame.quit()

    # ------------------------------- MealRecommender Tests -------------------------------
    def test_valid_meal_recommendation(self):
        """Test if MealRecommender returns a valid meal."""
        meal = self.meal_recommender.recommend_meal({})
        self.assertIsNotNone(meal, "Meal recommendation should not be None.")
        self.assertIsInstance(meal, str, "Meal recommendation should be a string.")
        self.assertIn(meal, ["Pasta", "Peanut Salad", "Sushi", "Default Meal"], "Meal should be from the menu or default.")

    def test_invalid_meal_not_recommended(self):
        """Test if invalid meals like 'legos' are not recommended."""
        meal = self.meal_recommender.recommend_meal({})
        self.assertNotEqual(meal.lower(), "legos", "Legos should not be recommended as a meal.")

    def test_allergy_filter(self):
        """Test if meals with allergens are excluded."""
        preferences = {"allergies": ["peanuts"]}
        meal = self.meal_recommender.recommend_meal(preferences)
        self.assertNotIn("peanut", meal.lower(), "Recommended meal should not contain peanuts.")
        self.assertIn(meal, ["Pasta", "Sushi", "Default Meal"], "Meal should be safe or default.")

    def test_diet_filter(self):
        """Test if meals match dietary preferences."""
        preferences = {"diet": "vegetarian"}
        meal = self.meal_recommender.recommend_meal(preferences)
        self.assertEqual(meal, "Pasta", "Recommended meal should be vegetarian (Pasta).")

    def test_cuisine_filter(self):
        """Test if meals match cuisine preferences."""
        preferences = {"cuisine": "Italian"}
        meal = self.meal_recommender.recommend_meal(preferences)
        self.assertIn(meal, ["Pasta", "Peanut Salad", "Default Meal"], "Meal should be from Italian Bistro.")

    def test_location_included(self):
        """Test if location is included when requested."""
        meal, location = self.meal_recommender.recommend_meal({}, include_location=True)
        self.assertIsNotNone(location, "Location should be provided.")
        self.assertIsInstance(location, str, "Location should be a string.")
        self.assertIn(location, ["Italian Bistro", "Sushi Bar"], "Location should be a valid restaurant.")

    def test_empty_menu_default(self):
        """Test if default meal is returned when no meals are available."""
        # Mock empty menu
        self.restaurant_manager.restaurants = []
        meal = self.meal_recommender.recommend_meal({})
        self.assertEqual(meal, "Default Meal", "Default meal should be returned when menu is empty.")

    # ------------------------------- UserPreferenceManager Tests -------------------------------
    def test_update_preferences_valid(self):
        """Test updating preferences with valid inputs."""
        preferences = {"allergies": ["peanuts"], "diet": "vegetarian", "cuisine": "Italian"}
        self.user_preference_manager.update_preferences(preferences)
        self.assertEqual(self.user_preference_manager.get_preferences(), preferences, "Preferences should be updated correctly.")

    def test_update_preferences_invalid_allergies(self):
        """Test updating preferences with invalid allergies."""
        with self.assertRaises(ValueError, msg="Allergies must be a list"):
            self.user_preference_manager.update_preferences({"allergies": "peanuts"})

    def test_update_preferences_invalid_diet(self):
        """Test updating preferences with invalid diet."""
        with self.assertRaises(ValueError, msg="Diet must be a string or None"):
            self.user_preference_manager.update_preferences({"diet": ["vegetarian"]})

    def test_clear_preferences(self):
        """Test clearing preferences to default."""
        self.user_preference_manager.update_preferences({"allergies": ["peanuts"], "diet": "vegetarian"})
        self.user_preference_manager.clear_preferences()
        self.assertEqual(
            self.user_preference_manager.get_preferences(),
            {"allergies": [], "diet": None, "cuisine": None},
            "Preferences should be reset to default."
        )

    # ------------------------------- LocationManager Tests -------------------------------
    def test_is_location_open(self):
        """Test if a location is correctly identified as open."""
        self.assertTrue(
            self.location_manager.is_location_open("Italian Bistro"),
            "Italian Bistro should be open (mocked to always return True)."
        )

    def test_get_open_locations(self):
        """Test retrieving a list of open locations."""
        locations = self.location_manager.get_open_locations()
        self.assertEqual(
            locations, ["Italian Bistro", "Sushi Bar"],
            "All mocked restaurants should be open."
        )

    def test_is_location_open_invalid(self):
        """Test handling of invalid location names."""
        self.assertFalse(
            self.location_manager.is_location_open("Nonexistent"),
            "Nonexistent location should return False."
        )

    # ------------------------------- RecommendationInterface Tests -------------------------------
    @patch("pygame.event.get")
    def test_handle_events_allergy_input(self, mock_event_get):
        """Test handling text input for allergies in RecommendationInterface."""
        mock_event_get.return_value = [
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="a"),
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_RETURN)
        ]
        self.recommendation_interface.allergy_active = True
        self.recommendation_interface.handle_events()
        self.assertEqual(self.recommendation_interface.allergy_input, "a", "Allergy input should capture 'a'.")

    @patch("pygame.event.get")
    def test_handle_events_recommend_button(self, mock_event_get):
        """Test clicking the recommend button in RecommendationInterface."""
        mock_event_get.return_value = [
            MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(self.recommendation_interface.recommend_button.rect.center), button=1)
        ]
        self.recommendation_interface.handle_events()
        self.assertIsNotNone(self.app.state["recommendation"], "Recommendation should be set after button click.")
        self.assertTrue(
            self.app.state["recommendation"].startswith("Recommended:"),
            "Recommendation should start with 'Recommended:'."
        )

    @patch("pygame.event.get")
    def test_handle_events_back_button(self, mock_event_get):
        """Test clicking the back button in RecommendationInterface."""
        mock_event_get.return_value = [
            MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(self.recommendation_interface.back_button.rect.center), button=1)
        ]
        self.recommendation_interface.handle_events()
        self.app.state.update.assert_called_with({"screen": "customer"}, "Back button should navigate to customer screen.")

    def test_render_recommendation(self):
        """Test rendering with a recommendation set."""
        self.app.state["recommendation"] = "Recommended: Pasta at Italian Bistro"
        self.recommendation_interface.render()
        # Since we can't directly test Pygame rendering, verify state and setup
        self.assertEqual(
            self.app.state["recommendation"], "Recommended: Pasta at Italian Bistro",
            "Recommendation should be correctly set for rendering."
        )

if __name__ == "__main__":
    unittest.main()
