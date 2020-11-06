from django.db import models
from authentication.models import User
from posts.models import Post
from comment.models import Comment
# Create your models here.


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = user = models.ForeignKey(User, on_delete=models.CASCADE)