from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from .serializers import UserSerializer
from .utils import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from .validators import *

# Create your views here.

@api_view(['GET'])
def login_view(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    user2 = UserSerializer(data=request.data)
    
    if(user2.is_valid()):
        user2 = user2.save()
        user2.set_password(user2.password)

    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed("username password required!")
    user = User.objects.filter(username= username).first()
    if user is None:
        raise exceptions.AuthenticationFailed("User not found!")
   
    if not(user.password == password):
        raise exceptions.AuthenticationFailed("Wrong password!")
    
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return JsonResponse({"user" : serialized_user, "acess_token": access_token, "refresh_token": refresh_token})


def register_view(request):
    if request.method == 'POST':
    
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        to_create_user = User(first_name = first_name, last_name = last_name, username = username, email =  email)
        to_create_user.set_password(password1)
        serialized_user = UserSerializer(to_create_user).data

        ALLOW_SHORT_PASSWORD = False
        ALLOW_SHORT_USERNAME = False
        MPL = 8 # Minimum password length
        MUL = 5 # Minimum username length

        User = get_user_model()
        
        if first_name == "" or last_name == "" or username == "" or email == "" or password1 == "":
            return JsonResponse({"user" : serialized_user, "message" : "All fields are required"})

        elif password1 != password2:
            return JsonResponse({"user" : serialized_user, "message" : "Passwords are not same"})
        
        elif (ALLOW_SHORT_PASSWORD) and (len(password1) < MPL):
            return JsonResponse({"user" : serialized_user, "message" : f"Password must have at least {MPL} characters"})
        
        elif (ALLOW_SHORT_USERNAME) and (len(username) < MUL):
            return JsonResponse({"user" : serialized_user, "message" : f"Username must have at least {MUL} characters"})
        
        elif not is_valid_password(password1):
            return JsonResponse({"user" : serialized_user, "message" : "Password can only contains alphabets, numbers"})
        
        elif not is_valid_username(username):
            return JsonResponse({"user" : serialized_user, "message" : "Username can only contains alphabets, numbers, _"})
        
        elif User.objects.filter(username = username).exists():
            return JsonResponse({"user" : serialized_user, "message" : "Username already is taken"})
        
        elif User.objects.filter(email = email).exists():
            return JsonResponse({"user" : serialized_user, "message" : "User with email already exists"})
        
        else:
            to_create_user.save()
            return JsonResponse({"user" : serialized_user, "message" : "User created successfuly"})
    else:
        pass
        # return render

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def something(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return JsonResponse({"user" : serialized_user})


@api_view(['GET'])
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
