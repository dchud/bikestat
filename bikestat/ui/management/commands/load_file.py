from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load a single bikeshare data file'

    def handle(self, *args, **options):
        print args
