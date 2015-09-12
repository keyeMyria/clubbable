# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_full_name(user):
    member = user.profile.member
    if member:
        return '%s' % member
    full_name = user.get_full_name()
    if full_name:
        return full_name
    if user.email:
        return user.email
    return user.username
