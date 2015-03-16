# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Notice(models.Model):
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


class MessageTemplate(models.Model):
    """
    A MessageTemplate is used to send e-mails to members.

    It may have one or more Notices attached. Subject and body are templates
    that are populated at send time from a context with the member's name, and
    the notice's description.
    """
    subject = models.CharField(max_length=255)
    text = models.TextField()
    html = models.TextField(blank=True)
    notices = models.ManyToManyField(Notice)

    def __str__(self):
        return self.subject

    def __unicode__(self):
        return self.subject

    def get_subject_or_notices(self):
        if self.notices:
            return ', '.join(['%s' % n for n in self.notices])
        return self.subject
