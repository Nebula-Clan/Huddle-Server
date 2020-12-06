
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^public', views.get_public_profile),
    url(r'^image/set', views.set_profile_image),
    url(r'^update_picture', views.update_picture),
    url(r'^update_username', views.update_username),
    url(r'^update_name', views.update_name),
    url(r'^update_password', views.update_password)
]
