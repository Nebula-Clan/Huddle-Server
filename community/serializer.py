from .models import Community
from posts.models import Post
from authentication.models import User
from posts.serializer import PostSerializer
from user_profile.serializers import PublicProfileSerializer
from rest_framework import serializers

class CommunityCompleteSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()
    members_number = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_posts(self, instance):
        posts = list(Post.objects.filter(community = instance.id))
        posts.reverse()
        return PostSerializer(posts, many = True).data

    def get_members(self, instance):
        users = instance.users.all()
        return PublicProfileSerializer(users, many = True).data
    
    def get_members_number(self, instance):
        return instance.users.count()
    # def get_admin(self, instance):
    #     admin = User.objects.filter(id = instance.admin).first()
    #     return PublicProfileSerializer(admin)

    class Meta:
        model = Community
        fields = ['id', 'name', 'about', 'date_created', 'picture', 'banner_picture', 'members_number', 'members', 'posts']

class CommunitySmallSerializer(serializers.ModelSerializer):

    members_number = serializers.SerializerMethodField()

    def get_members_number(self, instance):
        return instance.users.count()
    class Meta:
        model = Community
        fields = ['id', 'name', 'about', 'date_created', 'picture', 'banner_picture', 'members_number']