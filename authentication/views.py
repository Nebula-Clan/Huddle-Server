from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
# Create your views here.
@api_view(['GET'])
def login_view(request):
    if(request.method == 'GET'):
        return JsonResponse({'Yo' : 'nigga'})