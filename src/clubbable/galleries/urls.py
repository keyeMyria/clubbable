# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from galleries.views import *

urlpatterns = [
    url(r'^(\d+)/$', ImageList.as_view(), name='image_list'),
]
