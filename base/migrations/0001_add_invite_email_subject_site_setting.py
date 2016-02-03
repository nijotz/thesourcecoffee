# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.SiteSetting.objects.create(key="rewards.invite_email_subject",
            value="A friend has invited you to The Source Coffee!",
            description="The subject line for the invite email sent via the rewards app.")

    def backwards(self, orm):
        "Write your backwards methods here."
        orm.SiteSetting.objects.get(key="rewards.invite_email_subject").delete()

    models = {
        u'base.sitesetting': {
            'Meta': {'object_name': 'SiteSetting'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'value': ('json_field.fields.JSONField', [], {'default': "u'null'"})
        }
    }

    complete_apps = ['base']
    symmetrical = True
