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
from user_profile.serializers import PublicProfileSerializer
from hashtag.models import *
from django.db.models import Q
from category.methods import *
from category.models import categories, Category
from category.serializers import CategorySerializer
from community.models import Community
from community.serializer import CommunitySmallSerializer
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
    hashtag_filter = request.query_params.get('hashtag_filter', None)
    if hashtag_filter == "": hashtag_filter = None

    if serach_key == "" and category_filter is None and community_filter is None and hashtag_filter is None:
        return JsonResponse({'error': get_error_serialized(103, '\'key\' or \'category_filter\' or \'hashtag_filter\' or \'community_filter\' parameter is required').data}, status = HTTPStatus.BAD_REQUEST)
    
    if not(community_filter is None):
        community = Community.objects.filter(name__iexact = community_filter.lower()).first()
        if community is None:
            return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = HTTPStatus.BAD_REQUEST)
    if not(category_filter is None) and len(category_filter) > 2:
        cf_mapped = categoryname_mapper(category_filter)
        if cf_mapped is not None: category_filter = cf_mapped
    if not(hashtag_filter is None):
        hashtag_filter_id = 0
        hashtag_filter_ = Hashtag.objects.filter(text = hashtag_filter).first()
        if not(hashtag_filter_ is None): hashtag_filter_id = hashtag_filter_.id

    data = []

    if not(category_filter is None):
        posts_filtered = Post.objects.filter(category = category_filter)
        if not(community_filter is None):
            posts_filtered = posts_filtered.filter(community = community)
        data = []
        for item in posts_filtered:
            data.append((item.title, item.id))
    else:
        posts_filtered_ = Post.objects.all()
        if not(community_filter is None):
            posts_filtered_ = Post.objects.filter(community = community)
        data = []
        for item in posts_filtered:
            data.append((item.title, item.id))

    finded_ids = list(set(search(serach_key, data)))
    
    if not(hashtag_filter is None):
        finded_ids = PostHashtag.objects.filter(Q(post__in = finded_ids) & Q(hashtag = hashtag_filter_id)).values_list('post', flat = True)

    all_posts_finded = Post.objects.exclude(Q(title__isnull = True) | Q(title = "") | Q(header_image__isnull = True) | Q(header_image = "") | Q(header_image__icontains = "undefined") | Q(header_image__icontains = "null")).filter(id__in = finded_ids)
    
    return JsonResponse({"posts_finded" : PostSerializer(all_posts_finded, many = True, context = {"content_depth" : False}).data})

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
    
    if name is None:
        return JsonResponse({"error" : get_error_serialized(103, 'key parameter is required').data}, status = HTTPStatus.BAD_REQUEST)
    if name == "":
        return JsonResponse({"communities" : CommunitySmallSerializer(Community.objects.all(), many = True).data})
    data = [(community.name, community.id) for community in Community.objects.all()]
    finded_ids = search(name, data)

    finded_coms = Community.objects.filter(Q(id__in = finded_ids))

    return JsonResponse({"communities" : CommunitySmallSerializer(finded_coms, many = True).data})