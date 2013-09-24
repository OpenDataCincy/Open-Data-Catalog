from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from OpenDataCatalog.opendata.feeds import ResourcesFeed, TagFeed, IdeasFeed, UpdatesFeed
from OpenDataCatalog.opendata.models import Resource, Idea
from OpenDataCatalog.registration_backend import CatalogRegistrationView

from OpenDataCatalog.opendata.views import ResourceView, UserView, SubmitDataView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'flatpages': FlatPageSitemap,
    'resources': GenericSitemap({'queryset': Resource.objects.all(), 'date_field': 'created'}, priority=0.5),
    'ideas': GenericSitemap({'queryset': Idea.objects.all(), 'date_field': 'created_by_date'}, priority=0.5),
}

urlpatterns = patterns('',
    url(r'^$', 'OpenDataCatalog.opendata.views.home', name='home'),

    # The API urls
    url(r'^api/', include('OpenDataCatalog.api.urls')),

    url(r'^opendata/$', 'OpenDataCatalog.opendata.views.results'),

    url(r'^opendata/tag/(?P<tag_id>\d+)/$', 'OpenDataCatalog.opendata.views.tag_results', name='tag'),
    url(r'^opendata/search/$', 'OpenDataCatalog.opendata.views.search_results'),
    url(r'^opendata/resource/(?P<resource_id>\d+)/$', ResourceView.as_view()),
    url(r'^opendata/resource/(?P<resource_id>\d+)/(?P<slug>[-\w]+)/$', ResourceView.as_view()),
    url(r'^opendata/submit/$', SubmitDataView.as_view(), name='submit'),
    url(r'^opendata/submit/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='submit-thanks'),
    url(r'^ideas/$', 'OpenDataCatalog.opendata.views.idea_results', name='ideas'),
    url(r'^idea/(?P<idea_id>\d+)/$', 'OpenDataCatalog.opendata.views.idea_results'),
    url(r'^idea/(?P<idea_id>\d+)/(?P<slug>[-\w]+)/$', 'OpenDataCatalog.opendata.views.idea_results'),
    url(r'^thanks/$', 'OpenDataCatalog.opendata.views.thanks'),
    
    url(r'^tags/$', 'OpenDataCatalog.opendata.views.get_tag_list'),
    
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^accounts/register/$', CatalogRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/password_reset', 'django.contrib.auth.views.password_reset'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^opendata/nominate/', include('OpenDataCatalog.suggestions.urls'), name='nominate'),
    url(r'^contest/', include('OpenDataCatalog.contest.urls')),

    url(r'^feeds/$', 'OpenDataCatalog.opendata.views.feed_list'),
    url(r'^feeds/resources/$', ResourcesFeed()),
    url(r'^feeds/updates/$', UpdatesFeed()),
    url(r'^feeds/ideas/$', IdeasFeed()),
    url(r'^feeds/tag/(?P<tag_id>\d+)/$', TagFeed()),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),

    url(r'^catalog/', include("OpenDataCatalog.catalog.urls")),

    # User specific
    url(r'^users/(?P<username>\w+)/', UserView.as_view(), name='user'),

    # Uncomment the next line to enable the admin:
    url(r'^_admin_/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Process static files properly
urlpatterns += staticfiles_urlpatterns()

# Catch all for static pages
#urlpatterns += patterns('django.contrib.flatpages.views',
#    (r'^(?P<url>.*/)$', 'flatpage'),
#)
