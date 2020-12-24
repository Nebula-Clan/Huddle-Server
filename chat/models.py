from django.db import models
from authentication.models import User
from huddle.utils import random_string
import uuid
# Create your models here.

class DirectChatMessage(models.Model):
    TEXT_MAX_LENGTH = 1000
    text = models.TextField(max_length=TEXT_MAX_LENGTH)
    _from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    _to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    
class LastSeen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class Clients(models.Model):
    channel_name = models.TextField(max_length=1000)
    username = models.ForeignKey(User, on_delete=models.CASCADE)


def get_chat_dir(instance, filename):
    return f'uploads/chats/{instance.chat._from}/{instance.chat._to}/{random_string(50)}_{filename}'

class ChatFiles(models.Model):
    is_image = models.BooleanField()
    chat = models.ForeignKey(DirectChatMessage, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_chat_dir)