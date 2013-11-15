from django.db import models

from geopy import geocoders
from geopy.geocoders.googlev3 import GQueryError, GTooManyQueriesError


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
                place, (lat, lon) = google.geocode(address, exactly_one=False)[0]
            except GQueryError:
                lat = 0
                lon = 0
            except GTooManyQueriesError:
                lat = 0
                lon = 0

            self.latitude = lat
            self.longitude = lon

        return super(ThreeOneOne, self).save(force_insert, force_update, using, update_fields)
