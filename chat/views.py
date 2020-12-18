from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from http import HTTPStatus
from errors.error_repository import get_error_serialized, MISSING_REQUIRED_FIELDS, OBJECT_NOT_FOUND, PERMISSION_DENIED
from .models import DirectChatMessage, ChatFiles
# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload(request):
    file = request.FILES.get("data", None)
    chat_id = request.data.get("id", None)
    is_image = request.data.get("is_image", False)
    if(file is None or chat_id is None):
        return JsonResponse(data={"error" : get_error_serialized(MISSING_REQUIRED_FIELDS).data}, status=HTTPStatus.BAD_REQUEST)
    chat = DirectChatMessage.objects.filter(id=chat_id).first()
    if(chat is None):
        return JsonResponse(data={"error" : get_error_serialized(OBJECT_NOT_FOUND, detail="chat not found").data}, status=HTTPStatus.NOT_FOUND)
    if(chat._from != request.user):
        return JsonResponse(data=get_error_serialized(PERMISSION_DENIED), status=HTTPStatus.NOT_FOUND)
    ChatFiles.objects.create(chat=chat, is_image=is_image, file=file)
    return JsonResponse(data={'message' : "image uploaded successfully"}, status=HTTPStatus.CREATED)
