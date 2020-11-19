from rest_framework.permissions import AllowAny
from .models import Category
from rest_framework.decorators import api_view, permission_classes
from .serializers import CategorySerializer
from django.http.response import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(categories, many = True)
    return JsonResponse({"categories" : serialized_categories.data})