# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Selenium related test code.

This is in a seperate file, not testcases.py, so that testcases.py doesn't
have to depend on selenium.
"""

from __future__ import absolute_import

from selenium.webdriver.firefox.webdriver import WebDriver
from test_extras.testcases import DataPreservingTransactionTestCaseMixin
import django.test


class SeleniumTestCase(DataPreservingTransactionTestCaseMixin, django.test.LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # We quit selenium before calling super tearDownClass() because we
        # were getting "Failed to shutdown the live test server in 2 seconds."
        # errors from StoppableWSGIServer.shutdown() when we called super
        # tearDownClass first.
        cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()
