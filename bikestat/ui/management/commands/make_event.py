from optparse import make_option
import time

from django.core.management.base import BaseCommand
from django.db import connection

from ui.models import Event, Ride


class Command(BaseCommand):
    help = 'Extract events from loaded rides'

    option_list = BaseCommand.option_list + (
        make_option('--empty', action='store_true', default=False,
                    dest='empty', help='empty the events table first'),
    )

    def handle(self, *args, **options):
        if options.get('empty', False):
            print 'emptying out events table first'
            qs = Event.objects.all()
            print 'deleting %s event(s)' % qs.count()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM ui_event')
            cursor.execute('ALTER SEQUENCE ui_event_id_seq RESTART WITH 1')
            print 'done'
            # let me see that this happened before it scrolls away
            time.sleep(2)
        qs = Ride.objects.all()
        for ride in qs:
            event_start = Event(ride=ride, date=ride.date_start,
                                station=ride.station_start,
                                terminal=ride.terminal_start,
                                bike_num=ride.bike_num)
            event_start.save()
            event_end = Event(ride=ride, date=ride.date_end,
                              station=ride.station_end,
                              terminal=ride.terminal_end,
                              bike_num=ride.bike_num, is_end=True)
            event_end.save()
