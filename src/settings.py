import os

RECAPTCHA_PRIVATE_KEY='6LcD9MQSAAAAAAD26iRITwm083gElTsK-Ep3d3g6'

# Django settings for mysite project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Gloria W', 'strangest@comcast.net'),
)

MANAGERS = ADMINS

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AUTHENTICATION_BACKENDS = ('custom_auth.custom_auth.EmailOrUsernameModelBackend',)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pygotham',# Or path to database file if using sqlite3.
        'USER': 'pygotham',                      # Not used with sqlite3.
        'PASSWORD': 'see_local_settings_file',              # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5200',                      # Set to empty string for default. Not used with sqlite3.
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': '/apps/pygotham/src/sqlite_file',# Or path to database file if using sqlite3.
        #'USER': '',                      # Not used with sqlite3.
        #'PASSWORD': '',              # Not used with sqlite3.
        #'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://pygotham.org'
SSL_MEDIA_URL = 'https://pygotham.org'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'../static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'see local_settings'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.csrf',
    'django.core.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'accept_middleware.accept_header_parse.AcceptMiddleware',
)

ROOT_URLCONF = 'urls'
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'templates'),
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.csrf',
    'registration',
    'profiles',
    'captcha',
    'confreg',
    'talksub',
    'talkvote',
    'pygmail',
    'mailer',
    'custom_email_backend',
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
# One-week activation window; you may, of course, use a different value.

MAX_PAID = 350
MAX_SPONSORED = 30

ACCOUNT_ACTIVATION_DAYS = 1
LOGIN_REDIRECT_URL = '/confreg/user_state'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH='/tmp/email/'

#EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND='custom_email_backend.logging_smtp.LoggingSmtp'

EMAIL_FILE_PATH = os.path.join(os.path.dirname(__file__),'emaildata')
EMAIL_HOST='smtp-auth.no-ip.com'
EMAIL_HOST_PASSWORD='see_local_settings_file'
EMAIL_HOST_USER='pygotham@thepeoplesconference.com'
EMAIL_PORT=25
DEFAULT_FROM_EMAIL = "pygotham@thepeoplesconference.com"
SERVER_EMAIL = "pygotham@thepeoplesconference.com"
EMAIL_SUBJECT_PREFIX='Pygotham Site: '
EMAIL_USE_TLS=True
EMAIL_DEBUG=True
SEND_BROKEN_LINK_EMAILS=True

"""Affects the global state of all PyGotham talks.
Not currently implemented.
    
Possible states of talks
(1) Not yet accepting talks
(2) Accepting talks
(3) Talks are locked (no additions/edits allowed)
(4) Talk voting is on
(5) Talk voting is complete
"""
TALK_STATE = 1

TALK_SUBMISSION_LIMIT_PER_PERSON = 3

from local_settings import *
