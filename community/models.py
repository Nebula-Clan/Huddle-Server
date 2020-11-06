from django.db import models
from authentication.models import User
from posts.models import Post
# Create your models here.

def get_community_images_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/community_images/{instance.id}.{ext}'

def get_community_backimages_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/community_backimages/{instance.id}.{ext}'

class Community(models.Model):
    name = models.CharField(max_length = 100)
    users = models.ManyToManyField('authentication.User', related_name = 'in_community')
    admin = models.ForeignKey('authentication.User', related_name = 'admin_community', on_delete = models.CASCADE)
    about = models.CharField(max_length = 750)
    date_created = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to = get_community_images_directory)
    back_image = models.ImageField(upload_to = get_community_backimages_directory)
