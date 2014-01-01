from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import CrimeDataView, ThreeOneOneViewSet, ResourceViewSet, CPDViewSet, ArrestViewSet

router = routers.DefaultRouter()
router.register(r'threeoneones', ThreeOneOneViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'cpd', CPDViewSet)
router.register(r'arrests', ArrestViewSet)


urlpatterns = patterns('',
    url('^', include(router.urls)),
    # API urls (all are GET urls unless stated otherwise)
    url(r'^resources/$', 'OpenDataCatalog.api.views.resources'),
    url(r'^resources/(?P<resource_id>\d+)/$', 'OpenDataCatalog.api.views.resource'),
    url(r'^resources/search$', 'OpenDataCatalog.api.views.resource_search'),
    url(r'^tags/$', 'OpenDataCatalog.api.views.tags'),
    url(r'^tags/(?P<tag_name>.*)/$', 'OpenDataCatalog.api.views.by_tag'),
    url(r'^ideas/$', 'OpenDataCatalog.api.views.ideas'),
    url(r'^ideas/(?P<idea_id>\d+)/$', 'OpenDataCatalog.api.views.idea'),
    # GET to list, POST to create
    url(r'^suggestions/$', 'OpenDataCatalog.api.views.suggestions'),
    url(r'^suggestions/search$', 'OpenDataCatalog.api.views.search_suggestions'),
    url(r'^suggestions/(?P<suggestion_id>\d+)/$', 'OpenDataCatalog.api.views.suggestion'),
    # PUT to vote, DELETE to remove
    url(r'^suggestions/(?P<suggestion_id>\d+)/vote$', 'OpenDataCatalog.api.views.vote'),
    # POST to create
    url(r'^submit/$', 'OpenDataCatalog.api.views.submit'),

    url(r'^crime/$', CrimeDataView.as_view(), name='api-crime-data'),

)
