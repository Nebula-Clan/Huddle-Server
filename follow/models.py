from django.db import models
from authentication.models import User

class UserFollowing(models.Model):
    user = models.ForeignKey('authentication.User', related_name = 'followings', on_delete = models.CASCADE)
    following_user = models.ForeignKey('authentication.User', related_name = 'followers', on_delete = models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add = True) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['user','following_user'],  name = "unique_followers")
        ]