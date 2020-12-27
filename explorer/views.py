from posts.models import Post
from posts.serializer import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from .generate_posts import *
from django.db.models import Q
from category.methods import categoryname_mapper, categoryid_mapper
from errors.error_repository import get_error_serialized
from rest_framework import status
from hashtag.models import Hashtag, PostHashtag

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    user = request.user
    
    category_filter = request.query_params.get('category_filter', None)
    if category_filter == "": category_filter = None

    
    if not(category_filter is None) and len(category_filter) > 2:
        cf_mapped = categoryname_mapper(category_filter)
        if cf_mapped is not None: category_filter = cf_mapped
    
    posts_id = []
    posts_id.extend(related_community(user))
    posts_id.extend(related_likes(user))
    posts_id.extend(related_followings(user))
    
    posts_id_set = set(posts_id)

    if not(category_filter is None):
        posts = Post.objects.exclude(Q(header_image__isnull = True) | Q(header_image = "") | Q(header_image__icontains = "undefined") | Q(header_image__icontains = "null")).filter(Q(pk__in = posts_id_set), category = category_filter)
    else:
        posts = Post.objects.exclude(Q(header_image__isnull = True) | Q(header_image = "") | Q(header_image__icontains = "undefined") | Q(header_image__icontains = "null")).filter(Q(pk__in = posts_id_set))
        
    return JsonResponse({"posts":PostSerializer(posts, many = True, context = {"content_depth" : False}).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_by_hashtag(request):
    user = request.user

    hashtag_text = request.query_params.get('hashtag', None)
    if hashtag_text == "": hashtag_text = None
    
    if hashtag_text is None:
        return JsonResponse({"error" : get_error_serialized(103, 'hashtag field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    hashtag = Hashtag.objects.filter(text = hashtag_text).first()

    if hashtag is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Hashtag not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    posts_found_id = PostHashtag.objects.filter(hashtag = hashtag).values_list('post', flat = True)
    posts_found = Post.objects.filter(Q(pk__in = posts_found_id))
    return JsonResponse({"posts" : PostSerializer(posts_found, many = True, context = {"content_depth" : False}).data})