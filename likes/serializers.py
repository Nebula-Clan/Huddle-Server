from rest_framework import serializers
from .models import Like
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post_id', 'user_id']
        unique_together = ('post_id', 'user_id')