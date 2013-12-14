# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CincinnatiPolice'
        db.create_table(u'api_cincinnatipolice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('create_date', self.gf('django.db.models.fields.DateField')()),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
        ))
        db.send_create_signal(u'api', ['CincinnatiPolice'])


    def backwards(self, orm):
        # Deleting model 'CincinnatiPolice'
        db.delete_table(u'api_cincinnatipolice')


    models = {
        u'api.cincinnatipolice': {
            'Meta': {'object_name': 'CincinnatiPolice'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'event_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'})
        },
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