from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.common.models import AppVersion


class Command(BaseCommand):
    help = 'Create or update the externally hosted Android release advertised by NuruX.'

    def add_arguments(self, parser):
        parser.add_argument('--version-code', type=int, required=True)
        parser.add_argument('--version-name', required=True)
        parser.add_argument('--download-url', required=True)
        parser.add_argument('--release-notes', default='')
        parser.add_argument('--mandatory', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        if options['version_code'] < 1:
            raise CommandError('--version-code must be a positive integer.')

        version = AppVersion.objects.filter(
            version_code=options['version_code'],
        ).first() or AppVersion(version_code=options['version_code'])
        version.version_name = options['version_name'].strip()
        version.download_url = options['download_url'].strip()
        version.release_notes = options['release_notes'].strip()
        version.is_mandatory = options['mandatory']
        version.full_clean()
        version.save()

        self.stdout.write(self.style.SUCCESS(
            f'Published Android version {version.version_name} '
            f'({version.version_code}) at {version.download_url}'
        ))
