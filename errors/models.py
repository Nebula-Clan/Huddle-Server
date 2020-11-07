from django.db import models

class error(models.Model):
    code = models.IntegerField()
    message = models.CharField(max_length = 100)
