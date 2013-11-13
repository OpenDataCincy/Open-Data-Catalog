# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ThreeOneOne.method'
        db.alter_column(u'api_threeoneone', 'method', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'ThreeOneOne.method'
        db.alter_column(u'api_threeoneone', 'method', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'api.threeoneone': {
            'Meta': {'object_name': 'ThreeOneOne'},
            'actual_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'assignee_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'census_tract': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'csr': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'date_answered': ('django.db.models.fields.DateField', [], {}),
            'date_received': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'parcel_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'planned_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'request_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'revised_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['api']