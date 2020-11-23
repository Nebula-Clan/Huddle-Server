from rest_framework import serializers
from .models import error

class ErrorSerializer(serializers.ModelSerializer):

    detail = serializers.SerializerMethodField()

    def get_detail(self, instance):
        return self.context.get('detail', '')

    class Meta:
        model = error
        fields = ['code', 'message', 'detail']    