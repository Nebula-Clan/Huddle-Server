from rest_framework import serializers
from .models import *
from user_profile.serializers import PublicProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content']

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
        fields = ['id', 'author', 'content', 'total_replies', 'retrieved_replies']
        
class PostReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReply
        fields = ['post', 'reply']
class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model  = CommentReply
        fields = ['reply', 'reply_to']