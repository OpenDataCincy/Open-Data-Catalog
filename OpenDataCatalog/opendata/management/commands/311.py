from django.core.management.base import BaseCommand, CommandError

import xlrd

from geopy import geocoders


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
        count = 0
        addresses = {}
        for i in range(sheet.nrows):
            row = sheet.row_values(i)

            # row[0] is CSR#
            # row[1] is status
            # row[2] is the type
            # row[3] is description
            # row[4] is the date MM/DD/YYYY HH:MM:SS AM

            if 'trash' in row[2]:
                count += 1

                if row[7]:
                    address = u'%s Cincinnati, OH' % row[7]

                    if not address in addresses:
                        place, (lat, lon) = google.geocode(address)
                        addresses[address] = {
                            'lat': lat,
                            'lon': lon,
                        }
                    else:
                        lat = addresses[address].get('lat')
                        lon = addresses[address].get('lon')

                    js = 'var myLatLng = new google.maps.LatLng(%s, %s); ' % (lat, lon)
                    js += 'var marker = new google.maps.Marker({ position: myLatLng, title: "%s" }); ' % row[2]
                    js += 'marker.setMap(map);'

                    self.stdout.write(js)
                    self.stdout.write("\n")

                if count == 100:
                    break

        print count
