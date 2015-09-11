import logging
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from dropbox.client import DropboxOAuth2Flow
from dropboxer.models import DropboxUser
from dropboxer.tasks import check_dropbox_user


logger = logging.getLogger(__name__)


def _get_auth_flow(session):
    redirect_uri = reverse('dropbox_auth')
    return DropboxOAuth2Flow(
        settings.DROPBOX_APP_KEY,
        settings.DROPBOX_APP_SECRET,
        redirect_uri,
        session,
        'dropbox-auth-csrf-token',
    )


def auth_start(request):
        auth_url = _get_auth_flow(request.session).start()
        return HttpResponseRedirect(auth_url)


def auth_finish(request):
    try:
        access_token, user_id, url_state = _get_auth_flow(request.session).finish(request.GET)
    except DropboxOAuth2Flow.BadRequestException:
        return HttpResponseBadRequest()
    except DropboxOAuth2Flow.BadStateException:
        # Start the auth flow again.
        return auth_start(request)
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


def check_dropbox(request):
    """
    Schedule Dropbox to be checked, and return to dashboard.
    """
    dropbox_user = DropboxUser.objects.get_or_none(user=request.user)
    if not dropbox_user or not dropbox_user.access_token:
        return auth_start(request)

    check_dropbox_user.delay(dropbox_user)
    messages.info(request, 'Dropbox is being checked for new files.')
    return HttpResponseRedirect(reverse('dashboard'))
