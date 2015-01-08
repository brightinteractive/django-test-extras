# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django_migration_fixture import fixture
import test_app


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(test_app, 'painters.json')),
    ]
