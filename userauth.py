import json
class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password  
        self.role = role# Note: Don't store raw passwords in real apps

    def check_password(self, password):
        return self.password == password
    
    def is_admin(self):
        return self.role == "admin"
    
class UserManager:
    USERS_FILE = "users.json"
    def __init__(self):
        self.users = self.load_users()
    def load_users(self):
        """Reads the user's database from the JSON file."""
        with open(self.USERS_FILE, "r") as json_file:
            users = set()
            users_dictionary = json.load(json_file)
            for user in users_dictionary.keys():
                users.add(User(user, users_dictionary[user]["password"], users_dictionary[user]["role"]))
        return users

    def find_user(self, username):
        """Finds a user by username."""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def add_user(self, username, password, role="user"):
        """Adds a new user to the database."""
        if self.find_user(username):
            print(f"User {username} already exists.")
            return False
        new_user = User(username, password, role)
        self.users.add(new_user)
        self.save_users()
        return True
    
    def save_users(self):
        """Writes the user's database to the JSON file."""
        with open(self.USERS_FILE, "w") as json_file:
            users = {}
            for user in self.users:
                users[user.username] = {
                    "password": user.password,
                    "role": user.role
                }
            json.dump(users, json_file, indent = 4)

    def authenticate(self):
        user_id = input("Please enter your User ID: ")
        password = input("Enter password: ")
        for user in self.users:
            if user.username == user_id and user.password == password:
                return user.is_admin()
        return False

def authenticate_user(func):
    def wrapper(*args, **kwargs):
        users = UserManager()
        if users.authenticate():
            return func(*args, **kwargs)
        else:
            input("Authentication failed!")
    return wrapper

if __name__ == "__main__":
    # Read and print users
    users = UserManager()
    for user in users.users:
        print(user.username, user.password)
        print(user.is_admin())
    new_user = User("kate", "123456", "user")
    print(users.add_user(new_user.username, new_user.password, new_user.role))

