from .models import Category
from rest_framework import serializers
class CategorySerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField()
    PK = serializers.SerializerMethodField()

    def get_display_name(self, instance):
        return instance.get_name_display()

    def get_PK(self, instance):
        return instance.name
    
    class Meta:
        model = Category
        fields = ['PK', 'display_name', 'icon']