from .models import error
from .serializers import ErrorSerializer


AUTHENTICATION_FAILED = 113
AUTHENTICATION_REQUIRED = 114
PERMISSION_DENIED = 106
OBJECT_NOT_FOUND = 100
MISSING_REQUIRED_FIELDS = 103


errors_list = [
    (100, 'Object you are looking for does not exist in database'),
    (101, 'Wrong username or password'),
    (103, 'Required field(s) is missed'),
    (104, 'Username already is taken'),
    (105, 'User with this email already exists'),
    (106, 'This user is not allowed for this action'),
    (107, 'User already exists in this community'),
    (108, 'Order key parameter only can be \'top\', \'hot\', \'new\''),
    (109, 'Community with this name already exists'),
    (110, 'Same like exists!'),
    (111, 'This user dont follow requested user'),
    (112, 'This user already follow requested user'),
    (113, 'Authenticatio failed!'),
    (114, 'Should authorize first.'),
    (115, 'This user has previously reported the post'),
    (116, 'This post does not exist in this community'),
    (117, 'requested user does not exist in this community'),
    (118, 'Community admin can not remove him/her self')
]

def get_error(code):
    return error.objects.filter(code = code).first()

def get_error_serialized(code, detail = ''):
    return ErrorSerializer(get_error(code), context = {"detail" : detail})

def update_error_table():
    for tp_error in errors_list:
        if error.objects.filter(code = tp_error[0]).exists():
            continue
        new_error = error(code = tp_error[0], message = tp_error[1])
        new_error.save()
