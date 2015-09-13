# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
from django.http import HttpResponseRedirect
from dropboxer.models import DropboxUser
from dropboxer.utils import get_auth_flow


def dropbox_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        dropbox_user = DropboxUser.objects.get_or_none(user=request.user)
        if dropbox_user and dropbox_user.access_token:
            return view_func(request, *args, **kwargs)
        if not dropbox_user or not dropbox_user.access_token:
            flow = get_auth_flow(request)
            auth_url = flow.start()
            return HttpResponseRedirect(auth_url)
    return wrapped
