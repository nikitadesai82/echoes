import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hhs+(l=5mj8wnmd5idf8aa*#(hyi+!n3s4lxdda^3=#h(1)yfy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "sparkdesignstudio.co.in",
    "www.sparkdesignstudio.co.in","echoesofnature.co.in",
    "www.echoesofnature.co.in"
]
CSRF_TRUSTED_ORIGINS = [
    "https://sparkdesignstudio.co.in",
"https://www.sparkdesignstudio.co.in",
    "https://echoesofnature.co.in",
    "https://www.echoesofnature.co.in",
]

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eonapp',
                'import_export','storages',
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

ROOT_URLCONF = 'eon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'echo',
        'USER': 'admin',
        'PASSWORD': 'mythadmin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
from django.utils import timezone

TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
USE_I18N = True
USE_L10N = True



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



AWS_ACCESS_KEY_ID = "DO801BLZ8UBMN2F4L27Z"
AWS_SECRET_ACCESS_KEY = "Coh6ze8eJXtiMaIDXxS0Qr5DrgJv4TvrILKzwRnssKk"

AWS_STORAGE_BUCKET_NAME = "hoh-data"
AWS_S3_ENDPOINT_URL = "https://sfo3.digitaloceanspaces.com"
AWS_S3_CUSTOM_DOMAIN = "hoh-data.sfo3.cdn.digitaloceanspaces.com"

AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_STATIC_LOCATION = "static"
AWS_MEDIA_LOCATION = "media"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": AWS_MEDIA_LOCATION,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": AWS_STATIC_LOCATION,
        },
    },
}

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
