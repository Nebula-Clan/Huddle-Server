from posts.models import Post
from posts.serializer import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from .generate_posts import *
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    user = request.user
    related_likes_ = [rl[0] for rl in related_likes(user)]
    related_community_ = [rc[0] for rc in related_community(user)]
    related_followings_ = [rf[0] for rf in related_followings(user)]
    
    posts = Post.objects.filter(Q(pk__in = related_likes_) | Q(pk__in = related_community_) | Q(pk__in = related_followings_))
    return JsonResponse({"posts":PostSerializer(posts, many = True)})
