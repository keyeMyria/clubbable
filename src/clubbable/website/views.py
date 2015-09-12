from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext


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


@login_required
def dashboard(request):

    def get_tiles():
        """
        Return tiles from all dashboard apps
        """
        tiles_ = []
        for app in settings.DASHBOARD_APPS:
            module = __import__(app + '.dashboard')
            tiles_.extend(module.dashboard.get_tiles(request))
        return tiles_

    def get_3_per_row(items):
        """
        Arrange items into rows of 3
        """
        rows = []
        row = []
        for i, item in enumerate(items):
            if i % 3 and row:
                rows.append(row)
                row = []
            row.append(item)
        if row:
            rows.append(row)
        return rows

    tiles = get_tiles()
    context = RequestContext(request, {
        'full_name': get_full_name(request.user),
        'rows': get_3_per_row(tiles),
    })
    return render(request, 'website/dashboard.html', context)
