from posts.models import Post
from authentication.models import User
from user_profile.serializers import PublicProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from django.http.response import JsonResponse
from errors.error_repository import get_error_serialized
from rest_framework import status
from .serializers import ReportSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_report(request):
    user = request.user

    post_id = request.data.get('post_id', None)
    subjects = request.data.get('subjects', None)
    description = request.data.get('description', None)
    
    if subjects is None or len(subjects) == 0 or post_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'post_id, subjects fields is required').data}, status = status.HTTP_400_BAD_REQUEST)
    
    subjects_obj = []
    for subject in subjects:
        report_subject = ReportSubject.objects.filter(text = subject).first()
        if report_subject is None:
            return JsonResponse({"error" : get_error_serialized(100, f'This subject is not allowed: \'{subject}\'').data}, status = status.HTTP_400_BAD_REQUEST)
        subjects_obj.append(report_subject)
    
    report_post = Post.objects.filter(id = post_id).first()
    if report_post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    if Reports.objects.filter(user = user, post = report_post).exists():
        return JsonResponse({"error" : get_error_serialized(115).data}, status = status.HTTP_406_NOT_ACCEPTABLE)
    
    created_report = Reports.objects.create(user = user, post = report_post, description = description)
    for subject in subjects_obj:
        PostReport.objects.create(subject = subject, report = created_report)

    report_post.reports_number += 1

    return JsonResponse({"message" : f"report to post with id:{post_id} sended"})

@api_view(['GET'])
def post_reports(request):
    post_id = request.query_params.get('post_id', None)
    if post_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'post_id field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    all_reports = Reports.objects.filter(post = post)

    return JsonResponse({"reports" : ReportSerializer(all_reports, many = True).data})


@api_view(['GET'])
@permission_classes([AllowAny])
def reports_number(request):
    post_id = request.query_params.get('post_id', None)
    if post_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'post_id field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    reports_number = Reports.objects.filter(post = post).count()

    return JsonResponse({"reports_number" : reports_number})


@api_view(['GET'])
@permission_classes([AllowAny])
def users_reported(request):
    post_id = request.query_params.get('post_id', None)
    if post_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'post_id field is required').data}, status = status.HTTP_400_BAD_REQUEST)

    post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found').data}, status = status.HTTP_404_NOT_FOUND)
    
    users_reported_id = Reports.objects.filter(post = post).values_list('user', flat = True)
    users_reported = [User.objects.filter(id = user_id).first() for user_id in users_reported_id]
    users_serialized = PublicProfileSerializer(users_reported, many = True)
    return JsonResponse({"users_reported" : users_serialized.data})