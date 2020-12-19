from django.db import models
from authentication.models import User
from posts.models import Post

class Reports(models.Model):
    user = models.ForeignKey('authentication.User', on_delete = models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete = models.CASCADE)