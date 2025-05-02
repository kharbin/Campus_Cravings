import hashlib


class UserManager:
    def __init__(self):
        # Initialize with a simple list of users for demonstration
        # In a real app, this could be loaded from a file or database
        self.users = [
            {"username": "customer1", "password": "pass123"},
            {"username": "restaurant1", "password": "pass456"},
            {"username": "driver1", "password": "pass789"}
        ]

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_login(self, username, password):
        # Check if the username and password match any user in the list
        for user in self.users:
            if (user["username"] == username
            and self.hash_password(user["password"]) == self.hash_password(password)):
                return True
        return False
