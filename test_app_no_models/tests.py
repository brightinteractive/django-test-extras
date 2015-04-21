from django.test.testcases import TestCase
import test_app_no_models
import os
from test_extras.testrunners import get_coverage_files


class CoverageTests(TestCase):

    def test_get_coverage_gets_the_expected_files(self):
        coverage_files = get_coverage_files(['test_app_no_models'], ignore_dirs=[], ignore_files=['tests.py'])
        expected_coverage_file_names = ['__init__.py', 'views.py']
        full_paths = [os.path.join(os.path.dirname(test_app_no_models.__file__), file_name) for file_name in expected_coverage_file_names]
        self.assertEqual(len(full_paths), len(coverage_files))
        self.assertTrue(all(path in coverage_files for path in full_paths))
