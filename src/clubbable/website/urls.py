# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from website.views import *

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
]
