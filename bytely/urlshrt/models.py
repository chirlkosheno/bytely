from django.db import models


class Url(models.Model):
    short_url = models.CharField(max_length=128, unique=True)
    full_url = models.TextField(max_length=1024)
