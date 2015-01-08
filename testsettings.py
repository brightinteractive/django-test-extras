from distlib.version import NormalizedVersion
import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'test_extras',
    'test_app',
)

# Django 1.7's built-in migrations framework supersedes South
# See http://south.readthedocs.org/en/latest/releasenotes/1.0.html#library-migration-path
_current_version = NormalizedVersion(django.get_version())
_south_replaced_in_version = NormalizedVersion('1.7')
_south_supported_in_current_version = _current_version < _south_replaced_in_version
if _south_supported_in_current_version:
    INSTALLED_APPS += (
        'south',
    )

SECRET_KEY = 'stub-value-for-django'
