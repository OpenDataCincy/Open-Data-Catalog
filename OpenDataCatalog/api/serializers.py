from .models import ThreeOneOne

from rest_framework import serializers


class ThreeOneOneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreeOneOne
        fields = ('csr', 'status', 'date_received', 'latitude', 'longitude')
