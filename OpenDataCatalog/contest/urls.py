from django.conf.urls import patterns, url

from .views import ContestEntriesView, AddEntryView, AddEntryThanksView, ContestTemplateView, EntryView

urlpatterns = patterns('',
    url(r'^$', ContestEntriesView.as_view(), name='contest'),
    url(r'^(?P<contest_id>\d+)/$', ContestEntriesView.as_view(), name='contest-id'),
    url(r'^rules/$', ContestTemplateView.as_view(template_name='contest/rules.html'), name='contest-rules'),
    url(r'^add/$', AddEntryView.as_view(), name='contest-add'),
    url(r'^thanks/$', AddEntryThanksView.as_view(), name='contest-thanks'),
    url(r'^entry/(?P<entry_id>\d+)/$', EntryView.as_view(), name='contest-entry'),
    url(r'^entry/(?P<entry_id>\d+)/vote/$', 'OpenDataCatalog.contest.views.add_vote'),
    url(r'^entries/$', 'OpenDataCatalog.contest.views.get_entries_table'),
    url(r'^winners/$', 'OpenDataCatalog.contest.views.get_winners'),
)
