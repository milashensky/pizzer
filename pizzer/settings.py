import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_NAME = os.path.basename(BASE_DIR)
STORAGE_ROOT = os.path.join(BASE_DIR, '..', 'storage')
MEDIA_ROOT = os.path.join(STORAGE_ROOT, 'media')

MEDIA_URL = ''

SECRET_KEY = '2rk&9(nmg^rbhj+3t60*o-hn*17-ktu3zsu%wt3-cv0*au_dt+'

DEBUG = False
DEBUG_TOOLBAR = False
ALLOWED_HOSTS = ['*']
ANONYMOUS_USER_ID = -1


SERIALIZATION_MODULES = {
    'json': 'common.json'
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalogue',
    'common',
    'shop'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pizzer.urls'

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

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.vk.VKOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'django.contrib.auth.backends.AllowAllUsersRemoteUserBackend',
)

WSGI_APPLICATION = 'pizzer.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

###########################
# Load LOCAL_SETTINGS
###########################
try:
    from types import ModuleType
    import local_settings
    for key in dir(local_settings):
        value = getattr(local_settings, key)
        if not key.startswith('__') and not isinstance(value, ModuleType):
            globals()[key] = value
except ImportError:
    raise
