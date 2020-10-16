import re

def is_valid_password(password):
    after_shake = re.sub("[A-Za-z0-9]", "", password)
    if after_shake == "":
        return True
    return False

def is_valid_username(username):
    after_shake = re.sub("[A-Za-z0-9_]", "", username)
    if after_shake == "":
        return True
    return False