from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import xlrd
from datetime import date, time
import re
import datetime

from OpenDataCatalog.api.models import BikeRack, GenericData


class Command(BaseCommand):
    help = 'Supply an xls or xlsx file to parse for arrests'
    args = '<file.xls(x)>'

    option_list = BaseCommand.option_list + (
        make_option('--data',
            dest='data',
            default=False,),
    )

    available_data_options = [
        'bikeracks',
        'vacant',
        'graffiti',
    ]

    def handle(self, *args, **options):

        if not 'data' in options:
            raise CommandError('You must specify a type of data to parse.')

        else:
            if not options.get('data') in self.available_data_options:
                raise CommandError('The data type you specified is not available.')

        if not len(args):
            raise CommandError('You must supply an xls or xlsx document')

        print args[0]

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError('The file could not be opened')
        except xlrd.XLRDError:
            raise CommandError('Ensure the file is the correct format')

        self.stdout.write('Opened workbook: %s' % args[0])

        # # We just want the first sheet.
        try:
            sheet = workbook.sheet_by_index(0)
        except AttributeError:
            raise CommandError('Could not open first sheet.  Check file format.')
        except IndexError:
            raise CommandError('Could not open first sheet.')
        #
        # # # Go through each row and handle.
        for i in range(sheet.nrows):

            row = sheet.row_values(i)

            if options.get('data') == 'bikeracks':

                if u'NEIGHBORHOOD' in row[0]:
                    continue

                try:
                    rack_number = int(row[4])
                except ValueError:
                    rack_number = 0

                # Get the street and lat/lon in one fell swoop
                s = row[2].splitlines()
                (latitude, longitude) = s[2].strip('()').split(',')

                rack = BikeRack.objects.create(
                    rack_number=rack_number,
                    neighborhood=row[0].strip(),
                    location=row[1].strip(),
                    street=s[0].strip(),
                    latitude=latitude.strip(),
                    longitude=longitude.strip(),
                    placement=row[7].strip(),
                    rack_type=row[8].strip(),
                    description=row[9].strip()[:300],
                )

                self.stdout.write('Created bike rack: %s' % rack)

            elif options.get('data') == 'vacant':

                if u'NOTATION' in row[0]:
                    continue

                parcel_parts = row[8].splitlines()

                if len(parcel_parts) > 1:
                    parcel = parcel_parts[0].strip()
                else:
                    parcel = row[8].strip()

                try:
                    s = row[1].splitlines()
                    (latitude, longitude) = s[2].strip('()').split(',')
                    address = s[0]
                except IndexError:
                    latitude = 0
                    longitude = 0
                    address = 0

                item = GenericData.objects.create(
                    data_type='vacant',
                    community=row[12].strip(),
                    description=row[0].strip(),
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    location=row[10].strip(),
                    anon_location=row[9].strip(),
                    status=row[2].strip(),
                    comp_type=row[3].strip(),
                    sub_type=row[4].strip(),
                    approved=row[5].strip(),
                    x_coordinate=row[6],
                    y_coordinate=row[7],
                    parcel=parcel,
                    inspection_area=row[11],
                    street_direction=row[13].strip(),
                )
                self.stdout.write(u'Create Vacant record at %s' % item.address)

            elif options.get('data') == 'graffiti':

                if u'COMMUNITY' in row[0]:
                    continue

                try:
                    census_tract = float(row[9])
                except ValueError:
                    census_tract = None

                s = row[1].splitlines()
                (latitude, longitude) = s[2].strip('()').split(',')
                address = s[0]

                try:
                    date_received = datetime.datetime(*xlrd.xldate_as_tuple(row[6], workbook.datemode)).date()
                except (ValueError, TypeError):
                    date_received = None

                try:
                    date_planned_completion = datetime.datetime(*xlrd.xldate_as_tuple(row[15], workbook.datemode)).date()
                except (ValueError, TypeError):
                    date_planned_completion = None

                try:
                    x = int(row[7] * 24 * 3600)
                    time_received = datetime.time(x//3600, (x % 3600)//60, x % 60)

                except ValueError:
                    time_received = None

                item = GenericData.objects.create(
                    data_type='graffiti',
                    user_id=row[14].strip(),
                    community=row[0].strip(),
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    request_type=row[2].strip(),
                    csr=row[3].strip(),
                    status=row[4].strip(),
                    description=row[5].strip(),
                    date_received=date_received,
                    time_received=time_received,
                    date_planned_completion=date_planned_completion,
                    location=row[8].strip(),
                    census_tract=census_tract,
                    street_direction=row[22].strip()
                )
                self.stdout.write('Created graffiti record: %s' % item.id)
