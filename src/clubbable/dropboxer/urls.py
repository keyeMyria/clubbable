# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from dropboxer.views import *

urlpatterns = [
    url(r'^check/$', check_dropbox, name='check_dropbox'),
    url(r'^connect/$', connect, name='dropbox_connect'),
    url(r'^auth/$', auth, name='dropbox_auth'),
    url(r'^logout/$', dropbox_logout, name='dropbox_logout'),
    url(r'^config/$', configure_dropbox, name='dropbox_config'),
    url(r'^dropbox/$', webhook, name='dropbox_webhook'),
]
