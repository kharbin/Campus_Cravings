# scheduled_orders.py

import time
import threading
from datetime import datetime, timedelta

# In-memory list to store scheduled orders
scheduled_orders = []

# ------------------------------- Order Scheduling Logic -------------------------------

def schedule_order(user, meal, location, scheduled_time):
    """Schedules a food order for future delivery."""
    if scheduled_time <= datetime.now():
        print(f"[ERROR] Cannot schedule order in the past: {scheduled_time}")
        return

    order = {
        "user": user,
        "meal": meal,
        "location": location,
        "scheduled_time": scheduled_time,
        "status": "scheduled"
    }

    scheduled_orders.append(order)
    print(f"[SCHEDULED] {user} scheduled '{meal}' to be delivered at '{location}' on {scheduled_time}.")


def delivery_worker(poll_interval=10):
    """Continuously checks for orders to deliver based on current time."""
    while True:
        now = datetime.now()
        for order in scheduled_orders:
            if order["status"] == "scheduled" and order["scheduled_time"] <= now:
                order["status"] = "delivered"
                print(f"[DELIVERED] {order['user']}'s '{order['meal']}' delivered to '{order['location']}' at {now}.")
        time.sleep(poll_interval)


def start_delivery_thread(poll_interval=10):
    """Starts the background thread to deliver orders on time."""
    thread = threading.Thread(target=lambda: delivery_worker(poll_interval), daemon=True)
    thread.start()
    return thread


# ------------------------------- Example Usage -------------------------------
if __name__ == "__main__":
    # Start the delivery thread
    start_delivery_thread()

    # Example: Schedule Alice's order for 20 seconds in the future
    future_time = datetime.now() + timedelta(seconds=20)
    schedule_order(
        user="Bob",
        meal="Burger",
        location="Bizzell Library",
        scheduled_time=future_time
    )

    # Keep the main thread alive to observe delivery
    time.sleep(40)
