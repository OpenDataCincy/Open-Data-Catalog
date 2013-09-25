from django.core.management.base import BaseCommand

from OpenDataCatalog.opendata.models import Resource, Submission, CoordSystem, DataType
from django.contrib.auth.models import User

from simplejson import loads


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.get(pk=1)

        submission = Submission.objects.get(pk=args[0])

        data = loads(submission.json_text)

        self.stdout.write(str(data))

        self.stdout.write("\n\n" + data.get('time_period') + "\n\n")

        resource = Resource()
        resource.name = data.get('dataset_name')
        resource.short_description = data.get('description', 'n/a')[:255]
        resource.time_period = data.get('time_period', 'n/a')
        resource.release_date = data.get('release_date')
        resource.created_by = user
        resource.last_updated_by = user
        resource.description = data.get('description', 'n/a')
        resource.wkt_geometry = data.get('wkt_geometry', 0)
        resource.organization = data.get('organization', 'n/a')
        resource.usage = data.get('usage_limitations', 'n/a')
        resource.contact_phone = data.get('contact_phone', 'n/a')
        resource.contact_email = data.get('contact_email', 'user@example.com')
        resource.contact_url = data.get('contact_url', 'http://google.com')
        resource.area_of_interest = data.get('area_of_interest')
        resource.is_published = False
        resource.update_frequency = data.get('update_frequency', '')
        resource.data_formats = data.get('formats', '')

        resource.save()

        for t in data.get('types'):
            try:
                data_type = DataType.objects.get(pk=t)

            except DataType.DoesNotExist:
                data_type = None

            if data_type:
                resource.data_types.add(data_type)
                resource.save()

        for c in data.get('coord_system'):
            try:
                coord = CoordSystem.objects.get(pk=c)

            except CoordSystem.DoesNotExist:
                coord = None

            if coord:
                resource.coord_sys.add(coord)
                resource.save()
