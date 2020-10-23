from django.db import models
from authentication.models import User
# Create your models here.


class Like(models.Model):
    post_id = models.IntegerField(default=-1) #must be foreign Key! TODO
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

