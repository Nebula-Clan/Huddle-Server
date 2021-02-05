from . models import Community
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from errors.error_repository import get_error_serialized
from rest_framework import status
from posts.models import Post
from authentication.models import User

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_community(request):
    user = request.user

    community_name = request.data.get('community_name', None)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)
    
    new_name = request.data.get('name', None)
    new_about = request.data.get('about', None)
    new_pic = request.data.get('picture', None)
    new_banner = request.data.get('banner_picture', None)

    if not(new_name is None):
        if Community.objects.filter(name__iexact = new_name.lower()).exists():
            return JsonResponse({"error" : get_error_serialized(109).data}, status = status.HTTP_400_BAD_REQUEST)
        community.name = new_name.lower()
        community.save(update_fields = ['name'])
    
    if not(new_about is None):
        community.about = new_about
        community.save(update_fields = ['about'])
    
    if not(new_pic is None):
        community.picture = new_pic
        community.save(update_fields = ['picture'])
    
    if not(new_banner is None):
        community.banner_picture = new_banner
        community.save(update_fields = ['banner_picture'])
    
    return JsonResponse({"message" : "all fields updated successfuly"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_community(request):
    user = request.user

    community_name = request.data.get('community_name', None)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)
    
    community.delete()

    return JsonResponse({"message" : "Community deleted successfuly"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    user = request.user

    community_name = request.data.get('community_name', None)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)
    
    post_id = request.data.get('post_id', None)

    post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if post.community_id != community.id:
        return JsonResponse({"error" : get_error_serialized(116).data}, status = status.HTTP_400_BAD_REQUEST)
    
    post.delete()

    return JsonResponse({"message" : "Post deleted successfuly"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_user(request):
    user = request.user

    community_name = request.data.get('community_name', None)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)

    username = request.data.get('username', None)

    del_user = User.objects.filter(username = username).first()
    if del_user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User not found').data}, status = status.HTTP_400_BAD_REQUEST)
    
    if not community.users.filter(username = username).exists():
        return JsonResponse({"error" : get_error_serialized(117).data}, status = status.HTTP_400_BAD_REQUEST)
    
    if del_user == user:
        return JsonResponse({"error" : get_error_serialized(118).data}, status = status.HTTP_400_BAD_REQUEST)

    community.users.remove(del_user)

    return JsonResponse({"message" : "User removed from community successfuly"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_user(request):
    user = request.user

    community_name = request.data.get('community_name', None)
    if community_name is None:
        return JsonResponse({"error" : get_error_serialized(103, '\'community_name\' field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)
    
    username = request.data.get('username', None)

    dis_user = User.objects.filter(username = username).first()
    if dis_user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User not found').data}, status = status.HTTP_400_BAD_REQUEST)
    
    community.disabeled_users.add(dis_user)

    return JsonResponse({"message" : "User added to disabeled users successfuly"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def enable_user(request):
    user = request.user

    community_name = request.data.get('community_name', None)
    if community_name is None:
        return JsonResponse({"error" : get_error_serialized(103, '\'community_name\' field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    community = Community.objects.filter(name__iexact = community_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if community.admin != user:
        return JsonResponse({"error" : get_error_serialized(106, 'Only community admin is allowed for this request').data}, status = status.HTTP_404_NOT_FOUND)
    
    username = request.data.get('username', None)

    en_user = User.objects.filter(username = username).first()
    if en_user is None:
        return JsonResponse({"error" : get_error_serialized(100, 'User not found').data}, status = status.HTTP_400_BAD_REQUEST)
    
    community.disabeled_users.remove(en_user)

    return JsonResponse({"message" : "User enabled users successfuly"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_admin(request):
    user = request.user
    communtiy_name = request.query_params.get('community', None)
    if communtiy_name is None:
        return JsonResponse({"error" : get_error_serialized(103, '\'community\' field is required').data}, status = status.HTTP_400_BAD_REQUEST)
    
    community = Community.objects.filter(name__iexact = communtiy_name.lower()).first()
    if community is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Community not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    is_admin = community.admin == user
    return JsonResponse({"is_admin" : is_admin})