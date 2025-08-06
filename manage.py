#!/usr/bin/env python
import os
import sys
from pathlib import Path
import environ

def main():
    BASE_DIR = Path(__file__).resolve().parent
    env = environ.Env()
    environ.Env.read_env(BASE_DIR / '.env')

    django_env = env('DJANGO_ENV', default='dev')  # local default
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'HaltHR.settings.{django_env}')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
