import re

def is_valid_password(password):
    if ' ' in password:
        return False
    return True

def is_valid_username(username):
    after_shake = re.sub("[A-Za-z0-9_]", "", username)
    if after_shake == "":
        return True
    return False