from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^similarity', get_similar_to),
    url(r'^posts', get_hashtag_posts),
]