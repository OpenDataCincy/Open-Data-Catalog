from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import CPDBarChartView

urlpatterns = patterns('',
    url(r'^map/$', TemplateView.as_view(template_name='visualization/map.html'), name='visualization-map'),
    url(r'^cpd/$', CPDBarChartView.as_view(), name='visualization-cpd-bar'),
    url(r'^transit/$', TemplateView.as_view(template_name='visualization/transit.html'), name='visualization-transit'),
)
