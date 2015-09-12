# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from docs.views import *

urlpatterns = [
    url(r'^(\d+)/$', DocList.as_view(), name='doc_list'),
    url(r'^(\d+)/(?P<pk>\d+)/([^/]+)/$', download, name='doc_download'),
    url(r'^(\d+)/(?P<pk>\d+)/$', send, name='doc_send'),
]
