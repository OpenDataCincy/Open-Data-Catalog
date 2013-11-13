from django.db import models


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
    method = models.CharField(max_length=20, blank=True)
    parcel_number = models.CharField(max_length=30, blank=True, help_text=u'Land parcel number')
    date_answered = models.DateField()
    user_id = models.CharField(max_length=20)
    planned_completion_date = models.DateField(null=True)
    revised_completion_date = models.DateField(null=True)
    actual_completion_date = models.DateField(null=True)
    status_date = models.DateField(null=True)
    assignee_id = models.CharField(max_length=20)

    latitude = models.FloatField(null=True, default=0.0)
    longitude = models.FloatField(null=True, default=0.0)
