# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
WebDriver Plus related test code.

This is in a seperate file, not testcases.py, so that testcases.py doesn't
have to depend on selenium or webdriverplus.
"""

from __future__ import absolute_import

from bs4 import BeautifulSoup
from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from test_extras.testcases import DataPreservingTransactionTestCaseMixin
from webdriverplus import WebDriver
import django.test

# Default to Firefox but allow this to be overridden in Django settings
browser = getattr(settings, 'WEBDRIVERPLUS_BROWSER', 'firefox')


class WebDriverPlusTestCase(DataPreservingTransactionTestCaseMixin, django.test.LiveServerTestCase):
    # How long to wait for pages to load or elements to become available.
    # Can be overridden by subclasses (not tested yet!).
    PAGE_TIMEOUT_SECONDS = 10

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

    def find_and_wait(self, *args, **kwargs):
        return WebDriverWait(self.browser, self.PAGE_TIMEOUT_SECONDS).until(
            lambda browser: browser.find(*args, **kwargs)
            )

    def find_hidden_text(self, *args, **kwargs):
        element = self.browser.find(*args, **kwargs)
        return self.get_hidden_text(element)

    def get_hidden_text(self, element):
        """
        Like element.text, but doesn't just return an empty string if the
        element is hidden.
        """

        # element.text will work if the element is visible, but if it or
        # any of its parents are hidden it won't, so we resort to parsing the
        # HTML
        soup = BeautifulSoup(element.html)
        return soup.text
