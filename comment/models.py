from django.db import models
from posts.models import Post
from authentication.models import User
from django.utils.timezone import now
# Create your models here.

class Comment(models.Model):
    MAXIMUM_COMMENT_LENGTH = 100
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=MAXIMUM_COMMENT_LENGTH, null=False, blank=False, default="Comment!")
    create_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)

class CommentReply(models.Model):
    reply_to = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+")
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+")

class PostReply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+")