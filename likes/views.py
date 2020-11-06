from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from authentication.models import User
from posts.models import Post
from authentication.serializers import UserSerializer
from posts.serializer import PostSerializer
from comment.serializers import PostCommentsSerializer
from .serializers import *
from django.http import JsonResponse
from user_profile.serializers import PublicProfileSerializer
from http import HTTPStatus
@api_view(['GET', 'POST'])
def post_likes(request):
    if request.method == 'GET':
        post_id = request.query_params.get('id', None)
        if(post_id is None):
            return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
        post = Post.objects.filter(id=post_id).first()
        if(post is None):
            return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
        return JsonResponse(ViewPostLikesSerializer(post).data, status=HTTPStatus.FOUND)
    elif request.method == 'POST':
        post_id = request.data.get('post_id')
        username =  request.data.get('username')
        if not(post_id and username):
            return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
        post = Post.objects.filter(id=post_id).first()
        if(post is None):
            return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
        user = User.objects.filter(username=username).first()
        if(user is None):
            return JsonResponse({'message': 'User not found!'}, status=HTTPStatus.NOT_FOUND)
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

@api_view(['POST', 'GET'])
def comment_likes(request):
    if request.method == 'GET':
        comment_id = request.query_params.get('id', None)
        if(comment_id is None):
            return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
        comment = Comment.objects.filter(id=comment_id).first()
        if(comment is None):
            return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
        return JsonResponse(ViewCommentLikesSerializer(comment).data, status=HTTPStatus.FOUND)
    elif request.method == 'POST':
        comment_id = request.data.get('comment_id')
        username =  request.data.get('username')
        if not(comment_id and username):
            return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
        comment = Comment.objects.filter(id=comment_id).first()
        if(comment is None):
            return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
        user = User.objects.filter(username=username).first()
        if(user is None):
            return JsonResponse({'message': 'User not found!'}, status=HTTPStatus.NOT_FOUND)
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

@api_view(['POST'])
def get_user_likes(request):
    username = request.data.get('username')
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    likes = Like.objects.filter(user=user.id)
    if (likes == None):
        return JsonResponse({'username': username, 'likes_count': 0, 'posts': []}, status=HTTPStatus.FOUND)
    liked_posts = []
    for like in list(likes):
        post = Post.objects.get(id=like.post)
        liked_posts.append(PostSerializer(post).data)
    return JsonResponse({'username': username, 'likes_count': len(liked_posts), 'posts': liked_posts}, status=HTTPStatus.FOUND)