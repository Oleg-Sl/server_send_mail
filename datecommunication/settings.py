"""
Django settings for datecommunication project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#u-tk!zdn&es#h8+mtic+=-feucxq&7h84#4+fgi)c@lu*s-lo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['*']
# if DEBUG:
#     ALLOWED_HOSTS = []
# else:
#     ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djoser',
    'rest_framework',
    'django_filters',
    'corsheaders',
    
    # 'djoser',
    # 'rest_framework',
    'rest_framework_simplejwt',

    'statisticsapp',
    'cashflowapp',
    'activityapp',
    'api_v1',
    'api_v2',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    


]

ROOT_URLCONF = 'datecommunication.urls'

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

WSGI_APPLICATION = 'datecommunication.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'NAME': 'statistics_communication',
#             'ENGINE': 'django.db.backends.postgresql',
#             'USER': 'aton',
#             'PASSWORD': 'dl80Jfr3jDcYk79s2',
#             'HOST': '127.0.0.1',
#             'PORT': '5432',
#         }
#     }
DATABASES = {
        'default': {
            'NAME': 'statistics_communication',
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'aton',
            'PASSWORD': 'dl80Jfr3jDcYk79s2',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_URL = ''

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = '/home/atonlab/projects/aton_statistics/datecommunication/static'
# D:\Main projects\aton_statistic\datecommunication\datecommunication\wsgi.py


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


CORS_ORIGIN_WHITELIST = [
    "https://atonlab.bitrix24.ru",
    # "https://atonlab.bitrix24.ru/marketplace/app/199/",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://37.193.133.164",
    "https://37.193.133.164",
    "https://cdn-ru.bitrix24.ru",
]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['*']

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    # 'ACCESS_TOKEN_LIFETIME': datetime.timedelta(seconds=30),
    # 'ACCESS_TOKEN_LIFETIME': datetime.timedelta(seconds=20),
    # 'REFRESH_TOKEN_LIFETIME': datetime.timedelta(seconds=60),
    'ROTATE_REFRESH_TOKENS': True,
    # 'AUDIENCE': [],
    # 'JWT_ALLOW_REFRESH': True,
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=1),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(seconds=7),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    # 'SERIALIZERS': {},
    'TOKEN_MODEL': None,
}