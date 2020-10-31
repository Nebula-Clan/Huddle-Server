from django.db import models
from posts.models import Post
from authentication.models import User
# Create your models here.

class PostComment(models.Model):
    MAXIMUM_COMMENT_LENGTH = 100
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=MAXIMUM_COMMENT_LENGTH, null=False, blank=False, default="Comment!")
    