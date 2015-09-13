# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from club.models import GetOrNoneManager


class DropboxUser(models.Model):
    user = models.OneToOneField(User)  # Only one account per user
    access_token = models.CharField(max_length=255, blank=True)

    objects = GetOrNoneManager()
