"""
Django settings for milk project.
Ready for deployment on Vercel.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------
# SECRET KEY
# -----------------------------------------------------
SECRET_KEY = 'django-insecure-5!)vl&mlz$y4ep4gd1nm-4a3t-5n@zc4a-6$t7)p*qhj5tu##2'

# -----------------------------------------------------
# DEBUG MODE (Auto-switch on Vercel)
# -----------------------------------------------------
DEBUG = os.getenv("VERCEL") != "1"

# -----------------------------------------------------
# ALLOWED HOSTS
# -----------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [
        ".vercel.app",
        "localhost",
        "127.0.0.1",
    ]

# -----------------------------------------------------
# INSTALLED APPS
# -----------------------------------------------------
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',  # Needed for static files in local development
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'milkmain',
]

# -----------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Required for Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'milk.urls'

# -----------------------------------------------------
# TEMPLATES
# -----------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'milk.wsgi.application'

# -----------------------------------------------------
# DATABASE (SQLite)
# -----------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------
# STATIC FILES (VERY IMPORTANT FOR VERCEL)
# -----------------------------------------------------
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# -----------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
