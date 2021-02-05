from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search_in_users', views.search_in_users),
    url(r'^search_in_posts', views.search_in_posts),
    url(r'^search_in_categories', views.search_in_categories),
    url(r'^search_in_communities', views.search_in_communities),
]

