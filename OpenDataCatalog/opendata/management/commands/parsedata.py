from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import xlrd
from datetime import date, time
import re

from OpenDataCatalog.api.models import BikeRack


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
    ]

    def handle(self, *args, **options):

        if not 'data' in options:
            raise CommandError('You must specify a type of data to parse.')

        else:
            if not options.get('data') in self.available_data_options:
                raise CommandError('The data type you specified is not available.')

        if not len(args):
            raise CommandError('You must supply an xls or xlsx document')

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError('The file could not be opened')
        except xlrd.XLRDError:
            raise CommandError('Ensure the file is the correct format')

        self.stdout.write('Opened workbook: %s' % args[0])

        # We just want the first sheet.
        try:
            sheet = workbook.sheet_by_index(0)
        except AttributeError:
            raise CommandError('Could not open first sheet.  Check file format.')

        # # Go through each row and handle.
        for i in range(sheet.nrows):

            row = sheet.row_values(i)

            if options.get('data') == 'bikeracks':

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
                    description='',
                )

                self.stdout.write('Created bike rack: %s' % rack)
