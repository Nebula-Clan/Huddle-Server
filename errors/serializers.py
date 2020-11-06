from rest_framework import serializers
from .models import error

class ErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = error
        fields = ['code', 'message']