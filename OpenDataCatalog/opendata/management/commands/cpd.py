from django.core.management.base import BaseCommand, CommandError

import xlrd

from datetime import date

from OpenDataCatalog.api.models import CincinnatiPolice


class Command(BaseCommand):
    help = "Supply an xls or xlsx file to be parsed"
    args = "<something.xlsx>"

    def handle(self, *args, **options):

        if not len(args):
            raise CommandError('You did not supply an xls document...')

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError('The file \'%s\' could not be opened. Does it exist?' % args[0])
        except xlrd.XLRDError:
            raise CommandError('Are you sure that \'%s\' is an Excel file?' % args[0])

        self.stdout.write('Opened workbook: %s' % args[0])

        # We just want the first sheet.
        try:
            sheet = workbook.sheet_by_index(0)
        except AttributeError:
            raise CommandError('I have no idea why this thing will nt open')

        # # Go through each row and handle.
        # for i in range(sheet.nrows):
        for i in range(10):
            row = sheet.row_values(i)

            if u'Event_Number' in row[0]:
                continue

            try:
                date_tuple = xlrd.xldate_as_tuple(row[1], workbook.datemode)
                event_date = date(year=date_tuple[0], month=date_tuple[1], day=date_tuple[2])
            except TypeError:
                event_date = None

            c = CincinnatiPolice.objects.create(
                event_number=row[0],
                create_date=event_date,
                address=row[2],
                description=row[3],
                location=row[4],
            )

            self.stdout.write('Created: %s' % c)
