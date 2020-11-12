from django.db import models
from django.conf import settings
from posts.models import Post
# Create your models here.
class Hashtag(models.Model):
    text = models.TextField(max_length=settings.HASHTAG_MAXIMUM_LENGTH, unique=True)

class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)


