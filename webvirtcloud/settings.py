"""
Django settings for webvirtcloud project.

"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'nu-(5y569wn(ak-3ar_t!9vf8gmg=3uh(q1sez+drb*o*f@512'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bootstrap3',
    'corsheaders',
    'computes',
    'console',
    'networks',
    'storages',
    'interfaces',
    'instances',
    'secrets',
    'logs',
    'accounts',
    'create',
)

#MIDDLEWARE_CLASSES = (
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# 跨域请求白名单
CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com',
    'localhost:8000',
    '127.0.0.1:9000'
)

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.RemoteUserBackend',
#     #'accounts.backends.MyRemoteUserBackend',
# )

LOGIN_URL = '/accounts/login'

ROOT_URLCONF = 'webvirtcloud.urls'

WSGI_APPLICATION = 'webvirtcloud.wsgi.application'

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(os.path.dirname(__file__), '..', 'webvirtmgr.sqlite3'),
        'NAME': 'webvirt',
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'jxkj123',
        'HOST': '127.0.0.1',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': 3306,  # Set to empty string for default.
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],}
    }
]

LANGUAGE_CODE = 'zh_hans'
LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local')
LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '..', 'locale'),
)
## WebVirtCloud settings

# Wobsock port
WS_PORT = 6080

# Websock host
WS_HOST = '0.0.0.0'

# Websock public port
WS_PUBLIC_HOST = None

# Websock SSL connection
WS_CERT = None

VNC_TOKENS_FILE = os.path.join(BASE_DIR, 'vnc_tokens')

# list of console types
QEMU_CONSOLE_TYPES = ['vnc', 'spice']

# default console type
QEMU_CONSOLE_DEFAULT_TYPE = 'vnc'

# list taken from http://qemu.weilnetz.de/qemu-doc.html#sec_005finvocation
QEMU_KEYMAPS = ['ar', 'da', 'de', 'de-ch', 'en-gb', 'en-us', 'es', 'et', 'fi',
                'fo', 'fr', 'fr-be', 'fr-ca', 'fr-ch', 'hr', 'hu', 'is', 'it',
                'ja', 'lt', 'lv', 'mk', 'nl', 'nl-be', 'no', 'pl', 'pt',
                'pt-br', 'ru', 'sl', 'sv', 'th', 'tr']

# keepalive interval and count for libvirt connections
LIBVIRT_KEEPALIVE_INTERVAL = 5
LIBVIRT_KEEPALIVE_COUNT = 5

ALLOW_INSTANCE_MULTIPLE_OWNER = True
NEW_USER_DEFAULT_INSTANCES = []
CLONE_INSTANCE_DEFAULT_PREFIX = 'instance'
LOGS_PER_PAGE = 100
QUOTA_DEBUG = True
ALLOW_EMPTY_PASSWORD = True
SHOW_ACCESS_ROOT_PASSWORD = False
SHOW_ACCESS_SSH_KEYS = False
SHOW_PROFILE_EDIT_PASSWORD = False
INSTANCE_VOLUME_DEFAULT_FORMAT = 'qcow2'
INSTANCE_VOLUME_DEFAULT_BUS = 'virtio'
INSTANCE_VOLUME_DEFAULT_CACHE = 'directsync'

