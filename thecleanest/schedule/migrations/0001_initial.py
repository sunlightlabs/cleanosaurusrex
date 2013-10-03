# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NamelessWorker'
        db.create_table('schedule_namelessworker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('avatar_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('schedule', ['NamelessWorker'])

        # Adding model 'Assignment'
        db.create_table('schedule_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['schedule.NamelessWorker'])),
            ('defer_code', self.gf('django.db.models.fields.CharField')(default='fe7dba40458e40ef9ed70a6063750489', max_length=32)),
        ))
        db.send_create_signal('schedule', ['Assignment'])

        # Adding model 'Debit'
        db.create_table('schedule_debit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='debits', to=orm['schedule.NamelessWorker'])),
            ('skipped_assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='debits', null=True, to=orm['schedule.Assignment'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('schedule', ['Debit'])

        # Adding model 'Credit'
        db.create_table('schedule_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('debit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credits', null=True, to=orm['schedule.Debit'])),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='credits', to=orm['schedule.NamelessWorker'])),
            ('skipped_date', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('schedule', ['Credit'])

        # Adding model 'Coupon'
        db.create_table('schedule_coupon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coupons', to=orm['schedule.NamelessWorker'])),
            ('skipped_date', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('schedule', ['Coupon'])

        # Adding model 'Rating'
        db.create_table('schedule_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ratings', to=orm['schedule.Assignment'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('subject_of_judgement', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('schedule', ['Rating'])


    def backwards(self, orm):
        # Deleting model 'NamelessWorker'
        db.delete_table('schedule_namelessworker')

        # Deleting model 'Assignment'
        db.delete_table('schedule_assignment')

        # Deleting model 'Debit'
        db.delete_table('schedule_debit')

        # Deleting model 'Credit'
        db.delete_table('schedule_credit')

        # Deleting model 'Coupon'
        db.delete_table('schedule_coupon')

        # Deleting model 'Rating'
        db.delete_table('schedule_rating')


    models = {
        'schedule.assignment': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Assignment'},
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'defer_code': ('django.db.models.fields.CharField', [], {'default': "'5a87c39c1c894625800ab27e4d753051'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True'}),
            'skipped_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coupons'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.credit': {
            'Meta': {'ordering': "('timestamp',)", 'object_name': 'Credit'},
            'debit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credits'", 'null': 'True', 'to': "orm['schedule.Debit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skipped_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credits'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.debit': {
            'Meta': {'ordering': "('timestamp',)", 'object_name': 'Debit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skipped_assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'debits'", 'null': 'True', 'to': "orm['schedule.Assignment']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'debits'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.namelessworker': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'NamelessWorker'},
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'schedule.rating': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Rating'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': "orm['schedule.Assignment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject_of_judgement': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['schedule']