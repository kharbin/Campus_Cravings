from datetime import datetime
from ..restaurant_manager import RestaurantManager

class LocationManager:
    def __init__(self, restaurant_manager):
        self.restaurant_manager = restaurant_manager

    def is_location_open(self, location_name):
        """
        Check if a location is open based on its schedule.
        
        Args:
            location_name (str): Name of the location (restaurant).
        
        Returns:
            bool: True if open, False otherwise.
        """
        current_time = datetime.now().time()
        day = datetime.now().strftime("%a")
        
        for restaurant in self.restaurant_manager.restaurants:
            if restaurant["name"].lower() == location_name.lower():
                return self.restaurant_manager.is_open(restaurant["schedule"], day, current_time)
        return False

    def get_open_locations(self):
        """
        Return a list of open restaurant names.
        
        Returns:
            list: Names of open restaurants.
        """
        current_time = datetime.now().time()
        day = datetime.now().strftime("%a")
        return [
            restaurant["name"]
            for restaurant in self.restaurant_manager.restaurants
            if self.restaurant_manager.is_open(restaurant["schedule"], day, current_time)
        ]
