# -*- coding: utf-8 -*-
"""
Adds a tile to the dashboard
"""
from __future__ import unicode_literals
from django.template import loader
from dropboxer.models import DropboxUser


def get_tiles(request):
    """
    Return HTML tiles for the dashboard, or empty list if user is not staff
    """
    tiles = []
    if request.user.is_staff:
        dropbox_user = DropboxUser.objects.get_or_none(user=request.user)
        if dropbox_user and dropbox_user.access_token:
            # TODO: Use webhook instead
            template = loader.get_template('dropboxer/check_tile.html')
            tiles.append(template.render({}))
        else:
            template = loader.get_template('dropboxer/auth_tile.html')
            tiles.append(template.render({}))
    return tiles
