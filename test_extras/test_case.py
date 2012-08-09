# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.core import management
from django.core.management.commands import flush


class SkipFlushCommand(flush.Command):
    def handle_noargs(self, **options):
        return


class NonFlushingTransactionTestCaseMixin(object):
    """
    Mixin that prevents the database from being flushed in TransactionTestCase
     subclasses.

    If you mix this in then your tests must delete any data that they create,
    instead of relying on TransactionTestCase's flushing to do it for then.

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
        original_flush_command = management._commands['flush']
        try:
            management._commands['flush'] = SkipFlushCommand()
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_setup()
        finally:
            # unpatch flush back to the original
            management._commands['flush'] = original_flush_command
