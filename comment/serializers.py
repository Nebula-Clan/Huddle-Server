from rest_framework import serializers
from .models import *
from user_profile.serializers import PublicProfileSerializer
from posts.serializer import PostSerializer
from likes.models import CommentLike
class CommentSerializer(serializers.ModelSerializer):
    liked_by_viewer = serializers.SerializerMethodField()
    def get_liked_by_viewer(self, instance):
        viewer = self.context.get('viewer')
        if(not viewer):
            return False
        viewer_user = User.objects.filter(username=viewer).first()
        if(not viewer_user):
            return False
        return CommentLike.objects.filter(user=viewer_user.id, comment=instance.id).exists()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'liked_by_viewer']

class DisplayCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    def get_author(self, obj):
        return PublicProfileSerializer(obj.author).data
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_profile', 'content']

class PostCommentsSerializer(serializers.ModelSerializer):
    retrieved_replies = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    total_replies = serializers.SerializerMethodField()
    liked_by_viewer = serializers.SerializerMethodField()
    def get_liked_by_viewer(self, instance):
        viewer = self.context.get('viewer')
        if(not viewer):
            return False
        viewer_user = User.objects.filter(username=viewer).first()
        if(not viewer_user):
            return False
        return CommentLike.objects.filter(user=viewer_user.id, comment=instance.id).exists()
    def get_total_replies(self, obj):
        replies = CommentReply.objects.filter(reply_to=obj.id)
        return len(list(replies))
    def get_author(self, obj):
        return PublicProfileSerializer(obj.author).data
    def get_retrieved_replies(self, obj):
        depth = int(self.context.get('depth'))
        length = int(self.context.get('max_len'))
        if(depth <= 0):
            return []
        replies = CommentReply.objects.filter(reply_to=obj.id)
        replies = [item.reply for item in list(replies)]
        replies = replies[:length]
        result = []
        for reply in replies:
            if(reply is None):
                continue
            result.append(PostCommentsSerializer(instance=reply, context={'depth' : depth - 1, 'max_len' : length}).data)
        return result
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'total_replies', 'liked_by_viewer', 'retrieved_replies']
        
class PostReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReply
        fields = ['post', 'reply']
class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model  = CommentReply
        fields = ['reply', 'reply_to']

class UserCommentSerializer(serializers.ModelSerializer):
    post_replies = serializers.SerializerMethodField()
    comment_replies = serializers.SerializerMethodField()
    def get_comment_replies(self, obj):
        result = []
        user_comments = Comment.objects.filter(author=obj.id)
        user_comments = list(user_comments)
        for comment in user_comments:
            replied_to = CommentReply.objects.filter(reply=comment.id).first()
            if(replied_to is None):
                continue
            replied_to = replied_to.reply_to
            data = {
                    'user_comment': CommentSerializer(comment, context={'depth' : '0', 'max_len': '0', 'viewer' : self.context.get('viewer')}).data , 
                    'parent_comment': PostCommentsSerializer(replied_to, context={'depth' : '0', 'max_len': '0', 'viewer' : self.context.get('viewer')}).data
                }
            result.append(data)
        return result


    def get_post_replies(self, obj):
        result = []
        user_comments = Comment.objects.filter(author=obj.id)
        user_comments = list(user_comments)
        for comment in user_comments:
            replied_to = PostReply.objects.filter(reply=comment.id).first()
            if(replied_to is None):
                continue
            post = replied_to.post
            data = {
                    'user_comment': CommentSerializer(comment, context={'depth' : '0', 'max_len': '0'}).data , 
                    'post': PostSerializer(post, context={'depth' : '0', 'max_len': '0'}).data
                }
            result.append(data)
        return result
    class Meta:
        model = User
        fields = ['username', 'post_replies', 'comment_replies']