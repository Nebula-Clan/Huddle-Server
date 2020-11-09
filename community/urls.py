from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_community', views.create_community),
    url(r'^get_community', views.get_community),
    url(r'^join_community', views.join_community),
    url(r'^leave_community', views.leave_community),
    url(r'^community_members', views.get_community_members),
    url(r'^community_posts', views.get_community_posts)

    # url(r'^blah', views.blah)
]