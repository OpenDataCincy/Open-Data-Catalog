# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BikeRack'
        db.create_table(u'api_bikerack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rack_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('placement', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rack_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'api', ['BikeRack'])


    def backwards(self, orm):
        # Deleting model 'BikeRack'
        db.delete_table(u'api_bikerack')


    models = {
        u'api.arrest': {
            'Meta': {'object_name': 'Arrest'},
            'anon_arrest_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'anon_home_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'arrest_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'arrest_disp_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'arrest_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'badge_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'charge_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'charge_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'control_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'dob_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'event_time': ('django.db.models.fields.TimeField', [], {}),
            'home_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'home_city': ('django.db.models.fields.CharField', [], {'default': "u'Cincinnati'", 'max_length': '50', 'blank': 'True'}),
            'home_state': ('django.db.models.fields.CharField', [], {'default': "u'OH'", 'max_length': '2', 'blank': 'True'}),
            'home_zip': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nature': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'officer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'ra': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'report_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'seccode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'secno': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
        },
        u'api.bikerack': {
            'Meta': {'object_name': 'BikeRack'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'placement': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rack_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rack_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'api.cincinnatipolice': {
            'Meta': {'object_name': 'CincinnatiPolice'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'anon_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'event_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
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