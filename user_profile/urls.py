from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^public', views.get_public_profile),
    url(r'^image/set', views.set_profile_image)
]
