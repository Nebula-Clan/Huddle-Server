from rest_framework import serializers
from .models import PostComment
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['post', 'author', 'content']