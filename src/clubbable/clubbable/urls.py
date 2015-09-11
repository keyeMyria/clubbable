from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from website import urls as website_urls
from docs import urls as docs_urls
from galleries import urls as galleries_urls
# from dropboxer import urls as dropbox_urls


admin.autodiscover()

urlpatterns = [
    url(r'^$', 'website.views.landing', name='landing'),
    url(r'^home/$', include(website_urls)),
    url(r'^doc/$', include(docs_urls)),
    url(r'^img/$', include(galleries_urls)),
    # url(r'^dropbox/$', include(dropbox_urls)),

    url(r'^accounts/', include(auth_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
