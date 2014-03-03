from .models import ThreeOneOne, CincinnatiPolice, Arrest, BikeRack
from OpenDataCatalog.opendata.models import Resource

from rest_framework import serializers


class ThreeOneOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreeOneOne
        fields = ('csr', 'request_type', 'description', 'status', 'date_received', 'latitude', 'longitude')


class ResourceSerializer(serializers.ModelSerializer):
    resource_urls = serializers.RelatedField(many=True)

    class Meta:
        model = Resource
        fields = ('name', 'short_description', 'description', 'resource_urls',)


class CincinnatiPoliceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CincinnatiPolice
        fields = ['event_number', 'anon_address', 'create_date', 'description', 'location', ]


class ArrestSerializer(serializers.HyperlinkedModelSerializer):
    description = serializers.CharField(source='description', read_only=True)

    class Meta:
        model = Arrest
        fields = ['arrest_type', 'event_date', 'event_time', 'dob_year', 'charge_code', 'charge_type', 'anon_arrest_address',
                  'badge_number', 'control_number', 'description']


class BikeRackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BikeRack
        fields = ['rack_number', 'neighborhood', 'location', 'latitude', 'longitude', 'street', 'placement',
                  'rack_type', 'description']
