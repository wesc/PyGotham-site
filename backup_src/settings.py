import os

RECAPTCHA_PRIVATE_KEY='6LcD9MQSAAAAAAD26iRITwm083gElTsK-Ep3d3g6'

# Django settings for mysite project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Gloria W', 'pygotham@thepeoplesconference.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'pygotham',# Or path to database file if using sqlite3.
        #'USER': 'pygotham',                      # Not used with sqlite3.
        #'PASSWORD': '4ed5rf6tg7yh',              # Not used with sqlite3.
        #'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #'PORT': '5200',                      # Set to empty string for default. Not used with sqlite3.
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/apps/pygotham/src/sqlite_file',# Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',              # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
MEDIA_URL = 'https://pygotham.org'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

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
SECRET_KEY = 'g0--vl+z-iu*6wr3f-im$qi94y^58rxx_s6=3qymc64a@xq2c3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

TEMPLATE_DIRS = (
    "/app/pygotham/src/templates"
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
    'recaptcha',
    'pygmail',
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
# One-week activation window; you may, of course, use a different value.

ACCOUNT_ACTIVATION_DAYS = 1
LOGIN_REDIRECT_URL = '/'

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

EMAIL_FILE_PATH = os.path.join(os.path.dirname(__file__),'emaildata')
EMAIL_HOST='smtp-auth.no-ip.com'
EMAIL_HOST_PASSWORD='4ed5rf6tg7yh'
EMAIL_HOST_USER='pygotham@thepeoplesconference.com'
EMAIL_PORT=25
DEFAULT_FROM_EMAIL = "pygotham@thepeoplesconference.com"
SERVER_EMAIL = "pygotham@thepeoplesconference.com"
EMAIL_SUBJECT_PREFIX='Pygotham Site: '
EMAIL_USE_TLS=False
SEND_BROKEN_LINK_EMAILS=True
