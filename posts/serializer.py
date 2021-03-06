from .models import Post
from .models import Content
from rest_framework import serializers
from authentication.models import User
from likes.models import PostLike
from user_profile.serializers import PublicProfileSerializer
from hashtag.models import Hashtag, PostHashtag
from hashtag.serializers import HashtagSerializer
from category.models import Category
from category.serializers import CategorySerializer
from report.models import Reports
from huddle.settings import POST_MAXIMUM_REPORT

class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    post_content = serializers.SerializerMethodField()
    likes_number = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    header_image = serializers.SerializerMethodField()
    is_reported = serializers.SerializerMethodField()

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

    def get_category(self, instance):
        if instance.category is None:
            return None
        category_id = instance.category_id
        return CategorySerializer(Category.objects.get(name = category_id)).data
    
    def get_header_image(self, instance):
        if "undefined" in str(instance.header_image) or "null" in str(instance.header_image) or str(instance.header_image) == "":
            return None
        return str(instance.header_image)

    def get_is_reported(self, instance):
        if instance.reports_number >= POST_MAXIMUM_REPORT:
            return True
        return False
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'header_image', 'post_content',
                    'category', 'date_created', 'author', 'is_liked', 'likes_number', 'hashtags', 'is_reported']

class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Content
        fields = ['id', 'content_type', 'content_text']
