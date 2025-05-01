import random
from datetime import datetime
from ..restaurant_manager import RestaurantManager

class MealRecommender:
    def __init__(self, restaurant_manager):
        self.restaurant_manager = restaurant_manager

    def recommend_meal(self, user_preferences=None, include_location=False):
        """
        Recommend a meal based on user preferences and optionally include a location.
        
        Args:
            user_preferences (dict): User preferences (e.g., {"allergies": ["peanuts"], "diet": "vegetarian"}).
            include_location (bool): Whether to include a location in the recommendation.
        
        Returns:
            tuple or str: (meal, location) if include_location is True, else meal name.
        """
        user_preferences = user_preferences or {}
        # Get all available menu items from restaurants
        menu_items = self._get_available_menu_items(user_preferences)
        
        # Filter items based on preferences
        filtered_items = self._filter_menu_items(menu_items, user_preferences)
        
        # Select a random item (or use advanced logic in the future)
        selected_item = random.choice(filtered_items) if filtered_items else {"item": "Default Meal", "restaurant": None}
        meal = selected_item["item"]
        
        # Handle location if requested
        location = None
        if include_location and selected_item["restaurant"]:
            location = selected_item["restaurant"]["name"]
        
        return (meal, location) if include_location else meal

    def _get_available_menu_items(self, preferences):
        """Retrieve all menu items from open restaurants."""
        current_time = datetime.now().time()
        day = datetime.now().strftime("%a")
        items = []
        
        for restaurant in self.restaurant_manager.restaurants:
            if self.restaurant_manager.is_open(restaurant["schedule"], day, current_time):
                for item in restaurant["menu"]:
                    if self.restaurant_manager.is_item_available(item, current_time):
                        items.append({"item": item["item"], "restaurant": restaurant, "details": item})
        return items

    def _filter_menu_items(self, menu_items, preferences):
        """Filter menu items based on user preferences."""
        filtered = menu_items
        
        # Filter by allergies
        if "allergies" in preferences:
            filtered = [
                item for item in filtered
                if not any(allergen.lower() in item["item"].lower() for allergen in preferences["allergies"])
            ]
        
        # Filter by diet (e.g., vegetarian, vegan)
        if "diet" in preferences:
            filtered = [
                item for item in filtered
                if preferences["diet"].lower() in item["details"].get("dietary", [])
            ]
        
        # Filter by cuisine (e.g., Italian, Asian)
        if "cuisine" in preferences:
            filtered = [
                item for item in filtered
                if preferences["cuisine"].lower() in item["restaurant"]["name"].lower()
            ]
        
        return filtered
