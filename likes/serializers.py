from rest_framework import serializers
from user_profile.serializers import PublicProfileSerializer
from .models import *
from posts.models import Post 
from comment.models import Comment
class ViewPostLikesSerializer(serializers.ModelSerializer):
    liked_users = serializers.SerializerMethodField()
    def get_liked_users(self, obj):
        likes = PostLike.objects.filter(post= obj.id)
        return [PublicProfileSerializer(like.user).data for like in list(likes)]
    class Meta:
        model = Post
        fields = ['id', 'liked_users']
class ViewCommentLikesSerializer(serializers.ModelSerializer):
    liked_users = serializers.SerializerMethodField()
    def get_liked_users(self, obj):
        likes = CommentLike.objects.filter(comment= obj.id)
        return [PublicProfileSerializer(like.user).data for like in list(likes)]
    class Meta:
        model = Comment
        fields = ['id', 'liked_users']
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post', 'user']
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment', 'user']