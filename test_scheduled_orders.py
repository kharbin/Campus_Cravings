# test_scheduled_orders.py

import unittest
from datetime import datetime, timedelta
from scheduled_orders import schedule_order, scheduled_orders, start_delivery_thread

import time

class TestScheduledOrders(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start delivery thread with faster checking (every 1 second)
        start_delivery_thread(poll_interval=1)

    def setUp(self):
        # Clear scheduled orders before each test
        scheduled_orders.clear()

    def test_order_is_scheduled_properly(self):
        """Test that a future order is added to the schedule list."""
        future_time = datetime.now() + timedelta(seconds=5)
        schedule_order("test_user", "Pasta", "Library", future_time)
        self.assertEqual(len(scheduled_orders), 1)
        self.assertEqual(scheduled_orders[0]['status'], 'scheduled')

    def test_order_delivers_after_time_passes(self):
        """Test that a scheduled order is marked as delivered after the scheduled time."""
        future_time = datetime.now() + timedelta(seconds=3)
        schedule_order("test_user", "Salad", "Dorm", future_time)

        time.sleep(5)  # Wait long enough for delivery_worker to process

        self.assertEqual(scheduled_orders[0]['status'], 'delivered')

    def test_order_not_scheduled_in_past(self):
        """Test that scheduling an order in the past is rejected."""
        past_time = datetime.now() - timedelta(minutes=1)
        schedule_order("test_user", "Burger", "Gym", past_time)

        self.assertEqual(len(scheduled_orders), 0)


if __name__ == '__main__':
    unittest.main()
