from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^post/get', get_post_likes),
    url(r'^post/submit', submit_post_likes),
    url(r'^comment/get', get_comment_likes),
    url(r'^comment/submit', submit_comment_likes),
    
]