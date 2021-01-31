from django.conf.urls import url
from . import views, community_settingviews

urlpatterns = [
    url(r'^create_community', views.create_community),
    url(r'^get_community', views.get_community),
    url(r'^join_community', views.join_community),
    url(r'^leave_community', views.leave_community),
    url(r'^community_members', views.get_community_members),
    url(r'^community_posts', views.get_community_posts),
    url(r'^user_communities', views.user_communities),
    url(r'^update_community', community_settingviews.update_community),
    url(r'^delete_community', community_settingviews.delete_community),
    url(r'^remove_user', community_settingviews.remove_user),
    url(r'^disable_user', community_settingviews.disable_user),
    url(r'^delete_post', community_settingviews.delete_post),
    url(r'^is_admin', community_settingviews.is_admin),
    url(r'^enable_user', community_settingviews.enable_user)
]