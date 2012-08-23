# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
WebDriver Plus related test code.

This is in a seperate file, not testcases.py, so that testcases.py doesn't
have to depend on selenium or webdriverplus.
"""

from __future__ import absolute_import

from django.conf import settings
from webdriverplus import WebDriver
from test_extras.testcases import DataPreservingTransactionTestCaseMixin
import django.test

# Default to Firefox but allow this to be overridden in Django settings
browser = getattr(settings, 'WEBDRIVERPLUS_BROWSER', 'firefox')


class WebDriverPlusTestCase(DataPreservingTransactionTestCaseMixin, django.test.LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver(browser=browser)
        super(WebDriverPlusTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # We quit selenium before calling super tearDownClass() because we
        # were getting "Failed to shutdown the live test server in 2 seconds."
        # errors from StoppableWSGIServer.shutdown() when we called super
        # tearDownClass first.
        cls.browser.quit()
        super(WebDriverPlusTestCase, cls).tearDownClass()
