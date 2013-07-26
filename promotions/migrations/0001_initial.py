# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Code'
        db.create_table(u'promotions_code', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, primary_key=True)),
        ))
        db.send_create_signal(u'promotions', ['Code'])


    def backwards(self, orm):
        # Deleting model 'Code'
        db.delete_table(u'promotions_code')


    models = {
        u'promotions.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'})
        }
    }

    complete_apps = ['promotions']