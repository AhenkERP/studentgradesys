"""
Django settings for StudentGradeSystem project.
"""

from pathlib import Path
import environ
import os


# set BASE_DIR to the root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# set env to read from .env file
env = environ.Env(DEBUG=(bool, False))

# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# set ALLOWED_HOSTS to the list of hosts/domain names that this Django site can serve
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS') 

# set CSRF_TRUSTED_ORIGINS to the list of trusted origins for CSRF
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

# set CORS_ALLOWED_ORIGINS to the list of origins that are authorized to make cross-site HTTP requests
# CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS') 

# set CORS_ALLOW_ALL_ORIGINS to True to allow all origins to make cross-site HTTP requests
CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    'home',
    'user',
    'accounts',
    'lesson',
    'grade',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'django_filters',
    'django_db_logger',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StudentGradeSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'StudentGradeSystem.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('SQL_DATABASE', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': env('SQL_USER', default=''),
        'PASSWORD': env('SQL_PASSWORD', default=''),
        'HOST': env('SQL_HOST', default='localhost'),
        'PORT': env('SQL_PORT', default='3306'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25

}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'AUTHORIZATION_URL': env('DOMAIN') + '/o/authorize/',
    'TOKEN_URL': env('DOMAIN') + '/o/token/',
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = env('STATIC_ROOT')

FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o760
FILE_UPLOAD_MAX_MEMORY_SIZE = 50000000

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USER_AGENTS_CACHE = None

SESSION_COOKIE_AGE = 1800
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

CSRF_FAILURE_VIEW = 'home.views.csrf_failure'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG

DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = 25
# DJANGO_DB_LOGGER_ENABLE_FORMATTER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'INFO',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'INFO'
        },
        'django.request': { # logging 500 errors to database
            'handlers': ['db_log'],
            'level': 'INFO', # ERROR
            'propagate': False,
        }
    }
}

