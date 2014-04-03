from django.db import models

from geopy import geocoders
from geopy.geocoders.googlev3 import GQueryError, GTooManyQueriesError

from streetaddress import StreetAddressParser

from urllib2 import HTTPError


class CincinnatiPolice(models.Model):
    event_number = models.CharField(max_length=50, help_text=u'Event #')
    create_date = models.DateField(null=True)
    address = models.CharField(max_length=30, blank=True, default='')
    anon_address = models.CharField(max_length=50, blank=True, default='')
    description = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True, default='')

    latitude = models.FloatField(null=True, default=0.0)
    longitude = models.FloatField(null=True, default=0.0)

    def __unicode__(self):
        return u'%s' % self.description

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.address = self.address.strip()
        self.description = self.description.strip()
        self.location = self.location.strip()

        if self.address and not self.anon_address:
            # Let's anonymize this address
            address = StreetAddressParser().parse(self.address)

            if address.get('block') and int(address.get('block')) > 0:
                self.anon_address = u'%s block of %s' % (address.get('block'), address.get('street_full'))
            else:
                self.anon_address = self.address

        return super(CincinnatiPolice, self).save(force_insert, force_update, using, update_fields)


class Arrest(models.Model):
    arrest_type = models.IntegerField(default=0, null=True)
    control_number = models.IntegerField(default=0, null=True)
    rac = models.CharField(max_length=10, blank=True, default='')  # TODO: Determine meaning
    sex = models.CharField(max_length=1, default='', blank=True)
    ra = models.IntegerField(default=0, null=True)  # TODO: Determine meaning
    event_date = models.DateField()
    event_time = models.TimeField()
    secno = models.CharField(max_length=20, blank=True, default='')
    seccode = models.CharField(max_length=20, blank=True, default='')
    dob_year = models.IntegerField(null=True, blank=True)
    charge_code = models.IntegerField(null=True, blank=True)
    charge_type = models.IntegerField(null=True, blank=True)
    arrest_disp_code = models.IntegerField(null=True, blank=True)
    badge_number = models.IntegerField(null=True, blank=True)
    officer = models.CharField(max_length=30, blank=True, default='')
    nature = models.IntegerField(null=True, blank=True)
    report_number = models.CharField(max_length=30, default='', blank=True)

    # These will be anonymized into new fields
    arrest_address = models.CharField(max_length=50, default='', blank=True)
    home_address = models.CharField(max_length=50, default='', blank=True)
    home_city = models.CharField(max_length=50, default=u'Cincinnati', blank=True)
    home_state = models.CharField(max_length=2, default=u'OH', blank=True)
    home_zip = models.IntegerField(null=True)

    anon_arrest_address = models.CharField(max_length=50, default='', blank=True)
    anon_home_address = models.CharField(max_length=50, default='', blank=True)

    def __unicode__(self):
        return u'Arrest at %s' % self.anon_arrest_address

    def description(self):
        """
         A description field to match the other models
        """
        if self.anon_arrest_address:
            return u'Arrest at %s' % self.anon_arrest_address
        else:
            return u'Arrest on %s' % self.event_date

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.arrest_address = self.arrest_address.strip()
        self.home_address = self.home_address.strip()

        if self.arrest_address and not self.anon_arrest_address:
            address = StreetAddressParser().parse(self.arrest_address)

            if address.get('block') and int(address.get('block')) > 0:
                self.anon_arrest_address = u'%s block of %s' % (address.get('block'), address.get('street_full'))
            else:
                self.anon_arrest_address = self.arrest_address

        if self.home_address and not self.anon_home_address:
            address = StreetAddressParser().parse(self.home_address)

            if address.get('block') and int(address.get('block')) > 0:
                self.anon_home_address = u'%s block of %s' % (address.get('block'), address.get('street_full'))
            else:
                self.anon_home_address = self.home_address

        return super(Arrest, self).save(force_insert, force_update, using, update_fields=update_fields)


class ThreeOneOne(models.Model):
    csr = models.CharField(max_length=15, help_text=u'CSR #')
    status = models.CharField(max_length=20, help_text=u'Status of the call')
    request_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, default=u'')
    date_received = models.DateTimeField(null=True)
    street_address = models.CharField(max_length=100, blank=True)
    community = models.CharField(max_length=100, blank=True)
    census_tract = models.FloatField(null=True, blank=True)
    priority = models.CharField(max_length=20, blank=True)
    method = models.CharField(max_length=50, blank=True)
    parcel_number = models.CharField(max_length=30, blank=True, help_text=u'Land parcel number')
    date_answered = models.DateField()
    user_id = models.CharField(max_length=20)
    planned_completion_date = models.DateField(null=True)
    revised_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True)
    status_date = models.DateField(null=True)
    assignee_id = models.CharField(max_length=20, blank=True,)

    latitude = models.FloatField(null=True, default=0.0)
    longitude = models.FloatField(null=True, default=0.0)

    class Meta:
        verbose_name = u'311 report'
        verbose_name_plural = u'311 reports'

    def __unicode__(self):

        return unicode(self.request_type)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.latitude == 0 and self.longitude == 0:

            address = '%s Cincinnati, OH' % self.street_address

            google = geocoders.GoogleV3()

            try:
                place, (latitude, longitude) = google.geocode(address, exactly_one=False)[0]
            except GQueryError:
                latitude = 0
                longitude = 0
            except GTooManyQueriesError:
                latitude = 0
                longitude = 0
            except HTTPError, e:
                latitude = 0
                longitude = 0

            self.latitude = latitude
            self.longitude = longitude

        return super(ThreeOneOne, self).save(force_insert, force_update, using, update_fields)


class BikeRack(models.Model):
    rack_number = models.IntegerField(null=True, help_text=u'The unique rack identifier')
    neighborhood = models.CharField(max_length=200, help_text=u'Where it is, Cincy-hood-wise')
    location = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, default=0)
    longitude = models.FloatField(null=True, default=0)

    placement = models.CharField(max_length=100)
    rack_type = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def __unicode__(self):
        return u'Bike rack at %s' % self.street

    class Meta:
        ordering = ['rack_number', ]


class GenericData(models.Model):
    """
    A data model for various data sets that can live together for simplicity.
    For use in the API.
    """
    data_type = models.CharField(max_length=100, help_text=u'The specific type of data.')
    description = models.TextField(blank=True, default=u'')
    user_id = models.CharField(max_length=100, blank=True, default=u'')
    community = models.CharField(max_length=100, blank=True, default=u'')
    location = models.CharField(max_length=200, blank=True, default=u'')
    address = models.CharField(max_length=200, blank=True, default=u'')
    anon_location = models.CharField(max_length=200, blank=True, default=u'')
    anon_address = models.CharField(max_length=200, blank=True, default=u'')
    street_direction = models.CharField(max_length=2, blank=True, default=u'')
    latitude = models.FloatField(null=True, default=0)
    longitude = models.FloatField(null=True, default=0)

    date_received = models.DateField(null=True, blank=True)
    time_received = models.TimeField(null=True, blank=True)
    date_planned_completion = models.DateField(null=True, blank=True)

    x_coordinate = models.FloatField(null=True, default=0)
    y_coordinate = models.FloatField(null=True, default=0)
    parcel = models.CharField(max_length=100, blank=True)  # It may have alpha characters in it.
    census_tract = models.FloatField(null=True, blank=True)

    request_type = models.CharField(max_length=50, blank=True)
    csr = models.CharField(max_length=15, blank=True, help_text=u'CSR #')
    approved = models.CharField(max_length=3, blank=True)
    status = models.CharField(max_length=30, blank=True)
    comp_type = models.CharField(max_length=50, blank=True, help_text=u'Composition Type', default=u'')
    sub_type = models.CharField(max_length=50, blank=True, default=u'')

    def __unicode__(self):
        if self.data_type == 'vacant':
            return u'Vacant lot at %s' % self.address
        
        return u'Record: %s' % self.data_type

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.location = self.location.strip()
        self.address = self.address.strip()

        if self.location and not self.anon_location:
            address = StreetAddressParser().parse(self.location)

            if address.get('block') and int(address.get('block')) > 0:
                self.anon_location = u'%s block of %s' % (address.get('block'), address.get('street_full'))
            else:
                self.anon_location = self.location

        if self.address and not self.anon_address:
            address = StreetAddressParser().parse(self.address)

            if address.get('block') and int(address.get('block')) > 0:
                self.anon_address = u'%s block of %s' % (address.get('block'), address.get('street_full'))
            else:
                self.anon_address = self.address

        return super(GenericData, self).save(force_insert, force_update, using, update_fields=update_fields)




# class AreaOfInterest(models.Model):
#     city = models.CharField(max_length=100, default=u'Cincinnati')
#     state = models.CharField(max_length=2, blank=True, default=u'OH')
#     community = models.CharField(max_length=100, blank=True)

