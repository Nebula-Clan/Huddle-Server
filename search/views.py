from django.shortcuts import render
from authentication.models import User
from posts.models import Post
from .search_func import search
from rest_framework.decorators import api_view
from authentication.serializers import UserSerializer
from posts.serializer import PostSerializer
from django.http.response import JsonResponse
# Create your views here.

@api_view(['POST'])
def search_in_users(request):

    serach_key = request.data.get('search_key')

    data_usernames = list(User.objects.values_list('username', flat = True))
    finded_usernames = list(set(search(serach_key, data_usernames)))
    
    data_firstnames = list(User.objects.values_list('first_name', flat = True))
    finded_firstnames = list(set(search(serach_key, data_firstnames)))
    
    data_lastnames = list(User.objects.values_list('last_name', flat = True))
    finded_lastnames = list(set(search(serach_key, data_lastnames)))

    all_users_finded = []

    for username in finded_usernames:
        all_users_finded.append(UserSerializer(User.objects.get(username = username)).data)
    for firstname in finded_firstnames:
        for item in User.objects.filter(first_name = firstname):
            all_users_finded.append(UserSerializer(item).data)
    for lastname in finded_lastnames:
        for item in User.objects.filter(last_name = lastname):
            all_users_finded.append(UserSerializer(item).data)
    
    return JsonResponse({"users_finded" : all_users_finded})

@api_view(['POST'])
def search_in_posts(request):

    serach_key = request.data.get('search_key')

    data_titles = list(Post.objects.values_list('title', flat = True))
    finded_titles = list(set(search(serach_key, data_titles)))
    
    all_posts_finded = []

    for title in finded_titles:
        for item in Post.objects.filter(title = title):
            all_posts_finded.append(PostSerializer(item).data)

    return JsonResponse({"posts_finded" : all_posts_finded})
