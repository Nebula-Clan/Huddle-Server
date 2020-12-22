from posts.models import Post
from posts.serializer import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from .generate_posts import *
from django.db.models import Q
from category.methods import categoryname_mapper, categoryid_mapper

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
    print(posts_id)
    if not(category_filter is None):
        posts = Post.objects.filter(Q(pk__in = posts_id), category = category_filter)
    else:
        posts = Post.objects.filter(Q(pk__in = posts_id))
        
    return JsonResponse({"posts":PostSerializer(posts, many = True).data})

