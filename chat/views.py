from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from http import HTTPStatus
from errors.error_repository import get_error_serialized, MISSING_REQUIRED_FIELDS, OBJECT_NOT_FOUND, PERMISSION_DENIED
from .models import DirectChatMessage, ChatFiles, Clients
from huddle.utils import int_try_parse
import uuid
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from user_profile.serializers import PublicProfileSerializer
from .serializers import DirectChatViewSerializer
# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload(request):
    file = request.FILES.get("data", None)
    user_to = request.data.get("username", None)
    file_type = request.data.get("file_type", False)
    uuid_ =  request.data.get("uuid", None)
    file_type = int_try_parse(file_type, 1)
    
    if(file is None or user_to is None):
        return JsonResponse(data={"error" : get_error_serialized(MISSING_REQUIRED_FIELDS).data}, status=HTTPStatus.BAD_REQUEST)
    
    User = get_user_model()
    user_to = User.objects.filter(username=user_to).first()
    if(user_to is None):
        return JsonResponse(
                            data={ "error" : get_error_serialized(OBJECT_NOT_FOUND, detail="user not found").data}, 
                            status=HTTPStatus.NOT_FOUND)
    chat = DirectChatMessage.objects.create(_to=user_to, text="", _from=request.user, seen=False, file_type=file_type)
    if(uuid_ is not None):
        try:
            uuid_ = uuid.UUID(uuid_)
            chat.uuid= uuid_
        except ValueError:
            chat.delete()
            return JsonResponse(data={"error" : get_error_serialized(MISSING_REQUIRED_FIELDS, detail="Invalid UUID").data}, status=HTTPStatus.BAD_REQUEST)
    file = ChatFiles.objects.create(chat=chat, is_image=False, file=file)
    chat.text = str(file.file)
    chat.save()
    other_user_active_sessions = Clients.objects.filter(username=user_to)
    channel_layer = get_channel_layer()
    data = {
                "type" : "chat.message.recieve", 
                "_from" : PublicProfileSerializer(request.user).data,
                "message" : DirectChatViewSerializer(instance=chat, context={"target_username" : user_to.username}).data
            }
    for session in other_user_active_sessions:
            async_to_sync(channel_layer.send)(session.channel_name, data)
    return JsonResponse(data={'message' : "message sent successfully", "url" : chat.text}, status=HTTPStatus.CREATED)
