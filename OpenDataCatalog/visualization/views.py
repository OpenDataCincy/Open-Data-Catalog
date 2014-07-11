# Create your views here.
from django.views.generic import TemplateView

from boto.s3.connection import S3Connection

from django.conf import settings


class CPDBarChartView(TemplateView):
    template_name = 'visualization/cpd-bar-chart.html'

    def get_context_data(self, **kwargs):

        # Let's grab the 8 most used, I guess.

        return {

        }


class TransitDataView(TemplateView):
    template_name = 'visualization/transit.html'

    def get_context_data(self, **kwargs):

        # These are stored in local_settings.py, but should be set as environment variables
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

        bucket = conn.get_bucket('opendatacincy')

        return {
            'list': bucket.list(),
        }
