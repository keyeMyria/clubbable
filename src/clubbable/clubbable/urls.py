from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls, views as auth_views
from markdown import markdown
import yaml
from docs import urls as docs_urls
from galleries import urls as galleries_urls
from dropboxer import urls as dropbox_urls
from website.views import dashboard


def _get_login_context():
    with open(settings.BASE_DIR + '/clubbable/landing_page.yaml') as file:
        data = yaml.load(file)
    return {
        'club_name': settings.CLUB_NAME,
        'heading': data['heading'],
        'image': data['image'],
        'content_html': markdown(data['content_markdown']),
    }

# Replace the login url with out own definition that includes the context for
# the landing page
auth_urls.urlpatterns[0] = url(
    r'^login/$',
    auth_views.login,
    {'extra_context': _get_login_context()},
    name='login'
)

admin.autodiscover()

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^doc/', include(docs_urls)),
    url(r'^img/', include(galleries_urls)),
    url(r'^dropbox/', include(dropbox_urls)),

    url(r'^accounts/', include(auth_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
