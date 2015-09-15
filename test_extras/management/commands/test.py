# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf import settings
from test_extras.testrunners import result_hook_wrap, CoverageTestSuiteWrapper, PdbTestSuiteMixin, XmlTestSuiteMixin, ProfileTestSuiteWrapper, TagTestSuiteMixin
from django.core.management.commands.test import Command as CoreCommand

import argparse
import os
import sys


class Command(CoreCommand):
    """
    Similar to Django's standard 'test' management command,
    except that it also adds support for:

    --coverage
    --pdb
    --xmlreports
    --profile
    --tags
    --headless
    """

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument(
            '-c', '--coverage', action='store',
            dest='coverage', default=None,
            choices=['text', 'html', 'xml'],
            help='Coverage report; One of \'text\', \'html\', \'xml\''),
        parser.add_argument(
            '--pdb', action='store_true', dest='pdb',
            default=False,
            help='Drop into pdb on test failure.'),
        parser.add_argument(
            '-x', '--xmlreports', action='store_true',
            dest='xmlreports', default=False,
            help='Tells Django to store xml reports of the tests for Jenkins to use.'),
        parser.add_argument(
            '-f', '--profile', action='store_true',
            dest='profile', default=False,
            help='Profile tests.'),
        parser.add_argument(
            '-g', '--tags', action='store', dest='tags', default=None,
            help='Comma separated list of taGs to be tested. '
                 'Only tests that meet at least one of those tags '
                 'will be run.'),
        parser.add_argument(
            '-e', '--exclude-tags', action='store', dest='exclude_tags',
            default=None,
            help='Comma separated list of tags to not be tested. '
                 'Exclusion takes priority over inclusion. The list of '
                 'tags can also be specified in a setting '
                 '(TEST_EXCLUDE_TAGS). If both are '
                 'given, the command line options supersede the setting'),
        parser.add_argument(
            '-n', '--no-exclude', action='store_true',
            dest='no_exclude', default=False,
            help='Ignore tag exclusions from setting or command line'),
        parser.add_argument(
            '--headless', action='store_true',
            dest='headless', default=False,
            help='Start a virtual display, to facilitate running Selenium tests on virtual servers. Requires pyvirtualdisplay.'),
        parser.add_argument(
            '--no-exit', action='store_true',
            dest='no_exit', default=False,
            help="Don't call sys.exit(), useful if you're running with management.call_command()"),
        parser.add_argument(
            '--dump-options', action='store_true',
            # Only intended to be used by the django-test-extras automated test OptionParsingTests, so don't show in help
            help=argparse.SUPPRESS)

    def handle(self, *test_labels, **options):
        if options['dump_options']:
            # Dump the parsed options and then exit without running tests
            self.stdout.write(repr(options))
            return

        from django.test.utils import get_runner

        TestRunner = get_runner(settings)

        TestRunner = result_hook_wrap(TestRunner)

        if options['pdb'] and options['xmlreports']:
            from optparse import OptionError
            raise OptionError("--pdb, -x", "cannot have pdb and xmlreports specified")

        if options['pdb']:
            TestRunner = self.pdb_wrap(TestRunner)

        if options['xmlreports']:
            TestRunner = self.xml_wrap(TestRunner)

        if options['tags'] or self.have_tag_exclusions(options):
            exclusions = None
            if self.have_tag_exclusions(options) and not options['no_exclude']:
                exclusions = options.get('exclude_tags') or ','.join(
                    getattr(settings, 'TEST_EXCLUDE_TAGS'), [])
            TestRunner = self.tag_wrap(TestRunner, options.get('tags'),
                                       exclusions)

        if options['coverage']:
            TestRunner = self.coverage_wrap(TestRunner, options['coverage'])

        if options['profile']:
            TestRunner = self.profile_wrap(TestRunner)

        if options['headless']:
            self.start_headless_display()

        self._core_handle(TestRunner, *test_labels, **options)

    def have_tag_exclusions(self, options):
        return bool(options['exclude_tags'] or getattr(settings, 'TEST_EXCLUDE_TAGS', None))

    def profile_wrap(self, Runner):
        class ProfileTestSuiteRunner(ProfileTestSuiteWrapper):
            def __init__(self, *args, **kwargs):
                subject = Runner(*args, **kwargs)
                super(ProfileTestSuiteRunner, self).__init__(subject, *args, **kwargs)
        return ProfileTestSuiteRunner

    def coverage_wrap(self, Runner, report_type):
        class CoverageTestSuiteRunner(CoverageTestSuiteWrapper):
            def __init__(self, *args, **kwargs):
                subject = Runner(*args, **kwargs)
                super(CoverageTestSuiteRunner, self).__init__(subject, report_type, *args, **kwargs)
        return CoverageTestSuiteRunner

    def pdb_wrap(self, Runner):
        class PdbTestSuiteRunner(PdbTestSuiteMixin, Runner):
            pass
        return PdbTestSuiteRunner

    def xml_wrap(self, Runner):
        class XmlTestSuiteRunner(XmlTestSuiteMixin, Runner):
            pass
        return XmlTestSuiteRunner

    def tag_wrap(self, Runner, test_tags, test_exclude_tags):
        class TagTestRunner(TagTestSuiteMixin, Runner):
            tags = test_tags.split(',') if test_tags else []
            exclude_tags = test_exclude_tags.split(',') if test_exclude_tags else []
        return TagTestRunner

    def start_headless_display(self):
        # Import here instead of top of file so we don't depend on
        # pyvirtualdisplay unless the headless option isn't used.
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    def _core_handle(self, TestRunner, *test_labels, **options):
        """ Copied from django.core.management.commands.test (1.4)"""
        options['verbosity'] = int(options.get('verbosity'))

        if options.get('liveserver') is not None:
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options['liveserver']
            del options['liveserver']

        test_runner = TestRunner(**options)
        failures = test_runner.run_tests(test_labels)

        if failures and not options['no_exit']:
            sys.exit(bool(failures))
