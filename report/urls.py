from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^send_report', send_report),
    url(r'^reports_number', reports_number),
    url(r'^users_reported', users_reported),
    url(r'^post_reports', post_reports),
]