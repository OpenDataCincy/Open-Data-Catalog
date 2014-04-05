# Create your views here
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from OpenDataCatalog.opendata.models import *
from OpenDataCatalog.opendata.views import send_email
from OpenDataCatalog.suggestions.models import Suggestion

from datetime import datetime
from .encoder import *
from .rest import login_required
from rest_framework import viewsets, filters

import json
import csv


from .models import ThreeOneOne, CincinnatiPolice, Arrest, BikeRack, GenericData
from .serializers import ThreeOneOneSerializer, ResourceSerializer, CincinnatiPoliceSerializer, ArrestSerializer, \
    BikeRackSerializer, GraffitiSerializer, VacancySerializer


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class ThreeOneOneViewSet(viewsets.ModelViewSet):
    queryset = ThreeOneOne.objects.filter().exclude(latitude=0)
    serializer_class = ThreeOneOneSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('request_type', 'description', )

    http_method_names = ['get', ]  # No need to allow creation


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('name', )

    http_method_names = ['get', ]  # May allow creation later.


class CPDViewSet(viewsets.ModelViewSet):
    queryset = CincinnatiPolice.objects.all().order_by('-create_date')
    serializer_class = CincinnatiPoliceSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('event_number', 'location', 'create_date', )

    http_method_names = ['get', ]  # No need to allow creation.


class ArrestViewSet(viewsets.ModelViewSet):
    queryset = Arrest.objects.all().order_by('-event_date')
    serializer_class = ArrestSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('arrest_type', 'event_date', 'anon_arrest_address', )

    http_method_names = ['get', ]  # No record creation


class BikeRackViewSet(viewsets.ModelViewSet):
    queryset = BikeRack.objects.all()
    serializer_class = BikeRackSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('description', 'location', 'street', )

    http_method_names = ['get', ]


class GraffitiViewSet(viewsets.ModelViewSet):
    queryset = GenericData.objects.filter(data_type='graffiti')
    serializer_class = GraffitiSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('location', 'community', )

    http_method_names = ['get', ]


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = GenericData.objects.filter(data_type='vacant')
    serializer_class = VacancySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('anon_address', 'description', 'comp_type', 'sub_type', 'status')

    http_method_names = ['get', ]


class AnonCPDCSV(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cpd.csv";'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Event No.', 'Anon Address', 'Desc', 'Latitude', 'Longitude'])

        CSV_DOCUMENT_ROWS = 20000  # That's 20k.  Let's hope this works.

        # Get the page number from he URL
        page = int(kwargs.get('page', 1))

        # Figure out the max row we are going for
        high_end = (page * CSV_DOCUMENT_ROWS) - 1

        # Figure out the lowest row we are going for
        if page > 1:
            low_end = ((page - 1) * CSV_DOCUMENT_ROWS)
        else:
            low_end = 0

        crime_data = CincinnatiPolice.objects.filter().order_by('create_date')[low_end:high_end]

        for c in crime_data:
            writer.writerow([
                str(c.create_date),
                c.event_number,
                c.anon_address,
                c.description,
                c.latitude,
                c.longitude,
            ])

        return response


class AnonArrestsCSV(View):
    http_method_names = ['get', ]

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="arrests.csv";'

        writer = csv.writer(response)
        writer.writerow([
            'Arrest Type',
            'Control No',
            'RAC',
            'Sex',
            'RA',
            'Date',
            'Time',
            'Sec No',
            'Sec Code',
            'DOB Year',
            'Charge Code',
            'Charge Type',
            'Arrest Disp Code',
            'Badge Number',
            'Officer',
            'Nature',
            'Report No'
            'Arrest Addr',
            'Home Addr',
        ])

        arrests = Arrest.objects.filter().order_by('event_date')

        for a in arrests:
            writer.writerow([
                a.arrest_type,
                a.control_number,
                a.rac,
                a.sex,
                a.ra,
                str(a.event_date),
                str(a.event_time),
                a.secno,
                a.seccode,
                a.dob_year,
                a.charge_code,
                a.charge_type,
                a.arrest_disp_code,
                a.badge_number,
                a.officer,
                a.nature,
                a.report_number,
                a.anon_arrest_address,  # IMPORTANT THIS IS ANON
                a.anon_home_address,  # Ditto.
            ])

        return response


def http_badreq(body=""):
    res = HttpResponse("Bad Request\n" + body)
    res.status_code = 400
    return res


@login_required
def vote(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    remote_addr = request.META['REMOTE_ADDR']
    if request.method == 'PUT' and suggestion != None:
        did_vote = suggestion.rating.get_rating_for_user(request.user, remote_addr)
        
        if did_vote == None:
            suggestion.rating.add(score=1, user=request.user, ip_address=remote_addr)

        return HttpResponse(json_encode(suggestion))

    elif request.method == "DELETE" and suggestion != None:
        vote = suggestion.rating.get_ratings().filter(user = request.user)
        if vote:
            vote.delete()
                
        return HttpResponse(json_encode(suggestion))

    raise Http404


def add_suggestion(user, text, remote_addr):
    sug = Suggestion()
    sug.suggested_by = user
    sug.text = text
            
    sug.save()            
    sug.rating.add(score=1, user=user, ip_address=remote_addr)
            
    return sug

@login_required
def add_suggestion_view(request):
    json_string = request.raw_post_data
    json_dict = json_load(json_string)

    if (json_dict.has_key("text") == False):
        return http_badreq()

    text = json_dict["text"]

    return HttpResponse(json_encode(add_suggestion(request.user, text, request.META['REMOTE_ADDR'])))


def suggestion(request, suggestion_id):
    objs = Suggestion.objects.filter(pk = suggestion_id)

    if objs and len(objs) == 1:
        return HttpResponse(json_encode(objs[0]))
    else:
        raise Http404


@csrf_exempt
def suggestions(request):
    if (request.method == 'POST'):
        return add_suggestion_view(request)
    elif (request.method == 'GET'):
        return HttpResponse(json_encode(list(Suggestion.objects.all())))
    else:
        raise Http404


def search_suggestions(request):
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+"," ")

        return HttpResponse(json_encode(list(Suggestion.objects.filter(text__icontains=qs))))
    else:
        return http_badreq("Missing required parameter qs")


def ideas(request):
    return HttpResponse(json_encode(list(Idea.objects.all()), tiny_resource_encoder))


def idea(request, idea_id):
    obj = Idea.objects.filter(id = idea_id)
    if obj and len(obj) == 1:
        return HttpResponse(json_encode(obj[0]))
    else:
        raise Http404


def tags(request):
    return HttpResponse(json_encode(list(Tag.objects.all())))


def by_tag(request, tag_name):
    return HttpResponse(json_encode(list(Resource.objects.filter(tags__tag_name = tag_name))))


def resource_search(request):
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+", " ")
        search_resources = Resource.search(qs) 

        return HttpResponse(json_encode(list(search_resources), short_resource_encoder))
    else:
        return http_badreq("Must specify qs search param")


def resource(request, resource_id):
    rsrc = Resource.objects.filter(pk=resource_id, is_published=True)
    if rsrc and len(rsrc) == 1:
        return HttpResponse(json_encode(rsrc[0], full_resource_encoder))
    else:
        return HttpResponseNotFound()


def resources(request):
    """
    Returns a list of published resources
    """
    return HttpResponse(json_encode(list(
        Resource.objects.filter(is_published=True)), short_resource_encoder), content_type='application/json'
    )


def safe_key_getter(dic):
    def annon(key, f = lambda x: x):
        if dic.has_key(key):
            return f(dic[key])
        else:
            return None
    return annon

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        json_dict = safe_key_getter(json_load(request.raw_post_data))
    
        coord_list = json_dict("coord_system")
        type_list = json_dict("types")
        format_list = json_dict("formats")
        update_frequency_list = json_dict("update_frequency")

        coords, types, formats, updates = "", "", "", ""

        if coord_list is None:
            return http_badreq("coord_system should be a list")
        if type_list is None:
            return http_badreq("types should be a list")
        if format_list is None:
            return http_badreq("formats should be a list")
        if update_frequency_list is None:
            return http_badreq("update_frequency should be a list")

        for c in coord_list:
            coords = coords + " EPSG:" + CoordSystem.objects.get(pk=c).EPSG_code.__str__()
        
        for t in type_list:
            types = types + " " + UrlType.objects.get(pk=t).url_type        
            
        for f in format_list:
            formats = formats + " " + DataType.objects.get(pk=f).data_type

        for u in update_frequency_list:
            if u:
                updates = updates + " " + UpdateFrequency.objects.get(pk=u).update_frequency
                
        data = {
            "submitter": request.user.username,
            "submit_date": datetime.now(),
            "dataset_name": json_dict("dataset_name"),
            "organization": json_dict("organization"),
            "copyright_holder": json_dict("copyright_holder"),
            "contact_email": json_dict("contact_email"),
            "contact_phone": json_dict("contact_phone"),
            "url": json_dict("url"),
            "time_period": json_dict("time_period"),
            "release_date": json_dict("release_date"),
            "area_of_interest": json_dict("area_of_interest"),
            "update_frequency": updates,
            "coord_system": coords,
            "types": types,
            "formats": formats,
            "usage_limitations": json_dict("usage_limitations"),
            "collection_process": json_dict("collection_process"),
            "data_purpose": json_dict("data_purpose"),
            "intended_audience": json_dict("intended_audience"),
            "why": json_dict("why"),
        }
        
        for key in data:
            if (data[key] == None or (hasattr(data[key], "len") and len(data[key]) == 0)):
                return http_badreq(key + " is empty or not defined")

        send_email(request.user, data)

        return HttpResponse("Created")
    else:
        raise Http404


