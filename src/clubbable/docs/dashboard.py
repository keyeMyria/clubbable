# -*- coding: utf-8 -*-
"""
Adds a tile to the dashboard
"""
from __future__ import unicode_literals
from django.template import loader
from docs.models import Folder


def get_tiles(request):
    """
    Return HTML tiles for the dashboard, or empty list if user is not staff
    """
    tiles = []
    for folder in Folder.objects.all():
        template = loader.get_template('docs/folder_tile.html')
        tiles.append(template.render({'folder': folder}))
    return tiles
