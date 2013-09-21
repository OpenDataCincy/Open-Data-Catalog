from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^$', 'OpenDataCatalog.suggestions.views.list_all'),
   url(r'^post/$', 'OpenDataCatalog.suggestions.views.add_suggestion'),
   url(r'^vote/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.add_vote'),
   url(r'^unvote/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.remove_vote'),
   url(r'^close/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.close'),
)
