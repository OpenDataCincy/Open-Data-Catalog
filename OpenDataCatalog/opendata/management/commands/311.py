from django.core.management.base import BaseCommand, CommandError

import xlrd


class Command(BaseCommand):
    help = "Supply an xls or xlsx file to be parsed for Crime Data"
    args = "<something.xlsx>"

    def handle(self, *args, **options):

        try:
            workbook = xlrd.open_workbook(args[0])
        except IOError:
            raise CommandError('The file \'%s\' could not be opened. Does it exist?' % args[0])
        except xlrd.XLRDError:
            raise CommandError('Are you sure that \'%s\' is an Excel file?' % args[0])

        # We just want the first sheet.
        sheet = workbook.sheet_by_index(0)

        # # Go through each row and handle.
        for i in range(sheet.nrows):
            row = sheet.row_values(i)

            # row[0] is CSR#
            # row[1] is status
            # row[2] is the type
            # row[3] is description
            # row[4] is the date MM/DD/YYYY HH:MM:SS AM

            if 'trash' in row[2]:
                print row[0]
