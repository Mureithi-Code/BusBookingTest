import re

class Validators:
    @staticmethod
    def is_valid_email(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def is_strong_password(password):
        return len(password) >= 8 and any(char.isdigit() for char in password)

    @staticmethod
    def is_positive_integer(value):
        return isinstance(value, int) and value > 0
