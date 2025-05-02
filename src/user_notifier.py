import unittest
import sys
import io
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
from unittest.mock import patch

# ------------------------------- Architecture: Notification System with Rate Limiting and Time Restrictions -------------------------------
# Global dictionary to track driver notification attempts, mapping driver names to a deque of timestamps
# Using defaultdict(deque) for efficient storage and management of timestamp data
call_logs = defaultdict(deque)

# ------------------------------- Resource Management: System Constraints to Prevent Overuse -------------------------------
# Constants defining constraints to manage resource consumption
RATE_LIMIT = 3  # Maximum notifications per driver within the time window to prevent spamming
WINDOW_SECONDS = 10  # Time window (in seconds) for rate limiting to control frequency
ACTIVE_HOURS = (8, 22)  # Allowed notification hours (8 AM to 10 PM) to reduce off-hour resource usage

# ------------------------------- Function: Notify User with Validation, Rate Limiting, and Time Cutoff -------------------------------
def notify_user(order_message, driver_name, driver_confirmed, payment_made, restaurant_approved, now=None):
    """
    Sends a notification to the user about their order, enforcing validation, rate limiting, and time restrictions.
    
    Args:
        order_message (str): Message describing the order.
        driver_name (str): Name of the driver assigned to the order.
        driver_confirmed (bool): Whether the driver has confirmed the order.
        payment_made (bool): Whether payment has been completed.
        restaurant_approved (bool): Whether the restaurant has approved the order.
        now (datetime, optional): Current time for testing; defaults to datetime.now().
    
    Returns:
        str: Notification status message (success or failure with reason).
    """
    # ------------------------------- Architecture: Flexible Time Handling for Testing and Production -------------------------------
    # Allow passing a custom time for testing to avoid mocking; use real time in production
    if now is None:
        now = datetime.now()
    current_hour = now.hour

    # ------------------------------- Boundary: Time-Based Notification Restriction -------------------------------
    # Restrict notifications to active hours (8 AM to 10 PM) to prevent disturbances and conserve resources during off-hours
    if not (ACTIVE_HOURS[0] <= current_hour < ACTIVE_HOURS[1]):
        return "Notification Failed: Outside allowed notification hours."

    # ------------------------------- Security & Resource Management: Rate Limiting to Prevent Abuse -------------------------------
    # Enforce rate limiting per driver to prevent spamming, protecting system resources (CPU, memory, network)
    if driver_name:
        timestamps = call_logs[driver_name]
        # Efficiently remove old timestamps to maintain a sliding window, preventing unbounded memory growth
        while timestamps and (now - timestamps[0]).total_seconds() > WINDOW_SECONDS:
            timestamps.popleft()

        # Check if the number of attempts exceeds the rate limit to avoid resource exhaustion
        if len(timestamps) >= RATE_LIMIT:
            return "Notification Failed: Rate limit exceeded. Try again later."

        # Record the current attempt with O(1) append operation using deque
        timestamps.append(now)

    # ------------------------------- Reliability: Input Validation for Robustness -------------------------------
    # Validate inputs to ensure notifications are only sent for valid orders, reducing unnecessary processing
    if not driver_confirmed:
        return "Notification Failed: Driver has not confirmed the order yet."

    if not payment_made:
        return "Notification Failed: Payment is incomplete."

    if not restaurant_approved:
        return "Notification Failed: Restaurant has not approved the order."

    # ------------------------------- Edge Case: Handling Invalid Inputs -------------------------------
    # Check for empty or None inputs to prevent processing invalid data, conserving resources
    if not order_message or not order_message.strip():
        return "Notification Failed: Order message is empty!"

    if not driver_name or not driver_name.strip():
        return "Notification Failed: Driver name is missing!"

    # ------------------------------- Architecture: Notification Construction -------------------------------
    # Construct and return the success notification message
    notification = f"Notification Sent: {order_message} Your driver is {driver_name}."
    return notification

# ------------------------------- Unit Tests for Notification System -------------------------------
class TestUserNotifier(unittest.TestCase):

    def setUp(self):
        """
        Reset call_logs before each test to ensure a clean state, preventing memory accumulation during testing.
        """
        # ------------------------------- Resource Management: Test Cleanup -------------------------------
        # Clear call_logs to avoid residual data affecting test results or consuming memory
        call_logs.clear()

    # ------------------------------- Reliability Test: Successful Notification -------------------------------
    def test_notify_user_all_valid(self):
        """Test if a notification is successfully sent when all inputs are valid."""
        result = notify_user("Your order is ready!", "Alex", True, True, True)
        self.assertEqual(result, "Notification Sent: Your order is ready! Your driver is Alex.")

    # ------------------------------- Reliability Test: Driver Confirmation Validation -------------------------------
    def test_driver_not_confirmed(self):
        """Test if notification fails when the driver has not confirmed the order."""
        result = notify_user("Your order is ready!", "Alex", False, True, True)
        self.assertEqual(result, "Notification Failed: Driver has not confirmed the order yet.")

    # ------------------------------- Reliability Test: Payment Validation -------------------------------
    def test_payment_not_made(self):
        """Test if notification fails when payment is incomplete."""
        result = notify_user("Your order is ready!", "Alex", True, False, True)
        self.assertEqual(result, "Notification Failed: Payment is incomplete.")

    # ------------------------------- Reliability Test: Restaurant Approval Validation -------------------------------
    def test_restaurant_not_approved(self):
        """Test if notification fails when the restaurant has not approved the order."""
        result = notify_user("Your order is ready!", "Alex", True, True, False)
        self.assertEqual(result, "Notification Failed: Restaurant has not approved the order.")

    # ------------------------------- Edge Case Test: Empty Order Message -------------------------------
    def test_empty_order_message(self):
        """Test if notification fails when the order message is empty, ensuring invalid inputs are rejected."""
        result = notify_user("", "Alex", True, True, True)
        self.assertEqual(result, "Notification Failed: Order message is empty!")

    # ------------------------------- Edge Case Test: None Order Message -------------------------------
    def test_none_order_message(self):
        """Test if notification fails when the order message is None, handling null input cases."""
        result = notify_user(None, "Alex", True, True, True)
        self.assertEqual(result, "Notification Failed: Order message is empty!")

    # ------------------------------- Edge Case Test: Empty Driver Name -------------------------------
    def test_empty_driver_name(self):
        """Test if notification fails when the driver name is empty, preventing invalid notifications."""
        result = notify_user("Your order is ready!", "", True, True, True)
        self.assertEqual(result, "Notification Failed: Driver name is missing!")

    # ------------------------------- Edge Case Test: None Driver Name -------------------------------
    def test_none_driver_name(self):
        """Test if notification fails when the driver name is None, ensuring robust input validation."""
        result = notify_user("Your order is ready!", None, True, True, True)
        self.assertEqual(result, "Notification Failed: Driver name is missing!")

    # ------------------------------- Security & Resource Management Test: Rate Limiting Enforcement -------------------------------
    def test_rate_limiting(self):
        """Test if rate limiting prevents excessive notifications, protecting system resources from abuse."""
        driver = "Jordan"
        for i in range(RATE_LIMIT):
            result = notify_user(f"Order #{i+1}", driver, True, True, True)
            self.assertTrue("Notification Sent" in result)

        # Verify that further attempts are blocked to prevent resource overuse
        result = notify_user("Spam attempt", driver, True, True, True)
        self.assertEqual(result, "Notification Failed: Rate limit exceeded. Try again later.")

    # ------------------------------- Boundary Test: Time Cutoff Restriction -------------------------------
    def test_time_cutoff(self):
        """Test if notification fails outside allowed hours (8 AM to 10 PM), conserving resources during off-hours."""
        fake_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=2)  # 2 AM
        result = notify_user("Late order", "Jordan", True, True, True, now=fake_time)
        self.assertEqual(result, "Notification Failed: Outside allowed notification hours.")

# ------------------------------- Main Section: Simulation and Testing -------------------------------
if __name__ == "__main__":
    # ------------------------------- Architecture: Simulated Notification for Demonstration -------------------------------
    # Simulate a real-world notification scenario to demonstrate system functionality
    order_message = "Your Campus Cravings order is ready!"
    driver_name = "Jordan"
    driver_confirmed = True
    payment_made = True
    restaurant_approved = True

    result = notify_user(order_message, driver_name, driver_confirmed, payment_made, restaurant_approved)
    print("Notify User Output:")
    print(result)

    # ------------------------------- Reliability & Resource Management: Run Unit Tests with Output Logging -------------------------------
    # Custom Tee class to log test output to both console and file, ensuring reliable test result storage
    class Tee(io.TextIOBase):
        def __init__(self, *streams):
            self.streams = streams

        def write(self, data):
            for s in self.streams:
                s.write(data)
                s.flush()

        def flush(self):
            for s in self.streams:
                s.flush()

    # Save test results to a file while displaying on console, managing disk resources efficiently
    with open("test_results.txt", "w") as logfile:
        sys.stdout = Tee(sys.__stdout__, logfile)
        unittest.main(exit=False)

    # Restore standard output to prevent resource conflicts
    sys.stdout = sys.__stdout__
    print("\nTest results have also been saved to 'test_results.txt'.")
