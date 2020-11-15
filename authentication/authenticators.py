from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
import jwt
from django.conf import settings
class JWTAuthenticator(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        authorized_header = request.headers.get('Authorization')
        if authorized_header is None:
            return None
        try:
            access_token = authorized_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access token expired")
        except IndexError:
            raise  exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        user = User.objects.filter(id=payload['user_id']).first()
        if(user is None):
            raise exceptions.AuthenticationFailed("user not found")
        return user, access_token

class SimpleAuthenticator(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        authorized_header = request.headers.get('Authorization')
        access_token = ''
        if authorized_header is None:
            return None
        try:
            access_token = authorized_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload['user_id']).first()
        except:
            user = AnonymousUser()
        return user, access_token