# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS


class EnableDatabaseLoggingContext(object):
    """
    Allows you to enable SQL logging in Django tests despite the fact that
    Django forces DEBUG to False when tests are run.

    Use as follows:

        with EnableDatabaseLoggingContext():
            do_something_that_uses_the_database()
    """
    def __init__(self):
        using = DEFAULT_DB_ALIAS
        self.connection = connections[using]

    def __enter__(self):
        self.old_debug_cursor = self.connection.use_debug_cursor
        self.connection.use_debug_cursor = True
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.connection.use_debug_cursor = self.old_debug_cursor
