from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_post', views.create_post),
    url(r'^delete_post', views.delete_post),
    url(r'^update_post', views.update_post),
    url(r'^get_user_posts', views.get_user_posts),
    url(r'^get_short_post', views.get_short_post),
    url(r'^get_full_post', views.get_full_post),
    url(r'^get_content', views.get_content),
]
# if settings.DEBUG:
#     urlpattern += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
