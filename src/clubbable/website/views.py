from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from markdown import markdown
import yaml


@login_required
def dashboard(request):
    context = {}
    return render(request, 'website/dashboard.html', context)
