DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'test_extras',
    'test_app',
    'south',
)

SECRET_KEY = 'stub-value-for-django'
