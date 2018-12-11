from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name


class Document(models.Model):
    folder = models.ForeignKey(Folder, models.PROTECT)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='doc/%Y/%m/')

    def __str__(self):
        return self.description or self.filename

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    @property
    def doc_type(self):
        """
        Returns a doc type that can be used for selecting an icon based
        on file extension.
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
        ext = self.file.name.split('.')[-1]
        return doc_types.get(ext, 'pdf')
