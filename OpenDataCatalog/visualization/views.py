# Create your views here.
from django.views.generic import TemplateView


class CPDBarChartView(TemplateView):
    template_name = 'visualization/cpd-bar-chart.html'

    def get_context_data(self, **kwargs):

        # Let's grab the 8 most used, I guess.

        return {

        }
