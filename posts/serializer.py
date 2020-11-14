from .models import Post
from .models import Content
from rest_framework import serializers
from authentication.models import User
from likes.models import PostLike
from user_profile.serializers import PublicProfileSerializer
from hashtag.models import Hashtag, PostHashtag
from hashtag.serializers import HashtagSerializer
class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    post_content = serializers.SerializerMethodField()
    likes_number = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()

    def get_hashtags(self, instance):
        records = PostHashtag.objects.filter(post=instance.id)
        records = [record.hashtag for record in records]
        return HashtagSerializer(records, many=True).data
    def get_likes_number(self, instance):
        return PostLike.objects.filter(post = instance.id).count()
    
    def get_author(self, instance):
        author_depth = self.context.get('author_depth', True)
        if author_depth:
            return PublicProfileSerializer(User.objects.filter(id = instance.author_id).first()).data
        return instance.author_id
    
    def get_post_content(self, instance):
        content_depth = self.context.get('content_depth', True)
        if content_depth:
            return ContentSerializer(Content.objects.filter(id = instance.post_content_id).first()).data
        return instance.post_content_id
    
    def get_is_liked(self, instance):
        viewer = self.context.get('viewer')
        if(not viewer):
            return False
        viewer_user = User.objects.filter(username=viewer).first()
        if(not viewer_user):
            return False
        return PostLike.objects.filter(user=viewer_user.id, post=instance.id).exists()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'header_image', 'post_content',
                    'category', 'date_created', 'author', 'is_liked', 'likes_number', 'hashtags']

class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Content
        fields = ['id', 'content_type', 'content_text']
