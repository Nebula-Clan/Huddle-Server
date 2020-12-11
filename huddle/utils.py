

INFINITY = 1000000000000

def int_try_parse(number, default):
    try:
        number = int(number)
    except:
        number = default
    return number