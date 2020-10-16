from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login_view),
    url(r'^something', views.something),
    url(r'^refresh', views.refresh_token_view),
    url(r'^register', views.register_view),
]