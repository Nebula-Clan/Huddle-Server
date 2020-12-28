from django.shortcuts import render
from .models import Community
from posts.models import Post
from authentication.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializer import CommunityCompleteSerializer
from .serializer import CommunitySmallSerializer
from posts.serializer import PostSerializer
from user_profile.serializers import PublicProfileSerializer
from errors.serializers import ErrorSerializer
from errors.error_repository import *
from huddle.settings import PCOUNT
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_community(request):
    creator = request.user

    name = request.data.get('name')

    if Community.objects.filter(name__iexact = name.lower()).exists():
        return JsonResponse({"error" : get_error_serialized(109).data}, status = status.HTTP_400_BAD_REQUEST)

    about = request.data.get('about')

    picture = request.data.get('picture')
    banner_picture = request.data.get('banner_picture')
    
    to_create_community = Community(name = name, about = about, admin = creator)
    to_create_community.save()

    if not(picture is None):
        to_create_community.picture = picture
    if not(banner_picture is None):
        to_create_community.banner_picture = banner_picture
    to_create_community.save(update_fields = ['picture', 'banner_picture'])

    serialized_community = CommunitySmallSerializer(to_create_community).data
    return JsonResponse({"community" : serialized_community, "message" : "Community created successfuly"})

@api_view(['GET'])
def get_community(request):
    cm_name = request.query_params.get('name', None)
    summery = request.query_params.get('summery', 'f')
    if cm_name is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(name__iexact = cm_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)

    if summery == 't':
        community_serialized = CommunitySmallSerializer(community).data
    elif summery == 'f':
        community_serialized = CommunityCompleteSerializer(community).data
    else:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"community" : community_serialized})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_community_members(request):
    viewer = request.user
    cm_name = request.query_params.get('name', None)
    if cm_name is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(name__iexact = cm_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    members = community.users.all()
    return JsonResponse({"members" : PublicProfileSerializer(members, many = True, context = {"viewer_id" : viewer.id}).data})

@api_view(['GET'])
def get_community_posts(request):
    cm_name = request.query_params.get('name', None)
    if cm_name is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(name__iexact = cm_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
        
    try:
        offset_str = request.query_params.get('offset', None)
        if not(offset_str is None): offset = int(offset_str)
    except:
        return JsonResponse({"error" : get_error_serialized(110, 'offset must be integer').data})
    
    posts = list(Post.objects.filter(community = community.id))
    posts.sort(key = lambda post : post.date_created, reverse = True)

    if not(offset_str is None):
        posts = posts[PCOUNT * offset: PCOUNT * (offset + 1)]
    return JsonResponse({"posts" : PostSerializer(posts, context = {"content_depth" : False}, many = True).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_community(request):
    user = request.user
    cm_name = request.query_params.get('name')
    if cm_name is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(name__iexact = cm_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    if user in community.users.all():
        return JsonResponse({"error" : ErrorSerializer(get_error(107)).data}, status = status.HTTP_400_BAD_REQUEST)
    community.users.add(user)
    return JsonResponse({"message" : "user added successfuly"})

@api_view(['DELETE'])
def leave_community(request):
    to_delete_user = request.user
    cm_name = request.query_params.get('name', None)
    if cm_name is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(name__iexact = cm_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    if not(to_delete_user in community.users.all()):
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_400_BAD_REQUEST)
    community.users.remove(to_delete_user)
    return JsonResponse({"message" : "user removed successfuly from community"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_communities(request):
    user = request.user
    communities = user.in_community.all()
    communities_serialized = CommunitySmallSerializer(communities, many = True)

    user_serialized = PublicProfileSerializer(user)
    return JsonResponse({"user" : user_serialized.data, "communities" : communities_serialized.data})