from .models import ThreeOneOne
from OpenDataCatalog.opendata.models import Resource

from rest_framework import serializers


class ThreeOneOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreeOneOne
        fields = ('csr', 'request_type', 'status', 'date_received', 'latitude', 'longitude')


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'short_description', 'description', )
