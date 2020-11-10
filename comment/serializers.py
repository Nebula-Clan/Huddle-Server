from rest_framework import serializers
from .models import *
from user_profile.serializers import PublicProfileSerializer
from posts.serializer import PostSerializer
from likes.models import CommentLike
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content']

class DisplayCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    total_replies_count = serializers.SerializerMethodField()
    total_likes_count = serializers.SerializerMethodField()
    def get_total_likes_count(self, instance):
        return CommentLike.objects.filter(comment=instance.id).count()
    def get_total_replies_count(self, instance):
        replies = CommentReply.objects.filter(reply_to=instance.id)
        return len(replies)
    def get_is_liked(self, instance):
        viewer = self.context.get('viewer')
        if(not viewer):
            return False
        viewer_user = User.objects.filter(username=viewer).first()
        if(not viewer_user):
            return False
        return CommentLike.objects.filter(user=viewer_user.id, comment=instance.id).exists()
    def get_author(self, obj):
        return PublicProfileSerializer(obj.author).data
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'total_replies_count', 'is_liked', 'total_likes_count']

class RepliedCommentSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    def get_comment(self, instance):
        return DisplayCommentSerializer(instance, context=self.context).data
    def get_replies(self, instance):
        depth = int(self.context.get('depth'))
        length = int(self.context.get('max_len'))
        startIdx = int(self.context.get('start_index'))
        viewer = self.context.get('viewer')
        if(depth is None or length is None or startIdx is None or depth <= 0):
            return []
        replies = CommentReply.objects.filter(reply_to=instance.id)
        replies = [item.reply for item in list(replies)]
        if(startIdx is None or startIdx >= len(replies)):
            return []
        replies = replies[startIdx: startIdx + length]
        result = []
        for reply in replies:
            if(reply is None):
                continue
            result.append(RepliedCommentSerializer(instance=reply, context={'depth' : depth - 1, 'start_index' : startIdx , 'max_len' : length, 'viewer' : viewer}).data)
        return result
    
    class Meta:
        model = Comment
        fields = ['comment', 'replies']
        
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
    def get_comment_replies(self, instance):
        result = []
        user_comments = Comment.objects.filter(author=instance.id)
        user_comments = list(user_comments)
        for comment in user_comments:
            replied_to = CommentReply.objects.filter(reply=comment.id).first()
            if(replied_to is None):
                continue
            replied_to = replied_to.reply_to
            data = {
                    'user_comment': DisplayCommentSerializer(comment, context={'depth' : '0', 'max_len': '0', 'viewer' : self.context.get('viewer')}).data , 
                    'parent_comment': RepliedCommentSerializer(replied_to, context={'depth' : '0', 'max_len': '0', 'viewer' : self.context.get('viewer'), 'start_index': 0}).data
                }
            result.append(data)
        return result


    def get_post_replies(self, instance):
        result = []
        user_comments = Comment.objects.filter(author=instance.id)
        user_comments = list(user_comments)
        for comment in user_comments:
            replied_to = PostReply.objects.filter(reply=comment.id).first()
            if(replied_to is None):
                continue
            post = replied_to.post
            data = {
                    'user_comment': DisplayCommentSerializer(comment, context={'depth' : '0', 'max_len': '0'}).data , 
                    'post': PostSerializer(post, context={'depth' : '0', 'max_len': '0'}).data
                }
            result.append(data)
        return result
    class Meta:
        model = User
        fields = ['username', 'post_replies', 'comment_replies']