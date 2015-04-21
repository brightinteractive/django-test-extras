# -*- coding: utf-8 -*-
# (c) 2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.test import TestCase, TransactionTestCase
import test_app
import os
from test_extras.testcases import DataPreservingTransactionTestCaseMixin
from test_app.models import Painter
from test_extras.testrunners import get_coverage_files


class TestDataPreserving(DataPreservingTransactionTestCaseMixin, TransactionTestCase):
    def test_migration_data_present_in_test_1(self):
        painter = Painter.objects.get(id=1)
        self.assertEqual('Pablo Picasso', painter.name)

    def test_migration_data_present_in_test_2(self):
        """
        Test that the data is still available in a second test method
        """
        painter = Painter.objects.get(id=1)
        self.assertEqual('Pablo Picasso', painter.name)


class HookTests(TestCase):
    """
    Tests that HookingTextTestRunner is active and working
    """
    addSuccess_called = False

    def addSuccess(self):
        # Needs to be a class variable, not an instance variable, because
        # each test method is run using a different instance of HookTests
        HookTests.addSuccess_called = True

    def test_1_success(self):
        pass

    def test_2_check(self):
        self.assertTrue(HookTests.addSuccess_called)


class CoverageTests(TestCase):

    def test_get_coverage_gets_the_expected_files(self):
        coverage_files = get_coverage_files(['test_app'], ignore_dirs=['south_migrations', 'migrations', 'fixtures'], ignore_files=['tests.py'])
        expected_coverage_file_names = ['__init__.py', 'views.py', 'models.py']
        full_paths = [os.path.join(os.path.dirname(test_app.__file__), file_name) for file_name in expected_coverage_file_names]
        self.assertEqual(len(full_paths), len(coverage_files))
        self.assertTrue(all(path in coverage_files for path in full_paths))
