from django.db import models
from authentication.models import User
from posts.models import Post
# Create your models here.


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

