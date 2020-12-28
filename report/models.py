from django.db import models
from authentication.models import User
from posts.models import Post

report_subjects = [
        (1, 'insult'),
        (2, 'aggressive'),
        (3, 'resist'),
    ]

class Reports(models.Model):
    user = models.ForeignKey('authentication.User', on_delete = models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete = models.CASCADE)
    description = models.CharField(max_length = 500, null = True)

class ReportSubject(models.Model):
    text = models.CharField(choices = report_subjects, max_length = 20, null = False)

class PostReport(models.Model):
    subject = models.ForeignKey('report.ReportSubject', on_delete = models.CASCADE)
    report = models.ForeignKey('report.Reports', on_delete = models.CASCADE)

def update_report_subjects():
    for sub in report_subjects:
        if ReportSubject.objects.filter(text = sub[1]).exists():
            continue
        ReportSubject.objects.create(text = sub[1])