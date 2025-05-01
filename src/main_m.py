import unittest

# Function to recommend a meal based on user preferences
def aiMealRecommend(user_preferences={}, include_location=False):
    # Define the available menu options
    menu = ["Pasta", "Salad", "Burger", "Sushi"]
    
    # ------------------------------- Architecture: Handling User Preferences -------------------------------
    # Check if the user has specified any allergies and filter the menu accordingly
    if "allergies" in user_preferences:
        # Remove meals that contain any allergens specified in the user preferences
        menu = [meal for meal in menu if not any(allergen in meal.lower() for allergen in user_preferences["allergies"])]
    
    # Select the first meal from the filtered menu or set a default meal if no meals are available
    meal = menu[0] if menu else "Default Meal"
    
    # If location is requested, set the location to "Food Court"
    location = "Food Court" if include_location else None
    
    # Return the meal and location if include_location is True, otherwise just the meal
    return (meal, location) if include_location else meal

# Helper function to check if the location is open
def is_location_open(location):
    # For the purpose of this example, we assume the location is always open
    return True

# Unit test class to test the aiMealRecommend function
class TestaiMealRecommend(unittest.TestCase):
    
    # ------------------------------- Reliability Test: Ensure System Returns a Meal -------------------------------
    def test_valid_meal_recommendation(self):
        """Test if a meal is successfully recommended."""
        # Call the function with no user preferences (empty dictionary)
        meal = aiMealRecommend(user_preferences={})
        
        # Ensure that the meal recommendation is not None
        self.assertIsNotNone(meal, "Meal recommendation should not be None.")
        
        # Ensure that the meal recommendation is a string (a meal name)
        self.assertIsInstance(meal, str, "Meal recommendation should be a string.")
    
    # ------------------------------- Reliability Test: Validate Invalid Meals Are Not Recommended -------------------------------
    def test_invalid_meal_recommendation(self):
        """Test if 'legos' are not recommended as a meal."""
        # Call the function with no user preferences
        meal = aiMealRecommend(user_preferences={})
        
        # Ensure that the recommended meal is not 'legos'
        self.assertNotEqual(meal.lower(), "legos", "Legos should not be recommended as a meal.")
    
    # ------------------------------- Architecture Test: Validate Location Information is Included -------------------------------
    def test_boundary_location_availability(self):
        """Test if the meal recommendation includes an available location within operating hours."""
        # Call the function with the 'include_location' flag set to True
        meal, location = aiMealRecommend(user_preferences={}, include_location=True)
        
        # Ensure that the location is provided
        self.assertIsNotNone(location, "Location should be provided for meal recommendation.")
        
        # Ensure that the location is a string
        self.assertIsInstance(location, str, "Location should be a string.")
        
        # Ensure that the location is open (we assume it's always open in this example)
        self.assertTrue(is_location_open(location), "Location should be open during recommended time.")
    
    # ------------------------------- Reliability Test: Ensure Allergens Are Excluded From Meal -------------------------------
    def test_edge_case_allergy_in_meal(self):
        """Test if the recommendation avoids meals containing allergens listed in user preferences."""
        # Define user preferences with an allergy to peanuts
        user_preferences = {"allergies": ["peanuts"]}
        
        # Call the function with the specified allergies
        meal = aiMealRecommend(user_preferences=user_preferences)
        
        # Ensure that the recommended meal does not contain peanuts
        self.assertNotIn("peanuts", meal.lower(), "Recommended meal should not contain allergens.")

# ------------------------------- Security: Role-Based Access Control (RBAC) -------------------------------
# Phase 1: Define roles and their allowed actions
# A dictionary that maps roles to the list of actions they are allowed to perform
ROLES = {
    "admin": ["read", "write", "delete"],  # Admin can perform all actions
    "user": ["read", "write"],             # User can read and write
    "guest": ["read"]                      # Guest can only read
}

# Phase 2: Assign roles to users
# A dictionary that maps each user to their assigned role
users = {
    "alice": {"role": "admin"},  # Alice is an admin
    "bob": {"role": "user"},     # Bob is a user
    "carol": {"role": "guest"}   # Carol is a guest
}

# Phase 3: Check role before performing an action
# This function checks if the user has permission to perform the requested action
def can_perform_action(user, action):
    # Retrieve the role of the user
    role = user.get("role")
    # Check if the action is allowed for the user's role
    return action in ROLES.get(role, [])

# Phase 4: Attempt action with logging if denied
# This function simulates an action on a file and logs whether the user is allowed or not
def access_file(username, action):
    # Retrieve the user information from the 'users' dictionary
    user = users.get(username)
    # Check if the user exists and if they have permission to perform the action
    if user and can_perform_action(user, action):
        print(f"{username} performed '{action}' on the file.")  # Log success
    else:
        # Log access denial with a clear message
        print(f"[ACCESS DENIED] {username} attempted '{action}' without permission.")

# ------------------------------- Running the Tests -------------------------------
# Run the test cases when the script is executed directly
if __name__ == '__main__':
    unittest.main()
