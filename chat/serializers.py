
from .models import DirectChatMessage
import rest_framework.serializers as serializers
from user_profile.serializers import PublicProfileSerializer
from authentication.models import User
from errors.error_repository import get_error_serialized, OBJECT_NOT_FOUND
class DirectChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectChatMessage
        fields = ['id', 'text', '_from', '_to']

class DirectChatViewSerializer(serializers.ModelSerializer):
    is_sender = serializers.SerializerMethodField()
    _from = serializers.SerializerMethodField(method_name="get_from")
    _to = serializers.SerializerMethodField(method_name="get_to")
    def get_from(self, instance):
        return PublicProfileSerializer(instance=instance._from).data
    def get_to(self, instance):
        return PublicProfileSerializer(instance=instance._to).data
    def get_is_sender(self, instance):
        sender_username = self.context.get("target_username", None)
        if(sender_username is None):
            return False
        return self.instance._from.username == sender_username
    class Meta:
        model = DirectChatMessage
        fields = ['id', 'text', '_from', '_to', 'date', 'seen', 'is_sender']
class ChatUsersSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    def get_user(self, instance):
        return PublicProfileSerializer(instance=instance).data
    def get_last_message(self, instance):
        sender_username = self.context.get("target_username", None)
        sender = User.objects.filter(username=sender_username).first()
        if(sender is None):
            return {"error" : get_error_serialized(OBJECT_NOT_FOUND, detail="Sender not found.")}
        records = list(DirectChatMessage.objects.filter(_from=instance, _to=sender))
        records += list(DirectChatMessage.objects.filter(_to=instance, _from= sender))
        records = sorted(records, key=lambda x: x.date)[::-1]
        return DirectChatViewSerializer(
                        instance=records[0], 
                        context={"target_username" : self.context.get("target_username", None)
                    }).data
    class Meta:
        model = User
        fields = ['user', 'last_message']