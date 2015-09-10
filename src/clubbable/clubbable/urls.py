from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'website.views.dashboard', name='dashboard'),

    url(r'^accounts/', include(auth_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
