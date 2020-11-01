from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^get', get_likes),
    url(r'^submit', submit_like),
    url(r'^profile/get', get_user_likes)
]