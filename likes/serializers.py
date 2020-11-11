from rest_framework import serializers
from posts.serializer import PostSerializer
from user_profile.serializers import PublicProfileSerializer
from comment.serializers import DisplayCommentSerializer
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
class UserLikesSerializer(serializers.ModelSerializer):
    post_likes = serializers.SerializerMethodField()
    comment_likes = serializers.SerializerMethodField()
    def get_post_likes(self, instance):
        post_likes = PostLike.objects.filter(user=instance.id)
        posts = [like.post for like in post_likes]
        return PostSerializer(posts, many=True).data
    def get_comment_likes(self, instance):
        comment_likes = CommentLike.objects.filter(user=instance.id)
        comments = [like.post for like in comment_likes]
        return DisplayCommentSerializer(comments, context=self.context, many=True).data
    class Meta:
        model = User
        fields = ['username', 'post_likes', 'comment_likes']
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post', 'user']
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment', 'user']