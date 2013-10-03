# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Credit.timestamp'
        db.alter_column('schedule_credit', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Adding field 'Coupon.credit'
        db.add_column('schedule_coupon', 'credit',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['schedule.Credit'], unique=True, null=True),
                      keep_default=False)


        # Changing field 'Coupon.timestamp'
        db.alter_column('schedule_coupon', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'Credit.timestamp'
        db.alter_column('schedule_credit', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())
        # Deleting field 'Coupon.credit'
        db.delete_column('schedule_coupon', 'credit_id')


        # Changing field 'Coupon.timestamp'
        db.alter_column('schedule_coupon', 'timestamp', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'schedule.assignment': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Assignment'},
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'defer_code': ('django.db.models.fields.CharField', [], {'default': "'7c62f8d2de3d43c1b2d7fa8cbc07bfb9'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'credit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['schedule.Credit']", 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True'}),
            'skipped_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coupons'", 'to': "orm['schedule.NamelessWorker']"})
        },
        'schedule.credit': {
            'Meta': {'ordering': "('timestamp',)", 'object_name': 'Credit'},
            'debit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'credits'", 'null': 'True', 'to': "orm['schedule.Debit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skipped_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'deferral_exempt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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