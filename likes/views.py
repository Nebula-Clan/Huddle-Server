from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Like
from authentication.models import User
from authentication.serializers import UserSerializer
from .serializers import LikeSerializer
from django.http import JsonResponse
from http import HTTPStatus
@api_view(['GET'])
def get_likes(request):
    post_id = request.data.get('post_id')
    #check if post is available! TODO
    likes = Like.objects.filter(post_id=post_id)
    if (likes == None):
        return JsonResponse({'post_id': post_id, 'likes_count': 0, 'users': []}, status=HTTPStatus.FOUND)
    liked_users = []
    for like in list(likes):
        user = User.objects.filter(username=like.user_id).first()
        liked_users.append(UserSerializer(user).data)
    return JsonResponse({'post_id': post_id, 'likes_count': len(liked_users), 'users': liked_users}, status=HTTPStatus.FOUND)

@api_view(['POST'])
def submit_like(request):
    post_id = request.data.get('post_id')
    username =  request.data.get('username')
    #check if post is available! TODO
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message': 'User not found!'}, status=HTTPStatus.BAD_REQUEST)
    like_ = Like.objects.filter(post_id=post_id, user_id=user.id).first()
    if(like_ is not None):
        return JsonResponse({'message': 'Same like exists!'}, status=HTTPStatus.BAD_REQUEST)
    data = {'post_id': post_id, 'user_id': user.id}
    like = LikeSerializer(data=data)
    if(like.is_valid()):
        like.save()
    else:
        return JsonResponse({'message': 'Something wrong in like data.'}, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Like submitted.'}, status=HTTPStatus.CREATED)