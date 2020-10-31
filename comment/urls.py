from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^post/get', get_post_comments),
    url(r'^submit', submit_comment),
    url(r'^profile/get', get_user_comments)
]