from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login', views.login_view),
    url(r'^user', views.user),
    url(r'^refresh', views.refresh_token_view),
]
