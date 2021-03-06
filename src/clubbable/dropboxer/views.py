import logging
from django.contrib import messages
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpResponse,
)
from django.urls import reverse
import dropbox.oauth
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
    except dropbox.oauth.BadRequestException:
        return HttpResponseBadRequest()
    except dropbox.oauth.BadStateException:
        # Start the auth flow again.
        return connect(request)
    except dropbox.oauth.CsrfException:
        return HttpResponseForbidden()
    except dropbox.oauth.NotApprovedException:
        messages.warning(request, 'Dropbox authentication was not approved.')
        return HttpResponseRedirect(reverse('dashboard'))
    except dropbox.oauth.ProviderException as err:
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


def webhook(request):
    """
    Dropbox pings this view when files have changed
    """
    # TODO: Write this.
    check_dropbox.delay()
    return HttpResponse('Accepted', content_type='text/plain', status=202)
