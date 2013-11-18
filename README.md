Django Test Extras
==================

**Enhancements for the Django test command and testing utility code.**

**Author:** [Bright Interactive][1].

Adding to your Django Project
=============================

Requires Django 1.4 (might work with 1.3, not tested).

Add test\_extras to your INSTALLED_APPS. Run "./manage test --help" for help
on the new options provided.

Publishing releases to PyPI
===========================

To publish a new version of django-test-extras app to PyPI, set the
`__version__` string in `test_extras/__init__.py`, then run:

    # Run the tests against multiple environments
    tox
    # Publish to PyPI
    ./setup.py publish
    # Tag (change 1.0.0 to the version you are publishing!)
    git tag -a v1.0.0 -m 'version 1.0.0'
    git push --tags

Running the tests
=================

To run the tests against the current environment:

    ./manage.py test

To run the tests against multiple environments, install `tox` using
`pip install tox`, make sure you're not currently in a virtual environment,
then simply run `tox`:

    tox
    
Contact
=======

Join us in #brightinteractive on irc.freenode.net.

Changelog
=========

1.1.1
-----
* Fix data restore in Django 1.5/1.6 in DataPreservingTransactionTestCaseMixin
* Declare dependencies in setup.py

1.1.0
-----
* Add --no-exit option
* Change short option names to avoid conflicts with new Django 1.6 options. This is a breaking change - if you were using `-t` you should now use `--tags` instead and if you were using `-p` you should now use `--pdb` instead.

1.0.11
------
* Python 2.7 compatibility fix
* Allow test classes to hook addSuccess, addError and addFailure

1.0.10
------
* Fix tag inclusion/exclusion options not working if '-x' is also specified

1.0.0
-----

* Initial release

License
=======

Copyright (c) Bright Interactive Limited.
Started with django-reusable-app Copyright (c) DabApps.

All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[1]: http://www.bright-interactive.com/
