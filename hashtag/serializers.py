from rest_framework import serializers
from .models import *
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'text']
class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ['post', 'hashtag']