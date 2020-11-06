from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^post', post_likes),
    url(r'^comment', comment_likes),
    url(r'^profile', get_user_likes),
    
]