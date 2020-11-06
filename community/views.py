from django.shortcuts import render
from .models import Community
from authentication.models import User
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializer import CommunitySerializer
from user_profile.serializers import PublicProfileSerializer 
# Create your views here.

@api_view(['POST'])
def create_community(request):
    creator = request.user

    name = request.data.get('name')
    about = request.data.get('about')

    image = request.data.get('image')
    back_image = request.data.get('back_image')
    
    to_create_community = Community(name = name, about = about, admin = creator)
    to_create_community.save()

    if not(image is None):
        to_create_community.image = image
    if not(back_image is None):
        to_create_community.back_image = back_image
    to_create_community.save(update_fields = ['image', 'back_image'])

    serialized_community = CommunitySerializer(to_create_community).data
    return JsonResponse({"community" : serialized_community, "message" : "Community created successfuly"})

@api_view(['GET'])
def get_community(request):
    cm_id = request.data.get('community_id')
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"message" : "Community not found"}, status = status.HTTP_404_NOT_FOUND)
    cm_users = community.users.all()
    admin = User.objects.filter(id = community.admin_id).first()

    serialized_cm_users = []
    for cm_user in cm_users:
        serialized_cm_users.append(PublicProfileSerializer(cm_user).data)
    
    admin_serialized = PublicProfileSerializer(admin).data
    community_serialized = CommunitySerializer(community).data

    return JsonResponse({"community" : community_serialized,
                            "admin" : admin_serialized,
                            "users" : serialized_cm_users})

@api_view(['POST'])
def join_community(request):
    user = request.user
    cm_id = request.data.get('community_id')
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"message" : "Community not found"})
    if user in community.users.all():
        return JsonResponse({"message" : "User already exists"})
    community.users.add(user)
    return JsonResponse({"message" : "user added successfuly"})

@api_view(['DELETE'])
def leave_community(request):
    to_delete_user = request.user
    cm_id = request.data.get('community_id')
    community = Community.objects.filter(id = cm_id).first()
    if community is None:
        return JsonResponse({"message" : "Community not found"})
    if not(to_delete_user in community.users.all()):
        return JsonResponse({"message" : "User dont exists in this community"})
    community.users.remove(to_delete_user)
    return JsonResponse({"message" : "user removed successfuly"})
    