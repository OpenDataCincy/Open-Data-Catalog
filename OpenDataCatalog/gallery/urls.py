from django.conf.urls import patterns, url

from .views import GalleryHomeView

urlpatterns = patterns('',
    url(r'^', GalleryHomeView.as_view(), name='gallery-home'),
)
