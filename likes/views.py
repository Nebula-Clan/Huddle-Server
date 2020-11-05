from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Like
from authentication.models import User
from posts.models import Post
from authentication.serializers import UserSerializer
from posts.serializer import PostSerializer
from .serializers import LikeSerializer
from django.http import JsonResponse
from user_profile.serializers import PublicProfileSerializer
from http import HTTPStatus
@api_view(['POST'])
def get_likes(request):
    post_id = request.data.get('post_id')
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    likes = Like.objects.filter(post=post_id)
    if (likes == None):
        return JsonResponse({'post_id': post_id, 'likes_count': 0, 'users': []}, status=HTTPStatus.FOUND)
    liked_users = []
    for like in list(likes):
        user = User.objects.filter(username=like.user).first()
        liked_users.append(PublicProfileSerializer(user).data)
    return JsonResponse({'post_id': post_id, 'likes_count': len(liked_users), 'users': liked_users}, status=HTTPStatus.FOUND)

@api_view(['POST'])
def submit_like(request):
    post_id = request.data.get('post_id')
    username =  request.data.get('username')
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message': 'User not found!'}, status=HTTPStatus.NOT_FOUND)
    like_ = Like.objects.filter(post=post_id, user=user.id).first()
    if(like_ is not None):
        return JsonResponse({'message': 'Same like exists!'}, status=HTTPStatus.BAD_REQUEST)
    data = {'post': post_id, 'user': user.id}
    like = LikeSerializer(data=data)
    if(like.is_valid()):
        like.save()
    else:
        return JsonResponse({'message': 'Something wrong in like data.'}, status=HTTPStatus.BAD_REQUEST)
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