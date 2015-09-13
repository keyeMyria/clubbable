# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponse)
from django.shortcuts import render
from dropbox.client import DropboxOAuth2Flow
from club.utils import get_full_name
from dropboxer.decorators import dropbox_required
from dropboxer.models import DropboxUser
from dropboxer.tasks import check_dropbox_user
from dropboxer.utils import get_auth_flow


logger = logging.getLogger(__name__)


def connect(request):
    flow = get_auth_flow(request)
    auth_url = flow.start()
    return HttpResponseRedirect(auth_url)


def auth(request):
    try:
        flow = get_auth_flow(request)
        access_token, user_id, url_state = flow.finish(request.GET)
    except DropboxOAuth2Flow.BadRequestException:
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.BadStateException:
        # Start the auth flow again.
        return connect(request)
    except DropboxOAuth2Flow.CsrfException:
        return HttpResponseForbidden()
    except DropboxOAuth2Flow.NotApprovedException:
        messages.warning(request, 'Dropbox authentication was not approved.')
        return HttpResponseRedirect(reverse('dashboard'))
    except DropboxOAuth2Flow.ProviderException as err:
        logger.exception('Error authenticating Dropbox', err)
        return HttpResponseForbidden()
    dropbox_user, created = DropboxUser.objects.update_or_create(
        user=request.user,
        defaults={'access_token': access_token}
    )
    messages.success(request, 'Dropbox authentication successful.')
    return HttpResponseRedirect(reverse('dashboard'))


def dropbox_logout(request):
    dropbox_user = DropboxUser.objects.get(user=request.user)
    dropbox_user.access_token = ''
    dropbox_user.save()
    messages.info(request, 'You have disconnected your Dropbox account.')
    return HttpResponseRedirect(reverse('dashboard'))


@dropbox_required
def check_dropbox(request):
    """
    Schedule Dropbox to be checked, and return to dashboard.
    """
    dropbox_user = DropboxUser.objects.get(user=request.user)
    check_dropbox_user.delay(dropbox_user)
    messages.info(request, 'Dropbox is being checked for new files.')
    return HttpResponseRedirect(reverse('dashboard'))


@dropbox_required
def configure_dropbox(request):
    """
    Allow user to set their docs, galleries and mdb directories
    """
    dropbox_user = DropboxUser.objects.get(user=request.user)
    if request.method == 'POST':
        dropbox_user.galleries_folder = request.POST['galleries_folder']
        dropbox_user.docs_folder = request.POST['docs_folder']
        dropbox_user.mdb_folder = request.POST['mdb_folder']
        dropbox_user.save()
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, 'dropboxer/configure.html', {
        'full_name': get_full_name(request.user),
        'dropbox_user': dropbox_user,
    })


def webhook(request):
    """
    Dropbox pings this view when files have changed
    """
    # TODO: What does the request look like?
    logger.info()
    check_dropbox.delay()
    return HttpResponse('Accepted', content_type='text/plain', status=202)
