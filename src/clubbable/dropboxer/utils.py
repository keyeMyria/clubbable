# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from dropbox.client import DropboxOAuth2Flow


def get_auth_flow(session):
    redirect_uri = reverse('dropbox_auth')
    return DropboxOAuth2Flow(
        settings.DROPBOX_APP_KEY,
        settings.DROPBOX_APP_SECRET,
        redirect_uri,
        session,
        'dropbox-auth-csrf-token',
    )
