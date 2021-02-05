from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from authentication.authenticators import SimpleAuthenticator
from .models import *
from authentication.models import User
from posts.models import Post
from authentication.serializers import UserSerializer
from posts.serializer import PostSerializer
from comment.serializers import RepliedCommentSerializer
from .serializers import *
from django.http import JsonResponse
from user_profile.serializers import PublicProfileSerializer
from http import HTTPStatus
from errors.error_repository import get_error, get_error_serialized
from errors.serializers import ErrorSerializer
@api_view(['GET'])
@permission_classes([AllowAny])
def get_post_likes(request):
    post_id = request.query_params.get('id', None)
    if(post_id is None):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse(get_error_serialized(100, "Post not found!").data, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(ViewPostLikesSerializer(post).data, status=HTTPStatus.OK)
       
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_post_likes(request):
    post_id = request.data.get('post_id')
    user =  request.user
    if not(post_id and user):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse(get_error_serialized(100, "Post not found!").data, status=HTTPStatus.NOT_FOUND)
    like_ = PostLike.objects.filter(post=post_id, user=user.id).first()
    if(like_ is not None):
        return JsonResponse(ErrorSerializer(get_error(110)).data, status=HTTPStatus.BAD_REQUEST)
    data = {'post': post_id, 'user': user.id}
    like = PostLikeSerializer(data=data)
    if(like.is_valid()):
        like.save()
    else:
        return JsonResponse(like.errors, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Like submitted.'}, status=HTTPStatus.CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_comment_likes(request):
    comment_id = request.data.get('comment_id')
    user = request.user
    if not(comment_id and user):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse(get_error_serialized(100, "Comment not found!").data, status=HTTPStatus.NOT_FOUND)
    like_ = CommentLike.objects.filter(comment=comment.id, user=user.id).first()
    if(like_ is not None):
        return JsonResponse(ErrorSerializer(get_error(110)).data, status=HTTPStatus.BAD_REQUEST)
    data = {'comment': comment_id, 'user': user.id}
    like = CommentLikeSerializer(data=data)
    if(like.is_valid()):
        like.save()
    else:
        return JsonResponse(like.errors, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Like submitted.'}, status=HTTPStatus.CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_comment_likes(request):
    comment_id = request.query_params.get('id', None)
    if(comment_id is None):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse(get_error_serialized(100, "Coment not found!").data, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(ViewCommentLikesSerializer(comment).data, status=HTTPStatus.OK)

@api_view(['GET'])
@authentication_classes([SimpleAuthenticator])
def get_user_likes(request):
    username = request.query_params.get('username', None)
    viewer = request.query_params.get('viewer', None)
    if not(username):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse(get_error_serialized(100, "User not found!").data, status=HTTPStatus.NOT_FOUND)
    if not(request.user.is_anonymous) and viewer is None:
        viewer = request.user.username
    return JsonResponse(UserLikesSerializer(user, context={'viewer': viewer}).data, status=HTTPStatus.OK)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment_like(request):
    user = request.user
    comment_id = request.data.get('id', None)
    if not(comment_id and user):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse(get_error_serialized(100, "Comment not found!").data, status=HTTPStatus.NOT_FOUND)
    like = CommentLike.objects.filter(user=user.id, comment=comment.id).first()
    if(like is None):
        return JsonResponse(get_error_serialized(100, "Like not found!").data, status=HTTPStatus.NOT_FOUND)
    like.delete()
    return JsonResponse({"message": "Like deleted successfully."}, status=HTTPStatus.OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post_like(request):
    user = request.user
    post_id = request.data.get('id', None)
    if not(post_id and user):
        return JsonResponse(ErrorSerializer(get_error(103)).data, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse(get_error_serialized(100, "Post not found!").data, status=HTTPStatus.NOT_FOUND)
    like = PostLike.objects.filter(user=user.id, post=post.id).first()
    if(like is None):
        return JsonResponse(get_error_serialized(100, "Like not found!").data, status=HTTPStatus.NOT_FOUND)
    like.delete()
    return JsonResponse({"message": "Like deleted successfully."}, status=HTTPStatus.OK)