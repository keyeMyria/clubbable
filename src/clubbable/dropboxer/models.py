from django.contrib.auth.models import User
from django.db import models
from club.models import GetOrNoneManager


class DropboxUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True)

    objects = GetOrNoneManager()
