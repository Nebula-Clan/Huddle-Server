from rest_framework import serializers

class ErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = error
        fields = ['code', 'message']