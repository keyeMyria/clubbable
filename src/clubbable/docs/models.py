# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return '%s' % self.name


class Document(models.Model):
    """
    A Notice is usually a PDF document that is sent to members.
    """
    folder = models.ForeignKey(Folder)
    description = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=50)
    data = models.BinaryField()

    def __str__(self):
        return self.description or self.filename

    def __unicode__(self):
        return self.description or self.filename
