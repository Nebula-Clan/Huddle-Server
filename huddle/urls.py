"""huddle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import authentication.urls as auth_urls
import likes.urls as likes_urls
import user_profile.urls as profile_urls
import posts.urls as posts_urls
import search.urls as search_urls
import comment.urls as commnt_urls
import community.urls as community_urls
import hashtag.urls as hashtag_urls
import category.urls as category_urls
import draft.urls as draft_urls
from django.conf.urls import url
from . import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/auth/', include(auth_urls)),
    url(r'^api/likes/', include(likes_urls)),
    url(r'^api/comments/', include(commnt_urls)),
    url(r'^api/profile/', include(profile_urls)),
    url(r'^api/posts/', include(posts_urls)),
    url(r'^api/search/', include(search_urls)),
    url(r'^api/community/', include(community_urls)),
    url(r'^api/hashtag/', include(hashtag_urls)),
    url(r'^api/category/', include(category_urls)),
    url(r'^api/draft/', include(draft_urls)),
]

if(settings.DEBUG):
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)