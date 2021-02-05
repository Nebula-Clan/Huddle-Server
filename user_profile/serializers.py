from rest_framework import serializers
from authentication.models import User
from follow.models import UserFollowing

class PublicProfileSerializer(serializers.ModelSerializer):

    followed_by_viewer = serializers.SerializerMethodField()
    
    def get_followed_by_viewer(self, instance):
        viewer_id = self.context.get('viewer_id', None)
        if viewer_id is None:
            return False
        
        return UserFollowing.objects.filter(user = viewer_id, following_user = instance.id).exists()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 
                    'last_name', 'biology', 'profile_picture', 'banner_picture', 'followed_by_viewer']