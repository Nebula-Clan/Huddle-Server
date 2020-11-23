from rest_framework import serializers
from .models import *
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'text']
class HashtagListSerializer(serializers.Serializer):
    hashtags = serializers.ListField(child=serializers.CharField())
class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ['post', 'hashtag']