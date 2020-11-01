from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
from .utils import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from .validators import *

# Create your views here.
@api_view(['POST'])
def login_view(request):
    User = get_user_model()
    username = request.POST['username']
    password = request.POST['password']
    
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed("username password required!")
    user = User.objects.filter(username= username).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found!")
   
    if not User.check_password(user, password):
        raise exceptions.AuthenticationFailed("Wrong password!")
    
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return JsonResponse({"access_token": access_token, "refresh_token": refresh_token})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
    
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()

        if User.objects.all().count() != 0:
            last_id = User.objects.last().id
        else:
            last_id = 0
        to_create_id = last_id + 1
        to_create_user = User(id = to_create_id, first_name = first_name, last_name = last_name, username = username, email =  email)
        to_create_user.set_password(password)
        serialized_user = UserSerializer(to_create_user).data

        ALLOW_SHORT_PASSWORD = False
        ALLOW_SHORT_USERNAME = False
        MPL = 8 # Minimum password length
        MUL = 5 # Minimum username length

        if first_name == "" or last_name == "" or username == "" or email == "" or password == "":
            return JsonResponse({"user" : serialized_user, "message" : "All fields are required"})

        elif User.objects.filter(username = username).exists():
            return JsonResponse({"user" : serialized_user, "message" : "Username already is taken"})
        
        elif User.objects.filter(email = email).exists():
            return JsonResponse({"user" : serialized_user, "message" : "User with email already exists"})
        
        else:
            to_create_user.save()
            return JsonResponse({"user" : serialized_user, "message" : "User created successfuly"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return JsonResponse({"user" : serialized_user})


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    import jwt
    User = get_user_model()

    refresh_token = request.data.get('refresh_token')
    if(refresh_token is None):
        return exceptions.AuthenticationFailed("refresh token not found.")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return exceptions.AuthenticationFailed("refresh token expired.")
    except jwt.DecodeError:
        return exceptions.AuthenticationFailed("invalid token.")
    user = User.objects.filter(id= payload['user_id']).first()
    if(user is None):
        return exceptions.AuthenticationFailed("user not found!")
    access_token = generate_access_token(user)
    return JsonResponse({"access_token" : access_token, "refresh_token": refresh_token})
