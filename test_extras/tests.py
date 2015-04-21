# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
import os
from django.core.exceptions import ImproperlyConfigured

from django.test import TestCase
from django.test.utils import override_settings
import test_extras.management
from test_extras.testrunners import get_coverage_files


class CoverageTests(TestCase):

    @override_settings(INSTALLED_APPS=[])
    def test_get_coverage_raises_error_if_app_is_not_installed(self):
        with self.assertRaises(ImproperlyConfigured):
            get_coverage_files(['test'], ignore_dirs=[], ignore_files=[])

