from django.shortcuts import render
from posts.views import create_post, update_post, delete_post
from .models import DraftPost
from django.http.response import JsonResponse
from .serializers import DraftSerializer
from errors.error_repository import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http.request import HttpRequest

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    return create_post(request._request, True)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_drafts(request):
    user = request.user

    drafts = DraftPost.objects.filter(author = user)

    return JsonResponse({"draft_posts" : DraftSerializer(drafts, many = True, context = {"content_depth" : False, "author_depth" : True}).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_draft(request):
    draft_id = request.query_params.get('draft_id', None)
    
    if draft_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'draft_id field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    draft = DraftPost.objects.filter(id = draft_id).first()

    if draft is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Draft post not found!').data}, status = status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"draft_post" : DraftSerializer(draft, context = {"content_depth" : True, "author_depth" : True}).data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_draft(request):
    return update_post(request._request, is_draft = True)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_draft(request):
    return delete_post(request._request, is_draft = True)