import unittest
from datetime import datetime, time
from src.restaurant_manager import RestaurantManager

class TestRestaurantManager(unittest.TestCase):

    def setUp(self):
        """Setup for each test"""
        self.manager = RestaurantManager()

    def test_is_open_open_restaurant(self):
        """Test is_open method when restaurant is open"""
        # Test for 'Basic Knead' on Monday at 2pm (should be open from 1pm-12am)
        current_time = time(14, 0)  # 2:00 PM
        result = self.manager.is_open(self.manager.restaurants[0]['schedule'], "Mon", current_time)
        self.assertTrue(result)

    def test_is_open_closed_restaurant(self):
        """Test is_open method when restaurant is closed"""
        # Test for 'Cafe 201' on Sunday (should be closed)
        current_time = time(10, 0)  # 10:00 AM
        result = self.manager.is_open(self.manager.restaurants[1]['schedule'], "Sun", current_time)
        self.assertFalse(result)

    def test_is_open_invalid_time(self):
        """Test is_open with an invalid time format"""
        # Invalid time should still return False, as it doesn't match any open period
        current_time = time(4, 0)  # 4:00 AM, outside any valid time for 'Basic Knead'
        result = self.manager.is_open(self.manager.restaurants[0]['schedule'], "Mon", current_time)
        self.assertFalse(result)

    def test_is_item_available(self):
        """Test is_item_available with available time ranges"""
        # Testing 'Biscuits & Gravy (1)' at 9:00 AM (should be available only from 7:45 AM - 10:45 AM)
        item = self.manager.restaurants[1]['menu'][12]  # 'Biscuits & Gravy (1)'
        current_time = time(9, 0)  # 9:00 AM
        result = self.manager.is_item_available(item, current_time)
        self.assertTrue(result)

    def test_is_item_not_available(self):
        """Test is_item_available when item is out of time range"""
        # Testing 'Biscuits & Gravy (1)' at 11:00 AM (should be unavailable)
        item = self.manager.restaurants[1]['menu'][12]  # 'Biscuits & Gravy (1)'
        current_time = time(11, 0)  # 11:00 AM
        result = self.manager.is_item_available(item, current_time)
        self.assertFalse(result)

    def test_is_item_without_availability(self):
        """Test is_item_available for items that don't have a specific availability time"""
        # Testing a regular item that doesn't have availability restrictions
        item = self.manager.restaurants[0]['menu'][0]  # 'Build Your Own Pizza'
        current_time = time(9, 0)  # 9:00 AM
        result = self.manager.is_item_available(item, current_time)
        self.assertTrue(result)

    def test_filter_restaurants_no_filter(self):
        """Test filter_restaurants without meal exchange filter"""
        result = self.manager.filter_restaurants(False)
        self.assertEqual(len(result), 5)  # There are 5 restaurants

    def test_filter_restaurants_with_meal_exchange(self):
        """Test filter_restaurants with meal exchange filter"""
        result = self.manager.filter_restaurants(True)
        self.assertEqual(len(result), 5)  # Should return all restaurants with meal exchange available

    def test_is_open_edge_case(self):
        """Test edge case with exactly the opening time"""
        current_time = time(13, 0)  # Exactly at 1:00 PM for 'Basic Knead'
        result = self.manager.is_open(self.manager.restaurants[0]['schedule'], "Mon", current_time)
        self.assertTrue(result)

    def test_is_open_edge_case_end_time(self):
        """Test edge case with exactly the closing time"""
        current_time = time(0, 0)  # Exactly at midnight (12:00 AM) for 'Basic Knead'
        result = self.manager.is_open(self.manager.restaurants[0]['schedule'], "Mon", current_time)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
