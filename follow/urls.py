from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^send_follow', views.send_follow),
    url(r'^user_followings', views.user_followings),
    url(r'^user_followers', views.user_followers),
    url(r'^send_unfollow', views.send_unfollow),
]