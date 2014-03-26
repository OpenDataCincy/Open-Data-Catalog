from django.views.generic import TemplateView


class GalleryHomeView(TemplateView):
    template_name = 'gallery/home.html'

    def get_context_data(self, **kwargs):

        return {

        }
