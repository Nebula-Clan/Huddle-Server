from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
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
@api_view(['GET'])
@permission_classes([AllowAny])
def get_post_likes(request):
    post_id = request.query_params.get('id', None)
    if(post_id is None):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(ViewPostLikesSerializer(post).data, status=HTTPStatus.OK)
       
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_post_likes(request):
    post_id = request.data.get('post_id')
    user =  request.user
    if not(post_id and user):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    like_ = PostLike.objects.filter(post=post_id, user=user.id).first()
    if(like_ is not None):
        return JsonResponse({'message': 'Same like exists!'}, status=HTTPStatus.BAD_REQUEST)
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
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    like_ = CommentLike.objects.filter(comment=comment.id, user=user.id).first()
    if(like_ is not None):
        return JsonResponse({'message': 'Same like exists!'}, status=HTTPStatus.BAD_REQUEST)
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
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(ViewCommentLikesSerializer(comment).data, status=HTTPStatus.OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_likes(request):
    username = request.query_params.get('username', None)
    if not(username):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    viewer = None
    if not(request.user.is_anonymous):
        viewer = request.user.username
    return JsonResponse(UserLikesSerializer(user, context={'viewer': viewer}).data, status=HTTPStatus.OK)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment_like(request):
    user = request.user
    comment_id = request.data.get('id', None)
    comment_id = request.data.get('comment_id')
    user = request.user
    if not(comment_id and user):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    like = CommentLike.objects.filter(user=user.id).first()
    #TODO
    #delete comment