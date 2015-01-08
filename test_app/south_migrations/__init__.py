# -*- coding: utf-8 -*-
# (c) 2011-2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from dingus import patch
from django.db.models import get_app
import os
from south.v2 import DataMigration


class FixtureMigration(DataMigration):
    """
    Superclass for migrations that load data from a fixture.

    Subclasses should define ``fixture`` as a the name of the JSON file
    containing the data to load.
    """

    app_name = 'test_app'

    def fixture_path(self):
        app_path = os.path.dirname(get_app(self.app_name).__file__)
        fixture_path = os.path.join(app_path, 'fixtures', self.fixture)
        return fixture_path

    def get_fixture(self):
        return open(self.fixture_path()).read()

    def forwards(self, orm):
        # Make sure that the fixture file actually exists, because the
        # loaddata command does not raise an exception if no fixtures were
        # found which can lead to difficult to debug errors if the fixture
        # filename is specified incorrectly.
        open(self.fixture_path(), 'rb').close()

        _get_model = lambda model_identifier: orm[model_identifier]

        with patch('django.core.serializers.python._get_model', _get_model):
            from django.core.management import call_command
            call_command("loaddata", self.fixture)

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")
