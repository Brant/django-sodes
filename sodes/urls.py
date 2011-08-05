"""
url confs for sodes
"""

from django.conf.urls.defaults import *

from sodes.util.getters import use_slugs_for_url

urlpatterns = patterns('sodes.views',
    url(r'^$', 'index', {"template_name": "sodes/index.html"}, name="sodes_index"),
    url(r'^archives/(?P<year>\d+)/(?P<month>\d+)/$', 'archive', {"template_name": "sodes/archive.html"}, name="sodes_archive"),
)

if use_slugs_for_url():
    urlpatterns += patterns('sodes.views',
        url(r'^(?P<slug>[\w\-]+)/$', 'single_by_slug', {"template_name": "sodes/single.html"}, name="sodes_single"),
    )
else:
    urlpatterns += patterns('sodes.views',
        url(r'^(?P<category>[\w\-]+)/(?P<chronology>[\w\-]+)/$', 'single_by_category', {"template_name": "sodes/single.html"}, name="sodes_single"),
    )
