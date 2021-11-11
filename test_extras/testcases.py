# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from io import StringIO
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
        """
        # hold onto the original and replace flush command with a no-op
        # commands = management._commands
        commands = management.get_commands()
        original_flush_command = commands['flush']
        try:
            commands['flush'] = SkipFlushCommand()
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_setup()
        finally:
            # unpatch flush back to the original
            commands['flush'] = original_flush_command


class DataPreservingTransactionTestCaseMixin(NonFlushingTransactionTestCaseMixin):
    serialized_rollback = True
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
