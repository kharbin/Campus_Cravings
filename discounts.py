from datetime import datetime

# Discount data: code -> (expiration_date, allowed_roles, discount_amount)
discounts = {
    "STUDENT10": (datetime(2025, 6, 1), ["student"], 10.00),  # $10 off
    "WELCOME5": (datetime(2025, 12, 31), ["student", "faculty"], 5.00),  # $5 off
}

# Users and roles
users = {
    "alice": {"role": "student"},
    "bob": {"role": "faculty"},
    "carol": {"role": "guest"},
}

#Checks Experation Date
def is_discount_valid(code, current_date):
    if code in discounts:
        expiration_date, _, _ = discounts[code]
        return current_date <= expiration_date
    return False

#Verifies User is eligible for selected Discount
def is_user_eligible_for_discount(username, code):
    user = users.get(username)
    if not user or code not in discounts:
        return False
    _, allowed_roles, _ = discounts[code]
    return user["role"] in allowed_roles

#Applies Discount to total
def apply_discount(username, code, current_date):
    return is_discount_valid(code, current_date) and is_user_eligible_for_discount(username, code)

#Ensures total never drops below zero (due to a discount being applied)
def calculate_discounted_total(total, discount_code, current_date, username):
    if apply_discount(username, discount_code, current_date):
        _, _, discount_amount = discounts[discount_code]
        return max(total - discount_amount, 0.0)
    return total

