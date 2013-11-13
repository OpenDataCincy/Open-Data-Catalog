# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ThreeOneOne'
        db.create_table(u'api_threeoneone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csr', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('request_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('date_received', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('community', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('census_tract', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parcel_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('date_answered', self.gf('django.db.models.fields.DateField')()),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('planned_completion_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('revised_completion_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('actual_completion_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('status_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('assignee_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
        ))
        db.send_create_signal(u'api', ['ThreeOneOne'])


    def backwards(self, orm):
        # Deleting model 'ThreeOneOne'
        db.delete_table(u'api_threeoneone')


    models = {
        u'api.threeoneone': {
            'Meta': {'object_name': 'ThreeOneOne'},
            'actual_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'assignee_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'census_tract': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'csr': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'date_answered': ('django.db.models.fields.DateField', [], {}),
            'date_received': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'parcel_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'planned_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'request_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'revised_completion_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['api']