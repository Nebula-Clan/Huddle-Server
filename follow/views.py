from django.shortcuts import render
from authentication.models import User
from .models import UserFollowing
from django.http.response import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from errors.error_repository import get_error_serialized
from user_profile.serializers import PublicProfileSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_follow(request):
    user = request.user
    
    to_follow_username = request.data.get('to_follow', None)
    if to_follow_username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username of to follow user must be sended').data})
    
    to_follow = User.objects.get(username = to_follow_username)
    if to_follow is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with sended username does not exists').data})

    if UserFollowing.objects.filter(user = user, following_user = to_follow).exist():
        return JsonResponse({"error" : get_error_serialized(110).data})

    UserFollowing.objects.create(user = user, following_user = to_follow)

    return JsonResponse({"message" : f"user {to_follow.username} followed by {user.username}"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_unfollow(request):
    user = request.user
    
    to_unfollow_username = request.data.get('to_unfollow', None)
    if to_unfollow_username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username of to unfollow user must be sended').data})
    
    to_unfollow = User.objects.get(username = to_unfollow_username)
    if to_unfollow is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with sended username does not exists').data})

    finded_following = UserFollowing.objects.get(user = user, following_user = to_unfollow)

    if finded_following is None:
        return JsonResponse({"error" : get_error_serialized(111).data})
    
    finded_following.delete()


@api_view(['GET'])
@permission_classes([AllowAny])
def user_followings(request):
    username = request.query_params.get('username', None)
    if username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username is required').data})

    user = User.objects.get(username = username)
    if user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with this username does not exists').data})
    
    user_followings = UserFollowing.objects.filter(user = user.id)
    user_followings_serialized = PublicProfileSerializer(user_followings, many = True)
    return JsonResponse({"user_followings" : user_followings_serialized.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def user_followers(request):
    username = request.query_params.get('username', None)
    if username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username is required').data})

    user = User.objects.get(username = username)
    if user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with this username does not exists').data})
    
    user_followers = UserFollowing.objects.filter(following_user = user.id)
    user_followers_serialized = PublicProfileSerializer(user_followers, many = True)
    return JsonResponse({"user_followings" : user_followers_serialized.data})
