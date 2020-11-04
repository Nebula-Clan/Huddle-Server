from .models import Post
from .models import Content
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'header_image', 'post_content', 'category', 'date_created', 'author']


class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Content
        fields = ['id', 'content_type', 'content_text']
