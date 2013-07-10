# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plan'
        db.create_table(u'subscriptions_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stripe_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('interval', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'subscriptions', ['Plan'])

        # Adding unique constraint on 'Plan', fields ['amount', 'price', 'interval']
        db.create_unique(u'subscriptions_plan', ['amount', 'price', 'interval'])

        # Adding model 'Subscription'
        db.create_table(u'subscriptions_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(related_name='_subscription', unique=True, to=orm['customers.Customer'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['subscriptions.Plan'])),
            ('started', self.gf('django.db.models.fields.DateTimeField')()),
            ('canceled', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ended', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('current_period_start', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('current_period_end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'subscriptions', ['Subscription'])


    def backwards(self, orm):
        # Removing unique constraint on 'Plan', fields ['amount', 'price', 'interval']
        db.delete_unique(u'subscriptions_plan', ['amount', 'price', 'interval'])

        # Deleting model 'Plan'
        db.delete_table(u'subscriptions_plan')

        # Deleting model 'Subscription'
        db.delete_table(u'subscriptions_subscription')


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
        u'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'card_fingerprint': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'card_kind': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'card_last_4': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20'}),
            'state': ('django_localflavor_us.models.USStateField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'subscriptions.plan': {
            'Meta': {'unique_together': "(('amount', 'price', 'interval'),)", 'object_name': 'Plan'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'subscriptions.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'canceled': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'current_period_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'current_period_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'_subscription'", 'unique': 'True', 'to': u"orm['customers.Customer']"}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['subscriptions.Plan']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['subscriptions']