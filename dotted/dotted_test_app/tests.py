# -*- coding: utf-8 -*-
# (c) 2015 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
import os
from django.test.testcases import TestCase
from dotted import dotted_test_app
from test_extras.testrunners import get_coverage_files


class CoverageTests(TestCase):

    def test_get_coverage_works_for_dotted_app_labels(self):
        files = get_coverage_files(
            ['dotted.dotted_test_app'],
            ignore_dirs=[],
            ignore_files=['tests.py']
        )

        self.assertEqual(1, len(files))
        expected_path = os.path.join(os.path.dirname(dotted_test_app.__file__), '__init__.py')
        self.assertIn(expected_path, files)
