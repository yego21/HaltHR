import os
from pathlib import Path
import environ
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

django_env = env('DJANGO_ENV', default='prod')  # default prod for safety
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'HaltHR.settings.{django_env}')

application = get_wsgi_application()
