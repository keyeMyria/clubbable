# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Document(models.Model):
    """
    A Notice is usually a PDF document that is sent to members.
    """
    description = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=50)
    data = models.BinaryField()

    def __str__(self):
        return self.description or self.filename

    def __unicode__(self):
        return self.description or self.filename
