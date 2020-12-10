import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync
from authentication.authenticators import authenticate
from errors.error_repository import AUTHENTICATION_FAILED, AUTHENTICATION_REQUIRED,PERMISSION_DENIED, OBJECT_NOT_FOUND, MISSING_REQUIRED_FIELDS, get_error_serialized

from chat.models import Clients, DirectChatMessage
from chat.serializers import ChatUsersSerializer, DirectChatViewSerializer
from django.contrib.auth import get_user_model
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.channel_name)
        self.user = None
        self.accept()

    def disconnect(self, close_code):
        if(self.user is not None):
            Clients.objects.filter(username=self.user.id, channel_name=self.channel_name).delete()
            self.user = None

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(self.channel_name, text_data_json)   
    
    def chat_authenticate(self, event):
        token = event.get('access_token', None)
        user = authenticate(token)
        self.user = user
        if(user.is_anonymous):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_FAILED).data}))
            self.close()
        if(user.username != self.room_name):
            self.send(json.dumps({"error" : get_error_serialized(PERMISSION_DENIED).data}))
            self.close()
        record = Clients.objects.filter(username=user, channel_name=self.channel_name).first()
        if(record is None):
            Clients.objects.create(username=user, channel_name=self.channel_name)
    
    def chat_users(self, event):
        if(self.user is None):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_REQUIRED).data}))
            return
        chats_from_user = list(DirectChatMessage.objects.filter(_from=self.user))
        chats_to_user = list(DirectChatMessage.objects.filter(_to=self.user))
        users = [record._to for record in chats_from_user]
        users += [record._from for record in chats_to_user]
        users = list(set(users))
        data = ChatUsersSerializer(users, context={"target_username" : self.user.username}, many=True).data
        self.send(json.dumps(data))
    def chat_message_send(self, event):
        if(self.user is None):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_REQUIRED).data}))
            return
        to_username = event.get('to', None)
        text = event.get('text', None)
        if (to_username is None or text is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS).data}))
        Users = get_user_model()
        user_to = Users.objects.filter(username=to_username).first()
        if(user_to is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS, detail="User to send message not found!").data}))
        chat = DirectChatMessage.objects.create(_to=user_to, text=text, _from=self.user, seen=False)
        other_user_active_sessions = Clients.objects.filter(username=user_to)
        channel_layer = get_channel_layer()
        for session in other_user_active_sessions:
            async_to_sync(channel_layer.send)(session.channel_name, {"type" : "chat.message.recieve", "message" : DirectChatViewSerializer(instance=chat).data})   
    def chat_message_recieve(self, event):
        j = json.dumps(event["message"])
        self.send(j)
        
        
        