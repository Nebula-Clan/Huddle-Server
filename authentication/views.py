from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from .serializers import UserSerializer
from .utils import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
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
   
    if not(user.password == password):
        raise exceptions.AuthenticationFailed("Wrong password!")
    
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return JsonResponse({"user" : serialized_user, "acess_token": access_token, "refresh_token": refresh_token})

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
