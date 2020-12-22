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
from community.models import Community
from user_profile.serializers import PublicProfileSerializer
from django.db.models import Q
# Create your views here.

@api_view(['GET'])
def search_in_users(request):

    serach_key = request.query_params.get('key', None)
    if(serach_key is None):
        return JsonResponse({'error': get_error_serialized(103, 'key parameter is required')}, status = HTTPStatus.BAD_REQUEST)
    
    data_usernames = []
    data_firstnames = []
    data_lastnames = []
    for user in User.objects.all():
        data_usernames.append((user.username, user.id))
        data_firstnames.append((user.first_name, user.id))
        data_lastnames.append((user.last_name, user.id))
    
    all_users_finded = []
    all_users_finded.extend(list(set(search(serach_key, data_usernames))))
    
    all_users_finded.extend(list(set(search(serach_key, data_firstnames))))
    
    all_users_finded.extend(list(set(search(serach_key, data_lastnames))))

    all_users_finded_ = User.objects.filter(Q(id__in = all_users_finded))

    return JsonResponse({"users_finded" : PublicProfileSerializer(all_users_finded_, many = True).data})

@api_view(['GET'])
def search_in_posts(request):

    serach_key = request.query_params.get('key', "")
    category_filter = request.query_params.get('category_filter', None)
    if category_filter == "": category_filter = None
    community_filter = request.query_params.get('community_filter', None)
    if community_filter == "": community_filter = None

    if serach_key == "" and category_filter is None and community_filter is None:
        return JsonResponse({'error': get_error_serialized(103, '\'key\' or \'category_filter\' \'community_filter\' parameter is required').data}, status = HTTPStatus.BAD_REQUEST)
    
    if not(community_filter is None):
        community = Community.objects.filter(name__iexact = community_filter.lower()).first()
        if community is None:
            return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = HTTPStatus.BAD_REQUEST)
    if not(category_filter is None) and len(category_filter) > 2:
        cf_mapped = categoryname_mapper(category_filter)
        if cf_mapped is not None: category_filter = cf_mapped
    
    data = []

    if not(category_filter is None):
        posts_filtered = Post.objects.filter(category = category_filter)
        if not(community_filter is None):
            posts_filtered = posts_filtered.filter(community = community)
        data_titles = list(posts_filtered.values_list('title', flat = True))
        data_ids = list(posts_filtered.values_list('id', flat = True))
        data = [(data_titles[i], data_ids[i]) for i in range(len(data_titles))]
    else:
        posts_filtered_ = Post.objects.all()
        if not(community_filter is None):
            posts_filtered_ = Post.objects.filter(community = community)
        data_titles = list(posts_filtered_.values_list('title', flat = True))
        data_ids = list(posts_filtered_.values_list('id', flat = True))
        data = [(data_titles[i], data_ids[i]) for i in range(len(data_titles))]

    finded_ids = list(set(search(serach_key, data)))
    
    all_posts_finded = []

    for p_id in finded_ids:
        for item in Post.objects.filter(id = p_id):
            all_posts_finded.append(PostSerializer(item, context = {"content_depth" : False}).data)

    return JsonResponse({"posts_finded" : all_posts_finded})
