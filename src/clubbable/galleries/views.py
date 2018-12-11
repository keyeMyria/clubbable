from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from galleries.models import Gallery, Image


class ImageList(ListView):
    context_object_name = 'images'

    def get_queryset(self):
        gallery = get_object_or_404(Gallery, pk=self.args[0])
        return Image.objects.filter(gallery=gallery)
