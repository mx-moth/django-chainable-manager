# Django settings for test_project project.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

SITE_ID = 1

SECRET_KEY = 'rsq&amp;9q1#dw&amp;74yd7!1ikpg9ai1a378h76cem*t!xx=($x%j^_-'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chainablemanager',
)
