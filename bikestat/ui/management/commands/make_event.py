from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import connection

from ui.models import Event


class Command(BaseCommand):
    help = 'Extract events from loaded rides'

    option_list = BaseCommand.option_list + (
        make_option('--empty', action='store_true', default=False,
                    dest='empty', help='empty the events table first'),
    )

    def handle(self, *args, **options):
        cursor = connection.cursor()
        if options.get('empty', False):
            print 'deleting %s events' % Event.objects.count()
            cursor.execute('DELETE FROM ui_event')
            cursor.execute('ALTER SEQUENCE ui_event_id_seq RESTART WITH 1')
        cursor.execute('''
            INSERT INTO ui_event
                (ride_id, date, station_id, bike_id, is_end)
            SELECT id, date_start, station_start_id, bike_id, FALSE
            FROM ui_ride
            UNION ALL
            SELECT id, date_end, station_end_id, bike_id, TRUE
            FROM ui_ride
            ''')
        print 'inserted %s events' % Event.objects.count()
