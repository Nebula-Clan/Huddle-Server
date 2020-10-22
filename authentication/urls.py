from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.login_view),
    url(r'^user', views.user),
    url(r'^refresh', views.refresh_token_view),
<<<<<<< HEAD
    url(r'^register', views.register_view),
]
=======
]
>>>>>>> c9efe8d6759daebcd068a3fd05df486c293b8580
