
import string
import random
INFINITY = 1000000000000

def int_try_parse(number, default):
    try:
        number = int(number)
    except:
        number = default
    return number
def random_string(length):
    alphabet = string.ascii_letters
    result = ''
    for i in range(length):
        result += random.choice(alphabet)
    return result