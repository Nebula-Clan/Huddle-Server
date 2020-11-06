from .models import error

errors_list = [
    (100, 'Object you are looking for does not exist in database'),
    (101, 'Wrong username or password'),
    (103, 'Required field(s) is missed'),
    (104, 'Username already is taken'),
    (105, 'User with this email already exists')
]

def get_error(code):
    return error.objects.filter(code = code).first()

def update_error_table():
    for tp_error in errors_list:
        if error.objects.filter(code = tp_error[0]).exists():
            continue
        new_error = error(code = tp_error[0], message = tp_error[1])
        new_error.save()
