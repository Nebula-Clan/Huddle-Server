from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_categories', views.get_categories)
]