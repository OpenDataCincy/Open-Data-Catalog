# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Arrest'
        db.create_table(u'api_arrest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arrest_type', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('control_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('rac', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True)),
            ('ra', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('event_date', self.gf('django.db.models.fields.DateField')()),
            ('event_time', self.gf('django.db.models.fields.TimeField')()),
            ('secno', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('seccode', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('dob_year', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('charge_code', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('charge_type', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arrest_disp_code', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('badge_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('officer', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('nature', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arrest_address', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('home_address', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('home_city', self.gf('django.db.models.fields.CharField')(default=u'Cincinnati', max_length=50, blank=True)),
            ('home_state', self.gf('django.db.models.fields.CharField')(default=u'OH', max_length=2, blank=True)),
            ('anon_arrest_address', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('anon_home_address', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
        ))
        db.send_create_signal(u'api', ['Arrest'])


    def backwards(self, orm):
        # Deleting model 'Arrest'
        db.delete_table(u'api_arrest')


    models = {
        u'api.arrest': {
            'Meta': {'object_name': 'Arrest'},
            'anon_arrest_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'anon_home_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'arrest_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'arrest_disp_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arrest_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'badge_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'charge_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'charge_type': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'control_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'dob_year': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'event_time': ('django.db.models.fields.TimeField', [], {}),
            'home_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'home_city': ('django.db.models.fields.CharField', [], {'default': "u'Cincinnati'", 'max_length': '50', 'blank': 'True'}),
            'home_state': ('django.db.models.fields.CharField', [], {'default': "u'OH'", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nature': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'officer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'ra': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rac': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'seccode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'secno': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1', 'blank': 'True'})
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