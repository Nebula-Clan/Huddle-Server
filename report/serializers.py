from rest_framework import serializers
from authentication.models import User
from user_profile.serializers import PublicProfileSerializer
from .models import *

class ReportSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    reported_for = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_reported_for(self, instance):
        subjects_id = PostReport.objects.filter(report = instance).values_list('subject', flat = True)
        subjects = ReportSubject.objects.filter(id__in = subjects_id)
        return ReportSubjectSerializer(subjects, many = True).data

    def get_user(self, instance):
        return PublicProfileSerializer(instance.user).data

    def get_description(self, instance):
        if instance.description is None:
            return ""
        return instance.description

    class Meta:
        model = Reports
        fields = ['id', 'post', 'user', 'reported_for', 'description']
    
class ReportSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSubject
        fields = ['text']