from django.shortcuts import render
from authentication.models import User
from posts.models import Post
from .search_func import search
from rest_framework.decorators import api_view
from authentication.serializers import UserSerializer
from posts.serializer import PostSerializer
from django.http.response import JsonResponse
from http import HTTPStatus
from errors.error_repository import get_error_serialized
from category.methods import *
from category.models import categories, Category
from category.serializers import CategorySerializer
from django.db.models import Q
from community.models import Community
from community.serializer import CommunitySmallSerializer
# Create your views here.

@api_view(['GET'])
def search_in_users(request):

    serach_key = request.query_params.get('key', None)
    if(serach_key is None):
        return JsonResponse({'message': 'Bad request!'}, status=HTTPStatus.BAD_REQUEST)
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

@api_view(['GET'])
def search_in_posts(request):

    serach_key = request.query_params.get('key', "")
    category_filter = request.query_params.get('category_filter', None)
    if category_filter == "": category_filter = None

    if serach_key == "" and category_filter is None:
        return JsonResponse({'error': get_error_serialized(103, '\'key\' or \'category_filter\' parameter is required').data}, status = HTTPStatus.BAD_REQUEST)
    
    if not(category_filter is None) and len(category_filter) > 2:
        cf_mapped = categoryname_mapper(category_filter)
        if cf_mapped is not None: category_filter = cf_mapped
    
    data = []

    if not(category_filter is None):
        posts_filtered = Post.objects.filter(category = category_filter)
        data_titles = list(posts_filtered.values_list('title', flat = True))
        data_ids = list(posts_filtered.values_list('id', flat = True))
        data = [(data_titles[i], data_ids[i]) for i in range(len(data_titles))]
    else:
        data_titles = list(Post.objects.values_list('title', flat = True))
        data_ids = list(Post.objects.values_list('id', flat = True))
        data = [(data_titles[i], data_ids[i]) for i in range(len(data_titles))]

    finded_ids = list(set(search(serach_key, data)))
    
    all_posts_finded = []

    for p_id in finded_ids:
        for item in Post.objects.filter(id = p_id):
            all_posts_finded.append(PostSerializer(item, context = {"content_depth" : False}).data)

    return JsonResponse({"posts_finded" : all_posts_finded})

@api_view(['GET'])
def search_in_categories(request):
    category_text = request.query_params.get('key', None)
    if category_text == "": category_text = None

    if category_text is None:
        return JsonResponse({"error" : get_error_serialized(103, 'key parameter is required')}, status = HTTPStatus.BAD_REQUEST)
    
    data = [(cat[1], cat[0]) for cat in categories]
    finded_ids = search(category_text, data)
    finded_categories = Category.objects.filter(Q(name__in = finded_ids))

    return JsonResponse({"categories" : CategorySerializer(finded_categories, many = True).data})

    
@api_view(['GET'])
def search_in_communities(request):
    name = request.query_params.get('key', None)
    if name == "": name = None

    if name is None:
        return JsonResponse({"error" : get_error_serialized(103, 'key parameter is required').data}, status = HTTPStatus.BAD_REQUEST)
    
    data = [(community.name, community.id) for community in Community.objects.all()]
    finded_ids = search(name, data)

    finded_coms = Community.objects.filter(Q(id__in = finded_ids))

    return JsonResponse({"communities" : CommunitySmallSerializer(finded_coms, many = True).data})