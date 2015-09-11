from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from markdown import markdown
from yaml import load


def landing(request):
    """
    Landing page displays information about the club and allows members to log
    in.
    """
    data = load('../clubbable/landing_page.yaml')
    context = {
        'club_name': settings.CLUB_NAME,
        'heading': data['heading'],
        'image': data['image'],
        'content_html': markdown(data['content_markdown']),
    }
    return render(request, 'website/landing.html', context)


@login_required
def dashboard(request):
    context = {}
    return render(request, 'website/dashboard.html', context)
