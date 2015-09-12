# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from dropboxer.views import *

urlpatterns = [
    url(r'^check/$', check_dropbox, name='check_dropbox'),
    url(r'^auth/start/$', auth_start, name='dropbox_auth_start'),
    url(r'^auth/finish/$', auth_finish, name='dropbox_auth_finish'),
    url(r'^logout/$', dropbox_logout, name='dropbox_logout'),
]
