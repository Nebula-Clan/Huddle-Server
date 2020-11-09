from django.db import models
from authentication.models import User
from posts.models import Post
# Create your models here.

def get_community_pics_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/community_pics/{instance.id}.{ext}'

def get_community_bannerpics_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/community_bannerpics/{instance.id}.{ext}'

class Community(models.Model):
    name = models.CharField(max_length = 100)
    users = models.ManyToManyField(User, related_name = 'in_community')
    admin = models.ForeignKey(User, related_name = 'admin_community', on_delete = models.CASCADE)
    about = models.CharField(max_length = 750)
    date_created = models.DateTimeField(auto_now = True)
    picture = models.ImageField(upload_to = get_community_pics_directory)
    banner_picture = models.ImageField(upload_to = get_community_bannerpics_directory)
