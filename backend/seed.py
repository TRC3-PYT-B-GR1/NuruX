"""Explicit local demo reset utility.

Usage from backend/:
    python seed.py --reset

The command intentionally has no default password and never prints tokens.
"""

import argparse
import getpass
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management import call_command


def main():
    parser = argparse.ArgumentParser(description='Reset local data and create one NuruX administrator.')
    parser.add_argument('--reset', action='store_true', help='Required acknowledgement that all data will be deleted.')
    parser.add_argument('--username', default='admin')
    parser.add_argument('--email', default='admin@nurux.local')
    args = parser.parse_args()

    if not args.reset:
        parser.error('--reset is required because this command deletes all application data.')
    confirmation = input('Type RESET NURUX to delete all local application data: ')
    if confirmation != 'RESET NURUX':
        raise SystemExit('Reset cancelled.')

    password = os.getenv('NURUX_SEED_ADMIN_PASSWORD') or getpass.getpass('New admin password: ')
    validate_password(password)

    call_command('flush', interactive=False)
    user_model = get_user_model()
    user_model.objects.create_superuser(
        username=args.username,
        email=args.email,
        password=password,
        first_name='System',
        last_name='Administrator',
        role='super_admin',
    )
    print(f'Created administrator {args.username!r}. No token was generated.')


if __name__ == '__main__':
    main()
