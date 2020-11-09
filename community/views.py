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
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_community(request):
    creator = request.user

    name = request.data.get('name')
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
    cm_id = request.query_params.get('id', None)
    summery = request.query_params.get('summery', 'f')
    if cm_id is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)

    if summery == 't':
        community_serialized = CommunitySmallSerializer(community).data
    elif summery == 'f':
        community_serialized = CommunityCompleteSerializer(community).data
    else:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"community" : community_serialized})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_community_members(request):
    cm_id = request.query_params.get('id', None)
    if cm_id is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    members = community.users.all()
    return JsonResponse({"members" : PublicProfileSerializer(members, many = True).data})

@api_view(['GET'])
def get_community_posts(request):
    cm_id = request.query_params.get('id', None)
    if cm_id is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    if not Community.objects.filter(id = cm_id).exists():
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    posts = list(Post.objects.filter(community = cm_id))
    # posts.reverse()
    return JsonResponse({"posts" : PostSerializer(posts, many = True).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_community(request):
    user = request.user
    cm_id = request.query_params.get('id')
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    if user in community.users.all():
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    community.users.add(user)
    return JsonResponse({"message" : "user added successfuly"})

@api_view(['DELETE'])
def leave_community(request):
    to_delete_user = request.user
    cm_id = request.data.get('community_id')
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    if not(to_delete_user in community.users.all()):
        return JsonResponse({"error" : ErrorSerializer(get_error(100).data)}, status = status.HTTP_400_BAD_REQUEST)
    community.users.remove(to_delete_user)
    return JsonResponse({"message" : "user removed successfuly"})
