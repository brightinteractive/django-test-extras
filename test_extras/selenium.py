# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Selenium related test code.

This is in a seperate file, not testcases.py, so that testcases.py doesn't
have to depend on selenium.
"""

from __future__ import absolute_import

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from test_extras.testcases import DataPreservingTransactionTestCaseMixin
import selenium.webdriver.firefox.webdriver

# Default to Firefox but allow this to be overridden in Django settings
WebDriver = getattr(settings, 'WEBDRIVER_CLASS', selenium.webdriver.firefox.webdriver.WebDriver)


class SeleniumTestCase(DataPreservingTransactionTestCaseMixin, StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # We quit selenium before calling super tearDownClass() because we
        # were getting "Failed to shutdown the live test server in 2 seconds."
        # errors from StoppableWSGIServer.shutdown() when we called super
        # tearDownClass first.
        cls.browser.quit()
        super(SeleniumTestCase, cls).tearDownClass()
