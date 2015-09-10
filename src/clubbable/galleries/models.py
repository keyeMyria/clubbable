from itertools import chain
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from club.models import Meeting, Member, Guest


fs = FileSystemStorage(location=settings.UPLOAD_ROOT)


class Gallery(models.Model):
    name = models.CharField(max_length=255)
    # poster_image is the image for this gallery in the list of galleries
    poster_image = models.ForeignKey('Image', null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    def __unicode__(self):
        return '%s' % self.name


class Image(models.Model):
    gallery = models.ForeignKey(Gallery)
    description = models.CharField(max_length=255, blank=True)
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    members = models.ManyToManyField(Member)
    guests = models.ManyToManyField(Guest)
    creator = models.ForeignKey(Member, null=True)

    original = models.ImageField(upload_to='image/%Y/%m/', storage=fs)
    display = ImageSpecField(source='original',
                             processors=[ResizeToFit(600, 370)],
                             format='JPEG',
                             options={'quality': 90})
    thumbnail = ImageSpecField(source='original',
                               processors=[ResizeToFill(100, 75)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        if self.description:
            return '%s' % self.description
        people = ', '.join(('%s' % p
                            for p in chain(self.members, self.guests)))
        if self.meeting:
            return '%s: %s' % (self.meeting, people)
        return people
