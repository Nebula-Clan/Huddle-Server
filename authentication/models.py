from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
# Create your models here.
def get_user_directory(instance, filename):
    return f'uploads/userprofile/{instance.username}/{filename}'
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to=get_user_directory, null=True)
    biology = models.TextField(max_length=200, default='', blank=True)
    birth_date = models.DateField(default=timezone.now)
    pass