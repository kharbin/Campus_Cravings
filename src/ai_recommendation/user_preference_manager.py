class UserPreferenceManager:
    def __init__(self):
        self.preferences = {
            "allergies": [],
            "diet": None,
            "cuisine": None
        }

    def update_preferences(self, new_preferences):
        """
        Update user preferences with new values.
        
        Args:
            new_preferences (dict): New preferences to apply.
        """
        if "allergies" in new_preferences:
            if isinstance(new_preferences["allergies"], list):
                self.preferences["allergies"] = new_preferences["allergies"]
            else:
                raise ValueError("Allergies must be a list")
        
        if "diet" in new_preferences:
            if isinstance(new_preferences["diet"], str) or new_preferences["diet"] is None:
                self.preferences["diet"] = new_preferences["diet"]
            else:
                raise ValueError("Diet must be a string or None")
        
        if "cuisine" in new_preferences:
            if isinstance(new_preferences["cuisine"], str) or new_preferences["cuisine"] is None:
                self.preferences["cuisine"] = new_preferences["cuisine"]
            else:
                raise ValueError("Cuisine must be a string or None")

    def get_preferences(self):
        """Return the current preferences."""
        return self.preferences

    def clear_preferences(self):
        """Reset preferences to default."""
        self.preferences = {
            "allergies": [],
            "diet": None,
            "cuisine": None
        }
