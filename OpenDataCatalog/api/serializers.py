from .models import ThreeOneOne, CincinnatiPolice, Arrest
from OpenDataCatalog.opendata.models import Resource

from rest_framework import serializers


class ThreeOneOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreeOneOne
        fields = ('csr', 'request_type', 'description', 'status', 'date_received', 'latitude', 'longitude')


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'short_description', 'description', )


class CincinnatiPoliceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CincinnatiPolice
        fields = ['event_number', 'anon_address', 'create_date', 'description', 'location', ]


class ArrestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Arrest
        fields = ['arrest_type', 'event_date', 'event_time', 'dob_year', 'charge_code', 'anon_arrest_address',
                  'badge_number']
