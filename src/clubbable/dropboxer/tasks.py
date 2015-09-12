# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import shared_task
from dropboxer.models import DropboxUser


def check_galleries(user):
    if user.galleries_folder:
        # TODO: ...
        pass


def check_docs(user):
    if user.docs_folder:
        # TODO: ...
        pass


def check_mdb(user):
    if user.mdb_folder:
        # TODO: ...
        pass


@shared_task
def check_dropbox_user(user):
    """
    Check Dropbox for a Dropbox user.

    This task can be queued by a user, or can be called synchronously by
    check_dropbox()
    """
    check_galleries(user)
    check_docs(user)
    check_mdb(user)


@shared_task
def check_dropbox():
    """
    Traverse clubbable folders on Dropbox and if new files are found, import
    them
    """
    for user in DropboxUser.objects.order_by('username').distinct('username'):
        check_dropbox_user(user)
