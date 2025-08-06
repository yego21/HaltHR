from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

USE_CLOUDINARY = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET')
}

# STORAGES = {
#     'default': {
#         'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
#     },
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
#     },
# }


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}









