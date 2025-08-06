from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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
    'CLOUD_NAME': "dgee7iare",
    'API_KEY': "663622885671187",
    'API_SECRET': "K8dRpvBHgWdzqhTH1i8uq9pOLNE",
}