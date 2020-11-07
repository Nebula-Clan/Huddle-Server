from .models import Post
from .models import Content
from rest_framework import serializers
from authentication.models import User
from likes.models import PostLike
class PostSerializer(serializers.ModelSerializer):
    liked_by_viewer = serializers.SerializerMethodField()
    def get_liked_by_viewer(self, instance):
        viewer = self.context.get('viewer')
        if(not viewer):
            return False
        viewer_user = User.objects.filter(username=viewer).first()
        if(not viewer_user):
            return False
        return PostLike.objects.filter(user=viewer_user.id, post=instance.id).exists()
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'header_image', 'post_content', 'category', 'date_created', 'author', 'liked_by_viewer']


class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Content
        fields = ['id', 'content_type', 'content_text']
