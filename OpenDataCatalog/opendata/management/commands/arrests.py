from django.core.management.base import BaseCommand, CommandError

import xlrd
from datetime import date, time

from OpenDataCatalog.api.models import Arrest


class Command(BaseCommand):
    help = 'Supply an xls or xlsx file to parse for arrests'
    args = '<file.xls(x)>'

    def handle(self, *args, **options):

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
        # for i in range(10):
            row = sheet.row_values(i)

            if u'ARR_TYPE' in unicode(row[0]):
                continue

            # Great, let's build an arrest.
            arrest_date = date(year=int(row[7]), month=int(row[5]), day=int(row[6]))

            # Get the time of arrest
            arrest_time = self.parse_time(row[8])

            # Clean up some data so it works with the DB
            try:
                badge_number = int(row[17])
            except ValueError:
                badge_number = None

            try:
                home_zip = int(row[23])
            except ValueError:
                home_zip = None

            arrest = Arrest.objects.create(
                arrest_type=int(row[0]),
                control_number=int(row[1]),
                rac=row[2].strip(),
                sex=row[3].strip(),
                ra=int(row[4]),
                event_date=arrest_date,
                event_time=arrest_time,
                secno=row[9].strip(),
                seccode=row[10].strip(),
                dob_year=int(row[11]),
                charge_code=int(row[14]),
                charge_type=int(row[15]),
                arrest_disp_code=int(row[16]),
                badge_number=badge_number,
                officer=row[18].strip(),
                nature=int(row[19]),
                arrest_address=row[12].strip(),
                home_address=row[20].strip(),
                home_city=row[21].strip(),
                home_state=row[22].strip(),
                home_zip=home_zip,
                report_number=row[24].strip(),
            )

            self.stdout.write('%s. Created address: %s' % (i, arrest))

    def parse_time(self, t):
        """
        Parse time in format xxxx into time() format.
        """
        t = int(t)
        hours = t / 100
        minutes = t % 100

        try:
            parsed_time = time(hour=hours, minute=minutes)
        except Exception:
            parsed_time = None

        return parsed_time

