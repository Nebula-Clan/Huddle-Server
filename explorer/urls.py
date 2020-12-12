from . import views
from django.conf.urls import url

urlpatterns = [
    url(r"^get_posts", views.get_posts)

]