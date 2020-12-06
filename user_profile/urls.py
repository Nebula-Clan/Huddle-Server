
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^public', views.get_public_profile),
    url(r'^update_profile', views.update_profile)
]
