# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class DropboxUser(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255, blank=True)
    galleries_folder = models.CharField(max_length=255, blank=True)
    docs_folder = models.CharField(max_length=255, blank=True)
    mdb_folder = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s' % self.username

    def __unicode__(self):
        return '%s' % self.username
