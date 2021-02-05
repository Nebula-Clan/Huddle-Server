from . import views
from django.conf.urls import url

urlpatterns = [
    url(r"^get_posts", views.get_posts),
    url(r"^posts_by_hashtag", views.posts_by_hashtag)

]