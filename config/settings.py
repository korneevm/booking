# -*- coding: utf-8 -*-
import os
from os.path import join
from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Common(Configuration):

    # Application definition

    DJANGO_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
    )

    THIRD_PARTY_APPS = (
        'crispy_forms',  # Form layouts
        'floppyforms',
        'djcelery',
        'pytils',
        'constance',
        'constance.backends.database',
        'bootstrapform',
        'allauth',  # registration
        'allauth.account',  # registration
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'users',
        'startups',
        'booking',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = "CHANGEME!!!"

    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )

    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')

    ADMINS = (
        ('Mikhael Korneev', 'korneevm@gmail.com'),
    )

    MANAGERS = ADMINS

    TIME_ZONE = 'Europe/Moscow'

    LANGUAGE_CODE = 'ru-ru'

    SITE_ID = 1

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False

    ROOT_URLCONF = 'config.urls'

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

    # CELERY CONFIGURATION
    BROKER_URL = 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ALWAYS_EAGER = False
    CELERY_TIMEZONE = 'Europe/Moscow'
    CELERY_ENABLE_UTC = False

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.template.context_processors.request',
                    "allauth.account.context_processors.account",
                    'django.contrib.messages.context_processors.messages',
                    'constance.context_processors.config',
                ],
            },
        },
    ]

    CRISPY_TEMPLATE_PACK = 'bootstrap3'

    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    MEDIA_ROOT = join(BASE_DIR, '../media')

    MEDIA_URL = '/media/'

    WSGI_APPLICATION = 'config.wsgi.application'

    SITE_NAME = 'accel-propusk.iidf.ru'
    SITE_URL = 'localhost:8000'

    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    #ACCOUNT_EMAIL_VERIFICATION = 'optional'
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    ACCOUNT_LOGOUT_ON_GET = True
    #ACCOUNT_ADAPTER = 'registration.views.AccountAdapter'
    #SOCIALACCOUNT_QUERY_EMAIL = True
    #SOCIALACCOUNT_EMAIL_REQUIRED = True
    #SOCIALACCOUNT_AUTO_SIGNUP = True
    ACCOUNT_EMAIL_VERIFICATION = 'none'

    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "index"
    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
    CONSTANCE_REDIS_CONNECTION = 'redis://localhost:6379/0'
    CONSTANCE_CONFIG = {
        'PROFILE_BOOKING_CALENDAR_DAYS': (5, u'Количество дней для прокрутки в календаре при бронировании переговорки'),
        'ORDERS_EMAIL': ('reception2@bk.ru', u'E-mail, на который высылается информация о заказе пропусков'),
        'ORDERS_DAYS': (11, u'Количество дней наперед, доступные для заказа пропусков'),
        'BOOKING_HOURS': (2, u'Количество часов в день, доступное для бронирования переговорок, на стартап'),
    }


class Local(Common):
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    
    SITE_NAME = 'localhost:8000'

    INSTALLED_APPS = Common.INSTALLED_APPS

    DEFAULT_FROM_EMAIL = values.Value('Команда #tceh <noreply@tceh.com>')
    EMAIL_HOST = "localhost"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 1025
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    ADMIN_EMAILS = ['korneevm@gmail.com']

    MANDRILL_KEY = 'kd7IC8q0hA5K0PRZVLD51A'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../booking_local.sqlite3'),
        }
    }


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ("djangosecure", )

    SECRET_KEY = values.SecretValue(late_binding=True)

    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SESSION_COOKIE_SECURE = values.BooleanValue(False)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)

    ALLOWED_HOSTS = ["*"]

    DEFAULT_FROM_EMAIL = values.Value('<noreply@tceh.com>')
    EMAIL_HOST = values.Value('smtp.mandrillapp.com')
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="MANDRILL_API_KEY", late_binding=True)
    EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="MANDRILL_USERNAME", late_binding=True)
    EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT", late_binding=True)
    EMAIL_USE_TLS = True
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    ADMIN_EMAILS = ['korneevm@gmail.com']
    MANDRILL_KEY = values.SecretValue(environ_prefix="", environ_name="MANDRILL_API_KEY", late_binding=True)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../booking_production.sqlite3'),
        }
    }

