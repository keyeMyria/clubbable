from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
    context = {'full_name': get_full_name(request.user)}
    return render(request, 'website/dashboard.html', context)
