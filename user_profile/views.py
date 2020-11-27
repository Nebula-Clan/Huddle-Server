from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from http import HTTPStatus
from authentication.models import User
from posts.models import Post
from .serializers import PublicProfileSerializer
from likes.models import PostLike, CommentLike
from comment.serializers import UserCommentSerializer
from errors.error_repository import get_error_serialized, get_error
from errors.serializers import ErrorSerializer
@api_view(['GET'])
def get_public_profile(request):
    username = request.query_params.get('username', None)
    if(username is None):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)

    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse(get_error_serialized(100, "User not found!").data, status=HTTPStatus.NOT_FOUND)
    public_profile = PublicProfileSerializer(user)
    data = public_profile.data
    data['follower'] = "5"
    data['follower'] = "10"
    data['nickname'] = user.first_name + ' ' + user.last_name
    user_posts = Post.objects.filter(author=user.id)
    if(user_posts is not None):
        data['posts_count'] = str(len(list(user_posts)))
    else:
        data['posts_count'] = "0"
    post_likes = list(PostLike.objects.filter(user=user.id))
    comment_likes = list(CommentLike.objects.filter(user=user.id))
    data['likes_count'] = len(post_likes) + len(comment_likes)
    comment_serializer = UserCommentSerializer(user)
    if(comment_serializer is not None):
        data['comments_count'] = str(len(comment_serializer.get_post_replies(user)) + len(comment_serializer.get_comment_replies(user)))
    else:
        data['comments_count'] = "0"
    return JsonResponse(data=data, status=HTTPStatus.OK)

@api_view(['PUT'])
def set_profile_image(request):
    try:
        profile_image = request.FILES['profile_picture']
        banner_image = request.FILES['banner_picture']
        username = request.data.get('username')
        biology = request.data.get('biology')
    except:
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse(get_error_serialized(100, "User not found!").data, status=HTTPStatus.NOT_FOUND)
    user.profile_picture = profile_image
    user.banner_picture = banner_image
    user.biology = biology
    user.save(update_fields=['profile_picture', 'banner_picture', 'biology'])
    return JsonResponse(data={"message": "Image changed successfully!"}, status=HTTPStatus.OK)

@api_view(['PUT'])
def update_picture(request):
    user = request.user
    profile_picture = request.data.get('profile_picture', None)
    banner_picture = request.data.get('banner_picture', None)
    if not(profile_picture or banner_picture):
        return JsonResponse({"error" : get_error_serialized(103, 'profile_picture or banner_picture field is required').data})
    
    to_return_message = ""

    if profile_picture is not None:
        user.profile_picture = profile_picture
        user.save(update_fields = ['profile_picture'])
        to_return_message += "profile picture updated successfuly"

    if banner_picture is not None:
        user.banner_picture = banner_picture
        user.save(update_fields = ['banner_picture'])
        to_return_message += ", banner picture updated successfuly"
    
    # --------- TODO delete old images in media folder ---------- 

    return JsonResponse({"message" : to_return_message})

@api_view(['PUT'])
def update_username(request):
    user = request.user
    new_username = request.data.get('username', None)
    if new_username is None:
        return JsonResponse({"error" : get_error_serialized(103, 'username filed is required').data})
    
    user.username = new_username
    user.save(update_fields = ['username'])

    return JsonResponse({"message": f"username updated successfuly to {new_username}"})
    
@api_view(['PUT'])
def update_name(request):
    user = request.user
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    if first_name is None and last_name is None:
        return JsonResponse({"error" : get_error_serialized(103, 'first_name or last_name filed is required').data})

    to_return_message = ""

    if first_name is not None:
        user.first_name = first_name
        user.save(update_fields = ['first_name'])
        to_return_message += f"first name successfuly updated to \'{first_name}\'"
        
    if last_name is not None:
        user.last_name = last_name
        user.save(update_fields = ['last_name'])
        to_return_message += f", last name successfuly updated to \'{last_name}\'"

    return JsonResponse({"message": to_return_message})

