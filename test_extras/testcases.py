# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from StringIO import StringIO
from django.core import management
from django.core import serializers
from django.core.management import call_command
from django.core.management.commands import flush
from django.db import transaction, connection, connections, DEFAULT_DB_ALIAS, reset_queries, router
import os
import tempfile


class SkipFlushCommand(flush.Command):
    def handle_noargs(self, **options):
        return

    def __enter__(self):
        # hold onto the original and replace flush command with a no-op
        self.original_flush_command = management._commands['flush']
        management._commands['flush'] = self

    def __exit__(self, exc_type, exc_value, traceback):
        # unpatch flush back to the original
        management._commands['flush'] = self.original_flush_command


class NonFlushingTransactionTestCaseMixin(object):
    """
    Mixin that prevents the database from being flushed in TransactionTestCase
     subclasses.

    Only suitable for tests that don't change any database data - if your test
    does change the database then use DataPreservingTransactionTestCaseMixin
    instead.

    Only works if you mix it in first like this:
       class MyTestCase(NonFlushingTransactionTestCaseMixin, TransactionTestCase):
    not like this:
       class MyTestCase(TransactionTestCase, NonFlushingTransactionTestCaseMixin):
    """
    def _fixture_setup(self):
        """
        Overrides TransactionTestCase._fixture_setup() and replaces the flush
        command with a dummy command whilst it is running to prevent it from
        flushing the database.
        Django 1.4 flushes the database on fixture setup, but Django
        1.5 flushes the database on fixture teardown.
        """
        with SkipFlushCommand():
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_setup()

    def _fixture_teardown(self):
        """
        Overrides TransactionTestCase._fixture_teardown() and replaces
        the flush command with a dummy command whilst it is running to
        prevent it from flushing the database.
        Django 1.4 flushes the database on fixture setup, but Django
        1.5 flushes the database on fixture teardown.
        """
        with SkipFlushCommand():
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_teardown()


class DataPreservingTransactionTestCaseMixin(NonFlushingTransactionTestCaseMixin):
    """
    Mixin that prevents the database from being flushed in TransactionTestCase
     subclasses and that saves the database contents before each test and
     restores it afterwards, so it is suitable for use with tests that update
     the database.

    Only works if you mix it in first like this:
       class MyTestCase(DataPreservingTransactionTestCaseMixin, TransactionTestCase):
    not like this:
       class MyTestCase(TransactionTestCase, DataPreservingTransactionTestCaseMixin):
    """

    def setUp(self):
        super(DataPreservingTransactionTestCaseMixin, self).setUp()

        self.database_dumpfilepaths = {}

        # If the test case has a multi_db=True flag, back up all databases.
        # Otherwise, just use default.
        # This mirrors TransactionTestCase's behaviour
        if getattr(self, 'multi_db', False):
            databases = connections
        else:
            databases = [DEFAULT_DB_ALIAS]
        for db in databases:
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as dumpfile:
                call_command('dumpdata',
                    verbosity=0, interactive=False,
                    database=db, use_base_manager=True, format='json', stdout=dumpfile)
            self.database_dumpfilepaths[db] = dumpfile.name

    def tearDown(self):
        super(DataPreservingTransactionTestCaseMixin, self).tearDown()

        for (db, dumpfilepath) in self.database_dumpfilepaths.iteritems():
            call_command('superflush', verbosity=0, interactive=False, database=db)
            call_command('loaddata', dumpfilepath, verbosity=0, interactive=False)
            os.remove(dumpfilepath)
