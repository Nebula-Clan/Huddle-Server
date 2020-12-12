import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync
from authentication.authenticators import authenticate
from errors.error_repository import AUTHENTICATION_FAILED, AUTHENTICATION_REQUIRED,PERMISSION_DENIED, OBJECT_NOT_FOUND, MISSING_REQUIRED_FIELDS, get_error_serialized
from django.utils.timezone import now
from chat.models import Clients, DirectChatMessage, LastSeen
from chat.serializers import ChatUsersSerializer, DirectChatViewSerializer
from django.contrib.auth import get_user_model
import huddle.utils as utils
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.channel_name)
        self.user = None
        self.accept()

    def disconnect(self, close_code):
        if(self.user is not None):
            Clients.objects.filter(username=self.user.id, channel_name=self.channel_name).delete()
            last_seen_data = LastSeen.objects.filter(user=self.user).first()
            if(last_seen_data is None):
                print("Creating")
                last_seen_data = LastSeen.objects.create(user=self.user)
            # last_seen_data.last_seen = now()/
            last_seen_data.save()
            print(last_seen_data)
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
            return 
        if(user.username != self.room_name):
            self.send(json.dumps({"error" : get_error_serialized(PERMISSION_DENIED).data}))
            self.close()
            return
        last_seen_data = LastSeen.objects.filter(user=user).first()
        if(last_seen_data is None):
            last_seen_data = LastSeen.objects.create(user=self.user)
        # last_seen_data.last_seen = now()
        last_seen_data.save()
        record = Clients.objects.filter(username=user, channel_name=self.channel_name).first()
        if(record is None):
            Clients.objects.create(username=user, channel_name=self.channel_name)
        self.send(json.dumps({"type" : "chat.authenticate", "message" : "Authenticatied."}))
    
    def chat_users(self, event):
        if(self.user is None):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_REQUIRED).data}))
            return
        chats_from_user = list(DirectChatMessage.objects.filter(_from=self.user))
        chats_to_user = list(DirectChatMessage.objects.filter(_to=self.user))
        records = chats_from_user + chats_to_user
        records = sorted(records, key=lambda x : x.date)[::-1]
        users = []
        for record in records:
            if(record._from.id == self.user.id and record._to not in users):
                users.append(record._to)
            elif (record.to.id == self.user.id and record._from not in users):
                users.append(record._from)
        result = []
        for user in users: 
            result.append(ChatUsersSerializer(user, context={"target_username" : self.user.username}).data)
        self.send(json.dumps({"type" : "chat.users", "data" : result}))
    def chat_message_send(self, event):
        if(self.user is None):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_REQUIRED).data}))
            return
        to_username = event.get('to', None)
        text = event.get('text', None)
        if (to_username is None or text is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS).data}))
            return
        Users = get_user_model()
        user_to = Users.objects.filter(username=to_username).first()
        if(user_to is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS, detail="User to send message not found!").data}))
            return
        chat = DirectChatMessage.objects.create(_to=user_to, text=text, _from=self.user, seen=False)
        other_user_active_sessions = Clients.objects.filter(username=user_to)
        channel_layer = get_channel_layer()
        for session in other_user_active_sessions:
            async_to_sync(channel_layer.send)(session.channel_name, 
            {"type" : "chat.message.recieve", 
             "message" : DirectChatViewSerializer(instance=chat, context={"target_username" : user_to.username}).data})   
    def chat_message_recieve(self, event):
        self.send(json.dumps(event))
    def chat_message_get(self, event):
        if(self.user is None):
            self.send(json.dumps({"error" : get_error_serialized(AUTHENTICATION_REQUIRED).data}))
            return
        other_user = event.get("from", None)
        offset = event.get("offset", None)
        count = event.get("count", None)
        if (other_user is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS).data}))
            return
        offset = utils.int_try_parse(offset, 0)
        count = utils.int_try_parse(count, utils.INFINITY)
        Users = get_user_model()
        other_user = Users.objects.filter(username=other_user).first()
        if(other_user is None):
            self.send(json.dumps({"error" : get_error_serialized(MISSING_REQUIRED_FIELDS, detail="User to get messages not found!").data}))
            return
        chats = list(DirectChatMessage.objects.filter(_from= self.user, _to=other_user))
        chats += list(DirectChatMessage.objects.filter(_from=other_user, _to=self.user))
        chats = sorted(chats, key= lambda x : x.date)[::-1]
        result = []
        if(offset < len(chats)):
            chats = chats[offset: offset + count]
        else:
            chats = []
        for chat in chats:
            result.append(DirectChatViewSerializer(chat, context={"target_username" : self.user.username}).data)
        self.send(json.dumps({"type" : "chat.message.get", "data" : json.dumps(result)}))    
        
        