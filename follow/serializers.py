from .models import UserFollowing
from rest_framework import serializers

class UserFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ['user', 'following_user']