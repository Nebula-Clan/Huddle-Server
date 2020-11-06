from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^post/get', get_post_comments),
    url(r'^post/submit', submit_post_comment),
    url(r'^reply/submit', submit_reply_comment),
    url(r'^reply/get', get_reply_comments),
    url(r'^profile/get', get_user_comments)
]