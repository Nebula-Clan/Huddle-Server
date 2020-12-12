from django.db import models
from authentication.models import User
# Create your models here.

class DirectChatMessage(models.Model):
    TEXT_MAX_LENGTH = 1000
    text = models.TextField(max_length=TEXT_MAX_LENGTH)
    _from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    _to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
class LastSeen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class Clients(models.Model):
    channel_name = models.TextField(max_length=1000)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    