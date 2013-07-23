# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf import settings
from django.utils import unittest
import coverage
import django.test.simple
import os.path
import pdb
import xmlrunner
profile = None  # Fool pylint about double import
try:
    import cProfile as profile
except ImportError:
    if not profile:
        import profile


try:
    TextTestResult = unittest.TextTestResult
except AttributeError:
    TextTestResult = unittest._TextTestResult


class HookingTextTestResult(TextTestResult):
    """
    Allows test classes to define addSuccess addError or addFailure methods
    that get called when a test is successful, errors or fails.
    """
    def addSuccess(self, test):
        super(HookingTextTestResult, self).addSuccess(test)
        if hasattr(test, 'addSuccess'):
            test.addSuccess()

    def addError(self, test, err):
        super(HookingTextTestResult, self).addError(test, err)
        if hasattr(test, 'addError'):
            test.addError(err)

    def addFailure(self, test, err):
        super(HookingTextTestResult, self).addFailure(test, err)
        if hasattr(test, 'addFailure'):
            test.addFailure(err)


class HookingTextTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return HookingTextTestResult(self.stream, self.descriptions, self.verbosity)


def result_hook_wrap(TestRunner):
    class ResultHookTestRunner(TestRunner):
        def run_suite(self, suite, **kwargs):
            if TestRunner.run_suite != django.test.simple.DjangoTestSuiteRunner.run_suite:
                raise ValueError("run_suite was not the expected DjangoTestSuiteRunner.run_suite, some other code must have overridden it so it's not safe for this code to override it too")
            return HookingTextTestRunner(
                verbosity=self.verbosity, failfast=self.failfast).run(suite)
    return ResultHookTestRunner


class ProfileTestSuiteWrapper(object):
    def __init__(self, runner, *args, **kwargs):
        self.runner = runner

    def run_tests(self, *args, **kwargs):
        result = profile.runctx('self.runner.run_tests(*args, **kwargs)',
                       globals(),
                       locals(),
                       getattr(settings, 'TEST_PROFILE', None)
                       )
        return result


class CoverageTestSuiteWrapper(object):
    def __init__(self, runner, report_type, *args, **kwargs):
        self.runner = runner
        self.report_type = report_type

    def run_tests(self, *args, **kwargs):
        self._start_coverage()
        result = self.runner.run_tests(*args, **kwargs)
        self._finish_coverage()
        return result

    def _start_coverage(self):
        self.cov = coverage.coverage(branch=True)
        self.cov.erase()
        self.cov.start()

    def _finish_coverage(self):
        coverage_files = get_coverage_files(settings.TEST_COVERAGE_APPS,
                                            ignore_dirs=['tests'],
                                            ignore_files=['tests.py'])
        self.cov.stop()
        self.cov.save()
        reports = {'text': [self.cov.report],
                   'html': [self.cov.report, self.cov.html_report],
                   'xml': [self.cov.report, self.cov.xml_report]}
        for report in reports[self.report_type]:
            report(coverage_files)


def get_coverage_files_in_directory(dirname, ignore_dirs, ignore_files):
    """
    Return a list of all the python files under a given 'dirname' that
    should be included in a coverage report.
    """
    ret = []
    for (path, dirs, files) in os.walk(dirname):
        if os.path.basename(path) in ignore_dirs:
            continue

        for file in files:
            if not file.endswith('.py'):
                continue
            if file in ignore_files:
                continue
            ret.append(os.path.join(path, file))

    return ret


def get_coverage_files(app_labels, ignore_dirs, ignore_files):
    """
    Given a list of apps that are being tested (as strings),
    return a list of all the python files that should be included in
    a coverage report for that test.
    """
    from django.db.models import get_app

    ret = []

    for app_label in app_labels:
        module = get_app(app_label)
        dirname = os.path.dirname(module.__file__)
        ret.extend(get_coverage_files_in_directory(dirname, ignore_dirs, ignore_files))

    return ret


class ExceptionTestResultMixin(object):
    """
    A mixin class that can be added to any test result class.
    Drops into pdb on test errors/failures.
    """
    def addError(self, test, err):
        super(ExceptionTestResultMixin, self).addError(test, err)
        exctype, value, tb = err

        self.stream.writeln()
        self.stream.writeln(self.separator1)
        self.stream.writeln(">>> %s" % (self.getDescription(test)))
        self.stream.writeln(self.separator2)
        self.stream.writeln(self._exc_info_to_string(err, test).rstrip())
        self.stream.writeln(self.separator1)

        pdb.post_mortem(tb)

    def addFailure(self, test, err):
        super(ExceptionTestResultMixin, self).addFailure(test, err)
        exctype, value, tb = err

        self.stream.writeln()
        self.stream.writeln(self.separator1)
        self.stream.writeln(">>> %s" % (self.getDescription(test)))
        self.stream.writeln(self.separator2)
        self.stream.writeln(self._exc_info_to_string(err, test).rstrip())
        self.stream.writeln(self.separator1)

        # It would be good if we could make sure we're in the correct frame here
        pdb.post_mortem(tb)


class PdbTestResult(ExceptionTestResultMixin, unittest.TextTestResult):
    pass


class PdbTestRunner(unittest.TextTestRunner):
    """
    Override the standard DjangoTestRunner to instead drop into pdb on test errors/failures.
    """
    def _makeResult(self):
        return PdbTestResult(self.stream, self.descriptions, self.verbosity)


class PdbTestSuiteMixin(object):
    """
    Mixin to instead drop into pdb on test errors/failures.
    """
    def run_suite(self, suite, **kwargs):
        return PdbTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)


class XmlTestSuiteMixin(object):
    def run_suite(self, suite, **kwargs):
        return xmlrunner.XMLTestRunner(**kwargs).run(suite)


class TagTestSuiteMixin(object):
    def run_suite(self, suite, **kwargs):
        if self.tags or self.exclude_tags:
            suite = self.filter_by_tag(suite)
        return super(TagTestSuiteMixin, self).run_suite(suite, **kwargs)

    def filter_by_tag(self, tests):
        """
        Filter test suite to only include tagged tests.
        """
        def tags_in(test, tags=[]):
            return [tag in getattr(test.__class__, 'tags', []) for tag in tags]

        suite = unittest.TestSuite()
        for test in tests:
            if hasattr(test, '__iter__'):
                suite.addTest(self.filter_by_tag(test))
            else:
                if any(tags_in(test, self.tags)) or not self.tags:
                    if not any(tags_in(test, self.exclude_tags)):
                        suite.addTest(test)
        return suite
