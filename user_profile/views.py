from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from http import HTTPStatus
from authentication.models import User
from .serializers import PublicProfileSerializer
@api_view(['GET'])
def get_public_profile(request):
    try:
        username = request.data.get('username')
    except:
        return JsonResponse({'message': "Bad request!"}, HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({"message": "User not found!"}, HTTPStatus.NOT_FOUND)
    public_profile = PublicProfileSerializer(user)
    return JsonResponse(data=public_profile.data, status=HTTPStatus.OK)

@api_view(['PUT'])
def set_profile_image(request):
    try:
        image = request.FILES['image']
        username = request.data.get('username')
    except:
        return JsonResponse({'message': "Bad request!"}, HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({"message": "User not found!"}, HTTPStatus.NOT_FOUND)
    user.profile_picture = image
    user.save()
    return JsonResponse(data={"message": "Image changed successfully!"}, status=HTTPStatus.OK)
    return JsonResponse({'message': "Something wrong!"}, HTTPStatus.BAD_REQUEST)