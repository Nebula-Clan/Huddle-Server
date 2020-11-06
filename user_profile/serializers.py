from rest_framework import serializers
from authentication.models import User
class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 
                    'last_name', 'biology', 'profile_picture', 'banner_picture']