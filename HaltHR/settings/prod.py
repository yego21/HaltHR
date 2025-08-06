from .base import *
import dj_database_url

USE_CLOUDINARY = True

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "https://halthr.onrender.com/", ).split(",")
DATABASES = {
    'default': dj_database_url.parse(os.getenv("DATABASE_URL"))
}
print("DEBUG: ALLOWED_HOSTS env raw =", os.getenv("ALLOWED_HOSTS"))
print("DEBUG: ALLOWED_HOSTS parsed =", ALLOWED_HOSTS)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
}

STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
