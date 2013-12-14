from django.core.management.base import BaseCommand, CommandError

import xlrd
import time

from geopy import geocoders
from datetime import datetime

from OpenDataCatalog.api.models import ThreeOneOne


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

        # The geocoder
        google = geocoders.GoogleV3()

        # # Go through each row and handle.
        addresses = {}
        for i in range(sheet.nrows):
        # for i in range(50):
            row = sheet.row_values(i)

            if u'CSR #' in unicode(row[0]) or u'DESCRIPTION' in unicode(row[3]):
                continue

            if ThreeOneOne.objects.filter(csr=row[0]).exists():
                continue

            # if row[7]:
            #     address = u'%s Cincinnati, OH' % row[7]
            #
            #     if not address in addresses:
            #         try:
            #             place, (lat, lon) = google.geocode(address, exactly_one=False)[0]
            #         except Exception:
            #             print 'could not geocode %s' % address
            #
            #         addresses[address] = {
            #             'lat': lat,
            #             'lon': lon,
            #         }
            #     else:
            #         lat = addresses[address].get('lat')
            #         lon = addresses[address].get('lon')
            #
            #     js = 'var myLatLng = new google.maps.LatLng(%s, %s); ' % (lat, lon)
            #     js += 'var marker = new google.maps.Marker({ position: myLatLng, title: "%s" }); ' % row[2]
            #     js += 'marker.setMap(map);'
            #
            #     self.stdout.write(js)
            #     self.stdout.write("\n")

            try:
                date_received = datetime(*xlrd.xldate_as_tuple(row[4], workbook.datemode))
            except TypeError:
                date_received = None

            try:
                date_answered = datetime(*xlrd.xldate_as_tuple(row[13], workbook.datemode))
            except TypeError:
                date_answered = None

            try:
                planned_completion_date = datetime(*xlrd.xldate_as_tuple(row[15], workbook.datemode))
            except (ValueError, TypeError):
                planned_completion_date = None

            try:
                revised_completion_date = datetime(*xlrd.xldate_as_tuple(row[16], workbook.datemode))
            except (ValueError, TypeError):
                # Could not parse it
                revised_completion_date = None

            try:
                actual_completion_date = datetime(*xlrd.xldate_as_tuple(row[17], workbook.datemode))
            except (ValueError, TypeError):
                actual_completion_date = None

            try:
                status_date = datetime(*xlrd.xldate_as_tuple(row[18], workbook.datemode))
            except (ValueError, TypeError):
                status_date = None

            try:
                census_tract = float(row[9])
            except ValueError:
                census_tract = 0

            t = ThreeOneOne.objects.create(
                csr=row[0],
                status=row[1],
                request_type=row[2],
                description=unicode(row[3]),
                date_received=date_received,
                street_address=row[7],
                community=row[8],
                census_tract=census_tract,
                priority=row[10],
                method=row[11],
                parcel_number=row[12],
                date_answered=date_answered,
                user_id=row[14],
                planned_completion_date=planned_completion_date,
                revised_completion_date=revised_completion_date,
                actual_completion_date=actual_completion_date,
                status_date=status_date,
                assignee_id=row[19],
            )

            self.stdout.write('- Just did %s\n' % t)
