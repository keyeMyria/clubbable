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

    @property
    def doc_type(self):
        """
        Returns a doc type that can be used for selecting an icon based on
        file extension.
        """
        doc_types = {
            'pdf': 'pdf',
            'doc': 'word',
            'docx': 'word',
            'xls': 'excel',
            'xlsx': 'excel',
            'ppt': 'powerpoint',
            'pptx': 'powerpoint',
            'zip': 'archive',
        }
        ext = self.filename.split('.')[-1]
        return doc_types.get(ext, 'pdf')
