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
    
    to_follow = User.objects.filter(username = to_follow_username).first()
    if to_follow is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with sended username does not exists').data})

    if UserFollowing.objects.filter(user = user, following_user = to_follow).exists():
        return JsonResponse({"error" : get_error_serialized(112).data})

    UserFollowing.objects.create(user = user, following_user = to_follow)

    return JsonResponse({"message" : f"user {to_follow.username} followed by {user.username} successfuly"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def send_unfollow(request):
    user = request.user
    
    to_unfollow_username = request.query_params.get('to_unfollow', None)
    if to_unfollow_username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username of to unfollow user must be sended').data})
    
    to_unfollow = User.objects.filter(username = to_unfollow_username).first()
    if to_unfollow is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with sended username does not exists').data})

    finded_following = UserFollowing.objects.filter(user = user, following_user = to_unfollow).first()

    if finded_following is None:
        return JsonResponse({"error" : get_error_serialized(111).data})
    
    finded_following.delete()

    return JsonResponse({"message" : f"User {to_unfollow_username} unfollowed successfuly"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followings(request):
    viewer = request.user
    username = request.query_params.get('username', None)
    if username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username is required').data})

    user = User.objects.filter(username = username).first()
    if user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with sended username does not exists').data})
    
    user_following_ids = UserFollowing.objects.filter(user = user).values_list('following_user')
    user_followings = [User.objects.get(id = user_id[0]) for user_id in user_following_ids]
    user_followings_serialized = PublicProfileSerializer(user_followings, context = {"viewer_id" : viewer.id}, many = True)
    return JsonResponse({"user_followings" : user_followings_serialized.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followers(request):
    viewer = request.user
    username = request.query_params.get('username', None)
    if username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'Username is required').data})

    user = User.objects.filter(username = username).first()
    if user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User with this username does not exists').data})
    
    user_follower_ids = UserFollowing.objects.filter(following_user = user).values_list('user')
    print(user_follower_ids)
    user_followers = [User.objects.get(id = user_id[0]) for user_id in user_follower_ids]
    user_followers_serialized = PublicProfileSerializer(user_followers, context = {"viewer_id" : viewer.id}, many = True)
    return JsonResponse({"user_followers" : user_followers_serialized.data})
