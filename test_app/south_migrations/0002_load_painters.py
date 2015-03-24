# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from django.db import models
from test_app.south_migrations import FixtureMigration
import os.path


THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
APP_DIR = os.path.split(THIS_DIR)[0]
FIXTURES_DIR = os.path.join(APP_DIR, 'fixtures')


class Migration(FixtureMigration):
    fixture = os.path.join(FIXTURES_DIR, 'painters.json')

    models = {
        'test_app.painter': {
            'Meta': {'object_name': 'Painter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_app']
    symmetrical = True
