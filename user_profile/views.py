from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from http import HTTPStatus
from authentication.models import User
from posts.models import Post
from .serializers import PublicProfileSerializer
from likes.models import PostLike, CommentLike
from comment.serializers import UserCommentSerializer
from errors.error_repository import get_error_serialized, get_error
from errors.serializers import ErrorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_public_profile(request):
    viewer = request.user
    username = request.query_params.get('username', None)
    if(username is None):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)

    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse(get_error_serialized(100, "User not found!").data, status=HTTPStatus.NOT_FOUND)
    public_profile = PublicProfileSerializer(user, context = {"viewer_id" : viewer.id})
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
def update_profile(request):
    user = request.user
    profile_picture = request.data.get('profile_picture', None)
    banner_picture = request.data.get('banner_picture', None)
    new_username = request.data.get('username', None)
    new_pass = request.data.get('password', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    email = request.data.get('email', None)
    biology = request.data.get('biology', None)

    if not(profile_picture or banner_picture or new_username or new_pass or first_name or last_name or email or biology):
        return JsonResponse({"error" : get_error_serialized(103, 'first_name or last_name or profile_picture or banner_picture or username or password or email or biology field is required')}, status = HTTPStatus.BAD_REQUEST)

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
    
    if first_name is not None:
        user.first_name = first_name
        user.save(update_fields = ['first_name'])
        to_return_message += f" ,first name successfuly updated to \'{first_name}\'"
        
    if last_name is not None:
        user.last_name = last_name
        user.save(update_fields = ['last_name'])
        to_return_message += f", last name successfuly updated to \'{last_name}\'"
    
    if new_username is not None:
        if User.objects.filter(username = new_username).exists():
            return JsonResponse({"error" : get_error_serialized(104).data}, status = HTTPStatus.BAD_REQUEST)
        
        user.username = new_username
        user.save(update_fields = ['username'])
        to_return_message += f" ,username successfuly updated to \'{new_username}\'"
    
    if new_pass is not None:
        if User.check_password(user, new_pass):
            return JsonResponse({"error" : get_error_serialized(113).data}, status = HTTPStatus.BAD_REQUEST)
    
        user.set_password(new_pass)
        user.save(update_fields = ['password'])
        to_return_message += " ,password successfuly updated"
    
    if email is not None:
        user.email = email
        user.save(update_fields = ['email'])
        to_return_message += f" ,email successfuly updated to {email}"
    
    if biology is not None:
        user.biology = biology
        user.save(update_fields = ['biology'])
        to_return_message += " ,biology successfuly updated"
    
    return JsonResponse({"message" : to_return_message})


@api_view(['PUT'])
def update_password(request):
    user = request.user

    old_pass = request.data.get('old_password', None)
    new_pass = request.data.get('new_password', None)

    if not(old_pass and new_pass):
        return JsonResponse({"error" : get_error_serialized(103, "new_password or old_password field is required").data}, status = status.HTTPStatus.BAD_REQUEST)

    if not User.check_password(user, old_pass):
        return JsonResponse({"error" : get_error_serialized(101).data}, status = HTTPStatus.BAD_REQUEST)
    
    user.set_password(new_pass)
    user.save(update_fields = ['password'])

    return JsonResponse({"message" : "password successfuly updated"})
