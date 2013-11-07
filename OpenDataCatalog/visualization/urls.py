from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^map/$', TemplateView.as_view(template_name='visualization/map.html'), name='visualization-map'),
)
