class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged_in = False
    
    def log_in(self):
        self.is_logged_in = True
        print(f"{self.username} is now logged in.")
    
    def log_out(self):
        self.is_logged_in = False
        print(f"{self.username} is now logged out.")
    
    def get_user_info(self):
        return f"Email: {self.username}, Password: {self.password}, Logged In: {self.is_logged_in}"

