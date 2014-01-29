from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import xlrd
from datetime import date, time

from OpenDataCatalog.api.models import BikeRack


class Command(BaseCommand):
    help = 'Supply an xls or xlsx file to parse for arrests'
    args = '<file.xls(x)>'

    option_list = BaseCommand.option_list + (
        make_option('--data',
            dest='data',
            default=False,),
    )

    def handle(self, *args, **options):

        if not 'data' in options:
            raise CommandError('You must specify a type of data to parse.')

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
            print i
