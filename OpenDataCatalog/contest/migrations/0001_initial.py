# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contest'
        db.create_table(u'contest_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('vote_frequency', self.gf('django.db.models.fields.IntegerField')()),
            ('rules', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'contest', ['Contest'])

        # Adding model 'Entry'
        db.create_table(u'contest_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('nominator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nominator_link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nominator_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Not Released', max_length=255)),
            ('links', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data_owner', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rejected_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['contest.Contest'])),
            ('vote_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'contest', ['Entry'])

        # Adding model 'Vote'
        db.create_table(u'contest_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contest.Entry'])),
        ))
        db.send_create_signal(u'contest', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Contest'
        db.delete_table(u'contest_contest')

        # Deleting model 'Entry'
        db.delete_table(u'contest_entry')

        # Deleting model 'Vote'
        db.delete_table(u'contest_vote')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contest.contest': {
            'Meta': {'object_name': 'Contest'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vote_frequency': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contest.entry': {
            'Meta': {'object_name': 'Entry'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['contest.Contest']"}),
            'data_owner': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'links': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'nominator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nominator_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nominator_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rejected_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Not Released'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vote_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'contest.vote': {
            'Meta': {'object_name': 'Vote'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contest.Entry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['contest']