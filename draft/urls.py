from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^create", views.create),
    url(r"^get_drafts", views.get_drafts),
    url(r"^get_draft", views.get_draft),
    url(r"^update_draft", views.update_draft),
    url(r"^delete_draft", views.delete_draft)
]