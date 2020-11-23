from .models import Category
from rest_framework import serializers
class CategorySerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_title(self, instance):
        return instance.get_name_display()

    def get_id(self, instance):
        return instance.name
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'icon']