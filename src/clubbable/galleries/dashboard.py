# -*- coding: utf-8 -*-
"""
Adds tiles to the dashboard
"""
from __future__ import unicode_literals
from django.template import loader
from galleries.models import Gallery


def get_tiles(request):
    """
    Return HTML tiles for the dashboard
    """
    tiles = []
    for gallery in Gallery.objects.all():
        template = loader.get_template('galleries/gallery_tile.html')
        tiles.append(template.render({'gallery': gallery}))
    return tiles
